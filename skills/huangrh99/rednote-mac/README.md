# rednote-mac

Control the RedNote (Xiaohongshu / 小红书) Mac desktop app via macOS Accessibility API.

## Why rednote-mac?

Headless browser tools (like xiaohongshu-mcp) can't access:
- **Direct Messages** — requires native App session
- **Comment replies** — needs login state + App interaction  
- **Video comment lists** — AX API exposes full comment data in video posts
- **Author profile stats** — readable directly from the profile page

This skill talks directly to the App using macOS Accessibility API, bypassing all of that.

## Requirements

| Requirement | Notes |
|-------------|-------|
| macOS + RedNote App | [rednote.app](https://www.rednote.app) |
| Terminal accessibility permission | System Settings → Privacy & Security → Accessibility → enable Terminal |
| RedNote App visible on screen | Not minimized, screen not locked |
| Python + uv | For running the controller |

## Install (OpenClaw Plugin)

```bash
# 1. Sync dependencies
cd ~/.agents/skills/rednote-mac
uv sync

# 2. Register as OpenClaw plugin
ln -sf ~/.agents/skills/rednote-mac ~/.openclaw/extensions/rednote-mac

# 3. Enable plugin tools
openclaw config set tools.allow '["rednote-mac"]'

# 4. Restart gateway
openclaw gateway restart

# Verify
openclaw plugins list | grep rednote-mac
```

Or use the one-liner:
```bash
bash install.sh
```

## Install (Claude Desktop / Cursor)

```json
{
  "mcpServers": {
    "rednote-mac": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/rednote-mac", "python", "server.py"]
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `xhs_screenshot` | Capture current screen |
| `xhs_navigate` | Switch bottom tab: `home` / `messages` / `profile` |
| `xhs_navigate_top` | Switch top tab: `follow` / `discover` / `video` |
| `xhs_back` | Go back one page |
| `xhs_search` | Search keyword → results page |
| `xhs_scroll_feed` | Scroll feed (`direction`, `times`) |
| `xhs_open_note` | Open note by grid position (`col`, `row`) |
| `xhs_like` | Like current note |
| `xhs_collect` | Collect/save current note |
| `xhs_get_note_url` | Get share URL of current note |
| `xhs_follow_author` | Follow current note's author |
| `xhs_open_comments` | Open comment section |
| `xhs_scroll_comments` | Scroll comments |
| `xhs_get_comments` | Get comment list → `[{index, author, cx, cy}]` |
| `xhs_post_comment` | Post a comment |
| `xhs_reply_to_comment` | Reply to a comment (`index`, `text`) |
| `xhs_delete_comment` | Delete own comment (`index`) — irreversible |
| `xhs_open_dm` | Open DM conversation by index |
| `xhs_send_dm` | Send DM in current conversation |
| `xhs_get_author_stats` | Get profile stats (following / followers / likes / bio) |

## Known Limitations

**Image/text posts — comment text not readable via AX**
RedNote renders comments using Metal/Canvas, bypassing macOS Accessibility API entirely. Workaround: `xhs_screenshot()` + image analysis.

**Video posts** have no such limitation — comment panel is fully AX-accessible.

**App must stay visible** — minimize or lock screen and all mouse events fail.

## Architecture

```
xhs_controller.py    Core AX control logic (Python + atomacos)
index.ts             OpenClaw Plugin entry (registers 20 tools)
server.py            Standard MCP server (Claude Desktop / Cursor)
openclaw.plugin.json Plugin manifest
docs/                Reference docs (load on demand)
install.sh           One-command setup
```

## How it works

Uses `atomacos` (Python bindings for macOS Accessibility API) + `cliclick` for mouse events + `CGEventPost` for keyboard + scroll. No browser, no HTTP API — direct App control.
