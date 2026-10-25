# Quant API security staging

This is a **standby implementation**, not a deployed endpoint. It intentionally returns 503 for data ingestion and result retrieval until a durable store and server-side rate limiter are wired.

- `QUANT_READ_TOKEN`: 32+ character secret, read-only access.
- `QUANT_WRITE_TOKEN`: separate 32+ character secret, GitHub Actions ingest.
- `ALLOWED_ORIGIN`: optional browser-origin check, **not** a substitute for authentication.
- Never put bearer tokens in a public browser app. A public frontend requires a session-bound backend proxy.
- Rate limiting must be enforced in shared infrastructure (Vercel WAF / Cloudflare WAF or durable KV/Redis); **do not** use process-local memory counters in serverless functions.
- Suggested policy: reads 30/min per authenticated principal plus 60/min per IP; writes 6/min per principal plus 10/min per IP, with burst controls. Return 429 and Retry-After.
- Fail closed until the rate limiter, result store, and identity layer are actually configured.
- Limit POST body to 64 KiB; validate schema, version, timestamp, and reject replay/duplicate submissions before enabling ingest.
- Do not bind this standalone API to the existing production domain until staging verification.
