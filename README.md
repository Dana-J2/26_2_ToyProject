# 🍳 자취생의 냉털을 부탁해!

> **냉장고에 있는 재료로 지금 만들 수 있는 메뉴부터,  
> 재료를 조금만 더 사면 만들 수 있는 메뉴까지 추천하는 레시피 추천 프로젝트**

자취생은 매번 장을 보기보다 **지금 냉장고에 있는 재료를 어떻게 활용할지** 고민하는 경우가 많습니다.

이 프로젝트는 사용자가 보유한 재료와 조리 조건을 입력하면 만들기 좋은 레시피를 추천하고,  
추가 구매를 허용할 경우 **어떤 재료를 더 사면 만들 수 있는 메뉴가 가장 크게 늘어나는지**까지 제안하는 것을 목표로 합니다.

단순한 레시피 검색을 넘어 사용자의 **재료 보유 현황 · 조리시간 · 취향 · 추가 구매 부담**을 함께 고려한 추천 시스템을 구현했습니다.

---

## 🎯 Project Goal

### 1. 냉장고 속 재료 활용

사용자가 현재 보유하고 있는 재료를 기준으로 실제로 만들기 쉬운 메뉴를 우선 추천합니다.

### 2. 추가 구매 부담 최소화

현재 재료만으로 만들기 어려운 경우 필요한 재료를 조금 더 구매했을 때 만들 수 있는 레시피까지 함께 탐색합니다.

### 3. 사용자 취향 반영

사용자가 좋아하는 레시피를 선택하면 콘텐츠 기반 유사도를 활용해 선호 메뉴와 비슷한 레시피를 추천합니다.

### 4. 장보기까지 연결

특정 재료 하나를 추가했을 때 새롭게 만들 수 있는 메뉴가 얼마나 증가하는지 계산하여 효율적인 장보기 후보를 제안합니다.

---

## ✨ Main Features

| 기능 | 설명 |
|---|---|
| 🧊 보유 재료 기반 추천 | 현재 가지고 있는 재료와 레시피 재료 구성을 비교 |
| 🛒 추가 구매 허용 | 부족한 재료 수를 고려해 조금만 더 사면 만들 수 있는 메뉴까지 추천 |
| ⏱️ 조리시간 필터 | 사용자가 설정한 최대 조리시간을 초과하는 메뉴 제외 |
| 🚫 제외 재료 | 알레르기·비선호 재료 등이 포함된 레시피 제외 |
| ❤️ 취향 기반 추천 | 사용자가 선택한 선호 레시피와 콘텐츠가 유사한 메뉴에 가점 |
| ⭐ 평점 반영 | 레시피의 평가 정보를 추천 점수에 반영 |
| 🥕 장보기 추천 | 재료 하나를 추가 구매했을 때 확장되는 메뉴 수를 기준으로 구매 후보 제안 |

---

## 📊 Dataset

본 프로젝트는 Kaggle의 **Food.com Recipes and Interactions** 데이터를 기반으로 진행했습니다.

👉 [Food.com Recipes and User Interactions Dataset](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)

원본 데이터는 크게 다음 두 파일로 구성됩니다.

- `RAW_recipes.csv`
  - 레시피 이름
  - 조리시간
  - 재료
  - 조리 과정
  - 영양 정보
  - 태그 등

- `RAW_interactions.csv`
  - 사용자
  - 레시피
  - 평점
  - 리뷰 등 사용자-레시피 상호작용 정보

전처리 및 추천 대상 필터링 이후 **168,035개의 레시피**를 최종 추천 시스템에서 사용합니다.

---

## 🔎 Analysis & Preprocessing

추천 모델 구축 전 다음과 같은 전처리와 분석을 수행했습니다.

### Recipe Data

- 결측 레시피 정리
- 비정상 조리시간 처리
- 영양 정보 컬럼 분리
- 재료명 정규화
- 레시피별 평점 집계
- 추천에 활용하기 어려운 레시피 필터링
- 카테고리 및 태그 기반 레시피 특성 구축

### Interaction Data

- 미평가 데이터와 실제 평점 구분
- 레시피별 평균 평점 및 평가 개수 계산
- 평가 수 차이를 고려한 평점 지표 구축
- 사용자 리뷰 텍스트 분석

### NLP

레시피의 텍스트 정보를 활용하기 위해 다음 요소를 분석했습니다.

- 레시피 설명
- 재료명
- 태그
- Word2Vec 기반 재료 의미 정보

---

## 🧠 Recommendation System

최종 추천은 하나의 기준만 사용하는 방식이 아니라 여러 요소를 함께 반영합니다.

### 1️⃣ Ingredient Match

사용자가 가지고 있는 재료로 해당 레시피를 얼마나 충족할 수 있는지 계산합니다.

완전히 만들 수 있는 레시피뿐 아니라 사용자가 허용한 범위 내에서 재료를 추가 구매하면 만들 수 있는 레시피도 후보에 포함합니다.

---

### 2️⃣ Purchase Cost

레시피를 만들기 위해 추가로 필요한 재료가 적을수록 높은 점수를 부여합니다.

따라서 비슷한 조건의 메뉴라면 **지금 가진 재료를 더 많이 활용할 수 있는 메뉴**가 우선 추천됩니다.

---

### 3️⃣ Preference Similarity

사용자가 좋아하는 레시피를 선택한 경우 해당 레시피와 다른 메뉴 간 콘텐츠 유사도를 계산합니다.

콘텐츠 특징은 다음 정보를 조합해 구성했습니다.

- Ingredients TF-IDF
- Word2Vec 기반 재료 벡터
- Course Category
- Dish Type
- Main Ingredient Group
- Cuisine

최종 콘텐츠 행렬은

**168,035 recipes × 12,769 features**

형태로 저장되어 있습니다.

---

### 4️⃣ Rating

사용자 평가 정보를 활용해 평가가 좋은 레시피에 가점을 부여합니다.

---

### 5️⃣ Cooking Time

사용자가 설정한 최대 조리시간을 기준으로 후보를 필터링하며, 조건 내에서는 상대적으로 부담이 적은 메뉴를 추천 점수에 반영합니다.

---

## ⚖️ Final Recommendation Score

현재 최종 추천 점수는 다음 다섯 요소를 결합합니다.

| 요소 | Weight |
|---|---:|
| Ingredient Score | 30% |
| Purchase Score | 25% |
| Preference Score | 20% |
| Rating Score | 15% |
| Time Score | 10% |

즉, **현재 냉장고에 있는 재료를 최대한 활용하면서 추가 구매 부담을 줄이는 것**을 가장 중요한 기준으로 두고, 이후 사용자 취향과 레시피 평가·조리시간을 함께 반영합니다.

---

## 🛒 Grocery Recommendation

이 프로젝트에서는 레시피뿐 아니라 **다음에 어떤 재료를 사는 것이 효율적인지**도 추천합니다.

예를 들어 현재 냉장고에

`egg · onion · milk · cheddar cheese · bread`

가 있다고 가정하면,

각 후보 재료를 하나씩 추가했을 때 새롭게 만들 수 있는 레시피 수를 계산합니다.

이를 통해 단순히 자주 등장하는 재료가 아니라,

> **현재 내 냉장고 상태에서 가장 많은 메뉴를 새롭게 열어주는 재료**

를 장보기 후보로 제안합니다.

---

## ❤️ Taste-Based Recommendation

사용자는 대표 레시피 목록에서 좋아하는 메뉴를 선택할 수 있습니다.

선택된 레시피와 전체 후보 레시피의 콘텐츠 유사도를 계산해 기본 추천 점수에 취향 정보를 추가합니다.

- 선호 메뉴 미선택 → 기본 추천
- 선호 메뉴 1개 선택 → 해당 메뉴와의 유사도 반영
- 복수 메뉴 선택 → 여러 선호 메뉴를 함께 고려

취향 추천을 위한 레시피 군집은 **K=16**으로 구성했습니다.

> EDA에서 레시피 전체 구조를 살펴보기 위해 사용한 군집과 취향 선택을 위한 군집은 목적이 다르므로 별도로 관리합니다.

---

## 📁 Repository Structure

```text
26_2_ToyProject
│
├── notebooks/
│   └── Final_Analysis_Colab.ipynb
│
├── web_assets/
│   ├── content_matrix.npz
│   ├── recipe_row_mapping.csv
│   ├── recipe_clusters_taste_k16.csv
│   ├── taste_menu_candidates_v4.csv
│   ├── ingredient_vectorizer.joblib
│   ├── category_encoders.joblib
│   ├── word2vec.model
│   ├── word2vec_center.npy
│   ├── taste_cluster_model.joblib
│   ├── recommendation_rules.joblib
│   └── web_settings.json
│
├── data/
│   ├── analysis/
│   └── examples/
│
├── config/
│   └── model_v4_settings.json
│
├── reports/
│   └── figures/
│
├── docs/
│   ├── WEB_HANDOFF.md
│   └── asset_manifest.json
│
├── scripts/
│   └── verify_assets.py
│
├── requirements-assets.txt
└── README.md
```

### 주요 폴더

| 경로 | 내용 |
|---|---|
| `notebooks/` | 전체 분석 및 추천 모델링 Notebook |
| `web_assets/` | 웹 추천 구현에 필요한 저장 모델 및 콘텐츠 자산 |
| `data/analysis/` | EDA · 가설검정 · NLP 등 분석 결과 |
| `data/examples/` | 추천 시나리오별 예시 결과 |
| `config/` | 모델링 실행 당시 설정 |
| `reports/figures/` | 분석 과정에서 생성한 시각화 결과 |
| `docs/` | 웹 개발 연결 가이드 및 파일 정보 |
| `scripts/` | 저장 자산 검증 도구 |

---

## 📦 Data & Model Assets

GitHub 용량을 고려해 대용량 데이터와 전체 분석 산출물은 별도의 Google Drive에 저장했습니다.

### 🔗 Google Drive

👉 **[final_analysis 전체 폴더 보기](https://drive.google.com/drive/folders/18H9inARSUkZT6len6Q1FrTMFJNSmNLo2?usp=sharing)**

링크가 있는 사용자는 별도의 권한 요청 없이 파일을 열람할 수 있습니다.

Drive에는 다음과 같은 파일이 포함되어 있습니다.

### 주요 분석 데이터

- `recipes_preprocessed_final.csv`
- `recipe_bayesian_ratings.csv`
- `zero_rating_sentiment.csv`
- `recipe_clusters_eda.csv`
- `recipe_clusters_taste_k16.csv`
- NLP 분석 결과
- 가설검정 결과
- 추천 시나리오 결과
- 분석 그래프

### Web Assets

Drive의 `web_assets/` 폴더에는 웹 추천 구현에 필요한 자산이 별도로 정리되어 있습니다.

특히 `recipes_model_v4.csv`는 약 **791MB**로 GitHub에는 포함하지 않았습니다.

👉 [recipes_model_v4.csv 바로가기](https://drive.google.com/file/d/10Qd4Ys9_VbN1LptL43HUDnqCY5fc1AF2/view)

웹 개발 시에는 Drive의

`web_assets/recipes_model_v4.csv`

를 기준 파일로 사용합니다.

---

## 💻 Web Development

현재 저장소에는 **분석 결과와 웹 추천 구현에 필요한 모델·자산까지 준비되어 있으며, 실제 웹 화면과 Python 서버는 별도로 연결해야 합니다.**

### 1. Repository Clone

`git clone https://github.com/Dana-J2/26_2_ToyProject.git`

---

### 2. Large CSV Download

Google Drive에서

`web_assets/recipes_model_v4.csv`

를 다운로드한 뒤 저장소의 다음 위치에 배치합니다.

`web_assets/recipes_model_v4.csv`

---

### 3. Python Environment

저장 당시 모델 환경은 `requirements-assets.txt`에서 확인할 수 있습니다.

`pip install -r requirements-assets.txt`

현재 저장된 주요 라이브러리 버전은 다음과 같습니다.

| Library | Version |
|---|---:|
| numpy | 2.1.3 |
| pandas | 2.2.3 |
| scipy | 1.16.3 |
| scikit-learn | 1.6.1 |
| gensim | 4.4.0 |
| joblib | 1.6.0 |

웹 프레임워크 등 서버 구현에 필요한 라이브러리는 별도로 추가하면 됩니다.

---

### 4. Asset Verification

필수 파일이 정상적으로 배치되었는지 확인하려면

`python scripts/verify_assets.py`

를 실행합니다.

---

### 5. Recommendation Functions

추천 로직은

`notebooks/Final_Analysis_Colab.ipynb`

후반부에 정리되어 있습니다.

웹 서버에서는 분석과 모델 학습을 사용자 요청마다 다시 실행하지 않고, 이미 저장된 모델과 데이터를 불러와 추천 함수만 호출하는 구조를 권장합니다.

보다 구체적인 연결 방법은 아래 문서를 참고하세요.

👉 **[Web Development Handoff Guide](docs/WEB_HANDOFF.md)**

---

## 🧩 Main Web Assets

| File | Role |
|---|---|
| `recipes_model_v4.csv` | 최종 추천 대상 레시피 데이터 |
| `content_matrix.npz` | 콘텐츠 기반 추천 특징 행렬 |
| `recipe_row_mapping.csv` | Recipe ID와 콘텐츠 행렬 Row 연결 |
| `taste_menu_candidates_v4.csv` | 취향 선택 화면용 대표 메뉴 |
| `recommendation_rules.joblib` | 재료 정규화·추천 점수 관련 규칙 |
| `web_settings.json` | 추천 모델 설정 및 가중치 |
| `ingredient_vectorizer.joblib` | 재료 TF-IDF 변환기 |
| `category_encoders.joblib` | 카테고리 특징 변환 정보 |
| `word2vec.model` | 재료 Word2Vec 모델 |
| `word2vec_center.npy` | Word2Vec 중심 벡터 |
| `taste_cluster_model.joblib` | 취향 군집 모델 |

---

## ⚠️ Notes

### Recipe Order

`content_matrix.npz`의 행 순서와 레시피 데이터의 순서가 연결되어 있으므로 임의로 행 순서를 변경하면 안 됩니다.

`recipe_row_mapping.csv`를 통해 `recipe_id`와 콘텐츠 행렬의 위치를 연결합니다.

### Saved Lists & Sets

CSV에 저장된 재료 리스트·집합 컬럼은 문자열 형태로 저장되어 있으므로 웹 서버에서 다시 파싱해 사용해야 합니다.

안전한 JSON 파싱을 사용하며 `eval()`은 사용하지 않습니다.

### Taste Cluster Model

`taste_cluster_model.joblib`은 취향 군집 구축 과정에서 사용한 별도의 특징 공간에서 학습된 모델입니다.

현재 저장된 콘텐츠 행렬을 해당 모델에 직접 입력하는 용도가 아닙니다.

기존 군집과 대표 메뉴를 활용한 취향 추천에는 별도의 재학습이 필요하지 않습니다.

### Example Recommendation Files

`data/examples/`의 결과는 모델 작동 확인을 위한 예시입니다.

실제 서비스에서는 해당 CSV 결과를 그대로 반환하지 않고 사용자가 입력한 조건으로 추천 함수를 실행해야 합니다.

---

## 🚧 Current Status

### Completed

- ✅ Food.com 데이터 전처리
- ✅ EDA 및 통계 분석
- ✅ 리뷰 및 텍스트 NLP 분석
- ✅ 재료 정규화
- ✅ 레시피 콘텐츠 특징 구축
- ✅ 콘텐츠 기반 취향 추천
- ✅ 보유 재료 기반 추천
- ✅ 추가 구매 기반 추천
- ✅ 장보기 재료 추천
- ✅ 추천 점수 및 다양성 로직 구축
- ✅ 웹 개발용 모델·자산 저장
- ✅ Google Drive 데이터 공유 구조 구축

### Next

- ⬜ Web UI 구현
- ⬜ Python 추천 API 연결
- ⬜ 사용자 입력 검증
- ⬜ 실제 추천 결과 화면 연결
- ⬜ 서비스 시나리오 테스트

---

## 💡 Service Flow

**냉장고 재료 입력**

↓  

**제외 재료 · 최대 조리시간 · 추가 구매 범위 설정**

↓  

**좋아하는 메뉴 선택 Optional**

↓  

**조건에 맞는 레시피 후보 생성**

↓  

**재료 · 추가 구매 · 취향 · 평점 · 시간 점수 계산**

↓  

**최종 레시피 추천**

↓  

**추가 구매 시 메뉴 확장 결과 제공**

↓  

**다음 장보기에 유용한 재료 추천**

---

## 🥄 한 줄로 정리하면

> **있는 재료는 최대한 활용하고, 살 재료는 최소화하면서,  
> 내 취향에 맞는 다음 한 끼를 추천하는 냉장고 기반 레시피 추천 시스템입니다.**

## 웹 서비스 실행·배포

현재 웹 구현은 `app/`에 있습니다. 실제 Python 추천 함수로 기본·취향·장보기 추천을 실행합니다.

- [로컬 실행 안내](docs/LOCAL_WEB.md)
- [무료 배포 안내](docs/DEPLOYMENT.md)
- [사진·한국어 재료 안내](docs/VISUALS_AND_TRANSLATIONS.md)

