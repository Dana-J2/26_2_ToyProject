"""공유 파일과 별도 다운로드한 추천 CSV를 확인한다."""
import argparse
import hashlib
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--shared-only', action='store_true', help='저장소에 포함된 파일만 확인')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / 'docs/asset_manifest.json').read_text())
    errors = []
    for item in manifest:
        path = root / item['path']
        if not path.is_file():
            errors.append(f'파일 없음: {item["path"]}')
            continue
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
        if path.stat().st_size != item['bytes'] or digest.hexdigest() != item['sha256']:
            errors.append(f'파일 불일치: {item["path"]}')
    if not args.shared_only:
        recipes = root / 'web_assets/recipes_model_v4.csv'
        if not recipes.is_file() or recipes.stat().st_size != 790662192:
            errors.append('README의 Drive 링크에서 recipes_model_v4.csv를 web_assets에 내려받으세요.')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'공유 파일 {len(manifest)}개 무결성 확인 완료')
    if not args.shared_only:
        print('추천 CSV 크기 확인 완료. 서버 로딩 시 레시피 ID와 행 매핑도 확인하세요.')

if __name__ == '__main__':
    main()
