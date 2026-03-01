---
name: frontend-slides
description: Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, create solution decks (解决方案PPT), presales/sales pitch, or client proposal. Ideal for sales and presales teams making solution presentations. Helps non-designers discover their aesthetic through visual exploration rather than abstract choices.
---

# Frontend Slides Skill

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser. This skill helps non-designers discover their preferred aesthetic through visual exploration ("show, don't tell"), then generates production-quality slide decks.

**Reference files:** When generating CSS, image processing, PPT extraction, HTML structure, edit button, or animation code, read the corresponding file under `reference/` (and STYLE_PRESETS.md for presets and CSS Gotchas) so output is correct and complete.

## Core Philosophy

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** — Generate visual previews so users pick what they like, not abstract choices.
3. **Distinctive Design** — Avoid generic "AI slop" aesthetics. Every presentation should feel custom-crafted.
4. **Production Quality** — Well-commented, accessible, performant code.
5. **Viewport Fitting (CRITICAL)** — Every slide MUST fit exactly within the viewport. No scrolling within slides, ever.

---

## CRITICAL: Viewport Fitting Requirements

**Mandatory for ALL presentations.** Every slide must be fully visible without scrolling on any screen size.

### The Golden Rule

- Each slide = exactly one viewport height (`100vh` / `100dvh`).
- Content overflows? → Split into multiple slides or reduce content. Never scroll within a slide.

### Content Density Limits (per slide)

| Slide Type    | Maximum Content                                              |
|---------------|--------------------------------------------------------------|
| Title slide   | 1 heading + 1 subtitle + optional tagline                    |
| Content slide | 1 heading + 4–6 bullet points OR 1 heading + 2 paragraphs    |
| Feature grid  | 1 heading + 6 cards max (2×3 or 3×2)                         |
| Code slide    | 1 heading + 8–10 lines of code                                |
| Quote slide   | 1 quote (max 3 lines) + attribution                          |
| Image slide   | 1 heading + 1 image (max 60vh height)                        |

**Required base CSS:** Include the full mandatory base styles in every presentation. **Copy from [reference/viewport-and-base.css](reference/viewport-and-base.css)** (or inline equivalent). It covers: html/body lock, `.slide` = 100vh/100dvh + overflow hidden, `.slide-content`, `:root` clamp() variables, cards/lists/grids/images, responsive breakpoints (700px, 600px, 500px height; 600px width), and reduced-motion.

### Overflow Prevention Checklist

Before generating: (1) Every `.slide` has `height: 100vh; height: 100dvh; overflow: hidden;` (2) All font sizes and spacing use `clamp()` or viewport units (3) Content containers have `max-height` (4) Images `max-height: min(50vh, 400px)` or similar (5) Grids use `auto-fit` + `minmax()` (6) Breakpoints for heights 700/600/500 (7) No fixed pixel heights on content (8) Per-slide content within density limits.

### When Content Doesn't Fit

**DO:** Split into multiple slides; reduce bullets (max 5–6); shorten text; smaller code snippets; "continued" slide; when adding images, move image to new slide or reduce other content first. **DON'T:** Shrink fonts below readable; remove padding; allow scrolling; cram.

### Testing Viewport Fit

Recommend testing at: Desktop 1920×1080, 1440×900, 1280×720; Tablet 1024×768, 768×1024; Mobile 375×667, 414×896; Landscape 667×375, 896×414.

---

## Phase 0: Detect Mode

- **Mode A — New Presentation:** User wants slides from scratch → Phase 1 (Content Discovery).
- **Mode B — PPT Conversion:** User has .ppt/.pptx → Phase 4 (PPT Extraction).
- **Mode C — Existing HTML Enhancement:** Read file, enhance; **always maintain viewport fitting.**

### Mode C: Modification Rules

Before adding content: check current slide against density limits. **Images:** max `min(50vh, 400px)`; if slide already full → split into two slides (e.g. new slide for image). **Text:** max 4–6 bullets or 2 paragraphs per slide; if over → split or continuation slide. After any change: verify `.slide` has `overflow: hidden`, new elements use `clamp()`, new images have viewport max-height, density respected. If modifications cause overflow → **automatically split** and tell user. Test at 1280×720, 768×1024, 375×667.

---

## Solution PPT (解决方案 PPT) — 售前/销售专用

When purpose is **solution deck / 解决方案汇报 / 售前方案 / 投标演示**, use this default outline (10–20 slides): (1) Title (2) Agenda (3) Background & objectives (4) Pain points & challenges (5) Solution overview (6–8) Capabilities / product value (9) Case study (10) Implementation / roadmap (11) Next steps & contact. Adjust as needed; respect content density. **Style:** Prefer **Swiss Modern**, **Electric Studio**, **Dark Botanical**, **Notebook Tabs**. Avoid highly playful styles unless asked.

---

## Phase 1: Content Discovery (New Presentations)

**If AskUserQuestion is available:** Collect in one form. **If not (e.g. Cursor):** Ask the same questions in conversation, in order, and record answers before Phase 2.

### Step 1.1: Context + Images (single form or sequence)

Ask these five in one form (AskUserQuestion) or in sequence:

1. **Purpose:** What is this presentation for? — Solution deck (解决方案PPT) | Pitch deck | Teaching/Tutorial | Conference talk | Internal presentation
2. **Length:** Approximately how many slides? — Short (5–10) | Medium (10–20) | Long (20+)
3. **Content:** Do you have content ready or need help? — I have all content ready | I have rough notes | I have topic only
4. **Images:** No images | ./assets | Other (let user type/paste folder path, e.g. ~/Desktop/screenshots)
5. **Editing:** Do you need to edit text in the browser after generation? — Yes (in-browser edit, auto-save, export) | No

Remember the editing choice — it controls whether Phase 3 includes the edit button (see reference/edit-button-implementation.md).

**Get the content:** If user said "I have all content ready" → ask them to share it (paste text, bullet points, or path to file). If "I have rough notes" or "I have topic only" → help structure an outline, then ask for or draft the slide-by-slide content. You need concrete titles and body content before Phase 2.

### Step 1.2: Image Evaluation (if user provided images)

If "No images" → skip image pipeline; use text + CSS visuals. If folder provided: (1) List image files (2) Read/view each (3) Mark USABLE / NOT USABLE with reason; note content signal, shape, dominant colors (4) Propose slide outline with image assignments (5) Confirm outline via AskUserQuestion or conversation: "Looks good" | "Adjust images" | "Adjust outline". Co-design: usable images shape the outline from the start. Logo in previews: if USABLE logo exists, embed (e.g. base64) in the 3 style previews so user sees their brand in each style.

---

## Phase 2: Style Discovery

**Option A — Guided:** Ask mood (Impressed/Confident | Excited/Energized | Calm/Focused | Inspired/Moved; multiSelect up to 2). Create directory `.claude-design/slide-previews/` if needed. Generate **3 style previews** there (style-a.html, style-b.html, style-c.html): single title slide each, self-contained, ~50–100 lines. Pick 3 presets by mood (e.g. Impressed → Bold Signal, Electric Studio, Dark Botanical). **Never use:** purple gradients on white, Inter/Roboto, standard blue, predictable hero. **Use:** distinctive fonts (Clash Display, Satoshi, Cormorant Garamond, DM Sans), cohesive colors, atmospheric backgrounds, signature animation. Present previews; user picks Style A/B/C or "Mix elements". **Option B — Direct:** Ask "Which preset?" and show the preset list (below or from STYLE_PRESETS.md). User picks by name → skip to Phase 3.

**Presets (see STYLE_PRESETS.md for full list):** Bold Signal | Electric Studio | Creative Voltage | Dark Botanical | Notebook Tabs | Pastel Geometry | Split Pastel | Vintage Editorial | Neon Cyber | Terminal Green | Swiss Modern | Paper & Ink. Mood → preset mapping: Impressed/Confident → Bold Signal, Electric Studio, Dark Botanical; Excited/Energized → Creative Voltage, Neon Cyber, Split Pastel; Calm/Focused → Notebook Tabs, Paper & Ink, Swiss Modern; Inspired/Moved → Dark Botanical, Vintage Editorial, Pastel Geometry.

---

## Phase 3: Generate Presentation

Use content from Phase 1 and style from Phase 2. If no images, generate text-only with CSS visuals. If images: **Image pipeline** — process before HTML. **Operations:** See [reference/image-processing.py](reference/image-processing.py) for `crop_circle`, `resize_max`, `add_padding`. Dependency: `pip install Pillow`. Never repeat same image (except logo on title+closing); add CSS framing (border/glow) when image clashes with style. Save processed images to a new filename (e.g. `logo_round.png`, `screenshot_processed.png`); never overwrite originals. Reference in HTML with relative paths (e.g. `assets/logo_round.png`). **Image CSS:** `.slide-image` max-height min(50vh, 400px); `.screenshot` border+shadow; `.logo` max-height min(30vh, 200px). Adapt border/shadow to style accent. Placement: title = logo centered; feature = screenshot one side, text other; full-bleed or inline as needed.

**File structure:** Single: `presentation.html` + `assets/`. Multiple: `[name].html` + `[name]-assets/`.

**HTML architecture:** Follow [reference/html-architecture.md](reference/html-architecture.md). Include mandatory viewport base CSS, theme variables (clamp() for all typography/spacing), .slide + .slide-content, responsive breakpoints, .reveal + .visible for animations.

**Required JS:** Implement SlidePresentation: keyboard (arrows, space), touch/swipe, mouse wheel; progress bar and navigation dots (click dot to jump to slide); Intersection Observer to add `.visible` when a slide enters the viewport so .reveal animations run. Optional: cursor trail, particles, parallax, tilt, inline editing. **Edit button (only if user opted Yes):** See [reference/edit-button-implementation.md](reference/edit-button-implementation.md). Use JS hover with delay (no CSS ~ sibling); hotzone + E key + click to toggle.

**Code quality:** Clear section comments; semantic HTML; keyboard nav; ARIA where needed; reduced motion. **CSS negation:** Use `calc(-1 * clamp(...))`, never `-clamp()`. See STYLE_PRESETS.md "CSS Gotchas". Viewport: always respect density and overflow rules above.

---

## Phase 4: PPT Conversion

1. **Extract:** Run the logic from [reference/ppt-extract.py](reference/ppt-extract.py): `extract_pptx(user_pptx_path, output_dir)`. Dependency: `pip install python-pptx`. Use an output_dir (e.g. current directory or a new folder) so images are saved to `output_dir/assets/` and the future HTML can use `assets/` as sibling. Returns slides_data (per slide: title, content[], images[], notes).
2. **Confirm:** Present extracted slide list to user; ask to proceed to style selection.
3. **Style:** Phase 2 (Style Discovery) with extracted content in mind.
4. **Generate:** Build the HTML presentation in the **same output_dir** used in step 1 so that `assets/` is next to the .html file. Convert to chosen style; preserve text, images (reference from assets/), slide order, speaker notes (as HTML comments or separate file).

---

## Phase 5: Delivery

1. Delete `.claude-design/slide-previews/` if present.
2. Open presentation in browser (e.g. `open [filename].html`).
3. Summary: file, style, slide count; navigation (arrows, space, scroll, dots); customization (:root, fonts, .reveal). If inline editing: hover top-left or E to edit; Ctrl+S or "Save file".

---

## Style Reference: Effect → Feeling

- **Dramatic/Cinematic:** Slow fades, scale transitions, dark + spotlight, parallax, full-bleed.
- **Techy/Futuristic:** Neon glow, particles, grid, monospace accents, cyan/magenta palette.
- **Playful/Friendly:** Bouncy easing, rounded, pastel/bright, floating animations.
- **Professional/Corporate:** Subtle fast animations (200–300ms), clean sans, navy/slate, minimal decor.
- **Calm/Minimal:** Slow subtle motion, whitespace, muted palette, serif, content-focused.
- **Editorial:** Strong type hierarchy, pull quotes, image-text interplay, serif headline + sans body.

**Animation patterns (entrance, backgrounds, interactive):** See [reference/animation-patterns.md](reference/animation-patterns.md).

---

## Troubleshooting

- **Fonts not loading:** Check Fontshare/Google URL; font names in CSS.
- **Animations not triggering:** Intersection Observer; .visible class.
- **Scroll snap:** scroll-snap-type on html; scroll-snap-align on each .slide.
- **Mobile:** Disable heavy effects at 768px; test touch; reduce particles.
- **Performance:** Use will-change sparingly; prefer transform/opacity; throttle scroll/mousemove.

---

## Related Skills

- **learn** — FORZARA.md for the presentation
- **frontend-design** — Complex interactive pages beyond slides
- **design-and-refine:design-lab** — Component design iteration

---

## Example Flows

**New presentation:** User wants pitch/solution deck → ask purpose, length, content, images, editing → (if images) evaluate, outline, confirm → ask vibe → 3 previews → user picks style → (if images) run Pillow ops → generate HTML → open in browser.

**PPT conversion:** User has .pptx → extract with ppt-extract.py → confirm content → style selection → generate HTML with assets.
