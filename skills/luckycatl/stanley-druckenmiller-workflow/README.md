# Stanley Druckenmiller Workflow

Thesis-driven market analysis skill for OpenClaw.

This skill is designed for Druckenmiller-inspired macro/equity thinking with a live PM memo voice:
- Liquidity and rates first
- Consensus vs variant explicitly separated
- D1/D2 (first derivative / second derivative) regime logic
- Evidence anchors and safety disclaimers

Current product framing:
- Goal: hand most repetitive monitoring work to the machine and leave the highest-value judgment to the human.
- V1 scope: US-led macro engine + China / A-share transmission layer.
- Honest limitation: the skill can help with first-layer macro judgment, not fully replace second-layer execution judgment.
- Core panels and source reference: `references/core-panels-and-sources.md`
- A-share tape design reference: `references/a-share-tape-v1_1.md`

## What This Skill Produces

Depending on trigger, it can generate:
- AM morning brief (thesis + validation)
- EOD wrap
- Weekly review
- Monthly regime review
- Pre-trade thesis collision check
- Asset divergence monitor

All outputs are narrative and decision-oriented (not raw JSON dumps).

## Folder Structure

```text
stanley-druckenmiller-workflow/
  SKILL.md
  README.md
  references/
    core-panels-and-sources.md
    a-share-tape-v1_1.md
  scripts/
    market_panels.py
```

## Data Source Fallback (updated)

`market_panels.py` now has two layers:

### Global / cross-asset layer
Per symbol, default order is:
1. finshare（默认 `first`）
2. Yahoo chart API
3. Stooq CSV
4. FRED proxy mapping
5. Local cache

### A-share structure layer
A-share internal structure now uses **AkShare** when available, mainly for:
- 北向资金
- Shibor / 中国国债收益率
- 融资融券
- 地产链 / 运输链 / 消费分层 / 信用风险代理篮子

### Runtime cache scope (security fix)
By default, `market_panels.py` now writes cache files only inside the skill directory:
- `stanley-druckenmiller-workflow/.runtime/market-snapshots/`

It no longer writes to a workspace-level `memory/` directory by default.

If you explicitly want a different runtime/cache directory, set:

```bash
export STANLEY_RUNTIME_DIR=/your/explicit/runtime/path
```

If unset, the script stays confined to the skill-local runtime folder.

### finshare 最小可用接入（可选）

默认模式是 `first`：
- 先走 finshare
- finshare 失败再回退到 Yahoo / Stooq / FRED / Cache
- 仍可用 `auto` 改回“Yahoo 优先、finshare 兜底”

#### 1) 安装依赖（可选）

```bash
pip install finshare akshare
```

#### 2) 启用/关闭方式

- CLI 参数（单次运行）

```bash
python3 scripts/market_panels.py --finshare-mode first
python3 scripts/market_panels.py --finshare-mode auto
python3 scripts/market_panels.py --finshare-mode off
```

- 环境变量（默认全局行为）

```bash
export FINSHARE_MODE=first  # 默认，优先走 finshare
export FINSHARE_MODE=auto   # Yahoo 优先，finshare 兜底
export FINSHARE_MODE=off    # 完全禁用 finshare
```

- FRED API Key（可选，增强宏观序列稳定性）

```bash
export FRED_API_KEY="<your_fred_api_key>"
```

> 当同时提供参数和环境变量时，以 `--finshare-mode` 为准。

#### 3) 回滚方式

出现兼容问题时，可直接回滚到“无 finshare”行为：

```bash
export FINSHARE_MODE=off
python3 scripts/market_panels.py --output /tmp/stanley-panels.json
```

这会恢复为：Yahoo → Stooq → FRED → Cache，不依赖 finshare。

## Core Design Principles

1. Public data only (no private-info claims)
2. No explicit trade orders (no entry, stop, target, size)
3. Probabilistic language over certainty
4. Facts and interpretation separated
5. Mandatory fields:
   - what_would_change_my_mind
   - data_timestamp (ISO8601)
6. If data is missing, downgrade safely (DATA LIMITED)

## Triggers and Modes

- Mode A (AM brief):
  - `晨报`
  - `macro update`
  - `stan分析下当前市场`
  - `今天怎么看`

- Mode B (EOD wrap):
  - `EOD`
  - `收盘复盘`
  - `今天盘面总结`

- Mode C (Weekly):
  - `周报`
  - `weekly review`
  - `下周怎么看`

- Mode D (Pre-trade consult):
  - `交易前看一眼`
  - `should I buy/sell`
  - `帮我做交易前 sanity check`

- Mode E (Monthly):
  - `月报`
  - `monthly review`
  - `regime review`

- Mode F (13F rationale):
  - `13F`
  - `why did he buy XLF`
  - `Q3 to Q4 holdings changes`

- Mode G (Asset divergence):
  - `盯住 [TICKER]`
  - `check divergence for [TICKER]`
  - `资产背离警报`

## Evidence and Safety Contract

- Include `Evidence anchors` section (top 6-12; Mode G: 3-5)
- Each anchor should include:
  - panel/metric
  - direction/change
  - lookback window
  - timestamp
  - source
- Missing evidence must be tagged:
  - `[EVIDENCE INSUFFICIENT: missing X]`

Safety footer (always append):
- Chinese: `免责声明：以上内容是研究框架信息，不构成投资建议或交易指令。`
- English: `Disclaimer: The above content is research framework information and does not constitute investment advice or trading instructions.`

## Local Validation Checklist (Before Publish)

1. `SKILL.md` frontmatter valid (`name`, `description`, metadata)
2. Trigger words route to expected mode
3. Output contains mandatory fields
4. DATA LIMITED behavior works when data is missing
5. No explicit trading instructions in output
6. Chinese and English depth parity is preserved

## Publish Checklist (ClawHub)

Do this only when you are ready to publish.

1. Login:

```bash
clawhub login
clawhub whoami
```

2. Optional dry run checks:

```bash
clawhub list
```

3. Publish command template:

```bash
clawhub publish ./skills/stanley-druckenmiller-workflow \
  --slug stanley-druckenmiller-workflow \
  --name "Stanley Druckenmiller Workflow" \
  --version 1.0.0 \
  --changelog "Initial public release: thesis-driven macro workflow with A-G modes, evidence protocol, and safe downgrade behavior."
```

4. Verify result:

- Confirm package page on ClawHub
- Install from a clean env and run one trigger from Mode A and one from Mode G

## Versioning Suggestion

- Start: `1.0.0`
- Behavior changes in output contract: bump minor (`1.1.0`)
- Trigger or schema breaking changes: bump major (`2.0.0`)

## Global Macro Expansion (v2 in progress)

The skill now includes global proxy panels in `scripts/market_panels.py`:
- Global equities: FEZ, EWJ, FXI, EWH, EEM, VGK
- Global FX: EURUSD=X, USDJPY=X, USDCNH=X
- Global rates proxies: BNDX, BWX, EMB

Mode A output contract is updated to include a Regional Scoreboard (US / Europe / Asia) and explicit cross-region coverage checks.

## Notes

- This skill is Druckenmiller-inspired and should never claim direct affiliation.
- Keep style high-conviction but evidence-auditable.
