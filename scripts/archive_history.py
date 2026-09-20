"""Preserve owl-only history and workbench materials in a verified Release ZIP."""
from pathlib import Path
import zipfile,hashlib,json
R=Path(__file__).resolve().parents[1];V=(R/'VERSION').read_text().strip();D=R/'dist'/f'Sol-Luna-v{V}-source-history.zip'
files=[]
for relative in ['archive/history','archive/snapshots','workbench']:
 for p in (R/relative).rglob('*'):
  if p.is_file() and p.name!='.DS_Store' and '__pycache__' not in p.parts:
   assert not p.is_symlink(),p
   files.append(p)
manifest=[]
with zipfile.ZipFile(D,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(files):
  data=p.read_bytes();name=p.relative_to(R).as_posix();z.writestr(name,data)
  manifest.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
with zipfile.ZipFile(D) as z:
 assert z.testzip() is None
 for e in manifest:assert hashlib.sha256(z.read(e['path'])).hexdigest()==e['sha256'],e['path']
report={'version':V,'archive':D.name,'sha256':hashlib.sha256(D.read_bytes()).hexdigest(),'bytes':D.stat().st_size,'files':manifest,'zip_entries_verified':True}
(R/'archive/source-archive-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='files'}),'files:',len(files))
