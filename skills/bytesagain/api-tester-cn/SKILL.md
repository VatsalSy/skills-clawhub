---
name: api-tester-cn
version: 1.0.0
description: "API请求构造、curl命令生成、Mock数据、API文档、HTTP状态码速查、Headers说明。API request builder, curl generator, mock data, API documentation, HTTP status codes, headers reference."
tags: [api, http, curl, rest, developer-tools, 开发工具, mock, 接口测试]
author: BytesAgain
homepage: https://bytesagain.com
---

# API Tester — API 测试助手

API请求构造、curl命令生成、Mock数据生成、API文档撰写、HTTP状态码速查、Headers说明。

## 使用方式

Agent 根据用户需求，运行对应脚本命令，获取提示词后执行任务。

### 可用命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `request` | 构造API请求 | "帮我构造一个POST请求" |
| `curl` | 生成curl命令 | "帮我写个curl命令" |
| `mock` | 生成Mock数据 | "生成用户列表的Mock数据" |
| `doc` | 编写API文档 | "帮我写个API接口文档" |
| `status` | HTTP状态码速查 | "404是什么意思" |
| `headers` | HTTP Headers说明 | "Content-Type有哪些值" |

### 运行方式

```bash
bash scripts/api.sh <command>
```

## 触发关键词

api、接口、curl、http、rest、restful、请求、mock、接口文档、状态码、status code、headers、请求头、post请求、get请求、api测试、接口测试
