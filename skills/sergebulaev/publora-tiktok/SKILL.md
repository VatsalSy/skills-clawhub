---
name: publora-tiktok
description: >
  Post or schedule video content to TikTok using the Publora API. Use this skill
  when the user wants to publish or schedule TikTok videos via Publora.
---

# Publora — TikTok

Post and schedule TikTok video content via the Publora API.

> **Prerequisite:** Install the `publora` core skill for auth setup and getting platform IDs.

## Get Your TikTok Platform ID

```bash
GET https://api.publora.com/api/v1/platform-connections
# Look for entries like "tiktok-99887766"
```

## Post a TikTok Video

TikTok requires a video upload. Always attach a video to TikTok posts.

```javascript
const API_KEY = 'sk_YOUR_KEY';
const BASE_URL = 'https://api.publora.com/api/v1';
const headers = { 'Content-Type': 'application/json', 'x-publora-key': API_KEY };

// Step 1: Create post with TikTok settings
const postRes = await fetch(`${BASE_URL}/create-post`, {
  method: 'POST', headers,
  body: JSON.stringify({
    content: 'How we built our startup in 60 seconds #startup #tech #coding',
    platforms: ['tiktok-99887766'],
    platformSettings: {
      tiktok: {
        viewerSetting: 'PUBLIC_TO_EVERYONE',
        allowComments: true,
        allowDuet: true,
        allowStitch: true,
        commercialContent: false,
        brandOrganic: false,
        brandedContent: false
      }
    }
  })
});
const { postGroupId } = await postRes.json();

// Step 2: Get upload URL
const uploadRes = await fetch(`${BASE_URL}/get-upload-url`, {
  method: 'POST', headers,
  body: JSON.stringify({
    fileName: 'video.mp4', contentType: 'video/mp4',
    type: 'video', postGroupId
  })
});
const { uploadUrl } = await uploadRes.json();

// Step 3: Upload video (use fs/buffer in Node.js)
const fs = require('fs');
const axios = require('axios');
const videoBuffer = fs.readFileSync('./video.mp4');
await axios.put(uploadUrl, videoBuffer, {
  headers: { 'Content-Type': 'video/mp4' },
  maxContentLength: 512 * 1024 * 1024
});
```

## Schedule a TikTok Post

```javascript
body: JSON.stringify({
  content: 'Day in the life of a founder 📱',
  platforms: ['tiktok-99887766'],
  scheduledTime: '2026-03-16T18:00:00.000Z',
  platformSettings: {
    tiktok: {
      viewerSetting: 'PUBLIC_TO_EVERYONE',
      allowComments: true,
      allowDuet: false,
      allowStitch: false,
      commercialContent: false,
      brandOrganic: false,
      brandedContent: false
    }
  }
})
```

## TikTok Platform Settings Reference

| Setting | Type | Description |
|---------|------|-------------|
| `viewerSetting` | string | `PUBLIC_TO_EVERYONE`, `MUTUAL_FOLLOW_FRIENDS`, `SELF_ONLY` |
| `allowComments` | boolean | Allow viewer comments |
| `allowDuet` | boolean | Allow Duet feature |
| `allowStitch` | boolean | Allow Stitch feature |
| `commercialContent` | boolean | Mark as commercial/ad content |
| `brandOrganic` | boolean | Organic brand content |
| `brandedContent` | boolean | Paid brand partnership |

## Tips for TikTok

- **Video required** — text-only posts don't work on TikTok
- **Vertical 9:16** format only — anything else gets cropped
- **Max size:** 512 MB
- **Hook in first 1–3 seconds** — critical for watch time / algorithm
- **Best lengths:** 7–15 seconds for viral, 60+ for educational
- **Best times:** 6–10 PM on weekdays; 9 AM–11 AM on weekends
- **Trending sounds** dramatically increase reach when applicable
