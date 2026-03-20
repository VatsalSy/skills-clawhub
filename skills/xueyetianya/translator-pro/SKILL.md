---
version: "4.0.0"
name: translator-pro
description: "Translate text via LibreTranslate API with offline dictionary fallback. Use when translating content, detecting languages, managing glossaries, or setting up i18n."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
---

# translator-pro

Translation and localization toolkit — translate text via LibreTranslate free API with built-in English-Chinese dictionary fallback, detect languages, manage personal dictionaries, access domain glossaries, and scaffold i18n projects.

## Commands

### `translate`

Translate text using LibreTranslate API. Falls back to built-in dictionary when API is unavailable.

```bash
scripts/script.sh translate "hello world" auto zh
scripts/script.sh translate "你好" auto en
```

### `detect`

Detect the language of text using Unicode character range analysis.

```bash
scripts/script.sh detect "这是中文测试"
scripts/script.sh detect "Hello World"
```

### `batch`

Translate a text file line by line via LibreTranslate API.

```bash
scripts/script.sh batch readme.txt auto zh
```

### `compare`

Translate text into two languages side by side for comparison.

```bash
scripts/script.sh compare "Thank you" zh ja
```

### `lookup`

Look up a word in personal dictionary and built-in English-Chinese dictionary.

```bash
scripts/script.sh lookup "computer"
scripts/script.sh lookup "数据"
```

### `add`

Add a word and its translation to your personal dictionary.

```bash
scripts/script.sh add "kubernetes" "容器编排平台"
```

### `dict`

Manage personal dictionary — list all entries or export as CSV.

```bash
scripts/script.sh dict list
scripts/script.sh dict export
```

### `romanize`

Convert text to ASCII approximation using Unicode decomposition and script tagging.

```bash
scripts/script.sh romanize "café résumé"
scripts/script.sh romanize "你好世界"
```

### `count`

Count characters, words, sentences, and estimate reading time.

```bash
scripts/script.sh count "This is a sample text for counting."
```

### `diff`

Compare two translation files and show differences.

```bash
scripts/script.sh diff en/messages.json zh/messages.json
```

### `glossary`

Browse domain-specific terminology glossaries (tech, business, medical).

```bash
scripts/script.sh glossary tech
scripts/script.sh glossary business
```

### `i18n-init`

Create an internationalization directory structure for a project.

```bash
scripts/script.sh i18n-init myapp en,zh,ja
```

### `i18n-extract`

Extract translatable strings from source code files.

```bash
scripts/script.sh i18n-extract src/app.js
```

### `i18n-check`

Check i18n directories for missing translations compared to base language.

```bash
scripts/script.sh i18n-check i18n/
```

### `i18n-merge`

Merge new translations into an existing base translation file.

```bash
scripts/script.sh i18n-merge base.json new_translations.json
```

### `help`

```bash
scripts/script.sh help
```

### `version`

```bash
scripts/script.sh version
```

## Examples

```bash
# Quick translation
scripts/script.sh translate "How are you?" auto zh
scripts/script.sh detect "Bonjour le monde"
scripts/script.sh compare "Thank you" zh ja

# Build personal dictionary
scripts/script.sh add "microservice" "微服务"
scripts/script.sh lookup "microservice"
scripts/script.sh dict list

# i18n workflow
scripts/script.sh i18n-init myapp en,zh
scripts/script.sh i18n-extract src/main.py
scripts/script.sh i18n-check i18n/
```

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `TRANSLATOR_DIR` | No | Data directory (default: `~/.translator-pro/`) |

## Data Storage

All data saved in `~/.translator-pro/`:
- `dictionary.tsv` — Personal dictionary (word → translation)
- `glossaries/` — Custom glossary files
- `i18n/` — i18n project directories
- `history.log` — Translation history

## Requirements

- bash 4.0+
- curl (for LibreTranslate API)
- python3 (for JSON parsing and Unicode detection)

Translation API: LibreTranslate (free, no key required). Built-in English-Chinese dictionary (100+ words) provides offline fallback.

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
