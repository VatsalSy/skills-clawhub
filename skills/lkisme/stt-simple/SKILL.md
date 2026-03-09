---
name: stt-simple
version: 1.0.0
description: >
  Simple local Speech-To-Text using Whisper. One-command install with auto model download.
  Supports 99+ languages.
homepage: https://openai.com/research/whisper
---

# Simple Local STT (Whisper)

一键安装本地语音识别，支持 99+ 语言。

## 🚀 快速开始

### 安装（首次使用）

```bash
# 自动安装虚拟环境 + 依赖 + 模型
/root/.openclaw/workspace/skills/stt-simple/install.sh
```

### 使用

```bash
# 命令行转换
/root/.openclaw/venv/stt-simple/bin/whisper audio.ogg --model small --language Chinese

# Python API
/root/.openclaw/venv/stt-simple/bin/python \
  /root/.openclaw/workspace/skills/stt-simple/stt_simple.py \
  audio.ogg small zh
```

## 📦 安装脚本详解

`install.sh` 自动完成：

1. ✅ 创建虚拟环境 `/root/.openclaw/venv/stt-simple/`
2. ✅ 安装 `openai-whisper` + `ffmpeg`
3. ✅ 下载 Whisper small 模型（244MB）
4. ✅ 创建输出目录

## 🎯 模型选择

| 模型 | 大小 | 速度 | 精度 | 场景 |
|------|------|------|------|------|
| `tiny` | 39MB | ⚡⚡⚡ | ⭐⭐⭐ | 快速测试 |
| `base` | 74MB | ⚡⚡ | ⭐⭐⭐⭐ | 日常使用 |
| `small` | 244MB | ⚡ | ⭐⭐⭐⭐⭐ | **推荐** |
| `medium` | 769MB | 🐌 | ⭐⭐⭐⭐⭐ | 高精度 |
| `large` | 1.5GB | 🐌🐌 | ⭐⭐⭐⭐⭐+ | 最佳质量 |

## 🌍 语言代码

- 中文：`zh` 或 `Chinese`
- 英文：`en` 或 `English`
- 日文：`ja` 或 `Japanese`
- 自动检测：省略 `--language`

## 📁 输出格式

- `.txt` - 纯文本
- `.json` - 完整结果（含时间戳）
- `.srt` - 字幕格式
- `.vtt` - WebVTT

## 🔧 故障排查

```bash
# 检查安装
/root/.openclaw/venv/stt-simple/bin/whisper --version

# 重新安装
rm -rf /root/.openclaw/venv/stt-simple
/root/.openclaw/workspace/skills/stt-simple/install.sh
```
