"""Preserve shareable owl history; exclude local-only poster sources and Git backups."""
from pathlib import Path
import zipfile,hashlib,json,argparse
R=Path(__file__).resolve().parents[2];V=(R/'VERSION').read_text().strip()
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();D=a.output
assert not D.exists(),'Choose a new output filename; published archives are immutable'
D.parent.mkdir(parents=True,exist_ok=True)
files=[]
for relative in ['archive/history','archive/snapshots','archive/workbench','archive/legacy']:
 for p in (R/relative).rglob('*'):
  if p.is_relative_to(R/'archive/workbench/share-guide-v1.1.0'):
   continue  # User requested local-only retention of complete poster sources.
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
D.with_suffix('.manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='files'}),'files:',len(files))
