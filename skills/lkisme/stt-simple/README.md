# STT Simple - 本地语音识别

基于 OpenAI Whisper 的简单本地语音转文字工具。

## ✨ 特点

- 🚀 **一键安装** - 自动配置虚拟环境、依赖、模型
- 🌍 **99+ 语言** - 支持中文、英文、日文等
- 💰 **完全免费** - 本地运行，无 API 费用
- 🔒 **隐私安全** - 音频文件不出本地

## 📦 安装

```bash
# 进入技能目录
cd /root/.openclaw/workspace/skills/stt-simple

# 运行安装脚本（首次使用）
bash install.sh
```

安装完成后：
- 虚拟环境：`/root/.openclaw/venv/stt-simple/`
- 模型缓存：`~/.cache/whisper/`
- 输出目录：`/root/.openclaw/workspace/stt_output/`

## 🎯 使用方法

### 命令行

```bash
# 基本用法
/root/.openclaw/venv/stt-simple/bin/whisper audio.ogg --model small --language Chinese

# 指定输出目录
/root/.openclaw/venv/stt-simple/bin/whisper audio.ogg --model small --language Chinese --output_dir /tmp/output

# 输出多种格式
/root/.openclaw/venv/stt-simple/bin/whisper audio.ogg --model small --output_format txt,json,srt
```

### Python 脚本

```bash
/root/.openclaw/venv/stt-simple/bin/python \
  /root/.openclaw/workspace/skills/stt-simple/stt_simple.py \
  audio.ogg small zh
```

### Python API

```python
import whisper

model = whisper.load_model("small")
result = model.transcribe("audio.ogg", language="zh")
print(result["text"])
```

## 📊 模型对比

| 模型 | 大小 | CPU 速度 | 推荐场景 |
|------|------|---------|---------|
| tiny | 39MB | ⚡⚡⚡ | 快速测试 |
| base | 74MB | ⚡⚡ | 日常使用 |
| small | 244MB | ⚡ | **推荐** |
| medium | 769MB | 🐌 | 高精度需求 |
| large | 1.5GB | 🐌🐌 | 最佳质量 |

## 🌐 语言代码

| 语言 | 代码 | 别名 |
|------|------|------|
| 中文 | zh | Chinese |
| 英文 | en | English |
| 日文 | ja | Japanese |
| 韩文 | ko | Korean |
| 法文 | fr | French |
| 德文 | de | German |
| 西班牙文 | es | Spanish |

## 📁 输出格式

- `.txt` - 纯文本
- `.json` - 完整结果（含时间戳、置信度）
- `.srt` - 字幕格式（视频用）
- `.vtt` - WebVTT（网页用）

## 🔧 故障排查

### 检查安装状态

```bash
/root/.openclaw/venv/stt-simple/bin/whisper --version
```

### 重新安装

```bash
rm -rf /root/.openclaw/venv/stt-simple
bash /root/.openclaw/workspace/skills/stt-simple/install.sh
```

### 手动下载模型

```bash
# 模型会下载到 ~/.cache/whisper/
# 可以预先下载避免首次运行等待
/root/.openclaw/venv/stt-simple/bin/python -c "import whisper; whisper.load_model('small')"
```

## 📝 许可证

- Whisper: MIT License (OpenAI)
- 本技能：MIT License

## 🙏 致谢

基于 [OpenAI Whisper](https://github.com/openai/whisper) 构建。
