"""배포용 경량 데이터 생성. 원본 ID, 값, 행 순서를 보존한다."""
from pathlib import Path
import collections
import gzip
import hashlib
import json
import sqlite3
import sys
import zipfile
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'web_assets'
out=ROOT/'runtime_assets'
out.mkdir(exist_ok=True)
set_cols=['ingredient_set','core_set','main_ings_rule1_2','main_ings_rule2']
cols=['id','name','minutes_rec','bayesian_rating_rec','is_meal_candidate','taste_cluster']
details=['steps_list','ingredients_list','description']
vocabulary={};counts=collections.Counter();rows=[]
flat={c:[] for c in set_cols};offsets={c:[0] for c in set_cols}
db=sqlite3.connect(out/'details.sqlite');db.execute('DROP TABLE IF EXISTS recipes');db.execute('CREATE TABLE recipes (id INTEGER PRIMARY KEY, payload BLOB NOT NULL)')
for chunk in pd.read_csv(source/'recipes_model_v4.csv',usecols=cols+set_cols+details,keep_default_na=False,chunksize=5000):
 for row in chunk.to_dict('records'):
  rows.append({k:row[k] for k in cols})
  for c in set_cols:
   items=json.loads(row[c])
   if c=='ingredient_set':counts.update(items)
   for s in items:
    if s not in vocabulary:vocabulary[s]=len(vocabulary)
    flat[c].append(vocabulary[s])
   offsets[c].append(len(flat[c]))
  detail={'steps':json.loads(row['steps_list']),'original_ingredients':json.loads(row['ingredients_list']),'description':row['description']}
  db.execute('INSERT INTO recipes VALUES (?,?)',(int(row['id']),gzip.compress(json.dumps(detail,ensure_ascii=False).encode(),mtime=0)))
 db.commit()
db.close()
with gzip.open(out/'recipes.json.gz','wt') as f:json.dump(rows,f)
(out/'vocabulary.json').write_text(json.dumps(list(vocabulary)))
(out/'ingredient_counts.json').write_text(json.dumps(counts))
for c in set_cols:
 np.save(out/(c+'_values.npy'),np.array(flat[c],dtype=np.int32))
 np.save(out/(c+'_offsets.npy'),np.array(offsets[c],dtype=np.int32))
with zipfile.ZipFile(source/'content_matrix.npz') as z:
 for name in ['data.npy','indices.npy','indptr.npy','shape.npy']:
  (out/('matrix_'+name)).write_bytes(z.read(name))
files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.name!='manifest.json'}
(out/'manifest.json').write_text(json.dumps({'count':len(rows),'files':files},indent=2))
print('Prepared',len(rows),'recipes; bytes',sum(p.stat().st_size for p in out.iterdir()))
