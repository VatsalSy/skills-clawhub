#!/usr/bin/env node
/**
 * Cognitive Brain v5.0 - 改进版 Post-install Script
 * 添加依赖检查、交互式配置、v5.0 架构支持
 */

const fs = require('fs');
const path = require('path');
const { execSync, spawn } = require('child_process');
const readline = require('readline');

const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(__dirname, "..", "..");
const OPENCLAW_HOOKS_DIR = path.join(HOME, '.openclaw', 'hooks');
const CONFIG_PATH = path.join(SKILL_DIR, 'config.json');

// 创建 readline 接口
function ask(question, defaultValue = '') {
  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
    
    const prompt = defaultValue ? `${question} [${defaultValue}]: ` : `${question}: `;
    rl.question(prompt, (answer) => {
      rl.close();
      resolve(answer.trim() || defaultValue);
    });
  });
}

// ===== 0. 安装系统依赖 =====
async function installSystemDependencies(failedDeps) {
  console.log('\n📦 自动安装系统依赖...\n');
  
  // 检测操作系统
  const platform = process.platform;
  const isRoot = process.getuid && process.getuid() === 0;
  
  const sudo = isRoot ? '' : 'sudo ';
  
  for (const dep of failedDeps) {
    if (dep.name === 'Node.js') {
      console.log('  ⚠️  Node.js 需要手动安装');
      console.log('     请访问: https://nodejs.org/');
      continue;
    }
    
    try {
      if (platform === 'linux') {
        // 检测 Linux 发行版
        const isUbuntu = fs.existsSync('/etc/debian_version');
        const isCentOS = fs.existsSync('/etc/redhat-release');
        
        if (isUbuntu) {
          if (dep.name === 'PostgreSQL') {
            console.log('  ⏳ 安装 PostgreSQL...');
            execSync(`${sudo}apt-get update && ${sudo}apt-get install -y postgresql postgresql-contrib`, { stdio: 'inherit' });
            execSync(`${sudo}systemctl enable postgresql && ${sudo}systemctl start postgresql`, { stdio: 'inherit' });
            console.log('  ✅ PostgreSQL 安装并启动');
          } else if (dep.name === 'Redis') {
            console.log('  ⏳ 安装 Redis...');
            execSync(`${sudo}apt-get install -y redis-server`, { stdio: 'inherit' });
            execSync(`${sudo}systemctl enable redis-server && ${sudo}systemctl start redis-server`, { stdio: 'inherit' });
            console.log('  ✅ Redis 安装并启动');
          }
        } else if (isCentOS) {
          if (dep.name === 'PostgreSQL') {
            console.log('  ⏳ 安装 PostgreSQL...');
            execSync(`${sudo}yum install -y postgresql-server postgresql-contrib`, { stdio: 'inherit' });
            execSync(`${sudo}postgresql-setup initdb`, { stdio: 'inherit' });
            execSync(`${sudo}systemctl enable postgresql && ${sudo}systemctl start postgresql`, { stdio: 'inherit' });
            console.log('  ✅ PostgreSQL 安装并启动');
          } else if (dep.name === 'Redis') {
            console.log('  ⏳ 安装 Redis...');
            execSync(`${sudo}yum install -y redis`, { stdio: 'inherit' });
            execSync(`${sudo}systemctl enable redis && ${sudo}systemctl start redis`, { stdio: 'inherit' });
            console.log('  ✅ Redis 安装并启动');
          }
        } else {
          console.log(`  ⚠️  无法自动安装 ${dep.name}，请手动安装`);
        }
      } else if (platform === 'darwin') {
        // macOS
        try {
          execSync('which brew', { stdio: 'pipe' });
        } catch (e) {
          console.log('  ❌ 未检测到 Homebrew，请先安装: https://brew.sh/');
          return false;
        }
        
        if (dep.name === 'PostgreSQL') {
          console.log('  ⏳ 安装 PostgreSQL...');
          execSync('brew install postgresql', { stdio: 'inherit' });
          execSync('brew services start postgresql', { stdio: 'inherit' });
          console.log('  ✅ PostgreSQL 安装并启动');
        } else if (dep.name === 'Redis') {
          console.log('  ⏳ 安装 Redis...');
          execSync('brew install redis', { stdio: 'inherit' });
          execSync('brew services start redis', { stdio: 'inherit' });
          console.log('  ✅ Redis 安装并启动');
        }
      } else {
        console.log(`  ⚠️  不支持自动安装 ${dep.name} 在 ${platform} 平台`);
      }
    } catch (e) {
      console.error(`  ❌ ${dep.name} 安装失败:`, e.message);
      return false;
    }
  }
  
  return true;
}

// ===== 0. 安装 npm 依赖 =====
async function installNpmDependencies() {
  console.log('\n📦 安装 npm 依赖...\n');
  
  const skillDir = path.join(__dirname, "..", "..");
  const nodeModulesPath = path.join(skillDir, 'node_modules');
  
  // 检查是否已安装
  if (fs.existsSync(nodeModulesPath)) {
    console.log('  ✅ npm 依赖已存在，跳过安装');
    return true;
  }
  
  console.log('  ⏳ 正在安装 pg, redis, uuid...');
  
  try {
    // 使用 spawn 以便显示实时输出
    await new Promise((resolve, reject) => {
      const npm = spawn('npm', ['install', '--production'], {
        cwd: skillDir,
        stdio: 'inherit'
      });
      
      npm.on('close', (code) => {
        if (code === 0) {
          console.log('  ✅ npm 依赖安装成功');
          resolve();
        } else {
          reject(new Error(`npm install 退出码: ${code}`));
        }
      });
      
      npm.on('error', (err) => {
        reject(err);
      });
    });
    
    return true;
  } catch (e) {
    console.error('  ❌ npm install 失败:', e.message);
    console.log('\n请手动运行:');
    console.log(`  cd ${skillDir}`);
    console.log('  npm install\n');
    return false;
  }
}

// ===== 1. 依赖检查 =====
async function checkDependencies() {
  console.log('\n🔍 检查系统依赖...\n');
  
  const checks = [
    { name: 'Node.js', cmd: 'node -v', minVersion: '18.0.0' },
    { name: 'PostgreSQL', cmd: 'psql --version' },
    { name: 'Redis', cmd: 'redis-cli ping' }
  ];
  
  const results = [];
  
  for (const check of checks) {
    try {
      execSync(check.cmd, { stdio: 'pipe' });
      console.log(`  ✅ ${check.name} 已安装`);
      results.push({ name: check.name, ok: true });
    } catch (e) {
      console.log(`  ❌ ${check.name} 未安装或无法访问`);
      results.push({ name: check.name, ok: false });
    }
  }
  
  const failed = results.filter(r => !r.ok);
  
  if (failed.length > 0) {
    console.log('\n⚠️  缺少以下依赖:');
    for (const f of failed) {
      console.log(`   - ${f.name}`);
    }
    
    // 尝试自动安装
    const shouldInstall = await ask('是否自动安装缺少的依赖?', 'y');
    if (shouldInstall.toLowerCase() === 'y') {
      const installed = await installSystemDependencies(failed);
      if (installed) {
        console.log('\n✅ 系统依赖安装完成');
        return true;
      }
    }
    
    console.log('\n请手动安装后重试:');
    console.log('  Ubuntu/Debian: sudo apt install postgresql redis-server');
    console.log('  macOS: brew install postgresql redis');
    console.log('');
    
    const continueAnyway = await ask('是否继续安装? (可能无法正常工作)', 'n');
    if (continueAnyway.toLowerCase() !== 'y') {
      process.exit(1);
    }
  }
  
  return results.every(r => r.ok);
}

// ===== 2. 交互式配置 =====
async function interactiveConfig() {
  console.log('\n⚙️  配置 Cognitive Brain\n');
  console.log('请提供数据库连接信息（按 Enter 使用默认值）\n');
  
  const config = {
    version: "5.0.0",
    storage: {
      primary: {
        type: "postgresql",
        host: await ask('PostgreSQL 主机', 'localhost'),
        port: parseInt(await ask('PostgreSQL 端口', '5432')),
        database: await ask('PostgreSQL 数据库名', 'cognitive_brain'),
        user: await ask('PostgreSQL 用户名', 'postgres'),
        password: await ask('PostgreSQL 密码', ''),
        extensions: ["pgvector", "pg_trgm"]
      },
      cache: {
        type: "redis",
        host: await ask('Redis 主机', 'localhost'),
        port: parseInt(await ask('Redis 端口', '6379')),
        db: 0,
        keyPrefix: "brain:"
      }
    },
    embedding: {
      provider: "local",
      dimension: 384,
      options: {
        model: "paraphrase-multilingual-MiniLM-L12-v2",
        script: "scripts/embed.py"
      }
    },
    memory: {
      sensory: { ttl: 30000, maxSize: 100, storage: "redis" },
      working: { ttl: 3600000, maxSize: 50, storage: "redis" },
      episodic: { maxCount: 10000, decayRate: 0.1, storage: "postgresql" },
      semantic: { maxCount: 5000, storage: "postgresql" }
    },
    forgetting: {
      enabled: true,
      schedule: "0 3 * * *",
      minAge: 604800000,
      importanceThreshold: 0.2,
      cleanupOrphans: true
    },
    proactive: {
      enabled: true,
      maxSuggestions: 2,
      confidenceThreshold: 0.5
    }
  };
  
  // 验证密码不为空
  if (!config.storage.primary.password) {
    console.error('❌ 错误: PostgreSQL 密码不能为空');
    process.exit(1);
  }
  
  // 保存配置
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
  console.log('\n✅ 配置已保存');
  
  return config;
}

// ===== 3. 测试数据库连接 =====
async function testDatabaseConnection(config) {
  console.log('\n🗄️  测试数据库连接...\n');
  
  const { Pool } = require('pg');
  const pool = new Pool({
    host: config.storage.primary.host,
    port: config.storage.primary.port,
    database: config.storage.primary.database,
    user: config.storage.primary.user,
    password: config.storage.primary.password,
    connectionTimeoutMillis: 5000
  });
  
  try {
    await pool.query('SELECT 1');
    console.log('  ✅ PostgreSQL 连接成功');
    await pool.end();
    return true;
  } catch (e) {
    console.log(`  ❌ PostgreSQL 连接失败: ${e.message}`);
    console.log('\n可能的解决方案:');
    console.log('  1. 确认 PostgreSQL 正在运行: sudo systemctl status postgresql');
    console.log('  2. 创建数据库: sudo -u postgres createdb cognitive_brain');
    console.log('  3. 检查用户权限');
    await pool.end();
    return false;
  }
}

// ===== 4. 初始化数据库 =====
async function initDatabase() {
  console.log('\n🗄️  初始化数据库...\n');
  
  try {
    execSync(`node "${path.join(SKILL_DIR, 'scripts/tools/init-db.cjs')}"`, {
      cwd: SKILL_DIR,
      stdio: 'inherit',
      timeout: 60000
    });
    console.log('  ✅ 数据库初始化完成');
    return true;
  } catch (e) {
    console.log(`  ⚠️  数据库初始化问题: ${e.message}`);
    console.log('  可能已初始化过，继续...');
    return true; // 继续安装
  }
}

// ===== 5. 创建数据库索引 =====
async function createIndexes() {
  console.log('\n🔧 创建数据库索引...\n');
  
  try {
    execSync(`node "${path.join(SKILL_DIR, 'scripts/tools/create_indexes.cjs')}"`, {
      cwd: SKILL_DIR,
      stdio: 'inherit'
    });
    console.log('  ✅ 索引创建完成');
  } catch (e) {
    console.log(`  ⚠️  索引创建失败: ${e.message}`);
  }
}

// ===== 6. 同步 Hooks =====
async function syncHooks() {
  console.log('\n🔄 同步 hooks...\n');
  
  if (!fs.existsSync(OPENCLAW_HOOKS_DIR)) {
    fs.mkdirSync(OPENCLAW_HOOKS_DIR, { recursive: true });
  }

  const HOOKS_IN_SKILL = path.join(SKILL_DIR, 'hooks');
  
  if (!fs.existsSync(HOOKS_IN_SKILL)) {
    console.log('  ⚠️  未找到 hooks 目录，跳过');
    return;
  }
  
  const hookDirs = fs.readdirSync(HOOKS_IN_SKILL).filter(f => {
    return fs.statSync(path.join(HOOKS_IN_SKILL, f)).isDirectory();
  });
  
  for (const hookName of hookDirs) {
    const targetDir = path.join(OPENCLAW_HOOKS_DIR, hookName);
    const sourceDir = path.join(HOOKS_IN_SKILL, hookName);
    
    if (!fs.existsSync(targetDir)) {
      fs.mkdirSync(targetDir, { recursive: true });
    }
    
    const files = fs.readdirSync(sourceDir);
    for (const file of files) {
      fs.copyFileSync(path.join(sourceDir, file), path.join(targetDir, file));
    }
    console.log(`  ✅ Hook 已安装: ${hookName}`);
  }
}

// ===== 6. 设置 Cron =====
async function setupCron() {
  console.log('\n📅 设置定时任务...\n');
  
  const CRON_COMMENT = '# Cognitive Brain scheduled tasks';
  const CRON_JOBS = `0 3 * * * cd ${SKILL_DIR} && node scripts/core/forget.cjs run >> /tmp/brain-cron.log 2>&1
0 4 * * * cd ${SKILL_DIR} && node scripts/core/heartbeat_reflect.cjs check >> /tmp/brain-cron.log 2>&1`;
  
  try {
    let currentCron = '';
    try {
      currentCron = execSync('crontab -l 2>/dev/null', { encoding: 'utf8' });
    } catch (e) {
      // 没有 crontab 是正常的
    }
    
    if (!currentCron.includes('cognitive-brain')) {
      const newCron = currentCron.trim() + '\n' + CRON_COMMENT + '\n' + CRON_JOBS + '\n';
      const tmpFile = '/tmp/cron-tmp-' + Date.now();
      fs.writeFileSync(tmpFile, newCron);
      execSync(`crontab "${tmpFile}"`);
      fs.unlinkSync(tmpFile);
      console.log('  ✅ 定时任务已设置');
    } else {
      console.log('  ✅ 定时任务已存在');
    }
  } catch (e) {
    console.log(`  ⚠️  无法设置定时任务: ${e.message}`);
  }
}

// ===== 7. 创建必要文件 =====
async function createDataFiles() {
  console.log('\n📁 创建数据文件...\n');
  
  const files = [
    { name: '.user-model.json', content: { stats: { totalInteractions: 0 }, preferences: { topics: {} } } },
    { name: '.working-memory.json', content: { activeContext: { entities: [], topic: null } } },
    { name: '.prediction-cache.json', content: { predictions: [], lastUpdated: null } }
  ];

  for (const file of files) {
    const filePath = path.join(SKILL_DIR, file.name);
    if (!fs.existsSync(filePath)) {
      fs.writeFileSync(filePath, JSON.stringify(file.content, null, 2));
      console.log(`  ✅ 创建: ${file.name}`);
    } else {
      console.log(`  ✅ 已存在: ${file.name}`);
    }
  }
}

// ===== 8. 运行测试 =====
async function runTests() {
  console.log('\n🧪 运行测试...\n');
  
  try {
    execSync('./tests/run.sh', {
      cwd: SKILL_DIR,
      stdio: 'inherit',
      timeout: 60000
    });
    console.log('  ✅ 测试通过');
    return true;
  } catch (e) {
    console.log(`  ⚠️  测试失败: ${e.message}`);
    return false;
  }
}

// ===== 主流程 =====
async function main() {
  console.log('\n🧠 Cognitive Brain v5.0 安装程序\n');
  console.log('=' .repeat(50));
  
  // 0. 安装 npm 依赖
  const npmOk = await installNpmDependencies();
  if (!npmOk) {
    console.log('\n⚠️  npm 依赖安装失败，继续可能无法正常工作\n');
  }
  
  // 1. 检查系统依赖
  const depsOk = await checkDependencies();
  if (!depsOk) {
    console.log('\n⚠️  警告: 部分依赖未安装，继续可能无法正常工作\n');
  }
  
  // 2. 交互式配置
  const config = await interactiveConfig();
  
  // 3. 测试连接
  const dbOk = await testDatabaseConnection(config);
  if (!dbOk) {
    const retry = await ask('是否重试配置?', 'y');
    if (retry.toLowerCase() === 'y') {
      return main(); // 重新开始
    }
    console.log('\n❌ 安装中止');
    process.exit(1);
  }
  
  // 4. 初始化数据库
  await initDatabase();
  
  // 5. 创建索引
  await createIndexes();
  
  // 6. 同步 hooks
  await syncHooks();
  
  // 7. 设置 cron
  await setupCron();
  
  // 8. 创建数据文件
  await createDataFiles();
  
  // 9. 运行测试
  const testsOk = await runTests();
  
  // 完成
  console.log('\n' + '='.repeat(50));
  console.log('\n✨ Cognitive Brain v5.0 安装完成!\n');
  
  if (!testsOk) {
    console.log('⚠️  部分测试失败，但安装已完成\n');
  }
  
  console.log('使用方法:');
  console.log('  node src/index.js              # v5.0 新架构');
  console.log('  node scripts/core/brain.cjs    # v4.x 兼容');
  console.log('  node scripts/core/encode.cjs "内容"   # 编码记忆');
  console.log('  node scripts/core/recall.cjs --query "关键词"  # 检索记忆');
  console.log('  ./tests/run.sh                 # 运行测试');
  console.log('');
}

main().catch(e => {
  console.error('\n❌ 安装失败:', e.message);
  process.exit(1);
});

