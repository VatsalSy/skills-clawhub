const { chromium } = require('playwright');
const path = require('path');

/**
 * 小红书 Cookie 测试工具
 * 
 * 测试 Cookie 是否有效，能够正常访问小红书内容
 */

// 加载配置
const configPath = path.join(__dirname, '..', 'config.json');
const fs = require('fs');
let config = {};

if (fs.existsSync(configPath)) {
  config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

async function testCookie() {
  console.log('🔍 小红书 Cookie 测试工具\n');
  console.log('═══════════════════════════════════════════\n');
  
  // 检查 Cookie 配置
  if (!config.cookie || !config.cookie.enabled) {
    console.log('❌ Cookie 未启用，请先配置 Cookie');
    console.log('   运行：node scripts/get-cookie.js');
    process.exit(1);
  }
  
  if (!config.cookie.items || config.cookie.items.length === 0) {
    console.log('❌ Cookie 列表为空，请先配置 Cookie');
    console.log('   运行：node scripts/get-cookie.js');
    process.exit(1);
  }
  
  console.log(`📋 Cookie 状态：已启用 (${config.cookie.items.length} 个 Cookie)\n`);
  
  let browser;
  try {
    console.log('🌐 启动浏览器...');
    browser = await chromium.launch({
      headless: config.playwright?.headless !== false,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    console.log('✅ 浏览器启动成功\n');
    
    console.log('🔧 创建页面上下文...');
    const context = await browser.newContext({
      userAgent: config.playwright?.user_agent || 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      viewport: { width: 1280, height: 720 }
    });
    
    // 添加 Cookie
    const cookies = config.cookie.items.map(c => ({
      name: c.name,
      value: c.value,
      domain: c.domain || '.xiaohongshu.com',
      path: c.path || '/'
    }));
    
    await context.addCookies(cookies);
    console.log(`✅ 已加载 ${cookies.length} 个 Cookie\n`);
    
    const page = await context.newPage();
    
    // 设置反检测脚本
    await page.addInitScript(() => {
      Object.defineProperty(navigator, 'webdriver', { get: () => false });
      Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
      Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en'] });
    });
    
    console.log('🔗 访问小红书主页...');
    const baseUrl = config.xhs?.base_url || 'https://www.xiaohongshu.com';
    
    await page.goto(baseUrl, {
      waitUntil: 'networkidle',
      timeout: 30000
    });
    
    console.log('✅ 页面加载成功\n');
    
    // 测试 1: 检查是否登录
    console.log('═══════════════════════════════════════════');
    console.log('📊 测试结果:\n');
    
    // 检查用户信息
    const isLoggedIn = await page.evaluate(() => {
      const userProfile = document.querySelector('.user-info');
      const searchBox = document.querySelector('.search-box');
      const loginButton = document.querySelector('a[href="/login"]');
      
      return {
        hasUserProfile: !!userProfile,
        hasSearchBox: !!searchBox,
        hasLoginButton: !!loginButton,
        url: window.location.href
      };
    });
    
    if (isLoggedIn.hasUserProfile || isLoggedIn.hasSearchBox) {
      console.log('✅ Cookie 有效！已登录状态');
      console.log(`   URL: ${isLoggedIn.url}`);
    } else if (isLoggedIn.hasLoginButton) {
      console.log('⚠️  Cookie 可能已过期，显示登录按钮');
      console.log('   建议重新获取 Cookie');
    } else {
      console.log('⚠️  页面状态异常，可能被风控');
      console.log(`   URL: ${isLoggedIn.url}`);
    }
    
    // 截图保存
    const screenshotPath = path.join(__dirname, '..', 'test-screenshot.png');
    await page.screenshot({ path: screenshotPath, fullPage: false });
    console.log(`\n📸 截图已保存到：${screenshotPath}`);
    
    // 测试 2: 尝试搜索
    console.log('\n🔍 测试搜索功能...');
    
    try {
      // 等待搜索框出现
      await page.waitForSelector('.search-box, input[type="text"]', { timeout: 5000 });
      
      // 点击搜索框
      const searchBox = await page.$('.search-box, input[type="text"]');
      if (searchBox) {
        await searchBox.click();
        await page.type('.search-box input, input[type="text"]', '测试');
        await page.keyboard.press('Enter');
        
        // 等待搜索结果
        await page.waitForNavigation({ timeout: 10000 }).catch(() => {});
        
        console.log('✅ 搜索功能正常');
      }
    } catch (e) {
      console.log('⚠️  搜索功能测试跳过 (可能需要手动操作)');
    }
    
    console.log('\n═══════════════════════════════════════════');
    console.log('✅ Cookie 测试完成\n');
    
  } catch (error) {
    console.error('\n❌ 测试失败:', error.message);
    console.error('\n建议:');
    console.log('1. 检查网络连接');
    console.log('2. 重新获取 Cookie: node scripts/get-cookie.js');
    console.log('3. 检查 config.json 配置是否正确\n');
    process.exit(1);
    
  } finally {
    if (browser) {
      // 保持浏览器打开几秒以便查看
      console.log('\n👀 5 秒后关闭浏览器...');
      await new Promise(resolve => setTimeout(resolve, 5000));
      await browser.close();
    }
  }
}

testCookie().catch(err => {
  console.error('❌ 错误:', err);
  process.exit(1);
});
