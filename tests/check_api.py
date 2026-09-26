"""실행 중인 로컬 서버에서 추천 조건을 확인한다."""
import json
import urllib.request
import urllib.error
BASE='http://127.0.0.1:8765'
def get(path):
    with urllib.request.urlopen(BASE+path) as r:return json.load(r)
def recommend(**changes):
    payload={'owned_ingredients':['egg','onion','milk','cheddar cheese','bread'],'excluded_ingredients':['shrimp'],'max_minutes':60,'max_extra_ingredients':2,'liked_recipe_ids':[]}
    payload.update(changes)
    request=urllib.request.Request(BASE+'/api/recommend',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(request) as r:return json.load(r)
assert get('/api/status')['status']=='ready'
basic=recommend()
assert basic['ready'] and basic['extra'] and basic['shopping']
for track in ['ready','extra']:
    for r in basic[track]:
        assert r['minutes']<=60
        assert not any('shrimp' in x for x in r['ingredients'])
        assert (len(r['missing'])==0 if track=='ready' else len(r['missing'])>=1)
        assert len(r['missing'])<=2
assert basic['shopping'][0]['ingredient']=='flour'
assert basic['shopping'][0]['new_recipes']==45
assert get('/api/recipes/'+str(basic['ready'][0]['id']))['steps']
tastes=get('/api/tastes')
liked=[tastes[0]['id'],tastes[1]['id']]
personal=recommend(liked_recipe_ids=liked)
assert personal['personalized']
assert all(r['id'] not in liked for t in ['ready','extra'] for r in personal[t])
assert any(r['preference_score']!=0 for t in ['ready','extra'] for r in personal[t])
assert recommend(max_extra_ingredients=0)['extra']==[]
empty=recommend(owned_ingredients=['salt'],max_extra_ingredients=0)
assert not empty['ready'] and not empty['extra']
try:recommend(liked_recipe_ids=[-1])
except urllib.error.HTTPError as e:assert e.code==422
else:raise AssertionError('Invalid ID accepted')
print('PASS: basic, personal, excluded ingredient, shopping count, recipe steps, zero purchase, empty results, invalid ID')
