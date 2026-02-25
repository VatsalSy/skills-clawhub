# 属性类型参考

## 常见 attribute_type 值

以下是 ec_distribute.distribute_supply_attribute 表中常见的属性类型：

### ALLOCATED_QUALITY（分配品质）
**说明：** 记录需求单分配的商品品质信息  
**常见值：**
- `INTERNAL_BRAND` - 内部品牌
- `ORIGINAL_CURRENCY` - 原厂货币
- `ORIGINAL_INLAND_4S` - 原厂内陆4S
- `ORIGINAL_BRAND` - 原厂品牌
- `BRAND` - 品牌件
- `DISMANTLE` - 拆车件

### STRICT_DISTRIBUTE_CHANNEL（店铺分配赛道）
**说明：** 记录需求单分配的店铺赛道信息  
**常见值：**
- `CASS_STRICT_INTERNAL_BRAND_SUPPLY` - 开思严选内部品牌供应
- `CASS_STRICT_ORIGINAL_BRAND_SUPPLY` - 开思严选原厂品牌供应
- `CASS_STRICT_BRAND_SUPPLY` - 开思严选品牌供应
- `CASS_AGENT_SUPPLY` - 开思代运营供应

### 其他属性类型

根据实际业务需要，可能还包括：
- 供应商属性
- 价格属性
- 库存属性
- 其他业务属性

## 查询示例

### 查询所有属性类型
```sql
SELECT DISTINCT attribute_type 
FROM ec_distribute.distribute_supply_attribute
```

### 查询指定需求单的所有属性
```sql
SELECT * 
FROM ec_distribute.distribute_supply_attribute 
WHERE demand_id = 'B26020702530'
```

### 查询特定属性类型的所有记录
```sql
SELECT * 
FROM ec_distribute.distribute_supply_attribute 
WHERE attribute_type = 'ALLOCATED_QUALITY'
LIMIT 100
```
