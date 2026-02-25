---
name: query-allocated-quality
description: 查询开思汽配电商系统分流库中的分配属性信息。支持查询分配品质（ALLOCATED_QUALITY）和店铺分配赛道（STRICT_DISTRIBUTE_CHANNEL）。用于查询 ec_distribute.distribute_supply_attribute 表中指定 demand_id 和 attribute_type 的记录。适用于测试人员排查分配品质、分配赛道相关问题、验证数据配置等场景。
---

# 查询分流库分配属性

这个技能用于查询开思汽配电商系统【分流库】中的分配属性信息，包括分配品质和店铺分配赛道。

## 使用场景

- 查询指定需求单的分配品质配置
- 查询指定需求单的店铺分配赛道
- 验证分配属性数据是否正确
- 排查分配相关问题

## 数据库信息

**数据库：** ec_distribute（分流库）  
**表名：** distribute_supply_attribute  
**主要字段：**
- `id` - 记录ID
- `demand_id` - 需求单ID
- `standard_item_id` - 标准商品ID
- `supply_id` - 供应商ID
- `attribute_type` - 属性类型
- `attribute_value` - 属性值（JSON数组）
- `del_flag` - 删除标记（0=正常，1=已删除）
- `created_stamp` - 创建时间
- `last_updated_stamp` - 更新时间

## 查询方法

### 1. 查询分配品质

查询指定需求单的分配品质：

```sql
SELECT * 
FROM ec_distribute.distribute_supply_attribute dsa 
WHERE dsa.demand_id = '<需求单ID>' 
  AND attribute_type = 'ALLOCATED_QUALITY'
```

**品质类型示例：**
- `INTERNAL_BRAND` - 内部品牌
- `ORIGINAL_CURRENCY` - 原厂货币
- `ORIGINAL_INLAND_4S` - 原厂内陆4S
- `ORIGINAL_BRAND` - 原厂品牌

### 2. 查询店铺分配赛道

查询指定需求单的店铺分配赛道：

```sql
SELECT * 
FROM ec_distribute.distribute_supply_attribute dsa 
WHERE dsa.demand_id = '<需求单ID>' 
  AND attribute_type = 'STRICT_DISTRIBUTE_CHANNEL'
```

**赛道类型示例：**
- `CASS_STRICT_INTERNAL_BRAND_SUPPLY` - 开思严选内部品牌供应
- `CASS_STRICT_ORIGINAL_BRAND_SUPPLY` - 开思严选原厂品牌供应

### 3. 通用查询

查询指定需求单的所有属性：

```sql
SELECT * 
FROM ec_distribute.distribute_supply_attribute dsa 
WHERE dsa.demand_id = '<需求单ID>'
```

### 参数说明

- **需求单ID**（demand_id）：如 `B26020702530`，可变参数
- **属性类型**（attribute_type）：
  - `ALLOCATED_QUALITY` - 分配品质
  - `STRICT_DISTRIBUTE_CHANNEL` - 店铺分配赛道
  - 其他属性类型参考 `references/attribute-types.md`

## 使用 agent.py 脚本

工作空间中的 `agent.py` 提供了便捷的查询函数：

### 完整查询（推荐）

**查询所有属性，显示总记录数和分类统计：**

```python
from agent import query_all_attributes

# 查询指定需求单的所有分配属性
result = query_all_attributes('B26020702530')
```

**输出格式：**
- 先显示总记录数（如：找到 8 条记录）
- 显示各类型统计（如：分配品质 4 条、店铺分配赛道 4 条）
- 按类型分组展示所有记录

### 快捷查询函数

```python
from agent import query_allocated_quality, query_distribute_channel

# 查询分配品质
result = query_allocated_quality('B26020702530')

# 查询店铺分配赛道
result = query_distribute_channel('B26020702530')
```

### 通用查询函数

```python
from agent import query_distribute_attribute

# 自定义属性类型查询
result = query_distribute_attribute('B26020702530', 'ALLOCATED_QUALITY')
result = query_distribute_attribute('B26020702530', 'STRICT_DISTRIBUTE_CHANNEL')
```

## 执行步骤

1. 确认数据库连接信息（已配置在 agent.py 中）
2. 使用 Python 脚本或直接执行 SQL：
   - Python：调用 `agent.py` 中的函数
   - SQL：替换查询语句中的参数并执行
3. 分析返回结果

## 注意事项

- 确保有分流库的查询权限
- demand_id 需要加引号（字符串类型）
- attribute_value 字段为 JSON 数组格式
- del_flag = 0 表示正常记录，1 表示已删除
- 一个需求单可能对应多个标准商品（standard_item_id）
- 同一个需求单的不同商品可能有相同的分配属性
- **重要**：查询分流库时，必须先显示总记录数，再分类展示，绝对不能遗漏数据
- **推荐**：使用 `query_all_attributes()` 函数查询完整数据，避免遗漏
