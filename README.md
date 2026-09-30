# 🍳 자취생의 냉털을 부탁해!

**🌐 [냉털 시연하기](https://naengteol-wanr.onrender.com/)** · **📑 [최종 발표 자료](reports/presentation/final_presentation.pdf)**

외부 Render 서버에서 실행되어 개인 노트북이 꺼져 있어도 접속할 수 있습니다. 무료 서버는 미접속 시 절전 상태로 전환되어 첫 접속이 지연될 수 있습니다. 실제 예시 추천은 약 109초가 걸렸으며, 입력 조건에 따라 시간이 달라집니다.


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

원본 데이터는 **231,637개 레시피와 1,132,367건의 사용자 상호작용**으로 구성되며, 레시피 ID를 기준으로 연결합니다.

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

### EDA에서 정한 전처리 기준

- 이름이 결측인 레시피 1건은 제거하고, 리뷰가 없어도 평점이 있는 행은 유지했습니다.
- 영양성분 7종·조리시간·평가 및 리뷰 개수에는 `log1p`를 적용했습니다. 평점은 원척도를 유지했습니다.
- 조리시간 0분은 등록연도·조리 단계·가열 표현을 확인해 정제하고, 추천 범위는 **0분 초과 60분 이하**로 설정했습니다.
- 평가 수 편차를 보정하기 위해 베이지안 평점을 사용했습니다. 발표 기준 전체 평균은 `C=4.5406`, 사전 가중치는 평가 수 중앙값인 `m=2`입니다.

```text
Bayesian Rating = (v × R + m × C) / (v + m)
R: 레시피 평균 평점 · v: 평가 수 · C: 전체 평균 평점 · m: 사전 가중치
```

### Recipe Clustering · EDA

**재료 TF-IDF → SVD → K-means(K=6)**으로 데이터의 레시피 구성을 탐색했습니다. 음료·스무디, 베이킹·디저트, 일반 가정식 등 재료 조합의 패턴을 해석하는 용도이며, 취향 선택용 K=16 군집과 구분합니다.

### NLP

0점 리뷰의 의미를 확인하기 위해 **`cardiffnlp/twitter-roberta-base-sentiment-latest`**로 감성을 분석했습니다. 재료 간 의미적 관계는 별도로 **Word2Vec 50차원 벡터**로 표현해 콘텐츠 추천에 사용했습니다.

---

## 🧪 Hypothesis Testing

최종 발표 자료의 세 가지 가설검정을 추천 설계에 연결했습니다.

| 가설 | 분석 결과 | 추천 설계에 반영한 점 |
|---|---|---|
| 보유 재료 수에 따라 재료 추가 효과가 달라지는가? | 5·7·9개 조건에서 각각 100회 반복. Kruskal–Wallis `p=0.9623`, `ε²=0` | 재료 개수만으로 설명하기 어려워, 실제 보유 조합에서 추가 재료가 여는 메뉴 수를 계산 |
| 0점 평점은 부정적 평가인가? | 60,847건 중 긍정 66.44%·중립 17.49%·부정 16.07% | 발표의 평점 처리 기준에서는 긍정·중립 0점 51,067건을 평점 계산에서 제외 |
| 영양성분은 인기도·만족도와 관련이 있는가? | FDR 보정 후 12개 항목에서 유의하지만 `|ρ| ≤ 0.038`, 그룹 비교 효과크기도 매우 작음 | 통계적 유의성과 실질적 설명력을 구분하고, 영양성분을 핵심 추천 점수로 채택하지 않음 |

감성분석 결과는 모델의 예측이며, 리뷰 작성 의도를 확정하는 정답은 아닙니다.

---

## 🧠 Recommendation System

공통 후보 생성 엔진을 바탕으로 두 가지 추천을 제공합니다.

| 모델 | 질문 | 결과 |
|---|---|---|
| **MODEL 01 · 레시피 추천** | 오늘 뭐 먹지? | 바로 조리 / 추가 구매 후 조리 가능한 메뉴 |
| **MODEL 02 · 재료 추천** | 하나 더 뭐 살까? | 재료 하나로 새롭게 만들 수 있는 메뉴가 늘어나는 장보기 후보 |

### 🧂 Common Candidate Filter

- 기본 양념 47종은 별도 구매가 필요 없는 재료로 취급합니다.
- 소스·음료·요리 팁 등 실제 식사로 보기 어려운 레시피를 제외합니다.
- 보유 메인 재료가 하나 이상이고, 제외 재료·조리시간·추가 구매 범위를 만족하는 후보를 선별합니다.
- 메인 재료 판별은 5개 시나리오 검증을 거쳐 **RULE ❶+❷**를 채택해 양념·부재료만으로 과도한 추천이 발생하는 문제를 줄였습니다.

최종 추천은 하나의 기준만 사용하는 방식이 아니라 여러 요소를 함께 반영합니다.

### 1️⃣ Ingredient Match

사용자가 가지고 있는 재료로 해당 레시피를 얼마나 충족할 수 있는지 계산합니다.

완전히 만들 수 있는 레시피뿐 아니라 사용자가 허용한 범위 내에서 재료를 추가 구매하면 만들 수 있는 레시피도 후보에 포함합니다.

---

### 2️⃣ Purchase Cost

추가로 필요한 재료 수와 등장 빈도 기반 수급 난이도를 함께 반영합니다. 구매 부담이 적을수록 높은 점수를 부여합니다.

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

재료 TF-IDF · Word2Vec · 카테고리 벡터는 **1.0 : 1.0 : 0.5** 가중치로 결합합니다.

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

추가 구매 트랙의 기본 추천 점수는 다음 다섯 요소를 결합합니다.

| 요소 | Weight |
|---|---:|
| Ingredient Score | 30% |
| Purchase Score | 25% |
| Preference Score | 20% |
| Rating Score | 15% |
| Time Score | 10% |

즉, **현재 냉장고에 있는 재료를 최대한 활용하면서 추가 구매 부담을 줄이는 것**을 가장 중요한 기준으로 두고, 이후 사용자 취향과 레시피 평가·조리시간을 함께 반영합니다.

---

바로 조리 트랙은 구매 점수를 제외하고 가중치를 재정규화합니다. 취향 미선택 시에는 취향 점수도 제외하고 재정규화합니다. 추가 구매 트랙의 재료 점수는 **보유 재료 활용률과 레시피 재료 충족률**을 함께 반영합니다.

### 🌈 Diversity · MMR

비슷한 메뉴만 반복되지 않도록 최종 선택 단계에서 다양성을 보정합니다.

```text
선택 점수 = 0.9 × 추천 점수 − 0.1 × 이미 선택된 메뉴와의 최대 코사인 유사도
```

---

## 🛒 Grocery Recommendation

이 프로젝트에서는 레시피뿐 아니라 **다음에 어떤 재료를 사는 것이 효율적인지**도 추천합니다.

예를 들어 현재 냉장고에

`egg · onion · milk · cheddar cheese · bread`

가 있다고 가정하면,

부족 재료가 정확히 1개인 후보를 같은 재료끼리 묶어, 해당 재료를 추가했을 때 새롭게 만들 수 있는 레시피 수를 계산합니다. 메뉴 확장 수가 많은 재료를 상위 3개까지 추천하며, 장보기 순위 자체에는 취향 점수를 반영하지 않습니다.

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

취향 추천을 위한 레시피 군집은 **K=16**으로 구성했습니다. 재료 TF-IDF를 SVD로 축소한 뒤 군집화하고, 각 군집의 중심점과의 거리를 기준으로 대표 메뉴 3개를 선정했습니다. 웹에서는 이 후보 중 선호 메뉴를 최대 3개 선택하거나 생략할 수 있습니다.

> EDA에서 레시피 전체 구조를 살펴보기 위해 사용한 군집과 취향 선택을 위한 군집은 목적이 다르므로 별도로 관리합니다.

---

## 📁 Repository Structure

```text
26_2_ToyProject
│
├── app/                 # Python API · HTML/CSS/JavaScript
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
│   ├── figures/
│   └── presentation/
│       └── final_presentation.pdf
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
| `app/` | 실제 추천 API와 웹 화면 |
| `reports/presentation/` | 최종 발표 PDF |
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

현재 **HTML·CSS·JavaScript 화면과 FastAPI 서버를 연결**해 실제 Python 추천을 실행합니다. 사용자 요청마다 분석·학습을 다시 실행하지 않고 저장된 모델과 데이터를 사용합니다.

### 1. Repository Clone

```bash
git clone https://github.com/Dana-J2/26_2_ToyProject.git
cd 26_2_ToyProject
```

### 2. Large CSV Download

위 Google Drive의 `recipes_model_v4.csv`를 내려받아 `web_assets/recipes_model_v4.csv`에 배치합니다.

### 3. Python Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-web.txt
```

저장 모델의 라이브러리 버전은 `requirements-assets.txt`, 웹 실행 의존성은 `requirements-web.txt`에서 확인할 수 있습니다.

### 4. Asset Verification & Run

```bash
python scripts/verify_assets.py
python -m uvicorn app.main:app --host 127.0.0.1 --port 8765
```

브라우저에서 `http://127.0.0.1:8765`를 엽니다. 첫 실행에는 데이터 로딩 시간이 필요합니다. 웹 실행을 위해 감성분석이나 노트북 전체를 재실행할 필요는 없습니다.

### 5. Recommendation Functions

전체 분석은 `notebooks/Final_Analysis_Colab.ipynb`, 웹에서 사용하는 추천 함수는 `app/recommender.py`, API 연결은 `app/main.py`에 있습니다.

👉 [로컬 실행 안내](docs/LOCAL_WEB.md) · [모델·자산 연결 가이드](docs/WEB_HANDOFF.md) · [배포 안내](docs/DEPLOYMENT.md)

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

- ✅ HTML·CSS·JavaScript 웹 화면 구현
- ✅ Python 추천 API 연결 및 입력 검증
- ✅ 실제 추천·장보기 결과 화면 연결
- ✅ 무료 외부 서버 배포

### Next

- 국내 레시피 및 재료 데이터 보강
- 사용자 피드백 기반 개인화 개선
- 추천 속도 및 동시 접속 처리 개선

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

## 🌱 Limitations & Next Steps

- **국내 요리 반영:** 해외 레시피 중심이라 국내 자취 식문화와 재료 접근성을 충분히 반영하지 못합니다.
- **평가 희소성:** 사용자·레시피 간 평가가 부족해 개인화 수준에 제약이 있습니다.
- **규칙과 예측:** 기본 양념 보유 가정, 재료 수급 난이도, 감성 예측은 실제 사용자 상황과 다를 수 있습니다.
- **서비스 운영:** 무료 서버에서는 추천 응답이 느릴 수 있으며, 40명 동시 시연 성능은 보장하지 않습니다.

---

## 🥄 한 줄로 정리하면

> **있는 재료는 최대한 활용하고, 살 재료는 최소화하면서,
> 내 취향에 맞는 다음 한 끼를 추천하는 냉장고 기반 레시피 추천 시스템입니다.**

## 🔗 Related Documents

현재 웹 구현은 `app/`에 있습니다. 실제 Python 추천 함수로 기본·취향·장보기 추천을 실행합니다.

- [로컬 실행 안내](docs/LOCAL_WEB.md)
- [무료 배포 안내](docs/DEPLOYMENT.md)
- [사진·한국어 재료 안내](docs/VISUALS_AND_TRANSLATIONS.md)
