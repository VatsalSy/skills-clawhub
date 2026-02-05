---
name: tg-history
description: Efficiently extract and read Telegram group chat history as text, bypassing screenshots/OCR for zero-token-waste.
metadata:
  {
    "openclaw": {
      "requires": { "plugins": ["browser"] }
    }
  }
---

# tg-history Skill

极速、省钱的 Telegram 聊天记录读取工具。

## 功能
- **直接提取文本**：不通过截图或 OCR，直接从网页 DOM 中抓取聊天记录。
- **Token 暴减**：相比截图，Token 消耗降低 99% 以上。
- **精准格式**：自动整理为 `[时间] 发送者: 消息内容` 的清爽格式。

## 使用方法
直接对 AI 说：
- "帮我看看 [群名] 的聊天记录"
- "总结一下 [群名] 最近聊了什么"
- "运行 tg-history 获取 [群名] 历史"

## 优势
传统的“截图+AI识别”方案，一张图就要几千个像素数据；而 `tg-history` 直接读取网页上的文字，一段几百字的聊天记录只占用几百个字节的 Token。
