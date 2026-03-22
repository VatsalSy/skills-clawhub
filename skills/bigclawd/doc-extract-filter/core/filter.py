# 内容筛选模块
import re
import logging
from typing import Dict, List, Optional, Union, Pattern
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ContentFilter:
    """
    内容筛选器类，支持按关键词和正则表达式筛选文件内容
    """
    
    def __init__(self):
        """
        初始化内容筛选器
        """
        pass
    
    def filter_by_keyword(self, content: Union[str, List[str]], keywords: List[str], 
                         case_sensitive: bool = False) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        """
        按关键词筛选内容
        
        Args:
            content: 要筛选的内容，可以是字符串或字符串列表
            keywords: 关键词列表
            case_sensitive: 是否区分大小写，默认为 False
            
        Returns:
            包含筛选结果的字典
        """
        try:
            results = []
            
            if isinstance(content, str):
                content_list = [content]
            else:
                content_list = content
            
            for idx, text in enumerate(content_list):
                if not isinstance(text, str):
                    continue
                
                for keyword in keywords:
                    if case_sensitive:
                        matches = re.finditer(keyword, text)
                    else:
                        matches = re.finditer(keyword, text, re.IGNORECASE)
                    
                    for match in matches:
                        start = max(0, match.start() - 50)
                        end = min(len(text), match.end() + 50)
                        context = text[start:end].replace('\n', ' ')
                        
                        results.append({
                            "keyword": keyword,
                            "match": match.group(),
                            "context": context,
                            "position": match.start(),
                            "content_index": idx if len(content_list) > 1 else None
                        })
            
            return {
                "status": "success",
                "results": results,
                "total_matches": len(results)
            }
        except Exception as e:
            logger.error(f"关键词筛选时出错: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def filter_by_regex(self, content: Union[str, List[str]], pattern: str) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        """
        按正则表达式筛选内容
        
        Args:
            content: 要筛选的内容，可以是字符串或字符串列表
            pattern: 正则表达式模式
            
        Returns:
            包含筛选结果的字典
        """
        try:
            regex = re.compile(pattern)
            results = []
            
            if isinstance(content, str):
                content_list = [content]
            else:
                content_list = content
            
            for idx, text in enumerate(content_list):
                if not isinstance(text, str):
                    continue
                
                matches = regex.finditer(text)
                for match in matches:
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end].replace('\n', ' ')
                    
                    results.append({
                        "pattern": pattern,
                        "match": match.group(),
                        "context": context,
                        "position": match.start(),
                        "content_index": idx if len(content_list) > 1 else None
                    })
            
            return {
                "status": "success",
                "results": results,
                "total_matches": len(results)
            }
        except re.error as e:
            logger.error(f"正则表达式语法错误: {str(e)}")
            return {
                "status": "error",
                "error": f"正则表达式语法错误: {str(e)}"
            }
        except Exception as e:
            logger.error(f"正则筛选时出错: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def export_results(self, results: Dict, output_file: Union[str, Path]) -> Dict[str, str]:
        """
        导出筛选结果到文件
        
        Args:
            results: 筛选结果字典
            output_file: 输出文件路径
            
        Returns:
            导出结果状态
        """
        try:
            output_file = Path(output_file)
            
            if results.get("status") != "success":
                return {
                    "status": "error",
                    "error": "筛选结果无效"
                }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("# 筛选结果\n\n")
                f.write(f"总匹配数: {results.get('total_matches', 0)}\n\n")
                
                for idx, result in enumerate(results.get('results', [])):
                    f.write(f"匹配 #{idx + 1}:\n")
                    f.write(f"关键词/模式: {result.get('keyword', result.get('pattern', 'N/A'))}\n")
                    f.write(f"匹配内容: {result.get('match', 'N/A')}\n")
                    f.write(f"上下文: {result.get('context', 'N/A')}\n")
                    f.write(f"位置: {result.get('position', 'N/A')}\n")
                    if result.get('content_index') is not None:
                        f.write(f"内容索引: {result.get('content_index')}\n")
                    f.write("-" * 80 + "\n\n")
            
            return {
                "status": "success",
                "output_file": str(output_file)
            }
        except Exception as e:
            logger.error(f"导出结果时出错: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
