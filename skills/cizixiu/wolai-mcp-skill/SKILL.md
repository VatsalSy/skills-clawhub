---
name: wolai-mcp
description: 通过 wolai MCP 协议操作 wolai 笔记（MCP 版本）。支持读取页面/大纲/块内容、创建/删除/更新文档、搜索文档、Section 级编辑、块级精确操作、多栏布局等。比 API 版本功能更强大，支持删除、修改、搜索等 API 版本不支持的操作。当用户配置了 WOLAI_MCP_TOKEN 时优先使用此 skill。触发场景：「读取 wolai 页面」、「搜索 wolai 文档」、「删除 wolai 页面」、「修改 wolai 内容」、「存入 wolai 笔记」等。
---

# wolai MCP Skill

通过 wolai 官方 MCP 协议操作笔记，功能全面，支持读取、写入、搜索、删除、修改等所有操作。

MCP 服务地址：`https://api.wolai.com/v1/mcp`

---

## Setup

### 1. 获取 MCP Token

1. 打开 https://www.wolai.com/dev
2. 创建应用（或使用已有应用）
3. 在应用详情页找到 **MCP Token**（以 `sk-` 开头）
4. 复制 Token

### 2. 配置环境变量

告诉 AI 助手：
> 「帮我配置 wolai MCP Token，Token 是 sk-xxxxxx」

AI 会自动写入 `WOLAI_MCP_TOKEN` 环境变量。

---

## 凭证预检

```powershell
if (-not $env:WOLAI_MCP_TOKEN) {
    Write-Host "缺少 WOLAI_MCP_TOKEN，请按 Setup 步骤配置"
    exit 1
}
```

---

## 核心调用函数

```powershell
function Invoke-WolaiMcp {
    param(
        [string]$Tool,
        [hashtable]$Args = @{}
    )
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.Encoding]::UTF8

    $headers = @{
        "Authorization" = "Bearer $env:WOLAI_MCP_TOKEN"
        "Content-Type"  = "application/json"
        "Accept"        = "application/json, text/event-stream"
    }
    $bodyObj = @{
        jsonrpc = "2.0"
        id      = 1
        method  = "tools/call"
        params  = @{ name = $Tool; arguments = $Args }
    }
    $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes(($bodyObj | ConvertTo-Json -Depth 10))
    $raw = Invoke-RestMethod -Method POST `
        -Uri "https://api.wolai.com/v1/mcp" `
        -Headers $headers -Body $bodyBytes

    # 解析 SSE 响应
    $dataLine = ($raw -split "`n" | Where-Object { $_ -match "^data:" } | Select-Object -First 1)
    $json = $dataLine -replace "^data:\s*", ""
    $result = $json | ConvertFrom-Json
    # 提取 data 内容
    $text = $result.result.content[0].text
    return $text | ConvertFrom-Json
}
```

---

## 工具决策表

| 用户意图 | 优先工具 | 备注 |
|---------|---------|------|
| 列出所有文档 | `list_docs` | |
| 读取页面结构 | `get_page_outline` | 轻量，先用这个 |
| 读取某章节内容 | `get_section_content` | 配合 outline 使用 |
| 定位某个章节 | `locate_section` | 自然语言描述位置 |
| 读取完整页面块 | `get_page_blocks` | 最后手段 |
| 搜索文档 | `search_docs` | 按标题关键词 |
| 创建新页面 | `create_doc` | |
| 更新页面标题/封面 | `update_doc` | |
| 删除页面 | `delete_doc` | 默认移入回收站 |
| 在标题下追加内容 | `insert_under_heading` | 最常用写入方式 |
| 重写某章节 | `rewrite_section` | |
| 移动章节 | `move_section` | |
| 删除章节 | `delete_section` | |
| 精确插入块 | `insert_blocks_relative` | |
| 修改块内容 | `patch_block_content` | |
| 替换块 | `replace_block` | |
| 删除块 | `delete_block` | |
| 创建多栏布局 | `create_column_layout` | 2-5 栏 |

---

## 常用工作流

### 读取页面内容

```powershell
$pageId = "xxx"  # 从 URL 获取

# 第一步：获取大纲（轻量）
$outline = Invoke-WolaiMcp -Tool "get_page_outline" -Args @{ page_id = $pageId }

# 第二步：按需读取某个 section
$section = Invoke-WolaiMcp -Tool "get_section_content" -Args @{
    page_id    = $pageId
    section_id = "section_id_from_outline"
}
```

### 搜索文档

```powershell
$results = Invoke-WolaiMcp -Tool "search_docs" -Args @{ query = "会议纪要"; limit = 10 }
$results.data | ForEach-Object { "$($_.id) | $($_.title)" }
```

### 创建新页面并写入内容

```powershell
# 创建页面
$doc = Invoke-WolaiMcp -Tool "create_doc" -Args @{
    parent_id = "父页面ID"
    title     = "新页面标题"
}
$newPageId = $doc.data.id

# 写入内容（先获取大纲找到合适位置）
$outline = Invoke-WolaiMcp -Tool "get_page_outline" -Args @{ page_id = $newPageId }
```

### 在页面末尾追加内容

```powershell
# 定位末尾 section
$loc = Invoke-WolaiMcp -Tool "locate_section" -Args @{
    page_id = "xxx"
    query   = "底部最后一个章节"
}
$sectionId = ($loc.data.sections | Select-Object -Last 1).section_id

# 追加内容
Invoke-WolaiMcp -Tool "insert_under_heading" -Args @{
    page_id           = "xxx"
    target_section_id = $sectionId
    placement         = "append_inside"
    blocks            = @(@{ type = "text"; content = "追加的内容" })
}
```

### 修改块内容

```powershell
# 替换全部内容
Invoke-WolaiMcp -Tool "patch_block_content" -Args @{
    block_id = "xxx"
    patches  = @(@{ op = "replace_all"; content = "新内容" })
}

# 替换指定文字
Invoke-WolaiMcp -Tool "patch_block_content" -Args @{
    block_id = "xxx"
    patches  = @(@{ op = "replace_text"; old_text = "旧文字"; new_text = "新文字" })
}
```

### 删除页面

```powershell
# 移入回收站（可恢复）
Invoke-WolaiMcp -Tool "delete_doc" -Args @{ doc_id = "xxx" }

# 永久删除
Invoke-WolaiMcp -Tool "delete_doc" -Args @{ doc_id = "xxx"; forever = $true }
```

---

## 块类型说明（create_block / rewrite_section / insert_under_heading 通用）

### 文本类
```json
{ "type": "text",         "content": "普通文本" }
{ "type": "heading",      "content": "标题文字", "level": 1 }
{ "type": "quote",        "content": "引用内容" }
{ "type": "callout",      "content": "提示内容", "icon": {"type": "emoji", "icon": "💡"} }
{ "type": "bull_list",    "content": "无序列表项" }
{ "type": "enum_list",    "content": "有序列表项" }
{ "type": "toggle_list",  "content": "折叠块标题" }
{ "type": "todo_list",    "content": "待办事项", "checked": false }
{ "type": "todo_list_pro","content": "任务", "task_status": "todo" }
{ "type": "divider" }
```

### 代码
```json
{ "type": "code", "content": "print('hello')", "language": "python" }
```

### 媒体 / 嵌入
```json
{ "type": "image",    "link": "https://..." }
{ "type": "bookmark", "link": "https://..." }
{ "type": "embed",    "original_link": "https://..." }
```

### 表格
```json
{
  "type": "simple_table",
  "table_content": [["列1","列2"],["值1","值2"]],
  "table_setting": { "has_header": true }
}
```

### 子页面
```json
{ "type": "page", "content": "子页面标题", "icon": {"type": "emoji", "icon": "📄"} }
```

### 富文本 content 格式（带样式）
```json
[
  { "title": "普通文字" },
  { "title": "加粗文字", "bold": true },
  { "title": "斜体",     "italic": true },
  { "title": "链接文字", "link": "https://..." },
  { "title": "红色文字", "front_color": "red" },
  { "title": "代码",     "inline_code": true }
]
```

---

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| 401 Unauthorized | Token 无效或过期 | 检查 WOLAI_MCP_TOKEN |
| 403 Forbidden | 无页面权限 | 在页面协作中添加应用权限 |
| 404 Not Found | 页面/块 ID 不存在 | 检查 ID 是否正确 |
| 429 Too Many Requests | 请求过于频繁 | 降低调用频率 |

---

## 注意事项

- 页面 ID 从 URL 获取：`wolai.com/` 后面的部分
- MCP Token 以 `sk-` 开头，与 REST API Token（32位hex）不同
- 读取大页面时先用 `get_page_outline`，再按需读取 section，避免 token 浪费
- `delete_doc` 默认移入回收站，`forever: true` 才是永久删除，谨慎使用
- 团队空间页面需在「页面协作 → 应用权限」中添加应用
