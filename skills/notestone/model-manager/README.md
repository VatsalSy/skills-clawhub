# OpenClaw Model Manager Skill 🛠️

**💰 Optimize Your API Costs: Route Simple Tasks to Cheaper Models.**

Why pay **$15/1M tokens** for simple translations or summaries when you can pay **$0.60/1M**? That's a **25x price difference (96% savings)** for suitable tasks.

Interact with OpenRouter API to fetch available models, compare pricing instantly, and configure OpenClaw to use the most cost-effective models via the `openrouter/auto` gateway.

---

### 🇨🇳 中文说明

**💰 拒绝冤枉钱！自动路由高性价比模型，最高节省 96% Token 费用。**

为什么要花 **$15/1M tokens** 的价格去处理简单的翻译或摘要任务？明明可以用 **$0.60/1M** 的模型搞定！

这个 Skill 能帮你：
1.  **即时比价**：列出当前 OpenRouter 上的模型价格（每百万 Token 输入/输出成本），一目了然。
2.  **智能配置**：自动将简单任务路由给高性价比的小模型（如 GPT-4o-mini, Haiku），复杂任务留给大模型。
3.  **🆕 任务模拟器 (Plan Mode)**：输入你想做的任务，模拟展示“金齿轮”如何拆解任务并分配给不同模型，直接算出能省多少钱。

### 📉 Cost Savings Logic (Per 1M Output Tokens)

| Model | Best For | Price | Savings Potential |
| :--- | :--- | :--- | :--- |
| **Claude 3.5 Sonnet** | Complex reasoning, coding | $15.00 | Baseline |
| **GPT-4o-mini** | Summaries, chat, extraction | **$0.60** | **96% Cheaper** |
| **Llama 3 70B** | General purpose, open source | **$0.90** | **94% Cheaper** |
| **Haiku 3** | Fast tasks, classification | **$1.25** | **91% Cheaper** |

**Features ✨**
- **Compare Prices**: See input/output costs per 1M tokens side-by-side.
- **Smart Routing**: Configure `openrouter/auto` to handle easier tasks with efficient models.
- **Stay Updated**: Always access the latest price drops and new models from OpenRouter.
- **Plan & Simulate**: Preview how a complex task is split into cheaper sub-tasks.

## Installation 📦

1. Clone this repository into your OpenClaw skills directory:
   ```bash
   cd ~/.openclaw/workspace/skills
   git clone https://github.com/Notestone/openclaw-model-manager.git model-manager
   ```

2. That's it! OpenClaw will detect the `SKILL.md`.

## Usage 🚀

In your OpenClaw chat:

**List Models:**
> "list models"
> "列出模型"

**Simulate Savings (NEW):**
> "plan build a python scraper"
> "规划 写一个爬虫"

**Enable a Model:**
> "enable 1"
> "启用 1" (where 1 is the index from the list)

**Manual Command:**
You can also run it from the terminal:
```bash
python3 skills/model-manager/manage_models.py list
python3 skills/model-manager/manage_models.py plan "your task"
```

## How it Works 🧠

1. **Fetches** `https://openrouter.ai/api/v1/models` (public API).
2. **Filters** for top-tier models and sorts by context length.
3. **Displays** a markdown table with pricing (input/output per 1M tokens).
4. **Patches** `~/.openclaw/openclaw.json` to add the selected model ID to `agents.defaults.models` and `fallbacks`.
5. **Simulates** task decomposition using a local heuristic planner to estimate savings.

## Requirements

- Python 3.6+ (uses standard library only, no pip install needed!)
- OpenClaw Gateway (local installation)

## License

MIT
