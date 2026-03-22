#!/usr/bin/env python3
"""
Decide whether a timed status update is due for a task.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"
CONFIG_PATH = ROOT / "config" / "defaults.json"


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text())


def parse_ts(raw: str | None):
    if not raw:
        return None
    return datetime.fromisoformat(raw.replace('Z', '+00:00'))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('task_id')
    args = p.parse_args()

    defaults = load_json(CONFIG_PATH, {})
    task = load_json(STATE_DIR / f"{args.task_id}.json", None)
    if not task:
        raise SystemExit(f"task not found: {args.task_id}")

    interval = int(task.get('status_update_interval_seconds') or defaults.get('reporting', {}).get('status_update_interval_seconds', 300))
    last = parse_ts(task.get('last_status_update_at'))
    now = datetime.now(timezone.utc)
    if last is None:
        print(json.dumps({"due": True, "reason": "never_reported", "interval_seconds": interval}))
        return 0
    elapsed = (now - last).total_seconds()
    print(json.dumps({
        "due": elapsed >= interval,
        "reason": "interval_elapsed" if elapsed >= interval else "not_due",
        "elapsed_seconds": round(elapsed),
        "interval_seconds": interval
    }))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
