# 웹 배포

- 공개 주소: https://naengteol-wanr.onrender.com/
- 최초 배포 코드: `ef3b0e1`
- 확정 버전 태그: `web-v1-20260927`
- 운영: Render Free / Singapore / Docker
- GitHub `main` 변경 시 자동 배포됩니다. 문서만 수정할 때는 커밋 메시지에 `[skip render]`를 넣으면 재배포하지 않습니다.

현재 화면과 추천 동작을 2026-09-27 기준으로 확정했습니다.

## Render Free

저장소의 Dockerfile로 Web Service를 배포합니다. 인스턴스는 Free, 지역은 Singapore, Health Check Path는 `/api/health`입니다. 포트는 Render의 PORT 설정을 사용합니다. render.yaml에도 같은 설정이 있습니다.

무료 서비스는 사용하지 않으면 잠들어 첫 접속 시 준비 시간이 필요합니다. 무료 사용량 제한은 [Render 무료 정책](https://render.com/docs/free)을 따릅니다. 무료 사용량 초과 시 서비스 또는 새 빌드가 일시 중단될 수 있습니다. 유료 인스턴스나 디스크는 사용하지 않습니다.

공개 서버의 첫 확인에서 예시 냉장고의 기본·취향 추천은 각각 약 2분이 걸렸습니다. 무료 0.1 CPU 환경의 측정값이며 입력과 동시 접속에 따라 달라집니다. 대기 중에도 화면을 닫지 않고 기다려 주세요.

## 데이터

`deploy/assets`는 원본 레시피에서 웹에 필요한 값을 보존한 배포 묶음입니다. GitHub 파일 제한 이하로 나눈 조리법과 재료 배열을 포함합니다. 원본 791MB CSV는 기존처럼 Drive에서 제공합니다.

빌드할 때 `deploy/install_assets.py`가 해시를 확인하고 `runtime_assets`를 복원합니다. 사용자 입력과 추천 결과는 서버에 저장하지 않습니다. 재학습이나 감성분석을 실행할 필요가 없습니다.

추천 함수는 기존 노트북에서 추출한 `app/recommender.py`를 사용합니다. 메모리 사용을 줄이기 위해 읽기 전용 배열과 조리법 SQLite를 사용하고, 취향 유사도 계산은 나눠 처리합니다.

## 확인한 동작

아래 API 동작 검사는 공개 주소에서도 모두 통과했습니다.

- 원본 168,035개 레시피의 ID·이름·시간·평점·재료 집합 일치
- 나눠 계산한 코사인 유사도와 원래 계산 결과 일치
- 기본·취향 추천, 제외 재료, 장보기 증가 수, 조리법, 추가 구매 0개, 빈 결과, 잘못된 ID 처리

로컬에서 배포 데이터를 사용하려면 다음 순서로 실행합니다.

```sh
pip install -r requirements-deploy.txt
python deploy/install_assets.py
USE_PACKED_ASSETS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m uvicorn app.main:app --host 127.0.0.1 --port 8765
```
