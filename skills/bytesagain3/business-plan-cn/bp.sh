#!/usr/bin/env bash
CMD="$1"; shift 2>/dev/null; INPUT="$*"
case "$CMD" in
  generate) cat << 'PROMPT'
你是创业导师。生成完整商业计划书(Markdown)：1.执行摘要 2.公司概况 3.产品/服务 4.市场分析 5.营销策略 6.运营计划 7.团队 8.财务预测 9.融资需求。用中文。
项目描述：
PROMPT
    echo "$INPUT" ;;
  canvas) cat << 'PROMPT'
你是精益创业专家。生成精益画布(Lean Canvas)：1.问题 2.客户细分 3.独特价值 4.解决方案 5.渠道 6.收入来源 7.成本结构 8.关键指标 9.不公平优势。用中文。
项目描述：
PROMPT
    echo "$INPUT" ;;
  swot) cat << 'PROMPT'
你是战略分析师。SWOT分析：1.优势Strengths 2.劣势Weaknesses 3.机会Opportunities 4.威胁Threats 5.SO/WO/ST/WT策略建议。用中文。
分析对象：
PROMPT
    echo "$INPUT" ;;
  financial) cat << 'PROMPT'
你是财务分析师。财务预测(3年)：1.收入预测 2.成本结构 3.盈亏平衡点 4.现金流 5.关键假设。输出表格。用中文。
业务模型：
PROMPT
    echo "$INPUT" ;;
  pitch) cat << 'PROMPT'
你是路演教练。30秒电梯演讲：1.问题 2.方案 3.市场 4.优势 5.要什么。中英双语各一版。
项目：
PROMPT
    echo "$INPUT" ;;
  market) cat << 'PROMPT'
你是市场研究员。市场分析：1.TAM/SAM/SOM 2.竞争格局 3.趋势 4.客户画像 5.进入策略。用中文。
行业/产品：
PROMPT
    echo "$INPUT" ;;
  *) cat << 'EOF'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📋 Business Plan — 使用指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  generate [项目]    完整商业计划书
  canvas [项目]      精益画布
  swot [对象]        SWOT分析
  financial [模型]   3年财务预测
  pitch [项目]       30秒电梯演讲
  market [行业]      市场分析

  Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
EOF
    ;;
esac
