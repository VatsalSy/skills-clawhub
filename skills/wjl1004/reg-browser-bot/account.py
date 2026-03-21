#!/usr/bin/env python3
"""
账号管理模块
功能：多账号管理、Cookie保持、自动登录
"""

import os
import json
import time
import pickle
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class AccountManager:
    def __init__(self):
        self.accounts_dir = "/root/.openclaw/accounts"
        os.makedirs(self.accounts_dir, exist_ok=True)
        self.driver = None
    
    def init_browser(self, profile=None):
        """初始化浏览器，可指定配置"""
        options = Options()
        options.binary_location = "/usr/bin/chromium-browser"
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        
        if profile:
            # 使用指定用户配置
            options.add_argument(f'--user-data-dir={profile}')
        
        self.driver = webdriver.Chrome(options=options)
    
    def close(self):
        if self.driver:
            self.driver.quit()
    
    def save_cookies(self, name):
        """保存Cookies"""
        path = os.path.join(self.accounts_dir, f"{name}_cookies.json")
        cookies = self.driver.get_cookies()
        with open(path, 'w') as f:
            json.dump(cookies, f)
        return path
    
    def load_cookies(self, name):
        """加载Cookies"""
        path = os.path.join(self.accounts_dir, f"{name}_cookies.json")
        if not os.path.exists(path):
            return False
        
        self.driver.get("https://www.baidu.com")  # 先访问域名
        with open(path, 'r') as f:
            cookies = json.load(f)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        return True
    
    def save_session(self, name):
        """保存完整会话"""
        path = os.path.join(self.accounts_dir, f"{name}_session")
        with open(path, 'wb') as f:
            pickle.dump(self.driver, f)
        return path
    
    def load_session(self, name):
        """恢复会话"""
        path = os.path.join(self.accounts_dir, f"{name}_session")
        if not os.path.exists(path):
            return False
        with open(path, 'rb') as f:
            self.driver = pickle.load(f)
        return True
    
    def login(self, url, username_selector, password_selector, username, password, submit_selector=None):
        """通用登录"""
        self.driver.get(url)
        time.sleep(2)
        
        # 输入用户名
        elem = self.driver.find_element(By.CSS_SELECTOR, username_selector)
        elem.clear()
        elem.send_keys(username)
        
        # 输入密码
        elem = self.driver.find_element(By.CSS_SELECTOR, password_selector)
        elem.clear()
        elem.send_keys(password)
        
        # 提交
        if submit_selector:
            elem = self.driver.find_element(By.CSS_SELECTOR, submit_selector)
            elem.click()
        else:
            elem.send_keys(Keys.RETURN)
        
        time.sleep(3)
        return self.driver.current_url
    
    def is_logged_in(self, url, check_selector):
        """检查是否已登录"""
        self.driver.get(url)
        time.sleep(2)
        try:
            self.driver.find_element(By.CSS_SELECTOR, check_selector)
            return True
        except:
            return False
    
    def add_account(self, name, platform, username, password, cookies=None):
        """添加账号"""
        account = {
            'name': name,
            'platform': platform,
            'username': username,
            'password': password,  # 建议加密存储
            'cookies': cookies,
            'created': datetime.now().isoformat(),
            'last_used': None
        }
        path = os.path.join(self.accounts_dir, f"{name}.json")
        with open(path, 'w') as f:
            json.dump(account, f, ensure_ascii=False, indent=2)
        return path
    
    def list_accounts(self, platform=None):
        """列出账号"""
        accounts = []
        for f in os.listdir(self.accounts_dir):
            if f.endswith('.json'):
                with open(os.path.join(self.accounts_dir, f), 'r') as f:
                    account = json.load(f)
                    if platform is None or account.get('platform') == platform:
                        accounts.append(account)
        return accounts
    
    def get_account(self, name):
        """获取账号信息"""
        path = os.path.join(self.accounts_dir, f"{name}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return None
    
    def update_last_used(self, name):
        """更新最后使用时间"""
        path = os.path.join(self.accounts_dir, f"{name}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                account = json.load(f)
            account['last_used'] = datetime.now().isoformat()
            with open(path, 'w') as f:
                json.dump(account, f, ensure_ascii=False, indent=2)
    
    def delete_account(self, name):
        """删除账号"""
        for f in [f"{name}.json", f"{name}_cookies.json", f"{name}_session"]:
            path = os.path.join(self.accounts_dir, f)
            if os.path.exists(path):
                os.remove(path)


def main():
    import sys
    
    mgr = AccountManager()
    
    if len(sys.argv) < 2:
        print("""
账号管理工具

用法:
    python account.py add <名称> <平台> <用户名> <密码>
    python account.py list [平台]
    python account.py get <名称>
    python account.py delete <名称>
    python account.py login <名称> <URL> <用户名选择器> <密码选择器>
    python account.py save_cookies <名称>
    python account.py load_cookies <名称>
        """)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    try:
        if cmd == "add":
            name = sys.argv[2]
            platform = sys.argv[3]
            username = sys.argv[4]
            password = sys.argv[5]
            path = mgr.add_account(name, platform, username, password)
            print(f"账号已添加: {path}")
        
        elif cmd == "list":
            platform = sys.argv[2] if len(sys.argv) > 2 else None
            accounts = mgr.list_accounts(platform)
            for a in accounts:
                print(f"- {a['name']} ({a['platform']}): {a['username']}")
        
        elif cmd == "get":
            name = sys.argv[2]
            account = mgr.get_account(name)
            print(json.dumps(account, ensure_ascii=False, indent=2))
        
        elif cmd == "delete":
            name = sys.argv[2]
            mgr.delete_account(name)
            print(f"账号已删除")
        
        elif cmd == "login":
            name = sys.argv[2]
            url = sys.argv[3]
            user_sel = sys.argv[4]
            pass_sel = sys.argv[5]
            
            account = mgr.get_account(name)
            if not account:
                print("账号不存在")
                sys.exit(1)
            
            mgr.init_browser()
            mgr.login(url, user_sel, pass_sel, account['username'], account['password'])
            mgr.save_cookies(name)
            mgr.update_last_used(name)
            print("登录成功并保存Cookies")
            mgr.close()
    finally:
        pass


if __name__ == "__main__":
    main()
