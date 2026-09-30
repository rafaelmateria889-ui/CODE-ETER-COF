"""Install pinned native engine, verify archive, overlay authored game content.
No Python packages are needed to play. Python is only the Linux installer.
"""
import argparse, hashlib, os, platform, shutil, subprocess, urllib.request, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HASHES={'linux':'cc533c1a2ab84d63cbf9126d9dcb3f2dcc1a41c6206f2da419b0c91084f193e4','macos':'2b0a8ff44c23b764340d7e428ddbf3a86c4d157c16ee78fe7a960117464bfc12','windows':'9338eaeb68599ceb13b0867819a091ea3f92eba58077e800b4540b7a1f9c3731'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--install-only',action='store_true');args=ap.parse_args()
    target={'Linux':'linux','Windows':'windows'}.get(platform.system())
    if not target:raise SystemExit('Sistema nao suportado pelo instalador.')
    runtime=ROOT/'runtime'
    executable={'linux':'Ikemen_GO_Linux','windows':'Ikemen_GO.exe','macos':'Ikemen_GO_MacOS'}[target]
    if not (runtime/executable).exists():
        if runtime.exists():raise SystemExit('runtime existe sem o executavel esperado. Preserve/renomeie a pasta antes de reinstalar.')
        archive=ROOT/'ikemen-download.zip'
        print('Baixando Ikemen GO 1.0.0...',flush=True)
        urllib.request.urlretrieve(f'https://github.com/ikemen-engine/Ikemen-GO/releases/download/v1.0.0/Ikemen_GO-v1.0.0-{target}.zip',archive)
        if hashlib.sha256(archive.read_bytes()).hexdigest()!=HASHES[target]:raise SystemExit('SHA256 invalido: download nao utilizado.')
        with zipfile.ZipFile(archive) as z:
            for n in z.namelist():
                if Path(n).is_absolute() or '..' in Path(n).parts:raise SystemExit('Caminho invalido no arquivo.')
            z.extractall(runtime)
        archive.unlink()
    shutil.copytree(ROOT/'game',runtime,dirs_exist_ok=True)
    save=runtime/'save';save.mkdir(exist_ok=True)
    if not (save/'eter.ini').exists():shutil.copy2(ROOT/'game/data/eter/config.ini',save/'eter.ini')
    exe=runtime/executable;exe.chmod(exe.stat().st_mode|0o111)
    print('Pronto. Configuracoes pessoais preservadas em runtime/save/eter.ini.')
    if not args.install_only:raise SystemExit(subprocess.call([str(exe),'-config','save/eter.ini'],cwd=runtime))
if __name__=='__main__':main()

