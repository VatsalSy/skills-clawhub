import argparse
import json
import urllib.request
import urllib.error
import sys
import os

OPENROUTER_API = "https://openrouter.ai/api/v1/models"
CONFIG_FILE = os.path.expanduser("~/.openclaw/openclaw.json")

# --- Golden Gear Logic: Task Planner Simulation ---
class TaskPlanner:
    def __init__(self):
        # Pricing reference (approximate output price per 1M tokens)
        self.prices = {
            "tier1": {"id": "anthropic/claude-3.5-sonnet", "price": 15.00, "role": "Architect/Reasoning"},
            "tier2": {"id": "openai/gpt-4o-mini", "price": 0.60, "role": "Coder/Drafter"},
            "tier3": {"id": "local/llama-3", "price": 0.00, "role": "Reviewer/Privacy"},
        }

    def plan(self, task_description):
        """Simulate decomposing a task and routing it to optimal models."""
        
        # Simple heuristics for demo purposes
        task_lower = task_description.lower()
        
        if any(w in task_lower for w in ["code", "app", "script", "program", "debug"]):
            category = "Coding"
            steps = [
                {"phase": "1. System Design", "model": "tier1", "reason": "Requires complex logic & architecture"},
                {"phase": "2. Implementation", "model": "tier2", "reason": "High volume token generation (cost efficient)"},
                {"phase": "3. Security Review", "model": "tier3", "reason": "Zero-data-leakage privacy check"}
            ]
        elif any(w in task_lower for w in ["write", "blog", "post", "email", "summary"]):
            category = "Writing"
            steps = [
                {"phase": "1. Outline & Angle", "model": "tier1", "reason": "Creative direction & nuance"},
                {"phase": "2. Drafting", "model": "tier2", "reason": "Bulk text generation"},
                {"phase": "3. Proofreading", "model": "tier2", "reason": "Grammar & style check"}
            ]
        else:
            category = "General"
            steps = [
                {"phase": "1. Planning", "model": "tier1", "reason": "Strategy"},
                {"phase": "2. Execution", "model": "tier2", "reason": "Action"},
            ]

        # Calculate savings
        total_tokens_per_step = 1000 # Assumption
        
        # Scenario A: All SOTA (Tier 1)
        cost_baseline = len(steps) * (self.prices["tier1"]["price"] / 1_000_000) * total_tokens_per_step
        
        # Scenario B: Golden Gear Routing
        cost_optimized = 0
        for step in steps:
            model_key = step["model"]
            price = self.prices[model_key]["price"]
            cost_optimized += (price / 1_000_000) * total_tokens_per_step

        savings_pct = ((cost_baseline - cost_optimized) / cost_baseline) * 100

        # Output
        print(f"\n🧠 **Golden Gear Task Planner**")
        print(f"**Task:** \"{task_description}\"")
        print(f"**Category:** {category}\n")
        
        print("| Phase | Assigned Agent | Model | Price/1M | Why? |")
        print("| :--- | :--- | :--- | :--- | :--- |")
        
        for step in steps:
            m = self.prices[step["model"]]
            print(f"| {step['phase']} | {m['role']} | `{m['id']}` | ${m['price']:.2f} | {step['reason']} |")
            
        print(f"\n📉 **Financial Projection (per 1k runs):**")
        print(f"- Standard Cost (All Sonnet): **${cost_baseline * 1000:.2f}**")
        print(f"- Golden Gear Cost: **${cost_optimized * 1000:.2f}**")
        print(f"- **TOTAL SAVINGS:** **{savings_pct:.1f}%** 💸")
        print("\n*Simulation based on current OpenRouter pricing.*")

# --- Existing Functions ---

def fetch_models():
    """Fetch models from OpenRouter public API using standard library."""
    try:
        with urllib.request.urlopen(OPENROUTER_API, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('data', [])
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []

def filter_and_rank(models, limit=20):
    """Filter for popular/powerful models and rank them."""
    # Priority keywords for ranking
    priority_keywords = ["gpt-4o", "claude-3.5-sonnet", "o1-preview", "gemini-pro-1.5", "llama-3-70b", "deepseek-coder", "mistral-large", "qwen-2.5-72b"]
    
    ranked = []
    others = []
    
    for m in models:
        # Simple heuristic: prioritize models with specific keywords
        is_priority = any(k in m['id'] for k in priority_keywords)
        # Filter out very obscure or test models if needed
        if "test" in m['id'] or "beta" in m['id']: 
            if not is_priority: continue # Allow priority betas (e.g. o1-preview)
            
        if is_priority:
            ranked.append(m)
        else:
            others.append(m)
            
    # Sort priority models to top, then others by context length (descending)
    ranked.sort(key=lambda x: x['context_length'], reverse=True)
    others.sort(key=lambda x: x['context_length'], reverse=True)
    
    return (ranked + others)[:limit]

def display_models(models):
    """Print a markdown table of models."""
    print("| Index | ID | Context | Input Price ($/1M) | Output Price ($/1M) |")
    print("| :--- | :--- | :--- | :--- | :--- |")
    
    for idx, m in enumerate(models, 1):
        # Pricing is per token string, convert to float per 1M
        try:
            in_price = float(m['pricing']['prompt']) * 1_000_000
            out_price = float(m['pricing']['completion']) * 1_000_000
        except (ValueError, KeyError):
            in_price = 0.0
            out_price = 0.0
        
        name = m['id']
        print(f"| {idx} | `{m['id']}` | {m['context_length']//1000}k | ${in_price:.2f} | ${out_price:.2f} |")
        
    print("\nTo enable a model, use: `python3 skills/model-manager/manage_models.py enable <Index>`")

def enable_model(model_id, config_path):
    """Generate OpenClaw config patch to enable a model."""
    # Read current config to avoid overwriting existing
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Config file not found: {config_path}")
        return

    # Prepare patch data
    or_id = f"openrouter/{model_id}" if not model_id.startswith("openrouter/") else model_id
    
    try:
        current_fallbacks = config['agents']['defaults']['model']['fallbacks']
    except KeyError:
        current_fallbacks = []
    
    new_fallbacks = list(current_fallbacks)
    if or_id not in new_fallbacks: new_fallbacks.append(or_id)
    
    # Construct the minimal patch object
    patch = {
        "agents": {
            "defaults": {
                "models": {
                    or_id: {}
                },
                "model": {
                    "fallbacks": new_fallbacks
                }
            }
        }
    }
    
    print(json.dumps(patch))

def main():
    if len(sys.argv) < 2:
        print("Usage: manage_models.py <list|enable|plan> [target/task]")
        return

    action = sys.argv[1]
    
    if action == "plan":
        if len(sys.argv) < 3:
            print("Error: Please provide a task description. e.g., 'plan \"build a website\"'")
            return
        task = " ".join(sys.argv[2:])
        planner = TaskPlanner()
        planner.plan(task)
        return

    # For list/enable, fetch models first
    models = fetch_models()
    if not models:
        return

    sorted_models = filter_and_rank(models)

    if action == "list":
        display_models(sorted_models)
        
    elif action == "enable":
        if len(sys.argv) < 3:
            print("Error: Please specify a model index to enable.")
            return
            
        target = sys.argv[2]
        selected_model_id = None
        
        if target.isdigit():
            idx = int(target) - 1
            if 0 <= idx < len(sorted_models):
                selected_model_id = sorted_models[idx]['id']
        else:
            for m in models:
                if m['id'] == target:
                    selected_model_id = m['id']
                    break
        
        if selected_model_id:
            enable_model(selected_model_id, CONFIG_FILE)
        else:
            print(f"Error: Model '{target}' not found.")

if __name__ == "__main__":
    main()
