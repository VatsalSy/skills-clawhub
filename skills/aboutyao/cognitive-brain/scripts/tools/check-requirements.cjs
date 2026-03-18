#!/usr/bin/env node
/**
 * Cognitive Brain v5.0 - 安装前检查
 * 检查系统是否满足安装要求
 */

const { execSync } = require('child_process');

console.log('\n🔍 Cognitive Brain v5.0 安装前检查\n');
console.log('=' .repeat(50));

const checks = [
  {
    name: 'Node.js',
    cmd: 'node -v',
    check: (output) => {
      const version = output.match(/v(\d+)/)?.[1];
      return { ok: parseInt(version) >= 18, detail: output.trim() };
    },
    required: true,
    install: 'https://nodejs.org/ (>= 18)'
  },
  {
    name: 'PostgreSQL',
    cmd: 'psql --version',
    check: (output) => ({ ok: true, detail: output.trim() }),
    required: true,
    install: 'sudo apt install postgresql postgresql-contrib (Ubuntu/Debian)'
  },
  {
    name: 'PostgreSQL 服务',
    cmd: 'pg_isready',
    check: (output) => ({ ok: output.includes('accepting connections'), detail: 'running' }),
    required: true,
    install: 'sudo systemctl start postgresql'
  },
  {
    name: 'Redis',
    cmd: 'redis-cli ping',
    check: (output) => ({ ok: output.includes('PONG'), detail: 'running' }),
    required: true,
    install: 'sudo apt install redis-server (Ubuntu/Debian)'
  },
  {
    name: 'pgvector 扩展',
    cmd: 'psql -U postgres -c "SELECT * FROM pg_available_extensions WHERE name = \'vector\';" 2>/dev/null',
    check: (output) => ({ ok: output.includes('vector'), detail: output.includes('vector') ? 'available' : 'not found' }),
    required: false,
    install: 'sudo apt install postgresql-14-pgvector (根据 PG 版本调整)'
  }
];

let allRequiredOk = true;
let anyFailed = false;

for (const check of checks) {
  process.stdout.write(`\n  ${check.name}... `);
  
  try {
    const output = execSync(check.cmd, { encoding: 'utf8', stdio: 'pipe' });
    const result = check.check(output);
    
    if (result.ok) {
      console.log(`✅ ${result.detail}`);
    } else {
      console.log(`⚠️  ${result.detail}`);
      anyFailed = true;
    }
  } catch (e) {
    console.log(`❌ 未安装或无法访问`);
    console.log(`     安装: ${check.install}`);
    anyFailed = true;
    if (check.required) allRequiredOk = false;
  }
}

console.log('\n' + '=' .repeat(50));

if (allRequiredOk && !anyFailed) {
  console.log('\n✅ 系统检查通过，可以安装 Cognitive Brain v5.0\n');
  console.log('运行安装命令:');
  console.log('  clawhub install cognitive-brain');
  console.log('  或');
  console.log('  npm install && node scripts/tools/postinstall.cjs\n');
  process.exit(0);
} else if (allRequiredOk) {
  console.log('\n⚠️  系统基本满足要求，但部分可选功能可能无法使用\n');
  console.log('可以继续安装，但建议先安装可选依赖\n');
  process.exit(0);
} else {
  console.log('\n❌ 系统不满足最低要求，请先安装缺失的依赖\n');
  console.log('安装指南:');
  console.log('  Ubuntu/Debian:');
  console.log('    sudo apt update');
  console.log('    sudo apt install postgresql postgresql-contrib redis-server');
  console.log('    sudo systemctl start postgresql redis-server');
  console.log('    sudo -u postgres createdb cognitive_brain\n');
  process.exit(1);
}

