## v2.3.1 — 2026-02-28

### Polish: OPSEC + Clarity Improvements (skill-engineer review)

**OPSEC-1 fix:** Removed hardcoded internal org-specific credential path from all public-facing files. The credentials path is now configurable:
- New field: `wechat_secrets_path` in `config.json` (default: `~/.wechat-article-writer/secrets.json`)
- `scripts/publish_via_api.py` now reads the path from config.json, with fallback to default
- SKILL.md and README updated to reference the configurable path

**SQ-B2 fix:** Corrected pipeline heading from "11 Steps" to "9 Steps" (4a/4b are sub-steps of step 4, not independent steps). Matches the "9-step pipeline" description elsewhere.

**SQ-A6/SQ-D3 fix:** Added "Versioning" section to SKILL.md with semver conventions and CHANGELOG update guidance.

**skill.yml:** Added `config` block documenting `wechat_secrets_path` with type, default, and description.

---

# Changelog

## v2.3.0 — 2026-02-28

### Path C: WeChat Official Account API

Added **Path C** — direct API publishing without browser automation. Works for both verified and unverified subscription accounts.

**Why it matters:** Browser automation (Paths A and B) is fragile — WeChat's DOM changes without notice, session tokens expire, and browser setup varies by platform. The API is stable, headless, and doesn't require a logged-in browser session.

**How to use:**
```bash
python3 scripts/publish_via_api.py \
  --draft-dir ~/.wechat-article-writer/drafts/<slug> \
  --title "草稿标题（≤18字）" \
  --author "作者" \
  --source-url "https://..."
```
Store credentials at `~/.wechat-article-writer/secrets.json` (or custom path via `wechat_secrets_path` in config.json).

### New Script: `scripts/publish_via_api.py`

Complete, production-ready publisher:
- Gets access token from appid + appsecret
- Uploads images to WeChat CDN (`media/uploadimg`)
- Uploads cover as permanent material (`material/add_material`)
- Cleans HTML (strips meta, preview banners, verbose styles, section wrappers)
- Creates draft with correct `ensure_ascii=False` encoding
- Warns when field limits will be exceeded

### Critical Bug Fix: Chinese Text Encoding

`requests(..., json=payload)` uses `ensure_ascii=True` by default, causing all Chinese characters to appear as `\u5199\u4e66` in the WeChat editor. Fixed by using `data=json.dumps(..., ensure_ascii=False).encode("utf-8")`.

### Documented Undocumented API Limits

Official docs are wrong. Actual limits confirmed by binary search:
- `title`: ≤18 chars (not 64)
- `author`: ≤8 bytes (not 8 chars — Chinese chars are 3 bytes each)
- `content`: ~18KB UTF-8 (practical limit, not documented)
- Error codes are unreliable — same code can mean different field violations

### Documentation Updates

- `references/browser-automation.md`: Added Path C with full code examples and comparison table
- `REFERENCES/LESSONS_LEARNED.md`: Added 2026-02-28 session findings (4 new lessons + Path C checklist)
- `SKILL.md`: Updated Step 9 to mention three paths; Path C listed as preferred when credentials available; added `ensure_ascii` key rule

---

## v2.2.0 — 2026-02-26

### Browser Automation Overhaul

**Two publishing paths** based on environment:
- **Path A (Browser Tool):** For macOS/Titan where OpenClaw manages the browser via Playwright. Uses base64 chunking to bypass escaping issues. Fully documented with step-by-step evaluate calls.
- **Path B (Direct CDP):** For Linux/remote servers with standalone Chrome. Uses Python WebSocket for direct CDP access.

### Key Lessons Incorporated
- OpenClaw's browser tool uses Playwright, which isolates page contexts. External CDP connections see zero targets. Documented why and how to work within this constraint.
- HTML injection via base64 chunking: encode → chunk (3500 chars) → store in `window._b` → `atob()` → ClipboardEvent paste. Eliminates all escaping issues.
- Title field is now a `<textarea>` (changed from input/contenteditable). Updated selectors.
- Mixed content blocking: HTTPS pages cannot load HTTP localhost resources. Use blob paste, not URL injection.

### Pipeline State Improvements
- Added `publishing_sub` field for sub-phase tracking within the publishing step
- Tracks: preparing → chunking → text_injected → images_inserting → images_done → saving
- `chunks_stored`, `images_inserted` counters enable resume after compaction
- `publishing_path` field records which path (browser_tool vs direct_cdp) was used

### Cost Optimization
- Z.AI (GLM-Image) now documented as preferred illustration provider: ~$0.015/image vs ~$0.12 for OpenRouter
- 4 illustrations cost ~$0.06 total (was ~$0.50) — 8x cheaper with better Chinese text accuracy (97.9%)
- Updated figure-generation-guide.md with Z.AI as primary, OpenRouter as fallback

### Documentation
- `LESSONS_LEARNED.md` expanded with 2026-02-26 findings (5 new lessons)
- `browser-automation.md` fully rewritten with dual-path documentation
- Added pre-publishing checklist

---

## v2.1.0 — 2026-02-23

- Two-phase image injection (text first, then blob paste per image)
- Image verification step (count + position check)
- Save confirmation wait loop
- Initial LESSONS_LEARNED.md with first production session findings

## v1.0.0 — 2026-02-17

Initial release.

- 7 modes: topic, write, draft, publish, preview, voice, status
- Chinese-first writing with voice profile matching
- Quality gates: 8 content checks + 7 format checks with auto-fix
- Composes with: wechat-publisher, blog-writer, mermaid, autonomous-task-runner
- 64 trigger test cases (98.4% accuracy)
- Default voice profile for new users
- Config-driven auto-publish logic
