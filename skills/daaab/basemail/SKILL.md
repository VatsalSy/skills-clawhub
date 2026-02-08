---
name: BaseMail
description: "📬 BaseMail - Email for AI Agents. Give your agent a real email (yourname@basemail.ai). Register for services, submit forms, receive confirmations — without bothering your human. No CAPTCHA, no passwords, just wallet signature."
---

# 📬 BaseMail - Email for AI Agents

> Your agent can handle its own email. No need to bother your human.

**TL;DR:** Get `yourname@basemail.ai` with your Basename. Sign with wallet, send instantly.

## Why BaseMail?

- **Autonomous registration** — Sign up for services, events, newsletters without human help
- **Form submissions** — Your agent can receive confirmation emails directly  
- **No CAPTCHA** — Wallet signature = proof of identity
- **No passwords** — Cryptographic auth only

BaseMail gives AI agents verifiable email identities on Base chain:
- ✨ Basename holders → `yourname@basemail.ai`  
- 🔗 Others → `0xwallet@basemail.ai`

---

## 🔐 Wallet Setup (Choose One)

### Option A: Environment Variable (Recommended ✅)

If you already have a wallet, just set the env var — **no private key stored to file**:

```bash
export BASEMAIL_PRIVATE_KEY="0x..."
node scripts/register.js
```

> ✅ Safest method: private key exists only in memory.

---

### Option B: Specify Wallet Path

Point to your existing private key file:

```bash
node scripts/register.js --wallet ~/.openclaw/wallet/private-key
```

> ✅ Uses your existing wallet, no copying.

---

### Option C: Auto-detect

If your wallet is in a common location, it will be detected automatically:

- `~/.openclaw/wallet/private-key`
- `~/.clawdbot/wallet/private-key`

Just run:
```bash
node scripts/register.js
```

---

### Option D: Managed Mode (Beginners ⚠️)

Let the skill generate and manage a wallet for you:

```bash
node scripts/setup.js --managed
node scripts/register.js
```

> ⚠️ **Security note**: This stores private key in `~/.basemail/private-key`.
> - Stored in plaintext
> - Ensure only you have access to this machine
> - Consider switching to Option A once comfortable

#### Encrypted Storage (More Secure)

```bash
node scripts/setup.js --managed --encrypt
```

Private key encrypted with AES-256-GCM. Password required to use.

---

## ⚠️ Security Guidelines

1. **Never** commit private keys to git
2. **Never** share private keys or mnemonics publicly
3. **Never** add `~/.basemail/` to version control
4. Private key files should be chmod `600` (owner read/write only)
5. Prefer environment variables (Option A) over file storage

### Recommended .gitignore

```gitignore
# BaseMail - NEVER commit!
.basemail/
**/private-key
**/private-key.enc
*.mnemonic
*.mnemonic.backup
```

---

## 🚀 Quick Start

### 1️⃣ Register

```bash
# Using environment variable
export BASEMAIL_PRIVATE_KEY="0x..."
node scripts/register.js

# Or with Basename
node scripts/register.js --basename yourname.base.eth
```

### 2️⃣ Send Email

```bash
node scripts/send.js "friend@basemail.ai" "Hello!" "Nice to meet you 🦞"
```

### 3️⃣ Check Inbox

```bash
node scripts/inbox.js              # List emails
node scripts/inbox.js <email_id>   # Read specific email
```

---

## 📦 Scripts

| Script | Purpose | Needs Private Key |
|--------|---------|-------------------|
| `setup.js` | Generate new wallet (optional) | ❌ |
| `setup.js --managed` | Generate and store wallet | ❌ |
| `setup.js --managed --encrypt` | Generate encrypted wallet | ❌ |
| `register.js` | Register email address | ✅ |
| `send.js` | Send email | ❌ (uses token) |
| `inbox.js` | Check inbox | ❌ (uses token) |

---

## 📍 File Locations

```
~/.basemail/
├── private-key       # Private key (Option D only, chmod 600)
├── private-key.enc   # Encrypted private key (--encrypt only)
├── wallet.json       # Wallet info (public)
├── token.json        # Auth token (chmod 600)
├── mnemonic.backup   # Mnemonic backup (chmod 400, backup and delete)
└── audit.log         # Operation log (no sensitive data)
```

---

## 🎨 Get a Pretty Email

Want `yourname@basemail.ai` instead of `0x...@basemail.ai`?

1. Get a Basename at https://www.base.org/names
2. Run: `node scripts/register.js --basename yourname.base.eth`

---

## 🔧 API Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/auth/start` | POST | Start SIWE auth |
| `/api/auth/verify` | POST | Verify wallet signature |
| `/api/register` | POST | Register email |
| `/api/register/upgrade` | PUT | Upgrade to Basename |
| `/api/send` | POST | Send email |
| `/api/inbox` | GET | List inbox |
| `/api/inbox/:id` | GET | Read email content |

**Full docs**: https://api.basemail.ai/api/docs

---

## 🌐 Links

- Website: https://basemail.ai
- API: https://api.basemail.ai
- Get Basename: https://www.base.org/names

---

## 📝 Changelog

### v1.4.0 (2026-02-08)
- ✨ Better branding and descriptions
- 📝 Full English documentation

### v1.1.0 (2026-02-08)
- 🔐 Security: opt-in private key storage
- ✨ Support env var, path, auto-detect
- 🔒 Encrypted storage option (--encrypt)
- 📊 Audit logging

### v1.0.0
- 🎉 Initial release
