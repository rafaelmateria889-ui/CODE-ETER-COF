"""Two official native instances on loopback. NOT a two-network acceptance test.
Same ETER_RUNTIME/ETER_TEST_DEPS as native_smoke.py. No engine logic is changed.
"""
import os,shutil,subprocess,time,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=Path(os.environ['ETER_RUNTIME']);deps=Path(os.environ['ETER_TEST_DEPS'])
out=ROOT/'test-output/network';out.mkdir(parents=True,exist_ok=True)
env=os.environ.copy();env.update(LD_LIBRARY_PATH=str(deps/'x11/usr/lib/x86_64-linux-gnu'),LD_PRELOAD=str(deps/'headless_sdl.so'),DISPLAY='127.0.0.1:108',SDL_AUDIODRIVER='dummy',SDL_VIDEODRIVER='x11',LIBGL_ALWAYS_SOFTWARE='1')
telemetry='''\nlocal eterNetLog = io.open("net-test.csv", "w")
hook.add("loop", "eterNetwork", function()
 local old=id()
 for i=1,2 do
  if player(i) then eterNetLog:write(string.format("%d,%d,%d,%d,%d,%d\\n",gameTime(),i,stateNo(),life(),power(),numHelper(1450))) end
 end
 playerId(old);eterNetLog:flush()
end)
'''
xf=open(out/'xvfb.log','w');x=subprocess.Popen([str(deps/'x11/usr/bin/Xvfb'),':108','-screen','0','1280x720x24','-nolisten','unix','-listen','tcp','-ac'],env=env,stdout=xf,stderr=xf)
processes=[];runtimes=[]
try:
 time.sleep(1)
 for i in range(2):
  runtime=deps/f'net-test-{i}';shutil.copytree(source,runtime,dirs_exist_ok=True);shutil.copytree(ROOT/'game',runtime,dirs_exist_ok=True);runtimes.append(runtime)
  debug=runtime/'external/script/debug.lua';debug.write_text((source/'external/script/debug.lua').read_text()+telemetry)
  config=runtime/'data/eter/config.ini';config.write_text(config.read_text().replace('Rollback.LogsEnabled           = 0','Rollback.LogsEnabled           = 1'))
  (runtime/'save/logs').mkdir(parents=True,exist_ok=True)
  log=open(out/f'peer-{i}.log','w')
  args=['./Ikemen_GO_Linux','-config','data/eter/config.ini','-nosound','-p1','simon','-p2','techblade','-s','lab','-time','99','-p1.power','3000','-p2.power','3000','-ip','' if i==0 else '127.0.0.1']
  processes.append(subprocess.Popen(args,cwd=runtime,env=env,stdout=log,stderr=log));time.sleep(2)
 time.sleep(8)
 def xd(*args):return subprocess.check_output([str(deps/'x11/usr/bin/xdotool'),*args],env=env,text=True).strip()
 windows=[xd('search','--onlyvisible','--pid',str(p.pid)).splitlines()[-1] for p in processes]
 def focus(i):xd('windowfocus',windows[i]);time.sleep(.08)
 def key(k):xd('keydown',k);time.sleep(.08);xd('keyup',k)
 if '--disconnect' in sys.argv:
  processes[1].terminate();processes[1].wait(timeout=5);time.sleep(7)
 else:
  focus(0)
  # Servant, portal, command grab and confirmed super through physical key events.
  def motion(seq,button):
   held=set()
   for raw in seq:
    nxt=set(raw.split('+'))
    for k in held-nxt:xd('keyup',k)
    for k in nxt-held:xd('keydown',k)
    held=nxt;time.sleep(.055)
   key(button)
   for k in held:xd('keyup',k)
  motion(['s','s+a','a'],'g');time.sleep(1.4)
  key('q');time.sleep(.8)
  xd('keydown','d');time.sleep(.35);xd('keyup','d')
  motion(['d','s','s+d'],'g');time.sleep(1.5)
  xd('keydown','d');time.sleep(.65);xd('keyup','d')
  motion(['s','s+d','d','s','s+d','d'],'f+h');time.sleep(1.5)
  focus(1);key('e');time.sleep(.9);focus(0)
  for n in range(32):
   if any(p.poll() is not None for p in processes):break
   xd('keydown','d');time.sleep(.6);xd('keyup','d');key('e');time.sleep(.65)
  time.sleep(1)
finally:
 for p in processes:
  if p.poll() is None:p.terminate();p.wait(timeout=5)
 x.terminate();x.wait(timeout=5)
 for i,runtime in enumerate(runtimes):
  if (runtime/'net-test.csv').exists():shutil.copy2(runtime/'net-test.csv',out/f'peer-{i}.csv')
  shutil.copytree(runtime/'save/logs',out/f'logs-{i}',dirs_exist_ok=True)
logs=[(out/f'peer-{i}.log').read_text() for i in range(2)]
for i,log in enumerate(logs):print('PEER',i,log[-2500:])
if '--disconnect' in sys.argv:
 assert 'EventCodeDisconnectedFromPeer' in logs[0],logs[0]
 assert 'panic:' not in logs[0]
 print('PASS: host detected interrupted peer and exited the match without panic')
 raise SystemExit(0)
assert all('EventCodeRunning' in log for log in logs),'Rollback session did not run'
assert all('EventCodeDesync' not in log and 'panic:' not in log for log in logs),'Desync or panic'
rows=[]
for i in range(2):
 data=[list(map(int,line.split(','))) for line in (out/f'peer-{i}.csv').read_text().splitlines()]
 rows.append(data)
 print('PEER',i,'states',sorted({r[2] for r in data if r[1]==1}),'P2 min life',min(r[3] for r in data if r[1]==2))
 assert any(r[1]==2 and r[3]==0 for r in data),'No KO observed'
 assert sum(r[1]==1 and r[2]==180 and (j==0 or data[j-2][2]!=180) for j,r in enumerate(data))>=2,'Two round wins absent'
# Compare committed endpoint state sequences after deduplication; speculative rollback frames can differ.
summary=[]
for data in rows:
 endpoints=[]
 for r in data:
  if r[1]==1 and r[2]==180:
   e=(r[1],r[2],r[3],r[4])
   if not endpoints or e!=endpoints[-1]:endpoints.append(e)
 summary.append(endpoints)
assert summary[0]==summary[1],(summary[0],summary[1])
(out/'summary.json').write_text(json.dumps({'scope':'loopback only','frameDelay':2,'roundEndpoints':summary,'desyncDetected':False},indent=2))
print('PASS: two native rollback peers, two KOs, matching victory endpoints. Internet acceptance remains pending.')
