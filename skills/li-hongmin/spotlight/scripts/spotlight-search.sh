#!/bin/bash
# spotlight-search.sh - 使用 macOS Spotlight 搜索文件
# 用法: spotlight-search.sh <directory> <query> [--limit N]

set -euo pipefail

show_usage() {
    cat << EOF
用法: spotlight-search.sh <directory> <query> [--limit N]

参数:
  <directory>  要搜索的目录路径
  <query>      搜索关键词
  --limit N    返回最多 N 个结果（默认 20）

示例:
  spotlight-search.sh ~/Documents "项目计划"
  spotlight-search.sh ~/research/璐璐研究 "留日" --limit 10
EOF
}

# 参数解析
if [ $# -lt 2 ]; then
    show_usage
    exit 1
fi

DIRECTORY="$1"
QUERY="$2"
LIMIT=20

# 检查可选参数
shift 2
while [ $# -gt 0 ]; do
    case "$1" in
        --limit)
            LIMIT="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1" >&2
            show_usage
            exit 1
            ;;
    esac
done

# 检查目录是否存在
if [ ! -d "$DIRECTORY" ]; then
    echo "错误: 目录不存在: $DIRECTORY" >&2
    exit 1
fi

# 展开路径（处理 ~ 等）
DIRECTORY=$(cd "$DIRECTORY" && pwd)

# 使用 mdfind 搜索
# -onlyin: 限制搜索范围
# 2>/dev/null: 忽略错误信息
echo "🔍 在 $DIRECTORY 中搜索: $QUERY"
echo ""

results=$(mdfind -onlyin "$DIRECTORY" "$QUERY" 2>/dev/null | head -n "$LIMIT")

if [ -z "$results" ]; then
    echo "❌ 未找到匹配结果"
    exit 0
fi

# 统计结果数量
count=$(echo "$results" | wc -l | tr -d ' ')
echo "✅ 找到 $count 个结果（最多显示 $LIMIT 个）："
echo ""

# 输出结果
echo "$results" | while IFS= read -r file; do
    # 获取文件类型
    ext="${file##*.}"
    
    # 获取文件大小
    if [ -f "$file" ]; then
        size=$(ls -lh "$file" | awk '{print $5}')
        echo "📄 $file [$ext, $size]"
    elif [ -d "$file" ]; then
        echo "📁 $file/"
    else
        echo "❓ $file"
    fi
done

exit 0
