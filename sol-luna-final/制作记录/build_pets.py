#!/usr/bin/env python3
"""Extract generated artwork, align sequences and build native v2 pet packages.

Pillow + NumPy only. Originals are read-only. Connected parts are associated
with frame regions, so question marks and sleep/stars survive extraction.
"""
from pathlib import Path
from collections import defaultdict
import json, hashlib, math, zipfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'制作记录/原始素材'
OUT=ROOT/'预览'
COUNTS=[6,8,8,4,5,8,6,6,6,8,8]
STATES=['idle','running-right','running-left','waving','jumping','failed','waiting','running','review']
TIMES=[[1680,660,660,840,840,1920],[120]*7+[220],[120]*7+[220],
       [140]*3+[280],[140]*4+[280],[140]*7+[240],[150]*5+[260],
       [120]*5+[220],[150]*5+[280]]
GRIDS={'idle':(6,2),'work':(6,2),'flight':(8,4),'waiting':(6,2),
       'failed':(5,3),'social':(6,6),'gaze':(8,4)}

def components(mask):
    """Run-length connected components, avoiding per-pixel Python flood fill."""
    parents=[];runs=[];previous=[]
    def root(i):
        while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
        return i
    for y,row in enumerate(mask):
        edges=np.flatnonzero(np.diff(np.pad(row.astype(np.int8),(1,1))))
        current=[];j=0
        for left,right in zip(edges[::2],edges[1::2]):
            left=int(left);right=int(right);i=len(parents);parents.append(i)
            while j<len(previous) and previous[j][1]<left:j+=1
            k=j
            while k<len(previous) and previous[k][0]<=right:
                a=root(i);b=root(previous[k][2]);parents[a]=b;k+=1
            current.append((left,right,i));runs.append((y,left,right,i))
        previous=current
    groups=defaultdict(list)
    for y,l,r,i in runs:groups[root(i)].append((y,l,r))
    result=[]
    for rr in groups.values():
        area=sum(r-l for y,l,r in rr)
        if area<5:continue
        box=[min(l for y,l,r in rr),min(y for y,l,r in rr),max(r for y,l,r in rr),max(y for y,l,r in rr)+1]
        result.append({'area':area,'box':box,'runs':rr})
    return result

def mask_from_rgb(rgb,name):
    a=rgb.astype(np.int16)
    # Generated checkerboards are near-neutral; ivory interiors are enclosed
    # by colored feather outlines and recovered with exterior flood fill.
    # Work sheet has a light checkerboard and low-chroma slate laptop lids.
    # Its dark threshold preserves the complete lid, not just the gold emblem.
    seed=((a.max(2)-a.min(2))>20)|(a.max(2)<(150 if name=='work' else 105))
    im=Image.fromarray(seed.astype('uint8')*255).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    pad=Image.new('L',(im.width+2,im.height+2),0);pad.paste(im,(1,1))
    ImageDraw.floodfill(pad,(0,0),128)
    return np.asarray(pad)[1:-1,1:-1]!=128

def rgba_cut(rgb,mask):
    hard=Image.fromarray(mask.astype('uint8')*255)
    alpha=np.asarray(hard.filter(ImageFilter.GaussianBlur(.35))).copy()
    alpha[alpha<5]=0;alpha[alpha>250]=255
    inside=np.asarray(hard.filter(ImageFilter.MinFilter(5)))>0
    colors=rgb.astype(float);sums=np.zeros_like(colors);weights=np.zeros(mask.shape)
    for dy in range(-3,4):
        for dx in range(-3,4):
            wt=1/(1+dx*dx+dy*dy);m=np.roll(inside,(dy,dx),(0,1))
            sums+=np.roll(colors,(dy,dx),(0,1))*m[:,:,None]*wt;weights+=m*wt
    edge=(alpha>0)&~inside&(weights>0);clean=rgb.copy()
    clean[edge]=np.clip(sums[edge]/weights[edge,None],0,255).astype('uint8');clean[alpha==0]=0
    return Image.fromarray(np.dstack([clean,alpha]))

def extract(name):
    cols,rows=GRIDS[name];source=Image.open(SRC/(name+'.png')).convert('RGBA');rgb=np.asarray(source)[:,:,:3]
    genuine_alpha=np.asarray(source)[:,:,3].min()<250
    mask=np.asarray(source)[:,:,3]>8 if genuine_alpha else mask_from_rgb(rgb,name)
    cc=components(mask);mains=[c for c in cc if c['area']>1200]
    print(name,source.size,'large components',len(mains),flush=True)
    assert len(mains)==cols*rows,(name,len(mains),[(c['area'],c['box']) for c in mains])
    ys=np.array([(c['box'][1]+c['box'][3])/2 for c in mains]);centers=np.linspace(ys.min(),ys.max(),rows)
    for _ in range(20):
        labels=np.abs(ys[:,None]-centers).argmin(1)
        centers=np.array([np.mean(ys[labels==r]) for r in range(rows)])
    ordered=[]
    for row in range(rows):
        group=sorted([c for c,k in zip(mains,labels) if k==row],key=lambda c:c['box'][0])
        assert len(group)==cols,(name,row,len(group));ordered+=group
    extra=[c for c in cc if c['area']<=1200]
    assigned=defaultdict(list)
    # Distance to the character rectangle associates disconnected effect parts.
    for c in extra:
        x=(c['box'][0]+c['box'][2])/2;y=(c['box'][1]+c['box'][3])/2
        distances=[]
        for m in ordered:
            l,t,r,b=m['box'];dx=max(l-x,0,x-r);dy=max(t-y,0,y-b)
            distances.append(dx*dx+dy*dy)
        best=int(np.argmin(distances))
        if distances[best]<(source.width/cols*.45)**2:assigned[best].append(c)
    frames=[];records=[]
    for i,m in enumerate(ordered):
        parts=[m]+assigned[i];allmask=np.zeros(mask.shape,dtype=bool)
        for c in parts:
            for y,l,r in c['runs']:allmask[y,l:r]=True
        nonzero=np.argwhere(allmask);top,left=nonzero.min(0);bottom,right=nonzero.max(0)+1
        l=max(0,int(left)-5);t=max(0,int(top)-5);r=min(source.width,int(right)+5);b=min(source.height,int(bottom)+5)
        cut=source.crop((l,t,r,b)) if genuine_alpha else rgba_cut(rgb[t:b,l:r],allmask[t:b,l:r])
        main=[m['box'][0]-l,m['box'][1]-t,m['box'][2]-l,m['box'][3]-t]
        frames.append({'image':cut,'main':main,'asset':name,'index':i})
        records.append({'index':i,'sourceBox':[l,t,r,b],'mainBox':m['box'],'effectComponentCount':len(parts)-1})
    return frames,{'source':name+'.png','sourceMode':Image.open(SRC/(name+'.png')).mode,'genuineSourceAlpha':bool(genuine_alpha),'frames':records}

def body_anchor(frame):
    """Find gold chest badge, disambiguated from eyes and cape embroidery."""
    im=frame['image'];rgb=np.asarray(im)[:,:,:3].astype(float);l,t,r,b=frame['main'];w=r-l;h=b-t
    gold=(rgb[:,:,0]>145)&(rgb[:,:,1]>85)&(rgb[:,:,0]>rgb[:,:,2]*1.27)&(rgb[:,:,1]>rgb[:,:,2]*1.12)
    yy,xx=np.indices(gold.shape);cx=l+w*.5;cy=t+h*.63
    if frame['asset']=='flight':cx=l+w*.79;cy=t+h*.64
    if frame['asset']=='waiting':cx=l+w*.45
    if frame['asset']=='work':cx=l+w*.48
    if frame['asset']=='gaze':cy=t+h*.67
    region=(abs(xx-cx)<w*.17)&(abs(yy-cy)<h*.13)
    points=gold&region
    if points.sum()<8:return cx,cy
    weights=np.exp(-((xx-cx)/(w*.09))**2-((yy-cy)/(h*.08))**2)*points
    return float((xx*weights).sum()/weights.sum()),float((yy*weights).sum()/weights.sum())

def align(frames,kind,standing_height=None):
    heights=[f['main'][3]-f['main'][1] for f in frames]
    scale=160/(standing_height or max(heights))
    anchors=[body_anchor(f) for f in frames]
    if kind=='flight':
        # Use beak-side body landmark; one scale and one body plane for all phases.
        # Anchor is the bottom-right body extent for flight, independent of wings.
        anchors=[]
        for f in frames:
            l,t,r,b=f['main'];rgb=np.asarray(f['image'])[:,:,:3];a=np.asarray(f['image'])[:,:,3]
            # Forward-most 30% contains owl face, not the trailing wing fan.
            region=np.zeros(a.shape,bool);region[:,round(l+(r-l)*.72):r]=True
            y,x=np.where((a>128)&region)
            anchors.append((float(np.max(x)),float(np.median(y))))
        extents=[(a[0],a[1],f['image'].width-a[0],f['image'].height-a[1]) for f,a in zip(frames,anchors)]
        left=max(e[0] for e in extents);up=max(e[1] for e in extents);right=max(e[2] for e in extents);down=max(e[3] for e in extents)
        scale=min(176/(left+right),180/(up+down));target=(8+left*scale,12+up*scale)
    else:
        target=(80 if kind=='work' else 96,0)
        # Keep feet fixed. Never recenter or resize individual extended-wing frames.
        sx=[]
        for f,a in zip(frames,anchors):
            xanchor=f['main'][2] if kind=='work' else a[0]
            destx=182 if kind=='work' else target[0]
            sx.append(min((destx-6)/max(xanchor,1),(186-destx)/max(f['image'].width-xanchor,1)))
        scale=min(scale,min(sx),182/max(f['image'].height for f in frames))
    result=[];audit=[]
    for i,(f,a) in enumerate(zip(frames,anchors)):
        src=f['image'];w=max(1,round(src.width*scale));h=max(1,round(src.height*scale))
        obj=src.resize((w,h),Image.Resampling.LANCZOS);cell=Image.new('RGBA',(192,208))
        if kind=='flight':x=round(target[0]-a[0]*scale);y=round(target[1]-a[1]*scale)
        elif kind=='work':x=round(182-f['main'][2]*scale);y=round(190-f['main'][3]*scale)
        else:x=round(96-a[0]*scale);y=round(190-f['main'][3]*scale)
        if kind=='jump' and i==2:y-=13
        cell.alpha_composite(obj,(x,y));result.append(cell)
        audit.append({'asset':f['asset'],'sourceIndex':f['index'],'scale':scale,'paste':[x,y],'sourceMainBox':f['main'],'sourceAnchor':list(a)})
    return result,audit

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    OUT.mkdir(parents=True,exist_ok=True);raw={};sources=[]
    for key in GRIDS:raw[key],rec=extract(key);sources.append(rec)
    all_reports=[];all_frames={}
    for pet,p in [('sol',0),('luna',1)]:
        r={};audit={}
        idle=raw['idle'][p*6:p*6+6];r['idle'],audit['idle']=align(idle,'idle');r['idle'][-1]=r['idle'][0].copy()
        # User-approved fallback: flight trial had inconsistent wing/cape occlusion.
        # Preserve both original running sequences exactly, without mirroring badges.
        movement=Image.open(SRC/('original-running-'+pet+'.webp')).convert('RGBA')
        for state,mrow in [('running-right',0),('running-left',1)]:
            r[state]=[movement.crop((i*192,mrow*208,(i+1)*192,(mrow+1)*208)) for i in range(8)]
            audit[state]={'source':'original-running-'+pet+'.webp','preservedPixels':True,'flightTrialRejected':'Wing/cape occlusion inconsistent between phases'}
        social=raw['social'][p*18:p*18+18]
        r['waving'],audit['waving']=align([social[i] for i in [0,1,2,1]],'wave',social[0]['main'][3]-social[0]['main'][1])
        r['jumping'],audit['jumping']=align([social[i] for i in [6,7,8,7,6]],'jump',social[6]['main'][3]-social[6]['main'][1])
        r['jumping'][0]=r['idle'][0].copy();r['jumping'][-1]=r['idle'][0].copy()
        # Choose the coherent 4-pose segment from the generated failed sheet.
        fail=raw['failed'][0:4] if p==0 else raw['failed'][10:14]
        r['failed'],audit['failed']=align([fail[i] for i in [0,1,2,3,3,2,1,0]],'failed',fail[0]['main'][3]-fail[0]['main'][1])
        r['failed'][0]=r['idle'][0].copy();r['failed'][-1]=r['idle'][0].copy()
        r['waiting'],audit['waiting']=align(raw['waiting'][p*6:p*6+6],'waiting');r['waiting'][-1]=r['waiting'][0].copy()
        r['running'],audit['running']=align(raw['work'][p*6:p*6+6],'work')
        # The generated fifth book pose dropped the book. Never select that frame.
        book=social[12:18];r['review'],audit['review']=align([book[i] for i in [0,1,2,3,2,1]],'review')
        look,audit['look']=align(raw['gaze'][p*16:p*16+16],'gaze')
        frames=[]
        for state in STATES:
            frames.extend(r[state]);frames.extend([r['idle'][0].copy()]*(8-len(r[state])))
        frames+=look
        atlas=Image.new('RGBA',(1536,2288))
        for i,f in enumerate(frames):atlas.alpha_composite(f,((i%8)*192,(i//8)*208))
        dest=ROOT/'可直接安装'/pet;dest.mkdir(parents=True,exist_ok=True)
        atlas.save(dest/'spritesheet.webp',lossless=True,exact=True,method=6)
        meta={'id':pet,'displayName':'Sol · 晨光' if pet=='sol' else 'Luna · 月夜','description':'好奇观察、整理披风与思考工作。Curiosity, cape care and thoughtful work.' if pet=='sol' else '整理披风、深夜犯困与思考工作。Cape care, sleepy nights and thoughtful work.','spriteVersionNumber':2,'spritesheetPath':'spritesheet.webp'}
        (dest/'pet.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
        reopened=Image.open(dest/'spritesheet.webp').convert('RGBA');assert np.array_equal(np.asarray(atlas),np.asarray(reopened))
        checks=[]
        for i,f in enumerate(frames):
            box=f.getbbox();a=np.asarray(f)[:,:,3];assert box,(pet,i)
            assert box[0]>=3 and box[1]>=3 and box[2]<=189 and box[3]<=204,(pet,i,box)
            checks.append({'index':i,'box':list(box),'transparentFraction':round(float((a==0).mean()),4)})
        frames[0].save(OUT/(pet+'-idle.png'))
        for state,times in zip(STATES,TIMES):
            seq=r[state];seq[0].save(OUT/(pet+'-'+state+'.webp'),save_all=True,append_images=seq[1:],duration=times,loop=0,lossless=True,method=6)
        # Thinking-only is an explicitly labeled preview, not an extra native state.
        think=[r['running'][i] for i in [1,2,3,2]]
        think[0].save(OUT/(pet+'-thinking.webp'),save_all=True,append_images=think[1:],duration=[500,850,500,650],loop=0,lossless=True)
        sheet=Image.new('RGB',(1536,2288),(221,224,230))
        for i,f in enumerate(frames):sheet.paste(f,((i%8)*192,(i//8)*208),f)
        sheet.save(OUT/(pet+'-全帧检查.jpg'),quality=95)
        all_reports.append({'pet':pet,'spriteSha256':sha(dest/'spritesheet.webp'),'frameCount':88,'frames':checks,'alignment':audit,'losslessPixelRoundtrip':True})
        all_frames[pet]=r
    report={'status':'assembled-awaiting-visual-QA','nativeAppSelectedAndPlayed':False,'format':{'version':2,'width':1536,'height':2288,'counts':COUNTS},'sources':sources,'pets':all_reports,'decisions':{'solIdle':'curious + cape care','lunaIdle':'cape care + drowsy','work':'persistent laptop, think then type','failed':'folded wings, hunched shoulders and recover','movement':'original running; user-authorized fallback from inconsistent flight trial'}}
    (ROOT/'制作记录/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    with zipfile.ZipFile(ROOT/'Sol-Luna-安装包.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted((ROOT/'可直接安装').rglob('*')):
            if p.is_file():z.write(p,p.relative_to(ROOT/'可直接安装'))
    print('Built both native packages; visual QA still required.',flush=True)

if __name__=='__main__':main()
