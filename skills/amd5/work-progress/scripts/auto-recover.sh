#!/bin/bash
# 子代理超时自动恢复脚本
# 功能：检测超时的子代理任务并自动重新执行

WORKSPACE="${WORKSPACE_PATH:-$HOME/.openclaw/workspace}"
LOG_FILE="$WORKSPACE/memory/error.md"

echo "🔄 子代理超时自动恢复 ($(date +%Y-%m-%d %H:%M))"
echo "================================"

# ==================== 1. 获取所有 cron 任务 ====================
echo "📋 获取任务列表..."

# 获取最近运行的任务，检查是否有超时
RECENT_RUNS=$(openclaw cron list 2>/dev/null)

if [ -z "$RECENT_RUNS" ]; then
    echo "  ⚠️ 无法获取任务列表"
    exit 1
fi

# ==================== 2. 检测超时任务 ====================
echo "🔍 检测超时任务..."

# 检查日志中的超时错误
TIMEOUT_ERRORS=$(journalctl --user -u openclaw-gateway --since "30 minutes ago" 2>/dev/null | grep -i "timeout\|timed out" | tail -10)

if [ -n "$TIMEOUT_ERRORS" ]; then
    echo "  ⚠️ 发现超时错误:"
    echo "$TIMEOUT_ERRORS" | head -5
    
    # 提取任务名称（如果可能）
    TASK_NAMES=$(echo "$TIMEOUT_ERRORS" | grep -oE "task: [a-z0-9-]+" | cut -d' ' -f2 | sort -u)
    
    if [ -n "$TASK_NAMES" ]; then
        echo ""
        echo "📌 受影响的任务:"
        echo "$TASK_NAMES" | while read task; do
            echo "  - $task"
        done
        
        # ==================== 3. 自动恢复 ====================
        echo ""
        echo "🔄 尝试自动恢复..."
        
        # 这里可以根据任务名称重新触发
        # 由于需要任务 ID，这里只做日志记录
        echo "" >> "$LOG_FILE"
        echo "### [$(date +%Y-%m-%d %H:%M)] 子代理超时自动恢复" >> "$LOG_FILE"
        echo "受影响任务: $TASK_NAMES" >> "$LOG_FILE"
        echo "状态：已记录，建议手动重新执行" >> "$LOG_FILE"
        
        echo "  ✅ 已记录到错误日志，建议手动重新执行受影响的任务"
    else
        echo "  ⚠️ 无法识别具体任务，请手动检查"
    fi
else
    echo "  ✅ 无超时错误"
fi

# ==================== 4. 检查子代理进程 ====================
echo ""
echo "📊 检查子代理进程状态..."

# 检查是否有僵死的子代理进程
ZOMBIE_AGENTS=$(ps aux 2>/dev/null | grep -E "subagent|child" | grep -v grep | wc -l)

if [ "$ZOMBIE_AGENTS" -gt 10 ]; then
    echo "  ⚠️ 发现 $ZOMBIE_AGENTS 个子代理进程（可能过多）"
else
    echo "  ✅ 子代理进程正常 ($ZOMBIE_AGENTS 个)"
fi

# ==================== 5. 输出建议 ====================
echo ""
echo "================================"
echo "💡 建议:"

if [ -n "$TIMEOUT_ERRORS" ]; then
    echo "  1. 查看错误日志：journalctl --user -u openclaw-gateway"
    echo "  2. 检查 memory/error.md 中的详细记录"
    echo "  3. 手动重新执行失败的任务"
    echo "  4. 考虑增加子代理的 timeoutSeconds 参数"
else
    echo "  无需操作，系统运行正常"
fi

echo "NO_REPLY"
