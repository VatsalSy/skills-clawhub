from typing import Dict, Any, List
from parser import parse_meal_text
from units import to_grams
from cache import get as cache_get, set as cache_set
from usda_fdc import search_food, pick_best_candidate, get_food_detail, extract_per_100g_nutrients, USDAError
from translate import translate_food_name, is_chinese

QUERY_TTL = 24 * 3600
ITEM_TTL = 7 * 24 * 3600

def _round(x: float) -> float:
    return round(float(x), 1)

def _error(message: str, status: int = 500) -> Dict[str, Any]:
    return {"ok": False, "error": message, "status": status}

def lookup_food(name: str, qty: float, unit: str) -> Dict[str, Any]:
    grams, note = to_grams(name, qty, unit)
    if grams is None:
        return {
            "ok": False,
            "reason": note,
            "question": {
                "field": "amount_in_grams",
                "ask": f"「{name}」的份量我没法换算：你大概吃了多少克(g)或毫升(ml)？（例如 150g）"
            }
        }

    cache_key = f"item::{name.lower().strip()}::{int(round(grams))}g"
    cached = cache_get(cache_key)
    if cached:
        return {"ok": True, **cached}

    # Dictionary-based translation (acceleration cache for known Chinese names).
    # For unknown names, the main agent should use the Decomposer sub-agent (LLM).
    search_name = name
    translate_note = None
    if is_chinese(name):
        search_name, translate_note = translate_food_name(name)

    try:
        cands = search_food(search_name)
        best, conf = pick_best_candidate(cands, search_name)
        if not best:
            return {
                "ok": False,
                "reason": "not_found",
                "question": {
                    "field": "food_clarify",
                    "ask": f"我在USDA里没搜到「{name}」。你能换个更像“食材”的说法吗？（例如：鸡胸肉/熟米饭/全脂牛奶）"
                }
            }

        fdc_id = int(best["fdcId"])
        detail = get_food_detail(fdc_id)
        per100 = extract_per_100g_nutrients(detail)

        factor = grams / 100.0
        item = {
            "name_raw": f"{name} {qty}{unit}",
            "name_std": best.get("description") or name,
            "qty": qty,
            "unit": unit,
            "grams": _round(grams),
            "kcal": _round(per100["kcal"] * factor),
            "protein_g": _round(per100["protein_g"] * factor),
            "carb_g": _round(per100["carb_g"] * factor),
            "fat_g": _round(per100["fat_g"] * factor),
            "fiber_g": _round(per100["fiber_g"] * factor),
            "source": "usda_fdc",
            "fdcId": fdc_id,
            "confidence": _round(conf),
            "notes": [n for n in [note, translate_note] if n]
        }

        cache_set(cache_key, item, ITEM_TTL)
        return {"ok": True, **item}
    except USDAError as e:
        return _error(str(e), status=e.status or 500)
    except Exception as e:
        return _error(f"USDA 查询失败：{e}")

def lookup_meal(text: str, meal_type: str = "unknown") -> Dict[str, Any]:
    qkey = f"meal::{meal_type}::{text.strip().lower()}"
    cached = cache_get(qkey)
    if cached:
        return cached

    parsed = parse_meal_text(text)
    items: List[Dict[str, Any]] = []
    questions: List[Dict[str, Any]] = []

    for p in parsed:
        if len(p.name) <= 1:
            continue

        if p.qty is None or p.unit is None:
            if len(questions) < 2:
                questions.append({
                    "field": "missing_amount",
                    "ask": f"「{p.name}」你吃了多少？给我一个数字+单位（如 200g / 250ml / 1碗 / 2个）"
                })
            continue

        r = lookup_food(p.name, p.qty, p.unit)
        if not r.get("ok"):
            if "question" in r and len(questions) < 2:
                questions.append(r["question"])
            elif "error" in r and len(questions) < 2:
                questions.append({
                    "field": "api_error",
                    "ask": r["error"]
                })
            continue

        items.append(r)

    totals = {
        "kcal": _round(sum(i["kcal"] for i in items)),
        "protein_g": _round(sum(i["protein_g"] for i in items)),
        "carb_g": _round(sum(i["carb_g"] for i in items)),
        "fat_g": _round(sum(i["fat_g"] for i in items)),
        "fiber_g": _round(sum(i["fiber_g"] for i in items)),
    }

    out = {
        "type": "meal_nutrition",
        "meal_type": meal_type,
        "items": items,
        "totals": totals,
        "questions": questions
    }

    if items:
        cache_set(qkey, out, QUERY_TTL)
    return out
