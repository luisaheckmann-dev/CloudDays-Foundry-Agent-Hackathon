import hashlib
import json
import shutil
import sqlite3
import unittest
import uuid
from contextlib import closing
from dataclasses import replace
from unittest.mock import patch

from orderops.business import approval_gate, inventory, propose, save_approved
from orderops.config import LOCAL, ROOT
from orderops.tools import Dispatcher, definitions


class BusinessTests(unittest.TestCase):
    def setUp(self):
        self.work = LOCAL / ("unittest-" + uuid.uuid4().hex)
        self.work.mkdir(parents=True)
        self.addCleanup(shutil.rmtree, self.work)
        self.db = self.work / "drafts.sqlite3"

    def test_inventory_read_only(self):
        path = ROOT / "data" / "inventory.json"
        before = path.read_bytes()
        self.assertEqual(inventory("CD-100")["available"], 12)
        self.assertTrue(inventory("CD-100")["fixture"])
        self.assertFalse(inventory("CD-999")["found"])
        self.assertEqual(path.read_bytes(), before)

    def test_invalid_sku_type(self):
        for value in (None, {}, "", "x" * 41):
            with self.subTest(value=value), self.assertRaises(ValueError):
                inventory(value)

    def test_quantity_types_and_boundaries(self):
        for quantity in (True, False, 2.0, "2", 0, -1, 21, 1000000, None):
            with self.subTest(quantity=quantity), self.assertRaises(ValueError):
                propose("CD-300", quantity)
        self.assertEqual(propose("CD-300", 20).quantity, 20)
        self.assertEqual(propose("CD-100", 1).quantity, 1)

    def test_unknown_insufficient_and_blocked(self):
        for sku, quantity in (("CD-999", 1), ("CD-200", 4), ("CD-400", 1)):
            with self.subTest(sku=sku), self.assertRaises(ValueError):
                propose(sku, quantity)

    def test_gate_requires_flag_and_exact_human_confirmation(self):
        p = propose("CD-100", 2)
        for enabled, text in ((False, f"APPROVE {p.id}"), (True, "yes"),
                              (True, "APPROVE other"), (True, ""),
                              (True, f"APPROVE {p.id}\n"), (True, f"approve {p.id}"),
                              (True, f" APPROVE {p.id}"), (True, f"APPROVE {p.id} ")):
            result = save_approved(p, self.db, enabled=enabled, confirmation=text)
            self.assertEqual(result["status"], "denied")
            self.assertFalse(self.db.exists())

    def test_approval_is_idempotent_and_does_not_change_stock(self):
        p = propose("CD-100", 2)
        self.assertEqual(p.id, propose("CD-100", 2).id)
        self.assertNotEqual(p.id, propose("CD-100", 3).id)
        for expected in ("created", "duplicate"):
            self.assertEqual(save_approved(p, self.db, enabled=True,
                                          confirmation=f"APPROVE {p.id}")["status"], expected)
        with closing(sqlite3.connect(self.db)) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM drafts").fetchone()[0], 1)
            self.assertTrue(json.loads(db.execute("SELECT payload FROM drafts").fetchone()[0])["simulation"])
        self.assertEqual(inventory("CD-100")["available"], 12)

    def test_tampering_rejected(self):
        p = propose("CD-100", 2)
        for changed in (replace(p, quantity=3), replace(p, sku="CD-300"),
                        replace(p, policy_hash="0" * 64), replace(p, simulation=False)):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                save_approved(changed, self.db, enabled=True, confirmation=f"APPROVE {p.id}")
        self.assertFalse(self.db.exists())

    def test_policy_hash_matches_current_source(self):
        source = ROOT / "data" / "policy" / "order-policy-2026-11.txt"
        self.assertEqual(propose("CD-100", 2).policy_hash,
                         hashlib.sha256(source.read_bytes()).hexdigest())

    def copy_business_fixtures(self):
        (self.work / "data" / "policy").mkdir(parents=True)
        for parts in (("inventory.json",), ("policy", "order-policy-2026-11.txt")):
            shutil.copyfile((ROOT / "data").joinpath(*parts),
                            (self.work / "data").joinpath(*parts))

    def test_changed_policy_invalidates_staged_proposal(self):
        self.copy_business_fixtures()
        with patch("orderops.business.ROOT", self.work):
            original = propose("CD-100", 2)
            source = self.work / "data" / "policy" / "order-policy-2026-11.txt"
            source.write_bytes(source.read_bytes() + b"\nSynthetic test policy revision.\n")
            current = propose("CD-100", 2)
            self.assertNotEqual(original.policy_hash, current.policy_hash)
            self.assertNotEqual(original.id, current.id)
            with self.assertRaises(ValueError):
                save_approved(original, self.db, enabled=True,
                              confirmation=f"APPROVE {original.id}")
        self.assertFalse(self.db.exists())

    def test_stock_and_block_are_revalidated_before_write(self):
        self.copy_business_fixtures()
        with patch("orderops.business.ROOT", self.work):
            original = propose("CD-100", 2)
            path = self.work / "data" / "inventory.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            for available, blocked in ((1, False), (12, True)):
                data["items"][0].update(available=available, blocked=blocked)
                path.write_text(json.dumps(data), encoding="utf-8")
                with self.subTest(available=available, blocked=blocked), self.assertRaises(ValueError):
                    save_approved(original, self.db, enabled=True,
                                  confirmation=f"APPROVE {original.id}")
        self.assertFalse(self.db.exists())

    def test_denial_does_not_modify_existing_database(self):
        original = propose("CD-100", 2)
        save_approved(original, self.db, enabled=True, confirmation=f"APPROVE {original.id}")
        before = self.db.read_bytes()
        other = propose("CD-100", 3)
        self.assertEqual(save_approved(other, self.db, enabled=True,
                                       confirmation="yes")["status"], "denied")
        self.assertEqual(self.db.read_bytes(), before)

    def test_eof_denies(self):
        def closed(_):
            raise EOFError
        self.assertEqual(approval_gate(propose("CD-100", 2), self.db,
                                       enabled=True, read=closed)["status"], "denied")
        self.assertFalse(self.db.exists())

    def test_piped_approval_denied(self):
        with patch("orderops.business.sys.stdin.isatty", return_value=False):
            self.assertEqual(approval_gate(propose("CD-100", 2), self.db,
                                           enabled=True)["status"], "denied")
        self.assertFalse(self.db.exists())

    def test_unregistered_write_and_approval_injection_rejected(self):
        dispatcher = Dispatcher()
        bad = [
            ("save_approved", '{"sku":"CD-100","quantity":2}'),
            ("propose_order", '{"sku":"CD-100","quantity":2,"approved":true}'),
            ("get_inventory", '{"sku":"CD-100","shell":"read .env"}'),
            ("propose_order", "not-json"),
            ("propose_order", "[]"),
            ("propose_order", '{"sku":"CD-100","quantity":true}'),
            ("get_inventory", "x" * 4097),
        ]
        for name, args in bad:
            with self.subTest(name=name, args=args[:40]):
                self.assertEqual(json.loads(dispatcher.execute(name, args))["status"], "rejected")
        self.assertFalse(dispatcher.pending)
        self.assertFalse(self.db.exists())

    def test_proposal_only_in_memory_and_duplicate_collapsed(self):
        dispatcher = Dispatcher()
        for _ in range(2):
            result = json.loads(dispatcher.execute("propose_order", '{"sku":"CD-100","quantity":2}'))
            self.assertEqual(result["status"], "pending_human_approval")
        self.assertEqual(len(dispatcher.pending), 1)
        self.assertFalse(self.db.exists())

    def test_registered_tools_are_not_executable_deployments(self):
        tools = [tool.as_dict() for tool in definitions()]
        self.assertEqual([tool["name"] for tool in tools], ["get_inventory", "propose_order"])
        self.assertNotIn("save_approved", json.dumps(tools))
        self.assertTrue(all(tool["strict"] for tool in tools))

    def test_starter_todo_is_honest(self):
        # A participant may finish this TODO; either explicit TODO or correct result is acceptable.
        from starter.inventory import get_inventory
        try:
            result = get_inventory("CD-100")
        except NotImplementedError:
            return
        self.assertEqual(result["available"], 12)
