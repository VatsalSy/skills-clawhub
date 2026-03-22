---
name: r2-uploader
description: 使用 wrangler 命令上传文件到 Cloudflare R2。当用户需要上传文件到 R2 存储、返回公开 URL、批量上传时使用的是此技能。
compatibility:
  required_tools:
    - name: cloudflare
      description: Cloudflare Workers/Wrangler CLI 工具
---

# R2 文件上传技能（增强版）

使用 wrangler CLI 命令直接将文件上传到 Cloudflare R2 对象存储。

## 前置要求

1. **安装 wrangler CLI**:
   ```bash
   npm install -g wrangler
   ```

2. **登录 Cloudflare**:
   ```bash
   wrangler login
   ```

3. **创建 bucket**（如不存在）:
   ```bash
   wrangler r2 bucket create <bucket-name>
   ```

4. **自定义域名**（可选）：需在 Cloudflare Dashboard 配置 R2 存储桶域名

## 环境变量

可通过环境变量配置默认参数：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `R2_BUCKET` | 默认 bucket 名称 | `hugo-blog` |
| `R2_DOMAIN` | 默认自定义域名 | `cdn.example.com` |

## 核心工作流程

### 步骤 1：查找文件（处理路径空格问题）

当用户提供文件名或模糊路径时，先使用 `find` 命令定位文件：

```bash
# 查找文件
find /Users/victor/Desktop -name "<filename>" -type f 2>/dev/null
```

### 步骤 2：验证文件存在

```bash
ls -la "<file-path>"
```

### 步骤 3：处理含空格的路径

**问题**：wrangler 对某些含中文/空格的路径处理不一致

**解决方案**：
1. 优先尝试直接上传（路径用引号包裹）
2. 如果失败，复制到临时路径再上传：

```bash
# 复制到无空格路径
cp "<source-path>" "/tmp/r2-upload-$(basename "<source-path>")"

# 从临时路径上传
wrangler r2 object put "<bucket>/<path>/<filename>" --file "/tmp/r2-upload-$(basename "<source-path>")" --remote

# 清理临时文件
rm "/tmp/r2-upload-$(basename "<source-path>")"
```

### 步骤 4：执行上传

```bash
wrangler r2 object put "<bucket>/<path>/<filename>" --file "<file-path>" --remote
```

## 命令行用法

### 上传单个文件

```bash
wrangler r2 object put "<bucket>/<path>/<filename>" --file "<local-file-path>" --remote
```

### 从 URL 下载并上传

```bash
curl -L "<url>" | wrangler r2 object put "<bucket>/<path>/<filename>" --file - --remote
```

## 路径约定

- **上传路径格式**: `agent/YYYYMMDD/<filename>`
- **日期格式**: 使用 8 位数字日期，如 `20260321`

## 使用示例

### 示例 1：上传图片到默认 bucket

```bash
wrangler r2 object put "$R2_BUCKET/agent/20260321/photo.jpg" --file "./photo.jpg" --remote
```

### 示例 2：处理含空格的路径

```bash
# 如果直接上传失败，使用临时文件方式
cp "/path/with spaces/file.jpg" "/tmp/file.jpg"
wrangler r2 object put "hugo-blog/agent/20260321/file.jpg" --file "/tmp/file.jpg" --remote
rm "/tmp/file.jpg"
```

### 示例 3：从 URL 下载并上传

```bash
curl -L "https://example.com/image.png" | wrangler r2 object put "assets/agent/20260321/image.png" --file - --remote
```

### 示例 4：批量上传（当前目录）

```bash
for file in *.jpg; do
  wrangler r2 object put "bucket/agent/$(date +%Y%m%d)/$file" --file "$file" --remote
done
```

## URL 生成规则

上传成功后，文件访问 URL 为：

1. **默认 URL**: `https://<bucket>.<account-id>.r2.dev/<path>/<filename>`
2. **自定义 URL**: `https://<domain>/<path>/<filename>`（如配置了自定义域名）

### 示例

- Bucket: `hugo-blog`
- 路径：`agent/20260321/photo.jpg`
- 自定义域名：`cos.jiahongw.com`
- 最终 URL: `https://cos.jiahongw.com/agent/20260321/photo.jpg`

## 错误处理指南

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `The file does not exist` | 路径错误或空格处理问题 | 1. 使用 find 查找正确路径<br>2. 复制到/tmp 后上传 |
| `Authentication required` | 未登录 Cloudflare | 运行 `wrangler login` |
| `Bucket not found` | bucket 不存在 | 使用 `wrangler r2 bucket create <name>` 创建 |
| `Network error` | 网络连接问题 | 检查网络，重试上传 |

## 故障排查流程

当上传失败时，按以下步骤排查：

1. **验证文件存在**:
   ```bash
   ls -la "<file-path>"
   ```

2. **检查 wrangler 登录状态**:
   ```bash
   wrangler whoami
   ```

3. **尝试临时路径上传**:
   ```bash
   cp "<original-path>" "/tmp/$(basename "<original-path>")"
   wrangler r2 object put "<bucket>/<path>/<filename>" --file "/tmp/$(basename "<original-path>")" --remote
   ```

4. **验证 bucket 存在**:
   ```bash
   wrangler r2 bucket list
   ```

## 最佳实践

1. **使用日期前缀**: 按 `agent/YYYYMMDD/` 组织文件便于管理
2. **有意义的文件名**: 使用描述性文件名而非随机名
3. **检查上传结果**: 确认 "Upload complete" 消息
4. **大文件上传**: 确保网络稳定，必要时使用重试
5. **处理中文路径**: 遇到中文/空格路径时，优先使用临时文件方式

## 技能执行流程

当用户请求上传文件时：

1. **询问或识别文件路径**
   - 如果用户提供完整路径，直接使用
   - 如果只提供文件名，使用 `find` 命令查找

2. **验证文件存在**
   - 使用 `ls -la` 确认文件存在

3. **执行上传**
   - 优先尝试直接上传
   - 如果失败（特别是含空格/中文路径），使用临时路径方式

4. **返回 URL**
   - 成功后生成完整 URL：`https://$R2_DOMAIN/<path>/<filename>`
