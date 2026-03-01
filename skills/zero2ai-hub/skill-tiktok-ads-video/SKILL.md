---
name: skill-tiktok-ads-video
version: 2.0.0
description: Generate TikTok-style short-form ad videos with animated pill captions. Takes a base MP4 (Veo/Runway/Kling), overlays animated captions with fade in/out, mixes background audio. Built-in product presets — no captions JSON file needed. Use for TikTok ads, Reels, YouTube Shorts product videos.
metadata:
  openclaw:
    requires: { bins: ["uv"] }
---

# skill-tiktok-ads-video v2.0.0

Animated pill-style caption overlays for short-form video. No Premiere, no CapCut — pure Python. v2 ships with built-in product presets — no more manual captions JSON.

## Usage (v2 — product presets)

```bash
uv run --with moviepy --with pillow scripts/overlay.py \
  --video base.mp4 \
  --output final.mp4 \
  --product rain_cloud \
  --style subtitle_talk
```

### Products
- `rain_cloud` — Rain Cloud Humidifier
- `hydro_bottle` — Hydrogen Water Bottle
- `mini_cam` — Mini Clip Camera

### Styles
- `phrase_slam` — Bold full-screen phrase drops
- `subtitle_talk` — Conversational subtitle-style captions
- `random` — Randomly picks a style

### Optional audio
```bash
  --audio music.mp3 \
  --audio-start 8 \
  --audio-vol 0.5
```

No `--audio` keeps the original video audio.

## Custom fonts

```bash
--font-black /path/to/Montserrat-Black.ttf \
--font-bold  /path/to/Montserrat-Bold.ttf
```

Falls back to Montserrat from `~/.local/share/fonts/` if not specified.

## Legacy usage (v1 — manual captions JSON)

Still supported for backward compatibility:

```bash
uv run --with moviepy --with pillow scripts/overlay.py \
  --video base.mp4 \
  --output final.mp4 \
  --captions scripts/example_captions.json
```

## PIL textbbox fix

PIL's `textbbox((0,0), text, font)` returns `(x0, y0, x1, y1)` where `y0` is a non-zero offset (typically 7–15px depending on font size). Drawing text at `(x, y)` without compensating for this offset causes text to appear below the pill's visual center.

**Fix implemented in `pill()`:**
```python
bb    = draw.textbbox((0, 0), text, font=font)
x_off, y_off = bb[0], bb[1]
vis_w = bb[2] - bb[0]   # actual visual width
vis_h = bb[3] - bb[1]   # actual visual height

# Compensate offsets when drawing text
tx = cx - vis_w // 2 - x_off
ty = y - y_off
draw.text((tx, ty), text, font=font, fill=fg)
```

## Emoji note

NotoColorEmoji.ttf fails with PIL at arbitrary sizes (bitmap font with limited supported sizes). Use text alternatives (`"Free delivery"` instead of `"Free delivery 🚚"`) for reliable rendering.
