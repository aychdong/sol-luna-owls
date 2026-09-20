"""Release exact approved atlases, native-timed previews and an install ZIP."""
from pathlib import Path
import os
from PIL import Image
import json,zipfile,shutil
R=Path(__file__).resolve().parents[2];V=(R/'VERSION').read_text().strip()
D=Path(os.environ.get('SOL_LUNA_DIST',str(R/'dist')))
def zip_files(path,files):
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in sorted(files):
   i=zipfile.ZipInfo(name,(2026,9,19,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16;z.writestr(i,data)
def build():
 D.mkdir(parents=True,exist_ok=True);(R/'preview').mkdir(exist_ok=True)
 f=json.loads((R/'development/assets/native-format.json').read_text())
 for pet in ['sol','luna']:
  out=R/'pets'/pet;out.mkdir(parents=True,exist_ok=True)
  for n in ['pet.json','spritesheet.webp']:shutil.copy2(R/'development/assets/approved'/pet/n,out/n)
  a=Image.open(out/'spritesheet.webp').convert('RGBA');a.crop((0,0,192,208)).save(R/'preview'/f'{pet}-idle.png')
  for r,n in enumerate(f['animations']):
   ff=[a.crop((c*192,r*208,(c+1)*192,(r+1)*208)) for c in range(f['requiredFramesByRow'][r])]
   ff[0].save(R/'preview'/f'{pet}-{n}.webp',save_all=True,append_images=ff[1:],duration=f['animationTimingMs'][n],loop=0,lossless=True,exact=True)
 zip_files(D/f'Sol-Luna-v{V}-install.zip',[(f'{p}/{n}',(R/'pets'/p/n).read_bytes()) for p in ['sol','luna'] for n in ['pet.json','spritesheet.webp']])
 print('Built approved pixels, native-timed previews and four-file installation ZIP.')
if __name__=='__main__':build()
