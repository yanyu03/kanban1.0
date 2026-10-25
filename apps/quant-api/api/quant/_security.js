import { createHmac, timingSafeEqual } from 'node:crypto';
const json = (res, status, body) => { res.statusCode=status;res.setHeader('Content-Type','application/json; charset=utf-8');res.setHeader('Cache-Control','no-store');res.end(JSON.stringify(body)); };
export { json };
export function authorize(req, secret) {
  if (!secret || secret.length < 32) return false;
  const token = req.headers.authorization?.match(/^Bearer (.+)$/i)?.[1] ?? '';
  const a=createHmac('sha256',secret).update(token).digest();
  const b=createHmac('sha256',secret).update(secret).digest();
  return timingSafeEqual(a,b);
}
export function fail(res, status=401) { return json(res,status,{error:status===429?'RATE_LIMITED':status===503?'NOT_CONFIGURED':'UNAUTHORIZED'}); }
export function enforceOrigin(req) {
  const allowed=process.env.ALLOWED_ORIGIN;
  if(!allowed) return true;
  const origin=req.headers.origin;
  return !origin || origin===allowed;
}
