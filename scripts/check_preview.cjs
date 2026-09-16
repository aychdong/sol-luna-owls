// Exercise the self-contained preview script with a small DOM harness.
// This verifies state behavior and translations, not browser layout/rendering.
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const root=path.resolve(__dirname,'..'),file=path.join(root,'sol-luna-final/制作记录/preview-template.html');
const html=fs.readFileSync(file,'utf8'),script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script);
function element(){const classes=new Set();return{style:{},dataset:{},children:[],textContent:'',attrs:{},hidden:false,
 setAttribute(k,v){this.attrs[k]=String(v)},appendChild(e){this.children.push(e)},
 classList:{contains:k=>classes.has(k),toggle(k,v){const next=v===undefined?!classes.has(k):v;if(next)classes.add(k);else classes.delete(k);return next}},
 addEventListener(k,fn){this[k]=fn},getBoundingClientRect:()=>({x:0,y:0,width:192,height:208})};}
const ids=Object.fromEntries([...html.matchAll(/\bid="([^"]+)"/g)].map(m=>[m[1],element()]));
const labels=[element(),element()],stages=[ids['sol-stage'],ids['luna-stage']];
stages.forEach((e,i)=>e.querySelector=()=>ids[i?'luna':'sol']);
const translated=[...html.matchAll(/<[^>]+data-i18n="([^"]+)"[^>]*>/g)].map(m=>{const id=m[0].match(/\bid="([^"]+)"/);const e=id?ids[id[1]]:element();e.dataset.i18n=m[1];return e});
const doc={title:'',documentElement:{},body:element(),getElementById:id=>{assert(ids[id],id);return ids[id]},createElement:element,
 querySelectorAll:selector=>({'[data-i18n]':translated,'.state-label':labels,'.stage':stages}[selector]||[])};
let callback=null,lastDuration=null;
const ctx=vm.createContext({document:doc,navigator:{language:'zh-CN'},localStorage:{getItem:()=>null,setItem:()=>{}},matchMedia:()=>({matches:false}),
 setTimeout(fn,ms){callback=fn;lastDuration=ms;return 1},clearTimeout(){callback=null}});
vm.runInContext(script,ctx);
const evalJS=s=>vm.runInContext(s,ctx);
assert.equal(ids.states.children.length,11);
assert.equal(lastDuration,1680);
assert(translated.every(e=>typeof e.textContent==='string'&&e.textContent.length));
ids.states.children[7].onclick();
for(let i=0;i<18;i++){assert(callback);callback()}
assert.equal(evalJS('row'),0);assert.equal(evalJS('col'),0);
ids['play-mode'].onchange({target:{value:'loop'}});ids.states.children[7].onclick();
for(let i=0;i<18;i++)callback();assert.equal(evalJS('row'),7);
ids.next.onclick();assert.equal(evalJS('paused'),true);assert.equal(callback,null);
const col=evalJS('col');ids.prev.onclick();assert.equal(evalJS('col'),(col+5)%6);
ids.states.children[10].onclick();assert.equal(ids['frame-counter'].textContent,'帧 1 / 4');
assert(ids.hint.textContent.includes('仅供'));assert.equal(ids.sol.style.backgroundPosition,'14.285714285714285% 70%');
ids.states.children[9].onclick();assert.equal(ids['direction-control'].hidden,false);
for(let i=0;i<16;i++){ids.direction.oninput({target:{value:i}});assert.equal(ids.sol.style.backgroundPosition,(i%8/7*100)+'% '+((9+Math.floor(i/8))/10*100)+'%')}
ids.language.onclick();assert.equal(doc.documentElement.lang,'en');assert.equal(ids.next.textContent,'Next frame');
assert(translated.every(e=>typeof e.textContent==='string'&&e.textContent.length));assert(ids.hint.textContent.includes('Native gaze'));
ids.theme.onclick({target:ids.theme});assert.equal(ids.theme.attrs['aria-pressed'],'true');
ids.size.oninput({target:{value:96}});assert.equal(ids.sol.style.height,'104px');
const report={status:'passed',method:'Node VM DOM harness; browser rendering not exercised',checks:['JavaScript syntax','all bilingual labels','native three-pass transition','continuous loop','paused frame stepping','thinking preview mapping','sixteen direction mappings','theme and size controls']};
fs.writeFileSync(path.join(root,'sol-luna-final/制作记录/preview-script-checks.json'),JSON.stringify(report,null,2)+'\n');
console.log('PASS: bilingual labels and preview state controls. Browser rendering not exercised.');
