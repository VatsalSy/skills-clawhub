# calorie-lookup

USDA FoodData Central 营养查询与热量估算 Agent Skill。

将自然语言食物输入（支持中文）转化为结构化营养数据：热量、蛋白质、碳水、脂肪、膳食纤维。

USDA FoodData Central nutrition lookup & meal calorie estimation agent skill.

Converts natural language food input (Chinese supported) into structured nutrition data: calories, protein, carbs, fat, and fiber.

---

## 快速开始 / Quick Start

```bash
# 1. 安装依赖 / Install dependencies
python -m pip install -r requirements.txt

# 2. 复制配置文件并填入 API Key / Copy config and fill in your API key
#    免费申请 / Free sign-up：https://fdc.nal.usda.gov/api-key-signup.html
cp scripts/config_example.py scripts/config.py
# 编辑 scripts/config.py，填入你的 USDA_API_KEY
# Edit scripts/config.py and set your USDA_API_KEY

# 3. 试运行 / Try it
PYTHONPATH=scripts python -c "
from core import lookup_meal
print(lookup_meal('chicken breast 200g + rice 1 bowl'))
"
```

---

## 项目结构 / Project Structure

```
calorie-lookup/
├── SKILL.md                  # Skill 元数据 / Skill metadata
├── WORKFLOW.md               # 工作流说明 / Workflow description
├── HOOKS.md                  # Sub-agent 触发逻辑 / Sub-agent trigger logic
├── AGENTS.md                 # 开发者/Agent 指南 / Developer/Agent guide
├── agents/
│   ├── README.md             # Sub-agent 概览 / Sub-agent overview
│   └── calorie-lookup-decomposer.md  # Decomposer 合约 / Decomposer contract
├── scripts/
│   ├── __init__.py           # 模块导出 / Module exports
│   ├── core.py               # 主逻辑 / Main logic: lookup_meal / lookup_food
│   ├── config_example.py     # 配置模板 / Config template (tracked by git)
│   ├── parser.py             # 自然语言文本解析 / NL text parsing
│   ├── units.py              # 单位换算 / Unit conversion & portion defaults
│   ├── translate.py          # 中英食物名字典 / CN→EN dictionary (acceleration cache)
│   ├── usda_fdc.py           # USDA API 封装 / USDA API wrapper + error handling
│   └── cache.py              # SQLite 缓存 / SQLite cache
├── references/
│   └── usda_fdc.md           # USDA API 快速参考 / USDA API quick reference
├── pyproject.toml            # 项目元数据 / Project metadata
├── requirements.txt          # Python 依赖 / Python dependencies
└── LICENSE                   # MIT
```

---

## 架构 / Architecture

### 两条处理路径 / Two Processing Paths

**路径 A — 快速路径 / Path A — Fast Path**
纯英语简单食材 → `lookup_meal(text)` 直接处理。
Plain English simple ingredients → `lookup_meal(text)` directly.

**路径 B — 主路径 / Path B — Primary Path**
非英语/复合菜/套餐 → Decomposer Sub-agent（LLM 翻译 + 分解）→ 英文食材名 → `lookup_food()` 逐条查询 → 汇总。
Non-English / composite dishes / set meals → Decomposer Sub-agent (LLM translation + decomposition) → English ingredient names → `lookup_food()` per item → aggregate totals.

### 翻译策略 / Translation Strategy

- **主路径 / Primary**：LLM 翻译（通过 Decomposer Sub-agent）/ LLM translation (via Decomposer Sub-agent)
- **加速缓存 / Acceleration cache**：`scripts/translate.py` 内置 ~224 条中英字典 / ~224-entry CN→EN dictionary for known foods
- USDA API 仅支持英文查询，所有非英语输入最终都需转为英文 / USDA API only accepts English queries

### 数据流 / Data Flow

```
用户输入 / User Input
  → [Agent 判断路径 / Path Decision]
  → [解析/翻译 / Parse & Translate]
  → USDA API 查询 / Query
  → 营养计算 / Nutrition Calculation
  → 结构化输出 / Structured Output
  → SQLite 缓存 / Cache
```

---

## API

### `lookup_meal(text, meal_type="unknown")`

解析多食材文本，逐条查询并汇总。
Parses multi-ingredient text, queries each item, and aggregates totals.

```python
result = lookup_meal("chicken breast 200g + rice 1 bowl")
# {
#   "type": "meal_nutrition",
#   "items": [...],
#   "totals": {"kcal": ..., "protein_g": ..., "carb_g": ..., "fat_g": ..., "fiber_g": ...},
#   "questions": [...]
# }
```

### `lookup_food(name, qty, unit)`

查询单个食材的营养信息。
Queries nutrition info for a single ingredient.

```python
result = lookup_food("chicken breast", 200, "g")
# {"ok": True, "kcal": 330.0, "protein_g": 62.0, ...}
```

---

## 环境变量 / Environment Variables

| 变量 / Variable | 必需 / Required | 说明 / Description |
|------|------|------|
| `USDA_FDC_API_KEY` | 是 / Yes | USDA FoodData Central API Key |
| `CALORIE_SKILL_CACHE_DB` | 否 / No | SQLite 缓存路径 / Cache DB path（默认 / default: `calorie_skill_cache.sqlite3`）|

---

## License

MIT
