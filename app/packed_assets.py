"""원본 재료 집합을 작은 배열에 보관하는 배포용 로더."""
from pathlib import Path
import gzip
import json
import sqlite3
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
class IngredientSet:
    __slots__=('index','column')
    def __init__(self,index,column):self.index,self.column=index,column
    def __len__(self):
        values,offsets,vocabulary=self.column
        return int(offsets[self.index+1]-offsets[self.index])
    def __iter__(self):
        values,offsets,vocabulary=self.column
        return (vocabulary[int(i)] for i in values[offsets[self.index]:offsets[self.index+1]])
    def __contains__(self,value):return any(value==s for s in self)
    def __sub__(self,other):return {s for s in self if s not in other}
    def __and__(self,other):return {s for s in self if s in other}
def load(folder):
    folder=Path(folder)
    with gzip.open(folder/'recipes.json.gz','rt') as f:frame=pd.DataFrame(json.load(f))
    vocabulary=json.loads((folder/'vocabulary.json').read_text())
    for c in ['ingredient_set','core_set','main_ings_rule1_2','main_ings_rule2']:
        values=np.load(folder/(c+'_values.npy'),mmap_mode='r');offsets=np.load(folder/(c+'_offsets.npy'),mmap_mode='r')
        column=(values,offsets,vocabulary)
        frame[c]=[IngredientSet(i,column) for i in range(len(frame))]
    matrix=csr_matrix(tuple(np.load(folder/('matrix_'+name+'.npy'),mmap_mode='r') for name in ['data','indices','indptr']),shape=tuple(np.load(folder/'matrix_shape.npy')),copy=False)
    return frame,matrix,json.loads((folder/'ingredient_counts.json').read_text())
def detail(folder,recipe_id):
    with sqlite3.connect(f'file:{Path(folder)/"details.sqlite"}?mode=ro',uri=True) as db:
        row=db.execute('SELECT payload FROM recipes WHERE id=?',(recipe_id,)).fetchone()
    if row is None:raise KeyError(recipe_id)
    return json.loads(gzip.decompress(row[0]))
def bounded_cosine(left,right):
    """동일한 코사인 유사도를 열 묶음별로 계산한다."""
    from sklearn.metrics.pairwise import cosine_similarity
    if right.shape[0]<=8192:return cosine_similarity(left,right)
    result=np.empty((left.shape[0],right.shape[0]),dtype=np.result_type(left.dtype,right.dtype))
    for start in range(0,right.shape[0],8192):
        result[:,start:start+8192]=cosine_similarity(left,right[start:start+8192])
    return result
