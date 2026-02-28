import os
import json
from pathlib import Path

class PaperEngineer:
    def __init__(self, base_path="/Users/chenkuan/Desktop/毕业论文"):
        self.base_path = Path(base_path)
        self.structs_path = self.base_path / "structs.json"
        self.summaries_path = self.base_path / "summaries.json"
        self.body_dir = self.base_path / "论文正文"

    def ensure_dirs(self):
        """确保必要目录存在"""
        self.body_dir.mkdir(parents=True, exist_ok=True)
        (self.base_path / "已处理文献").mkdir(parents=True, exist_ok=True)

    def update_summary_from_body(self, section_id: str, new_content: str):
        """
        当正文层文件被修改后，调用此函数来更新总结层。
        这是一个简化示例，实际需要更复杂的内容分析。
        """
        if not self.summaries_path.exists():
            return "总结层文件不存在，请先初始化。"

        with open(self.summaries_path, 'r', encoding='utf-8') as f:
            summaries = json.load(f)

        # 这里应实现查找对应section_id并更新其section_summary的逻辑
        # 以及一个简单的内容摘要生成算法
        # updated = some_summarize_function(new_content)
        # ...

        with open(self.summaries_path, 'w', encoding='utf-8') as f:
            json.dump(summaries, f, ensure_ascii=False, indent=2)
        return f"已尝试根据正文更新总结层节点 {section_id}。"

    # 可以在此添加更多函数，如：generate_framework, parse_pdf, merge_final_draft 等

# 供OpenClaw Gateway调用的主要异步函数
async def sync_on_body_change(section_id: str, new_content: str):
    engineer = PaperEngineer()
    result = engineer.update_summary_from_body(section_id, new_content)
    return result

async def initialize_project():
    engineer = PaperEngineer()
    engineer.ensure_dirs()
    return f"项目目录已就绪于: {engineer.base_path}"