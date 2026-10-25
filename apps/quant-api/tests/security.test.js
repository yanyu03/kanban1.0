import test from 'node:test';
import assert from 'node:assert/strict';
import {authorize,enforceOrigin} from '../api/quant/_security.js';
const secret='0123456789abcdef0123456789abcdef';
test('valid token',()=>assert.equal(authorize({headers:{authorization:'Bearer '+secret}},secret),true));
test('invalid token',()=>assert.equal(authorize({headers:{authorization:'Bearer wrong'}},secret),false));
test('missing secret fails closed',()=>assert.equal(authorize({headers:{}},''),false));
test('short secret fails closed',()=>assert.equal(authorize({headers:{authorization:'Bearer abc'}},'abc'),false));
test('origin check is not authentication',()=>{
 const old=process.env.ALLOWED_ORIGIN;process.env.ALLOWED_ORIGIN='https://price.250221.xyz';
 try{assert.equal(enforceOrigin({headers:{origin:'https://evil.example'}}),false);assert.equal(enforceOrigin({headers:{}}),true)}
 finally{if(old===undefined)delete process.env.ALLOWED_ORIGIN;else process.env.ALLOWED_ORIGIN=old}
});
