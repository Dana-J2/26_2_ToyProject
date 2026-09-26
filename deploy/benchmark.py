import os,sys,time,resource,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import packed_assets,recommender as e
import joblib,pandas as pd
root=Path(__file__).resolve().parents[1]
t=time.time();f,m,c=packed_assets.load(root/'runtime_assets')
e.cosine_similarity=packed_assets.bounded_cosine
e.model_recipes=f;e.X_model_content=m;e.model_id_to_idx=pd.Series(f.index,index=f.id)
for k,v in joblib.load(root/'web_assets/recommendation_rules.joblib').items():setattr(e,k,v)
def memory():return round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(2**20 if sys.platform=='darwin' else 1024),1)
print('load',round(time.time()-t,2),'s peak',memory(),flush=True)
for liked in [None,[37825,310914]]:
 t=time.time();payload=dict(owned_ingredients=['egg','onion','milk','cheddar cheese','bread'],excluded_ingredients=['shrimp'],max_minutes=60,max_extra_ingredients=2,liked_recipe_id=liked)
 a,b=e.get_final_recommendations(payload,top_k=6);g=e.suggest_grocery_shopping(payload['owned_ingredients'],payload['excluded_ingredients'])
 print('recommend',liked,round(time.time()-t,2),'s peak',memory(),'MiB',flush=True)
 print('IDs',a.id.tolist(),b.id.tolist(),'shopping',g[['ingredient','new_recipes']].to_dict('records'),flush=True)
