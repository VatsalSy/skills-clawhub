---
name: mcdonald-order
description: 麦当劳助手 - 查询/领取优惠券、活动日历、餐品营养信息、门店查询、查询/创建外送地址、查询/创建外送订单、查询门店可用优惠券、查询餐品列表、查询餐品详情
version: 1.0.0
author: developer
metadata: {"openclaw": {"emoji": "🍔", "category": "lifestyle", "tags": ["麦当劳", "优惠券", "美食", "快餐"]}}
---

# 🍔 麦当劳助手

当用户询问麦当劳相关问题时，使用此 skill 调用麦当劳 MCP 服务获取实时数据。

## 适用场景

- 查询/领取优惠券
- 查看活动日历
- 查询餐品营养信息
- 搭配指定热量套餐
- 查询/创建外送地址
- 查询/创建外送订单
- 查询门店可用优惠券
- 查询餐品列表
- 查询餐品详情

## 配置要求

### 必需配置
用户需要在 MCP 官网注册并获取 API Token：
- 访问 https://mcp.mcd.cn 获取 Token
- 设置环境变量 `MCD_TOKEN` 或在调用时替换 `<YOUR_TOKEN>`

### 可选配置
- `MCD_MCP_URL`: MCP 服务地址，默认 `https://mcp.mcd.cn`

## 调用方式

使用 exec 工具执行 curl 命令调用 MCP 服务：

```bash
MCD_URL="${MCD_MCP_URL:-https://mcp.mcd.cn}"
MCD_AUTH="Authorization: Bearer ${MCD_TOKEN:-<YOUR_TOKEN>}"

curl -s -X POST "$MCD_URL" \
  -H "$MCD_AUTH" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"<工具名>","arguments":{<参数>}},"id":1}'
```

## 可用工具

### 1. 查询可领优惠券 (available-coupons)

查看当前可领取的所有优惠券。

**触发词**: "有什么优惠券"、"可以领什么券"、"今天有什么优惠"

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"available-coupons","arguments":{}},"id":1}'
```

### 2. 一键领取优惠券 (auto-bind-coupons)

自动领取所有可用优惠券到账户。

**触发词**: "帮我领券"、"一键领券"、"全部领取"

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"auto-bind-coupons","arguments":{}},"id":1}'
```

### 3. 查询我的优惠券 (query-my-coupons)

查看已领取的优惠券列表。

**触发词**: "我有哪些优惠券"、"我的券"、"已领取的券"

**参数**:
- `page`: 页码，默认 "1"
- `pageSize`: 每页数量，默认 "50"

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"my-coupons","arguments":{"page":"1","pageSize":"50"}},"id":1}'
```

### 4. 查询活动日历 (campaign-calender)

查看近期麦当劳活动安排。

**触发词**: "最近有什么活动"、"麦当劳活动"、"促销活动"

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"campaign-calender","arguments":{}},"id":1}'
```

### 5. 查询餐品营养信息 (list-nutrition-foods)

获取麦当劳常见餐品的营养成分数据，包括能量、蛋白质、脂肪、碳水化合物、钠、钙等信息。适用于用户咨询热量、营养或搭配指定热量套餐。

**触发词**: "热量"、"卡路里"、"营养信息"、"多少大卡"、"帮我搭配XX卡的套餐"

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"list-nutrition-foods","arguments":{}},"id":1}'
```

### 6. 查询外送地址 (delivery-query-addresses)

查询用户已保存的配送地址列表，同时返回匹配的门店信息（storeCode、beCode）。这是下单流程的第一步，后续查询餐品、计算价格、创建订单都依赖此接口返回的门店信息。

**触发词**: "我要点外卖"、"麦乐送"、"配送地址"、"送餐到家"

**参数**: 无

**流程说明**:
- 返回结果包含 `addressId`、`storeCode`、`beCode` 等关键字段
- 若用户无地址，引导创建新地址
- 若有多个地址，引导用户选择

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"delivery-query-addresses","arguments":{}},"id":1}'
```

### 7. 创建外送地址 (delivery-create-address)

为用户创建新的配送地址。当用户没有已保存地址或需要配送到新地址时使用。

**触发词**: "添加新地址"、"新的配送地址"、"送到XX"

**参数**（全部必填）:
- `city`: 城市名称，如 "南京市"
- `contactName`: 联系人姓名
- `gender`: 性别，如 "先生"、"女士"
- `phone`: 联系人手机号码（11位，以1开头）
- `address`: 配送地址，如 "清竹园9号楼"
- `addressDetail`: 门牌号，如 "2单元508"

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"delivery-create-address","arguments":{"city":"南京市","contactName":"李明","gender":"先生","phone":"18612345678","address":"清竹园9号楼","addressDetail":"2单元508"}},"id":1}'
```

### 8. 查询门店可用优惠券 (query-store-coupons)

查询用户在当前门店可用的优惠券及券对应的可用商品。**必须先调用 delivery-query-addresses 获取门店信息。**

**触发词**: "这个门店能用什么券"、"有什么优惠券可以用"、"下单前看看优惠"

**参数**（全部必填，来自 delivery-query-addresses 返回）:
- `storeCode`: 门店编码
- `beCode`: BE编码

**前置条件**: 必须已调用 `delivery-query-addresses` 获取 storeCode 和 beCode

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"query-store-coupons","arguments":{"storeCode":"S001","beCode":"BE001"}},"id":1}'
```

### 9. 查询餐品列表 (query-meals)

查询门店可售餐品列表，获取商品 code 用于后续下单。**必须先调用 delivery-query-addresses 获取门店信息。**

**触发词**: "有什么吃的"、"菜单"、"餐品列表"、"想点餐"

**参数**（全部必填，来自 delivery-query-addresses 返回）:
- `storeCode`: 门店编码
- `beCode`: BE编码

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"query-meals","arguments":{"storeCode":"S001","beCode":"BE001"}},"id":1}'
```

### 10. 查询餐品详情 (query-meal-detail)

查询单个餐品的详细信息。**必须先调用 delivery-query-addresses 获取门店信息。**

**触发词**: "这个餐品详情"、"具体介绍一下"、"有什么配料"

**参数**（全部必填）:
- `storeCode`: 门店编码（来自 delivery-query-addresses）
- `beCode`: BE编码（来自 delivery-query-addresses）
- `code`: 餐品编码（来自 query-meals）

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"query-meal-detail","arguments":{"storeCode":"S001","beCode":"BE001","code":"10001"}},"id":1}'
```

### 11. 计算价格 (calculate-price)

计算商品价格（含优惠），用于下单前确认费用。**必须先调用 delivery-query-addresses 获取门店信息。**

**触发词**: "多少钱"、"总价"、"算一下价格"、"用券后多少钱"

**参数**:
- `storeCode`: 门店编码（必填，来自 delivery-query-addresses）
- `beCode`: BE编码（必填，来自 delivery-query-addresses）
- `items`: 商品列表（必填，至少一个商品）
  - `productCode`: 商品编码（必填，来自 query-meals）
  - `quantity`: 数量（必填）
  - `couponId`: 优惠券ID（选填）
  - `couponCode`: 优惠券编码（选填）

**返回字段说明**（金额单位为分，需除以100展示）:
- `productOriginalPrice`: 商品原价
- `productPrice`: 商品现价
- `deliveryPrice`: 运费
- `packingPrice`: 打包费
- `discount`: 总优惠
- `price`: 最终价格

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"calculate-price","arguments":{"storeCode":"S001","beCode":"BE001","items":[{"productCode":"10001","quantity":1}]}},"id":1}'
```

### 12. 创建外送订单 (create-order)

创建麦乐送外卖订单。**必须先调用 delivery-query-addresses 获取地址和门店信息，且必须先调用 calculate-price 计算价格并等待用户确认。**

**触发词**: "下单"、"我要点这个"、"帮我下单"、"创建订单"

**参数**:
- `addressId`: 配送地址ID（必填，来自 delivery-query-addresses）
- `storeCode`: 门店编码（必填，来自 delivery-query-addresses）
- `beCode`: BE编码（必填，来自 delivery-query-addresses）
- `items`: 商品列表（必填，至少一个商品）
  - `productCode`: 商品编码（必填）
  - `quantity`: 数量（必填）
  - `couponId`: 优惠券ID（选填）
  - `couponCode`: 优惠券编码（选填）

**前置条件**: 
1. 必须已调用 `delivery-query-addresses`
2. 必须已调用 `calculate-price` 且用户确认价格

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"create-order","arguments":{"addressId":"addr_123","storeCode":"S001","beCode":"BE001","items":[{"productCode":"10001","quantity":1}]}},"id":1}'
```

### 13. 查询订单详情 (query-order)

查询麦当劳订单的详细信息和配送进度。

**触发词**: "查下订单"、"订单状态"、"我的订单"、"配送到哪了"

**参数**:
- `orderId`: 麦当劳订单追踪编号（必填，34位数字字符串）

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"query-order","arguments":{"orderId":"1030938730000733964700499858"}},"id":1}'
```

### 14. 获取当前时间 (now-time-info)

返回当前的完整时间信息，帮助判断活动是否在有效期内。

**触发词**: "现在几点"、"今天几号"（通常无需用户触发，AI 自动调用以判断活动时效）

```bash
curl -s -X POST "${MCD_MCP_URL:-https://mcp.mcd.cn}" \
  -H "Authorization: Bearer ${MCD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"now-time-info","arguments":{}},"id":1}'
```


## 响应处理

### 成功响应
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{"type": "text", "text": "..."}],
    "structuredContent": {...}
  },
  "id": 1
}
```

解析 `result.content[0].text` 或 `result.structuredContent` 获取数据。

### 错误响应
```json
{
  "jsonrpc": "2.0",
  "error": {"code": -32000, "message": "Token expired"},
  "id": 1
}
```

常见错误：
- `Token expired`: Token 过期，需要重新获取
- `Unauthorized`: Token 无效
- `Rate limited`: 请求过于频繁，稍后再试

## 输出格式建议

### 优惠券列表
以表格或清单形式展示，包含：
- 优惠券名称
- 优惠金额/折扣
- 有效期
- 使用条件

### 营养信息
以表格展示，包含：
- 餐品名称
- 热量 (kcal)
- 蛋白质 (g)
- 脂肪 (g)
- 碳水化合物 (g)

### 餐品列表
以分类清单展示，包含：
- 餐品名称
- 价格
- 商品编码（供下单使用）

### 订单价格
展示完整价格明细（金额单位为分，需除以100）：
- 商品原价 / 现价
- 运费 / 打包费
- 优惠金额
- 最终应付金额

## 使用示例

### 示例1：领取优惠券

**用户**: 今天麦当劳有什么优惠券可以领？

**AI 执行**: 调用 `available-coupons`

**AI 回复**: 
> 当前可领取的优惠券：
> 1. 🍟 麦辣鸡腿堡套餐立减5元 (有效期至2月10日)
> 2. 🥤 任意饮品第二杯半价 (有效期至2月15日)
> 
> 需要帮你一键领取吗？

### 示例2：外卖点餐完整流程

**用户**: 我想点麦乐送

**AI 执行流程**:
1. 调用 `delivery-query-addresses` → 获取用户地址列表和门店信息
2. 用户选择地址后，调用 `query-meals` → 展示餐品列表
3. 用户选择餐品后，调用 `calculate-price` → 展示价格明细
4. 用户确认价格后，调用 `create-order` → 创建订单
5. 引导用户完成支付

**AI 回复**:
> 您有以下配送地址：
> 1. 📍 清竹园9号楼 2单元508（李明 先生）
> 
> 请选择配送地址，或者告诉我新的地址信息来创建。

### 示例3：用券下单

**用户**: 我想用优惠券点外卖

**AI 执行流程**:
1. 调用 `delivery-query-addresses` → 获取门店信息
2. 用户选择地址后，调用 `query-store-coupons` → 展示当前门店可用券及对应商品，并引导用户使用query-meals查看更多商品
3. 用户选择券和商品后，调用 `calculate-price`（带 couponId/couponCode）→ 展示优惠后价格
4. 用户确认后，调用 `create-order` → 创建订单

## 注意事项

1. **Token 安全**: 不要在公开场合暴露用户的 MCD_TOKEN
2. **频率限制**: 避免短时间内大量请求
3. **数据时效**: 优惠券和活动信息实时变化，建议用户及时查询
4. **热量搭配**: 使用营养信息帮用户搭配套餐时，注意计算总热量
5. **外卖下单流程依赖**: 查询餐品、计算价格、创建订单等操作必须先调用 `delivery-query-addresses` 获取门店信息，不可跳过
6. **价格单位**: `calculate-price` 返回的金额单位为分，展示时需除以100
7. **下单前确认**: 创建订单前必须先调用 `calculate-price` 并等待用户确认价格
8. **门店券校验**: `query-store-coupons` 返回的是当前门店可用券，与 `query-my-coupons`（用户所有券）不同
