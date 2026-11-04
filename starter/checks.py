"""Run separately: python -m unittest starter.checks -v (initially RED by design)."""
import unittest

from starter.inventory import get_inventory


class ParticipantChecks(unittest.TestCase):
    def test_known_sku(self):
        self.assertEqual(get_inventory("CD-100")["available"], 12)

    def test_unknown_sku(self):
        self.assertFalse(get_inventory("CD-999")["found"])
