const { chromium } = require('playwright');

async function main() {
  console.log('🔍 测试不依赖 Cookie 的数据获取...\n');
  
  const browser = await chromium.launch({
    headless: false
  });
  
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    // 访问 explore 页面（公开页面）
    await page.goto('https://www.xiaohongshu.com/explore', {
      waitUntil: 'networkidle',
      timeout: 30000
    });
    
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    // 获取页面内容
    const title = await page.title();
    console.log('页面标题:', title);
    
    // 检查是否可以看到内容
    const hasContent = await page.evaluate(() => {
      const items = document.querySelectorAll('.note-item');
      return items.length;
    });
    
    console.log('找到的笔记元素:', hasContent);
    
    if (hasContent > 0) {
      console.log('\n✅ 可以访问公开内容（无需登录）');
      
      // 获取前 5 个笔记的信息
      const notes = await page.evaluate(() => {
        const items = Array.from(document.querySelectorAll('.note-item')).slice(0, 5);
        return items.map(el => {
          const title = el.querySelector('.footer .title span')?.textContent?.trim();
          const link = el.querySelector('a[href^="/explore/"]')?.href;
          return { title, link };
        });
      });
      
      console.log('\n获取到的笔记:');
      notes.forEach((note, idx) => {
        console.log(`${idx + 1}. ${note.title}`);
        console.log(`   ${note.link}`);
      });
      
      console.log('\n💡 结论:');
      console.log('   - 公开内容（explore 页面）可以正常访问');
      console.log('   - 搜索页面可能需要登录才能看到结果');
      
    } else {
      console.log('\n⚠️  无法获取内容，可能需要登录');
    }
    
  } catch (error) {
    console.error('❌ 测试失败:', error.message);
  } finally {
    await browser.close();
  }
}

main();
