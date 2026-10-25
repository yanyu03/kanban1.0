import { authorize, fail, json } from './_security.js';
export default function handler(req,res){
  if(req.method!=='GET') return json(res,405,{error:'METHOD_NOT_ALLOWED'});
  if(!process.env.QUANT_READ_TOKEN) return fail(res,503);
  if(!authorize(req,process.env.QUANT_READ_TOKEN)) return fail(res,401);
  return json(res,200,{service:'price-radar-quant',status:'STANDBY',resultsAvailable:false});
}
