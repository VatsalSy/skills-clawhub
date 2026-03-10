#!/bin/bash
# use-openclaw-manual - OpenClaw 文档管理技能
# 用法：./run.sh --init|--sync|--search <词>|--read <文件>|--stats|--help

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYNC_SCRIPT="$SCRIPT_DIR/scripts/sync-docs.sh"
SEARCH_SCRIPT="$SCRIPT_DIR/scripts/search-docs.sh"

# 可配置路径
export OPENCLAW_MANUAL_PATH="${OPENCLAW_MANUAL_PATH:-$HOME/.openclaw/workspace/docs/openclaw_manual}"
export DOC_UPDATE_LOG="${DOC_UPDATE_LOG:-$SCRIPT_DIR/docs-update.log}"

show_help() {
  cat << EOF
📚 use-openclaw-manual - OpenClaw 文档管理技能

用法：./run.sh [选项]

核心功能:
  --init          首次同步文档（从 GitHub 克隆）
  --sync          增量同步文档更新
  --check         检查是否有更新

搜索功能:
  --search <词>   搜索文档内容
  --title <词>    搜索文档标题
  --file <词>     搜索文件名
  --read <文件>   阅读文档内容
  --stats         显示文档统计

示例:
  ./run.sh --init
  ./run.sh --search "agent binding"
  ./run.sh --title "cron"
  ./run.sh --read concepts/agent.md
  ./run.sh --stats

环境变量:
  OPENCLAW_MANUAL_PATH   - 文档目录 (默认：~/.openclaw/workspace/docs/openclaw_manual)
  DOC_NOTIFY_CHANNEL     - 通知渠道 (默认：webchat)

EOF
}

# 检查文档是否已同步
check_initialized() {
  if [ ! -d "$OPENCLAW_MANUAL_PATH" ] || [ -z "$(ls -A $OPENCLAW_MANUAL_PATH 2>/dev/null)" ]; then
    echo "❌ 文档未同步"
    echo ""
    echo "请先运行：./run.sh --init"
    exit 1
  fi
}

# 主函数
main() {
  if [ $# -eq 0 ]; then
    show_help
    exit 0
  fi

  case "$1" in
    --init)
      echo "🚀 初始化文档同步..."
      "$SYNC_SCRIPT" --init
      ;;
    
    --sync)
      echo "🔄 同步文档更新..."
      "$SYNC_SCRIPT" --sync
      ;;
    
    --check)
      echo "🔍 检查文档更新..."
      "$SYNC_SCRIPT" --check
      ;;
    
    --search|-s)
      shift
      check_initialized
      "$SEARCH_SCRIPT" --search "$@"
      ;;
    
    --title|-t)
      shift
      check_initialized
      "$SEARCH_SCRIPT" --title "$@"
      ;;
    
    --file|-f)
      shift
      check_initialized
      "$SEARCH_SCRIPT" --file "$@"
      ;;
    
    --read|-r)
      shift
      check_initialized
      "$SEARCH_SCRIPT" --read "$@"
      ;;
    
    --stats)
      check_initialized
      "$SEARCH_SCRIPT" --stats
      ;;
    
    --help|-h)
      show_help
      ;;
    
    *)
      echo "❌ 未知选项：$1"
      echo ""
      show_help
      exit 1
      ;;
  esac
}

main "$@"
