# 웹 추천 연결 안내

현재 모델은 168,035개 레시피와 12,769개 콘텐츠 특징을 사용합니다.

## 필수 연결

- `recipes_model_v4.csv`: 추천 대상 전체 데이터. `ingredient_set`, `core_set`, `main_ings_rule1_2`, `main_ings_rule2` 등 집합 컬럼은 JSON을 읽은 뒤 set으로 복원합니다. `ing`, 카테고리, 조리 단계 등 리스트 컬럼도 JSON 파싱합니다. `eval`은 사용하지 않습니다.
- `content_matrix.npz`: `scipy.sparse.load_npz`로 읽습니다. 전체 레시피 간 유사도 행렬을 만들지 않고 선택한 메뉴와 후보 간 유사도만 계산합니다.
- `recipe_row_mapping.csv`: `recipe_id` → `row_index`입니다. CSV의 레시피 순서·ID와 일치하는지 먼저 확인합니다.
- `taste_menu_candidates_v4.csv`: 취향 선택 화면에 표시할 대표 메뉴입니다.
- `recommendation_rules.joblib`: `BASE_ALIASES`, `MERGE_MAP`, `INGREDIENT_TIER`, `TIER_DIFFICULTY`, `FINAL_WEIGHTS` 등의 실제 저장값입니다. joblib.load 후 추천 함수가 참조하는 이름에 연결합니다.
- `web_settings.json`: 행렬 크기, 버전, 점수 가중치와 기본 규칙입니다.

고정된 데이터셋에서 선택한 기존 레시피로 추천할 때는 저장된 콘텐츠 행렬을 재사용합니다. `ingredient_vectorizer.joblib`, `category_encoders.joblib`, `word2vec.model`, `word2vec_center.npy`는 특징 생성 재현용입니다.
`taste_cluster_model.joblib`은 EDA 재료 TF-IDF→SVD 공간에서 학습한 모델이므로 콘텐츠 행렬을 직접 넣으면 안 됩니다. 현재 자산에는 해당 EDA 변환기와 SVD가 없으며, 기존 군집과 대표 메뉴를 사용하는 데는 추가 학습이 필요하지 않습니다. 새 레시피의 군집 예측까지 확장하려면 해당 변환기도 따로 내보내야 합니다.

## 서버에 연결한 함수

4-2: normalize_base, normalize_model_ingredient
4-3: tier_of
4-7: contains_excluded, build_candidates
4-8: 점수·MMR 관련 함수와 get_final_recommendations
4-11: suggest_grocery_shopping

`app/recommender.py`에 아래 함수들을 원문 그대로 추출했습니다. `app/main.py`가 recipe 컬럼·저장 규칙·콘텐츠 행렬을 불러오고 model_recipes, X_model_content, model_id_to_idx 등을 준비합니다. 서버 시작 시 한 번 로딩하고 요청별로 기본·취향·장보기 추천을 계산합니다.

## 화면 입력

USER_INPUT은 테스트 예시입니다. HTML에서 받은 재료와 선택한 메뉴 ID를 실제 입력으로 전달합니다. 추천 함수에는 단일 ID 또는 ID 목록이 지원됩니다. 제외 재료·최대 시간·추가 구매 수는 서버에서도 검증합니다.

## 확인할 경우

취향 미선택, 복수 선택, 제외 재료 포함, 후보 없음, 추가 구매 0개, 재료 1종 장보기 추천을 확인합니다. 기본·취향 추천 결과를 단순 CSV 출력 예시로 대체하지 않습니다.
