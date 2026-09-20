"""Build the public page and a self-contained copy from approved assets."""
from pathlib import Path
import re, base64, os, mimetypes
R=Path(__file__).resolve().parents[2]
V=(R/'VERSION').read_text().strip()
D=Path(os.environ.get('SOL_LUNA_DIST',str(R/'dist')));D.mkdir(parents=True,exist_ok=True)
html=(R/'development/templates/preview.html').read_text().replace('{{VERSION}}',V)
(R/'index.html').write_text(html)
offline=html
for a,b in set(re.findall(r"url\('([^']+)'\)|<img src=\"([^\"]+)\"",html)):
 name=a or b;p=R/name;mime=mimetypes.guess_type(name)[0] or 'application/octet-stream'
 offline=offline.replace(name,f'data:{mime};base64,'+base64.b64encode(p.read_bytes()).decode())
# Keep the downloadable quick guide accessible outside the project folder.
offline=offline.replace('href="media/sol-luna-quick-guide.png"','href="https://aychdong.github.io/sol-luna-owls/media/sol-luna-quick-guide.png"')
(D/f'Sol-Luna-v{V}-user-preview.html').write_text(offline)
print('Built public bilingual preview and self-contained user-preview.html.')
