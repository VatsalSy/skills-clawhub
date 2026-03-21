---
name: figma-to-static
description: >
  Convert Figma design files to pixel-level mobile-first static HTML/CSS pages.
  Use when: (1) user provides a Figma file link and wants a static web page,
  (2) user sends design screenshots/assets and says "按设计图还原",
  (3) user asks to build a landing page from Figma,
  (4) iterating on Figma-to-code pixel accuracy.
  Handles: Figma REST API asset extraction, layered DOM reconstruction (not whole-image paste),
  visual diff pipeline with region heatmap for quality validation, mobile-first responsive layout.
  NOT for: React/Vue/SPA frameworks, server-side rendering, interactive JS-heavy pages.
---

# Figma → Static HTML/CSS

## Constraints

- **Only native HTML + CSS.** No React, Vue, or any framework.
- **Mobile-first.** PC: centered `max-width`, background stretches.
- **Directory structure:** `assets/ css/ html/`
- **Layered UI structure.** Never paste a whole section as a single `<img>` unless the design element is truly an image (photo/illustration). Text, buttons, status indicators → real DOM.
- **Avoid absolute positioning.** Prefer `flexbox`, `grid`, `margin`, `padding`, and normal document flow. Only use `position: absolute` as last resort (e.g., decorative badges on cards, small floating labels).
- **Image dimensions must be declared.** Every `<img>` must have explicit `width`/`height` attributes or CSS `aspect-ratio` to prevent layout shift (CLS).
- **BEM-like semantic class names.** Use `.block__element--modifier` (e.g. `.signin-card__label`, `.hero-topbar__brand`). Never use `.s1`, `.btn2`, `.c-red` abbreviations.
- **1:1 pixel-level restoration target.** Use visual diff pipeline to validate.

## Multi-Page Strategy

- If the user specifies multiple pages (e.g., "首页 + 活动页 + 个人中心"), create separate HTML files: `html/index.html`, `html/activity.html`, `html/profile.html`, etc.
- If the user does not specify, **default to single page** (`html/index.html`).
- Each page shares the same `css/styles.css` and `assets/` directory.
- If Figma file has multiple pages (top-level Page nodes), ask user which pages to implement.

## Version Control

- **Commit after each completed section** (not after every CSS tweak).
- Commit message format: `feat: add <section-name> section` or `fix: adjust <section-name> <what>`
- **Never push** unless user explicitly asks.
- Small, reversible commits. If unsure about a change, commit current state first, then experiment.

## Completion Criteria

The page is "done" when ALL of the following are met:
1. **Layout confirmed** by user (skeleton step).
2. **All sections implemented** with real DOM and real assets (no placeholders).
3. **Visual diff similarity ≥ 90%** against the full-page design reference.
4. **No horizontal scroll** on mobile viewport (375px-414px test).
5. **User explicitly confirms** final result.

## Workflow

### 0. Environment Check

Before starting, verify Figma REST API access:

```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/me"
```

- **200** → Token valid, proceed.
- **401/403** → Token invalid or expired. Guide user:
  1. Go to Figma → Account Settings → Personal access tokens
  2. Generate new token (needs "File content" scope)
  3. Set as env var: `export FIGMA_TOKEN=figd_...`
  4. Or pass `--token` to the script
- **No token set** → Guide user:
  1. Ask if they have a Figma token. If yes, set it: `export FIGMA_TOKEN=<token>`
  2. If no, walk them through creating one at https://www.figma.com/developers/api#access-tokens
  3. Remind: **never share tokens in chat** — use server env vars only
- **Network error** → Figma API unreachable. Check:
  1. `curl -I https://api.figma.com/v1/me` — if DNS fails, server may lack outbound access
  2. Try with proxy if needed: `export HTTPS_PROXY=...`

If REST API is unavailable, fall back to user-provided ZIP assets and design screenshots.

### 1. Gather Inputs

Required (at least one):
- Figma file URL + fileKey
- User-provided ZIP of design assets (PNG/SVG)
- Design reference screenshots

If Figma file available:
- Use `scripts/fetch_figma_rest.py` to extract node structure + images via REST API (not MCP — MCP has tool-call limits).
- User must provide `FIGMA_TOKEN` in environment or pass `--token`.

If ZIP provided:
- Unzip to a `source/` dir.
- Rename files to meaningful names (`design-banner.png`, `play1-bg.png`, etc.).
- Copy usable assets to `assets/`.

### 2. Analyze Structure → Layout First, Then Details

**Critical rule: always build the skeleton before polishing pixels.**

1. **Identify sections** from the full-page design:
   - Scan top-to-bottom, name each visual block (hero, signin, feature-1, feature-2, footer…).
   - Output a section map with approximate vertical order and height ratios.

2. **Build the skeleton** — placeholder-only HTML/CSS:
   - One `<section>` per block with a colored background or placeholder text.
   - Flex/grid layout structure in place (no absolute positioning).
   - Correct vertical stacking order and relative heights.
   - `overflow-x: hidden` on body, scrollable rows marked.

3. **Take skeleton screenshot → send to user for confirmation.**
   - Ask: "布局结构和分段顺序对吗？"
   - Do NOT proceed to detail work until user confirms the layout.

4. **Only then, layer in details** per confirmed section:
   - Insert real assets (images, icons).
   - Build real DOM for text, buttons, status indicators, timelines.
   - Apply typography, colors, spacing, borders from Figma node data.
   - Take screenshot → send to user after each section completes.
   - Git commit after each section is done.

5. **Missing assets? Try to fetch before asking:**
   - Check if the asset exists in `assets/` or `source/`.
   - If REST API is available, try `scripts/fetch_figma_rest.py --nodes <node-id>` to download directly from Figma.
   - If the node ID is unknown, ask the user for the specific layer/node ID.
   - If REST API fails or the asset cannot be found, ask the user to send the file directly.

6. **NEVER generate fake assets.**
   - Do NOT screenshot a design and crop it to create an "asset".
   - Do NOT draw/create placeholder images to simulate missing design elements.
   - Do NOT use solid-color boxes or emoji to stand in for real icons/photos.
   - Every pixel must come from either: (a) Figma export, (b) user-provided file, or (c) CSS/SVG reconstruction of simple shapes (borders, backgrounds, gradients — NOT complex illustrations).

### 3. Build the Page

Generate three directories:

**`html/index.html`** (or `html/<page>.html` for multi-page)
- Semantic `<section>` per design block.
- Real DOM elements for text, status, buttons, timelines.
- Images only for true visual assets (backgrounds, illustrations, photos).
- `<meta viewport>` with `width=device-width, initial-scale=1`.

**`css/styles.css`**
- `:root` variables for max-width and theme colors.
- `overflow-x: hidden` on `html, body, .page-shell` to prevent horizontal scroll.
- `overflow-x: clip` on `.stage` containers; only specific scrollable rows get `overflow-x: auto`.
- Percentage-based positioning for overlays (derived from Figma node coordinates).
- `clamp()` for responsive typography.
- `@media (min-width: 801px)` for PC centered layout.

**`assets/*`**
- Named meaningfully (not `figma-01.png`).
- Prefer user-provided assets over Figma exports when available.

### 4. Auto-Extract CSS from Figma Nodes

After fetching `nodes.json`, run the auto-extraction script:

```bash
python3 scripts/figma_to_css.py --nodes rest-assets/nodes.json --out source/figma-extracted.css
```

This parses every node and outputs CSS property blocks for:
- Colors, fonts, spacing, shadows, borders, border-radius
- Auto-layout: flex-direction, gap, justify-content, align-items, padding

Use the extracted CSS as a reference when writing `styles.css`. Do NOT copy-paste blindly — adapt to the actual DOM structure.

### 5. Extract Exact Properties from Figma Nodes

**All visual properties must match the Figma design exactly. Do NOT guess or eyeball.**

Parse `nodes.json` and extract per-element:

| Property | Figma field | CSS mapping |
|---|---|---|
| Background color | `fills[0].color` → `{r,g,b,a}` | `rgb(r*255, g*255, b*255)` or `rgba(...)` |
| Text color | `fills[0].color` on Text node | `color:` |
| Font family | `fontName.family` | `font-family:` |
| Font size | `fontSize` | `font-size:` (use px, convert to rem/vw as needed) |
| Font weight | `fontWeight` | `font-weight:` |
| Line height | `lineHeightPx` or `lineHeightPercent` | `line-height:` |
| Letter spacing | `letterSpacing` | `letter-spacing:` |
| Border radius | `cornerRadius` | `border-radius:` |
| Border | `strokes[0]` | `border:` |
| Opacity | `opacity` | `opacity:` |
| Shadow | `effects[]` where `type==="DROP_SHADOW"` | `box-shadow:` |
| Padding | layout padding values | `padding:` |

**Rules:**
- Always read from Figma JSON first. Only fall back to visual estimation if the field is missing.
- Convert Figma 0-1 RGBA values to CSS 0-255 RGB: multiply by 255 and round.
- For mobile responsive: convert fixed `px` font sizes to `clamp()` or `vw` units while preserving the design-ratio proportions.
- If a property looks wrong in the rendered output (e.g., color mismatch due to alpha blending), check the Figma node's parent chain — inherited styles may override.
- **Element gap/spacing must match Figma exactly.** Calculate from `itemSpacing` or adjacent node coordinate differences. Never estimate.
- **Text alignment must match Figma.** Use `textAlignHorizontal` / `textAlignVertical` from the node. Never default all text to `text-align: center`.
- **Text alignment per block.** Multi-line text blocks must use the Figma node's `textAlign` value (left/center/right), not a global default.
- **Text shadow must match Figma.** Extract from `effects[]` where `type === "DROP_SHADOW"` or `"INNER_SHADOW"`. Never omit and never add fake ones.
- **Content padding from Figma auto-layout.** Extract `paddingLeft`, `paddingRight`, `paddingTop`, `paddingBottom` from the parent Frame. Never guess padding values.
- **List/grid gap from Figma.** Extract `itemSpacing` from Figma auto-layout. Never use a generic `gap: 8px` without checking.
- **Max-width from Figma Frame width.** Content container widths must come from the actual Figma Frame dimension, not an arbitrary value.
- **Hover/active/disabled states.** If the design has variant frames for interactive states, implement them with `:hover` / `:active` / `:disabled` pseudo-classes.

### 6. Visual Diff Validation (with Region Heatmap)

After each major iteration:

```bash
# 1. Screenshot current render
google-chrome --headless=new --disable-gpu --no-sandbox \
  --window-size=800,5338 \
  --screenshot=compare/current.png \
  http://127.0.0.1:PORT/html/

# 2. Compare with region heatmap (default 5x5 grid)
python3 scripts/visual_diff.py \
  --current compare/current.png \
  --target assets/design-main.png \
  --diff compare/diff.png \
  --regions 5 \
  --threshold 30
```

The heatmap overlay shows:
- **Green** → low error (good match)
- **Yellow** → moderate error
- **Red** → high error (needs fixing)
- **Labeled boxes** on regions with MAE > threshold

Focus iteration on red regions first.

### 7. Preview Server

When running on a cloud server, start a temporary HTTP server for public preview:

```bash
# Find an available port (e.g. 8090 if 8080 is taken)
python3 -m http.server PORT --bind 0.0.0.0
```

- Run in background so it persists across iterations.
- Bind to `0.0.0.0` (not `127.0.0.1`) so it's accessible via public IP.
- Check for port conflicts before starting (`lsof -i :PORT` or `ss -tlnp`).
- Provide user with `http://<PUBLIC_IP>:PORT/html/` link.
- If running behind a firewall, ensure the port is open.

### 8. Screenshot & Send to User (Every Iteration)

After each code generation iteration, before reporting results:

1. Take a screenshot of the current render:
```bash
google-chrome --headless=new --disable-gpu --no-sandbox \
  --window-size=800,5338 \
  --screenshot=compare/current.png \
  http://127.0.0.1:PORT/html/
```

2. **Send the screenshot to the user** via the messaging platform (Telegram/Discord/etc.) using the media/file sending tool — do NOT just send a URL, send the actual image.

3. Then optionally run visual diff against target and mention the similarity score.

This ensures the user can verify visual quality **without opening a browser** on every iteration.

## Anti-Patterns (Learned the Hard Way)

1. **Never paste a full section as one `<img>`.** User will say "按设计图结构来" — rebuild with real DOM.
2. **Never invent content.** All text must come from Figma node data or design reference. If unsure, ask.
3. **Never fake assets.** No screenshots cropped as "assets", no solid-color placeholder boxes for real images, no emoji as icons. Every visual element must come from Figma export, user-provided file, or pure CSS (gradients/borders only).
4. **Never skip `overflow-x: hidden` on body.** Page will scroll horizontally on mobile.
5. **Never use Figma MCP for bulk extraction.** It has tool-call limits. Use REST API instead.
6. **Never hardcode pixel positions for overlays.** Use percentage-based positioning from Figma coordinates.
7. **Avoid `position: absolute`.** Default to flexbox/grid/normal flow. Absolute is only for small decorative overlays (badges, floating labels, tiny icons). Layout structure must work without absolute positioning.
8. **Never put `overflow-x: auto` on body/page-shell.** Only on specific scrollable rows (e.g., signin cards).
9. **Timeline/progress bars must be real DOM.** Not simplified single-color divs. Build track + progress + nodes + labels.
10. **Never guess a property when Figma JSON has the data.** Read the JSON first, estimate only as last resort.

## Scripts

- `scripts/fetch_figma_rest.py` — Extract node metadata + images via Figma REST API
- `scripts/figma_to_css.py` — Auto-parse `nodes.json` → CSS property blocks
- `scripts/visual_diff.py` — Compare rendered screenshot against target with region heatmap

## References

- `references/file-structure.md` — Standard project directory layout
- `references/css-patterns.md` — Reusable CSS patterns for common design elements
