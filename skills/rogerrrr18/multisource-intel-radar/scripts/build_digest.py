#!/usr/bin/env python3
import argparse
import datetime as dt
import re
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime


def read_feeds(path):
    feeds = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '\t' not in line:
                continue
            title, url = line.split('\t', 1)
            feeds.append((title, url))
    return feeds


def extract_items(xml_text):
    items = []
    try:
        root = ET.fromstring(xml_text)
    except Exception:
        return items

    # RSS
    for it in root.findall('.//item'):
        title = (it.findtext('title') or '').strip()
        link = (it.findtext('link') or '').strip()
        desc = (it.findtext('description') or '').strip()
        pub = (it.findtext('pubDate') or '').strip()
        items.append((title, link, desc, pub))

    # Atom
    for it in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = (it.findtext('{http://www.w3.org/2005/Atom}title') or '').strip()
        link_el = it.find('{http://www.w3.org/2005/Atom}link')
        link = (link_el.attrib.get('href') if link_el is not None else '') or ''
        desc = (it.findtext('{http://www.w3.org/2005/Atom}summary') or it.findtext('{http://www.w3.org/2005/Atom}content') or '').strip()
        pub = (it.findtext('{http://www.w3.org/2005/Atom}updated') or it.findtext('{http://www.w3.org/2005/Atom}published') or '').strip()
        items.append((title, link, desc, pub))

    return items


def parse_dt(s):
    if not s:
        return None
    try:
        return parsedate_to_datetime(s)
    except Exception:
        pass
    try:
        return dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
    except Exception:
        return None


def score(text, keywords):
    t = text.lower()
    k_hits = sum(1 for k in keywords if k.lower() in t)
    if k_hits == 0:
        return 0
    rel = min(40, k_hits * 15)
    actionable = 20 if any(x in t for x in ['how', '模板', '步骤', 'framework', 'playbook', 'case', 'strategy']) else 8
    novelty = 15 if any(x in t for x in ['new', '首次', '发布', '开源', '融资', '增长']) else 6
    evidence = 10 if any(x in t for x in ['data', '数据', '%', 'million', '亿', '报告']) else 4
    return rel + actionable + novelty + evidence


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--feeds', required=True)
    ap.add_argument('--keywords', default='创业,AI,增长,金融')
    ap.add_argument('--hours', type=int, default=48)
    ap.add_argument('--limit', type=int, default=10)
    ap.add_argument('--max-feeds', type=int, default=15)
    args = ap.parse_args()

    keywords = [k.strip() for k in args.keywords.split(',') if k.strip()]
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=args.hours)

    candidates = []
    for src_title, url in read_feeds(args.feeds)[: args.max_feeds]:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=12) as r:
                xml_text = r.read().decode('utf-8', errors='ignore')
        except Exception:
            continue

        for title, link, desc, pub in extract_items(xml_text):
            text = f"{title} {desc}"
            sc = score(text, keywords)
            if sc <= 0:
                continue
            pub_dt = parse_dt(pub)
            if pub_dt and pub_dt.tzinfo is None:
                pub_dt = pub_dt.replace(tzinfo=dt.timezone.utc)
            if pub_dt and pub_dt < cutoff:
                continue
            candidates.append({
                'score': sc,
                'source': src_title,
                'title': title[:160],
                'link': link,
            })

    candidates.sort(key=lambda x: x['score'], reverse=True)
    picked = candidates[: args.limit]

    print('=== TOP SIGNALS ===')
    for i, c in enumerate(picked, 1):
        print(f"{i}. [{c['score']}] {c['title']}\n   - {c['source']}\n   - {c['link']}")


if __name__ == '__main__':
    main()
