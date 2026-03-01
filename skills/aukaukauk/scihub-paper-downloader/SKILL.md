---
name: scihub-paper-downloader
description: "Download academic papers from Sci-Hub. Given a DOI, returns the PDF download URL."
metadata: { "openclaw": { "emoji": "📚", "requires": { "bins": ["python3"] } } }
allowed-tools: ["exec"]
---

# Sci-Hub Paper Downloader

Get PDF download URLs from Sci-Hub by DOI. Tries official mirrors (sci-hub.se, sci-hub.st, sci-hub.ru) automatically.

## Usage

```
python3 {baseDir}/scihub-paper-downloader.py <DOI>
```

Output JSON:

```json
{"doi": "10.xxx", "pdf_url": "https://...", "mirror": "https://sci-hub.st", "status": "found"}
```

`status` is `found` when a PDF URL is available, `not_found` when all mirrors fail.

## Downloading the PDF

This skill only returns the URL. Use curl to download:

```
curl -L -o paper.pdf "<pdf_url>"
```

## Finding Papers

To find a paper's DOI before using this skill:

- **web_search** — general queries, fast
- **Google Scholar** (`site:scholar.google.com`) — comprehensive academic search
- **Semantic Scholar** (`site:semanticscholar.org`) — citation graph, related papers
- **arXiv** (`site:arxiv.org`) — preprints (often free, no Sci-Hub needed)
- **PubMed** (`site:pubmed.ncbi.nlm.nih.gov`) — biomedical literature
