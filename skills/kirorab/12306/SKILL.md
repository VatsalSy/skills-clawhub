---
name: 12306
description: Query China Railway 12306 for train schedules, remaining tickets, and station info. Use when user asks about train/高铁/火车 tickets, schedules, or availability within China.
metadata: {"openclaw":{"emoji":"🚄","requires":{"bins":["node"]}}}
---

# 12306 Train Query

Query train schedules and remaining tickets from China Railway 12306.

## Query Tickets

```bash
node {baseDir}/scripts/query.mjs <from> <to> [-d YYYY-MM-DD] [-t G|D|Z|T|K]
```

### Examples

```bash
# All trains from Beijing to Shanghai tomorrow
node {baseDir}/scripts/query.mjs 北京 上海 -d 2026-02-24

# Only high-speed trains (G)
node {baseDir}/scripts/query.mjs 揭阳 杭州 -d 2026-02-24 -t G

# Multiple types: G and D trains
node {baseDir}/scripts/query.mjs 深圳 长沙 -d 2026-02-25 -t GD

# JSON output
node {baseDir}/scripts/query.mjs 广州 武汉 --json
```

### Options

- `-d, --date <YYYY-MM-DD>`: Travel date (default: today)
- `-t, --type <G|D|Z|T|K>`: Filter train types (combinable, e.g. `GD`)
- `--json`: Output raw JSON

### Output Columns

| Column | Meaning |
|--------|---------|
| 商务/特等 | Business class / Premium |
| 一等座 | First class |
| 二等座 | Second class |
| 软卧/动卧 | Soft sleeper / Bullet sleeper |
| 硬卧 | Hard sleeper |
| 硬座 | Hard seat |
| 无座 | Standing |
| 可买 | ✅ = available, ❌ = sold out |

Values: number = remaining seats, `有` = available (qty unknown), `--` = not applicable

## Station Lookup

```bash
node {baseDir}/scripts/stations.mjs 杭州
node {baseDir}/scripts/stations.mjs 香港西九龙
```

## Notes

- Data comes directly from 12306 official API (no key needed)
- Station data is cached for 7 days in `{baseDir}/data/stations.json`
- Supports city names (resolves to main station) or exact station names
- Works for all train types: G (高铁), D (动车), Z (直达), T (特快), K (快速)
