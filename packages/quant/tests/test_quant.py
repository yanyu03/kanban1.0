import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quant import analyze

def quote(i, price=100, quote_type="channel_reference", sku="SSD-A"):
    return dict(quote_key=str(i), amount_cny=price, quote_type=quote_type,
        source_date=f"2026-10-{20+i%3:02d}", source_url=f"https://example.com/{i}",
        precise_variant_confirmed=True, canonical_sku=sku, condition_bucket="new")

class QuantTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(analyze([])["status"], "NO_INPUT_DATA")
    def test_median(self):
        s=analyze([quote(i, p) for i,p in enumerate([90,100,110,120,130])])["signals"][0]
        self.assertEqual(s["median_reference_cny"],110)
        self.assertEqual(s["status"],"REFERENCE_RANGE_ONLY")
        self.assertFalse(s["buy_confirmed"])
    def test_excluded(self):
        s=analyze([quote(0,100),quote(1,1,"user_hypothesis")])["signals"][0]
        self.assertEqual(s["sample_count"],1)
    def test_no_sku(self):
        q=quote(0);del q["canonical_sku"]
        self.assertEqual(analyze([q])["status"],"INSUFFICIENT_SKU_NORMALIZATION")
    def test_duplicate_key(self):
        self.assertEqual(analyze([quote(0),quote(0)])["signals"][0]["sample_count"],1)

if __name__=="__main__":
    unittest.main()
