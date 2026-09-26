"""배포 데이터의 원본 일치와 유사도 계산 동등성 확인."""
import sys,json,gzip
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.packed_assets import load,detail,bounded_cosine
root=Path(__file__).resolve().parents[1]
f,m,counts=load(root/'runtime_assets')
columns=['id','name','minutes_rec','bayesian_rating_rec','ingredient_set','core_set','main_ings_rule1_2','main_ings_rule2']
position=0
for chunk in pd.read_csv(root/'web_assets/recipes_model_v4.csv',usecols=columns,keep_default_na=False,chunksize=5000):
 for row in chunk.to_dict('records'):
  target=f.iloc[position]
  assert row['id']==target.id and row['name']==target['name']
  assert row['minutes_rec']==target.minutes_rec and row['bayesian_rating_rec']==target.bayesian_rating_rec
  for col in columns[4:]:assert set(json.loads(row[col]))==set(target[col]),(position,col)
  position+=1
assert position==168035
# 묶음 경계 양쪽의 실제 콘텐츠 벡터로 비교한다.
query=m[[0,8191,168034]];right=m[:17000]
np.testing.assert_allclose(bounded_cosine(query,right),cosine_similarity(query,right),rtol=1e-12,atol=1e-12)
assert detail(root/'runtime_assets',int(f.iloc[0].id))['original_ingredients']
print('PASS: all 168,035 row values/ingredient sets; chunked cosine; recipe detail')
