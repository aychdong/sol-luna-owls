"""Check package pixels, animation timelines and the original-running fallback."""
from pathlib import Path
from io import BytesIO
import json, hashlib, zipfile
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'sol-luna-final'
NAMES = ['idle','running-right','running-left','waving','jumping','failed','waiting','running','review']
COUNTS = [6,8,8,4,5,8,6,6,6,8,8]
TIMES = [[1680,660,660,840,840,1920],[120]*7+[220],[120]*7+[220],
         [140]*3+[280],[140]*4+[280],[140]*7+[240],[150]*5+[260],
         [120]*5+[220],[150]*5+[280]]

def pixels(im):
    arr = np.asarray(im.convert('RGBA')).copy()
    arr[arr[:,:,3] == 0] = 0
    return arr

def same(a,b): return np.array_equal(pixels(a),pixels(b))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

checks=[]
with zipfile.ZipFile(ROOT / 'releases/v1/Sol-Luna-安装包.zip') as old:
    for pet in ('sol','luna'):
        folder=PACKAGE/'可直接安装'/pet
        meta=json.loads((folder/'pet.json').read_text())
        assert meta['id']==pet and meta['spriteVersionNumber']==2
        assert meta['spritesheetPath']=='spritesheet.webp'
        atlas=Image.open(folder/meta['spritesheetPath'])
        assert atlas.size==(1536,2288) and atlas.mode=='RGBA'
        assert not getattr(atlas,'is_animated',False)
        baseline=Image.open(BytesIO(old.read(pet+'/spritesheet.webp')))
        original_running=same(atlas.crop((0,208,1536,624)),baseline.crop((0,208,1536,624)))
        assert original_running, pet+' original running changed'
        frames=[]
        for r in range(11):
            row=[]
            for c in range(8):
                cell=atlas.crop((192*c,208*r,192*(c+1),208*(r+1)))
                box=cell.getbbox(); assert box and box[0]>=3 and box[1]>=3 and box[2]<=189 and box[3]<=204
                assert (np.asarray(cell)[:,:,3]==0).mean()>.2
                row.append(cell)
            frames.append(row)
        assert same(Image.open(PACKAGE/'预览'/f'{pet}-idle.png'),frames[0][0])
        assert same(frames[0][0],frames[0][5])
        assert same(frames[6][0],frames[6][5])
        assert same(frames[5][0],frames[5][7])
        timelines=[]
        for row,state in enumerate(NAMES):
            im=Image.open(PACKAGE/'预览'/f'{pet}-{state}.webp')
            decoded=[];elapsed=0
            for i in range(im.n_frames):
                im.seek(i);im.load();duration=im.info['duration']
                decoded.append((elapsed,elapsed+duration,im.copy()));elapsed+=duration
            assert elapsed==sum(TIMES[row]),(pet,state,elapsed)
            time=0
            for c,duration in enumerate(TIMES[row]):
                sample=time+duration/2
                displayed=next(img for start,end,img in decoded if start<=sample<end)
                assert same(displayed,frames[row][c]),(pet,state,c,'timeline differs from native sheet')
                time+=duration
            timelines.append({'state':state,'nativeFrames':COUNTS[row],'durationMs':elapsed,'previewMatchesAtlas':True})
        # Check opaque interior of each laptop lid, independent of edge antialiasing.
        laptop=[int(np.asarray(f)[167:178,137:159,3].min()) for f in frames[7][:6]]
        assert min(laptop)==255,(pet,'laptop interior lost',laptop)
        checks.append({'pet':pet,'spriteSha256':sha(folder/'spritesheet.webp'),'populatedCells':88,
                       'originalRunningPixelIdentical':original_running,'seamlessIdleEndpoints':True,
                       'staticFirstFrameMatches':True,'allLaptopInteriorMinAlpha':laptop,'timelines':timelines})

with zipfile.ZipFile(PACKAGE/'Sol-Luna-安装包.zip') as archive:
    expected={p+'/'+f for p in ('sol','luna') for f in ('pet.json','spritesheet.webp')}
    assert set(archive.namelist())==expected and archive.testzip() is None
    for name in expected:assert archive.read(name)==(PACKAGE/'可直接安装'/name).read_bytes()

report={'status':'passed','pets':checks,'zipExactlyFourInstallFiles':True,
        'visualReview':{'method':'Frame contact sheets inspected at enlarged and pet-scale sizes',
                        'laptopPresentEveryWorkFrame':True,'questionMarkSleepAndStarsRetained':True,
                        'gazeBrowTuftsRemainBilateral':True,'failedWingsStayFolded':True,
                        'flightRejected':'Inconsistent wing/cape occlusion; original running restored'},
        'nativeUiExercised':False,'browserRenderingExercised':False}
(PACKAGE/'制作记录/quality-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
validation=PACKAGE/'制作记录/validation.json';data=json.loads(validation.read_text())
data['status']='pixel-and-contact-sheet-QA-passed-native-ui-unverified'
validation.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('PASS: native atlases, animation timelines, laptop interiors, original running and four-file ZIP.')
