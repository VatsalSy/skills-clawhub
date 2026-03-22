#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc-extract-filter - 文件处理技能封装脚本

支持 PDF、Word、Excel 文件的文本提取和关键词筛选
适配 OpenClaw 和 CoPaw 智能体调用规范
"""

import os
import sys
import json
import logging
import click
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.extractor import FileExtractor
from core.filter import ContentFilter

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DocExtractFilter:
    """
    文件处理技能类
    """
    
    @staticmethod
    def process(file_path, action, keywords=None):
        """
        处理文件操作
        
        Args:
            file_path: 文件路径
            action: 操作类型，extract 或 filter
            keywords: 关键词列表，仅 filter 操作需要
            
        Returns:
            结构化 JSON 格式的结果
        """
        try:
            # 验证文件路径
            file_path = Path(file_path)
            if not file_path.exists():
                return {
                    "success": False,
                    "data": {},
                    "error": f"文件不存在: {file_path}"
                }
            
            # 初始化提取器和筛选器
            extractor = FileExtractor()
            filter = ContentFilter()
            
            # 提取文本
            extract_result = extractor.extract_text(file_path)
            
            if "error" in extract_result:
                return {
                    "success": False,
                    "data": {},
                    "error": extract_result["error"]
                }
            
            text = extract_result.get("text", "")
            
            # 根据操作类型处理
            if action == "extract":
                return {
                    "success": True,
                    "data": {
                        "text": text
                    },
                    "error": ""
                }
            elif action == "filter":
                if not keywords:
                    return {
                        "success": False,
                        "data": {},
                        "error": "filter 操作需要提供关键词"
                    }
                
                # 筛选关键词
                filter_result = filter.filter_by_keyword(text, keywords)
                
                if filter_result.get("status") != "success":
                    return {
                        "success": False,
                        "data": {},
                        "error": filter_result.get("error", "筛选失败")
                    }
                
                # 构建筛选后的文本
                filtered_text = ""
                for result in filter_result.get("results", []):
                    filtered_text += f"关键词: {result['keyword']}\n"
                    filtered_text += f"匹配: {result['match']}\n"
                    filtered_text += f"上下文: {result['context']}\n"
                    filtered_text += "-" * 80 + "\n"
                
                return {
                    "success": True,
                    "data": {
                        "text": text,
                        "filtered_text": filtered_text,
                        "matches": filter_result.get("results", []),
                        "total_matches": filter_result.get("total_matches", 0)
                    },
                    "error": ""
                }
            else:
                return {
                    "success": False,
                    "data": {},
                    "error": f"不支持的操作类型: {action}"
                }
                
        except Exception as e:
            logger.error(f"处理文件时出错: {str(e)}")
            return {
                "success": False,
                "data": {},
                "error": str(e)
            }


@click.command()
@click.option('--file_path', required=True, help='文件路径')
@click.option('--action', required=True, type=click.Choice(['extract', 'filter']), help='操作类型')
@click.option('--keywords', help='关键词列表，逗号分隔')
def cli(file_path, action, keywords):
    """
    命令行接口
    """
    # 处理关键词参数
    keyword_list = []
    if keywords:
        keyword_list = [k.strip() for k in keywords.split(',')]
    
    # 调用处理函数
    result = DocExtractFilter.process(file_path, action, keyword_list)
    
    # 输出 JSON 格式结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    cli()
