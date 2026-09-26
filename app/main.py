from contextlib import asynccontextmanager
from pathlib import Path
from threading import Lock, Thread
import json
import logging
import sys
import os
import joblib
import numpy as np
import pandas as pd
from scipy.sparse import load_npz
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from . import recommender as engine

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'web_assets'
STATIC = ROOT / 'app/static'
PACKED = os.environ.get('USE_PACKED_ASSETS') == '1'
RUNTIME = ROOT / 'runtime_assets'
state = {'status': 'loading', 'message': '레시피를 준비하고 있어요.'}
compute_lock = Lock()
from .localization import label, search_key

def load_assets():
    try:
        settings = json.loads((ASSETS / 'web_settings.json').read_text())
        if PACKED:
            from . import packed_assets
            frame, matrix, packed_counts = packed_assets.load(RUNTIME)
            engine.cosine_similarity = packed_assets.bounded_cosine
        else:
            source = ASSETS / 'recipes_model_v4.csv'
            if not source.exists():
                raise FileNotFoundError('web_assets/recipes_model_v4.csv를 내려받아 주세요. README에 링크가 있습니다.')
            columns = ['id','name','minutes_rec','bayesian_rating_rec','ingredient_set','core_set','main_ings_rule1_2','main_ings_rule2','is_meal_candidate','steps_list','ingredients_list','description','taste_cluster']
            header = pd.read_csv(source, nrows=0).columns
            frame = pd.read_csv(source, usecols=[c for c in columns if c in header], keep_default_na=False)
            for col in ['ingredient_set','core_set','main_ings_rule1_2','main_ings_rule2']:
                frame[col] = frame[col].map(lambda value: {sys.intern(s) for s in json.loads(value)})
            if frame['is_meal_candidate'].dtype != bool:
                frame['is_meal_candidate'] = frame['is_meal_candidate'].map({'True':True,'False':False})
            matrix = load_npz(ASSETS / 'content_matrix.npz')
        mapping = pd.read_csv(ASSETS / 'recipe_row_mapping.csv')
        if not np.array_equal(frame['id'].to_numpy(), mapping['recipe_id'].to_numpy()):
            raise ValueError('레시피와 콘텐츠 행렬의 ID 순서가 다릅니다.')
        if list(matrix.shape) != settings['content_shape'] or len(frame) != matrix.shape[0]:
            raise ValueError('콘텐츠 행렬 크기를 확인하세요.')
        if not np.array_equal(mapping['row_index'], np.arange(len(frame))) or not frame['id'].is_unique:
            raise ValueError('레시피 행 매핑을 확인하세요.')
        rules = joblib.load(ASSETS / 'recommendation_rules.joblib')
        for name in ['BASE_ALIASES','MERGE_MAP','INGREDIENT_TIER','TIER_DIFFICULTY','FINAL_WEIGHTS']:
            setattr(engine, name, rules[name])
        engine.model_recipes = frame
        engine.X_model_content = matrix
        engine.model_id_to_idx = pd.Series(frame.index, index=frame['id'])
        counts = pd.Series(packed_counts).sort_values(ascending=False) if PACKED else frame['ingredient_set'].explode().value_counts()
        state['ingredients'] = [{'id':s,'label':label(s),'count':int(count)} for s,count in counts.items()]
        state['vocabulary'] = set(counts.index)
        tastes = pd.read_csv(ASSETS / 'taste_menu_candidates_v4.csv')
        state['tastes'] = [recipe_card(frame.loc[engine.model_id_to_idx.loc[int(row.id)]]) | {'cluster':int(row.taste_cluster)} for row in tastes.itertuples()]
        state.update(status='ready', message='준비 완료', recipe_count=len(frame))
    except Exception as exc:
        logging.exception('Asset loading failed')
        state.update(status='error', message=str(exc))

@asynccontextmanager
async def lifespan(app):
    Thread(target=load_assets, daemon=True).start()
    yield

app = FastAPI(title='냉털 · 레시피 추천', lifespan=lifespan)
app.mount('/static', StaticFiles(directory=STATIC), name='static')

@app.get('/')
def home():
    return FileResponse(STATIC / 'index.html')

@app.get('/api/health')
def health():
    if state['status'] != 'ready':
        raise HTTPException(503,state['message'])
    return {'status':'ready'}

@app.get('/api/status')
def status():
    return {k:state[k] for k in ['status','message','recipe_count'] if k in state}

def require_ready():
    if state['status'] != 'ready':
        raise HTTPException(503, state['message'])

@app.get('/api/ingredients')
def ingredients(q: str = Query('', max_length=80)):
    require_ready()
    query = q.strip().lower()
    korean_query = search_key(query)
    rows = state['ingredients']
    if query:
        rows = [r for r in rows if query in r['id'] or korean_query in search_key(r['label'])]
        rows = sorted(rows, key=lambda r:(r['id']!=query and r['label']!=query,-r['count']))
    return rows[:12]

@app.get('/api/tastes')
def tastes():
    require_ready()
    return state['tastes']

def recipe_card(row):
    items = sorted(row['ingredient_set'])
    missing = row.get('missing_core', [])
    return {'id':int(row['id']),'name':str(row['name']),'minutes':float(row['minutes_rec']),
            'rating':round(float(row['bayesian_rating_rec']),2),'ingredients':items,
            'ingredient_labels':[label(s) for s in items],
            'missing':[{'id':s,'label':label(s)} for s in missing],
            'owned_count':int(row.get('owned_core_count',0)),'core_count':len(row['core_set']),
            'preference_score':float(row.get('preference_score',0)),
            'score':float(row.get('final_score',0))}

class RecommendationInput(BaseModel):
    owned_ingredients: list[str] = Field(min_length=1, max_length=60)
    excluded_ingredients: list[str] = Field(default_factory=list, max_length=30)
    max_minutes: int = Field(default=60, ge=1, le=60)
    max_extra_ingredients: int = Field(default=2, ge=0, le=5)
    liked_recipe_ids: list[int] = Field(default_factory=list, max_length=3)

@app.post('/api/recommend')
def recommend(body: RecommendationInput):
    require_ready()
    owned = list(dict.fromkeys(s.strip() for s in body.owned_ingredients if s.strip()))
    excluded = list(dict.fromkeys(s.strip() for s in body.excluded_ingredients if s.strip()))
    if not owned or any(len(s)>100 for s in owned+excluded):
        raise HTTPException(422,'보유 재료를 선택해 주세요.')
    if any(s not in state['vocabulary'] for s in owned+excluded):
        raise HTTPException(422,'검색 목록에 있는 재료를 선택해 주세요.')
    liked = list(dict.fromkeys(body.liked_recipe_ids))
    if any(i not in engine.model_id_to_idx.index for i in liked):
        raise HTTPException(422,'선호 메뉴 ID를 확인해 주세요.')
    value = {'owned_ingredients':owned,'excluded_ingredients':excluded,'max_minutes':body.max_minutes,
             'max_extra_ingredients':body.max_extra_ingredients,'liked_recipe_id':liked or None}
    with compute_lock:
        a,b = engine.get_final_recommendations(value,top_k=6)
        grocery = engine.suggest_grocery_shopping(owned,excluded,body.max_minutes)
    def cards(frame):return [] if frame is None else [recipe_card(row) for _,row in frame.iterrows()]
    shopping = [{'ingredient':r.ingredient,'label':label(r.ingredient),'new_recipes':int(r.new_recipes),
                 'tier':int(r.tier),'examples':[{'id':int(i),'name':n} for i,n in zip(r.example_ids,r.example_names)]}
                for r in grocery.itertuples()]
    return {'ready':cards(a),'extra':cards(b),'shopping':shopping,'personalized':bool(liked),
            'conditions':body.model_dump()}

@app.get('/api/recipes/{recipe_id}')
def detail(recipe_id:int):
    require_ready()
    if recipe_id not in engine.model_id_to_idx.index:
        raise HTTPException(404,'레시피를 찾을 수 없습니다.')
    row = engine.model_recipes.loc[engine.model_id_to_idx.loc[recipe_id]]
    if PACKED:
        from .packed_assets import detail as read_detail
        return recipe_card(row) | read_detail(RUNTIME,recipe_id)
    return recipe_card(row) | {'steps':json.loads(row.get('steps_list','[]')),
                              'original_ingredients':json.loads(row.get('ingredients_list','[]')),
                              'description':str(row.get('description',''))}
