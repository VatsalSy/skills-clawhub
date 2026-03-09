#!/bin/bash
# STT Simple - One-Command Install
# Creates virtual environment, installs Whisper, downloads model

set -e

# Configuration
VENV_DIR="/root/.openclaw/venv/stt-simple"
OUTPUT_DIR="/root/.openclaw/workspace/stt_output"
MODEL_NAME="small"
SKILL_DIR="$(dirname "$0")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }
log_ok() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo "========================================"
echo "  STT Simple - Local Speech-to-Text"
echo "  Installing Whisper + Dependencies"
echo "========================================"
echo ""

# Step 1: Check Python
log_step "Checking Python..."
if ! command -v python3 &> /dev/null; then
    log_error "Python3 not found. Please install Python 3.8+"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
log_ok "Python $PYTHON_VERSION found"

# Step 2: Check/Create Virtual Environment
log_step "Setting up virtual environment..."
if [ -d "$VENV_DIR" ]; then
    log_warn "Virtual environment exists, recreating..."
    rm -rf "$VENV_DIR"
fi

python3 -m venv "$VENV_DIR"
log_ok "Virtual environment created: $VENV_DIR"

# Step 3: Install FFmpeg
log_step "Checking FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    log_warn "FFmpeg not found, installing..."
    if command -v apt-get &> /dev/null; then
        apt-get update && apt-get install -y ffmpeg
    elif command -v yum &> /dev/null; then
        yum install -y ffmpeg
    elif command -v brew &> /dev/null; then
        brew install ffmpeg
    else
        log_error "Cannot install FFmpeg automatically. Please install manually."
        exit 1
    fi
    log_ok "FFmpeg installed"
else
    log_ok "FFmpeg already installed: $(ffmpeg -version | head -1)"
fi

# Step 4: Install Whisper
log_step "Installing OpenAI Whisper (this may take 2-5 minutes)..."
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install openai-whisper
log_ok "Whisper installed"

# Step 5: Download Model
log_step "Downloading Whisper '$MODEL_NAME' model (~244MB)..."
# Model downloads on first use, trigger it
echo "import whisper; print('Loading model...'); whisper.load_model('$MODEL_NAME'); print('Done')" | "$VENV_DIR/bin/python"
log_ok "Model downloaded to ~/.cache/whisper"

# Step 6: Create Output Directory
log_step "Creating output directory..."
mkdir -p "$OUTPUT_DIR"
log_ok "Output directory: $OUTPUT_DIR"

# Step 7: Verify Installation
echo ""
echo "========================================"
log_step "Verifying installation..."
echo "========================================"

"$VENV_DIR/bin/whisper" --version
echo ""

# Test with a quick import
echo "import whisper; print('Whisper version:', whisper.__version__)" | "$VENV_DIR/bin/python"

echo ""
echo "========================================"
echo "  ✅ Installation Complete!"
echo "========================================"
echo ""
echo "Usage:"
echo "  # Transcribe audio file"
echo "  $VENV_DIR/bin/whisper audio.ogg --model small --language Chinese"
echo ""
echo "  # Or use Python script"
echo "  $VENV_DIR/bin/python $SKILL_DIR/stt_simple.py audio.ogg small zh"
echo ""
echo "Output directory: $OUTPUT_DIR"
echo ""
