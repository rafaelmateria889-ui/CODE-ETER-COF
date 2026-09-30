"""Authoritative editable move data -> native Ikemen GO v1.0.0 CNS and CMD."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def ctrl(label,typ,trig,body):return f'\n[State 0, {label}]\ntype = {typ}\n{trig}\n{body}\n'
def state(num,anim=None,stance='S',move='A',physics=None):
    return f'\n[Statedef {num}]\ntype = {stance}\nmovetype = {move}\nphysics = {physics or stance}\nanim = {anim if anim is not None else num}\nctrl = 0\n'+('velset = 0,0\n' if stance!='A' else '')
def hit(damage,stance='S',low=False,fall=False,super=False,special=False):
    return f'''attr = {stance},{'HA' if super else 'SA' if special else 'NA'}
damage = {damage},{int(damage*.06) if special else 0}
animtype = {'Hard' if damage>60 else 'Light'}
guardflag = {'L' if low else 'HA' if stance=='A' else 'MA'}
hitflag = MAF
priority = 4,Hit
pausetime = {10 if damage>60 else 7},{10 if damage>60 else 7}
sparkno = 2
guard.sparkno = 40
sparkxy = -10,-95
hitsound = S0,{1 if damage>60 else 0}
guardsound = S0,0
ground.type = {'Low' if low else 'High'}
ground.slidetime = 16
ground.hittime = {22 if damage>60 else 16}
ground.velocity = -5,{'-8' if fall else '0'}
guard.velocity = -4
air.type = High
air.velocity = -5,-7
air.hittime = 22
fall = {int(fall)}
fall.recover = 1
getpower = {0 if super else 45},18
givepower = 25,12'''
def build(kind):
    tech=kind=='techblade';name='Techblade' if tech else 'Simon'
    p=ROOT/'game/chars'/kind;p.mkdir(parents=True,exist_ok=True)
    (p/f'{kind}.def').write_text(f'''[Info]
name = "{name}"
displayname = "{name}"
versiondate = 09,29,2026
mugenversion = 1.0
author = "CODE-ETER-COF / Rafael Materia"
localcoord = 640,360
pal.defaults = 1
[Files]
cmd = {kind}.cmd
cns = {kind}.cns
st = {kind}.cns
stcommon = common1.cns
sprite = {kind}.sff
anim = {kind}.air
sound = {kind}.snd
movelist = movelist.dat
''')
    cns=f'''[Data]
life = 1000
power = 3000
attack = 100
defence = 100
fall.defence_up = 30
liedown.time = 26
airjuggle = 12
sparkno = 2
guard.sparkno = 40
KO.echo = 0
volume = 0
[Size]
xscale = 1
yscale = 1
ground.back = 18
ground.front = 20
air.back = 15
air.front = 15
height = 148
attack.dist = 105
proj.attack.dist = 110
head.pos = 3,-143
mid.pos = 0,-85
shadowoffset = 0
[Velocity]
walk.fwd = {4.1 if tech else 3.8}
walk.back = -3.1
run.fwd = {7.6 if tech else 7.0},0
run.back = -6.5,-4.6
jump.neu = 0,-12.0
jump.back = -4.5
jump.fwd = 4.6
runjump.back = -4.5,-11.5
runjump.fwd = 7.0,-11.5
air.gethit.groundrecover = -.2,-5.5
air.gethit.airrecover.mul = .5,.2
air.gethit.airrecover.add = 0,-6
air.gethit.airrecover.back = -2
air.gethit.airrecover.fwd = 2
air.gethit.airrecover.up = -3
air.gethit.airrecover.down = 2
[Movement]
airjump.num = 0
airjump.height = 70
yaccel = .65
stand.friction = .80
crouch.friction = .82
stand.friction.threshold = .2
crouch.friction.threshold = .2
air.gethit.groundlevel = 25
air.gethit.groundrecover.ground.threshold = -30
air.gethit.groundrecover.groundlevel = 15
air.gethit.airrecover.threshold = -1
air.gethit.airrecover.yaccel = .5
air.gethit.trip.groundlevel = 20
down.bounce.offset = 0,30
down.bounce.yaccel = .5
down.bounce.groundlevel = 20
down.friction.threshold = .1
'''
    for num in [170,180,190]:
        cns+=state(num,move='I')
        if num==190:cns+=ctrl('Ready','ChangeState','trigger1 = Time >= 30','value = 0\nctrl = 1')
    cns+=state(100,move='I').replace('ctrl = 0','ctrl = 1')+ctrl('Run','VelSet','trigger1 = 1','x = const(velocity.run.fwd.x)')
    cns+=ctrl('Stop','ChangeState','trigger1 = command != "holdfwd"','value = 0\nctrl = 1')
    cns+=state(105,stance='A',move='I')+ctrl('Hop','VelSet','trigger1 = Time = 0','x = -6.5\ny = -4.6')
    cns+=ctrl('Land','ChangeState','trigger1 = Vel Y > 0 && Pos Y >= 0','value = 0\nctrl = 1')
    table=[]
    for base,stance in [(200,'S'),(400,'C'),(600,'A')]:
        for i,(button,damage,length) in enumerate([('x',38,21),('a',52,27),('y',78,33),('b',92,36)]):
            num=base+i*10;low=stance=='C' and i in [1,3]
            cns+=state(num,stance=stance)+'juggle = 4\n'
            cns+=ctrl('Swing','PlaySnd','trigger1 = Time = 2',f'value = 0,{2 if tech and i==2 else 0}')
            cns+=ctrl('Strike','HitDef','trigger1 = Time = 6',hit(damage,stance,low,low and i==3))
            cns+=ctrl('Recover','ChangeState',f'trigger1 = Time >= {length}',f'value = {50 if stance=="A" else 11 if stance=="C" else 0}\nctrl = 1')
            table.append(dict(state=num,button=button,stance=stance,startup=6,active=6,total=length,damage=damage,low=low))
    for num in [800,1300] if not tech else [800]:
        cns+=state(num)
        cns+=ctrl('Grab','HitDef','trigger1 = Time = 6\ntrigger1 = P2BodyDist X < 32\ntrigger1 = P2StateType != A\ntrigger1 = P2MoveType != H',f'''attr = S,{'NT' if num==800 else 'ST'}
hitflag = M-
priority = 1,Miss
pausetime = 0,0
sparkno = -1
guard.sparkno = -1
hitsound = S0,3
p1stateno = 810
p2stateno = 820
fall = 1
getpower = 70
givepower = 40''')
        cns+=ctrl('Damage','VarSet','trigger1 = Time = 0',f'v = 0\nvalue = {135 if num==800 else 175}')
        cns+=ctrl('Whiff','ChangeState','trigger1 = Time >= 32','value = 0\nctrl = 1')
    cns+=state(810)
    cns+=ctrl('Hold','TargetBind','trigger1 = Time < 15','pos = 35,-45')
    cns+=ctrl('Damage','TargetLifeAdd','trigger1 = Time = 15','value = -var(0)\nkill = 1')
    cns+=ctrl('Throw','TargetState','trigger1 = Time = 15','value = 821')
    cns+=ctrl('Recover','ChangeState','trigger1 = Time >= 35','value = 0\nctrl = 1')
    # Custom victim states must use the victim's own common falling physics afterwards.
    cns+='\n[Statedef 820]\ntype = A\nmovetype = H\nphysics = N\nctrl = 0\nvelset = 0,0\n'
    cns+=ctrl('Victim animation','ChangeAnim2','trigger1 = Time = 0','value = 5000')
    cns+=ctrl('Fail safe','SelfState','trigger1 = Time >= 60','value = 5050')
    cns+='\n[Statedef 821]\ntype = A\nmovetype = H\nphysics = N\nctrl = 0\nvelset = -7,-9\n'
    cns+=ctrl('Fall','SelfState','trigger1 = 1','value = 5050')
    specials=[(1000,100,42,'Investida Ignea' if tech else 'Mao do Limiar'),(1200,125,42,'Corte Ascendente' if tech else 'Ruptura Ascendente'),(3000,255,66,'Sobrecarga da Lamina' if tech else 'Brecha Entre Mundos')]
    if tech:specials.append((1300,90,42,'Corte de Pressao'))
    for num,damage,length,title in specials:
        cns+=f'\n; {title}\n'+state(num)+'juggle = 8\n'
        if num==3000:
            cns+='poweradd = -1000\n'
            cns+=ctrl('Super flash','SuperPause','trigger1 = Time = 0','time = 18\nmovetime = 0\nanim = -1\nsound = S0,4\ndarken = 1\np2defmul = 1')
        if tech and num==1000:cns+=ctrl('Drive','VelSet','trigger1 = Time >= 5 && Time < 16','x = 8.5')
        if num==1200:
            cns+=ctrl('Launch','VelSet','trigger1 = Time = 8','x = 2.5\ny = -9')
            cns+=ctrl('Air','StateTypeSet','trigger1 = Time = 8','statetype = A\nphysics = A')
        cns+=ctrl('Audio','PlaySnd','trigger1 = Time = 5',f'value = 0,{2 if tech else 3}')
        cns+=ctrl('Hit','HitDef','trigger1 = Time = 9',hit(damage,fall=num in [1200,3000],super=num==3000,special=True))
        cns+=ctrl('Recover','ChangeState',f'trigger1 = Time >= {length}',f'value = {50 if num==1200 else 0}\nctrl = 1')
        table.append(dict(state=num,name=title,startup=9,active=9,total=length,damage=damage))
    cns+=state(1100,move='I')
    if tech:cns+=ctrl('Step','VelSet','trigger1 = Time >= 5 && Time < 14','x = 9')
    else:
        cns+=ctrl('Travel','PosAdd','trigger1 = Time = 14','x = min(170,frontedgedist-26)')
        cns+=ctrl('Intangible','NotHitBy','trigger1 = Time >= 12 && Time < 17','value = SCA\ntime = 1')
        cns+=ctrl('Push','PlayerPush','trigger1 = Time >= 12 && Time < 17','value = 0')
        cns+=ctrl('Color','PalFX','trigger1 = Time = 11','time = 8\nadd = 90,-30,10\nmul = 256,150,180')
    cns+=ctrl('Recover','ChangeState','trigger1 = Time >= 36','value = 0\nctrl = 1')
    cns+='\n[Statedef -2]\n'
    cns+=ctrl('AI walk','ChangeState','triggerall = AILevel > 0\ntriggerall = RoundState = 2\ntriggerall = Ctrl\ntriggerall = StateType = S\ntrigger1 = P2BodyDist X > 90','value = 20')
    cns+=ctrl('AI attack','ChangeState','triggerall = AILevel > 0\ntriggerall = RoundState = 2\ntriggerall = Ctrl\ntriggerall = StateType != A\ntrigger1 = P2BodyDist X < 90 && Random < 80','value = ifelse(Random < 450,200,ifelse(Random < 700,220,1000))')
    (p/f'{kind}.cns').write_text(cns)
    cmd='[Remap]\nx = x\na = a\ny = y\nb = b\n[Defaults]\ncommand.time = 22\ncommand.buffer.time = 4\n'
    for name_,seq,time in [('super','~D, DF, F, D, DF, F, x+y',32),('qcf','~D, DF, F, x',24),('qcb','~D, DB, B, x',24),('dp','F, D, DF, x',24),('grab','x+a',1),('dash','F,F',12),('backdash','B,B',12),('step','~D, DB, B, a',24),('throwsp','F,D,DF,a',24)]:
        cmd+=f'\n[Command]\nname = "{name_}"\ncommand = {seq}\ntime = {time}\n'
    for button in ['x','a','y','b','c','z']:
        cmd+=f'\n[Command]\nname = "{button}"\ncommand = {button}\ntime = 1\n'
    for name_,s in [('holdfwd','/$F'),('holdback','/$B'),('holdup','/$U'),('holddown','/$D')]:
        cmd+=f'\n[Command]\nname = "{name_}"\ncommand = {s}\ntime = 1\nbuffer.time = 1\n'
    cmd+='\n[Statedef -1]\n'
    routes=[('super',3000),('dp',1200),('qcf',1000 if tech else 1100),('qcb',1300 if tech else 1000),('step',1100),('throwsp',1300 if not tech else 1200)]
    for command,num in routes:
        trig=f'triggerall = AILevel = 0\ntriggerall = RoundState = 2\ntriggerall = StateType != A\ntriggerall = command = "{command}"\n'
        if num==3000:trig+='triggerall = Power >= 1000\n'
        trig+='trigger1 = Ctrl\ntrigger2 = MoveContact && (StateNo = 200 || StateNo = 210 || StateNo = 220 || StateNo = 400 || StateNo = 410 || StateNo = 420)'
        cmd+=ctrl(command,'ChangeState',trig,f'value = {num}')
    for command,num in [('c',1000),('z',1100),('grab',800),('dash',100),('backdash',105)]:
        cmd+=ctrl(command,'ChangeState',f'triggerall = AILevel = 0\ntriggerall = RoundState = 2\ntriggerall = command = "{command}"\ntriggerall = StateType != A\ntrigger1 = Ctrl',f'value = {num}')
    for i,button in enumerate(['x','a','y','b']):
        cmd+=ctrl('Normal '+button,'ChangeState',f'triggerall = AILevel = 0\ntriggerall = RoundState = 2\ntriggerall = command = "{button}"\ntrigger1 = Ctrl',f'value = ifelse(StateType = A,{600+i*10},ifelse(command = "holddown",{400+i*10},{200+i*10}))')
    for button,num in [('y',220),('b',230)]:
        cmd+=ctrl('Chain '+button,'ChangeState',f'triggerall = AILevel = 0\ntriggerall = command = "{button}"\ntriggerall = MoveContact\ntrigger1 = StateNo = 200 || StateNo = 210',f'value = {num}')
    (p/f'{kind}.cmd').write_text(cmd)
    (p/'movelist.dat').write_text(f'''{name.upper()} / PROTOTIPO 0.1

X = soco leve   A = chute leve
Y = soco forte  B = chute forte
Frente, frente : corrida
Tras, tras : recuo
Tras / baixo+tras : defesa alta / baixa
X + A : agarrao normal (perto)

C / RT : {'Investida Ignea' if tech else 'Mao do Limiar'}
Z / RB : {'Passo Fantasma' if tech else 'Fenda de Entrada'}
Baixo, diagonal frente, frente + X : {'Investida Ignea' if tech else 'Fenda de Entrada'}
Baixo, diagonal tras, tras + X : {'Corte de Pressao' if tech else 'Mao do Limiar'}
Frente, baixo, diagonal frente + X : {'Corte Ascendente' if tech else 'Ruptura Ascendente'}
Frente, baixo, diagonal frente + A : {'Corte Ascendente' if tech else 'Abraco do Abismo'}
Duplo quarto de lua para frente + X+Y : super (1 barra)
Leve > forte > especial: cancela ao acertar/defender.
''')
    return table
if __name__=='__main__':
    tables={k:build(k) for k in ['simon','techblade']}
    (ROOT/'docs/frame-data.json').write_text(json.dumps(tables,indent=2)+'\n')
    print('Generated both characters and frame data.')

