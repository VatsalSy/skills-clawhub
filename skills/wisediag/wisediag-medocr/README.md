---
name: wiseocr
description: "PDF OCR — Convert PDF to Markdown via WiseDiag cloud API (requires WISEDIAG_API_KEY). Files are uploaded to WiseDiag servers for processing. Supports table recognition, multi-column layouts, and high-accuracy text extraction."
registry:
  homepage: https://github.com/wisediag/WiseOCR
  author: wisediag
  credentials:
    required: true
    env_vars:
      - WISEDIAG_API_KEY
---

# ⚠️ Privacy Warning

**IMPORTANT - READ BEFORE INSTALLING:**

This tool **uploads your files to WiseDiag's cloud servers** for OCR processing.

**Do NOT use with sensitive or confidential documents** unless:
- You trust WiseDiag's data handling policies
- You accept that file contents will be transmitted and processed remotely

**For sensitive documents, use offline/local OCR tools instead.**

---

# WiseOCR (OpenClaw Skill, powered by WiseDiag)

A high-accuracy OCR tool that converts PDF files into Markdown format.

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)

## Features

- PDF to Markdown conversion with high accuracy
- Table recognition and structured formatting
- Multi-column layout support
- Automatic file saving with input filename

## Installation

```bash
pip install -r requirements.txt
```

## 🔑 API Key Setup (Required)

**Get your API key:**
👉 https://console.wisediag.com/apiKeyManage

```bash
# Temporary (current terminal session)
export WISEDIAG_API_KEY=your_api_key_here

# Permanent (add to ~/.zshrc or ~/.bashrc)
echo 'export WISEDIAG_API_KEY=your_api_key_here' >> ~/.zshrc
source ~/.zshrc
```

## CLI Usage

**Use the provided script to process files** — it handles authentication, upload, retry logic, and output saving.

```bash
cd scripts

# Basic usage
python3 wiseocr.py -i "/path/to/uploaded_file.pdf"

# If the input file has been copied or renamed, use -n to preserve the original filename
python3 wiseocr.py -i "/tmp/ocr_input.pdf" -n "my_report"

# Specify output directory
python3 wiseocr.py -i input.pdf -o ~/my_ocr_results

# Higher quality rendering
python3 wiseocr.py -i input.pdf --dpi 300
```

The Markdown result is saved to `~/.openclaw/workspace/WiseOCR/{name}.md` automatically. If `-n` is provided, the output uses that name; otherwise it falls back to the input filename. No additional saving is needed.

## Arguments

| Flag | Description |
|------|-------------|
| `-i, --input` | Input PDF file path (required) |
| `-n, --name` | Original filename without extension for output (recommended when input file is renamed/copied) |
| `-o, --output` | Output directory (default: ~/.openclaw/workspace/WiseOCR) |
| `--dpi` | PDF rendering DPI, 72-600 (default: 200) |

## Troubleshooting

**"WISEDIAG_API_KEY is not set" error:**
Make sure you've set the environment variable correctly. Run `echo $WISEDIAG_API_KEY` to check.

**"Authentication failed" error:**
Your API key may be invalid or expired. Visit https://console.wisediag.com/apiKeyManage to check or regenerate your key.

## Data Privacy

Files are sent to WiseDiag's OCR API (`https://openapi.wisediag.com/v1/ocr/pdf`) for processing and are not permanently stored. Results are returned directly to you.

**Service documentation:** https://openapi.wisediag.com/docs

## License

MIT
