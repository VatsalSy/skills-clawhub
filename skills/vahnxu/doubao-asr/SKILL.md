---
name: doubao-asr
description: "Transcribe audio via Doubao Seed-ASR 2.0 API (ByteDance/Volcengine). Best-in-class Chinese speech recognition. 通过豆包语音大模型转写音频，中文识别效果业界领先。Use when the user needs high-quality Chinese transcription, or asks for Doubao/豆包/Volcengine/火山引擎 transcription."
homepage: https://www.volcengine.com/docs/6561/1354868
metadata:
  {
    "openclaw":
      {
        "emoji": "🫘",
        "requires": { "bins": ["python3"], "env": ["VOLCENGINE_APP_ID", "VOLCENGINE_ACCESS_TOKEN", "VOLCENGINE_ACCESS_KEY_ID", "VOLCENGINE_SECRET_ACCESS_KEY", "VOLCENGINE_TOS_BUCKET"], "pip": ["requests"] },
        "primaryEnv": "VOLCENGINE_APP_ID",
      },
  }
---

# Doubao ASR

Transcribe audio files via ByteDance Volcengine's Seed-ASR 2.0 API. Best-in-class accuracy for Chinese (Mandarin, Cantonese, Sichuan dialect, etc.) and supports 13+ languages.

通过字节跳动火山引擎 Seed-ASR 2.0 大模型转写音频文件。中文识别（普通话、粤语、四川话等方言）准确率业界领先，支持 13+ 种语言。

## Sending audio to OpenClaw

Currently, audio files can be sent to OpenClaw via messaging platforms such as **Discord**, **Telegram**, or **WhatsApp**. Send the audio file in a chat message and ask the bot to transcribe it.

目前可通过 **Discord**、**Telegram** 或 **WhatsApp** 等即时通讯平台向 OpenClaw 发送音频文件，发送后让 bot 转写即可。

> **Note**: Direct voice recording in the OpenClaw web UI is not yet supported. Use a messaging app to send pre-recorded audio files.
>
> **提示**：OpenClaw 网页端暂不支持直接录音，请通过即时通讯应用发送预录制的音频文件。

## Quick start

```bash
python3 {baseDir}/scripts/transcribe.py /path/to/audio.m4a
```

Defaults:

- Model: Seed-ASR 2.0 Standard
- Output: stdout (transcript text)

## Useful flags

```bash
python3 {baseDir}/scripts/transcribe.py /path/to/audio.m4a --out /tmp/transcript.txt
python3 {baseDir}/scripts/transcribe.py /path/to/audio.mp3 --format mp3
python3 {baseDir}/scripts/transcribe.py /path/to/audio.m4a --json --out /tmp/result.json
python3 {baseDir}/scripts/transcribe.py /path/to/audio.m4a --speakers  # speaker diarization / 说话人分离
python3 {baseDir}/scripts/transcribe.py https://example.com/audio.mp3  # direct URL (skip upload)
```

## How it works

The Doubao API accepts audio via URL (not direct file upload). The script:

1. **Uploads audio to Volcengine TOS** (object storage) using a time-limited presigned URL — audio stays within Volcengine infrastructure, no third-party services involved
2. Submits transcription task to Seed-ASR 2.0
3. Polls until complete (typically 1-3 minutes for a 10-min audio)
4. Returns transcript text

> **Privacy**: By default, audio is uploaded to your own Volcengine TOS bucket via presigned URL. No data is sent to third-party services.

### Custom upload endpoint

If you prefer to use a different storage service (e.g. Aliyun OSS, AWS S3, your own server), set `DOUBAO_ASR_UPLOAD_URL` to your upload endpoint. The script will POST the file as multipart form data and expect a JSON response with a `url` field.

You can also pass a direct audio URL as the argument to skip upload entirely:

```bash
python3 {baseDir}/scripts/transcribe.py https://your-bucket.tos.volces.com/audio.m4a
```

## Dependencies

- Python 3.9+
- `requests` library: `pip install requests`

## Credentials

### Required: Doubao ASR API

Get credentials from the Volcengine Speech console:

1. Open https://console.volcengine.com/speech/app
2. Create an app (or use existing)
3. In the left sidebar, find "豆包录音文件识别模型 2.0" and click into it
4. Copy **APP ID** and **Access Token**

Set environment variables:

```bash
export VOLCENGINE_APP_ID="your_app_id"
export VOLCENGINE_ACCESS_TOKEN="your_access_token"
```

### Required: Volcengine TOS (for audio upload)

The Doubao API requires audio to be accessible via URL. TOS provides secure, private temporary upload within Volcengine.

1. Open https://console.volcengine.com/tos
2. Create a bucket (e.g. `my-asr-audio`, region: cn-beijing)
3. Get your IAM access key from https://console.volcengine.com/iam/keymanage/

```bash
export VOLCENGINE_ACCESS_KEY_ID="your_ak"
export VOLCENGINE_SECRET_ACCESS_KEY="your_sk"
export VOLCENGINE_TOS_BUCKET="your_bucket_name"
# Optional:
# export VOLCENGINE_TOS_REGION="cn-beijing"  (default)
```

### Alternative: Custom upload endpoint

Skip TOS setup by providing your own upload endpoint:

```bash
export DOUBAO_ASR_UPLOAD_URL="https://your-server.com/upload"
```

## Supported formats

WAV, MP3, MP4, M4A, OGG, FLAC — up to 5 hours, 512MB max.
