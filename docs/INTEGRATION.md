# Price Radar integration status

## GitHub Actions
- Runs unit tests and read-only NumPy/Pandas reference-price statistics.
- Requires GitHub Actions secrets: `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` to fetch real quotes.
- Secret key is used **only on GitHub runner**, never embedded in the Vercel frontend, committed files, or artifacts.
- No secrets configured: workflow falls back to an empty fixture, clearly reports `NO_INPUT_DATA`.
- No database writes; verified charts are untouched.
- Reference quotes lacking explicit canonical SKU or condition remain unclassified and cannot generate buy confirmations.

## Frontend migration
Existing Vercel deployment source retrieval returned truncated base64 data, so the frontend source is **not yet migrated**. Never commit partial HTML as complete source. Preserve production deployment.

## Next
1. Export full frontend source through original source repository or Vercel CLI.
2. Establish an explicit SKU/condition mapping registry, verified with source evidence.
3. Store versioned quant results separately from verified historical price points.
4. Backtest before enabling decision signals.
