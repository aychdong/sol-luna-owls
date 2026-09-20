// State-control and local-link checks; this is not a browser rendering test.
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script);
function element(){const classes=new Set();return {style:{},dataset:{},children:[],attrs:{},textContent:'',value:'',hidden:false,
  get options(){return this.children},appendChild(e){this.children.push(e)},setAttribute(k,v){this.attrs[k]=String(v)},
  classList:{toggle(k){if(classes.has(k)){classes.delete(k);return false}classes.add(k);return true}}};}
const ids=Object.fromEntries([...html.matchAll(/\bid="([^"]+)"/g)].map(m=>[m[1],element()]));
const labels=[...html.matchAll(/<[^>]+data-i18n="([^"]+)"[^>]*>/g)].map(m=>{const id=m[0].match(/\bid="([^"]+)"/);const e=id?ids[id[1]]:element();e.dataset.i18n=m[1];return e});
let callback=null,duration=null;
const ctx=vm.createContext({document:{documentElement:{},body:element(),createElement:element,getElementById:id=>{assert(ids[id],id);return ids[id]},querySelectorAll:()=>labels},
  setTimeout(fn,ms){callback=fn;duration=ms;return 1},clearTimeout(){callback=null}});
vm.runInContext(script,ctx);const get=s=>vm.runInContext(s,ctx);
assert.equal(ids.action.children.length,10);assert.equal(ids.directions.children.length,16);
assert.equal(get('selected'),9);assert.equal(get('frame'),9);assert.equal(ids['sol-new'].style.backgroundPosition,'-240px -2600px');
for(let i=0;i<16;i++){ids.directions.children[i].onclick();assert.equal(get('frame'),i);assert.equal(ids['sol-new'].style.backgroundPosition,`${-(i%8)*240}px ${-(9+Math.floor(i/8))*260}px`)}
for(let i=0;i<9;i++){ids.action.onchange({target:{value:i}});const n=get('actions[selected].t.length');assert.equal(get('frame'),0);assert(callback);for(let f=0;f<n;f++)callback();assert.equal(get('frame'),0);}
ids.action.onchange({target:{value:7}});assert.equal(duration,120);ids.speed.onchange({target:{value:.5}});assert.equal(duration,240);
ids.next.onclick();assert.equal(get('frame'),1);assert.equal(callback,null);ids.prev.onclick();assert.equal(get('frame'),0);
ids.language.onclick();assert.equal(ids.next.textContent,'Next');assert(labels.every(e=>e.textContent.length));
ids.size.onchange({target:{value:96}});assert.equal(ids['sol-new'].style.width,'96px');assert.equal(ids['sol-new'].style.height,'104px');
ids['left-loop'].onclick();assert.equal(get('frame'),8);for(let i=0;i<8;i++)callback();assert.equal(get('frame'),8);assert.equal(get('leftOnly'),true);
ids.theme.onclick();assert.equal(ids.theme.attrs['aria-pressed'],'true');
const links=[...html.matchAll(/(?:href|src)="([^"]+)"|url\('([^']+)'\)/g)].map(m=>m[1]||m[2]);
for(const link of links.filter(x=>!x.startsWith('https:')))assert(fs.existsSync(path.resolve(root,decodeURI(link))),`Missing local asset: ${link}`);
const report={status:'passed',method:'Node VM control checks and local file checks; no browser/native UI test',checks:['10 V1 state choices','16 direction mappings','native frame durations','loop wrap','slow playback','paused stepping','bilingual labels','96 px size','dark background control',`${links.length} local asset and download links`]};
fs.writeFileSync(path.join(root,'reports/preview-checks.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
