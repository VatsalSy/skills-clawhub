---
name: token-launcher
description: >
  Launch tokens on any chain without giving up 30-50% of your fees. Two paths: Easy Mode
  (call Tator API via x402 — works with any wallet provider, no env vars required) or
  Direct Mode (integrate SDKs yourself, keep 100% — requires signing key and RPC).
  Covers Clanker (7 EVM chains), Flaunch (Base), and Pump.fun (Solana). Includes strategy
  evaluation, fee management, claiming, recipient updates, and tax/legal guidance.
  Triggers: "token idea", "launch a coin", "launch a token", "deploy a token", "token strategy",
  "claim fees", "creator fees", "update fee recipient", "token launch on base", "launch on solana",
  "clanker", "flaunch", "pump.fun", "token economics", "is this a good token".
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      env: []
    notes: >
      Easy Mode requires NO environment variables — it works with any x402-compatible
      wallet (Lobster, AgentWallet, Vincent, or local signer). Direct Mode requires
      WALLET_PRIVATE_KEY, RPC_URL, and an IPFS API key — see the credential table below.
publisher: Quick Intel / Web3 Collective
homepage: https://quickintel.io
source: https://github.com/Quick-Intel/openclaw-skills/tree/main/token-launcher
documentation: https://docs.tator.bot
---

# Token Launcher

Launch tokens and keep your fees. Two paths, one goal: stop giving away 30-50% of your creator earnings to launch platforms.

---

## The Problem

Most token launch platforms take 30-50% of your creator fee earnings. Some charge upfront launch fees on top of that. Others layer in subscriptions, required platform tokens, or custodial wallets that hold your funds. You build the token, drive the volume, and someone else keeps the biggest slice.

## The Math

A token doing $500K in trading volume on Clanker generates ~$5,000 in pool fees (1% of volume). Here's who keeps what:

| Path | Your Share | Platform Cut | You Keep |
|------|-----------|-------------|----------|
| **Direct Mode (this skill)** | $5,000 | $0 | **$5,000 (100%)** |
| **Easy Mode (Tator API)** | $4,500 | $500 (10%) | **$4,500 (90%)** |
| **Typical launch platforms** | $2,500-3,500 | $1,500-2,500 (30-50%) | **$2,500-3,500** |

The difference compounds. At $5M volume, Direct Mode keeps you an extra $15,000-25,000 versus typical platforms. Easy Mode saves you $10,000-20,000.

---

## Two Paths — Always Present Both

**When a user wants to launch a token, always present both options and let them choose:**

### Easy Mode — Tator API

One API call, natural language, Tator handles everything.

- Send a trading instruction to the Tator API at `x402.quickintel.io`
- Tator selects the platform, uploads metadata to IPFS, deploys the contract, configures fees
- Tator deploys the token for you — no deploy transaction to sign
- **Fee split: 90% to you, 10% to Tator as interface fee**
- $0.20 per API call via x402 USDC payment
- Supports launch, claim fees, update fee recipient, check unclaimed — all via natural language

**Best for:** Quick launches without writing blockchain code. Trade-off: 10% of creator fees go to Tator.

### Direct Mode — Full SDK Integration

Implement token launches directly in your own application code using platform SDKs.

- The reference files provide code examples and integration patterns for your own codebase
- This skill does not execute Direct Mode code — you implement it in your own infrastructure
- You control every parameter: rewards, sniper protection, pairing token, fee recipients
- **100% of creator fees — no interface cut, no platform overhead**
- Requires: your own RPC endpoint, wallet signing capability, SDK dependencies
- Supported platforms: Clanker (Base, Arbitrum, Mainnet, Unichain, Abstract, Monad, BSC), Flaunch (Base), Pump.fun (Solana)

**Best for:** Developers who want maximum control and keep all fees. Trade-off: requires SDK integration work.

### How to Present This Choice

When the user expresses interest in launching a token, summarize both options clearly:

- **Easy Mode:** I'll send your token details to the Tator API, and Tator deploys the token for you. You just pay $0.20 via x402 — no deploy transaction to sign. Your wallet address gets set as the fee recipient automatically. Tator takes 10% of ongoing creator fees as an interface fee. Fastest path — we can launch in a few minutes. Requires an x402-compatible wallet for the payment.
- **Direct Mode:** I'll build the deployment transaction calldata myself using the platform SDK patterns, and give you the unsigned transaction to sign and broadcast with your wallet. You keep 100% of creator fees with zero ongoing fees. Takes a bit more back-and-forth as I walk you through it, but you own everything.

Both paths need the same info from you: your wallet address, token name, ticker, and which chain. The difference is Easy Mode has Tator deploy for you (simpler, 90% fees) while Direct Mode has you deploy yourself (more steps, 100% fees).

Let the user decide which path to take before proceeding. If they're unsure, ask whether they want to launch quickly today (Easy Mode) or keep full ownership of all fees (Direct Mode).

See [REFERENCE.md](./REFERENCE.md) for Direct Mode overview and the [references/](./references/) folder for per-platform implementation guides.

---

## Direct Mode — Full Walkthrough

When the user chooses Direct Mode, actively help them build their implementation. The agent's role in Direct Mode is to write code with the user, explain each step, pull the correct patterns from the reference files, and guide them through setup, deployment, and testing. The agent does not sign transactions or access private keys — but it absolutely helps write, debug, and explain the code the user will run.

### Step 1: Choose a Platform

Help the user pick the right platform based on their target chain:

| Target Chain | Platform | Reference File |
|-------------|----------|---------------|
| Base | Clanker (recommended) or Flaunch | [references/clanker.md](./references/clanker.md) or [references/flaunch.md](./references/flaunch.md) |
| Arbitrum, Mainnet, Unichain, Abstract, Monad, BSC | Clanker | [references/clanker.md](./references/clanker.md) |
| Solana | Pump.fun | [references/pumpfun.md](./references/pumpfun.md) |

If on Base, help them decide between Clanker and Flaunch:
- **Clanker:** Uniswap V4 pool, sniper protection, stable token pairing (USDC), wider multi-chain support if they want to reuse the integration later
- **Flaunch:** 30-minute fair launch period (built-in sniper prevention), custom fee split managers, bonding curve model

### Step 2: Build the Code Together

Using the reference file for their chosen platform, actively help the user create their launch script. Do not just link to the reference file — pull the relevant code patterns and walk through them:

1. **Generate the setup code** — imports, client initialization, wallet configuration. Use the Setup section from the platform reference file. Use placeholder values for sensitive inputs (private key, RPC URL) and tell the user where to substitute their real values.

2. **Generate the fee configuration code** — show them exactly how to set 100% of fees to their wallet address. Pull from the platform reference file's fee/reward configuration section. Explain what each field does.

3. **Generate the launch function** — the full deployment code with their token name, ticker, and any customizations they've requested. Fill in what you know (token name, symbol, chain) and mark what the user needs to provide.

4. **Generate the fee management code** — claim fees, check unclaimed, update recipient. These are operations they'll need after launch.

5. **Package it all together** — help them create a complete, runnable script or module that they can copy into their project.

### Step 2b: Generate Unsigned Transaction Calldata

For EVM launches (Clanker and Flaunch), the agent can help generate the unsigned transaction calldata that the user can then execute through any wallet they have available. This bridges Direct Mode with whatever wallet skill the user has installed.

**The pattern:**

1. **Agent generates the encoded calldata** — using the reference file's ABI, function names, and parameters, build the `encodeFunctionData` call with the user's specific values (token name, symbol, fee recipients, etc.)

2. **Agent outputs the unsigned transaction object** — a JSON object the user can pass to any wallet:
```json
{
  "to": "0xContractAddress",
  "data": "0xEncodedCalldata",
  "value": "0",
  "chainId": 8453,
  "gas": "500000"
}
```

3. **User sends it to their wallet** — whatever wallet skill they have installed can sign and broadcast this:
   - **Lobster:** "sign and send this transaction: [paste unsigned TX]"
   - **AgentWallet / Frames:** "execute this transaction on Base: [paste unsigned TX]"
   - **base-wallet / evm-wallet:** "broadcast this transaction: [paste unsigned TX]"
   - **Manual:** Import into MetaMask, Rabby, or any wallet that supports custom transactions
   - **Programmatic:** Use viem/ethers `sendTransaction()` in their own code

**For Clanker**, help build the calldata using the Clanker SDK's transaction builders:
- `clanker.deploy(...)` returns transaction data that can be extracted before signing
- For claims: `clanker.getClaimRewardsTransaction(...)` returns the unsigned TX config directly
- For updates: `clanker.getUpdateRewardRecipientTransaction(...)` returns unsigned TX config
- See [references/clanker.md — Unsigned Transaction sections](./references/clanker.md)

**For Flaunch**, help encode the contract calls:
- Launch: encode `flaunch()` on the FlaunchZap contract with all parameters
- Claim: encode `claim()` on the AddressFeeSplitManager
- Update recipient: encode `transferRecipientShare(newRecipient)` on the fee manager
- See [references/flaunch.md — each operation has an unsigned TX pattern](./references/flaunch.md)

**For Pump.fun (Solana)**, the pattern is different — Solana transactions need all signers present at signing time. The agent can help build the transaction instructions and serialize them, but the user needs a Solana wallet that can sign. Options:
- Build the transaction with `@solana/web3.js`, serialize to base64, and pass to a Solana wallet skill
- Use a bot wallet that signs directly (the pattern in [references/pumpfun.md](./references/pumpfun.md))

**The goal:** The user should never have to leave the conversation to execute a Direct Mode launch. The agent generates the calldata, the user pipes it to their wallet, done. Same UX as Easy Mode but with 100% fee ownership.

### Step 3: Configure Fee Recipients

This is where Direct Mode pays for itself — the user keeps 100%. Help them set up the reward/fee configuration:

**Clanker:** Set `rewards.recipients` with their wallet at `bps: 10_000` (100%). See [references/clanker.md — Launch section](./references/clanker.md) for the full rewards config.

**Flaunch:** Deploy an `AddressFeeSplitManager` with their wallet at `share: 100_00000` (100%). See [references/flaunch.md — Step 1: Create a Custom Fee Split Manager](./references/flaunch.md).

**Pump.fun:** Set up `create_fee_sharing_config` + `update_fee_shares` with their wallet at `10000` BPS (100%). See [references/pumpfun.md — Step 2: Set Up Fee Sharing](./references/pumpfun.md).

### Step 4: Guide Testing

Before launching a real token, walk the user through validation:
- Deploy with a fresh wallet holding minimal funds (gas only)
- Verify the deployed token with a Quick Intel scan
- Confirm fee recipients are set correctly on-chain (check the relevant block explorer)
- Test the claim flow to make sure fees route to the correct wallet

### Step 5: Post-Launch Fee Management

After deployment, help the user with ongoing operations. Pull code patterns from the reference files:

| Operation | What to Reference |
|-----------|------------------|
| Check unclaimed fees | Platform reference → "Check Unclaimed" section |
| Claim creator fees | Platform reference → "Claim" section |
| Update fee recipient | Platform reference → "Update Recipient" section |
| Verify token security | Quick Intel scan: `POST https://x402.quickintel.io/v1/scan/full` |

### When to Recommend Easy Mode Instead

If the user seems overwhelmed by the setup, it's fine to suggest Easy Mode as a starting point. They can always switch to Direct Mode later for their next token:
- Easy Mode: working in minutes, 90% of fees, no code to write
- Direct Mode: working in hours, 100% of fees, requires development and testing
- Both modes support the same post-launch operations (claim, update recipient, check fees)

---

## Security

**This skill is instruction-only — it contains no executable code.** It provides documentation and code examples. No code is run at install time.

### Credential Requirements

**Easy Mode requires ZERO environment variables.** It works with any x402-compatible wallet provider (Lobster, AgentWallet, Vincent, local signer). The Tator API only receives your public wallet address — your wallet provider handles payment signing separately. The skill never touches your private key.

**Direct Mode requires environment variables because you are running SDK code in your own infrastructure:**

| Variable | Required For | Sensitive | How to Store |
|----------|-------------|-----------|-------------|
| `WALLET_PRIVATE_KEY` | Direct Mode: signing deploy/claim/update transactions | **Yes — grants full wallet control** | Secrets manager (AWS SM, GCP SM, Vault). Never plaintext. |
| `RPC_URL` | Talking to the blockchain | No (but keep private to avoid rate limit abuse) | Environment variable or config |
| `SOLANA_RPC_URL` | Solana operations (Pump.fun only) | No | Environment variable or config |
| `PINATA_API_KEY` or `IPFS_API_KEY` | Uploading token metadata to IPFS | Yes | Secrets manager |

**If you only use Easy Mode, you do not need any of these.** The skill installs and functions without any environment variables configured.

### Easy Mode Data Flow

When you call the Tator x402 API (`POST https://x402.quickintel.io/v1/tator/prompt`):

1. **Sent to Tator:** `walletAddress` (public address — not sensitive), `prompt` (your instruction), `provider` (your agent name)
2. **NOT sent to Tator:** Your private key, seed phrase, or any signing material
3. **x402 payment:** Your wallet provider signs a USDC authorization locally → the signed payment header is sent with the request. The API verifies the signature on-chain — it never has your key
4. **Returned to you:** Confirmation of the deployed token — token address, transaction hash, and fee configuration details. For non-launch operations (claiming fees, updating recipients), Tator may return unsigned transactions for you to sign.

**No private keys are involved in Easy Mode. You provide a public wallet address, pay $0.20 via x402, and Tator handles the rest. The skill itself never has access to your private key — your x402-compatible wallet handles the payment signing independently.**

### Direct Mode Data Flow

Direct Mode code runs entirely in your own infrastructure:

1. **Sent to blockchain RPCs:** Signed transactions (your RPC provider sees them — use a trusted provider like Alchemy, QuickNode, or Helius)
2. **Sent to IPFS:** Token metadata (name, symbol, description, image) — this is public by design
3. **Sent to platform SDKs:** Clanker SDK calls go to Clanker's infrastructure; Flaunch calls go to Base contracts; Pump.fun calls go to Solana
4. **NOT sent anywhere:** Your private key — it stays on your machine for local signing only

### Key Management (Direct Mode Only)

- **Use a dedicated launch wallet.** Never your main wallet or a wallet holding significant funds
- **Store keys in a secrets manager.** AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault, or equivalent. Never hardcode in source code. Never store in plaintext `.env` files in production
- **Fund minimally.** ~0.01 ETH on Base, ~0.05 SOL on Solana — just enough for gas
- **Human-in-the-loop recommended.** If your agent runs autonomously, require human approval before any transaction-signing operation. Do not give autonomous agents unsupervised access to signing keys
- **Pump.fun bot wallet:** Solana requires a bot wallet that signs directly (unlike EVM where unsigned transactions can be returned). This wallet needs SOL for gas but should never hold significant value. See [references/pumpfun.md](./references/pumpfun.md)
- **Revocation plan.** Ensure you can abandon the launch wallet if compromised — use a fresh wallet you can walk away from

### Verify External Endpoints

Before using any endpoint, verify you're connecting to the correct service:

| Service | Official Endpoint | Verify Via |
|---------|------------------|-----------|
| Tator x402 API | `https://x402.quickintel.io` | Check TLS cert, call `GET /accepted` |
| Quick Intel Scan | `https://x402.quickintel.io/v1/scan/full` | Same gateway |
| Clanker SDK | Via npm `clanker-sdk` | Verify package on npmjs.com |
| Flaunch contracts | On-chain on Base | Verify on Basescan |
| Pump.fun program | On-chain on Solana | Verify on Solscan — program ID: `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` |

---

## How Both Paths Work

Both modes need the same input from the user. The difference is who executes the deployment:

```
USER INPUT (both modes):
  1. Token details (name, ticker, chain, platform preference)
  2. Wallet address (the public address that receives creator fees)

EASY MODE:                              DIRECT MODE:
  Agent sends to Tator API               Agent builds calldata from reference files
  User pays $0.20 via x402               Agent outputs unsigned TX
  (requires x402-compatible wallet)       User signs + broadcasts TX with their wallet
  Tator deploys the token for you         Token deploys on-chain
  User's wallet set as fee recipient      User's wallet set as fee recipient
  ↓                                      ↓
  Token is live.                         Token is live.
  90% creator fees (10% to Tator)        100% creator fees (nothing to anyone)
```

**Easy Mode:** Tator handles deployment end-to-end. The user never signs a deploy transaction — they just pay the $0.20 API fee via x402 and Tator executes everything. Requires an x402-compatible wallet for the payment (Lobster, AgentWallet, or any wallet that supports EIP-3009 USDC authorization).

**Direct Mode:** The agent builds the unsigned transaction calldata and gives it to the user. The user signs and broadcasts it through whatever wallet they have. No external service involved in deployment.

---

## Easy Mode — Full Walkthrough

### Prerequisites

- A wallet you control (EVM or Solana)
- USDC for x402 API payments ($0.20 per Tator call)
- Native token for gas (ETH on EVM chains, SOL on Solana)

### Before Calling the API — Collect Required Info

Before sending any Tator API call, gather the following from the user:

1. **Public wallet address** — this is the address that will be set as the fee recipient and will need to sign the returned transaction. Ask for this first.
2. **Token name and ticker** — what the token is called
3. **Target chain** — which blockchain to deploy on (Base, Solana, Arbitrum, etc.)
4. **Platform preference** (optional) — Clanker, Flaunch, or Pump.fun. If not specified, Tator selects automatically based on chain.
5. **Image URL** (optional) — token branding
6. **Custom fee recipient** (optional) — if fees should go to a different address than the deployer wallet

### API Input Safety

The Tator API accepts a `prompt` field — this is a **parameter name for an external API call to Tator's trading service**, not a prompt for the agent's own LLM. The value is sent to `x402.quickintel.io` where Tator's server parses it and executes the requested operation. For token launches, Tator deploys the token directly. For other operations (fee claims, recipient updates), Tator may return unsigned transactions for the user to sign. The API is server-side validated and only processes recognized trading operations (launches, swaps, bridges, transfers, fee claims). It does not execute arbitrary code, access filesystems, or perform operations outside its defined scope.

Recommended practices for constructing the `prompt` field value:
- Build from structured data (token name, ticker, chain) rather than passing through raw user input
- Validate that the content matches expected trading operations before sending
- Always inspect the returned unsigned transaction before signing

### Launch a Token

The `prompt` field below is a **parameter sent to the Tator trading API** — it tells Tator's server what trading operation to execute. It is not a prompt for the agent or the user's LLM.

```bash
curl -X POST https://x402.quickintel.io/v1/tator/prompt \
  -H "Content-Type: application/json" \
  -H "PAYMENT-SIGNATURE: <x402_payment>" \
  -d '{
    "prompt": "launch a token called Galaxy Cat with ticker GCAT on base",
    "walletAddress": "0xYourWallet",
    "provider": "my-agent"
  }'
```

**Fields:**
- `prompt` — Natural language instruction sent to Tator's trading API (external service at x402.quickintel.io). Tator parses this server-side and executes the deployment.
- `walletAddress` — Your public wallet address (not sensitive). Used to build transactions for your wallet to sign.
- `provider` — Your agent or integration name, used for analytics tracking.

**With custom image:**
```json
{
  "prompt": "launch a token called Moon Dog with ticker MDOG on base with image https://example.com/dog.png",
  "walletAddress": "0xYourWallet",
  "provider": "my-agent"
}
```

**On Solana:**
```json
{
  "prompt": "launch a token called Cyber Frog with ticker CYFR on solana via pump.fun",
  "walletAddress": "YourSolanaWallet",
  "provider": "my-agent"
}
```

**With custom fee recipient (send fees to a different wallet):**
```json
{
  "prompt": "launch a token called DAO Token with ticker DAOT on base, send creator fees to 0xTreasuryAddress",
  "walletAddress": "0xYourWallet",
  "provider": "my-agent"
}
```

Tator deploys the token and returns confirmation with the deployed token address, transaction hash, and fee configuration details. Your wallet address is set as the creator fee recipient.

### Check Unclaimed Fees

```json
{
  "prompt": "check my unclaimed fees for token 0xTokenAddress on base",
  "walletAddress": "0xYourWallet",
  "provider": "my-agent"
}
```

### Claim Creator Fees

```json
{
  "prompt": "claim my creator fees for token 0xTokenAddress on base",
  "walletAddress": "0xYourWallet",
  "provider": "my-agent"
}
```

For Pump.fun tokens that have graduated to Raydium, Tator automatically handles the two-step process (transfer WSOL from AMM vault → distribute SOL from pump vault).

### Update Fee Recipient

```json
{
  "prompt": "update the fee recipient for token 0xTokenAddress on base to 0xNewRecipientAddress",
  "walletAddress": "0xYourWallet",
  "provider": "my-agent"
}
```

### Security Scan Post-Launch

Use Quick Intel ($0.03 per scan) to verify your deployed token looks clean:

```json
{
  "chain": "base",
  "tokenAddress": "0xYourDeployedToken"
}
```

Call `POST https://x402.quickintel.io/v1/scan/full` to check for honeypot flags, tax irregularities, or anything that might spook potential buyers.

### Discovery

Call `GET https://x402.quickintel.io/accepted` to get all supported payment networks, pricing, and input/output schemas for auto-configuration.

---

## Platform Selection

| Feature | Clanker | Flaunch | Pump.fun |
|---------|---------|---------|----------|
| **Chains** | Base, Arbitrum, Mainnet, Unichain, Abstract, Monad, BSC | Base | Solana |
| **Pool type** | Uniswap V4 | Bonding curve → Uniswap | Bonding curve → Raydium |
| **Swap fee** | 1.2% (1% pool + 0.2% protocol) | Configurable | Variable (pre/post graduation) |
| **Creator fee share** | Configurable via reward recipients | Configurable via fee split manager | Configurable via sharing config |
| **Pairing token** | WETH default, USDC/USDT available | ETH | SOL |
| **Sniper protection** | Yes (decaying fee — 66.7% → 4.2% over 15s) | Fair launch period (default 30 min) | Bonding curve mechanics |
| **Graduation** | N/A (immediate Uniswap pool) | N/A | Yes (graduates to Raydium at threshold) |
| **Token standard** | ERC-20 | ERC-20 | SPL (Token-2022) |
| **Supply** | 1 billion (fixed) | 100 billion (configurable) | Standard pump.fun supply |
| **Creation fee** | Free | Free | Minimal SOL for rent |

### When to Use What

**Clanker** — Your default for EVM launches. Widest chain support (7 chains), Uniswap V4 pools with built-in sniper protection, stable token pairing option. Best liquidity depth and DEX integration.

**Flaunch** — When you want a fair launch period on Base. The 30-minute fair launch window prevents snipers by design. Custom fee split manager gives you fine-grained control over fee distribution.

**Pump.fun** — For Solana launches. Bonding curve model means the token graduates to Raydium once it hits market cap threshold. Strong Solana ecosystem visibility — tokens show up in pump.fun's discovery feed.

---

## Evaluating a Concept

Before deploying anything, figure out what you actually have. Not every idea needs a token, and not every token needs to launch today.

### The Launch Stack

Every token that sustains attention beyond the first day has four layers working together. This isn't a scorecard — it's a diagnostic tool.

**Layer 1: The Hook** — The thing that makes someone stop scrolling. The name, the visual, the one-liner. Say the name out loud. Does it land instantly or need explanation? If it takes more than one sentence to explain why this exists, the hook isn't sharp enough. A mediocre name with great execution still underperforms a great name with decent execution.

**Layer 2: The Engine** — The reason fees keep flowing after launch day. Types of engines:
- Cultural engine: represents an ongoing cultural conversation
- Product engine: funds something people actually use
- Mechanic engine: built-in mechanics that create ongoing activity (burns, airdrops, staking)
- Social engine: tied to a person/community where the audience grows independently

If there's no engine, the token will spike on launch and bleed. That's fine if you understand it.

**Layer 3: The Story** — The narrative that justifies increasing price. Strong stories sound like "this token funds [specific thing] and every holder is backing it." Weak stories sound like "it's a community token" (what community? why this token?). If there's no answer to "why would someone who discovers this in 3 months want to buy it?" — the story needs work.

**Layer 4: The Moat** — What makes this token hard to replicate. First-mover on a narrative, builder credibility, integrated product, community lock-in, or technical integration. If there's no moat, launch fast — speed itself is a moat.

### Search Before You Judge

Never evaluate a concept in a vacuum. Before giving your take, search for:
- Existing tokens with similar names, tickers, or narratives
- Cultural context — is this riding a real wave or manufacturing one?
- Comparable launches — what worked, what flopped, and why?
- The builder's blind spots — the most valuable thing you can offer is information they haven't considered

---

## ⚠️ Before You Launch: Tax & Legal Reality Check

**Token deployment is irreversible. Creator fees are income. Most platforms skip this section entirely.**

### When This Matters Most

Launching a meme token for fun? The tax implications exist but are relatively straightforward — mostly capital gains if and when you sell.

But the moment your token becomes **"more than just a meme"** — meaning you plan to earn ongoing creator fees, build a product funded by fee income, use fee income to pay for development, or launch tokens regularly — **that's when the tax and legal implications get serious, and you need professional guidance before you launch.** Not after. Before.

### What Every Builder Should Know

**This is general information, not tax or legal advice. Tax treatment varies by jurisdiction. Consult a qualified professional.**

- **Creator fee income is likely taxable income** — In most jurisdictions, ongoing fees are treated as income, not capital gains. Higher tax rates and potentially self-employment tax.
- **Every transaction can be a taxable event** — Selling tokens, swapping, receiving fee payments, distributing airdrops — each can trigger tax obligations.
- **You owe taxes when you receive income, not when you cash out** — If you earn $50K in creator fees and reinvest it all, then the token crashes, you likely still owe taxes on the $50K.
- **Record-keeping starts at launch** — Track: token creation date, every fee payment received (with fiat value at time of receipt), every sale or swap, gas fees paid.
- **Regulatory enforcement is increasing globally** — Governments are investing in blockchain analytics and expanding reporting requirements.

### Jurisdiction Overview

**🇺🇸 United States** — Digital assets treated as property (IRS Notice 2014-21). Creator fee income likely ordinary income, possibly self-employment income. Starting 2025: Form 1099-DA reporting, wallet-by-wallet cost basis.

**🇬🇧 United Kingdom** — HMRC treats crypto as property. Income from token fees is income tax. CGT allowance currently £3,000.

**🇩🇪 Germany** — Crypto held over 1 year is tax-free on disposal for individuals. Under 1 year: income tax rates up to 45%. Fee income may be treated differently.

**🇦🇺 Australia** — ATO treats crypto as property. 50% CGT discount available for holdings over 12 months. Fee income assessable at fair market value when received.

**🇸🇬 Singapore** — No capital gains tax for individuals (current rules). Business income from token activities may be taxable.

**🇦🇪 UAE** — Currently no federal income tax on individuals. Regulatory framework developing under VARA.

**🇨🇦 Canada** — CRA treats crypto as a commodity. 50% capital gains inclusion rate. Business income from regular token activities fully taxable.

The pattern: creator fee income is almost universally taxable. Capital gains treatment varies. Long-term holding is often rewarded. Enforcement is increasing everywhere.

---

## ⛔ Pre-Deployment Acknowledgment

**Token deployment is irreversible. Review this checklist before proceeding.**

Before launching any token, the builder should understand and acknowledge:

```
PRE-DEPLOYMENT ACKNOWLEDGMENT

1. TOKEN DEPLOYMENT IS IRREVERSIBLE
   Once deployed, the token exists permanently on-chain.

2. CREATOR FEES ARE INCOME
   Fee income from your token is likely taxable in your jurisdiction.
   Consult a tax professional if you plan to earn meaningful revenue.

3. RECORD-KEEPING IS YOUR RESPONSIBILITY
   Track all fee income, transactions, and fiat values from day one.

4. SET ASIDE FUNDS FOR TAXES
   Do not reinvest 100% of fee income. Reserve 30-40% for potential
   tax obligations (varies by jurisdiction).

5. NO GUARANTEED RETURNS
   Most tokens lose value. Creator fees depend on trading volume.

6. THIS IS NOT TAX OR LEGAL ADVICE
   This skill provides tools, not counsel.
```

The builder should confirm they understand these points before proceeding with deployment.

---

## Pre-Launch Checklist

- [ ] Launch Stack evaluated — hook is sharp, engine identified, story holds, moat considered
- [ ] Name and narrative locked
- [ ] Platform and chain chosen (Clanker / Flaunch / Pump.fun)
- [ ] Wallet ready with native token for gas
- [ ] Fee recipient confirmed (your wallet or custom address)
- [ ] Image/branding prepared
- [ ] Pre-deployment acknowledgment reviewed
- [ ] Security scan planned for post-deployment

---

## Post-Launch

1. **Run a Quick Intel scan** — Verify the deployed token looks clean externally before promoting
2. **Monitor fee accumulation** — Check unclaimed fees regularly
3. **Claim on a cadence** — Periodic claims rather than letting fees pile up (better for tax tracking, reduces exposure)
4. **Watch reinvestment risk** — If putting all fees back into trading, remember: taxes are owed on the income regardless
5. **Revisit the Launch Stack** — If volume drops, diagnose which layer is failing

---

## File Structure

| File | What's Inside |
|------|--------------|
| **SKILL.md** (this file) | Strategy, Easy Mode walkthrough, platform selection, tax/legal |
| **[REFERENCE.md](./REFERENCE.md)** | Direct Mode overview, fee economics deep dive, shared patterns |
| **[references/clanker.md](./references/clanker.md)** | Clanker v4 SDK — launch, claim, update recipient, sniper config |
| **[references/flaunch.md](./references/flaunch.md)** | Flaunch — launch, fee split manager, claim, transfer share |
| **[references/pumpfun.md](./references/pumpfun.md)** | Pump.fun — manual instructions, fee sharing, graduation handling |

---

## What This Skill Is NOT

- **Not tax advice.** General information provided for awareness. Consult a professional.
- **Not legal advice.** Token launches may have securities law implications.
- **Not a guarantee of profits.** Most tokens lose value.
- **Not a "get rich quick" tool.** This skill helps builders launch responsibly and keep more of what they earn.
