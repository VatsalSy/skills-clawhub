#!/usr/bin/env node
/**
 * Cognitive Brain - Hook 同步脚本
 * 检测并同步 hooks 版本
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execSync } = require('child_process');

const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(__dirname, "..", "..");
const HOOKS_IN_SKILL = path.join(SKILL_DIR, 'hooks');
const OPENCLAW_HOOKS_DIR = path.join(HOME, '.openclaw', 'hooks');
const VERSION_FILE = path.join(SKILL_DIR, '.hook-version');

// 计算文件哈希
function getFileHash(filePath) {
  try {
    const content = fs.readFileSync(filePath);
    return crypto.createHash('md5').update(content).digest('hex');
  } catch (e) {
    return null;
  }
}

// 递归收集所有文件哈希
function collectFileHashes(dirPath, prefix = '', hashes = []) {
  try {
    const entries = fs.readdirSync(dirPath).sort();
    
    for (const entry of entries) {
      const entryPath = path.join(dirPath, entry);
      const stat = fs.statSync(entryPath);
      const entryName = prefix ? `${prefix}/${entry}` : entry;
      
      if (stat.isFile()) {
        const hash = getFileHash(entryPath);
        if (hash) hashes.push(`${entryName}:${hash}`);
      } else if (stat.isDirectory()) {
        collectFileHashes(entryPath, entryName, hashes);
      }
    }
  } catch (e) {
    // 忽略错误
  }
  
  return hashes;
}

// 计算目录哈希
function getDirectoryHash(dirPath) {
  const hashes = collectFileHashes(dirPath);
  return hashes.length > 0 
    ? crypto.createHash('md5').update(hashes.join('|')).digest('hex')
    : null;
}

// 获取当前安装的 hook 版本
function getInstalledVersion() {
  try {
    if (fs.existsSync(VERSION_FILE)) {
      return JSON.parse(fs.readFileSync(VERSION_FILE, 'utf8'));
    }
  } catch (e) {
    // 忽略错误
  }
  return null;
}

// 保存 hook 版本
function saveVersion(version) {
  fs.writeFileSync(VERSION_FILE, JSON.stringify(version, null, 2));
}

// 同步 hooks
function syncHooks(force = false) {
  console.log('🔄 检查 hooks 同步状态...\n');
  
  if (!fs.existsSync(HOOKS_IN_SKILL)) {
    console.log('❌ Skill hooks 目录不存在');
    return false;
  }
  
  // 计算当前 skill hooks 的哈希
  const skillHash = getDirectoryHash(HOOKS_IN_SKILL);
  const installedVersion = getInstalledVersion();
  
  console.log(`  Skill hooks 哈希: ${skillHash?.substring(0, 8)}...`);
  
  // 检查是否需要更新
  if (!force && installedVersion && installedVersion.hash === skillHash) {
    console.log('  安装版本哈希: ' + installedVersion.hash.substring(0, 8) + '...');
    console.log('  ✅ Hooks 已是最新版本\n');
    return true;
  }
  
  if (installedVersion) {
    console.log('  安装版本哈希: ' + installedVersion.hash.substring(0, 8) + '...');
    console.log('  ⚠️  版本不一致，需要更新\n');
  } else {
    console.log('  安装版本: 未记录');
    console.log('  ⚠️  首次安装或版本信息丢失\n');
  }
  
  // 执行同步
  console.log('📦 正在同步 hooks...\n');
  
  if (!fs.existsSync(OPENCLAW_HOOKS_DIR)) {
    fs.mkdirSync(OPENCLAW_HOOKS_DIR, { recursive: true });
  }
  
  const hookDirs = fs.readdirSync(HOOKS_IN_SKILL).filter(f => {
    return fs.statSync(path.join(HOOKS_IN_SKILL, f)).isDirectory();
  });
  
  let updatedCount = 0;
  
  for (const hookName of hookDirs) {
    const sourceDir = path.join(HOOKS_IN_SKILL, hookName);
    const targetDir = path.join(OPENCLAW_HOOKS_DIR, hookName);
    
    if (!fs.existsSync(targetDir)) {
      fs.mkdirSync(targetDir, { recursive: true });
      console.log(`  📁 创建目录: ${hookName}`);
    }
    
    const files = fs.readdirSync(sourceDir);
    for (const file of files) {
      const sourceFile = path.join(sourceDir, file);
      const targetFile = path.join(targetDir, file);
      
      // 比较文件内容
      const sourceHash = getFileHash(sourceFile);
      const targetHash = getFileHash(targetFile);
      
      if (sourceHash !== targetHash) {
        fs.copyFileSync(sourceFile, targetFile);
        console.log(`  ✅ 更新: ${hookName}/${file}`);
        updatedCount++;
      }
    }
  }
  
  // 保存新版本信息
  const version = {
    hash: skillHash,
    syncedAt: new Date().toISOString(),
    skillVersion: require(path.join(SKILL_DIR, 'package.json')).version
  };
  saveVersion(version);
  
  if (updatedCount > 0) {
    console.log(`\n✅ Hooks 同步完成，更新了 ${updatedCount} 个文件`);
    console.log(`   版本: ${version.skillVersion}`);
    console.log(`   时间: ${version.syncedAt}\n`);
  } else {
    console.log('\n✅ Hooks 已是最新版本（内容未变更）\n');
  }
  
  return true;
}

// 检查 hook 状态（不执行同步）
function checkStatus() {
  console.log('🔍 Hook 同步状态检查\n');
  
  const skillHash = getDirectoryHash(HOOKS_IN_SKILL);
  const installedVersion = getInstalledVersion();
  
  console.log(`  Skill 目录: ${HOOKS_IN_SKILL}`);
  console.log(`  系统目录: ${OPENCLAW_HOOKS_DIR}`);
  console.log(`  版本文件: ${VERSION_FILE}`);
  console.log();
  
  console.log(`  Skill hooks 哈希: ${skillHash?.substring(0, 16)}...`);
  
  if (installedVersion) {
    console.log(`  安装版本哈希: ${installedVersion.hash?.substring(0, 16)}...`);
    console.log(`  同步时间: ${installedVersion.syncedAt || '未知'}`);
    console.log(`  Skill 版本: ${installedVersion.skillVersion || '未知'}`);
    console.log();
    
    if (installedVersion.hash === skillHash) {
      console.log('  ✅ 状态: 已同步');
    } else {
      console.log('  ⚠️  状态: 需要同步（版本不一致）');
      console.log('  💡 运行: npm run sync-hooks');
    }
  } else {
    console.log('  安装版本: 未记录');
    console.log();
    console.log('  ⚠️  状态: 需要同步（首次安装）');
    console.log('  💡 运行: npm run sync-hooks');
  }
  
  console.log();
}

// CLI
const args = process.argv.slice(2);
const command = args[0];

if (command === 'status') {
  checkStatus();
} else if (command === 'force') {
  syncHooks(true);
} else {
  syncHooks(false);
}

module.exports = { syncHooks, checkStatus };

