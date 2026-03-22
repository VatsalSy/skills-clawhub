---
name: speech-recognition-local
description: 本地语音转文字。使用 faster-whisper 在本地运行 Whisper 模型，无需 API 费用。当用户发送语音消息(.ogg, .m4a, .mp3)时自动触发。
---

# 本地语音识别

## 使用方式

收到语音消息后，自动调用转录脚本。

## 转录命令

```bash
python3 ~/.openclaw/workspace/skills/speech-recognition-local/scripts/transcribe.py <audio_file> [language]
```

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| audio_file | - | 音频文件路径 |
| language | zh | 语言：zh/en/ja/auto |

## 模型说明

- 默认使用 `base` 模型
- 首次使用自动下载
- 已启用 VAD 过滤静音
- 模型缓存在内存中

## 限制

- 支持格式：.ogg, .m4a, .mp3, .wav
- 文件大小限制：25MB
