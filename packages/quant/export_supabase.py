"""Read-only Supabase reference quote exporter. Never writes to the database."""
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

COLUMNS = ("quote_key,brand_label,model_label,capacity_gb,amount_cny,"
           "quote_type,source_url,source_date,precise_variant_confirmed,"
           "eligible_for_verified_chart")
def fetch_quotes():
    url = os.environ["SUPABASE_URL"].rstrip("/")
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    if not url.startswith("https://"):
        raise ValueError("SUPABASE_URL must use HTTPS")
    rows = []
    offset = 0
    while True:
        query = urllib.parse.urlencode({"select": COLUMNS, "order": "quote_key.asc",
                                       "limit": 1000, "offset": offset})
        req = urllib.request.Request(url + "/rest/v1/radar_reference_quotes?" + query,
            headers={"apikey": key, "Authorization": "Bearer " + key,
                     "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as response:
            batch = json.load(response)
        if not isinstance(batch, list):
            raise ValueError("Unexpected Supabase response")
        rows.extend(batch)
        if len(batch) < 1000:
            return rows
        offset += len(batch)

def normalize(rows):
    """Conservative mapping: no speculative SKU/condition inference."""
    result = []
    for row in rows:
        item = dict(row)
        item["canonical_sku"] = None
        item["condition_bucket"] = None
        result.append(item)
    return result

if __name__ == "__main__":
    target = Path("data/quotes.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    records = normalize(fetch_quotes())
    target.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Fetched reference rows:", len(records))
