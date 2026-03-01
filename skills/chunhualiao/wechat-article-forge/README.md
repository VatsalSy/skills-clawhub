# wechat-article-writer

> 从选题到发布的公众号一体化写作工作流

An OpenClaw skill that automates the full lifecycle of a WeChat Official Account (微信公众号) article: topic research, multi-agent writing with quality gates, scrapbook-style illustrations, formatting, and publishing to the draft box.

**v2.3.1** — Three publishing paths: Official Account API (new, recommended), browser tool, or direct CDP.

---

## What It Does

```
forge write 关于AI编程工具的深度评测
```

That single command runs a **9-step pipeline**:

1. **Research + Prep** — topic angles, verified `sources.json` bank, voice profile, outline
2. **Write** via Writer subagent (Chinese-first, constrained to source bank)
3. **Review** via Reviewer subagent (blind 8-dimension craft scoring)
4. **Revise** — 4a: up to 2 automated cycles; 4b: human-in-the-loop if needed
5. **Fact-check** via Fact-Checker subagent (verify every claim, generate reference list)
6. **Format** to WeChat HTML via `wenyan-cli` + post-processing (`scripts/format.sh`)
7. **Preview** on local HTTP server for human approval
8. **Illustrate + Embed** — scrapbook images via article-illustrator, upload to WeChat CDN
9. **Publish** to WeChat draft box — via API (preferred) or browser automation (fallback)

---

## Architecture

```
Orchestrator (Main Agent) — routes, tracks, enforces gates
    ├── Writer Subagent — drafts + revises (Opus model)
    ├── Reviewer Subagent — blind craft scoring (Sonnet model)
    ├── Fact-Checker Subagent — verifies claims via web search (Sonnet model)
    └── article-illustrator — scrapbook images (after text passes)
```

- **Writer never self-reviews.** Writer is constrained to a verified source bank — must mark `[UNVERIFIED]` for any claims outside the bank.
- **Reviewer is blind.** Never sees outline or brief — judges craft as a reader would.
- **Fact-Checker is independent.** Verifies every claim (institutions, names, numbers, quotes) via web search. Generates reference list.
- **Orchestrator is lean.** Routes, tracks versions, enforces quality gates.
- **Illustrations are gated.** No images until text is human-approved (~$0.06/article via Z.AI).

---

## Setup

Run the one-click setup script after installation:

```bash
bash <skill-dir>/scripts/setup.sh <workspace-dir>
```

This creates `~/.wechat-article-writer/`, installs dependencies, appends rules to `AGENTS.md` and `HEARTBEAT.md`, validates API keys, and generates `config.json`.

### API Keys

| Key | Purpose | Required? |
|-----|---------|-----------|
| `ZAI_API_KEY` | Image generation via Z.AI ($0.015/image) | Preferred |
| `GLM_API_KEY` | Image generation via BigModel China | Alternative |
| `OPENROUTER_API_KEY` | Image generation fallback | Alternative |

At least one image key is required for illustrations.

### Publishing Credentials

**Path C (API — recommended):** Store appid + appsecret in your credentials file (configure path via `wechat_secrets_path` in `config.json`; default: `~/.wechat-article-writer/secrets.json`):
```json
{ "appid": "wx...", "appsecret": "..." }
```
No browser setup needed. Works for unverified subscription accounts.

**Path A/B (browser fallback):** If no API credentials, the skill automates `mp.weixin.qq.com` via Chrome CDP. See `references/browser-automation.md`.

---

## Commands

| Command | Description |
|---------|-------------|
| `forge topic <subject>` | Research + propose 3 topic angles |
| `forge write <subject>` | Full pipeline: research → write → review → illustrate → publish |
| `forge draft <subject>` | Write + format only, stop before illustrations |
| `forge publish <draft-id>` | Push existing draft to WeChat |
| `forge preview <draft-id>` | Format check + preview snippet |
| `forge voice train` | Build voice profile from past articles |
| `forge status` | Show all drafts and their status |

---

## Publishing (Step 9)

The skill checks for publishing credentials in this order and uses the first available method:

### Path C — WeChat Official Account API ✓ (recommended)

**Requirements:** Credentials file at `wechat_secrets_path` (configured in `config.json`) with `appid` + `appsecret`.

```bash
python3 scripts/publish_via_api.py \
  --draft-dir ~/.wechat-article-writer/drafts/<slug> \
  --title "草稿标题（≤18字）" \
  --author "作者" \
  --source-url "https://..."
```

**What it does:**
1. Fetches OAuth2 access token
2. Uploads all images to WeChat CDN (`cgi-bin/media/uploadimg`)
3. Uploads cover as permanent material (`cgi-bin/material/add_material`)
4. Cleans HTML content (strips wrapper tags, verbose styles, preview banners)
5. Creates draft via `cgi-bin/draft/add` with `ensure_ascii=False` encoding

**⚠️ Undocumented WeChat API field limits** (confirmed empirically, February 2026):

| Field | Documented | Actual Limit |
|-------|-----------|--------------|
| `title` | 64 chars | **≤18 chars** (36 bytes) |
| `author` | 8 chars | **≤8 bytes** (= 2 Chinese chars) |
| `digest` | 120 chars | **~28 Chinese chars** |
| `content` | 20,000 bytes | **~18KB UTF-8** |

> **Important:** Error codes are unreliable. `errcode 45003` claims "title too large" but may actually mean content too large. Test fields independently when debugging.

> **Title workaround:** The API title is only for the draft box listing. Edit it to the full version in the WeChat editor UI before publishing — the UI has no 18-char limit.

### Path A — OpenClaw Browser Tool (macOS/Titan)

Uses the `browser` tool to drive `mp.weixin.qq.com` directly via Playwright. Injects article HTML via base64 chunking + clipboard paste. No Python/CDP needed. See `references/browser-automation.md` → Path A.

### Path B — Direct CDP WebSocket (Linux/Remote)

Connects to Chrome's CDP endpoint directly from Python. Requires Chrome launched with `--remote-debugging-port=18800 --remote-allow-origins='*'`. See `references/browser-automation.md` → Path B.

---

## Quality Gates

### Reviewer Scoring (8 dimensions)

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| Insight Density (洞察密度) | 20% | Non-obvious ideas per section? |
| Originality (新鲜感) | 15% | Genuinely new framing? |
| Emotional Resonance (情感共鸣) | 15% | Earned emotional arc? |
| Completion Power (完读力) | 15% | Every section earns the next scroll? |
| Voice (语感) | 10% | Natural Chinese, sounds like a person? |
| Evidence (论据) | 10% | Named researchers, institutions, publication venues. |
| Content Timeliness (内容时效性) | 10% | Core argument rests on principles, not news? |
| Title (标题) | 5% | Clear, specific, ≤26 chars? |

**Pass threshold:** weighted_total ≥ 9.0, no dimension below 7, Originality ≥ 8.

**Hard blockers (instant FAIL):** 教材腔, 翻译腔, 鸡汤腔, 灌水, 模板化, 标题党.

### Pipeline State Machine

State is persisted to `pipeline-state.json` in each draft directory. Survives context compaction and session restarts — the orchestrator always resumes from the exact step it left off, including sub-phases within publishing (image upload progress, chunks stored, etc.).

---

## Illustrations

Uses the **article-illustrator** skill's scrapbook pipeline:

1. Read scrapbook system prompt (`references/scrapbook-prompt.md`)
2. Generate JSON plan with 300–500 char physical mixed-media descriptions
3. Generate all images in parallel via Z.AI (preferred) or OpenRouter (fallback)
4. Upload images to WeChat CDN (Path C) or embed as base64 (Paths A/B)

**Style:** Hand-crafted scrapbook collages — torn paper, washi tape, cork boards, hand-drawn markers.

**Cost:** ~$0.06 per article (4 images × $0.015 via Z.AI).

> **Z.AI CDN note:** After generation, the CDN URL may return 404 immediately. The script retries with a 4-second delay (up to 5 attempts). This is a known Z.AI behavior, not a credential issue.

---

## Configuration

`~/.wechat-article-writer/config.json`:

```json
{
  "default_article_type": "教程",
  "chrome_debug_port": 18800,
  "chrome_display": ":1",
  "chrome_user_data_dir": "/tmp/openclaw-browser2",
  "wechat_author": "你的公众号名称",
  "wechat_secrets_path": "~/.wechat-article-writer/secrets.json",
  "word_count_targets": {
    "资讯": [800, 1500],
    "周报": [1000, 2000],
    "教程": [1500, 3000],
    "观点": [1200, 2500],
    "科普": [1500, 3000]
  }
}
```

---

## Data Layout

```
~/.wechat-article-writer/
├── config.json
├── voice-profile.json
├── session.json
└── drafts/
    └── <slug-YYYYMMDD>/
        ├── pipeline-state.json      # State machine (compaction-safe)
        ├── meta.json                # Status, title, timestamps
        ├── outline.md
        ├── sources.json             # Verified source bank
        ├── draft.md                 # → draft-v2.md, ...
        ├── review-v1.json           # → review-v2.json, ...
        ├── fact-check.json          # Claim verification results
        ├── formatted.html           # WeChat HTML (pre-images)
        ├── wechat_image_urls.json   # WeChat CDN URLs after upload (Path C)
        ├── wechat_draft_id.json     # media_id after successful draft creation
        └── images/
            ├── illustration-plan.json
            ├── img1.png
            └── img1.prompt.txt
```

---

## Known Issues & Workarounds

| Issue | Workaround |
|-------|-----------|
| WeChat API title limit is 18 chars (not 64 as documented) | Use short API title; edit to full title in WeChat editor UI before publishing |
| `requests(..., json=)` escapes Chinese as `\uXXXX` | Use `data=json.dumps(..., ensure_ascii=False).encode("utf-8")` instead |
| Z.AI CDN 404 immediately after generation | Retry with 4s delay; resolves within 1-2 attempts |
| WeChat error codes are unreliable | Test fields independently; ignore errmsg text |

---

## Scripts

| Script | Description |
|--------|-------------|
| `scripts/setup.sh` | One-click environment setup |
| `scripts/format.sh` | Markdown → WeChat HTML via wenyan-cli |
| `scripts/publish_via_api.py` | New in v2.3.0 — API-based publisher (Path C) |

---

## References

| File | When to load |
|------|-------------|
| `references/writer-prompt.md` | Step 2 (writing) and Step 4 (revision) |
| `references/reviewer-rubric.md` | Step 3 — full 8-dimension scoring criteria |
| `references/fact-checker-prompt.md` | Step 5 — claim verification protocol |
| `references/browser-automation.md` | Step 9 — all three publishing paths |
| `references/pipeline-state.md` | On resume — state machine schema |
| `references/wechat-html-rules.md` | Step 6 — what HTML/CSS works in WeChat |
| `REFERENCES/LESSONS_LEARNED.md` | Hard-won lessons from production sessions |

---

## Quality Scorecard

| Category | Score | Details |
|----------|-------|---------|
| Completeness (SQ-A) | 8/8 | All checks pass including versioning conventions |
| Clarity (SQ-B) | 5/5 | Pipeline heading corrected, no contradictions |
| Balance (SQ-C) | 5/5 | Writer≠Reviewer≠Fact-Checker, scripts for deterministic tasks |
| Integration (SQ-D) | 5/5 | article-illustrator dependency declared, file layout consistent |
| Scope (SCOPE) | 3/3 | Clean boundaries, no org-specific refs in README |
| OPSEC | 2/2 | No hardcoded paths, no secrets |
| References (REF) | 3/3 | All 14 reference files present and cited |
| Architecture (ARCH) | 2/2 | SoC maintained, deterministic/judgment tasks split correctly |
| **Total** | **33/33** | |

*Scored by skill-engineer — iteration 2, v2.3.1**

---

## License

MIT
