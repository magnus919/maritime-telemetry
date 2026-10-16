// Original local-only integration probe. No external provider or vessel connection.
const fs=require('node:fs'), os=require('node:os'), path=require('node:path');
const assert=require('node:assert/strict'), net=require('node:net');
const {randomBytes}=require('node:crypto');
const WebSocket=require('ws'), schema=require('@signalk/signalk-schema');
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'maritime-signalk-'));
process.env.SIGNALK_NODE_CONFIG_DIR=temp;
process.env.SIGNALK_NODE_CONDFIG_DIR=temp;
process.env.SIGNALK_DISABLE_SERVER_UPDATES='1';
for (const key of ['ADMINUSER','SECURITYSTRATEGY','SECRETKEY','PORT','SSLPORT','LISTEN_FDS']) delete process.env[key];
// The pinned upstream server does not expose a host argument at its listen call.
// This process-local test adapter forces EVERY TCP listener to loopback, port 0.
const originalListen=net.Server.prototype.listen;
net.Server.prototype.listen=function(...args){
 const cb=args.find(a=>typeof a==='function');
 return originalListen.call(this,{host:'127.0.0.1',port:0},cb);
};
const Server=require('signalk-server');
const interfaces=Object.fromEntries(Object.keys(require('signalk-server/dist/interfaces')).map(k=>[k,['rest','ws'].includes(k)]));
const server=new Server({config:{configPath:temp,settings:{port:3000,mdns:false,pipedProviders:[],interfaces,security:{strategy:'./tokensecurity'}}},
 securityConfig:{allow_readonly:true,allowDeviceAccessRequests:false,allowNewUserRegistration:false,
 secretKey:randomBytes(32).toString('hex'),users:[{username:'lab',type:'admin',password:require('bcryptjs').hashSync(randomBytes(32).toString('hex'),4)}]}});
const sockets=[];
const deadline=setTimeout(()=>{console.error('FAIL integration deadline');process.exit(1)},20000);
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function connect(url){
 const ws=new WebSocket(url);sockets.push(ws);const received=[];
 ws.on('message',data=>received.push(JSON.parse(data.toString())));
 await new Promise((resolve,reject)=>{ws.once('open',resolve);ws.once('error',reject)});
 ws.send(JSON.stringify({context:'vessels.self',subscribe:[{path:'environment.water.temperature',period:100,minPeriod:0,policy:'instant'}]}));
 await sleep(100);
 return {ws,received};
}
(async()=>{
 try{
  await server.start();
  assert.equal(server.app.server.address().address,'127.0.0.1');
  const base=`http://127.0.0.1:${server.app.server.address().port}`;
  const discovery=await (await fetch(base+'/signalk')).json();
  assert.ok(discovery.endpoints);
  let client=await connect(base.replace('http','ws')+'/signalk/v1/stream?subscribe=none');
  function publish(value){
   const delta={context:'vessels.self',updates:[{source:{label:'synthetic-lab'},timestamp:new Date().toISOString(),values:[{path:'environment.water.temperature',value}]}]};
   const result=schema.validateDelta(delta);assert.equal(result.valid,true,JSON.stringify(result.errors));
   server.app.handleMessage('synthetic-lab',delta);
  }
  publish(293.15);await sleep(300);
  let leaf=await (await fetch(base+'/signalk/v1/api/vessels/self/environment/water/temperature')).json();
  assert.equal(leaf.value,293.15);assert.ok(leaf.timestamp);assert.ok(leaf.$source);
  assert.ok(client.received.some(d=>d.updates?.some(u=>u.values?.some(v=>v.value===293.15))));
  const denied=await fetch(base+'/signalk/v1/api/vessels/self/electrical/switches/lab/state',{method:'PUT',headers:{'content-type':'application/json'},body:JSON.stringify({value:true})});
  assert.ok([401,403].includes(denied.status),`unexpected write status ${denied.status}`);
  client.ws.close();await sleep(100);
  client=await connect(base.replace('http','ws')+'/signalk/v1/stream?subscribe=none');
  publish(null);await sleep(300);
  assert.ok(client.received.some(d=>d.updates?.some(u=>u.values?.some(v=>v.value===null))));
  publish(294.15);await sleep(300);
  leaf=await (await fetch(base+'/signalk/v1/api/vessels/self/environment/water/temperature')).json();assert.equal(leaf.value,294.15);
  console.log('LAB_RESULT '+JSON.stringify({passed:true,server:'2.33.0',schema:'1.8.2',checks:['loopback','discovery','schema-delta','REST-value-source-time','WebSocket-subscription','anonymous-PUT-denied','reconnect','null-update','recovery'],scope:'synthetic local server; no hardware, TLS, token revocation or plugin lifecycle verification'}));
 }catch(e){console.error('LAB_FAIL',e);process.exitCode=1}
 finally{
  for(const ws of sockets)ws.terminate();
  await server.stop();clearTimeout(deadline);net.Server.prototype.listen=originalListen;
  fs.rmSync(temp,{recursive:true,force:true});
  // Upstream imports retain background handles; this standalone probe owns its process.
  process.exit(process.exitCode || 0);
 }
})();
