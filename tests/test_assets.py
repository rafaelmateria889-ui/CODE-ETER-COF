import io,re,struct,unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
class Assets(unittest.TestCase):
    def test_native_sprite_archives(self):
        for path in (ROOT/'game').rglob('*.sff'):
            data=path.read_bytes();self.assertEqual(data[:12],b'ElecbyteSpr\0')
            total,offset=struct.unpack_from('<II',data,20);seen=set()
            for i in range(total):
                next_,size,x,y,g,n,linked,same=struct.unpack_from('<IIhhHHHB',data,offset)
                if not size:self.assertLess(linked,i,f'{path}: forward linked sprite')
                else:
                    im=Image.open(io.BytesIO(data[offset+32:offset+32+size]));im.load()
                    self.assertEqual(im.mode,'P');self.assertGreater(im.width,0)
                self.assertNotIn((g,n),seen);seen.add((g,n))
                if i<total-1:self.assertGreater(next_,offset)
                offset=next_
            self.assertEqual(offset,0)
            if path.parent.name in ['simon','techblade']:
                air=path.with_suffix('.air').read_text()
                for g,n in re.findall(r'^(\d+),\s*(\d+),',air,re.M):self.assertIn((int(g),int(n)),seen)
    def test_disjoint_keyboards(self):
        s=(ROOT/'game/data/eter/config.ini').read_text()
        sets=[]
        for p in [1,2]:
            block=s.split(f'[Keys_P{p}]')[1].split('[')[0]
            pairs=dict(re.findall(r'^(\w+)[ \t]*=[ \t]*(.*)$',block,re.M))
            vals=[pairs[k].strip() for k in ['up','down','left','right','x','a','y','b','c','z']]
            self.assertEqual(len(vals),len(set(vals)))
            sets.append(set(vals))
        self.assertFalse(sets[0]&sets[1])
    def test_character_states_are_defined(self):
        for name in ['simon','techblade']:
            p=ROOT/'game/chars'/name
            cns=(p/f'{name}.cns').read_text();cmd=(p/f'{name}.cmd').read_text()
            states=set(map(int,re.findall(r'\[Statedef (\d+)\]',cns)))
            actions=set(map(int,re.findall(r'\[Begin Action (\d+)\]',(p/f'{name}.air').read_text())))
            for n in re.findall(r'^anim = (\d+)$',cns,re.M):self.assertIn(int(n),actions,f'{name}: missing action {n}')
            for n in [200,210,220,230,400,410,420,430,600,610,620,630,800,810,820,821,1000,1100,1200,1300,3000]:self.assertIn(n,states)
            self.assertIn('Power >= 1000',cmd)
            self.assertIn('poweradd = -1000',cns)
            for n in [1001,1101,1201,1301,3100,3110,3111]:self.assertIn(n,states)
            self.assertIn('MoveHit && NumTarget > 0 && P2Life > 0',cns)
            if name=='simon':
                for n in [1310,1400,1401,1450,1451]:self.assertIn(n,states)
                self.assertIn('NumHelper(1450) = 0',cmd)
                self.assertIn('Root, MoveType = H',cns)
                self.assertIn('stateno = 1451',cns)
if __name__=='__main__':unittest.main()
