"""재료 ID를 유지하는 한국어 표시와 검색 별칭."""
import json
import re
from functools import lru_cache
from pathlib import Path
TERMS = json.loads(Path(__file__).with_name('ingredient_ko.json').read_text())
ALIASES = {'계란':'달걀','계란흰자':'달걀흰자','계란노른자':'달걀노른자','쇠고기':'소고기','소고기':'소고기','닭 가슴살':'닭가슴살','양송이':'양송이','우스터 소스':'우스터소스','마요네즈':'마요네즈','녹말':'전분','전지우유':'통 우유','파마산':'파르메산','모짜렐라':'모차렐라','쥬스':'주스','요구르트':'요거트','버터넛호박':'버터넛 호박'}
# 긴 재료 이름부터 매칭한다.
PATTERN = re.compile(r"(?<![a-z])(" + '|'.join(re.escape(s) for s in sorted(TERMS,key=len,reverse=True)) + r")(?![a-z])", re.I)
@lru_cache(maxsize=20000)
def label(value):
    text=value.lower().strip()
    if text in TERMS:return TERMS[text]
    text=text.replace('salt & pepper','salt and pepper').replace('fresh ground','freshly ground')
    # 사전에 없는 복수형만 단수형을 확인한다.
    def singular(match):
        word=match.group()
        if word in TERMS:return word
        for candidate in [word[:-3]+'y' if word.endswith('ies') else '',word[:-2] if word.endswith('es') else '',word[:-1] if word.endswith('s') else '']:
            if candidate and candidate in TERMS:return candidate
        return word
    text=re.sub(r"[a-z]+",singular,text)
    result=PATTERN.sub(lambda m:TERMS[m.group().lower()],text)
    return re.sub(r'\s+',' ',result).strip(' ,')
def search_key(value):
    text=value.lower().strip()
    for old,new in ALIASES.items():text=text.replace(old,new)
    return re.sub(r'[\s\-·,]','',text)
