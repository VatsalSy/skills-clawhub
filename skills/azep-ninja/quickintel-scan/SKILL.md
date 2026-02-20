---
name: quickintel-scan
description: "Scan any token for security risks, honeypots, and scams using Quick Intel's contract analysis API. Use when: checking if a token is safe to buy, detecting honeypots, analyzing contract ownership and permissions, finding hidden mint/blacklist functions, or evaluating token risk before trading. Triggers: 'is this token safe', 'scan token', 'check for honeypot', 'audit contract', 'rug pull check', 'token security', 'safe to buy', 'scam check'. Supports 63 chains including Base, Ethereum, Solana, Sui, Tron. Costs $0.03 USDC per scan via x402 payment protocol. Works with any x402-compatible wallet."
---

# Quick Intel Token Security Scanner

## What You Probably Got Wrong

**This is NOT a free API.** Quick Intel uses the x402 payment protocol — you pay $0.03 USDC per scan, no API keys, no subscriptions. Your wallet signs a payment authorization, and the scan executes.

**x402 is not complicated.** You call the endpoint → get a 402 response with payment requirements → sign a payment → retry with the payment header → get your scan results. Most wallet libraries handle this automatically.

**63 chains supported.** Not just EVM — Solana, Sui, Radix, Tron, and Injective are supported too. If you're checking a token, Quick Intel probably supports that chain.

---

## Security Model

**Quick Intel is a read-only scanning service.** Understanding the trust boundaries:

### What Quick Intel CAN do
- Analyze token contracts for security risks, honeypots, and scam patterns
- Return detailed audit data (ownership, permissions, tax rates, liquidity status)
- Charge $0.03 USDC via x402 for the scan computation

### What Quick Intel CANNOT do
- Access your private keys (they never leave your wallet)
- Execute any transactions on your behalf
- Move, approve, or interact with your tokens in any way
- Modify any contracts or on-chain state

### What YOU must do
- **NEVER paste private keys, seed phrases, or wallet credentials into any prompt or API call.** Quick Intel only needs the token's contract address and chain — it does not need YOUR wallet address.
- **Treat scan results as one data point, not a guarantee.** A clean scan does not mean a token is safe forever — ownership can change, code can be upgraded via proxies, and liquidity can be pulled after your scan.
- **Cross-reference with other sources.** For high-value decisions, verify scan results against block explorer data, DEX aggregator liquidity checks, and community sentiment.

### Trust Boundary

```
┌─────────────────────────────────────────────────────┐
│  YOUR SIDE (you control)                            │
│                                                     │
│  • Private keys (never shared)                      │
│  • Payment authorization (EIP-3009 for $0.03 USDC)  │
│  • Decision to trade based on scan results           │
│                                                     │
├─────────────────────────────────────────────────────┤
│  QUICK INTEL'S SIDE (external service)              │
│                                                     │
│  • Receives: token address + chain name              │
│  • Analyzes: contract bytecode, on-chain state       │
│  • Returns: read-only security audit data            │
│  • Charges: $0.03 USDC via x402 payment              │
│                                                     │
│  Quick Intel NEVER receives your private key.        │
│  Quick Intel NEVER interacts with your tokens.       │
│  Quick Intel is READ-ONLY — no transactions,         │
│  no approvals, no state changes.                     │
└─────────────────────────────────────────────────────┘
```

### Who Operates This

Quick Intel's endpoint (`x402.quickintel.io`) is operated by **Quick Intel LLC**, a registered US based cryptocurrency security company. The same scanning infrastructure:

- Processes **over 50 million token scans** across 40+ blockchain networks
- Provides security scanning APIs to **DexTools**, **DexScreener**, and **Tator Trader**
- Has been operational since April 2023
- More information: [quickintel.io](https://quickintel.io)

### Verifying Scan Results

Scan results are based on automated contract analysis. For additional confidence, especially before large trades:

1. **Check the contract on a block explorer** — Look up the token on [BaseScan](https://basescan.org), [Etherscan](https://etherscan.io), [Solscan](https://solscan.io), etc. Verify that the contract is verified and the source code matches expectations.
2. **Confirm liquidity independently** — If `liquidity: false`, check a DEX aggregator (1inch, Jupiter, Odos) directly. The scanner may miss non-standard pairs.
3. **Review holder distribution** — A token where one wallet holds 90%+ of supply is risky regardless of what the contract code shows.
4. **Check token age and activity** — Recently deployed contracts with no transaction history carry higher risk.
5. **Re-scan periodically** — Contract ownership, fee structures, and blacklists can change. A scan is a snapshot, not a permanent verdict.

> **Bottom line:** Quick Intel provides data to inform your decisions. It reads contracts — it never touches your wallet or tokens. The $0.03 payment is the only transaction involved.

---

## Overview

| Detail | Value |
|--------|-------|
| **Endpoint** | `POST https://x402.quickintel.io/v1/scan/full` |
| **Cost** | $0.03 USDC (30000 atomic units) |
| **Payment Networks** | Base, Ethereum, Arbitrum, Optimism, Polygon, Avalanche, Unichain, Linea, MegaETH, **Solana** |
| **Payment Token** | USDC (native Circle USDC on each chain) |
| **Protocol** | x402 v2 (HTTP 402 Payment Required) |
| **Idempotency** | Supported via `payment-identifier` extension |

## Supported Chains (63)

| Chain | Chain | Chain | Chain |
|-------|-------|-------|-------|
| eth | arbitrum | bsc | opbnb |
| base | core | linea | pulse |
| zksync | shibarium | maxx | polygon |
| scroll | polygonzkevm | fantom | avalanche |
| bitrock | loop | besc | kava |
| metis | astar | oasis | iotex |
| conflux | canto | energi | velas |
| grove | mantle | lightlink | optimism |
| klaytn | solana | radix | sui |
| injective | manta | zeta | blast |
| zora | inevm | degen | mode |
| viction | nahmii | real | xlayer |
| tron | worldchain | apechain | morph |
| ink | sonic | soneium | abstract |
| berachain | unichain | hyperevm | plasma |
| monad | megaeth | | |

**Note:** Use exact chain names as shown (e.g., `"eth"` not `"ethereum"`, `"bsc"` not `"binance"`).

## Pre-Flight Checks

Before calling the API, verify:

### 1. USDC Balance on a Supported Payment Chain

You need at least $0.03 USDC on any supported payment chain. Base is recommended for EVM (lowest fees), Solana is also supported.

**Check balance (viem):**
```javascript
const balance = await publicClient.readContract({
  address: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", // USDC on Base
  abi: erc20Abi,
  functionName: "balanceOf",
  args: [walletAddress],
});
const hasEnough = balance >= 30000n; // $0.03 with 6 decimals
```

**Check balance (ethers.js):**
```javascript
const USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";
const balance = await usdcContract.balanceOf(walletAddress);
const hasEnough = balance >= 30000n; // $0.03 with 6 decimals
```

### 2. Valid Token Address

- EVM: 42-character hex address starting with `0x`
- Solana: Base58 encoded address (32-44 characters)

## How x402 Payment Works

x402 is an HTTP-native payment protocol. Here's the complete flow:

### EVM Payment Flow (Base, Ethereum, Arbitrum, etc.)

```
┌─────────────────────────────────────────────────────────────┐
│  1. REQUEST    POST to endpoint with scan parameters        │
│                                                             │
│  2. 402        Server returns "Payment Required"            │
│                PAYMENT-REQUIRED header contains payment info │
│                                                             │
│  3. SIGN       Your wallet signs EIP-3009 authorization     │
│                (transferWithAuthorization for USDC)          │
│                                                             │
│  4. RETRY      Resend request with PAYMENT-SIGNATURE header │
│                Contains base64-encoded signed payment proof  │
│                                                             │
│  5. SETTLE     Server verifies signature, settles on-chain  │
│                                                             │
│  6. RESPONSE   Server returns scan results (200 OK)         │
│                PAYMENT-RESPONSE header contains tx receipt   │
└─────────────────────────────────────────────────────────────┘
```

### Solana (SVM) Payment Flow

```
┌─────────────────────────────────────────────────────────────┐
│  1. REQUEST    POST to endpoint with scan parameters        │
│                                                             │
│  2. 402        Server returns "Payment Required"            │
│                Solana entry includes extra.feePayer address  │
│                                                             │
│  3. BUILD      Build SPL TransferChecked transaction:       │
│                - Set feePayer to gateway's facilitator       │
│                - Transfer USDC to gateway's payTo address    │
│                - Partially sign with your wallet             │
│                                                             │
│  4. RETRY      Resend request with PAYMENT-SIGNATURE header │
│                payload: { transaction: "<base64>" }          │
│                                                             │
│  5. SETTLE     Gateway co-signs as feePayer, submits to     │
│                Solana, confirms transaction                  │
│                                                             │
│  6. RESPONSE   Server returns scan results (200 OK)         │
│                PAYMENT-RESPONSE header contains tx signature │
└─────────────────────────────────────────────────────────────┘
```

### x402 v2 Headers

| Header | Direction | Description |
|--------|-----------|-------------|
| `PAYMENT-REQUIRED` | Response (402) | Base64 JSON with payment requirements and accepted networks |
| `PAYMENT-SIGNATURE` | Request (retry) | Base64 JSON with signed EIP-3009 authorization (EVM) or partially-signed transaction (SVM) |
| `PAYMENT-RESPONSE` | Response (200) | Base64 JSON with settlement tx hash/signature and block number |

**Note:** The legacy `X-PAYMENT` header is also accepted for v1 backward compatibility, but `PAYMENT-SIGNATURE` is preferred.

---

## ⚠️ PAYMENT-SIGNATURE Payload Structure (CRITICAL)

This is the exact structure your `PAYMENT-SIGNATURE` header must contain after base64 decoding. Getting this wrong is the #1 cause of payment failures.

### EVM Payment Payload (Decoded)

```json
{
  "x402Version": 2,
  "scheme": "exact",
  "network": "eip155:8453",
  "payload": {
    "signature": "0x804f6127...1b",
    "authorization": {
      "from": "0xYourWalletAddress",
      "to": "0xPayToAddressFrom402Response",
      "value": "30000",
      "validAfter": "0",
      "validBefore": "1771454085",
      "nonce": "0xa1b2c3d4...bytes32hex"
    }
  }
}
```

### SVM (Solana) Payment Payload (Decoded)

```json
{
  "x402Version": 2,
  "scheme": "exact",
  "network": "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",
  "payload": {
    "transaction": "base64-encoded-partially-signed-solana-transaction"
  }
}
```

### Field-by-Field Rules

| Field | Location | Type | Notes |
|-------|----------|------|-------|
| `x402Version` | Top level | Number | **Must be `2`.** Missing this may cause failures. |
| `scheme` | Top level | String | Always `"exact"` |
| `network` | Top level | String | CAIP-2 identifier from the 402 response (e.g., `"eip155:8453"`) |
| `signature` | `payload.signature` | String | **MUST be a direct child of `payload`, NOT inside `authorization`.** `0x`-prefixed hex. |
| `from` | `payload.authorization.from` | String | Your wallet address, `0x`-prefixed |
| `to` | `payload.authorization.to` | String | `payTo` address from the 402 response, `0x`-prefixed |
| `value` | `payload.authorization.value` | String | **Decimal string** (e.g., `"30000"`). NOT hex, NOT BigInt. |
| `validAfter` | `payload.authorization.validAfter` | String | **Decimal string** Unix timestamp. Use `"0"` for immediate. |
| `validBefore` | `payload.authorization.validBefore` | String | **Decimal string** Unix timestamp. Set ~1 hour in the future. |
| `nonce` | `payload.authorization.nonce` | String | `0x`-prefixed bytes32 hex. Must be unique per payment. |

### ❌ Common Mistakes That Cause Payment Failures

**1. `signature` nested inside `authorization` (WRONG)**
```json
// ❌ WRONG — causes "Cannot read properties of undefined (reading 'length')"
{
  "payload": {
    "authorization": {
      "from": "0x...",
      "to": "0x...",
      "value": "30000",
      "signature": "0x..."
    }
  }
}
```
```json
// ✅ CORRECT — signature is a SIBLING of authorization
{
  "payload": {
    "signature": "0x...",
    "authorization": {
      "from": "0x...",
      "to": "0x...",
      "value": "30000"
    }
  }
}
```

**2. Missing `x402Version` at top level**
```json
// ❌ WRONG — missing x402Version
{
  "scheme": "exact",
  "network": "eip155:8453",
  "payload": { ... }
}
```
```json
// ✅ CORRECT
{
  "x402Version": 2,
  "scheme": "exact",
  "network": "eip155:8453",
  "payload": { ... }
}
```

**3. Using hex or BigInt for `value`/`validAfter`/`validBefore`**
```json
// ❌ WRONG — hex strings
{ "value": "0x7530", "validAfter": "0x0", "validBefore": "0x69A1F3C5" }

// ❌ WRONG — raw numbers (may lose precision)
{ "value": 30000, "validAfter": 0, "validBefore": 1771454085 }

// ✅ CORRECT — decimal strings
{ "value": "30000", "validAfter": "0", "validBefore": "1771454085" }
```

**4. Wrong endpoint path**
```
❌ /v1/scan/auditfull
✅ /v1/scan/full                (correct public endpoint)
```

---

## Payment-Identifier (Idempotency)

The gateway supports the `payment-identifier` extension. If your agent might retry requests (network failures, timeouts), include a unique payment ID in the payload extensions to avoid paying twice:

```javascript
const paymentPayload = {
  x402Version: 2,
  scheme: 'exact',
  network: 'eip155:8453',
  payload: { /* ... */ },
  extensions: {
    'payment-identifier': {
      paymentId: 'pay_' + crypto.randomUUID().replace(/-/g, '')
    }
  }
};
```

If the gateway has already processed a request with the same payment ID, it returns the cached response without charging again. Payment IDs must be 16-128 characters, alphanumeric with hyphens and underscores.

### Discovery Endpoint

Query the gateway's accepted payments and schemas before making calls:

```
GET https://x402.quickintel.io/accepted
```

Returns all routes, supported payment networks, pricing, and input/output schemas for agent integration.

---

## Wallet Integration Patterns

### Pattern 1: Using `@x402/fetch` (Simplest — Recommended)

The `@x402/fetch` library handles the entire 402 → sign → retry flow automatically:

```javascript
import { x402Fetch } from '@x402/fetch';
import { createWallet } from '@x402/evm';

const wallet = createWallet(process.env.PRIVATE_KEY);

const response = await x402Fetch('https://x402.quickintel.io/v1/scan/full', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    chain: 'base',
    tokenAddress: '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00'
  }),
  wallet,
  preferredNetwork: 'eip155:8453'
});

const scanResult = await response.json();
```

### Pattern 2: Manual EVM Signing with viem (Full Control)

Complete working example for agents that need manual control over the payment flow:

```javascript
import { keccak256, toHex, verifyTypedData } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';

const SCAN_URL = 'https://x402.quickintel.io/v1/scan/full';
const PREFERRED_NETWORK = 'eip155:8453'; // Base

const account = privateKeyToAccount(process.env.PRIVATE_KEY);

// ── Step 1: Hit the endpoint, get 402 with payment requirements ──

const scanBody = JSON.stringify({
  chain: 'base',
  tokenAddress: '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00',
});

const initialRes = await fetch(SCAN_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: scanBody,
});

if (initialRes.status !== 402) {
  throw new Error(`Expected 402, got ${initialRes.status}`);
}

const paymentRequired = await initialRes.json();

// ── Step 2: Find your preferred network in the accepts array ──

const networkInfo = paymentRequired.accepts.find(
  (a) => a.network === PREFERRED_NETWORK
);
if (!networkInfo) {
  throw new Error(`Network ${PREFERRED_NETWORK} not available`);
}

// ── Step 3: Sign EIP-712 TransferWithAuthorization ──

// Generate a unique nonce (bytes32)
const nonce = keccak256(toHex(`${Date.now()}-${Math.random()}`));

// Validity window: valid immediately, expires in 1 hour
const validAfter = 0n;
const validBefore = BigInt(Math.floor(Date.now() / 1000) + 3600);

// EIP-712 domain — values come from the 402 response extra fields
const domain = {
  name: networkInfo.extra.name,       // "USD Coin"
  version: networkInfo.extra.version,  // "2"
  chainId: 8453,                       // Must match the network
  verifyingContract: networkInfo.asset, // USDC contract address
};

const types = {
  TransferWithAuthorization: [
    { name: 'from', type: 'address' },
    { name: 'to', type: 'address' },
    { name: 'value', type: 'uint256' },
    { name: 'validAfter', type: 'uint256' },
    { name: 'validBefore', type: 'uint256' },
    { name: 'nonce', type: 'bytes32' },
  ],
};

const message = {
  from: account.address,
  to: networkInfo.payTo,
  value: BigInt(networkInfo.amount),  // BigInt for signing
  validAfter,
  validBefore,
  nonce,
};

const signature = await account.signTypedData({
  domain,
  types,
  primaryType: 'TransferWithAuthorization',
  message,
});

// ── Step 4: Build the PAYMENT-SIGNATURE payload ──
// CRITICAL: signature is a SIBLING of authorization, not nested inside it.
// CRITICAL: value/validAfter/validBefore must be DECIMAL STRINGS in the payload.

const paymentPayload = {
  x402Version: 2,
  scheme: 'exact',
  network: PREFERRED_NETWORK,
  payload: {
    signature,                         // ← Direct child of payload
    authorization: {                   // ← No signature in here
      from: account.address,
      to: networkInfo.payTo,
      value: networkInfo.amount,                  // Decimal string: "30000"
      validAfter: validAfter.toString(),          // Decimal string: "0"
      validBefore: validBefore.toString(),        // Decimal string: "1771454085"
      nonce,                                      // 0x-prefixed bytes32
    },
  },
};

const paymentHeader = Buffer.from(JSON.stringify(paymentPayload)).toString('base64');

// ── Step 5: Retry the request with the payment header ──

const paidRes = await fetch(SCAN_URL, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'PAYMENT-SIGNATURE': paymentHeader,
  },
  body: scanBody,
});

// ── Step 6: Handle the response ──

// Check settlement receipt in the PAYMENT-RESPONSE header
const paymentResponse = paidRes.headers.get('payment-response');
if (paymentResponse) {
  const receipt = JSON.parse(Buffer.from(paymentResponse, 'base64').toString());
  console.log('Settlement tx:', receipt.txHash);
}

const scanResult = await paidRes.json();
console.log('Scan result:', scanResult);
```

### Pattern 3: Manual EVM Signing with ethers.js (Full Control)

Complete working example using ethers.js v6:

```javascript
import { ethers } from 'ethers';

const SCAN_URL = 'https://x402.quickintel.io/v1/scan/full';
const PREFERRED_NETWORK = 'eip155:8453'; // Base

const wallet = new ethers.Wallet(process.env.PRIVATE_KEY);

// ── Step 1: Hit the endpoint, get 402 with payment requirements ──

const scanBody = JSON.stringify({
  chain: 'base',
  tokenAddress: '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00',
});

const initialRes = await fetch(SCAN_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: scanBody,
});

if (initialRes.status !== 402) {
  throw new Error(`Expected 402, got ${initialRes.status}`);
}

const paymentRequired = await initialRes.json();

// ── Step 2: Find your preferred network in the accepts array ──

const networkInfo = paymentRequired.accepts.find(
  (a) => a.network === PREFERRED_NETWORK
);
if (!networkInfo) {
  throw new Error(`Network ${PREFERRED_NETWORK} not available`);
}

// ── Step 3: Sign EIP-712 TransferWithAuthorization ──

// Generate a unique nonce (bytes32)
const nonce = ethers.keccak256(
  ethers.toUtf8Bytes(`${Date.now()}-${Math.random()}`)
);

// Validity window: valid immediately, expires in 1 hour
const validAfter = 0n;
const validBefore = BigInt(Math.floor(Date.now() / 1000) + 3600);

// EIP-712 domain — values come from the 402 response extra fields
const domain = {
  name: networkInfo.extra.name,        // "USD Coin"
  version: networkInfo.extra.version,   // "2"
  chainId: 8453,                        // Must match the network
  verifyingContract: networkInfo.asset,  // USDC contract address
};

const types = {
  TransferWithAuthorization: [
    { name: 'from', type: 'address' },
    { name: 'to', type: 'address' },
    { name: 'value', type: 'uint256' },
    { name: 'validAfter', type: 'uint256' },
    { name: 'validBefore', type: 'uint256' },
    { name: 'nonce', type: 'bytes32' },
  ],
};

const message = {
  from: wallet.address,
  to: networkInfo.payTo,
  value: BigInt(networkInfo.amount),  // BigInt for signing
  validAfter,
  validBefore,
  nonce,
};

// ethers.js signTypedData takes positional args: domain, types, message
const signature = await wallet.signTypedData(domain, types, message);

// ── Step 4: Build the PAYMENT-SIGNATURE payload ──
// CRITICAL: signature is a SIBLING of authorization, not nested inside it.
// CRITICAL: value/validAfter/validBefore must be DECIMAL STRINGS in the payload.

const paymentPayload = {
  x402Version: 2,
  scheme: 'exact',
  network: PREFERRED_NETWORK,
  payload: {
    signature,                         // ← Direct child of payload
    authorization: {                   // ← No signature in here
      from: wallet.address,
      to: networkInfo.payTo,
      value: networkInfo.amount,                  // Decimal string: "30000"
      validAfter: validAfter.toString(),          // Decimal string: "0"
      validBefore: validBefore.toString(),        // Decimal string: "1771454085"
      nonce,                                      // 0x-prefixed bytes32
    },
  },
};

const paymentHeader = Buffer.from(JSON.stringify(paymentPayload)).toString('base64');

// ── Step 5: Retry the request with the payment header ──

const paidRes = await fetch(SCAN_URL, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'PAYMENT-SIGNATURE': paymentHeader,
  },
  body: scanBody,
});

// ── Step 6: Handle the response ──

const paymentResponse = paidRes.headers.get('payment-response');
if (paymentResponse) {
  const receipt = JSON.parse(
    Buffer.from(paymentResponse, 'base64').toString()
  );
  console.log('Settlement tx:', receipt.txHash);
}

const scanResult = await paidRes.json();
console.log('Scan result:', scanResult);
```

### Pattern 4: Solana Wallet (SVM)

```javascript
import { createSvmClient } from '@x402/svm/client';
import { toClientSvmSigner } from '@x402/svm';
import { wrapFetchWithPayment } from '@x402/fetch';
import { createKeyPairSignerFromBytes } from '@solana/kit';
import { base58 } from '@scure/base';

// Create Solana signer
const keypair = await createKeyPairSignerFromBytes(
  base58.decode(process.env.SOLANA_PRIVATE_KEY)
);
const signer = toClientSvmSigner(keypair);
const client = createSvmClient({ signer });
const paidFetch = wrapFetchWithPayment(fetch, client);

// Call scan API (x402 payment via Solana USDC)
const response = await paidFetch('https://x402.quickintel.io/v1/scan/full', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    chain: 'base',
    tokenAddress: '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00'
  })
});

const scanResult = await response.json();
```

### Pattern 5: AgentWallet (frames.ag)

AgentWallet handles the entire x402 flow in one call:

```javascript
const response = await fetch('https://frames.ag/api/wallets/{username}/actions/x402/fetch', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${AGENTWALLET_API_TOKEN}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    url: 'https://x402.quickintel.io/v1/scan/full',
    method: 'POST',
    body: {
      chain: 'base',
      tokenAddress: '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00'
    }
  })
});

const scanResult = await response.json();
```

### Pattern 6: Vincent Wallet (heyvincent.ai)

```javascript
// Vincent handles x402 via its transaction signing API
const paymentAuth = await vincent.signPayment({
  network: 'eip155:8453',
  amount: '30000',
  token: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
  recipient: recipientFromHeader
});

// Then retry with the signed payment
const response = await fetch('https://x402.quickintel.io/v1/scan/full', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'PAYMENT-SIGNATURE': paymentAuth.encoded
  },
  body: JSON.stringify({ chain: 'base', tokenAddress: '0x...' })
});
```

### Pattern 7: Sponge Wallet (x402_fetch — One-Liner)

Sponge Wallet handles the entire x402 payment flow automatically via its `x402_fetch` endpoint — no manual signing, no 402 parsing, no header construction:

```bash
curl -sS -X POST "https://api.wallet.paysponge.com/api/x402/fetch" \
  -H "Authorization: Bearer $SPONGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://x402.quickintel.io/v1/scan/full",
    "method": "POST",
    "body": {
      "chain": "base",
      "tokenAddress": "0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00"
    },
    "preferred_chain": "base"
  }'
```

Sponge detects the 402, signs the payment with the agent's managed wallet, retries, and returns the scan results along with `payment_made` and `payment_details` metadata. See the **sponge-wallet** skill for setup and registration.

### Other Compatible Wallets

Any wallet that supports x402 or EIP-3009 signing works with Quick Intel, including [Lobster.cash](https://lobster.cash) (Crossmint-powered agent wallets with Amazon checkout and Visa cards) and any wallet built on Crossmint's infrastructure. See their respective skills or docs for setup and onboarding.

---

## API Request

```http
POST https://x402.quickintel.io/v1/scan/full
Content-Type: application/json

{
  "chain": "base",
  "tokenAddress": "0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `chain` | string | Yes | Lowercase chain name (see supported chains) |
| `tokenAddress` | string | Yes | Token contract address |

## API Response

The scan returns comprehensive security analysis:

```json
{
  "tokenDetails": {
    "tokenName": "Ribbita by Virtuals",
    "tokenSymbol": "TIBBIR",
    "tokenDecimals": 18,
    "tokenSupply": 1000000000,
    "tokenCreatedDate": 1736641803000
  },
  "tokenDynamicDetails": {
    "is_Honeypot": false,
    "buy_Tax": "0.0",
    "sell_Tax": "0.0",
    "transfer_Tax": "0.0",
    "has_Trading_Cooldown": false,
    "liquidity": false
  },
  "isScam": null,
  "isAirdropPhishingScam": false,
  "contractVerified": true,
  "quickiAudit": {
    "contract_Renounced": true,
    "hidden_Owner": false,
    "is_Proxy": false,
    "can_Mint": false,
    "can_Blacklist": false,
    "can_Update_Fees": false,
    "can_Pause_Trading": false,
    "has_Suspicious_Functions": false,
    "has_Scams": false
  }
}
```

### Key Fields to Check

#### Immediate Red Flags (DO NOT BUY)

| Field | Bad Value | Meaning |
|-------|-----------|---------|
| `is_Honeypot` | `true` | Cannot sell — funds trapped |
| `isScam` | `true` | Known scam contract |
| `isAirdropPhishingScam` | `true` | Phishing attempt |
| `has_Scams` | `true` | Contains scam patterns |
| `can_Potentially_Steal_Funds` | `true` | Has theft mechanisms |

#### High Risk Warnings

| Field | Risky Value | Meaning |
|-------|-------------|---------|
| `buy_Tax` / `sell_Tax` | `> 10` | High tax reduces profits |
| `can_Mint` | `true` | Owner can inflate supply |
| `can_Blacklist` | `true` | Owner can block your wallet |
| `can_Pause_Trading` | `true` | Owner can freeze trading |
| `hidden_Owner` | `true` | Ownership obscured |
| `contract_Renounced` | `false` | Owner retains control |

#### Positive Signals

| Field | Good Value | Meaning |
|-------|------------|---------|
| `contract_Renounced` | `true` | No owner control |
| `contractVerified` | `true` | Source code public |
| `is_Launchpad_Contract` | `true` | From known launchpad |
| `can_Mint` | `false` | Fixed supply |
| `can_Blacklist` | `false` | No blocking capability |

### ⚠️ Liquidity Warning

The `liquidity` field in `tokenDynamicDetails` indicates whether Quick Intel detected a liquidity pool for the token. **However, this field has important limitations:**

- **`liquidity: false` does not always mean the token is illiquid.** Quick Intel checks major DEX pairs (e.g., WETH, USDC, USDT, native token). If the token is paired against a non-standard or niche token (e.g., a custom stablecoin, another meme token, or a chain-specific asset), it may not be detected.
- **Cross-DEX coverage varies by chain.** On popular chains like Base and Ethereum, coverage is broad. On newer or less common chains, fewer DEX routers are checked.
- **LP lock status is separate.** Even if `liquidity: true`, check `lp_Locks` in the response for lock details. Unlocked liquidity means the deployer can pull it at any time (rug pull risk).

**Recommended approach for agents:**
1. If `liquidity: false`, do NOT assume the token is untradeable. Verify independently by querying a DEX aggregator (e.g., 1inch, Jupiter, Odos) for the token's available pairs.
2. If `liquidity: true`, still check the LP lock status and the size of the pool before trading.
3. For non-standard pairings (token paired against another small-cap token), treat liquidity as unverified and proceed with extra caution — thin or exotic pairs carry additional slippage and exit risk.

### Interpreting Results

**Safe to trade (all must be true):**
- `is_Honeypot` = false
- `isScam` = null or false
- `has_Scams` = false
- `buy_Tax` and `sell_Tax` < 10%
- No `has_Suspicious_Functions`

**Proceed with caution:**
- `contract_Renounced` = false (owner can still act)
- `can_Update_Fees` = true (taxes could increase)
- `is_Proxy` = true (code can change)
- `liquidity` = false (verify independently — may be non-standard pair)

**Do not trade:**
- `is_Honeypot` = true
- `isScam` = true
- `can_Potentially_Steal_Funds` = true
- `buy_Tax` or `sell_Tax` > 50%

## Complete Example

```javascript
import { x402Fetch } from '@x402/fetch';
import { createWallet } from '@x402/evm';

async function scanToken(chain, tokenAddress) {
  const wallet = createWallet(process.env.PRIVATE_KEY);

  // Pre-flight: Check USDC balance
  const balance = await checkUSDCBalance(wallet.address);
  if (balance < 30000n) {
    throw new Error('Insufficient USDC on Base. Need at least $0.03');
  }

  // Scan token (x402 payment handled automatically by x402Fetch)
  const response = await x402Fetch('https://x402.quickintel.io/v1/scan/full', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chain, tokenAddress }),
    wallet,
    preferredNetwork: 'eip155:8453'
  });

  if (!response.ok) {
    throw new Error(`Scan failed: ${response.status}`);
  }

  const result = await response.json();

  // Analyze results
  const analysis = {
    token: result.tokenDetails.tokenName,
    symbol: result.tokenDetails.tokenSymbol,
    safe: !result.tokenDynamicDetails.is_Honeypot &&
          !result.isScam &&
          !result.quickiAudit.has_Scams,
    risks: []
  };

  if (result.tokenDynamicDetails.is_Honeypot) {
    analysis.risks.push('HONEYPOT - Cannot sell');
  }
  if (result.quickiAudit.can_Mint) {
    analysis.risks.push('Owner can mint new tokens');
  }
  if (result.quickiAudit.can_Blacklist) {
    analysis.risks.push('Owner can blacklist wallets');
  }
  if (!result.quickiAudit.contract_Renounced) {
    analysis.risks.push('Contract not renounced');
  }
  if (parseFloat(result.tokenDynamicDetails.buy_Tax) > 5) {
    analysis.risks.push(`High buy tax: ${result.tokenDynamicDetails.buy_Tax}%`);
  }
  if (parseFloat(result.tokenDynamicDetails.sell_Tax) > 5) {
    analysis.risks.push(`High sell tax: ${result.tokenDynamicDetails.sell_Tax}%`);
  }

  // Liquidity check — verify independently if false
  if (!result.tokenDynamicDetails.liquidity) {
    analysis.risks.push(
      'Liquidity not detected by scanner — may use non-standard pair. ' +
      'Verify via DEX aggregator before trading.'
    );
  }

  return analysis;
}

// Usage
const result = await scanToken('base', '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00');
console.log(result);
// {
//   token: "Ribbita by Virtuals",
//   symbol: "TIBBIR",
//   safe: true,
//   risks: ["Contract not renounced", "Liquidity not detected by scanner..."]
// }
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `402 Payment Required` | No payment header | Sign and include PAYMENT-SIGNATURE header |
| `402 Payment verification failed` | Invalid signature or insufficient USDC | Check payload structure (see Common Mistakes above), verify USDC balance |
| `402 Signature verification failed: Cannot read properties of undefined` | `signature` nested inside `authorization` instead of as a sibling | Move `signature` to be a direct child of `payload` |
| `402 Nonce already used` | Replay detected or retry without payment-identifier | Use payment-identifier for safe retries |
| `400 Invalid Chain` | Unknown chain name | Check supported chains list |
| `400 Invalid Address` | Malformed address | Verify address format |
| `404 Token Not Found` | Token doesn't exist | Check address and chain |
| `500 Scan Failed` | Contract analysis error | Retry or contact support |

## Important Notes

- **NEVER share private keys or seed phrases.** Quick Intel only needs the token's contract address and chain name. It does not need your wallet address for scanning.
- **Scan results are read-only data.** No transactions are returned, no approvals are requested, no on-chain state is modified. The only transaction is the $0.03 USDC payment.
- **Payment is charged regardless of outcome.** Even if the scan returns limited data (unverified contract, new token), you still pay $0.03. Use `payment-identifier` to safely retry without being charged twice.
- **Scan results are point-in-time.** A safe token today could be rugged tomorrow if not renounced. Re-scan periodically for tokens you hold.
- **Not financial advice.** Quick Intel provides data, not recommendations.
- **Solana tokens** use different analysis than EVM — some fields may be null.
- **Multi-chain payment:** You can pay on any supported chain — 9 EVM chains (Base, Ethereum, Arbitrum, Optimism, Polygon, Avalanche, Unichain, Linea, MegaETH) plus Solana. The 402 response lists all accepted networks.
- **Solana payment:** Pay with USDC on Solana using the SVM payment flow. The 402 response includes the `extra.feePayer` address needed to build the transaction.
- **Liquidity data is best-effort.** The scanner checks major DEX pairs but may miss tokens paired against non-standard assets. Always verify liquidity independently before executing trades, especially for new or niche tokens.
- **Quick Intel's endpoint (`x402.quickintel.io`) is operated by Quick Intel LLC**, a registered US based company providing crypto security APIs to platforms including DexTools and DexScreener. For more information: [quickintel.io](https://quickintel.io)

## Cross-Reference

For trading tokens after scanning, see the **tator-trade** skill which provides AI-powered trading with unsigned transactions.

For token launch strategy, evaluation, and tax guidance, see the **token-launcher** skill.

## Resources

- **Quick Intel Docs:** https://docs.quickintel.io
- **x402 Protocol:** https://www.x402.org
- **x402 EVM Spec:** https://github.com/coinbase/x402/blob/main/specs/schemes/exact/scheme_exact_evm.md
- **Gateway Discovery:** https://x402.quickintel.io/accepted
- **Quick Intel:** https://quickintel.io
- **Support:** https://t.me/quickintel