---
name: bnbot
description: Control Twitter/X via BNBOT Chrome Extension - scrape tweets, post, reply, navigate, and analyze accounts.
version: 0.1.0
homepage: https://github.com/jackleeio/bnbot-mcp-server
metadata:
  openclaw:
    emoji: "\U0001F916"
    os: [darwin, linux, windows]
    requires:
      bins: [bnbot-mcp-server]
    install:
      - id: node
        kind: node
        package: bnbot-mcp-server
        bins: [bnbot-mcp-server]
        label: Install bnbot-mcp-server (npm)
---

# BNBOT - Control Twitter/X with AI

BNBOT lets you control Twitter/X directly from your AI assistant through the BNBOT Chrome Extension.

## Prerequisites

1. Install the [BNBOT Chrome Extension](https://chromewebstore.google.com/detail/bnbot)
2. Open Twitter/X in Chrome
3. In the BNBOT sidebar, go to **Settings** and enable the **OpenClaw** toggle

## How It Works

This skill uses the `bnbot-mcp-server` MCP server to communicate with the BNBOT Chrome Extension via WebSocket. The extension executes actions directly on the Twitter/X page.

```
OpenClaw → MCP Server (stdio) → WebSocket (localhost:18900) → Chrome Extension → Twitter/X
```

## Available Tools

### Scraping

- `scrape_timeline` - Scrape tweets from the timeline (params: `limit`, `scrollAttempts`)
- `scrape_bookmarks` - Scrape bookmarked tweets (params: `limit`)
- `scrape_search_results` - Search and scrape results (params: `query`, `limit`)
- `scrape_current_view` - Scrape currently visible tweets
- `account_analytics` - Get account analytics (params: `startDate`, `endDate` in YYYY-MM-DD)

### Posting

- `post_tweet` - Post a tweet (params: `text`, optional `images` array of URLs)
- `post_thread` - Post a thread (params: `tweets` array of `{text, images?}`)
- `submit_reply` - Reply to a tweet (params: `text`, optional `tweetUrl`, optional `image`)

### Navigation

- `navigate_to_tweet` - Go to a specific tweet (params: `tweetUrl`)
- `navigate_to_search` - Go to search page (params: optional `query`)
- `navigate_to_bookmarks` - Go to bookmarks
- `navigate_to_notifications` - Go to notifications
- `return_to_timeline` - Go back to home timeline

### Status

- `get_extension_status` - Check if extension is connected
- `get_current_page_info` - Get info about the current Twitter/X page

## Usage Examples

- "Scrape my Twitter timeline and summarize the top topics"
- "Search for tweets about AI agents and collect the most engaging ones"
- "Post a tweet saying: Just discovered an amazing AI tool!"
- "Navigate to my bookmarks and export them"
- "Go to @elonmusk's latest tweet and reply with a thoughtful comment"
- "Post a thread about the top 5 productivity tips"
