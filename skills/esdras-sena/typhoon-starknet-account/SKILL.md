---
name: typhoon-starknet-account
description: Create a Starknet account to your agent through Typhoon anonymous deployer and interact with Starknet contracts (read/write + preflight).
---

# typhoon-starknet-account

This skill provides **agent-facing scripts** for:
- Creating/loading a Starknet account (Typhoon flow)
- Discovering ABI / functions
- Reading & writing to contracts
- Preflight (simulate + fee estimate)
- Allowance checks with human amounts

## CRITICAL: Account Creation Flow

When the user asks to create a Starknet account (in any form like "create an account", "create a Starknet account for my agent", "I need a wallet", etc.), **ALWAYS follow this flow**:

### Step 1: Check if account already exists

```bash
node ~/Documents/typhoon-starknet-account/scripts/check-account.js
```

**If `hasAccount: false`:**
- Proceed to Step 2

### Step 2: Provide funding instructions

Tell the user:

---

**To create your Starknet account, you need to fund it through Typhoon:**

1. Go to the Typhoon website: https://www.typhoon-finance.com/app
2. Make a deposit and download your deposit note
   - **Recommended:** Make a STRK deposit (this will be used to deploy and fund your agent account)
3. Copy **all the content** of your downloaded note file and paste it here

---

Then **wait for the user to paste the note content**.

### Step 3: Create the account

Once the user pastes the note JSON, run:

```bash
node ~/Documents/typhoon-starknet-account/scripts/create-account.js '<paste the note JSON here>'
```

The note format is:
```json
{
  "secret": "0x...",
  "nullifier": "0x...",
  "txHash": "0x...",
  "pool": "0x...",
  "day": "0x..."
}
```

### Step 4: Confirm success

After successful creation, show the user:
- Their new account address
- Explorer link (Voyager/Starkscan)
- Remind them the private key is stored securely

---

## Show Account Address

When user asks "what's my address", "show my wallet", "my account address", etc.:

```bash
node ~/Documents/typhoon-starknet-account/scripts/show-address.js
```

If multiple accounts exist, it returns all. Pass index to get specific one:
```bash
node ~/Documents/typhoon-starknet-account/scripts/show-address.js 0
```

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `check-account.js` | Check if account(s) exist |
| `show-address.js` | Show account address(es) |
| `load-account.js` | Load an existing local account artifact |
| `create-account.js` | Create + deploy a new account via Typhoon |
| `get-abi.js` | Fetch ABI summary + list functions (+ optional candidate ranking) |
| `call-contract.js` | Call a view function |
| `invoke-contract.js` | Call an external function |
| `check-allowance.js` | Check ERC20 allowance (supports human amount) |
| `multicall.js` | Execute multiple calls in one tx |
| `estimate-fee.js` | Preflight fee estimate for a call/multicall |
| `simulate.js` | Preflight simulate for a call/multicall |
| `token-info.js` | Token metadata (decodes felt short strings) |
| `decode-felt.js` | Decode felt short strings |

---
, "argent"
## Core Agent Workflow (no hardcoding)

### 1) Address & docs discovery (agent planning)
If the user mentions protocols/tokens/apps (e.g. "Ekubo", "STRK", "ETH"), the **agent must first search** for:
- The relevant contract addresses
- The protocol documentation

**Research constraint:** all agent research must be done through **MCP** (Model Context Protocol) — no interactive browser/UI. Use machine-readable sources (APIs, docs URLs, GitHub raw files) via agent fetch tools.

This skill does **not** do web search by itself; it provides the onchain tooling once addresses are known.

### 2) Load account
```bash
node ~/Documents/typhoon-starknet-account/scripts/load-account.js
```

### 3) ABI discovery (+ optional ranking)
```bash
node ~/Documents/typhoon-starknet-account/scripts/get-abi.js '{"contractAddress":"0x..."}'
```

If you want the script to return **ranked candidates** (to help the agent decide), pass a `query`:
```bash
node ~/Documents/typhoon-starknet-account/scripts/get-abi.js '{"contractAddress":"0x...","query":"swap exact tokens for tokens"}'
```

### 4) Read
```bash
node ~/Documents/typhoon-starknet-account/scripts/call-contract.js '{"contractAddress":"0x...","method":"<view_fn>","args":[...]}'
```

Optional: decode felt short strings:
```bash
node ~/Documents/typhoon-starknet-account/scripts/call-contract.js '{"contractAddress":"0x...","method":"symbol","args":[],"decodeShortStrings":true}'
```

### 5) Allowance check (raw or human)
Raw base units:
```bash
node ~/Documents/typhoon-starknet-account/scripts/check-allowance.js '{"tokenAddress":"0x...","ownerAddress":"0x...","spenderAddress":"0x...","requiredAmount":"20000000000000000000"}'
```
Human amount (script fetches decimals):
```bash
node ~/Documents/typhoon-starknet-account/scripts/check-allowance.js '{"tokenAddress":"0x...","ownerAddress":"0x...","spenderAddress":"0x...","requiredAmountHuman":"20"}'
```

### 6) Preflight (recommended)
Fee estimate:
```bash
node ~/Documents/typhoon-starknet-account/scripts/estimate-fee.js '{"privateKeyPath":"...","accountAddress":"0x...","calls":[{"contractAddress":"0x...","method":"...","args":[...]}]}'
```
Simulation:
```bash
node ~/Documents/typhoon-starknet-account/scripts/simulate.js '{"privateKeyPath":"...","accountAddress":"0x...","calls":[{"contractAddress":"0x...","method":"...","args":[...]}]}'
```

### 7) Execute
Single write:
```bash
node ~/Documents/typhoon-starknet-account/scripts/invoke-contract.js '{"privateKeyPath":"...","accountAddress":"0x...","contractAddress":"0x...","method":"...","args":[...]}'
```

Approve + action in one tx:
```bash
node ~/Documents/typhoon-starknet-account/scripts/multicall.js '{"privateKeyPath":"...","accountAddress":"0x...","calls":[{"contractAddress":"0x...","method":"approve","args":["0xspender","123"]},{"contractAddress":"0x...","method":"...","args":[...]}]}'
```

## Setup
```bash
cd ~/Documents/typhoon-starknet-account/scripts && npm install
```
