// Original offline integration probe; input is synthetic CANboat -si -camel JSONL.
const fs=require('node:fs'), assert=require('node:assert/strict');
const {EventEmitter}=require('node:events');
const mapper=require('@signalk/n2k-signalk');
const schema=require('@signalk/signalk-schema');
const pluginModule=require('signalk-n2kais-to-nmea0183');
const input=process.argv[2];
if(!input) throw new Error('Usage: node probe.cjs synthetic-decoded.jsonl');
const rows=fs.readFileSync(input,'utf8').trim().split('\n').map(JSON.parse)
 .filter(x=>!x.version).map(x=>x.pgn?x:Object.values(x)[0]);
assert.equal(rows.length,13);
const app=new EventEmitter();
app.config={version:'2.33.0'}; // Only the plugin's field-naming contract, not a running server.
app.debug=()=>{};app.error=()=>{};app.getSelfPath=()=> '987654321';
function values(delta){return delta.updates.flatMap(u=>u.values||[])}
function position(delta){return values(delta).find(x=>x.path==='navigation.position')}
const trials=[];
for(let trial=0;trial<3;trial++){
 const deltas=rows.map(row=>mapper.toDelta(row,{}));
 for(const delta of deltas){const v=schema.validateDelta(delta);assert.equal(v.valid,true,JSON.stringify(v.errors))}
 assert.equal(deltas[0].context,'vessels.urn:mrn:imo:mmsi:123456789');
 assert.equal(deltas[10].context,'vessels.urn:mrn:imo:mmsi:234567890');
 assert.equal(deltas[0].updates[0].source.src,'35');
 assert.deepEqual(position(deltas[0]).value,{longitude:-2,latitude:1});
 assert.equal(position(deltas[8]),undefined); // Known upstream4.7.0 limitation, NOT desired behavior.
 assert.equal(position(deltas[9]),undefined);
 for(const i of [2,3,6,7,12]) assert.equal(position(deltas[i]),undefined);
 const sentences=rows.map(row=>pluginModule.convert(app,{},'987654321',row)?.nmea||null);
 assert.ok(sentences[0].startsWith('!AIVDM,'));assert.equal(sentences[11],null);
 assert.equal(pluginModule.convert(app,{},'123456789',rows[0]),undefined);
 assert.ok(pluginModule.convert(app,{sendSelf:true},'123456789',rows[11])?.nmea);
 assert.equal(pluginModule.convert(app,{},'987654321',{...rows[0],pgn:129040}),undefined);
 // Test actual start/stop hooks against a local event bus; no TCP server/device.
 let emitted=0;const receive=()=>emitted++;app.on('nmea0183out',receive);
 const plugin=pluginModule.default(app);
 for(let i=0;i<2;i++){
  plugin.start({});assert.equal(app.listenerCount('N2KAnalyzerOut'),1);
  app.emit('N2KAnalyzerOut',rows[0]);plugin.stop();
  assert.equal(app.listenerCount('N2KAnalyzerOut'),0);
  app.emit('N2KAnalyzerOut',rows[0]);
 }
 assert.equal(emitted,2);app.removeListener('nmea0183out',receive);
 trials.push({deltas,sentences,checks:['MMSI-context','schema','source','static-not-position','self-filter','unsupported-129040','plugin-stop-restart']});
}
console.log(JSON.stringify({passed:true,scope:'offline functions and event bus; no server or chartplotter',
 known_limitations:['mapper4.7.0 omits zero-longitude position','mapper omits unavailable position instead of clearing prior state','0183 conversion is lossy; inspect independent pyais report'],trials},null,2));
