#!/usr/bin/env python3
"""Local, reproducible post-production of the approved Sol/Luna assets.

Requires Pillow and numpy. No network, no changes to source artwork.
Generates a v2 atlas, lossless WebP, previews, and validation evidence.
"""
from pathlib import Path
from collections import deque
import hashlib, json, math, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    'sol': ROOT/'制作记录/原始素材/sol-atlas-generated.png',
    'luna': ROOT/'制作记录/原始素材/luna-atlas-final-generated.png',
}
STATES = ['idle','running-right','running-left','waving','jumping','failed','waiting','running','review']
COUNTS = [6,8,8,4,5,8,6,6,6,8,8]
TIMES = [[1680,660,660,840,840,1920],[120]*7+[220],[120]*7+[220],
         [140]*3+[280],[140]*4+[280],[140]*7+[240],
         [150]*5+[260],[120]*5+[220],[150]*5+[280]]

def components(mask, minimum=80):
    seen = mask.copy()
    result=[]
    for yy,xx in zip(*np.where(seen)):
        if not seen[yy,xx]: continue
        todo=[(int(yy),int(xx))];seen[yy,xx]=False;pixels=[]
        while todo:
            y,x=todo.pop();pixels.append((y,x))
            for dy,dx in ((0,1),(0,-1),(1,0),(-1,0)):
                ny,nx=y+dy,x+dx
                if 0<=ny<seen.shape[0] and 0<=nx<seen.shape[1] and seen[ny,nx]:
                    seen[ny,nx]=False;todo.append((ny,nx))
        if len(pixels)>=minimum:
            p=np.asarray(pixels);result.append(p)
    return sorted(result,key=lambda p:float(p[:,1].mean()))

def foreground_seed(rgb):
    a=rgb.astype(np.int16)
    # The model supplied a neutral checkerboard. Feather/cape/gold colors
    # form closed, chromatic silhouettes around neutral ivory interiors.
    return ((a.max(2)-a.min(2))>19) | (a.max(2)<130)

def row_bands(rgb):
    active=foreground_seed(rgb).sum(1)>20
    ranges=[];start=None
    for y,on in enumerate(active):
        if on and start is None:start=y
        if not on and start is not None:
            if y-start>40:ranges.append((start,y))
            start=None
    if start is not None:ranges.append((start,len(active)))
    assert len(ranges)==11, f'Expected eleven rows, got {ranges}'
    edges=[0]+[(ranges[i-1][1]+ranges[i][0])//2 for i in range(1,11)]+[rgb.shape[0]]
    return list(zip(edges[:-1],edges[1:]))

def silhouette(rgb):
    seed=Image.fromarray(foreground_seed(rgb).astype('uint8')*255)
    seed=seed.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    # Pad before flood fill so no clipped-edge assumption enters the mask.
    padded=Image.new('L',(seed.width+2,seed.height+2),0);padded.paste(seed,(1,1))
    ImageDraw.floodfill(padded,(0,0),128)
    a=np.asarray(padded)[1:-1,1:-1]
    return a!=128

def matte_cutout(rgb,mask):
    """Rebuild clean antialiasing without retaining grey checkerboard fringes."""
    hard=Image.fromarray(mask.astype('uint8')*255)
    alpha=np.asarray(hard.filter(ImageFilter.GaussianBlur(.38))).copy()
    alpha[alpha<4]=0;alpha[alpha>251]=255
    inside=np.asarray(hard.filter(ImageFilter.MinFilter(5)))>0
    # Extend nearby solid foreground color through the thin boundary. This
    # removes checkerboard contamination from the generated outer pixels.
    sums=np.zeros_like(rgb,dtype=float);weights=np.zeros(mask.shape,dtype=float)
    colors=rgb.astype(float)
    for dy in range(-3,4):
        for dx in range(-3,4):
            wt=1.0/(1+dx*dx+dy*dy)
            m=np.roll(inside,(dy,dx),(0,1))
            sums+=np.roll(colors,(dy,dx),(0,1))*m[:,:,None]*wt
            weights+=m*wt
    edge=(alpha>0)&~inside&(weights>0)
    clean=rgb.copy();clean[edge]=np.clip(sums[edge]/weights[edge,None],0,255).astype('uint8')
    clean[alpha==0]=0
    return Image.fromarray(np.dstack([clean,alpha]))

def source_frames(key):
    rgb=np.asarray(Image.open(SOURCES[key]).convert('RGB'))
    guide_rgb=np.asarray(Image.open(SOURCES['sol']).convert('RGB')) if key=='luna' else None
    guide_bands=row_bands(guide_rgb) if guide_rgb is not None else None
    frames=[];records=[]
    for row,(top,bottom) in enumerate(row_bands(rgb)):
        strip=rgb[top:bottom];mask=silhouette(strip)
        if guide_rgb is not None:
            gt,gb=guide_bands[row]
            # Luna is an identity-preserving edit of the same poses. Use only
            # an eroded interior from Sol as an opaque-white-region prior;
            # Luna's own colored silhouette still determines its outer edge.
            guide=Image.fromarray(silhouette(guide_rgb[gt:gb]).astype('uint8')*255)
            guide=guide.resize((strip.shape[1],strip.shape[0]),Image.Resampling.NEAREST)
            guide=guide.filter(ImageFilter.MinFilter(7))
            mask|=np.asarray(guide)>0
            padded=Image.new('L',(strip.shape[1]+2,strip.shape[0]+2),0)
            padded.paste(Image.fromarray(mask.astype('uint8')*255),(1,1))
            ImageDraw.floodfill(padded,(0,0),128)
            mask=np.asarray(padded)[1:-1,1:-1]!=128
        comps=components(mask)
        print(key,'row',row,'components',[(len(p),int(p[:,1].min()),int(p[:,1].max())) for p in comps],flush=True)
        assert len(comps)==8, f'{key} row {row}: {len(comps)} components'
        for col,p in enumerate(comps):
            one=np.zeros(mask.shape,dtype=bool);one[p[:,0],p[:,1]]=True
            l=max(0,int(p[:,1].min())-4);r=min(strip.shape[1],int(p[:,1].max())+5)
            t=max(0,int(p[:,0].min())-4);b=min(strip.shape[0],int(p[:,0].max())+5)
            rgba=matte_cutout(strip[t:b,l:r],one[t:b,l:r])
            frames.append(rgba)
            records.append({'row':row,'column':col,'sourceBox':[l,top+t,r,top+b],
                            'opaquePixelCount':int(one.sum())})
    return frames,records

def normalize_frames(raw):
    # One global scale preserves drawing proportions and coherent character size.
    standing_height=np.median([f.getbbox()[3]-f.getbbox()[1] for f in raw[:8]])
    scale=160/standing_height
    frames=[]
    for i,f in enumerate(raw):
        row,col=divmod(i,8)
        scaled=f.resize((round(f.width*scale),round(f.height*scale)),Image.Resampling.LANCZOS)
        box=scaled.getbbox();obj=scaled.crop(box)
        if obj.width>174 or obj.height>180:
            # Only extended-wing extremities may exceed the regular envelope.
            ratio=min(174/obj.width,180/obj.height)
            obj=obj.resize((round(obj.width*ratio),round(obj.height*ratio)),Image.Resampling.LANCZOS)
        cell=Image.new('RGBA',(192,208))
        y=190-obj.height
        if row==4 and col in (2,3):y-=14 if col==2 else 10
        cell.alpha_composite(obj,((192-obj.width)//2,y))
        frames.append(cell)
    # Retain a settled pose for first frame / reduced motion. Recover quickly
    # in setback animation instead of starting with a prolonged closed-eye pose.
    frames[5*8:6*8]=[frames[0],frames[5*8],frames[5*8+1],frames[5*8+3],
                     frames[5*8+4],frames[5*8+5],frames[5*8+6],frames[0]]
    # The five-frame hop must settle before the next repetition.
    frames[4*8]=frames[0]
    frames[4*8+4]=frames[0]
    for row,count in enumerate(COUNTS[:9]):
        for col in range(count,8):frames[row*8+col]=frames[0]
    return frames,scale

def make_atlas(frames):
    atlas=Image.new('RGBA',(1536,2288))
    for i,frame in enumerate(frames):atlas.alpha_composite(frame,((i%8)*192,(i//8)*208))
    return atlas

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def validate(key,atlas,frames,scale,records):
    dest=ROOT/'可直接安装'/key
    reopened=Image.open(dest/'spritesheet.webp').convert('RGBA')
    assert reopened.size==(1536,2288)
    assert np.array_equal(np.asarray(atlas),np.asarray(reopened)), 'Lossless WebP differs'
    reports=[]
    for i,f in enumerate(frames):
        a=np.asarray(f)[:,:,3];box=f.getbbox()
        assert box and box[0]>=6 and box[1]>=6 and box[2]<=186 and box[3]<=202,(key,i,box)
        assert (a==0).mean()>.3
        assert (a==255).sum()>1000
        reports.append({'row':i//8,'column':i%8,'alphaBox':list(box),
                        'transparentFraction':round(float((a==0).mean()),4)})
    for r,count in enumerate(COUNTS):
        unique=len({hashlib.sha256(f.tobytes()).hexdigest() for f in frames[r*8:r*8+count]})
        assert unique>=min(count,3),(key,r,unique)
    return {'pet':key,'status':'passed','width':1536,'height':2288,'mode':'RGBA',
            'frameCount':88,'requiredFramesByRow':COUNTS,'sourceToOutputScale':scale,
            'webpLosslessPixelRoundtrip':True,'sourceSha256':sha(SOURCES[key]),
            'spriteSha256':sha(dest/'spritesheet.webp'),'frames':reports,'sourceExtraction':records}

def make_previews(key,frames):
    preview=ROOT/'预览'
    frames[0].save(preview/f'{key}-idle.png')
    for row,state in enumerate(STATES):
        seq=frames[row*8:row*8+COUNTS[row]]
        seq[0].save(preview/f'{key}-{state}.webp',save_all=True,append_images=seq[1:],
                    duration=TIMES[row],loop=0,lossless=True,method=6)
    # Technical contact sheet at native dimensions over neutral gray.
    sheet=Image.new('RGB',(1536,2288),(222,225,230))
    for i,f in enumerate(frames):sheet.paste(f,((i%8)*192,(i//8)*208),f)
    sheet.save(preview/f'{key}-全帧检查.jpg',quality=93)

def main():
    allreports=[];allframes={}
    for key in SOURCES:
        raw,records=source_frames(key);frames,scale=normalize_frames(raw)
        atlas=make_atlas(frames);dest=ROOT/'可直接安装'/key;dest.mkdir(parents=True,exist_ok=True)
        atlas.save(dest/'spritesheet.webp',lossless=True,exact=True,method=6)
        metadata={'id':key,'displayName':('Sol · 晨光' if key=='sol' else 'Luna · 月夜'),
                  'description':('晨光猫头鹰：琥珀眼、短腿、金纹披风与太阳徽章。' if key=='sol' else '月夜猫头鹰：琥珀眼、短腿、深靛蓝金纹披风与月亮主题配饰。'),
                  'spriteVersionNumber':2,'spritesheetPath':'spritesheet.webp'}
        (dest/'pet.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
        make_previews(key,frames)
        allreports.append(validate(key,atlas,frames,scale,records));allframes[key]=frames
    summary={'status':'passed','scope':'Package format, alpha, cell bounds, lossless encoding, non-empty animation frames',
             'nativeAppSelectedAndPlayed':False,'appFormatVerifiedVersion':'26.901.51231',
             'pets':allreports}
    (ROOT/'制作记录/validation.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    print('Validated both pets.',flush=True)

if __name__=='__main__':main()
