"""Package delivery and rollback copies without editing pixels."""
from pathlib import Path
import os
import hashlib,json
from build_release import zip_files
R=Path(__file__).resolve().parents[2];V=(R/'VERSION').read_text().strip();D=Path(os.environ.get('SOL_LUNA_DIST',str(R/'dist')))
files=[('可直接安装/'+f'{p}/{n}',(R/'pets'/p/n).read_bytes()) for p in ['sol','luna'] for n in ['pet.json','spritesheet.webp']]
files += [('预览/动画预览.html',(D/f'Sol-Luna-v{V}-user-preview.html').read_bytes()),('使用说明.md',(R/'docs/INSTALL.md').read_bytes()),('Sol-Luna-安装包.zip',(D/f'Sol-Luna-v{V}-install.zip').read_bytes())]
zip_files(D/f'Sol-Luna-v{V}-user-delivery.zip',files)
for label,base in [('V1-original','development/assets/baselines/v1-original'),('R3','development/assets/baseline-r3')]:
 zip_files(D/f'Sol-Luna-{label}-rollback.zip',[(f'{p}/{n}',(R/base/p/n).read_bytes()) for p in ['sol','luna'] for n in ['pet.json','spritesheet.webp']])
names=[f'Sol-Luna-v{V}-install.zip',f'Sol-Luna-v{V}-user-delivery.zip',f'Sol-Luna-v{V}-user-preview.html','Sol-Luna-V1-original-rollback.zip','Sol-Luna-R3-rollback.zip']
if (D/f'Sol-Luna-v{V}-source-history.zip').exists():names.append(f'Sol-Luna-v{V}-source-history.zip')
(D/f'SHA256SUMS-v{V}-user-downloads.txt').write_text(''.join(hashlib.sha256((D/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in names))
(R/'development/reports/release-files.json').write_text(json.dumps({'version':V,'assets':names+[f'SHA256SUMS-v{V}-user-downloads.txt']},indent=2)+'\n')
print('Delivery, rollback packages and checksums ready.')
