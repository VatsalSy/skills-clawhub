#!/usr/bin/env python3
"""Visual diff with region heatmap: compare rendered screenshot against target.

Usage:
  python3 visual_diff.py --current current.png --target design-main.png [--diff diff.png] [--regions 5]

Outputs:
  - MAE and similarity percentage
  - Diff image with region grid heatmap showing per-region error
"""
import argparse
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description="Compare images with region heatmap")
    p.add_argument("--current", required=True)
    p.add_argument("--target", required=True)
    p.add_argument("--diff", default="diff.png")
    p.add_argument("--regions", type=int, default=5, help="Grid divisions (NxN)")
    p.add_argument("--threshold", type=float, default=30.0, help="MAE threshold to flag a region as 'bad'")
    args = p.parse_args()

    from PIL import Image, ImageChops, ImageStat, ImageDraw, ImageFont

    cur = Image.open(args.current).convert("RGB")
    tgt = Image.open(args.target).convert("RGB").resize(cur.size)
    diff = ImageChops.difference(cur, tgt)

    # Global stats
    stat = ImageStat.Stat(diff)
    mae = sum(stat.mean) / 3
    sim = max(0, 100 - mae / 255 * 100)

    # Region heatmap
    n = args.regions
    rw, rh = cur.width // n, cur.height // n
    overlay = Image.new("RGBA", cur.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    bad_regions = []

    for row in range(n):
        for col in range(n):
            box = (col * rw, row * rh, (col + 1) * rw, (row + 1) * rh)
            region = diff.crop(box)
            rstat = ImageStat.Stat(region)
            rmae = sum(rstat.mean) / 3
            pct = min(rmae / 255, 1.0)

            # Color: green (good) → yellow → red (bad)
            if pct < 0.5:
                r_val = int(255 * pct * 2)
                g_val = 255
            else:
                r_val = 255
                g_val = int(255 * (1 - pct) * 2)
            alpha = int(40 + pct * 100)

            draw.rectangle(box, fill=(r_val, g_val, 0, alpha))
            draw.rectangle(box, outline=(255, 255, 255, 80))

            if rmae > args.threshold:
                bad_regions.append({"row": row, "col": col, "mae": round(rmae, 2), "box": box})

    # Composite diff with overlay
    diff_rgba = diff.convert("RGBA")
    composite = Image.alpha_composite(diff_rgba, overlay).convert("RGB")

    # Draw labels on bad regions
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except Exception:
        font = ImageFont.load_default()

    for br in bad_regions:
        x, y = br["box"][0] + 4, br["box"][1] + 4
        draw2 = ImageDraw.Draw(composite)
        draw2.rectangle([x - 2, y - 2, x + 80, y + 18], fill=(0, 0, 0, 180))
        draw2.text((x, y), f"MAE {br['mae']}", fill=(255, 80, 80), font=font)

    # Draw grid
    draw3 = ImageDraw.Draw(composite)
    for i in range(1, n):
        draw3.line([(i * rw, 0), (i * rw, cur.height)], fill=(255, 255, 255, 60), width=1)
        draw3.line([(0, i * rh), (cur.width, i * rh)], fill=(255, 255, 255, 60), width=1)

    Path(args.diff).parent.mkdir(parents=True, exist_ok=True)
    composite.save(args.diff)

    print(f"Global MAE: {mae:.2f}")
    print(f"Similarity: {sim:.2f}%")
    print(f"Regions: {n}x{n}, threshold: {args.threshold}")
    print(f"Bad regions ({len(bad_regions)}):")
    for br in bad_regions:
        print(f"  Row {br['row']}, Col {br['col']}: MAE {br['mae']}")
    print(f"Diff saved: {args.diff}")


if __name__ == "__main__":
    main()
