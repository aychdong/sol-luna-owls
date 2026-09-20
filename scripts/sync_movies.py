"""Publish local delivery after verifying staging; keep the previous folder intact."""
from pathlib import Path
import argparse,shutil,hashlib,json,datetime
p=argparse.ArgumentParser();p.add_argument('--destination',type=Path,required=True);a=p.parse_args()
R=Path(__file__).resolve().parents[1];v=(R/'VERSION').read_text().strip();dest=a.destination;stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S');stage=dest.parent/('.Sol-Luna-staging-'+stamp)
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def inventory(root):return {p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file() and p.name!='.DS_Store' and '__pycache__' not in p.parts}
assert not stage.exists();stage.mkdir(parents=True)
shutil.copytree(R/'pets',stage/'可直接安装');(stage/'预览').mkdir();(stage/'旧版回退').mkdir();(stage/'发布记录').mkdir()
shutil.copy2(R/'dist'/f'Sol-Luna-v{v}-offline-preview.html',stage/'预览/动画预览.html')
shutil.copy2(R/'dist'/f'Sol-Luna-v{v}-install.zip',stage/'Sol-Luna-安装包.zip')
for label in ['R3','V1-original']:shutil.copy2(R/'dist'/f'Sol-Luna-{label}-rollback.zip',stage/'旧版回退'/f'Sol-Luna-{label}-rollback.zip')
shutil.copy2(R/'docs/INSTALL.md',stage/'使用说明.md')
for name in ['package-validation.json','preview-checks.json']:shutil.copy2(R/'reports'/name,stage/'发布记录'/name)
(stage/'素材与项目位置.txt').write_text(f'当前正式版：V1 + R4 / v{v}\n完整项目：{R}\n素材：{R}/assets\n历史原图与试作：{R}/archive/history\n项目说明：{R}/docs/PROJECT.md\nGitHub：https://github.com/aychdong/sol-luna-owls\n下载与历史归档：https://github.com/aychdong/sol-luna-owls/releases/tag/v{v}\n')
for pet in ['sol','luna']:
 for n in ['pet.json','spritesheet.webp']:assert sha(stage/'可直接安装'/pet/n)==sha(R/'pets'/pet/n)
assert sha(stage/'Sol-Luna-安装包.zip')==sha(R/'dist'/f'Sol-Luna-v{v}-install.zip')
new=inventory(stage);(stage/'发布记录/SHA256SUMS.txt').write_text(''.join(h+'  '+n+'\n' for n,h in sorted(new.items())))
backup=None;before={}
if dest.exists():
 before=inventory(dest);backup=dest.parent/'历史版本'/f'{dest.name}-发布前-{stamp}';backup.parent.mkdir(exist_ok=True);assert not backup.exists();dest.rename(backup);assert inventory(backup)==before
stage.rename(dest);assert all(sha(dest/n)==h for n,h in new.items())
report={'status':'passed','version':v,'destinationRelativeToMovies':'动画建模/'+dest.name,'previousDeliveryBackup':str(backup.relative_to(dest.parent)) if backup else None,'previousFilesVerified':len(before),'newFilesVerified':len(new),'installedPetsModified':False}
(R/'reports/movies-delivery.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
