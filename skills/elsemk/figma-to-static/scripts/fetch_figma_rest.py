#!/usr/bin/env python3
"""Fetch Figma node metadata and export images via REST API.

Usage:
  python3 fetch_figma_rest.py --file-key FILE_KEY --nodes "305:2,304:60" [--scale 2] [--out-dir ./rest-assets] [--token TOKEN]

If --token is not provided, reads FIGMA_TOKEN from environment.
"""
import argparse, json, os, pathlib, urllib.parse, urllib.request

API = "https://api.figma.com/v1"


def req(url, token):
    r = urllib.request.Request(url, headers={"X-Figma-Token": token})
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read())


def download(url, out):
    out.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, out)


def main():
    p = argparse.ArgumentParser(description="Fetch Figma nodes + images via REST API")
    p.add_argument("--file-key", required=True, help="Figma file key from URL")
    p.add_argument("--nodes", required=True, help="Comma-separated node IDs (e.g. 305:2,304:60)")
    p.add_argument("--out-dir", default="./rest-assets")
    p.add_argument("--scale", type=float, default=2)
    p.add_argument("--format", default="png")
    p.add_argument("--token", default=None)
    args = p.parse_args()

    token = args.token or os.environ.get("FIGMA_TOKEN")
    if not token:
        raise SystemExit("ERROR: FIGMA_TOKEN not set. Pass --token or set env var.")

    out = pathlib.Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    nodes = [n.strip() for n in args.nodes.split(",") if n.strip()]
    ids_csv = ",".join(nodes)
    ids_enc = urllib.parse.quote(ids_csv, safe=":,")

    # Fetch node metadata
    nodes_url = f"{API}/files/{args.file_key}/nodes?ids={ids_enc}"
    nodes_data = req(nodes_url, token)
    (out / "nodes.json").write_text(json.dumps(nodes_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # Fetch image export URLs
    img_url = (
        f"{API}/images/{args.file_key}?ids={ids_enc}"
        f"&format={urllib.parse.quote(args.format)}&scale={args.scale}"
    )
    img_data = req(img_url, token)
    (out / "images.json").write_text(json.dumps(img_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # Download images
    images = img_data.get("images", {})
    manifest = []
    for nid in nodes:
        u = images.get(nid)
        safe = nid.replace(":", "-")
        if not u:
            manifest.append({"node": nid, "status": "missing"})
            continue
        f = out / f"node-{safe}.{args.format}"
        try:
            download(u, f)
            manifest.append({"node": nid, "status": "ok", "file": str(f)})
        except Exception as e:
            manifest.append({"node": nid, "status": "failed", "error": str(e)})

    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"DONE: {out}")
    for m in manifest:
        print(f"  {m['node']}: {m['status']}")


if __name__ == "__main__":
    main()
