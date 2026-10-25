import { authorize, fail, json, enforceOrigin } from './_security.js';
export default async function handler(req,res){
  if(req.method!=='GET') return json(res,405,{error:'METHOD_NOT_ALLOWED'});
  if(!enforceOrigin(req)) return fail(res,403);
  if(!process.env.QUANT_READ_TOKEN) return fail(res,503);
  if(!authorize(req,process.env.QUANT_READ_TOKEN)) return fail(res,401);
  // Fail closed until a persistent result backend is connected.
  return json(res,503,{error:'RESULT_STORE_NOT_CONFIGURED'});
}
