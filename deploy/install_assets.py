"""빌드 시에만 배포 데이터 압축 해제 및 무결성 검사."""
from pathlib import Path
import gzip,hashlib,json,shutil,zipfile,io
root=Path(__file__).resolve().parents[1];source=root/'deploy/assets';out=root/'runtime_assets';out.mkdir(exist_ok=True)
manifest=json.loads((source/'manifest.json').read_text())
for name,digest in manifest['files'].items():
 if hashlib.sha256((source/name).read_bytes()).hexdigest()!=digest:raise ValueError('손상된 배포 파일: '+name)
 if name not in manifest['detail_parts']:shutil.copyfile(source/name,out/name)
with gzip.GzipFile(fileobj=io.BytesIO(b''.join((source/n).read_bytes() for n in manifest['detail_parts']))) as zipped, (out/'details.sqlite').open('wb') as target:shutil.copyfileobj(zipped,target)
if hashlib.sha256((out/'details.sqlite').read_bytes()).hexdigest()!=manifest['details_sha256']:raise ValueError('조리법 데이터 해시 불일치')
with zipfile.ZipFile(root/'web_assets/content_matrix.npz') as zipped:
 for name in ['data.npy','indices.npy','indptr.npy','shape.npy']:(out/('matrix_'+name)).write_bytes(zipped.read(name))
print('Runtime assets ready')
