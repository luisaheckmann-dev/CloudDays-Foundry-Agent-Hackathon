import hashlib
import json
import sqlite3
import sys
from contextlib import closing
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from orderops.config import ROOT

POLICY_ID = "OPS-2026-11"
MAX_QUANTITY = 20


def inventory(sku):
    if not isinstance(sku, str) or not sku or len(sku) > 40:
        raise ValueError("SKU muss eine nichtleere Zeichenfolge sein.")
    data = json.loads((ROOT / "data" / "inventory.json").read_text(encoding="utf-8"))
    item = next((x for x in data["items"] if x["sku"] == sku), None)
    if item is None:
        return {"found": False, "sku": sku, "source": "data/inventory.json", "fixture": True}
    return {**item, "found": True, "source": "data/inventory.json",
            "fixture": True, "as_of": data["as_of"]}


@dataclass(frozen=True)
class Proposal:
    id: str
    sku: str
    quantity: int
    policy_id: str = POLICY_ID
    simulation: bool = True


def propose(sku, quantity):
    if type(quantity) is not int or not 1 <= quantity <= MAX_QUANTITY:
        raise ValueError(f"Menge muss eine ganze Zahl von 1 bis {MAX_QUANTITY} sein (kein bool/float).")
    item = inventory(sku)
    if not item["found"]:
        raise ValueError("Unbekannte SKU: kein Entwurf.")
    if item["blocked"]:
        raise ValueError("Produkt gesperrt: kein Entwurf.")
    if quantity > item["available"]:
        raise ValueError(f"Bestand unzureichend: nur {item['available']} verfügbar.")
    canonical = json.dumps([POLICY_ID, sku, quantity], separators=(",", ":"))
    proposal_id = hashlib.sha256(canonical.encode()).hexdigest()[:16]
    return Proposal(proposal_id, sku, quantity)


def save_approved(proposal, db_path, *, enabled=False, confirmation=""):
    """CLI trust boundary, never exposed as a model-callable function."""
    validated = propose(proposal.sku, proposal.quantity)
    if proposal != validated:
        raise ValueError("Manipulierter Entwurf.")
    if not enabled or confirmation != f"APPROVE {proposal.id}":
        return {"status": "denied", "simulation": True, "id": proposal.id}
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path, timeout=5)) as db:
        with db:
            db.execute("""CREATE TABLE IF NOT EXISTS drafts
                (id TEXT PRIMARY KEY, payload TEXT NOT NULL, approved_at TEXT NOT NULL)""")
            cursor = db.execute(
                "INSERT OR IGNORE INTO drafts VALUES (?, ?, ?)",
                (proposal.id, json.dumps(asdict(proposal)), datetime.now(timezone.utc).isoformat()),
            )
            inserted = cursor.rowcount == 1
    return {"status": "created" if inserted else "duplicate", "simulation": True,
            "id": proposal.id, "sku": proposal.sku, "quantity": proposal.quantity}


def approval_gate(proposal, db_path, *, enabled=False, read=None):
    print("LOKALE SIMULATION; KEINE BESTELLUNG:", json.dumps(asdict(proposal)))
    if not enabled:
        print("Schreibgate deaktiviert. Kein Entwurf gespeichert.")
        return save_approved(proposal, db_path)
    if read is None:
        if not sys.stdin.isatty():
            print("Keine interaktive Terminaleingabe; Freigabe über Pipe/Automation verweigert.")
            return save_approved(proposal, db_path)
        read = input
    try:
        confirmation = read(f"Nur lokal freigeben: APPROVE {proposal.id} (sonst Ablehnung): ")
    except (EOFError, KeyboardInterrupt):
        confirmation = ""
    return save_approved(proposal, db_path, enabled=True, confirmation=confirmation)
