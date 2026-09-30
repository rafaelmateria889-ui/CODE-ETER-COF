"""Native smoke runner. ETER_RUNTIME points to an extracted Ikemen GO 1.0.0.
ETER_TEST_DEPS contains an optional extracted Xvfb/xdotool tree under x11/.
The SDL shim disables only CI-unavailable gamepad/sensor enumeration.
"""
import os, subprocess, time, shutil, sys, io
from pathlib import Path
from PIL import ImageGrab
ROOT=Path(__file__).resolve().parents[1]
runtime=Path(os.environ['ETER_RUNTIME']).resolve()
deps=Path(os.environ['ETER_TEST_DEPS']).resolve()
shutil.copytree(ROOT/'game',runtime,dirs_exist_ok=True)
env=os.environ.copy()
env.update(LD_LIBRARY_PATH=str(deps/'x11/usr/lib/x86_64-linux-gnu'),
           LD_PRELOAD=str(deps/'headless_sdl.so'),DISPLAY='127.0.0.1:107',
           SDL_AUDIODRIVER='dummy',SDL_VIDEODRIVER='x11',LIBGL_ALWAYS_SOFTWARE='1')
out=ROOT/'test-output';out.mkdir(exist_ok=True)
debug=runtime/'external/script/debug.lua'
original_debug=debug.read_text()
telemetry=runtime/'telemetry.csv'
telemetry.unlink(missing_ok=True)
debug.write_text(original_debug+'''\n
local eterLog = io.open("telemetry.csv", "w")
local eterFrame = 0
hook.add("loop", "eterSmoke", function()
  eterFrame = eterFrame + 1
  local old = id()
  for i=1,2 do
    if player(i) then
      eterLog:write(string.format("%d,%d,%d,%d,%d,%s\\n", eterFrame, i, stateNo(), life(), power(), tostring(ctrl())))
    end
  end
  playerId(old)
  eterLog:flush()
end)
''')
xf=open(out/'xvfb.log','w');ef=open(out/'engine.log','w')
x=subprocess.Popen([str(deps/'x11/usr/bin/Xvfb'),':107','-screen','0','1280x720x24','-nolisten','unix','-listen','tcp','-ac'],env=env,stdout=xf,stderr=xf)
p=None
try:
    time.sleep(1)
    args=['./Ikemen_GO_Linux','-config','data/eter/config.ini','-nosound']
    if '--menu' not in sys.argv and '--options' not in sys.argv:args+=['-p1','simon','-p2','techblade','-s','lab','-time','99']
    p=subprocess.Popen(args,cwd=runtime,env=env,stdout=ef,stderr=ef)
    def key(k,mode='key'):
        if mode=='key':
            key(k,'keydown');time.sleep(.07);key(k,'keyup');return
        subprocess.run([str(deps/'x11/usr/bin/xdotool'),mode,k],env=env,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    def shot(name):
        data=io.BytesIO();ImageGrab.grab(xdisplay=env['DISPLAY']).save(data,format='PNG')
        tmp=out/f'{name}.tmp';tmp.write_bytes(data.getvalue());tmp.replace(out/f'{name}.png')
    time.sleep(7);shot('menu' if '--menu' in sys.argv else 'idle')
    if '--options' in sys.argv:
        for _ in range(4):key('Down')
        key('Return');time.sleep(2);shot('options')
    elif '--combat' in sys.argv:
        def reset():
            key('F4');time.sleep(3)
        key('d','keydown');time.sleep(.75);key('d','keyup')
        key('Right','keydown');key('h');time.sleep(.6);shot('blocked');key('Right','keyup')
        reset();key('d','keydown');time.sleep(.9);key('d','keyup');key('f+g');time.sleep(.35);shot('throw');time.sleep(1)
        reset();key('F3')
        motion=['keydown','s','sleep','.04','keydown','d','sleep','.04','keyup','s','sleep','.04','keyup','d']
        subprocess.run([str(deps/'x11/usr/bin/xdotool')]+motion+motion+['keydown','f','keydown','h','sleep','.08','keyup','f','keyup','h'],env=env,check=True)
        time.sleep(.3);shot('super');time.sleep(1)
        reset()
        for n in range(28):
            if p.poll() is not None:break
            key('d','keydown');time.sleep(.62);key('d','keyup');key('e');time.sleep(.75)
            if n in [7,15,23]:shot('match-'+str(n))
        shot('match-end')
    elif '--menu' in sys.argv:
        key('Return');time.sleep(2);shot('select')
        key('f');key('i');time.sleep(.6);key('f');time.sleep(8);shot('selected-fight')
    else:
        key('d','keydown');time.sleep(.45);key('d','keyup')
        key('h');time.sleep(.15);shot('attack')
        time.sleep(1);key('e');time.sleep(.25);shot('special')
        time.sleep(1);key('q');time.sleep(.2);shot('portal')
        time.sleep(1);key('w');time.sleep(.2);shot('jump')
        time.sleep(1);key('s','keydown');key('j');time.sleep(.12);shot('sweep');key('s','keyup')
        time.sleep(3);key('p');time.sleep(.25);shot('tech-special')
    print('Native process alive:',p.poll() is None)
finally:
    if p and p.poll() is None:p.terminate();p.wait(timeout=5)
    x.terminate();x.wait(timeout=5)
    debug.write_text(original_debug)
    if telemetry.exists():shutil.copy2(telemetry,out/'telemetry.csv')
print((out/'engine.log').read_text()[-5000:])
if (out/'telemetry.csv').exists():
    lines=[x.split(',') for x in (out/'telemetry.csv').read_text().splitlines() if len(x.split(','))==6]
    for i in ['1','2']:
        rows=[x for x in lines if x[1]==i]
        if rows:print('P'+i,'states:',sorted(set(int(x[2]) for x in rows)),'minimum life:',min(int(x[3]) for x in rows))
