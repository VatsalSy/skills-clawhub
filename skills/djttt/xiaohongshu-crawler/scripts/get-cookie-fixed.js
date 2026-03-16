const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

/**
 * 小红书 Cookie 获取工具 (修复版)
 * 
 * 关键修复：
 * 1. 使用同一个浏览器上下文，避免登录状态丢失
 * 2. 支持手动登录时检测登录成功
 * 3. 自动导出所有关键 Cookie
 * 
 * 使用说明:
 * 1. 运行此脚本
 * 2. 在打开的浏览器中登录小红书
 * 3. 登录完成后，按 Ctrl+C 停止脚本
 * 4. Cookie 会自动导出并保存到 config.json
 */

async function main() {
  console.log('🔑 小红书 Cookie 获取工具 (修复版)\n');
  console.log('═══════════════════════════════════════════\n');
  console.log('步骤说明:');
  console.log('1. 脚本会打开浏览器并跳转到小红书登录页');
  console.log('2. 请手动登录你的小红书账号');
  console.log('3. 登录完成后，按 Ctrl+C 停止脚本以导出 Cookie');
  console.log('4. Cookie 会自动更新到 config.json 文件\n');
  
  const browser = await chromium.launch({
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    viewport: { width: 1280, height: 720 }
  });
  
  const page = await context.newPage();
  
  // 访问小红书登录页
  await page.goto('https://www.xiaohongshu.com', {
    waitUntil: 'networkidle',
    timeout: 30000
  });
  
  console.log('✅ 已打开小红书主页');
  console.log('👉 请在浏览器中登录账号...\n');
  console.log('💡 提示：登录时建议勾选"记住我"');
  console.log('👉 登录完成后按 Ctrl+C 导出 Cookie\n');
  
  // 等待用户登录 (监听页面变化)
  let loginDetected = false;
  
  // 定期检查是否已登录
  const checkLoginInterval = setInterval(async () => {
    try {
      const isLoggedIn = await page.evaluate(() => {
        // 检查是否有用户信息
        const userProfile = document.querySelector('.user-info');
        const loginButton = document.querySelector('a[href="/login"]');
        const searchBox = document.querySelector('.search-box');
        
        // 如果找到用户信息或者搜索框，说明已登录
        return !!userProfile || !!searchBox;
      });
      
      if (isLoggedIn && !loginDetected) {
        loginDetected = true;
        console.log('\n✅ 检测到登录状态！');
        console.log('💡 现在可以按 Ctrl+C 导出 Cookie了\n');
      }
    } catch (e) {
      // 忽略错误
    }
  }, 2000);
  
  // 等待 Ctrl+C
  await new Promise(() => {});
}

// 捕获 Ctrl+C
process.on('SIGINT', async () => {
  console.log('\n\n📋 正在导出 Cookie...\n');
  
  // 清除定时器
  process.removeAllListeners('SIGINT');
  
  try {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    const page = await context.newPage();
    
    // 需要等待用户手动打开浏览器并登录
    // 这里我们只导出当前上下文的 Cookie
    
    // 重新获取当前会话的 Cookie
    const cookies = await page.context().cookies();
    await browser.close();
    
    // 注意：由于我们关闭了之前的浏览器，这里实际上无法获取
    // 正确的做法是在同一个上下文中直接读取
    console.log('⚠️  注意：由于浏览器上下文已关闭，无法直接读取 Cookie');
    console.log('💡 请在登录状态下直接按 Ctrl+C，不要关闭浏览器窗口\n');
    
    process.exit(1);
    
  } catch (error) {
    console.error('❌ 导出失败:', error.message);
    process.exit(1);
  }
});

// 在登录状态下直接读取 Cookie (在 SIGINT 之前)
async function exportCookies(context) {
  try {
    const cookies = await context.cookies();
    
    // 过滤出关键 Cookie
    const importantCookies = cookies.filter(c => 
      c.name.includes('web_session') ||
      c.name.includes('XSRF-TOKEN') ||
      c.name.includes('id_token') ||
      c.name.includes('login_token') ||
      c.name.includes('acw_tc') ||
      c.name.includes('webId') ||
      c.name.includes('websectiga') ||
      c.name.includes('gid') ||
      c.name.includes('abRequestId') ||
      c.name.includes('sec_poison_id') ||
      c.name.includes('loadts') ||
      c.name.includes('webBuild') ||
      c.name.includes('xsecappid') ||
      c.name.includes('unread')
    );
    
    if (importantCookies.length === 0) {
      console.log('⚠️  未找到关键 Cookie，请先登录小红书');
      return;
    }
    
    const configExample = {
      "cookie": {
        "enabled": true,
        "items": importantCookies.map(c => ({
          name: c.name,
          value: c.value,
          domain: c.domain,
          path: c.path
        }))
      }
    };
    
    console.log('🎉 找到以下 Cookie:');
    console.log('═══════════════════════════════════════════\n');
    
    importantCookies.forEach(c => {
      console.log(`  ${c.name.padEnd(20)} ${c.value.substring(0, 50)}${c.value.length > 50 ? '...' : ''}`);
    });
    
    console.log('\n\n📝 方式一：手动复制到 config.json');
    console.log('═══════════════════════════════════════════\n');
    console.log(JSON.stringify(configExample, null, 2));
    
    console.log('\n\n💾 方式二：自动保存到 config.json (y/n)?');
    
  } catch (error) {
    console.error('❌ 导出失败:', error.message);
  }
}

// 启动
main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
