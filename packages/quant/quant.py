"""Offline reference-price analysis. No database writes and no buy confirmation."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd

EXCLUDED = {"user_hypothesis", "promo_unresolved"}
REQUIRED = {"quote_key", "amount_cny", "quote_type", "source_date", "source_url", "precise_variant_confirmed"}

def analyze(records):
    df = pd.DataFrame(records)
    if df.empty:
        return {"status": "NO_INPUT_DATA", "input_rows": 0, "eligible_rows": 0, "signals": [], "model_version": "quant-kit-0.2.0"}
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
    df["amount_cny"] = pd.to_numeric(df["amount_cny"], errors="coerce")
    df["source_date"] = pd.to_datetime(df["source_date"], errors="coerce", utc=True)
    confirmed = df["precise_variant_confirmed"].fillna(False).eq(True)
    valid = df.loc[(df["amount_cny"] > 0) & df["source_date"].notna() & df["source_url"].notna() & confirmed & ~df["quote_type"].isin(EXCLUDED)].copy()
    for col, status in (("canonical_sku", "INSUFFICIENT_SKU_NORMALIZATION"), ("condition_bucket", "INSUFFICIENT_CONDITION_DATA")):
        if col not in valid.columns:
            return {"status": status, "input_rows": len(df), "eligible_rows": len(valid), "signals": [], "model_version": "quant-kit-0.2.0"}
        valid = valid.loc[valid[col].notna() & valid[col].astype(str).str.strip().ne("")].copy()
    valid = valid.drop_duplicates(subset=["quote_key"])
    signals = []
    for (sku, condition), group in valid.groupby(["canonical_sku", "condition_bucket"]):
        prices = group["amount_cny"].to_numpy(dtype=float)
        sources = int(group["source_url"].nunique())
        dates = int(group["source_date"].dt.date.nunique())
        q25, q75 = np.quantile(prices, [0.25, 0.75])
        sufficient = len(group) >= 5 and sources >= 2 and dates >= 2
        signals.append({"canonical_sku": str(sku), "condition_bucket": str(condition),
            "sample_count": int(len(group)), "distinct_source_urls": sources, "distinct_dates": dates,
            "median_reference_cny": round(float(np.median(prices)), 2),
            "q25_reference_cny": round(float(q25), 2), "q75_reference_cny": round(float(q75), 2),
            "status": "REFERENCE_RANGE_ONLY" if sufficient else "INSUFFICIENT_EVIDENCE",
            "buy_confirmed": False})
    return {"status": "OK", "input_rows": len(df), "eligible_rows": len(valid), "signals": signals, "model_version": "quant-kit-0.2.0"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", default="output/quant_results.json")
    args = parser.parse_args()
    rows = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError("Expected a JSON array")
    result = analyze(rows)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(result["status"], len(result["signals"]))
