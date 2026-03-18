---
name: agentimghost
description: AgentImgHost API and MCP server for uploading, listing, and deleting images. Returns direct public CDN URLs.
homepage: https://agent-img.com
metadata:
  {
    "openclaw":
      { "emoji": "🖼️", "requires": { "env": ["AGENTIMGHOST_API_KEY"] }, "primaryEnv": "AGENTIMGHOST_API_KEY" },
  }
---

# SKILLS.md — AgentImgHost Image Upload Guide

This document teaches AI agents, bots, and scripts how to upload images to **AgentImgHost** and use the returned public URL.

---

## Overview

AgentImgHost provides a **REST API** and an **MCP server** for uploading images. After a successful upload, the service returns the **direct public URL** — no intermediate proxying. The image is immediately accessible worldwide via CDN.

---

## Authentication

All API requests require a **Bearer token** in the `Authorization` header.

```
Authorization: Bearer aih_your_token_here
```

You can find your token in the **Account** section of the web dashboard at `https://agent-img.com/account`.

---

## Upload an Image

### Endpoint

```
POST https://agent-img.com/api/upload
```

### Request

| Parameter | Type | Description |
|-----------|------|-------------|
| `file` | multipart/form-data | The image file to upload |

### Response (201 Created)

```json
{
  "url": "https://agent-img.com/a1b2c3def456/7f8e9a0b1c2d.png",
  "id": "7f8e9a0b1c2d",
  "filename": "screenshot.png",
  "size_bytes": 48291,
  "expires_at": null
}
```

| Field | Description |
|-------|-------------|
| `url` | **Direct Cloudflare public URL** — use this in your responses/messages |
| `id` | Unique image ID (UUID hex) |
| `filename` | Original filename |
| `size_bytes` | File size in bytes |
| `expires_at` | ISO 8601 expiry date, or `null` if no expiry |

---

## Examples

### Bash / curl

```bash
curl -X POST https://agent-img.com/api/upload \
  -H "Authorization: Bearer aih_your_token_here" \
  -F "file=@/path/to/image.png"
```

**Response:**
```json
{
  "url": "https://agent-img.com/a1b2c3/uuid.png",
  "id": "uuid",
  "filename": "image.png",
  "size_bytes": 12345,
  "expires_at": null
}
```

### Python

```python
import httpx

TOKEN = "aih_your_token_here"
API_URL = "https://agent-img.com/api/upload"

def upload_image(path: str) -> str:
    """Upload an image file and return its public URL."""
    with open(path, "rb") as f:
        response = httpx.post(
            API_URL,
            headers={"Authorization": f"Bearer {TOKEN}"},
            files={"file": (path.split("/")[-1], f)},
        )
    response.raise_for_status()
    return response.json()["url"]

url = upload_image("screenshot.png")
print(f"Image available at: {url}")
```

### Python (bytes / in-memory)

```python
import httpx

TOKEN = "aih_your_token_here"

def upload_bytes(data: bytes, filename: str = "image.png") -> str:
    response = httpx.post(
        "https://agent-img.com/api/upload",
        headers={"Authorization": f"Bearer {TOKEN}"},
        files={"file": (filename, data, "image/png")},
    )
    response.raise_for_status()
    return response.json()["url"]
```

### Node.js / JavaScript

```javascript
const FormData = require('form-data');
const fs = require('fs');
const fetch = require('node-fetch');

async function uploadImage(filePath) {
  const form = new FormData();
  form.append('file', fs.createReadStream(filePath));

  const response = await fetch('https://agent-img.com/api/upload', {
    method: 'POST',
    headers: {
      Authorization: 'Bearer aih_your_token_here',
      ...form.getHeaders(),
    },
    body: form,
  });

  const data = await response.json();
  return data.url;
}
```

---

## Resizing Images Before Upload

If your image exceeds the file-size limit for your plan (Free: 1 MB, Pro: 2 MB, Business: 5 MB), resize it before uploading. Below is a recommended workflow.

### Workflow

1. **Get the image** — use an existing file, or generate/download one.
2. **Check the file size** — it must be under your plan's limit.
3. **If too large, resize it** using the commands below.
4. **Upload** the resized image.

### macOS (built-in `sips`)

```bash
# Scale the longest edge to 1600px (preserves aspect ratio)
sips -Z 1600 /path/to/image.png

# Check the new file size
ls -lh /path/to/image.png

# Upload
curl -s -X POST https://agent-img.com/api/upload \
  -H "Authorization: Bearer aih_your_token_here" \
  -F "file=@/path/to/image.png"
```

### Linux (ImageMagick `convert` / `magick`)

```bash
# Scale the longest edge to 1600px (preserves aspect ratio)
convert /path/to/image.png -resize 1600x1600 /path/to/image.png
# or with ImageMagick 7+
magick /path/to/image.png -resize 1600x1600 /path/to/image.png

# Check the new file size
ls -lh /path/to/image.png

# Upload
curl -s -X POST https://agent-img.com/api/upload \
  -H "Authorization: Bearer aih_your_token_here" \
  -F "file=@/path/to/image.png"
```

### Reducing quality (JPEG)

If resizing dimensions alone isn't enough, reduce JPEG quality:

```bash
# macOS — lower quality to 80%
sips -s formatOptions 80 /path/to/image.jpg

# Linux (ImageMagick)
convert /path/to/image.jpg -quality 80 /path/to/image.jpg
```

### Converting PNG → JPEG for smaller size

PNG files are often much larger than JPEG. Convert when transparency isn't needed:

```bash
# macOS
sips -s format jpeg /path/to/image.png --out /path/to/image.jpg

# Linux (ImageMagick)
convert /path/to/image.png -quality 85 /path/to/image.jpg
```

### One-liner: resize + upload

```bash
# macOS — resize to 1600px max, then upload in one line
sips -Z 1600 /tmp/shot.png && curl -s -X POST https://agent-img.com/api/upload \
  -H "Authorization: Bearer aih_your_token_here" \
  -F "file=@/tmp/shot.png"

# Linux — same with ImageMagick
convert /tmp/shot.png -resize 1600x1600 /tmp/shot.png && curl -s -X POST https://agent-img.com/api/upload \
  -H "Authorization: Bearer aih_your_token_here" \
  -F "file=@/tmp/shot.png"
```

> **Tip:** Start with 1600px max dimension. If still over the limit, try 1200px or 800px, or reduce JPEG quality to 70–80%.

---

## Delete an Image

```bash
curl -X DELETE https://agent-img.com/api/images/{image_id} \
  -H "Authorization: Bearer aih_your_token_here"
```

**Response:**
```json
{ "deleted": "7f8e9a0b1c2d" }
```

---

## Error Codes

| Status | Meaning |
|--------|---------|
| `401` | Invalid or missing API token |
| `413` | File too large for your plan |
| `415` | Unsupported file type (must be an image) |
| `429` | Image limit reached and circular overwrite is disabled |
| `500` | Server error — try again |

---

## Supported Image Formats

`JPEG`, `PNG`, `GIF`, `WebP`, `AVIF`, `SVG`, `BMP`, `TIFF`

---

## Plan Limits

| Plan | Max Images | Max File Size | Price |
|------|-----------|---------------|-------|
| Free | 100 | 1 MB | Free |
| Pro | 1,000 | 2 MB | $1/month |
| Business | 10,000 | 5 MB | $5/month |
| Custom | Unlimited | Custom | Contact us |

Manage your plan at `https://agent-img.com/account`.

---

## Circular Overwrite

By default, when you reach your image limit, the **oldest image is automatically deleted** to make room for the new upload. You can disable this in **Settings** (`https://agent-img.com/config`) to get a `429` error instead.

---

## URL Structure

All image URLs follow this pattern:

```
https://agent-img.com/{user_folder}/{image_uuid}.{ext}
```

- `user_folder` — your unique R2 folder (UUID hex, assigned at registration)
- `image_uuid` — UUID hex assigned to each upload
- `ext` — file extension based on content type

URLs are **permanent** while your plan is active. After plan cancellation, images are retained for the grace period defined by your plan before being deleted.

---

## MCP Server

AgentImgHost also exposes an **MCP (Model Context Protocol)** server, allowing AI agents and tools that support MCP to upload, list, and delete images natively.

### Endpoint

```
https://agent-img.com/mcp/
```

Transport: **Streamable HTTP** (default FastMCP transport).

### Authentication

Use the same API key as the REST API — pass it as a **Bearer token**. MCP clients typically accept this in their configuration.

### Available Tools

| Tool | Description |
|------|-------------|
| `upload_image` | Upload a base64-encoded image and get back its public URL |
| `list_images` | List your uploaded images (with pagination) |
| `delete_image` | Delete an image by its ID |
| `get_account_info` | Get your plan, limits, and current usage |

### MCP Client Configuration

Add this to your MCP client config (e.g. `claude_desktop_config.json`, Cursor settings, etc.):

```json
{
  "mcpServers": {
    "agentimghost": {
      "url": "https://agent-img.com/mcp/",
      "headers": {
        "Authorization": "Bearer aih_your_token_here"
      }
    }
  }
}
```

### Tool: `upload_image`

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `image_data` | string | Base64-encoded image file content |
| `filename` | string | Filename with extension (e.g. `"screenshot.png"`) |

**Returns:**
```json
{
  "url": "https://agent-img.com/a1b2c3/7f8e9a0b.png",
  "id": "7f8e9a0b1c2d3e4f",
  "filename": "screenshot.png",
  "size_bytes": 48291,
  "expires_at": null
}
```

### Tool: `list_images`

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | int | 50 | Max images to return (1–200) |

**Returns:**
```json
{
  "total": 42,
  "returned": 42,
  "images": [
    {
      "id": "7f8e9a0b1c2d3e4f",
      "url": "https://agent-img.com/a1b2c3/7f8e9a0b.png",
      "filename": "screenshot.png",
      "size_bytes": 48291,
      "uploaded_at": "2025-03-15T10:30:00+00:00",
      "expires_at": null
    }
  ]
}
```

### Tool: `delete_image`

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `image_id` | string | The UUID of the image to delete |

**Returns:**
```json
{ "deleted": "7f8e9a0b1c2d3e4f", "url": "https://agent-img.com/a1b2c3/7f8e9a0b.png" }
```

### Tool: `get_account_info`

No parameters. Returns your plan, limits, and usage:
```json
{
  "plan": "Pro",
  "max_images": 1000,
  "max_file_size_mb": 2.0,
  "retention_days": "unlimited",
  "total_images": 42,
  "images_today": 5,
  "circular_overwrite": true
}
```
