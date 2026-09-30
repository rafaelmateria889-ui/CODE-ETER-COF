"""Original procedural pixel sprites and native MUGEN SFFv1/SND assets.

Rebuild: python tools/build_assets.py (Pillow 11+). No downloaded game art.
Coordinates and palettes are deliberately editable rather than baked AI poses.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io, math, struct, wave, random
from collections import deque

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'game'
KEY = (255, 0, 255)
INK = '#070b13'

def mix(a,b,t): return tuple(x+(y-x)*t for x,y in zip(a,b))
def poly(d,pts,c,outline=INK):
    pts=[(round(x),round(y)) for x,y in pts]
    d.polygon(pts,fill=c)
    if outline:d.line(pts+[pts[0]],fill=outline,width=1)
def segment(d,a,b,w,c,light,armor=False):
    dx,dy=b[0]-a[0],b[1]-a[1]; l=max(1,math.hypot(dx,dy)); nx,ny=-dy/l,dx/l
    p=[(a[0]+nx*w,a[1]+ny*w),(b[0]+nx*w*.65,b[1]+ny*w*.65),(b[0]-nx*w*.65,b[1]-ny*w*.65),(a[0]-nx*w,a[1]-ny*w)]
    poly(d,p,c)
    poly(d,[p[0],p[1],(b[0]+nx*w*.15,b[1]+ny*w*.15),(a[0]+nx*w*.1,a[1]+ny*w*.1)],light,None)
    if armor:
        for t in [.3,.64]:
            m=mix(a,b,t); d.line((m[0]-nx*w*.45,m[1]-ny*w*.45,m[0]+nx*w*.5,m[1]+ny*w*.5),fill='#070c13',width=2)

def ring(d,x,y,t,r=28):
    for k,c in [(8,'#260e28'),(5,'#601a3b'),(3,'#d63356'),(1,'#ffb4be')]:
        d.ellipse((x-r*.38-k,y-r-k,x+r*.38+k,y+r+k),outline=c,width=2)
    for i in range(8):
        a=i*math.pi/4+t*.8
        px=x+math.cos(a)*r*.5; py=y+math.sin(a)*r*1.2
        poly(d,[(px-3,py-2),(px+math.cos(a)*8,py+math.sin(a)*7),(px+3,py+2)],'#ed5372',None)

def fighter(kind,action='idle',t=0):
    im=Image.new('RGB',(256,256),KEY); d=ImageDraw.Draw(im)
    tech=kind=='techblade'; accent='#ff8d32' if tech else '#e84a64'
    # Articulated side-view silhouette; origin at (104, 226).
    hip=[104,151]; chest=[105,108]; head=[107,81]
    bk=[84,185]; bf=[77,223]; fk=[123,186]; ff=[132,223]
    be=[81,130]; bh=[92,115]; fe=[132,121]; fh=[145,101]
    bob=math.sin(t*math.tau)*1.7
    crouch=action in ('crouch','low','cguard')
    if action in ('walk','run'):
        stride=math.sin(t*math.tau); amp=21 if action=='walk' else 29
        bf=[99+stride*amp,222-max(0,stride)*10];ff=[106-stride*amp,222-max(0,-stride)*10]
        bk=mix(hip,bf,.52);bk=(bk[0]-8,bk[1]-5);fk=mix(hip,ff,.5);fk=(fk[0]+10,fk[1]-9)
        if action=='run': chest[0]+=17;head[0]+=22;fe=[145,136];fh=[164,113];be=[79,123];bh=[65,148];bob-=5
    if crouch:
        hip=[99,182];chest=[111,142];head=[115,113];bk=[74,198];bf=[77,224];fk=[132,195];ff=[149,224];be=[92,168];bh=[107,139];fe=[138,158];fh=[145,130]
    if action=='jump':
        hip=[103,156];chest=[107,112];head=[110,85];bk=[81,179];bf=[82,198];fk=[133,166];ff=[116,188];fe=[139,124];fh=[143,97];be=[82,122];bh=[90,98]
    # Attack excursion deliberately uses held anticipation and fast extension.
    q=max(0,math.sin(min(1,t)*math.pi))
    if action in ('punch','heavy','portal','super','throw','upper'):
        chest[0]+=q*8;head[0]+=q*8
        if action=='upper': fe=[127,101-q*22];fh=[124,85-q*47]
        elif action=='throw':fe=[141,120];fh=[147+q*25,100];be=[124,137];bh=[145+q*20,122]
        else:fe=[135+q*17,119-q*10];fh=[140+q*(65 if action=='heavy' else 45),104+q*10]
        if action=='heavy':hip[0]+=q*7;ff[0]+=q*10;head[1]+=q*4
    if action in ('kick','hkick','low'):
        q=max(0,math.sin(t*math.pi));hip[0]-=q*5;chest[0]-=q*12;head[0]-=q*17
        fk=[122+q*26,185-q*(40 if action!='low' else -5)];ff=[131+q*55,223-q*(99 if action=='hkick' else 75 if action=='kick' else 10)]
        fe=[119,124];fh=[130,105]
    if action in ('hurt','guard','cguard'):
        if action=='hurt':chest[0]-=12;head[0]-=21;head[1]+=5;fe=[133,122];fh=[151,133]
        else:fe=[130,chest[1]+13];fh=[128,head[1]+1];be=[122,chest[1]+25];bh=[140,head[1]+15]
    if action=='victory':fe=[125,103];fh=[127,63];be=[81,139];bh=[95,151]
    if action=='down':
        src=fighter(kind,'hurt',0); crop=src.crop((55,55,160,227)).rotate(82,expand=True,resample=Image.Resampling.NEAREST)
        im.paste(crop,(38,224-crop.height)); return im
    points=[hip,chest,head,bk,bf,fk,ff,be,bh,fe,fh]
    points=[(x,y+bob) for x,y in points];hip,chest,head,bk,bf,fk,ff,be,bh,fe,fh=points
    cloth='#182536' if tech else '#202735';hi='#40586c' if tech else '#454e5d';shade='#101725'
    # Rear arm and cape/scarf, articulated legs with layered armor.
    if tech:
        poly(d,[(chest[0]-10,chest[1]-12),(chest[0]-23,chest[1]+13),(hip[0]-34-math.sin(t*6)*5,hip[1]+18),(hip[0]-11,hip[1]+6)],'#111726')
        d.line((chest[0]-20,chest[1]+4,hip[0]-31,hip[1]+13),fill='#34384e',width=2)
    for knee,foot,offset in [(bk,bf,-7),(fk,ff,8)]:
        segment(d,(hip[0]+offset,hip[1]),knee,10,shade if offset<0 else cloth,hi,tech)
        d.ellipse((knee[0]-7,knee[1]-7,knee[0]+7,knee[1]+7),fill='#0c1321',outline='#566271')
        segment(d,knee,(foot[0],foot[1]-7),8,cloth,hi,True)
        poly(d,[(foot[0]-7,foot[1]-13),(foot[0]+6,foot[1]-11),(foot[0]+13,foot[1]-3),(foot[0]+13,foot[1]+1),(foot[0]-10,foot[1]+1)],'#0c111c')
        d.line((foot[0]-9,foot[1]+1,foot[0]+13,foot[1]+1),fill='#ffa15a' if tech else '#657384',width=2)
    segment(d,(chest[0]-13,chest[1]+5),be,7,shade,hi,tech);segment(d,be,bh,6,shade,hi,tech)
    # Tailored coat/vest torso, facets avoid flat stick-figure appearance.
    poly(d,[(chest[0]-17,chest[1]-7),(chest[0]+15,chest[1]-8),(chest[0]+23,chest[1]+14),(hip[0]+14,hip[1]+8),(hip[0]-15,hip[1]+8),(chest[0]-20,chest[1]+15)],cloth)
    poly(d,[(chest[0]-15,chest[1]-6),(chest[0]-3,chest[1]-2),(hip[0]-1,hip[1]+5),(hip[0]-12,hip[1]+5)],shade,None)
    poly(d,[(chest[0]-3,chest[1]-2),(chest[0]+15,chest[1]-6),(chest[0]+17,chest[1]+11),(chest[0]+2,chest[1]+14)],hi)
    poly(d,[(chest[0]+2,chest[1]+16),(chest[0]+17,chest[1]+13),(hip[0]+11,hip[1]-1),(hip[0]+1,hip[1]-1)],'#2b394d')
    if tech:
        d.line((chest[0]+2,chest[1]+3,chest[0]+14,chest[1]+5),fill=accent,width=2)
        for j in range(3):d.line((hip[0]-8,hip[1]-13+j*5,hip[0]+9,hip[1]-12+j*5),fill='#627180',width=1)
    else:
        d.line((chest[0]-8,chest[1]-6,hip[0]+9,hip[1]),fill='#0b121d',width=5)
        for xx in [-8,1,10]:d.rectangle((hip[0]+xx-4,hip[1]-12,hip[0]+xx+2,hip[1]-3),fill='#303b4c',outline='#607080')
    d.line((hip[0]-14,hip[1]+5,hip[0]+14,hip[1]+5),fill='#0a0e18',width=5)
    d.rectangle((hip[0]+1,hip[1]+2,hip[0]+6,hip[1]+7),fill='#939a9d')
    # Neck/head: exposed human face for Simon, entirely concealed metal for Techblade.
    hx,hy=head
    d.rectangle((hx-5,hy+14,hx+5,hy+27),fill='#454657' if tech else '#cda699',outline=INK)
    if tech:
        poly(d,[(hx-13,hy-11),(hx+3,hy-15),(hx+15,hy-7),(hx+15,hy+15),(hx+5,hy+22),(hx-13,hy+17),(hx-19,hy+3)],'#111925')
        poly(d,[(hx-13,hy-9),(hx+2,hy-12),(hx+12,hy-6),(hx-6,hy-3),(hx-10,hy+11)],'#3d4c60')
        poly(d,[(hx-5,hy-2),(hx+13,hy-5),(hx+12,hy+15),(hx+4,hy+19),(hx-7,hy+11)],'#111017')
        d.line((hx-4,hy+2,hx+13,hy),fill='#ff7325',width=3)
        d.line((hx+3,hy+2,hx+13,hy),fill='#fff0b4',width=1)
        poly(d,[(hx,hy+8),(hx+13,hy+5),(hx+10,hy+14),(hx+4,hy+16)],'#434857')
        d.line((hx+6,hy+8,hx+6,hy+15),fill='#ed7335',width=1)
    else:
        poly(d,[(hx-9,hy-7),(hx+8,hy-8),(hx+12,hy),(hx+11,hy+5),(hx+15,hy+8),(hx+10,hy+11),(hx+7,hy+19),(hx-1,hy+21),(hx-9,hy+12)],'#d9b4a4')
        poly(d,[(hx-8,hy),(hx-3,hy+7),(hx-2,hy+18),(hx+7,hy+19),(hx,hy+22),(hx-9,hy+12)],'#9a716b',None)
        d.line((hx+4,hy+3,hx+10,hy+2),fill='#252530',width=2)
        d.point((hx+9,hy+4),fill='#e8e6e0');d.line((hx+6,hy+13,hx+10,hy+12),fill='#754f52')
        poly(d,[(hx-11,hy+12),(hx-15,hy+3),(hx-15,hy-6),(hx-8,hy-12),(hx+3,hy-16),(hx+1,hy-11),(hx+12,hy-9),(hx+15,hy-3),(hx+8,hy-4),(hx+4,hy+3),(hx+1,hy-4),(hx-4,hy+5),(hx-8,hy),(hx-8,hy+13)],'#151725')
        for a,b in [((-10,-7),(-5,-10)),((-7,-4),(0,-10)),((1,-9),(7,-6))]:d.line((hx+a[0],hy+a[1],hx+b[0],hy+b[1]),fill='#44414e')
    # Foreground arm has mechanical knuckles or gloved human hand.
    shoulder=(chest[0]+14,chest[1]+3)
    segment(d,shoulder,fe,9,cloth,hi,tech)
    poly(d,[(shoulder[0]-9,shoulder[1]-5),(shoulder[0]+6,shoulder[1]-8),(shoulder[0]+13,shoulder[1]+3),(shoulder[0]+4,shoulder[1]+10),(shoulder[0]-8,shoulder[1]+7)],hi)
    d.line((shoulder[0]+1,shoulder[1]-5,shoulder[0]+8,shoulder[1]+1),fill=accent,width=2)
    segment(d,fe,fh,7,'#293446' if tech else '#252c39','#71808e' if tech else '#535866',tech)
    d.ellipse((fh[0]-5,fh[1]-5,fh[0]+7,fh[1]+5),fill='#7b858d' if tech else '#151d2a',outline=INK)
    for j in range(3):d.line((fh[0]+j*3,fh[1]-3,fh[0]+j*3,fh[1]+2),fill='#303646' if tech else '#58616c')
    if tech:
        # A sheathed or extended orange blade; all hands remain metal.
        if action in ('heavy','portal','super','upper','punch'):
            dx,dy=(70,-29) if action!='upper' else (10,-78)
            end=(fh[0]+dx,fh[1]+dy)
            if q>.5:
                for off,col in [(11,'#582838'),(6,'#9c4339'),(2,'#ff9341')]:
                    d.arc((fh[0]-20,fh[1]-60,fh[0]+92,fh[1]+45),200,335,fill=col,width=off)
            d.line((fh[0]-8,fh[1]+5,*end),fill='#7d371f',width=7)
            d.line((fh[0],fh[1],*end),fill='#ff902f',width=4)
            d.line((fh[0]+1,fh[1]-1,end[0],end[1]),fill='#fff0b8',width=1)
            d.line((fh[0]-4,fh[1]-6,fh[0]+5,fh[1]+7),fill='#8a8c92',width=3)
        else:
            d.line((bh[0],bh[1],bh[0]-32,bh[1]-58),fill='#13101a',width=6)
            d.line((bh[0],bh[1],bh[0]-32,bh[1]-58),fill='#ee8337',width=2)
    elif action in ('portal','super'):
        ring(d,151,121,t,28)
        if q>.3:
            segment(d,(157,121),(184+q*28,119),11,'#88566a','#dfacb4',True)
            for j in range(4):segment(d,(180+q*28,112+j*5),(194+q*27,114+j*5),2,'#c9a7a8','#f8d3c5')
    elif action=='teleport':
        ring(d,104,151,t,68)
    return im


# GPT Image atlases are retained verbatim in assets/source. Slicing, alpha
# quantization and origin normalization below are build operations for SFFv1.
procedural_fighter = fighter
_atlases = {}
_frames = {}
def fighter(kind,action='idle',t=0):
    if action in ('cpunch','airstrike'):
        row=(0 if action=='cpunch' else 1)+(2 if kind=='techblade' else 0)
        phase=0 if t<.08 else 1 if t<.22 else 2 if t<.35 else 3 if t<.65 else 4 if t<.85 else 5
        return atlas_cell('combat-extra.png',row*6+phase)
    if action in ('servant','tentacle'):
        idx=(0 if action=='servant' else 6)+min(5,int(t*6))
        return atlas_cell('summons.png',idx)
    path=ROOT/'assets/source'/('simon-v2.png' if kind=='simon' else f'{kind}.png')
    if not path.exists():
        out=Image.new('RGB',(384,256),KEY);out.paste(procedural_fighter(kind,action,t),(64,0));return out
    if kind not in _atlases:_atlases[kind]=Image.open(path).convert('RGBA')
    atlas=_atlases[kind]
    if action in ('idle','guard','victory'): idx=min(5,int(t*6)%6)
    elif action in ('walk','run'):idx=6+min(5,int(t*6)%6)
    elif action in ('crouch','cguard'):idx=18
    elif action=='jump':idx=19
    elif action=='hurt':idx=22
    elif action=='down':idx=23
    elif action in ('kick','hkick','low'):
        idx=(21 if action=='low' else 20) if .18<t<.78 else (18 if action=='low' else 0)
    elif action=='teleport':idx=0
    else:
        seq=[0,12,14,15,16,17]
        phase=0 if t<.08 else 1 if t<.20 else 2 if t<.30 else 3 if t<.53 else 4 if t<.78 else 5
        idx=seq[phase]
    if (kind,idx) not in _frames:
        # Generative atlases may extend an extremity beyond a nominal cell.
        # Extract a padded region and discard isolated neighboring fragments.
        cell=atlas.crop(((idx%6)*256-64,(idx//6)*256,(idx%6+1)*256+64,(idx//6+1)*256))
        w,h=cell.size;mask=bytearray(1 if a>=100 else 0 for a in cell.getchannel('A').getdata());components=[]
        for start in range(w*h):
            if not mask[start]:continue
            queue=deque([start]);mask[start]=0;component=[]
            while queue:
                u=queue.popleft();component.append(u);x=u%w;y=u//w
                for v in ([u-1] if x else [])+([u+1] if x<w-1 else [])+([u-w] if y else [])+([u+w] if y<h-1 else []):
                    if mask[v]:mask[v]=0;queue.append(v)
            components.append(component)
        main=max(components,key=len)
        clean=bytearray(w*h)
        for comp in components:
            xs=[u%w for u in comp];ys=[u//w for u in comp]
            # Keep the central figure and its portal/katana effects; no stray feet.
            keep=comp is main or (idx<18 and len(comp)>8 and min(xs)>58 and max(xs)<w-58 and (min(ys)>12 or len(comp)>400))
            if keep:
                for u in comp:clean[u]=255
        alpha=Image.frombytes('L',(w,h),bytes(clean)).resize((261,174),Image.Resampling.NEAREST)
        rgb=cell.convert('RGB').resize((261,174),Image.Resampling.LANCZOS)
        out=Image.new('RGB',(384,256),KEY);out.paste(rgb,(37,64),alpha)
        _frames[(kind,idx)]=out
    out=_frames[(kind,idx)].copy()
    if action=='teleport' and kind=='simon':ring(ImageDraw.Draw(out),168,153,t,69)
    return out

def atlas_cell(filename,idx):
    key=(filename,idx)
    if key not in _frames:
        path=ROOT/'assets/source'/filename
        if not path.exists():return Image.new('RGB',(384,256),KEY)
        atlas=Image.open(path).convert('RGBA')
        cw=atlas.width//6
        cell=atlas.crop(((idx%6)*cw,(idx//6)*cw,(idx%6+1)*cw,(idx//6+1)*cw))
        rgba=cell.resize((174,174),Image.Resampling.LANCZOS)
        mask=rgba.getchannel('A').point(lambda a:255 if a>=100 else 0)
        out=Image.new('RGB',(384,256),KEY);out.paste(rgba.convert('RGB'),(81,64),mask)
        _frames[key]=out
    return _frames[key].copy()

def sff(path,entries):
    """Each sprite contains its own indexed PCX palette; index 0 is transparent."""
    encoded=[]; seen={}
    for group,index,im,ax,ay in entries:
        im=im.convert('RGB'); key=(im.size,im.tobytes())
        if key in seen:
            encoded.append((group,index,b'',ax,ay,seen[key])); continue
        seen[key]=len(encoded)
        pal=im.quantize(colors=254,method=Image.Quantize.MEDIANCUT)
        colors=pal.getpalette(); palette=[*KEY]+colors[:765]; palette+= [0]*(768-len(palette))
        raw=bytes(0 if p==KEY else v+1 for p,v in zip(im.getdata(),pal.getdata()))
        out=Image.frombytes('P',im.size,raw);out.putpalette(palette)
        buf=io.BytesIO();out.save(buf,format='PCX');encoded.append((group,index,buf.getvalue(),ax,ay,0))
    header=b'ElecbyteSpr\0'+bytes([0,0,0,1])+struct.pack('<IIII',len(set(e[0] for e in entries)),len(entries),512,32)+bytes(480)
    assert len(header)==512
    pos=512;data=bytearray(header)
    for i,(g,n,pcx,ax,ay,linked) in enumerate(encoded):
        nextpos=pos+32+len(pcx) if i<len(encoded)-1 else 0
        data+=struct.pack('<IIhhHHHB',nextpos,len(pcx),ax,ay,g,n,linked,0)+bytes(13)+pcx
        pos+=32+len(pcx)
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)

def sound(path):
    chunks=[]
    for i in range(5):
        rng=random.Random(320+i);rate=22050;frames=int(rate*(.12+i*.045));raw=bytearray()
        for k in range(frames):
            t=k/rate;env=(1-k/frames)**2
            freq=170 if i<2 else 430 if i==2 else 76
            val=(math.sin(math.tau*(freq*t-80*t*t))*.45+rng.uniform(-1,1)*.4)*env
            raw+=struct.pack('<h',int(val*19000))
        b=io.BytesIO()
        with wave.open(b,'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(raw)
        chunks.append(b.getvalue())
    data=bytearray(b'ElecbyteSnd\0'+bytes([0,0,0,1])+struct.pack('<II',len(chunks),512)+bytes(488));pos=512
    for i,chunk in enumerate(chunks):
        data+=struct.pack('<IIII',pos+16+len(chunk) if i<len(chunks)-1 else 0,len(chunk),0,i)+chunk;pos+=16+len(chunk)
    path.write_bytes(data)

# action: pose, number of frames, duration per frame. Strike data matches these frames.
ANIMS={0:('idle',12,5),5:('idle',2,2),10:('crouch',2,2),11:('crouch',4,7),12:('idle',2,2),20:('walk',12,3),21:('walk',12,4),40:('crouch',2,2),41:('jump',6,5),42:('jump',6,5),43:('jump',6,5),47:('crouch',2,3),100:('run',12,2),105:('jump',6,3),120:('guard',2,2),130:('guard',4,5),131:('cguard',4,5),132:('guard',4,5),140:('idle',2,2),150:('guard',3,3),151:('guard',3,3),152:('cguard',3,3),153:('cguard',3,3),154:('guard',3,3),170:('victory',6,8),180:('victory',6,8),181:('victory',6,8),190:('idle',8,5),195:('idle',8,5),200:('punch',7,3),210:('kick',9,3),220:('heavy',11,3),230:('hkick',12,3),400:('punch',7,3),410:('low',9,3),420:('heavy',11,3),430:('low',12,3),600:('punch',7,3),610:('kick',9,3),620:('heavy',11,3),630:('hkick',12,3),800:('throw',9,3),810:('throw',12,3),1000:('portal',14,3),1100:('teleport',12,3),1200:('upper',14,3),1300:('throw',14,3),3000:('super',22,3)}
for a in [5000,5001,5002,5010,5011,5012,5020,5021,5022,5030,5035,5040,5050,5060,5070,5080,5081,5090,5100,5101,5102,5110,5120,5150,5200,5210,5300]:ANIMS[a]=('down' if a in [5100,5101,5102,5110,5150] else 'hurt',3,4)

for a in [400,420]:ANIMS[a]=('cpunch',10 if a==420 else 7,3)
for a in [600,610,620,630]:ANIMS[a]=('airstrike',12,3)
ANIMS.update({1310:('throw',16,3),1400:('portal',18,3),1450:('servant',22,3),1460:('tentacle',12,3),3100:('super',19,3)})

def build_char(kind):
    entries=[];air=['; Generated from original GPT Image atlases; effects composited by the build.']
    for action,(pose,n,duration) in ANIMS.items():
        air.append(f'\n[Begin Action {action}]')
        # 640x360 local coordinates; sprites share this geometry.
        low=action in [10,11,400,410,420,430,131,152,153]
        air+=['Clsn2Default: 2',f'Clsn2[0] = -18, {-99 if low else -143}, 22, -62',f'Clsn2[1] = -21, -63, 24, 0']
        attacking=action in [200,210,220,230,400,410,420,430,600,610,620,630,800,1000,1200,1300,3000,1450]
        for i in range(n):
            # Active windows sit in the extended poses, rather than startup.
            active=([11,12,13] if action==1450 else [3,4,5] if action in [1000,1200,1300,3000] else [3,4] if action in [210,410,610] else [4,5] if action in [220,230,420,430,620,630] else [2,3])
            if attacking and i in active:
                reach=114 if action in [1000,3000] else 92 if action in [220,620] and kind=='techblade' else 80 if action in [230,630] else 66
                top,bottom=(-35,-5) if action in [410,430] else (-178,-60) if action==1200 else (-90,-40) if action in [400,420,1450] else (-128,-70)
                air+=['Clsn1: 1',f'Clsn1[0] = 8, {top}, {reach}, {bottom}']
            entries.append((action,i,fighter(kind,pose,i/max(1,n-1)),168,226))
            air.append(f'{action}, {i}, 0, 0, {duration}')
    # Small and large portraits, using our same art, not third-party photographs.
    portrait=fighter(kind).crop((136,70,204,143));entries.append((9000,0,portrait.resize((50,50),Image.Resampling.NEAREST),0,0))
    entries.append((9000,1,fighter(kind).crop((118,49,238,189)),0,0))
    p=OUT/'chars'/kind;p.mkdir(parents=True,exist_ok=True)
    sff(p/f'{kind}.sff',entries);sound(p/f'{kind}.snd');(p/f'{kind}.air').write_text('\n'.join(air)+'\n')
    return entries

def stage():
    im=Image.new('RGB',(960,450),'#0c1220');d=ImageDraw.Draw(im)
    for y in range(450):
        v=max(0,1-abs(y-200)/230); d.line((0,y,960,y),fill=(int(9+v*8),int(15+v*10),int(26+v*15)))
    for x in range(0,960,48):d.line((x,0,x,325),fill='#202d40')
    for y in range(37,325,48):d.line((0,y,960,y),fill='#202d40')
    d.line((0,324,960,324),fill='#6b8396',width=2)
    for y in [339,358,385,422]:d.line((0,y,960,y),fill='#283b50')
    for x in range(-600,1600,90):d.line((480+(x-480)*.45,325,x,450),fill='#26394b')
    for x in range(70,960,175):d.line((x,295,x+42,295),fill='#426274',width=2)
    d.ellipse((340,319,620,382),outline='#405769',width=2)
    d.line((480,326,480,378),fill='#678596');d.line((446,350,514,350),fill='#678596')
    sff(OUT/'stages/lab.sff',[(0,0,im,480,0)])
    # Preview contact sheet for art review and editable source traceability.
    sheet=Image.new('RGB',(1024,512),'#131b29')
    for j,kind in enumerate(['simon','techblade']):
        for k,act in enumerate(['idle','heavy','kick','portal']):
            sprite=fighter(kind,act,.5).crop((64,0,320,256)); mask=sprite.point(lambda _:0).convert('L')
            mask=Image.eval(sprite.convert('RGB').getchannel('G'),lambda v:255 if v else 0)
            # exact color-key mask, preserve dark pixel art colors
            mask=Image.frombytes('L',sprite.size,bytes(0 if px==KEY else 255 for px in sprite.getdata()))
            sheet.paste(sprite,(k*256,j*256),mask)
    (ROOT/'docs').mkdir(exist_ok=True);sheet.save(ROOT/'docs/sprites-preview.png')


def ui():
    def font(n):
        for f in ['/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf','C:/Windows/Fonts/arialbd.ttf']:
            if Path(f).exists():return ImageFont.truetype(f,n)
        return ImageFont.load_default(size=n)
    bg=Image.new('RGB',(1280,720),'#0a101c');d=ImageDraw.Draw(bg)
    for x in range(0,1280,64):d.line((x,0,x-210,720),fill='#101b2b')
    d.line((65,64,1215,64),fill='#52616f',width=1)
    d.text((65,35),'01 / COMBAT PROTOTYPE',font=font(13),fill='#b3c4d1')
    d.text((1010,35),'SIMON  /  TECHBLADE',font=font(13),fill='#b3c4d1')
    title=bg.copy()
    for kind,x in [('simon',15),('techblade',920)]:
        im=fighter(kind).crop((64,0,320,256));alpha=Image.frombytes('L',im.size,bytes(0 if px==KEY else 255 for px in im.getdata()))
        im=im.resize((560,560),Image.Resampling.NEAREST);alpha=alpha.resize((560,560),Image.Resampling.NEAREST)
        title.paste(im,(x-80,80),alpha)
    d=ImageDraw.Draw(title)
    d.text((640,118),'CODE',font=font(38),fill='#a2b8ca',anchor='mt')
    d.text((640,157),'ETER',font=font(116),fill='#eff2ef',anchor='mt',stroke_width=1)
    d.text((640,300),'PORTALS  /  STEEL  /  IMPACT',font=font(14),fill='#da9b64',anchor='mt')
    d.line((530,342,750,342),fill='#dc8951',width=2)
    d.text((640,683),'1 CONTRA 1    -    TECLADO + CONTROLE',font=font(13),fill='#8fa5b7',anchor='mt')
    entries=[(0,0,title,640,0),(1,0,bg,640,0)]
    for group,color in [(100,'#304455'),(101,'#ef6984'),(102,'#ffad5a')]:
        im=Image.new('RGB',(104,104),KEY if group!=100 else '#182938');d=ImageDraw.Draw(im)
        d.rectangle((0,0,103,103),outline=color,width=3)
        entries.append((group,0,im,0,0))
    sff(OUT/'data/eter/ui.sff',entries)

if __name__=='__main__':
    for kind in ['simon','techblade']:
        es=build_char(kind);print(kind,len(es),'frames', (OUT/'chars'/kind/f'{kind}.sff').stat().st_size,'bytes')
    stage();ui()
