import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from export_supabase import normalize

class ExportTests(unittest.TestCase):
    def test_no_invented_sku(self):
        row = {"quote_key": "X", "model_label": "unresolved", "amount_cny": 200}
        output = normalize([row])[0]
        self.assertIsNone(output["canonical_sku"])
        self.assertIsNone(output["condition_bucket"])
        self.assertEqual(output["amount_cny"], 200)
    def test_empty(self):
        self.assertEqual(normalize([]), [])

if __name__ == "__main__":
    unittest.main()
