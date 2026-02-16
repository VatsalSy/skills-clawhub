---
name: solana-connect
description: OpenClaw Solana Connect — A toolkit for OpenClaw agents to interact with the Solana blockchain. Connect wallets, send transactions, check balances, manage tokens, and build Solana-powered autonomous agents. Perfect for OpenClaw users who want their AI agents to interact with Solana natively.
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "env": ["SOLANA_RPC_URL"],
          },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "@solana/web3.js",
              "label": "Install Solana web3.js",
            },
            {
              "id": "npm",
              "kind": "npm", 
              "package": "@solana/spl-token",
              "label": "Install SPL Token library",
            },
          ],
      },
  }
---

# 🔗 OpenClaw Solana Connect

> The missing link between OpenClaw agents and Solana blockchain

**Built for OpenClaw** — A purpose-built toolkit that enables autonomous AI agents running on OpenClaw to interact seamlessly with the Solana blockchain.

---

## ⚠️ Security Warning

This toolkit handles private keys and can send real cryptocurrency transactions. Please read these security guidelines carefully.

### Always Use Testnet First

```bash
# Set testnet RPC for development
export SOLANA_RPC_URL=https://api.testnet.solana.com

# Only switch to mainnet after thorough testing
export SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
```

### Best Practices

1. **Use a Dedicated Wallet** — Never use your main wallet. Create a separate wallet with limited funds for agent trading.

2. **Set Spending Limits** — Configure maximum transaction amounts to prevent catastrophic losses.

3. **Enable Confirmations** — Always confirm large transactions with the human operator.

4. **Store Private Keys Securely** — Use environment variables, never hardcode private keys in code.

5. **Monitor Activity** — Regularly review transaction history and wallet balances.

### Recommended Configuration

```javascript
// Recommended: Use environment variables for sensitive data
const config = {
  rpcUrl: process.env.SOLANA_RPC_URL,
  // NEVER hardcode private keys in source code
  // Use: process.env.AGENT_PRIVATE_KEY instead
};
```

---

## Why OpenClaw Solana Connect?

Most Solana toolkits are designed for human developers to integrate into their apps. This toolkit is different:

- 🧠 **AI-First Design** — Built for autonomous agents, not developers
- 🔄 **OpenClaw Native** — Works out of the box with OpenClaw skills
- 🤖 **Agent-Friendly** — Natural language inputs, automatic validation
- 🛡️ **Secure by Default** — Sandboxed transactions, clear permissions

---

## Installation

```bash
# Install via ClawHub
clawhub install solana-connect

# Or clone manually
git clone https://github.com/Seenfinity/openclaw-solana-connect.git
```

### Configuration

Set your Solana RPC endpoint:

```bash
# For testing (RECOMMENDED FIRST)
export SOLANA_RPC_URL=https://api.testnet.solana.com

# For production (mainnet)
export SOLANA_RPC_URL=https://api.mainnet-beta.solana.com

# Or use Helius (free tier available)
export SOLANA_RPC_URL=https://api.mainnet.helius-rpc.com
```

---

## Testing

```bash
cd solana-connect
npm install
node test.js
```

All tests pass:
- ✅ Generate wallet
- ✅ Connect to Solana RPC
- ✅ Get balance
- ✅ Get token accounts
- ✅ Get transactions

---

## What Can It Do?

### Wallet Operations
- Generate new wallets (for agent use)
- Connect existing wallets (via private key or seed phrase)
- Check balances (SOL, tokens, NFTs)
- Get transaction history

### Transaction Operations
- Send SOL to any address
- Send SPL tokens
- Sign and verify messages
- Simulate transactions before sending

### Token Operations
- Get token balances
- Get NFT holdings
- Fetch token metadata
- Check if address is a token account

### Smart Contract / Program
- Fetch program accounts
- Get program data
- Decode transaction instructions

---

## Quick Start

```javascript
const { connectWallet, getBalance, sendSol } = require('./scripts/solana.js');

// Connect with a private key (base58)
const wallet = await connectWallet(privateKey);

// Check balance
const balance = await getBalance(walletAddress);

// Send SOL
const tx = await sendSol(fromWallet, toAddress, amountInSol);
```

---

## Example: Agent Trading on Solana

```javascript
// 1. Check portfolio balance
const balance = await getBalance(agentWallet);

// 2. Get token accounts
const tokens = await getTokenAccounts(agentWallet);

// 3. Execute trade (via DEX integration)
// const result = await swapToken(inputMint, outputMint, amount);
```

---

## Available Functions

### `connectWallet`

Connect to an existing wallet or generate a new one.

```javascript
const { connectWallet } = require('./scripts/solana.js');

// From private key (base58)
const wallet = await connectWallet('your-private-key-base58');

// Generate new wallet (returns { address, privateKey })
const newWallet = await connectWallet();
```

### `getBalance`

Get SOL and token balances for any address.

```javascript
const { getBalance } = require('./scripts/solana.js');

const balance = await getBalance('SolanaAddress');
// Returns: { sol: 12.5, tokens: [...], nfts: [...] }
```

### `sendSol`

Send SOL from one address to another.

```javascript
const { sendSol } = require('./scripts/solana.js');

const tx = await sendSol(fromWallet, toAddress, 1.0); // 1 SOL
```

### `getTokenAccounts`

Get all SPL tokens and NFTs for an address.

```javascript
const { getTokenAccounts } = require('./scripts/solana.js');

const tokens = await getTokenAccounts(walletAddress);
```

### `sendToken`

Send SPL tokens.

```javascript
const { sendToken } = require('./scripts/solana.js');

const tx = await sendToken(fromWallet, toAddress, tokenMint, amount);
```

---

## Use Cases

### 1. Autonomous Trading Agents
Build AI agents that autonomously trade on Solana DEXs based on market analysis.

### 2. NFT Floor Monitor
Create agents that monitor NFT collections and alert on price changes.

### 3. DeFi Yield Optimizer
Agents that find and execute yield farming opportunities across Solana protocols.

### 4. Wallet Manager
Manage multiple wallets, automate payments, track portfolios.

### 5. Analytics Dashboard
AI agents that analyze on-chain data and generate insights.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   OpenClaw Agent                    │
│                  (Your AI Agent)                    │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│           OpenClaw Solana Connect                   │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │   Wallet    │  │  Transaction │  │   Token   │  │
│  │  Manager    │  │   Handler    │  │  Manager  │  │
│  └─────────────┘  └──────────────┘  └───────────┘  │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│              @solana/web3.js                        │
│                  Solana RPC                         │
└─────────────────────────────────────────────────────┘
```

---

## Requirements

- OpenClaw agent
- Node.js 18+
- Solana RPC endpoint (Helius recommended)

---

## Roadmap

- [x] Basic wallet operations
- [x] Balance queries
- [ ] Token transfers
- [ ] NFT support
- [ ] DeFi integrations (Jupiter, Raydium)
- [ ] MCP server mode

---

## Resources

- 🌐 **GitHub**: [github.com/Seenfinity/openclaw-solana-connect](https://github.com/Seenfinity/openclaw-solana-connect)
- 📖 **Solana Docs**: [docs.solana.com](https://docs.solana.com)
- 🔧 **Helius RPC**: [helius.dev](https://helius.dev)
- 🛡️ **Solana Security**: [docs.solana.com/security](https://docs.solana.com/security)

---

## License

MIT © 2026 Seenfinity

---

*Built for OpenClaw agents. Powered by Solana.*
