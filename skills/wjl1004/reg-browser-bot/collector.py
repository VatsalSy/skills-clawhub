#!/usr/bin/env python3
"""
数据采集模块
功能：竞品监控、舆情监控、批量采集
"""

import os
import json
import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DataCollector:
    def __init__(self):
        self.driver = None
        self.data_dir = "/root/.openclaw/data"
        os.makedirs(self.data_dir, exist_ok=True)
    
    def init_browser(self, headless=True):
        options = Options()
        options.binary_location = "/usr/bin/chromium-browser"
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def close(self):
        if self.driver:
            self.driver.quit()
    
    def navigate(self, url):
        self.driver.get(url)
        time.sleep(2)
    
    def scroll_down(self, times=3):
        """滚动页面"""
        for _ in range(times):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
    
    def get_elements(self, selector, by='css'):
        """获取元素列表"""
        if by == 'css':
            return self.driver.find_elements(By.CSS_SELECTOR, selector)
        elif by == 'xpath':
            return self.driver.find_elements(By.XPATH, selector)
    
    def extract_text(self, elements):
        """提取文本列表"""
        return [e.text for e in elements if e.text.strip()]
    
    def save_json(self, data, filename):
        """保存JSON"""
        path = os.path.join(self.data_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path
    
    def save_csv(self, data, filename, headers=None):
        """保存CSV"""
        path = os.path.join(self.data_dir, filename)
        with open(path, 'w', encoding='utf-8', newline='') as f:
            if headers:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            else:
                writer = csv.writer(f)
                writer.writerows(data)
        return path
    
    # ========== 预设采集器 ==========
    
    def collect_taobao_products(self, keyword, pages=3):
        """采集淘宝商品"""
        results = []
        for page in range(1, pages + 1):
            url = f"https://s.taobao.com/search?q={keyword}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_{datetime.now().strftime('%Y%m%d')}&ie=utf8&page={page}"
            self.navigate(url)
            self.scroll_down(2)
            
            items = self.get_elements('.item')
            for item in items:
                try:
                    title = item.find_element(By.CSS_SELECTOR, '.title').text
                    price = item.find_element(By.CSS_SELECTOR, '.price').text
                    results.append({'标题': title, '价格': price})
                except:
                    pass
        
        return self.save_csv(results, f'taobao_{keyword}_{datetime.now().strftime("%Y%m%d")}.csv')
    
    def collect_jd_products(self, keyword, pages=3):
        """采集京东商品"""
        results = []
        for page in range(1, pages + 1):
            url = f"https://search.jd.com/Search?keyword={keyword}&enc=utf-8&page={page}"
            self.navigate(url)
            self.scroll_down(2)
            
            items = self.get_elements('.gl-item')
            for item in items:
                try:
                    title = item.find_element(By.CSS_SELECTOR, '.p-name em').text
                    price = item.find_element(By.CSS_SELECTOR, '.p-price strong i').text
                    results.append({'标题': title, '价格': price})
                except:
                    pass
        
        return self.save_csv(results, f'jd_{keyword}_{datetime.now().strftime("%Y%m%d")}.csv')
    
    def collect_douyin_products(self, keyword, pages=3):
        """采集抖音商品"""
        results = []
        url = f"https://www.douyin.com/search/{keyword}"
        self.navigate(url)
        self.scroll_down(3)
        
        items = self.get_elements('[data-e2e="search-item"]')
        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, '[class*="title"]').text
                price = item.find_element(By.CSS_SELECTOR, '[class*="price"]').text
                results.append({'标题': title, '价格': price})
            except:
                pass
        
        return self.save_csv(results, f'douyin_{keyword}_{datetime.now().strftime("%Y%m%d")}.csv')
    
    def monitor_price(self, url, selector):
        """监控价格"""
        self.navigate(url)
        try:
            price = self.driver.find_element(By.CSS_SELECTOR, selector).text
            return {'url': url, 'price': price, 'time': datetime.now().isoformat()}
        except:
            return {'url': url, 'price': None, 'time': datetime.now().isoformat()}


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("""
数据采集工具

用法:
    python collector.py taobao <关键词> [页数]
    python collector.py jd <关键词> [页数]
    python collector.py douyin <关键词> [页数]
    python collector.py monitor <URL> <选择器>
        """)
        sys.exit(1)
    
    cmd = sys.argv[1]
    collector = DataCollector()
    collector.init_browser()
    
    try:
        if cmd == "taobao":
            keyword = sys.argv[2] if len(sys.argv) > 2 else "白酒"
            pages = int(sys.argv[3]) if len(sys.argv) > 3 else 3
            path = collector.collect_taobao_products(keyword, pages)
            print(f"已保存: {path}")
        
        elif cmd == "jd":
            keyword = sys.argv[2] if len(sys.argv) > 2 else "白酒"
            pages = int(sys.argv[3]) if len(sys.argv) > 3 else 3
            path = collector.collect_jd_products(keyword, pages)
            print(f"已保存: {path}")
        
        elif cmd == "douyin":
            keyword = sys.argv[2] if len(sys.argv) > 2 else "白酒"
            path = collector.collect_douyin_products(keyword)
            print(f"已保存: {path}")
        
        elif cmd == "monitor":
            url = sys.argv[2] if len(sys.argv) > 2 else ""
            selector = sys.argv[3] if len(sys.argv) > 3 else ".price"
            result = collector.monitor_price(url, selector)
            print(json.dumps(result, ensure_ascii=False))
    finally:
        collector.close()


if __name__ == "__main__":
    main()
