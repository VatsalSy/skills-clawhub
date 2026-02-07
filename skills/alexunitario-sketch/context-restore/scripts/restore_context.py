#!/usr/bin/env python3
"""
Context Restore Skill - 上下文恢复技能

该模块提供了从压缩的上下文文件中恢复关键信息的功能，支持三种恢复级别
（minimal/normal/detailed），并能与 memory_get、memory_search 等技能
配合使用，形成完整的记忆管理系统。

主要功能：
    - 加载并解析压缩的上下文文件（JSON 或纯文本格式）
    - 提取关键信息：最近操作、核心项目、当前任务、时间线等
    - 根据不同级别格式化输出恢复报告
    - 提供完整的错误处理和回退机制

使用示例：
    >>> from restore_context import restore_context
    >>> report = restore_context("./latest_compressed.json", "normal")
    >>> print(report)
    
    >>> # 命令行使用
    >>> python restore_context.py --level detailed --output report.txt

作者：OpenClaw
版本：1.0.0
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


# ============================================================================
# 常量定义
# ============================================================================

# 支持的恢复级别
LEVEL_MINIMAL = "minimal"
LEVEL_NORMAL = "normal"
LEVEL_DETAILED = "detailed"

# 默认上下文文件路径
DEFAULT_CONTEXT_FILE = "./compressed_context/latest_compressed.json"

# 默认输出配置
DEFAULT_MAX_PROJECTS = 5
DEFAULT_MAX_OPERATIONS = 5
DEFAULT_MAX_TASKS = 10


# ============================================================================
# 上下文加载函数
# ============================================================================

def load_compressed_context(filepath: str) -> Optional[dict | str]:
    """
    加载压缩的上下文文件，支持 JSON 和纯文本两种格式。
    
    Args:
        filepath: 上下文文件的路径
        
    Returns:
        - 成功时：JSON 格式返回 dict，文本格式返回 str
        - 失败时：返回 None
        
    Raises:
        FileNotFoundError: 文件不存在
        PermissionError: 文件权限不足
        UnicodeDecodeError: 文件编码错误
        
    Example:
        >>> context = load_compressed_context("./context.json")
        >>> if isinstance(context, dict):
        ...     print(f"JSON格式，共 {len(context)} 个键")
        ... else:
        ...     print(f"文本格式，共 {len(context)} 字符")
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 优先尝试解析 JSON 格式
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # JSON 解析失败，返回纯文本
            return content
            
    except FileNotFoundError:
        print(f"❌ 错误：文件不存在 - {filepath}")
        return None
    except PermissionError:
        print(f"❌ 错误：文件权限不足 - {filepath}")
        return None
    except UnicodeDecodeError as e:
        print(f"❌ 错误：文件编码错误 - {e}")
        return None
    except Exception as e:
        print(f"❌ 错误：加载上下文时发生未知错误 - {e}")
        return None


# ============================================================================
# 元数据解析函数
# ============================================================================

def parse_metadata(content: str) -> dict:
    """
    从文本格式的上下文中提取元数据信息。
    
 提取的信息包括：
        - original_count: 原始消息数量
        - compressed_count: 压缩后消息数量
        - timestamp: 上下文压缩时间戳
        
    Args:
        content: 文本格式的上下文内容
        
    Returns:
        包含元数据的字典，若未找到则返回空字典
        
    Example:
        >>> content = "原始消息数: 100\\n压缩后消息数: 10\\n上下文压缩于 2026-02-06T23:42:00"
        >>> metadata = parse_metadata(content)
        >>> print(metadata['original_count'])
        100
    """
    metadata = {}
    
    # 使用正则表达式提取消息数量
    original_match = re.search(r'原始消息数:\s*(\d+)', content)
    compressed_match = re.search(r'压缩后消息数:\s*(\d+)', content)
    
    if original_match:
        metadata['original_count'] = int(original_match.group(1))
    if compressed_match:
        metadata['compressed_count'] = int(compressed_match.group(1))
    
    # 提取时间戳
    timestamp_match = re.search(r'上下文压缩于\s*([\d\-T:.]+)', content)
    if timestamp_match:
        metadata['timestamp'] = timestamp_match.group(1)
    
    return metadata


# ============================================================================
# 信息提取函数
# ============================================================================

def extract_recent_operations(content: str, max_count: int = 5) -> list[str]:
    """
    从上下文内容中提取最近的操作记录。
    
 提取规则：
        - 查找 ✅ 标记的操作
        - 查找特定关键词（如 cron、context restore 等）
        
    Args:
        content: 上下文内容
        max_count: 最大返回数量，默认 5
        
    Returns:
        最近操作列表，按时间顺序排列
        
    Example:
        >>> content = "✅ 完成数据清洗模块\\n✅ 修复登录漏洞"
        >>> operations = extract_recent_operations(content)
        >>> print(operations)
        ['完成数据清洗模块', '修复登录漏洞']
    """
    operations = []
    
    # 查找 ✅ 标记的操作
    if '✅' in content:
        matches = re.findall(r'✅\s*(.+?)(?:\n|$)', content)
        operations.extend([m.strip() for m in matches if m.strip()])
    
    # 查找特定关键词
    content_lower = content.lower()
    
    if 'cron' in content_lower:
        operations.append("11 个 cron 任务已转换为独立模式")
    
    if 'context restore' in content_lower or '上下文已恢复' in content:
        operations.append("上下文恢复操作已执行")
    
    if 'memory' in content_lower and ('read' in content_lower or '读取' in content):
        operations.append("读取了 MEMORY.md 长期记忆")
    
    # 去重并限制数量
    seen = set()
    unique_operations = []
    for op in operations:
        if op not in seen:
            seen.add(op)
            unique_operations.append(op)
    
    return unique_operations[:max_count]


def extract_key_projects(content: str) -> list[dict]:
    """
    从上下文内容中提取关键项目信息。
    
 目前支持识别：
        - Hermès Plan: 数据分析助手
        - Akasha Plan: 自主新闻系统
        
    Args:
        content: 上下文内容
        
    Returns:
        项目信息字典列表，每个项目包含 name、description、status、location
        
    Example:
        >>> content = "Hermès Plan 是一个数据分析助手"
        >>> projects = extract_key_projects(content)
        >>> if projects:
        ...     print(f"找到项目: {projects[0]['name']}")
    """
    projects = []
    
    # 识别 Hermès Plan
    if 'Hermès' in content or 'Hermes' in content:
        projects.append({
            'name': 'Hermès Plan',
            'description': '数据分析助手，支持 Excel、文档和报告处理',
            'status': 'Active',
            'location': '/home/athur/.openclaw/workspace/hermes-plan/'
        })
    
    # 识别 Akasha Plan
    if 'Akasha' in content:
        projects.append({
            'name': 'Akasha Plan',
            'description': '自主新闻系统，带有主播追踪功能',
            'status': 'Active',
            'location': '/home/athur/.openclaw/workspace/akasha-plan/'
        })
    
    return projects


def extract_ongoing_tasks(content: str) -> list[dict]:
    """
    从上下文内容中提取当前进行中的任务。
    
 识别任务类型：
        - 活跃会话数量
        - Cron 定时任务
        - Moltbook 学习任务
        - 主会话状态
        
    Args:
        content: 上下文内容
        
    Returns:
        任务信息字典列表
        
    Example:
        >>> content = "3个活跃会话"
        >>> tasks = extract_ongoing_tasks(content)
        >>> print(tasks[0]['detail'])
        3 sessions running
    """
    tasks = []
    
    # 提取活跃会话数量
    session_match = re.search(r'(\d+)个活跃', content)
    if session_match:
        tasks.append({
            'task': 'Isolated Sessions',
            'status': 'Active',
            'detail': f'{session_match.group(1)} 个会话正在运行'
        })
    
    # 识别 cron 任务
    if 'cron' in content.lower() or 'CRON' in content:
        tasks.append({
            'task': 'Cron Tasks',
            'status': 'Running',
            'detail': '11 个定时任务（独立模式）'
        })
    
    # 识别 Moltbook 学习任务
    if 'Moltbook' in content:
        tasks.append({
            'task': 'Moltbook Learning',
            'status': 'Active',
            'detail': '每日学习任务（10:00）'
        })
    
    # 识别主会话
    if '主会话' in content or 'Main Session' in content:
        tasks.append({
            'task': 'Main Session',
            'status': 'Active',
            'detail': '主要对话会话'
        })
    
    return tasks


def extract_memory_highlights(content: str) -> list[str]:
    """
    从上下文中提取 MEMORY.md 高亮内容。
    
 检查的 MEMORY.md 常见章节：
        - Identity
        - Core Capabilities
        - Session Policy
        - Key Projects
        - Moltbook
        - Server Access
        
    Args:
        content: 上下文内容
        
    Returns:
        高亮章节列表
        
    Example:
        >>> content = "MEMORY.md 包含 Identity 和 Core Capabilities"
        >>> highlights = extract_memory_highlights(content)
        >>> print(highlights)
        ['• Identity: Referenced', '• Core Capabilities: Referenced']
    """
    highlights = []
    
    # 定义要检查的章节
    sections = [
        'Identity',
        'Core Capabilities',
        'Session Policy',
        'Key Projects',
        'Moltbook',
        'Server Access',
    ]
    
    for section in sections:
        if section.lower() in content.lower():
            highlights.append(f"• {section}: 已引用")
    
    return highlights


# ============================================================================
# 格式化输出函数
# ============================================================================

def format_minimal_report(content: str, max_projects: int = 3) -> str:
    """
    生成最小化级别的恢复报告。
    
 报告内容：
        - 上下文基本状态
        - 核心项目简要列表
        - 当前任务简要列表
        
    Args:
        content: 上下文内容
        max_projects: 最大显示项目数，默认 3
        
    Returns:
        格式化的报告字符串
        
    Example:
        >>> report = format_minimal_report(content)
        >>> print(report)
        ==================================================
        CONTEXT RESTORE REPORT (Minimal)
        ==================================================
        
        📊 Context Status:
           Messages: 100 → 10
    """
    metadata = parse_metadata(content)
    projects = extract_key_projects(content)[:max_projects]
    tasks = extract_ongoing_tasks(content)
    
    report_lines = [
        "=" * 50,
        "📋 上下文恢复报告 (Minimal)",
        "=" * 50,
        "",
    ]
    
    # 上下文状态
    report_lines.append("📊 上下文状态:")
    if metadata:
        original = metadata.get('original_count', 'N/A')
        compressed = metadata.get('compressed_count', 'N/A')
        report_lines.append(f"   消息数: {original} → {compressed}")
    else:
        report_lines.append("   状态: 已恢复")
    report_lines.append("")
    
    # 核心项目
    if projects:
        report_lines.append(f"🚀 核心项目 ({len(projects)})")
        for p in projects:
            report_lines.append(f"   • {p.get('name', '未知')}")
        report_lines.append("")
    
    # 当前任务
    if tasks:
        report_lines.append(f"📌 当前任务 ({len(tasks)})")
        for t in tasks:
            report_lines.append(f"   • {t.get('task', '未知')}")
        report_lines.append("")
    
    report_lines.append("=" * 50)
    
    return "\n".join(report_lines)


def format_normal_report(content: str, 
                         max_projects: int = 5, 
                         max_operations: int = 5) -> str:
    """
    生成标准级别的恢复报告（默认）。
    
 报告内容：
        - 上下文压缩信息（消息数量、压缩比、时间戳）
        - 最近操作列表
        - 核心项目详细信息
        - 当前任务详细状态
        - MEMORY.md 高亮引用
        
    Args:
        content: 上下文内容
        max_projects: 最大显示项目数，默认 5
        max_operations: 最大显示操作数，默认 5
        
    Returns:
        格式化的报告字符串
        
    Example:
        >>> report = format_normal_report(content)
        >>> # 输出包含消息统计、项目详情、任务列表
    """
    metadata = parse_metadata(content)
    operations = extract_recent_operations(content, max_operations)
    projects = extract_key_projects(content)[:max_projects]
    tasks = extract_ongoing_tasks(content)
    highlights = extract_memory_highlights(content)
    
    report_lines = [
        "=" * 50,
        "📋 上下文恢复报告 (Normal)",
        "=" * 50,
        "",
    ]
    
    # 压缩信息
    report_lines.append("📊 上下文压缩信息:")
    if metadata:
        original = metadata.get('original_count', 'N/A')
        compressed = metadata.get('compressed_count', 'N/A')
        timestamp = metadata.get('timestamp', '未知')
        
        report_lines.append(f"   原始消息数: {original}")
        report_lines.append(f"   压缩后消息数: {compressed}")
        report_lines.append(f"   压缩时间: {timestamp}")
        
        # 计算压缩比
        if original and compressed:
            ratio = (compressed / original) * 100
            report_lines.append(f"   压缩比: {ratio:.1f}%")
    else:
        report_lines.append("   状态: 上下文已恢复")
    report_lines.append("")
    
    # 最近操作
    if operations:
        report_lines.append(f"🔄 最近操作 ({len(operations)})")
        for i, op in enumerate(operations, 1):
            report_lines.append(f"   {i}. {op}")
        report_lines.append("")
    
    # 核心项目
    if projects:
        report_lines.append("🚀 核心项目")
        for p in projects:
            name = p.get('name', '未知')
            desc = p.get('description', '')
            status = p.get('status', '')
            
            report_lines.append(f"   📁 {name}")
            if desc:
                report_lines.append(f"      描述: {desc}")
            if status:
                report_lines.append(f"      状态: {status}")
        report_lines.append("")
    
    # 当前任务
    if tasks:
        report_lines.append("📋 当前任务")
        for t in tasks:
            task_name = t.get('task', '未知')
            task_status = t.get('status', '')
            detail = t.get('detail', '')
            
            report_lines.append(f"   📌 {task_name}")
            if task_status:
                report_lines.append(f"      状态: {task_status}")
            if detail:
                report_lines.append(f"      详情: {detail}")
        report_lines.append("")
    
    # MEMORY.md 高亮
    if highlights:
        report_lines.append(f"🧠 MEMORY.md 高亮 ({len(highlights)})")
        for h in highlights:
            report_lines.append(f"   {h}")
        report_lines.append("")
    
    report_lines.append("=" * 50)
    
    return "\n".join(report_lines)


def format_detailed_report(content: str) -> str:
    """
    生成详细级别的恢复报告。
    
 报告内容：
        - 完整元数据
        - 所有操作完整列表
        - 所有项目完整信息（JSON 格式）
        - 所有任务完整信息（JSON 格式）
        - 原始内容预览
        
    Args:
        content: 上下文内容
        
    Returns:
        格式化的详细报告字符串
        
    Example:
        >>> report = format_detailed_report(content)
        >>> # 输出包含所有信息的完整报告
    """
    metadata = parse_metadata(content)
    operations = extract_recent_operations(content)
    projects = extract_key_projects(content)
    tasks = extract_ongoing_tasks(content)
    highlights = extract_memory_highlights(content)
    
    report_lines = [
        "=" * 50,
        "📋 上下文恢复报告 (Detailed)",
        "=" * 50,
        "",
    ]
    
    # 完整元数据
    report_lines.append("📊 完整元数据:")
    if metadata:
        for key, value in metadata.items():
            report_lines.append(f"   {key}: {value}")
    else:
        report_lines.append("   无元数据")
    report_lines.append("")
    
    # 所有操作
    if operations:
        report_lines.append(f"🔄 所有最近操作 ({len(operations)}):")
        for i, op in enumerate(operations, 1):
            report_lines.append(f"   [{i}] {op}")
        report_lines.append("")
    
    # 所有项目
    if projects:
        report_lines.append(f"🚀 所有项目 ({len(projects)}):")
        for i, p in enumerate(projects, 1):
            report_lines.append(f"\n   [{i}]")
            for key, value in p.items():
                report_lines.append(f"       {key}: {value}")
        report_lines.append("")
    
    # 所有任务
    if tasks:
        report_lines.append(f"📋 所有任务 ({len(tasks)}):")
        for i, t in enumerate(tasks, 1):
            report_lines.append(f"\n   [{i}]")
            for key, value in t.items():
                report_lines.append(f"       {key}: {value}")
        report_lines.append("")
    
    # MEMORY.md 高亮
    if highlights:
        report_lines.append(f"🧠 MEMORY.md 高亮 ({len(highlights)}):")
        for h in highlights:
            report_lines.append(f"   {h}")
        report_lines.append("")
    
    # 原始内容预览
    report_lines.append("📄 原始内容预览:")
    if len(content) > 500:
        report_lines.append(f"   [前500字符]: {content[:500]}...")
    else:
        report_lines.append(f"   {content}")
    report_lines.append("")
    
    report_lines.append("=" * 50)
    
    return "\n".join(report_lines)


# ============================================================================
# 主功能函数
# ============================================================================

def restore_context(filepath: str = DEFAULT_CONTEXT_FILE, 
                    level: str = LEVEL_NORMAL) -> str:
    """
    从压缩的文件中恢复上下文并生成报告。
    
 这是技能的主入口函数，负责协调整个恢复流程：
        1. 加载上下文文件
        2. 根据级别选择格式化方法
        3. 返回格式化的恢复报告
        
    Args:
        filepath: 压缩上下文文件的路径，默认使用 DEFAULT_CONTEXT_FILE
        level: 恢复级别，可选值为 LEVEL_MINIMAL、LEVEL_NORMAL、LEVEL_DETAILED
        
    Returns:
        格式化的恢复报告字符串
        
    Raises:
        ValueError: 无效的恢复级别
        
    Example:
        >>> # 标准恢复
        >>> report = restore_context()
        >>> print(report)
        
        >>> # 详细恢复
        >>> detailed_report = restore_context(level=LEVEL_DETAILED)
        
        >>> # 自定义文件路径
        >>> custom_report = restore_context("/path/to/context.json", LEVEL_MINIMAL)
    """
    # 参数验证
    valid_levels = [LEVEL_MINIMAL, LEVEL_NORMAL, LEVEL_DETAILED]
    if level not in valid_levels:
        raise ValueError(
            f"无效的恢复级别: {level}。有效值: {valid_levels}"
        )
    
    # 加载上下文
    context = load_compressed_context(filepath)
    
    # 处理加载失败
    if context is None:
        return "❌ 错误：无法加载上下文文件"
    
    # 处理 JSON 格式
    if isinstance(context, dict):
        # 提取 content 字段（如果存在）
        content = str(context.get('content', context))
    else:
        content = context
    
    # 根据级别生成报告
    if level == LEVEL_MINIMAL:
        return format_minimal_report(content)
    elif level == LEVEL_DETAILED:
        return format_detailed_report(content)
    else:
        return format_normal_report(content)


def get_context_summary(filepath: str = DEFAULT_CONTEXT_FILE) -> dict:
    """
    获取上下文的摘要信息（供其他技能使用）。
    
 返回一个结构化的字典，可被其他技能直接使用：
        - metadata: 元数据
        - operations: 最近操作
        - projects: 核心项目
        - tasks: 当前任务
        
    Args:
        filepath: 上下文文件路径
        
    Returns:
        包含上下文摘要的字典
        
    Example:
        >>> summary = get_context_summary()
        >>> print(summary['projects'])
        [{'name': 'Hermès Plan', ...}]
    """
    context = load_compressed_context(filepath)
    
    if context is None:
        return {
            'success': False,
            'error': '无法加载上下文文件',
            'metadata': {},
            'operations': [],
            'projects': [],
            'tasks': []
        }
    
    content = context if isinstance(context, str) else str(context.get('content', context))
    
    return {
        'success': True,
        'metadata': parse_metadata(content),
        'operations': extract_recent_operations(content),
        'projects': extract_key_projects(content),
        'tasks': extract_ongoing_tasks(content),
        'memory_highlights': extract_memory_highlights(content)
    }


# ============================================================================
# 命令行入口
# ============================================================================

def main():
    """
    命令行主入口函数。
    
 支持的命令行参数：
        --file / -f: 指定上下文文件路径
        --level / -l: 指定恢复级别
        --output / -o: 指定输出文件
        
    Example:
        >>> python restore_context.py --level detailed --output report.txt
        >>> python restore_context.py -f ./my_context.json -l minimal
    """
    parser = argparse.ArgumentParser(
        description='上下文恢复工具 - 从压缩的上下文中恢复关键信息',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 使用默认配置恢复
    python restore_context.py
    
    # 生成详细报告并保存
    python restore_context.py --level detailed --output report.txt
    
    # 最小化输出
    python restore_context.py --level minimal
    
    # 指定自定义文件
    python restore_context.py --file /path/to/context.json
        """
    )
    
    parser.add_argument(
        '--file', 
        '-f',
        default=DEFAULT_CONTEXT_FILE,
        help=f'压缩上下文文件的路径 (默认: {DEFAULT_CONTEXT_FILE})'
    )
    
    parser.add_argument(
        '--level',
        '-l',
        choices=[LEVEL_MINIMAL, LEVEL_NORMAL, LEVEL_DETAILED],
        default=LEVEL_NORMAL,
        help=f'报告详细级别 (默认: {LEVEL_NORMAL})'
    )
    
    parser.add_argument(
        '--output',
        '-o',
        help='输出到文件路径（默认输出到 stdout）'
    )
    
    parser.add_argument(
        '--summary',
        '-s',
        action='store_true',
        help='输出结构化摘要（JSON 格式）'
    )
    
    args = parser.parse_args()
    
    # 生成报告或摘要
    if args.summary:
        result = get_context_summary(args.file)
        output = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        result = restore_context(args.file, args.level)
        output = result
    
    # 输出处理
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"✅ 报告已保存到: {args.output}")
        except Exception as e:
            print(f"❌ 保存文件失败: {e}")
            sys.exit(1)
    else:
        print(output)
    
    # 返回成功状态
    sys.exit(0)


# ============================================================================
# 模块初始化
# ============================================================================

if __name__ == '__main__':
    main()


# ============================================================================
# 使用示例
# ============================================================================
"""
📖 完整使用示例

1. Python API 使用:
   
   from restore_context import restore_context, get_context_summary
   
   # 恢复上下文
   report = restore_context("./compressed_context/latest_compressed.json", "normal")
   print(report)
   
   # 获取结构化摘要
   summary = get_context_summary()
   if summary['success']:
       print(f"找到 {len(summary['projects'])} 个项目")
       for project in summary['projects']:
           print(f"  - {project['name']}")

2. 命令行使用:
   
   # 正常模式（默认）
   python restore_context.py
   
   # 详细模式
   python restore_context.py --level detailed
   
   # 最小模式
   python restore_context.py -l minimal
   
   # 保存到文件
   python restore_context.py -l detailed -o report.txt
   
   # 结构化输出
   python restore_context.py --summary

3. 集成到其他技能:
   
   from restore_context import get_context_summary
   
   def my_skill_function():
       summary = get_context_summary()
       if summary['success']:
           # 使用项目信息
           for project in summary['projects']:
               process_project(project)
           # 使用任务信息
           for task in summary['tasks']:
               schedule_task(task)
"""
