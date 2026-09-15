"""Build the offline preview, repository index, and checksum manifest."""
from pathlib import Path
import base64, hashlib, json, re, zipfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'sol-luna-final'
template = (PACKAGE / '制作记录/preview-template.html').read_text()
pattern = r'const DATA = /\* PET_DATA \*/ .*?;'
assert len(re.findall(pattern, template)) == 1
embedded = ['data:image/webp;base64,' + base64.b64encode(
    (PACKAGE / '可直接安装' / pet / 'spritesheet.webp').read_bytes()).decode()
    for pet in ('sol', 'luna')]
offline = re.sub(pattern, lambda _: 'const DATA = ' + json.dumps(embedded) + ';', template)
(PACKAGE / '预览/动画预览.html').write_text(offline)
relative = ['sol-luna-final/可直接安装/' + pet + '/spritesheet.webp' for pet in ('sol', 'luna')]
(ROOT / 'index.html').write_text(re.sub(pattern, lambda _: 'const DATA = ' + json.dumps(relative) + ';', template))
with zipfile.ZipFile(PACKAGE / 'Sol-Luna-安装包.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for file in sorted((PACKAGE / '可直接安装').rglob('*')):
        if file.is_file():
            archive.write(file, file.relative_to(PACKAGE / '可直接安装'))
files = []
for f in sorted(PACKAGE.rglob('*')):
    if f.is_file() and f.name != 'files-manifest.json' and '__pycache__' not in str(f):
        files.append({'path': str(f.relative_to(PACKAGE)), 'bytes': f.stat().st_size,
                      'sha256': hashlib.sha256(f.read_bytes()).hexdigest()})
(PACKAGE / '制作记录/files-manifest.json').write_text(json.dumps({
    'version': '2026-09-14-bilingual', 'status': 'complete', 'files': files
}, ensure_ascii=False, indent=2) + '\n')
print('Built bilingual previews and installation ZIP; indexed', len(files), 'package files.')
