# doc-extract-filter

## 元数据

### 基本信息
- **name**: doc-extract-filter
- **description**: 文件处理技能，支持 PDF、Word、Excel 文件的文本提取和关键词筛选
- **version**: 1.0.0
- **author**: file-agent team
- **license**: MIT-0

### OpenClaw 配置
```json
{
  "name": "doc-extract-filter",
  "description": "文件处理技能，支持 PDF、Word、Excel 文件的文本提取和关键词筛选",
  "version": "1.0.0",
  "author": "file-agent team",
  "license": "MIT-0",
  "type": "tool",
  "entry_point": "scripts/doc-extract-filter.py",
  "parameters": {
    "file_path": {
      "type": "string",
      "description": "文件路径",
      "required": true
    },
    "action": {
      "type": "string",
      "description": "操作类型：extract 或 filter",
      "required": true
    },
    "keywords": {
      "type": "array",
      "description": "关键词列表（仅 filter 操作需要）",
      "required": false
    }
  }
}
```

### CoPaw 配置
```yaml
name: doc-extract-filter
description: 文件处理技能，支持 PDF、Word、Excel 文件的文本提取和关键词筛选
version: 1.0.0
author: file-agent team
license: MIT-0
type: tool
entry_point: scripts/doc-extract-filter.py
parameters:
  file_path:
    type: string
    description: 文件路径
    required: true
  action:
    type: string
    description: 操作类型：extract 或 filter
    required: true
  keywords:
    type: array
    description: 关键词列表（仅 filter 操作需要）
    required: false
```

## 使用说明

### 功能
- **extract**: 提取文件中的文本内容
- **filter**: 提取文件中的文本并筛选包含指定关键词的内容

### 调用方式

#### CLI 调用
```bash
python scripts/doc-extract-filter.py --file_path "path/to/file.pdf" --action "extract"
python scripts/doc-extract-filter.py --file_path "path/to/file.pdf" --action "filter" --keywords "关键词1,关键词2"
```

#### Python 函数调用
```python
from scripts.doc_extract_filter import DocExtractFilter

# 提取文本
result = DocExtractFilter.process("path/to/file.pdf", "extract")

# 筛选关键词
result = DocExtractFilter.process("path/to/file.pdf", "filter", ["关键词1", "关键词2"])
```

### 返回格式
```json
{
  "success": true,
  "data": {
    "text": "提取的文本内容",
    "filtered_text": "筛选后的文本内容" // 仅 filter 操作返回
  },
  "error": ""
}
```

### 错误处理
- 文件不存在：返回错误信息
- 不支持的文件类型：返回错误信息
- 操作失败：返回错误信息

## 安装与测试

### 安装
1. 将 `doc-extract-filter` 目录复制到 OpenClaw/CoPaw 的 skills 目录
2. 运行 `pip install -r requirements.txt` 安装依赖

### 测试
使用 `docs/test.pdf` 文件测试功能：
```bash
# 测试提取文本
python scripts/doc-extract-filter.py --file_path "docs/test.pdf" --action "extract"

# 测试关键词筛选
python scripts/doc-extract-filter.py --file_path "docs/test.pdf" --action "filter" --keywords "单价,小计,总金额"
```

### 独立运行
doc-extract-filter 现在包含了所有必要的核心代码，可以独立运行，不依赖于外部的 src 目录。