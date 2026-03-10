#!/bin/bash
# use-openclaw-manual - 文档同步脚本
# 从 GitHub 同步 OpenClaw 官方文档到本地

set -e

REPO="openclaw/openclaw"
DOCS_PATH="docs/"
TEMP_REPO="/tmp/openclaw-docs-$$"

# 技能目录
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 可配置路径（支持环境变量覆盖）
export OPENCLAW_MANUAL_PATH="${OPENCLAW_MANUAL_PATH:-$HOME/.openclaw/workspace/docs/openclaw_manual}"
LAST_COMMIT_FILE="${LAST_COMMIT_FILE:-$OPENCLAW_MANUAL_PATH/.last-docs-commit}"
LOG_FILE="${DOC_UPDATE_LOG:-$SKILL_DIR/docs-update.log}"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 获取最新 commit (仅 docs 目录)
get_latest_commit() {
  curl -s "https://api.github.com/repos/$REPO/commits?path=$DOCS_PATH&per_page=1" 2>/dev/null | \
    python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['sha'] if d else '')" 2>/dev/null || echo ""
}

# 获取变更文件列表
get_changed_files() {
  local old_commit="$1"
  local new_commit="$2"
  local sync_type="$3"
  
  if [ "$sync_type" = "full" ]; then
    # 首次同步：获取所有 docs 文件
    curl -s "https://api.github.com/repos/$REPO/git/trees/$new_commit?recursive=1" 2>/dev/null | \
      python3 -c "import sys,json; d=json.load(sys.stdin); files=[f['path'] for f in d.get('tree',[]) if f['path'].startswith('docs/') and f['type']=='blob']; print('\n'.join(files))" 2>/dev/null || echo ""
  else
    # 增量同步：获取两个 commit 之间的变更文件
    curl -s "https://api.github.com/repos/$REPO/compare/$old_commit...$new_commit" 2>/dev/null | \
      python3 -c "import sys,json; d=json.load(sys.stdin); files=[f['filename'] for f in d.get('files',[]) if f['filename'].startswith('docs/')]; print('\n'.join(files))" 2>/dev/null || echo ""
  fi
}

# 同步文档
sync_docs() {
  local sync_type="$1"
  local latest_commit="$2"
  local changed_files="$3"
  local files_count="$4"
  
  log "📥 开始同步 $files_count 个文件 ($sync_type)..."
  
  # 清理临时目录
  rm -rf "$TEMP_REPO"
  mkdir -p "$TEMP_REPO"
  cd "$TEMP_REPO"
  
  # 初始化 git 仓库并配置 sparse-checkout
  git init >/dev/null 2>&1
  git remote add origin "https://github.com/$REPO.git" >/dev/null 2>&1
  git config core.sparseCheckout true >/dev/null 2>&1
  echo "docs/" > .git/info/sparse-checkout
  
  # 浅克隆 docs 目录
  if ! git pull --depth 1 origin main >/dev/null 2>&1; then
    log "❌ 克隆失败"
    cd - >/dev/null
    rm -rf "$TEMP_REPO"
    exit 1
  fi
  
  # 如果是首次同步，清空本地目录
  if [ "$sync_type" = "full" ]; then
    log "🗑️ 清空本地文档目录..."
    rm -rf "$OPENCLAW_MANUAL_PATH"
    mkdir -p "$OPENCLAW_MANUAL_PATH"
  fi
  
  # 同步到本地
  local synced=0
  echo "$changed_files" | while read -r file; do
    if [ -n "$file" ] && [ -f "$TEMP_REPO/$file" ]; then
      # 提取相对路径 (去掉 docs/ 前缀)
      REL_PATH="${file#docs/}"
      TARGET_DIR="$OPENCLAW_MANUAL_PATH/$(dirname "$REL_PATH")"
      
      # 创建目录并复制文件
      mkdir -p "$TARGET_DIR"
      cp "$TEMP_REPO/$file" "$TARGET_DIR/"
      synced=$((synced + 1))
    fi
  done
  
  # 清理临时目录
  cd - >/dev/null
  rm -rf "$TEMP_REPO"
  
  log "✅ 同步完成 ($synced 个文件)"
}

# 更新 baseline
update_baseline() {
  local commit="$1"
  mkdir -p "$(dirname "$LAST_COMMIT_FILE")"
  echo "$commit" > "$LAST_COMMIT_FILE"
  log "✅ Baseline 已更新：${commit:0:7}"
}

# 主函数
main() {
  local mode="${1:---check}"
  
  case "$mode" in
    --init)
      log "🔄 开始文档同步（完整）..."
      
      # 获取最新 commit
      LATEST_COMMIT=$(get_latest_commit)
      if [ -z "$LATEST_COMMIT" ]; then
        log "❌ 获取 commit 失败，请检查网络连接"
        exit 1
      fi
      
      # 获取所有 docs 文件
      CHANGED_FILES=$(get_changed_files "" "$LATEST_COMMIT" "full")
      FILES_COUNT=$(echo "$CHANGED_FILES" | grep -c . || echo 0)
      
      if [ "$FILES_COUNT" -eq 0 ]; then
        log "⚠️ 未找到 docs 文件"
        exit 1
      fi
      
      # 同步文档
      sync_docs "full" "$LATEST_COMMIT" "$CHANGED_FILES" "$FILES_COUNT"
      
      # 更新 baseline
      update_baseline "$LATEST_COMMIT"
      
      log "✅ 完整同步完成"
      ;;
    
    --sync)
      log "🔄 开始文档同步（增量）..."
      
      # 获取最新 commit
      LATEST_COMMIT=$(get_latest_commit)
      if [ -z "$LATEST_COMMIT" ]; then
        log "❌ 获取 commit 失败"
        exit 1
      fi
      
      # 读取上次记录的 commit
      LAST_COMMIT=$(cat "$LAST_COMMIT_FILE" 2>/dev/null || echo "")
      
      if [ -z "$LAST_COMMIT" ]; then
        log "⚠️ 未初始化，请运行：./run.sh --init"
        exit 1
      fi
      
      if [ "$LATEST_COMMIT" = "$LAST_COMMIT" ]; then
        log "✅ 文档已是最新"
        exit 0
      fi
      
      # 获取变更文件列表
      CHANGED_FILES=$(get_changed_files "$LAST_COMMIT" "$LATEST_COMMIT" "incremental")
      FILES_COUNT=$(echo "$CHANGED_FILES" | grep -c . || echo 0)
      
      if [ "$FILES_COUNT" -eq 0 ]; then
        log "⚠️ 无 docs 文件变更"
        update_baseline "$LATEST_COMMIT"
        exit 0
      fi
      
      # 同步文档
      sync_docs "incremental" "$LATEST_COMMIT" "$CHANGED_FILES" "$FILES_COUNT"
      
      # 更新 baseline
      update_baseline "$LATEST_COMMIT"
      
      log "✅ 增量同步完成"
      ;;
    
    --check)
      log "🔍 检查文档更新..."
      
      LATEST_COMMIT=$(get_latest_commit)
      LAST_COMMIT=$(cat "$LAST_COMMIT_FILE" 2>/dev/null || echo "")
      
      if [ -z "$LAST_COMMIT" ]; then
        log "⚠️ 未初始化，请运行：./run.sh --init"
        exit 1
      elif [ "$LATEST_COMMIT" = "$LAST_COMMIT" ]; then
        log "✅ 文档已是最新"
      else
        log "🔄 发现更新！运行以下命令同步："
        log "   ./run.sh --sync"
      fi
      ;;
    
    --help|-h)
      echo "用法：sync-docs.sh [选项]"
      echo ""
      echo "选项:"
      echo "  --init     首次初始化（完整同步）"
      echo "  --sync     增量同步（仅更新变更文件）"
      echo "  --check    仅检查更新，不同步"
      echo "  --help     显示帮助"
      echo ""
      ;;
    
    *)
      echo "❌ 未知选项：$mode"
      echo "运行 './sync-docs.sh --help' 查看帮助"
      exit 1
      ;;
  esac
}

main "$@"
