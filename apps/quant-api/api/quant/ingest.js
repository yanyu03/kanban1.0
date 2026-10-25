import { authorize, fail, json } from './_security.js';
export default function handler(req,res){
  if(req.method!=='POST') return json(res,405,{error:'METHOD_NOT_ALLOWED'});
  if(!process.env.QUANT_WRITE_TOKEN) return fail(res,503);
  if(!authorize(req,process.env.QUANT_WRITE_TOKEN)) return fail(res,401);
  // Never claim successful ingest without durable storage.
  return json(res,503,{error:'RESULT_STORE_NOT_CONFIGURED'});
}
