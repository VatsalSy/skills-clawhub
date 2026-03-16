const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  console.log('🔍 详细 Cookie 测试...\n');
  
  // 读取配置
  const configPath = path.join(__dirname, '..', 'config.json');
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  
  console.log('📝 配置的 Cookie:');
  config.cookie.items.forEach(c => {
    console.log(`   ${c.name}: ${c.value.substring(0, 20)}...`);
  });
  console.log('');
  
  // 使用 headless: false 可以看到浏览器实际发生了什么
  const browser = await chromium.launch({
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const context = await browser.newContext({
    cookies: config.cookie.items.map(c => ({
      name: c.name,
      value: c.value,
      domain: c.domain || '.xiaohongshu.com',
      path: c.path || '/'
    }))
  });
  
  const page = await context.newPage();
  
  console.log('🌐 正在访问小红书...\n');
  
  try {
    await page.goto('https://www.xiaohongshu.com', {
      waitUntil: 'networkidle',
      timeout: 30000
    });
    
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    // 获取页面内容
    const content = await page.content();
    
    // 检查是否显示登录提示
    const hasLoginPrompt = await page.evaluate(() => {
      const text = document.body.textContent || '';
      return text.includes('登录后查看') || text.includes('请登录') || text.includes('Sign in');
    });
    
    // 检查是否显示探索页
    const hasExploreContent = await page.evaluate(() => {
      const title = document.querySelector('h1')?.textContent || '';
      return title.includes('小红书') || title.includes('Home');
    });
    
    console.log('📊 测试结果:');
    console.log(`   页面标题：${await page.title()}`);
    console.log(`   显示登录提示：${hasLoginPrompt}`);
    console.log(`   显示探索内容：${hasExploreContent}`);
    console.log('');
    
    if (hasLoginPrompt && !hasExploreContent) {
      console.log('❌ Cookie 无效 - 需要登录后才能访问');
      console.log('\n💡 可能原因:');
      console.log('   1. Cookie 已被服务器吊销');
      console.log('   2. Cookie 需要配合 IP 地址使用');
      console.log('   3. 账号需要短信验证');
      console.log('   4. Cookie 来自不同的浏览器/设备');
    } else if (hasExploreContent) {
      console.log('✅ Cookie 有效！');
      
      // 尝试访问搜索页
      await page.goto('https://www.xiaohongshu.com/search_result?keyword=测试');
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      const searchHasContent = await page.evaluate(() => {
        return document.querySelectorAll('.note-item').length > 0;
      });
      
      if (searchHasContent) {
        console.log('   ✓ 搜索功能正常');
      } else {
        console.log('   ✗ 搜索功能需要额外验证');
      }
    } else {
      console.log('⚠️  未知状态，请手动检查浏览器窗口');
    }
    
    console.log('\n👀 浏览器已打开，请手动验证 Cookie 状态');
    console.log('   如果登录成功，按 Ctrl+C 继续\n');
    
    // 等待用户操作
    await new Promise(() => {});
    
  } catch (error) {
    console.error('❌ 测试失败:', error.message);
  } finally {
    await browser.close();
  }
}

main();
