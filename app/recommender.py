"""통합 노트북의 추천 함수를 그대로 분리한 모듈."""

import re

import numpy as np

import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

def normalize_base(name):
    s = " ".join(str(name).lower().strip().split())
    return BASE_ALIASES.get(s, s)

def normalize_model_ingredient(name):
    s = normalize_base(name)
    return MERGE_MAP.get(s, s)

def tier_of(name):
    return INGREDIENT_TIER.get(name, 4)

def contains_excluded(ingredient_set, excluded_set):
    for ing in ingredient_set:
        for ex in excluded_set:
            if re.search(r"\b" + re.escape(ex) + r"\b", ing):
                return True
    return False

def build_candidates(owned_raw, excluded_raw, max_min, max_extra, liked_id=None, rule_type='rules_1_2'):
    if rule_type not in {'rules_1_2', 'rule2'}:
        raise ValueError('rule_type을 확인하세요.')
    if not 0 < max_min <= 60 or not isinstance(max_extra, int) or max_extra < 0:
        raise ValueError('조리시간은 1~60분, 추가 구매 수는 0 이상입니다.')
    liked_ids = [] if liked_id is None else ([int(liked_id)] if np.isscalar(liked_id) else list(dict.fromkeys(map(int, liked_id))))
    unknown = [rid for rid in liked_ids if rid not in model_id_to_idx.index]
    if unknown:
        raise ValueError(f'추천 대상에 없는 선호 ID: {unknown}')
    owned = {normalize_model_ingredient(i) for i in owned_raw}
    excluded = {normalize_model_ingredient(i) for i in excluded_raw}
    main_col = "main_ings_rule1_2" if rule_type == 'rules_1_2' else "main_ings_rule2"
    has_excluded = (
        model_recipes["ingredient_set"].apply(lambda s: contains_excluded(s, excluded))
        if excluded else pd.Series(False, index=model_recipes.index)
    )
    missing = model_recipes["core_set"].apply(lambda x: sorted(x - owned))
    missing_n = missing.apply(len)
    owned_main = model_recipes[main_col].apply(lambda x: len(x & owned))
    mask = (
        model_recipes["is_meal_candidate"]
        & model_recipes["minutes_rec"].notna()
        & (model_recipes["minutes_rec"] <= max_min)
        & (~has_excluded)
        & (missing_n <= max_extra)
        & (owned_main >= 1)
    )
    if liked_ids:
        mask &= ~model_recipes["id"].isin(liked_ids)
    candidates = model_recipes[mask].copy()
    if len(candidates) == 0:
        for col in ["missing_core", "missing_count", "owned_main_count", "owned_core_count",
                    "utilization", "match_ratio", "purchase_cost", "max_missing_tier",
                    "time_score", "rating_score", "preference_score"]:
            candidates[col] = []
        return candidates, owned
    candidates["missing_core"] = missing[mask]
    candidates["missing_count"] = missing_n[mask]
    candidates["owned_main_count"] = owned_main[mask]
    candidates["owned_core_count"] = candidates["core_set"].apply(lambda x: len(x & owned))
    candidates["utilization"] = candidates["owned_core_count"] / max(len(owned), 1)
    candidates["match_ratio"] = candidates["core_set"].apply(
        lambda x: len(x & owned) / len(x) if x else 1.0)
    candidates["purchase_cost"] = candidates["missing_core"].apply(
        lambda xs: sum(1.0 + TIER_DIFFICULTY[tier_of(i)] for i in xs))
    candidates["max_missing_tier"] = candidates["missing_core"].apply(
        lambda xs: max((tier_of(i) for i in xs), default=0))
    candidates["time_score"] = (1 - candidates["minutes_rec"] / max_min).clip(0, 1)
    candidates["rating_score"] = ((candidates["bayesian_rating_rec"] - 1) / 4).clip(0, 1)
    if liked_ids:
        candidates["preference_score"] = cosine_similarity(
            X_model_content[model_id_to_idx.loc[liked_ids].to_numpy()], X_model_content
        ).mean(axis=0)[candidates.index]
    else:
        candidates["preference_score"] = 0.0
    return candidates, owned

def diversify(candidates, top_k=10, pool_size=100, relevance_weight=0.9):
    pool = candidates.sort_values("final_score", ascending=False).head(pool_size).copy()
    remaining, selected = list(pool.index), []
    while remaining and len(selected) < top_k:
        if not selected:
            best = remaining[0]
        else:
            sims = cosine_similarity(
                X_model_content[remaining], X_model_content[selected]).max(axis=1)
            best, best_mmr = None, -np.inf
            for pos, idx in enumerate(remaining):
                mmr = (relevance_weight * pool.loc[idx, "final_score"]
                       - (1 - relevance_weight) * sims[pos])
                if mmr > best_mmr:
                    best_mmr, best = mmr, idx
        selected.append(best)
        remaining.remove(best)
    return pool.loc[selected]

def score_tracks(candidates, max_extra=2, use_preference=True, top_k=10):
    wa = {"ingredient_score": .30, "preference_score": .20,
          "rating_score": .15, "time_score": .10}
    wb = dict(FINAL_WEIGHTS)
    if not use_preference:
        wa.pop("preference_score")
        wb.pop("preference_score")
    wa = {k: v / sum(wa.values()) for k, v in wa.items()}
    wb = {k: v / sum(wb.values()) for k, v in wb.items()}
    a = candidates[candidates["missing_count"] == 0].copy()
    a_top = None
    if len(a) > 0:
        a["ingredient_score"] = a["utilization"]
        a["final_score"] = sum(a[k] * v for k, v in wa.items())
        a_top = diversify(a, top_k=top_k)
    b = candidates[candidates["missing_count"] >= 1].copy()
    b_top = None
    if len(b) > 0:
        b["ingredient_score"] = .5 * b["match_ratio"] + .5 * b["utilization"]
        b["purchase_score"] = (
            1 - b["purchase_cost"] / (max_extra * 2.0)).clip(0, 1)
        b["final_score"] = sum(b[k] * v for k, v in wb.items())
        b_top = diversify(b, top_k=top_k)
    return a_top, b_top

def get_final_recommendations(user_input, rule_type='rules_1_2', top_k=10):
    max_min = user_input.get("max_minutes", 60)
    max_extra = user_input.get("max_extra_ingredients", 2)
    liked_id = user_input.get("liked_recipe_id", None)
    use_pref = liked_id is not None and (np.isscalar(liked_id) or len(liked_id) > 0)
    candidates, owned_set = build_candidates(
        owned_raw=user_input["owned_ingredients"],
        excluded_raw=user_input["excluded_ingredients"],
        max_min=max_min,
        max_extra=max_extra,
        liked_id=liked_id,
        rule_type=rule_type
    )
    if len(candidates) == 0:
        print("조건을 만족하는 추천 후보 레시피가 없습니다.")
        return None, None
    track_a, track_b = score_tracks(
        candidates=candidates,
        max_extra=max_extra,
        use_preference=use_pref,
        top_k=top_k
    )
    return track_a, track_b

def suggest_grocery_shopping(owned_raw, excluded_raw, max_min=60, top_n_ingredients=3, top_k_recipes=3):
    candidates, _ = build_candidates(owned_raw, excluded_raw, max_min, 1, rule_type='rules_1_2')
    candidates = candidates.loc[candidates['missing_count'].eq(1)].copy()
    columns = ['ingredient', 'new_recipes', 'tier', 'example_ids', 'example_names']
    if candidates.empty:
        return pd.DataFrame(columns=columns)
    candidates['purchase_ingredient'] = candidates['missing_core'].map(lambda items: items[0])
    summary = candidates.groupby('purchase_ingredient').size().rename('new_recipes').reset_index()
    summary = summary.rename(columns={'purchase_ingredient': 'ingredient'})
    summary['tier'] = summary['ingredient'].map(tier_of)
    summary = summary.sort_values(['new_recipes', 'tier', 'ingredient'], ascending=[False, True, True]).head(top_n_ingredients)
    ids, names = [], []
    for ingredient in summary['ingredient']:
        examples = candidates.loc[candidates['purchase_ingredient'].eq(ingredient)].sort_values(
            ['bayesian_rating_rec', 'id'], ascending=[False, True]
        ).head(top_k_recipes)
        ids.append(examples['id'].tolist())
        names.append(examples['name'].tolist())
    summary['example_ids'], summary['example_names'] = ids, names
    return summary[columns]
