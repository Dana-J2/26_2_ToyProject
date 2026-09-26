# 26_2_ToyProject

자취생의 냉털을 부탁해! 레시피 분석과 웹 추천 개발용 데이터입니다.
분석 노트북과 저장된 모델·결과, 실제 Python 추천 함수를 사용하는 로컬 웹 프로토타입입니다.

## 웹 개발 시작하기

1. 저장소를 clone합니다. `content_matrix.npz`가 약 80MB이므로 다운로드에 시간이 걸릴 수 있습니다.
2. [공유 Drive 폴더](https://drive.google.com/drive/folders/18H9inARSUkZT6len6Q1FrTMFJNSmNLo2?usp=sharing)의 **web_assets → recipes_model_v4.csv**를 다운로드해 로컬 **`web_assets/recipes_model_v4.csv`**로 저장합니다. 폴더는 링크가 있는 누구나 보기로 공유되어 있습니다. 파일은 약 791MB라 GitHub에는 넣지 않았습니다.
3. Python 가상환경에서 `pip install -r requirements-web.txt`로 필요한 라이브러리를 설치합니다.
4. `python scripts/verify_assets.py`로 공유 파일의 무결성과 필수 CSV 크기를 확인합니다.
5. `python -m uvicorn app.main:app --host 127.0.0.1 --port 8765`를 실행하고 http://127.0.0.1:8765 를 엽니다. 첫 실행 때 CSV를 읽은 뒤 사용할 수 있습니다. 사용자 요청마다 분석·학습을 다시 실행하지 않습니다.

## 폴더 구성

| 폴더 | 내용 |
|---|---|
| `app/` | FastAPI 서버와 노트북에서 추출한 추천 함수 |
| `app/static/` | HTML·CSS·JavaScript 화면 |
| `notebooks/` | 사용자가 공유했던 실행 결과 포함 Colab 노트북 사본 |
| `web_assets/` | 콘텐츠 행렬, ID 매핑, 대표 메뉴, 학습 모델, 재료 규칙 |
| `config/` | 노트북 실행 당시 예시 입력과 설정 |
| `data/examples/` | 예시 입력에 대한 기본·취향·장보기 추천 결과 |
| `data/analysis/` | 가설검정, 전처리, 감성분석, EDA 및 NLP 결과 |
| `reports/figures/` | 분석 그래프 PNG·SVG |
| `docs/` | 원본 Drive 주소·파일 크기·해시 목록과 개발 안내 |
| `scripts/` | 파일 확인 도구 |

## 추천 흐름

- 보유 재료·제외 재료·최대 조리시간·추가 구매 수를 입력합니다.
- `taste_menu_candidates_v4.csv`에서 선호 메뉴 ID를 1~3개 고릅니다. 선택하지 않으면 기본 추천입니다.
- 트랙 A는 바로 조리, 트랙 B는 추가 구매 후 조리입니다.
- 장보기 추천은 재료 1종 추가로 가능한 메뉴 수가 많은 순서입니다. 현재 장보기 순위에는 개인 취향 점수가 들어가지 않습니다.
- EDA k=6과 취향 선택 k=16을 구분합니다.

`data/examples`의 personal 결과는 선호 ID가 비어 있던 실행의 예시라 basic과 같을 수 있습니다. 실제 사용자 추천값으로 고정해서 사용하지 마세요.

## 저장 자산 사용 시 주의

자세한 연결 방법은 [개발 안내](docs/WEB_HANDOFF.md)를 참고하세요. 레시피 행 순서와 콘텐츠 행렬 행 순서를 바꾸지 않아야 합니다. CSV에 저장된 리스트·집합은 JSON 파싱 후 원래 타입으로 복원해야 합니다.
모델 파일은 이 프로젝트에서 생성한 신뢰할 수 있는 파일만 불러오세요.

## 원본과 제외 파일

[공유 Drive 분석 결과 폴더](https://drive.google.com/drive/folders/18H9inARSUkZT6len6Q1FrTMFJNSmNLo2?usp=sharing)

- `recipes_model_v4.csv`: 약 791MB. 위 링크로 별도 제공하며 `web_assets` 복사본 하나만 사용하면 됩니다.
- [recipes_preprocessed_final.csv](https://drive.google.com/file/d/1f1KgAC6aTGtIv4SF_wIApUGSkKyaERfO/view): 약 581MB. 전체 분석 중간 산출물이며 웹 추천에는 위 최종 CSV를 사용합니다.
- `cache/`: 원본 폴더가 비어 있어 포함하지 않았습니다.
- 원본 `RAW_recipes.csv`, `RAW_interactions.csv`, `recipe_metadata_final.csv`는 이번 Drive 결과 폴더에 없으므로 포함하지 않았습니다. 전체 분석 재실행 시 원래 `DartB_Dana/data`에서 받아야 합니다.

노트북은 Colab Drive 경로를 사용합니다. 저장소의 결과 폴더 배치는 팀 공유용이며, 노트북 전체 재실행 시 경로를 그대로 사용할 수 있는 구조는 아닙니다. 저장된 모델로 웹을 만드는 경우 원본 CSV나 감성분석 재실행은 필요하지 않습니다.

## 프로토타입 확인

- 예시 냉장고 채우기 → 취향 메뉴 선택(선택 사항) → 내 재료로 추천받기
- 바로 조리 / 추가 구매 후 조리 탭과 장보기 추천을 확인합니다.
- 장보기 재료의 담기를 누르면 보유 재료에 추가됩니다. 추천받기를 다시 눌러 새 결과를 확인합니다.
- 레시피 카드는 유사 요리 참고 사진을 사용합니다. 레시피명·조리법은 원문 영어이며, 자주 쓰는 재료에 한해 한국어 검색명을 제공합니다.
- 서버 실행 중 `python tests/check_api.py`로 주요 추천 동작을 검증할 수 있습니다.
