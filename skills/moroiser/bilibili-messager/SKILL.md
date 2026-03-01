---
name: bilibili-messager
description: "Bilibili private messaging via browser automation. B站私信发送，通过浏览器自动化发送私信。Use when user needs to send B站私信、回复消息。Requires browser login."
metadata: {"openclaw": {"emoji": "📺", "requires": {"config": ["browser.enabled"]}}}
---

# Bilibili Private Messaging

通过浏览器自动化发送B站私信。

## ⚠️ 执行模式

**重要：连续执行所有步骤，中途不要停止！**

## ⚠️ 减少快照

快照数据量大，可能导致网络超时。**只在必要时获取快照：**
- 第一次：打开页面后，需要找到用户
- 最后一次：发送后确认结果

**点击后不需要快照，直接发送消息！**

## 前置条件

- 用户需要在浏览器中已登录 B站账号
- 需要知道目标用户的用户名（支持部分匹配）

## 操作流程

### 步骤 1：打开页面

```
browser action=open targetUrl=https://message.bilibili.com/#/whisper
```

### 步骤 2：获取快照，找到用户

```
browser action=snapshot
```

在快照中找到目标用户（按用户名部分匹配），记录 ref。

### 步骤 3：点击进入对话

```
browser action=act request={"kind": "click", "ref": "<用户ref>"}
```

### 步骤 4：直接发送消息（不要获取快照！）

**点击后立即用 JavaScript 发送，不要再获取快照：**

```javascript
() => {
  const inputArea = document.querySelector('[contenteditable="true"]');
  if (inputArea) {
    inputArea.textContent = '消息内容';
    inputArea.dispatchEvent(new InputEvent('input', { bubbles: true }));
    const sendBtn = document.evaluate(
      "//div[contains(text(), '发送')]", 
      document, 
      null, 
      XPathResult.FIRST_ORDERED_NODE_TYPE, 
      null
    ).singleNodeValue;
    if (sendBtn) sendBtn.click();
    return 'Message sent';
  }
  return 'Input not found';
}
```

### 步骤 5：获取快照确认发送成功

```
browser action=snapshot
```

确认消息已出现在聊天记录中，然后向用户报告结果。

## 注意事项

- 消息长度限制：500字符
- 发送频率有限制，避免刷屏
- 如果找不到用户，先向用户确认用户名是否正确
