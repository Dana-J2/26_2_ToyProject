"""GitHub 파일 제한 내에서 배포 데이터 패키징."""
from pathlib import Path
import gzip,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'runtime_assets';out=ROOT/'deploy/assets';out.mkdir(exist_ok=True)
for file in source.glob('*'):
 if file.name.startswith('matrix_') or file.name in ['manifest.json','details.sqlite']:continue
 (out/file.name).write_bytes(file.read_bytes())
# SQLite는 gzip 압축 후 분할한다. 원본 CSV는 포함하지 않는다.
compressed=gzip.compress((source/'details.sqlite').read_bytes(),compresslevel=6,mtime=0)
parts=[]
for i,start in enumerate(range(0,len(compressed),40*1024*1024)):
 name=f'details.sqlite.gz.part{i:02d}';(out/name).write_bytes(compressed[start:start+40*1024*1024]);parts.append(name)
manifest={'count':168035,'detail_parts':parts,'details_sha256':hashlib.sha256((source/'details.sqlite').read_bytes()).hexdigest(),'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.name!='manifest.json'}}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
print('Packaged',round(sum(p.stat().st_size for p in out.iterdir())/2**20,1),'MiB')
