<p align="center">
  <img src="./assets/icon.svg" width="120" height="120" alt="ShieldClaw Logo">
</p>

<h1 align="center">ShieldClaw（盾爪）</h1>
<p align="center">OpenClaw 安全技能套件</p>

> 为 OpenClaw 提供安全防护，像盾牌一样守护用户数据和系统安全。

## 🏗️ 项目结构

```
shieldclaw/
├── packages/
│   ├── core/           # 核心底座（类型定义 + 共享服务）
│   ├── scan/           # 扫描插件 - Skill 安全扫描
│   ├── guard/          # 防护插件 - 实时行为监控
│   ├── audit/          # 审计插件 - 操作日志与报告
│   └── vault/          # 保险箱插件 - 敏感数据加密
│
├── apps/
│   └── openclaw-integration/  # OpenClaw 集成示例
│
├── tests/              # 测试套件
├── scripts/            # 构建脚本
├── package.json        # 根 package.json (monorepo)
├── pnpm-workspace.yaml # pnpm workspace 配置
└── README.md           # 本文件
```

## 🚀 快速开始

### 环境要求

- Node.js >= 18.0.0
- pnpm >= 8.0.0
- Electron >= 28.0.0（OpenClaw 依赖）

### 安装依赖

```bash
# 安装 pnpm（如果尚未安装）
npm install -g pnpm

# 进入项目目录
cd shieldclaw

# 安装所有依赖
pnpm install
```

### 构建

```bash
# 构建所有包
pnpm build

# 构建指定包
pnpm build:core
pnpm build:scan
```

### 开发模式

```bash
# 监听所有包的变化
pnpm dev
```

### 测试

```bash
# 运行所有测试
pnpm test

# 运行指定包的测试
pnpm test:core
```

## 📦 包说明

### @shieldclaw/core

核心底座，提供共享服务：

- **StorageService**: SQLite + WAL 模式 + 写入队列
- **CryptoService**: AES-256-GCM + 系统密钥链
- **LoggerService**: 文件日志 + 审计日志
- **ConfigService**: 配置管理（electron-store）
- **EventBus**: 事件总线（插件间通信）

```typescript
import { createCore } from '@shieldclaw/core';

const core = createCore({
  dbPath: './shieldclaw.db',
  logDir: './logs',
  logLevel: 'info',
});

await core.crypto.initialize();
```

### @shieldclaw/scan

Skill 安全扫描模块：

- 静态代码分析（危险函数、混淆代码、硬编码密钥）
- 权限评估（对比基准权限）
- 网络行为检测（可疑域名）
- 风险评分（0-100）

```typescript
import { SkillScanner } from '@shieldclaw/scan';

const scanner = new SkillScanner(core);
const report = await scanner.scan('/path/to/skill');
```

### @shieldclaw/guard

实时防护插件：

- 文件系统操作拦截
- 网络请求监控
- 进程执行拦截
- 通过 OpenClaw Hook 框架注册规则

```typescript
// 由 OpenClaw 加载并激活
// 用户配置启用/禁用
{
  "guard": {
    "enabled": true,
    "strictMode": false,
    "sensitivePaths": ["~/.ssh", "~/.aws"]
  }
}
```

### @shieldclaw/audit

审计插件：

- 全生命周期日志
- 可视化仪表盘
- 合规报告生成（PDF/Excel）

### @shieldclaw/vault

保险箱插件：

- 敏感数据识别（手机号、身份证、邮箱等）
- AES-256-GCM 加密
- 智能脱敏处理

## 🔧 OpenClaw 集成

```typescript
import { OpenClawApp } from '@shieldclaw/openclaw-integration';

const app = new OpenClawApp();

// 初始化 ShieldClaw
await app.initialize();

// 扫描 Skill
const report = await app.scanSkill('/path/to/skill');

// 关闭时清理
await app.shutdown();
```

## ⚙️ 配置

配置文件位置：`~/.config/OpenClaw/shieldclaw-config.json`

```json
{
  "shieldclaw": {
    "scan": {
      "enabled": true,
      "autoScanOnInstall": true,
      "threatIntelUpdateInterval": 3600
    },
    "guard": {
      "enabled": true,
      "strictMode": false,
      "allowedDomains": ["api.openai.com", "github.com"],
      "sensitivePaths": ["~/.ssh", "~/.aws"]
    },
    "audit": {
      "enabled": true,
      "retentionDays": 180,
      "autoReport": {
        "enabled": false,
        "frequency": "weekly"
      }
    },
    "vault": {
      "enabled": true,
      "authMethod": "system",
      "patterns": ["mobile", "idcard", "email", "bankcard"]
    }
  }
}
```

## 📋 开发计划

详见 [docs/开发计划.md](./docs/开发计划.md)

| 阶段 | 内容 | 状态 |
|------|------|------|
| 1 | 项目基础设施 | [x] 已完成 |
| 2 | shieldclaw-core 核心底座 | [ ] 进行中 |
| 3 | shieldclaw-scan 扫描模块 | [ ] 待开始 |
| 4 | Hook 框架 + Guard | [ ] 待开始 |
| 5 | shieldclaw-audit 审计 | [ ] 待开始 |
| 6 | shieldclaw-vault 保险箱 | [ ] 待开始 |
| 7 | 集成测试与文档 | [ ] 待开始 |

## 🔐 安全说明

- 加密密钥存储在系统密钥链（Windows Credential / macOS Keychain）
- 审计日志使用 SQLite WAL 模式，支持高并发写入
- Vault 数据使用 AES-256-GCM 加密，每个数据独立 IV

## 📄 许可证

MIT

---

**ShieldClaw** - 守护你的 OpenClaw 🛡️
