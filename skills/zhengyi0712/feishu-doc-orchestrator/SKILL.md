---
name: feishu-doc-orchestrator
description: |
  飞书文档创建与权限管理工作流 - 支持 Markdown 导入、分块添加、权限自动分配。
  用于创建飞书文档(docx)并自动完成权限管理（添加协作者+转移所有权）。
  当用户需要：1) 创建飞书文档并设置权限 2) 将 Markdown 导入飞书 3) 批量处理文档权限 时使用此技能。
---

# 飞书文档创建与权限管理

自动化飞书文档创建工作流，支持 Markdown 导入、智能分块添加、权限自动分配。

## 功能概述

- **文档创建**：从 Markdown 或纯文本创建飞书文档(docx)
- **权限管理**：自动添加协作者并转移所有权
- **智能分块**：自动将内容分割为飞书 API 支持的块类型
- **工作流追踪**：完整的工作流日志和状态追踪

## 快速开始

### 场景1：创建文档并自动分配权限

```python
# 创建新文档并自动给用户添加权限
result = feishu_doc_create_with_permission(
    title="我的文档",
    collaborator_id="ou_xxx",  # 用户 open_id
    perm="full_access"  # 权限级别
)
# 返回: {"document_id": "xxx", "document_url": "https://feishu.cn/docx/xxx", "permission_status": {...}}
```

### 场景2：Markdown 导入飞书

```bash
# 使用编排器完整工作流
python scripts/orchestrator.py input.md "文档标题" "run-name"

# 工作流步骤：
# 1. 解析 Markdown → 块结构
# 2. 创建文档 + 权限设置
# 3. 添加内容块
# 4. 验证文档
# 5. 记录日志
```

### 场景3：给现有文档添加权限

```python
# 添加协作者权限
feishu_perm_add(
    token="doc_id",
    type="docx",
    member_type="openid",
    member_id="ou_xxx",
    perm="full_access"
)

# 转移所有权
feishu_doc_transfer_owner(
    document_id="doc_id",
    new_owner_id="ou_xxx"
)
```

## 详细使用指南

### 智能 Token 模式选择

脚本根据文档标题智能判断使用哪种 Token 模式：

| 标题包含关键词 | 使用的 Token 模式 | 说明 |
|---------------|------------------|------|
| `文件夹`、`用户`、`个人`、`我的` | **user_access_token** | 文档属于用户，无需权限转移 |
| 其他情况 | **tenant_access_token**（默认） | 文档属于应用，需添加协作者权限 |

### 权限级别

- `view` - 仅查看
- `edit` - 可编辑
- `full_access` - 完全访问（可管理权限）

### 工作流目录结构

```
workflow/feishu-doc-runs/run-2026-02-10-143022/
├── step1_parse/              # Markdown 解析结果
│   └── blocks.json
├── step2_create_with_permission/  # 文档创建+权限
│   └── doc_with_permission.json
├── step3_add_blocks/         # 块添加结果
│   └── add_result.json
└── step4_verify/             # 验证结果
    └── verify_result.json
```

## 脚本说明

### scripts/doc_creator_with_permission.py

**功能**：创建文档并自动完成权限管理（原子操作）

**使用方式**：
```bash
# 默认模式（Tenant Token）
python scripts/doc_creator_with_permission.py "产品需求文档"

# User Token 模式（检测到关键词）
python scripts/doc_creator_with_permission.py "我的个人笔记"

# 强制使用 User Token
python scripts/doc_creator_with_permission.py "测试文档" --user-token
```

**输出**：`output/doc_with_permission.json`

### scripts/orchestrator.py

**功能**：完整工作流编排（5步骤）

**使用方式**：
```bash
python scripts/orchestrator.py <markdown文件> [文档标题] [运行名称]

# 示例
python scripts/orchestrator.py input.md "我的文档" "test-run-01"
```

### scripts/add_permission.py

**功能**：给现有文档添加权限并转移所有权

**使用方式**：
```bash
python scripts/add_permission.py <文档ID> <用户open_id>

# 示例
python scripts/add_permission.py xxxxxxxxxxxxxxxxxxxx ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 配置要求

### 必需配置

在 `.claude/feishu-config.env` 中配置：

```env
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_API_DOMAIN=https://open.feishu.cn
FEISHU_WEB_DOMAIN=https://feishu.cn
FEISHU_AUTO_COLLABORATOR_ID=ou_xxx  # 默认协作者ID
FEISHU_AUTO_COLLABORATOR_TYPE=openid
FEISHU_AUTO_COLLABORATOR_PERM=full_access
FEISHU_DEFAULT_FOLDER=fldcnxxx  # 可选，默认文件夹
```

### OAuth 授权（User Token 模式需要）

运行自动授权脚本：

```bash
python scripts/auto_auth.py
```

此脚本会自动：
1. 启动本地服务器接收回调
2. 打开浏览器飞书授权页面
3. 自动捕获授权码
4. 获取并保存 token 到 `.claude/feishu-token.json`

## 依赖安装

```bash
# 必需依赖
pip install requests lark-oapi
```

## API 参考

### 支持的块类型

- 标题 (Heading1-9)
- 文本 (Text)
- 无序列表 (Bullet)
- 有序列表 (Numbered)
- 引用 (Quote)
- 代码块 (Code)
- 分割线 (Divider)
- 表格 (Table)
- 图片 (Image) - 通过 URL

详细块类型定义参见 `references/block_types.md`

## 故障排除

### 常见问题

**Q: 添加权限失败，提示 "Permission denied"**
- 确保使用 tenant_access_token 添加协作者
- 检查文档ID是否正确
- 确认应用有 `drive:permission` 权限

**Q: 转移所有权失败**
- 确保 user_access_token 有效且未过期
- 检查是否具有转移所有权的权限
- 确认 lark-oapi SDK 已安装

**Q: 文档创建成功但内容为空**
- 检查 blocks.json 是否正确生成
- 确认块类型和格式符合飞书 API 要求
- 查看 step3_add_blocks/add_result.json 错误日志

## 注意事项

1. **Token 类型必须一致**：文档创建和块添加必须使用相同类型的 Token
2. **Tenant Token 创建后必须立即添加协作者**：否则后续的块添加会因权限不足而失败
3. **User Token 需要先授权**：确保运行 auto_auth.py 完成授权流程

## 相关资源

- [飞书开放平台和权限管理 API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/drive-v1/permission-member/create)
- [飞书文档块类型 API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/docx-v1/document-block/overview)
