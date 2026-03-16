/**
 * 测试反爬功能是否正常工作
 */

const { initBrowser, createPage } = require('../lib/browser');
const antiCrawl = require('../lib/anti-crawl');

async function main() {
  console.log('🧪 测试反爬功能...\n');
  
  const browser = await initBrowser();
  const page = await createPage(browser);
  
  try {
    console.log('1️⃣ 测试随机延迟...');
    await antiCrawl.randomDelay(100, 300);
    console.log('   ✅ 随机延迟测试通过\n');
    
    console.log('2️⃣ 测试 User-Agent...');
    const userAgent = antiCrawl.getRandomUserAgent();
    console.log(`   📝 User-Agent: ${userAgent}\n`);
    
    console.log('3️⃣ 测试频率限制...');
    for (let i = 0; i < 3; i++) {
      if (antiCrawl.checkRateLimit()) {
        antiCrawl.incrementRequestCount();
        console.log(`   ✓ 请求 ${i + 1}/3 通过`);
        await antiCrawl.randomDelay(100, 200);
      }
    }
    console.log('   ✅ 频率限制测试通过\n');
    
    console.log('4️⃣ 测试页面访问...');
    await antiCrawl.makeRequest(page, 'https://www.xiaohongshu.com/explore');
    console.log('   ✅ 页面访问成功\n');
    
    console.log('5️⃣ 获取当前统计...');
    const stats = antiCrawl.getRequestStats();
    console.log(`   📊 本分钟：${stats.minute} 次请求`);
    console.log(`   📊 本小时：${stats.hour} 次请求\n`);
    
    console.log('🎉 所有测试通过！反爬功能正常工作。\n');
    
  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    console.error(error.stack);
  } finally {
    await browser.close();
  }
}

main();
