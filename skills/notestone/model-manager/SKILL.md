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

---

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

## Commands

- `list models` or `ls models` or `列出模型`: Fetch and display top models from OpenRouter with pricing comparisons.
- `enable <model_id>` or `启用 <model_id>`: Add a model to OpenClaw's configuration (agents.defaults.models & fallbacks).
- `plan <task>` or `规划 <task>`: **[NEW]** Simulate task decomposition and calculate potential savings.
  - Example: `plan "build a python stock scraper"`

## Implementation Details

This skill uses a Python script `manage_models.py` to:
1. Fetch `https://openrouter.ai/api/v1/models` (public API, no key needed).
2. Filter and rank models (e.g., sort by context length, pricing, or popularity).
3. Generate `config.patch` commands for OpenClaw.
4. **TaskPlanner**: A local heuristic engine that simulates multi-agent routing logic.

## Usage Example

**1. Check Prices:**
User: "list models"
Agent: (Runs script, displays table)
| ID | Name | Context | Price |
| :--- | :--- | :--- | :--- |
| 1 | `anthropic/claude-3.5-sonnet` | 200k | $3/$15 |
...

**2. Simulate Savings:**
User: "plan build a web scraper"
Agent: (Runs planner)
| Phase | Model | Price | Why? |
| :--- | :--- | :--- | :--- |
| Design | Claude 3.5 Sonnet | $15.00 | Complex logic |
| Code | GPT-4o-mini | $0.60 | Bulk generation |
| Review | Llama 3 (Local) | $0.00 | Privacy check |
**TOTAL SAVINGS: 65.3%** 💸

**3. Enable Model:**
User: "enable 1"
Agent: (Runs config patch) "Model enabled! You can now use it in tasks."
