"""Verify byte-exact promotion, untouched V1 actions, timelines and ZIP."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,zipfile
R=Path(__file__).resolve().parents[1];V=(R/'VERSION').read_text().strip();F=json.loads((R/'assets/native-format.json').read_text());records=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for pet in ['sol','luna']:
 folder=R/'pets'/pet
 for n in ['pet.json','spritesheet.webp']:assert (folder/n).read_bytes()==(R/'assets/approved'/pet/n).read_bytes()
 meta=json.loads((folder/'pet.json').read_text());assert meta['id']==pet and meta['spriteVersionNumber']==2
 im=Image.open(folder/'spritesheet.webp');assert im.mode=='RGBA' and im.size==(1536,2288);assert b'VP8L' in (folder/'spritesheet.webp').read_bytes()
 a=np.array(im);r3=np.array(Image.open(R/'assets/baseline-r3'/pet/'spritesheet.webp').convert('RGBA'));v1=np.array(Image.open(R/'assets/baselines/v1-original'/pet/'spritesheet.webp').convert('RGBA'))
 def changed(b):
  mask=np.any(a!=b,axis=2);return [[r+1,c+1] for r in range(11) for c in range(8) if mask[r*208:(r+1)*208,c*192:(c+1)*192].any()]
 assert changed(r3)==[[11,2],[11,3],[11,4],[11,6],[11,7]]
 assert np.array_equal(a[:1872],v1[:1872]),'V1 action rows changed'
 assert np.array_equal(np.array(Image.open(R/'preview'/f'{pet}-idle.png')),a[:208,:192])
 for row,name in enumerate(F['animations']):
  anim=Image.open(R/'preview'/f'{pet}-{name}.webp');decoded=[];elapsed=0
  for i in range(anim.n_frames):
   anim.seek(i);anim.load();d=anim.info['duration'];decoded.append((elapsed,elapsed+d,np.array(anim.convert('RGBA'))));elapsed+=d
  assert elapsed==sum(F['animationTimingMs'][name]);t=0
  for i,d in enumerate(F['animationTimingMs'][name]):
   actual=next(f for lo,hi,f in decoded if lo<=t+d/2<hi);assert np.array_equal(actual,a[row*208:(row+1)*208,i*192:(i+1)*192]),(pet,name,i);t+=d
 records.append({'pet':pet,'atlas_sha256':sha(folder/'spritesheet.webp'),'changed_cells_vs_r3':changed(r3),'changed_cells_vs_v1':changed(v1),'all_72_v1_action_cells_unchanged':True,'other_83_r3_cells_unchanged':True})
with zipfile.ZipFile(R/'dist'/f'Sol-Luna-v{V}-install.zip') as z:
 expected={f'{p}/{n}' for p in ['sol','luna'] for n in ['pet.json','spritesheet.webp']};assert set(z.namelist())==expected and z.testzip() is None
 for n in expected:assert z.read(n)==(R/'pets'/n).read_bytes()
for e in json.loads((R/'assets/provenance.json').read_text()):assert sha(R/e['path'])==e['sha256']
report={'status':'passed','version':V,'approved_source':'V1 gaze repair R4','atlas_dimensions':[1536,2288],'lossless_webp':True,'approved_files_byte_identical':True,'native_animation_timelines_verified':True,'install_zip_exactly_four_files':True,'native_ui_triggers_retested':False,'records':records}
(R/'reports/package-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
