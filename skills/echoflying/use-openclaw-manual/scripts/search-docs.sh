#!/bin/bash
# use-openclaw-manual - 文档搜索脚本
# 提供快速、简洁的文档搜索功能

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export OPENCLAW_MANUAL_PATH="${OPENCLAW_MANUAL_PATH:-$HOME/.openclaw/workspace/docs/openclaw_manual}"
LOG_FILE="${DOC_UPDATE_LOG:-$SCRIPT_DIR/docs-update.log}"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 检查文档是否已同步
check_initialized() {
  if [ ! -d "$OPENCLAW_MANUAL_PATH" ] || [ -z "$(ls -A $OPENCLAW_MANUAL_PATH 2>/dev/null)" ]; then
    echo "❌ 文档未同步，请先运行：./run.sh --init"
    exit 1
  fi
}

# 搜索文档内容（简洁输出）
search_content() {
  local keyword="$1"
  local limit="${2:-10}"
  
  echo "🔍 搜索内容：'$keyword'"
  echo "📁 路径：$OPENCLAW_MANUAL_PATH"
  echo "---"
  
  local results=$(grep -rn "$keyword" "$OPENCLAW_MANUAL_PATH" --include="*.md" 2>/dev/null | head -"$limit")
  
  if [ -z "$results" ]; then
    echo "未找到匹配项"
    return 0
  fi
  
  echo "$results" | while IFS=: read -r file lineno content; do
    rel_path="${file#$OPENCLAW_MANUAL_PATH/}"
    echo "$rel_path:$lineno"
    echo "  $content"
    echo ""
  done
  
  local total=$(grep -r "$keyword" "$OPENCLAW_MANUAL_PATH" --include="*.md" 2>/dev/null | wc -l)
  echo "---"
  echo "共 $total 个匹配（显示前 $limit 个）"
}

# 搜索标题
search_title() {
  local keyword="$1"
  local limit="${2:-10}"
  
  echo "🔍 搜索标题：'$keyword'"
  echo "---"
  
  local results=$(grep -rn "^#" "$OPENCLAW_MANUAL_PATH" --include="*.md" 2>/dev/null | grep -i "$keyword" | head -"$limit")
  
  if [ -z "$results" ]; then
    echo "未找到匹配标题"
    return 0
  fi
  
  echo "$results" | while IFS=: read -r file lineno title; do
    rel_path="${file#$OPENCLAW_MANUAL_PATH/}"
    echo "$rel_path:$lineno"
    echo "  $title"
    echo ""
  done
  
  local total=$(grep -r "^#" "$OPENCLAW_MANUAL_PATH" --include="*.md" 2>/dev/null | grep -i "$keyword" | wc -l)
  echo "---"
  echo "共 $total 个匹配标题"
}

# 搜索文件名
search_file() {
  local keyword="$1"
  local limit="${2:-20}"
  
  echo "🔍 搜索文件名：'$keyword'"
  echo "---"
  
  local results=$(find "$OPENCLAW_MANUAL_PATH" -name "*$keyword*.md" 2>/dev/null | head -"$limit")
  
  if [ -z "$results" ]; then
    echo "未找到匹配文件"
    return 0
  fi
  
  echo "$results" | while read -r file; do
    echo "${file#$OPENCLAW_MANUAL_PATH/}"
  done
  
  local total=$(find "$OPENCLAW_MANUAL_PATH" -name "*$keyword*.md" 2>/dev/null | wc -l)
  echo "---"
  echo "共 $total 个匹配文件"
}

# 阅读文档
read_document() {
  local doc="$1"
  local lines="${2:-50}"
  
  local file="$OPENCLAW_MANUAL_PATH/$doc"
  
  if [ ! -f "$file" ]; then
    echo "❌ 文档不存在：$doc"
    echo ""
    echo "提示：使用 --search 搜索相关文档"
    exit 1
  fi
  
  echo "📄 $doc (前 $lines 行)"
  echo "---"
  head -"$lines" "$file"
}

# 显示统计
show_stats() {
  echo "📊 文档统计"
  echo "---"
  echo "路径：$OPENCLAW_MANUAL_PATH"
  echo ""
  
  local file_count=$(find "$OPENCLAW_MANUAL_PATH" -type f ! -name ".*" | wc -l)
  local md_count=$(find "$OPENCLAW_MANUAL_PATH" -name "*.md" | wc -l)
  local dir_count=$(find "$OPENCLAW_MANUAL_PATH" -type d | wc -l)
  local total_lines=$(find "$OPENCLAW_MANUAL_PATH" -name "*.md" -exec cat {} \; 2>/dev/null | wc -l)
  local total_words=$(find "$OPENCLAW_MANUAL_PATH" -name "*.md" -exec cat {} \; 2>/dev/null | wc -w)
  
  echo "文件：$file_count 个 (Markdown: $md_count 个)"
  echo "目录：$dir_count 个"
  echo "总行数：$total_lines"
  echo "总词数：$total_words"
  echo ""
  
  echo "主要目录:"
  ls -1 "$OPENCLAW_MANUAL_PATH" 2>/dev/null | head -10 | while read -r dir; do
    if [ -d "$OPENCLAW_MANUAL_PATH/$dir" ]; then
      local count=$(find "$OPENCLAW_MANUAL_PATH/$dir" -type f 2>/dev/null | wc -l)
      echo "  📁 $dir/ ($count 个文件)"
    fi
  done
}

# 主函数
main() {
  check_initialized
  
  local mode="${1:---help}"
  shift 2>/dev/null || true
  
  case "$mode" in
    --search|-s)
      local keyword="$1"
      local limit="${2:-10}"
      
      if [ -z "$keyword" ]; then
        echo "❌ 请提供搜索关键词"
        echo "用法：--search <关键词> [数量]"
        exit 1
      fi
      
      search_content "$keyword" "$limit"
      log "搜索：$keyword"
      ;;
    
    --title|-t)
      local keyword="$1"
      local limit="${2:-10}"
      
      if [ -z "$keyword" ]; then
        echo "❌ 请提供搜索关键词"
        exit 1
      fi
      
      search_title "$keyword" "$limit"
      log "搜索标题：$keyword"
      ;;
    
    --file|-f)
      local keyword="$1"
      local limit="${2:-20}"
      
      if [ -z "$keyword" ]; then
        echo "❌ 请提供搜索关键词"
        exit 1
      fi
      
      search_file "$keyword" "$limit"
      log "搜索文件：$keyword"
      ;;
    
    --read|-r)
      local doc="$1"
      local lines="${2:-50}"
      
      if [ -z "$doc" ]; then
        echo "❌ 请提供文档路径"
        exit 1
      fi
      
      read_document "$doc" "$lines"
      ;;
    
    --stats)
      show_stats
      ;;
    
    --help|-h)
      echo "用法：search-docs.sh [选项]"
      echo ""
      echo "选项:"
      echo "  --search, -s <词> [数量]  搜索内容"
      echo "  --title, -t <词>          搜索标题"
      echo "  --file, -f <词>           搜索文件名"
      echo "  --read, -r <文件> [行数]  阅读文档"
      echo "  --stats                   显示统计"
      echo "  --help, -h                显示帮助"
      ;;
    
    *)
      echo "❌ 未知选项：$mode"
      exit 1
      ;;
  esac
}

main "$@"
