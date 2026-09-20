"""Build the bilingual release page and embedded offline copy."""
from pathlib import Path
import re,base64
R=Path(__file__).resolve().parents[1];V=(R/'VERSION').read_text().strip()
html=(R/'templates/preview.html').read_text().replace('{{VERSION}}',V);(R/'index.html').write_text(html)
offline=html
for ref in set(re.findall(r"url\('([^']+)'\)|<img src=\"([^\"]+)\"",html)):
 name=ref[0] or ref[1];p=R/name;mime='image/webp' if p.suffix=='.webp' else 'image/png'
 offline=offline.replace(name,f'data:{mime};base64,'+base64.b64encode(p.read_bytes()).decode())
for path in ['README.md','docs/INSTALL.md','reports/package-validation.json']:
 offline=offline.replace('href="'+path+'"','href="https://github.com/aychdong/sol-luna-owls/blob/v'+V+'/'+path+'"')
(R/'dist'/f'Sol-Luna-v{V}-offline-preview.html').write_text(offline)
print('Built bilingual online and self-contained offline previews.')
