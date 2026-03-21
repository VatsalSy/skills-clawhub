#!/usr/bin/env python3
"""
浏览器自动化工具 - 登录/点击/填表
"""

import sys
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Browser:
    def __init__(self, headless=True, screenshot_dir="/root/.openclaw/screenshots"):
        self.driver = None
        self.headless = headless
        self.screenshot_dir = screenshot_dir
        os.makedirs(screenshot_dir, exist_ok=True)
        self.init()
    
    def init(self):
        options = Options()
        options.binary_location = "/usr/bin/chromium-browser"
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        self.driver = webdriver.Chrome(options=options)
    
    def navigate(self, url):
        """打开URL"""
        self.driver.get(url)
        print(f"已打开: {url}")
        return True
    
    def click(self, selector, by='css'):
        """点击元素"""
        try:
            if by == 'css':
                elem = self.driver.find_element(By.CSS_SELECTOR, selector)
            elif by == 'xpath':
                elem = self.driver.find_element(By.XPATH, selector)
            elif by == 'id':
                elem = self.driver.find_element(By.ID, selector)
            elif by == 'name':
                elem = self.driver.find_element(By.NAME, selector)
            elem.click()
            return True
        except Exception as e:
            print(f"点击失败: {e}")
            return False
    
    def input(self, selector, text, by='css'):
        """输入文本"""
        try:
            if by == 'css':
                elem = self.driver.find_element(By.CSS_SELECTOR, selector)
            elif by == 'xpath':
                elem = self.driver.find_element(By.XPATH, selector)
            elif by == 'id':
                elem = self.driver.find_element(By.ID, selector)
            elem.clear()
            elem.send_keys(text)
            return True
        except Exception as e:
            print(f"输入失败: {e}")
            return False
    
    def screenshot(self, name="screenshot.png"):
        """截图"""
        path = os.path.join(self.screenshot_dir, name)
        self.driver.save_screenshot(path)
        return path
    
    def get_html(self):
        """获取页面源码"""
        return self.driver.page_source
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    
    browser = Browser()
    
    if cmd == "navigate":
        url = sys.argv[2] if len(sys.argv) > 2 else "https://www.baidu.com"
        browser.navigate(url)
    
    elif cmd == "click":
        selector = sys.argv[2] if len(sys.argv) > 2 else ""
        browser.click(selector)
    
    elif cmd == "input":
        selector = sys.argv[2] if len(sys.argv) > 2 else ""
        text = sys.argv[3] if len(sys.argv) > 3 else ""
        browser.input(selector, text)
    
    elif cmd == "screenshot":
        name = sys.argv[2] if len(sys.argv) > 2 else "screenshot.png"
        path = browser.screenshot(name)
        print(f"截图: {path}")
    
    elif cmd == "html":
        print(browser.get_html())
    
    elif cmd == "help":
        print("""
浏览器自动化命令:
  navigate <URL>    打开网页
  click <selector>  点击元素 (css/xpath/id/name)
  input <selector> <text>  输入文本
  screenshot [name]  截图
  html             获取页面源码
        """)
    
    browser.close()

if __name__ == "__main__":
    main()
