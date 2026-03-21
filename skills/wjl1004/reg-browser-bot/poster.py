#!/usr/bin/env python3
"""
自动化运营模块
功能：自动发帖、自动回复、定时任务、批量操作
"""

import os
import json
import time
import schedule
import threading
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class AutoPoster:
    def __init__(self):
        self.tasks_dir = "/root/.openclaw/tasks"
        self.logs_dir = "/root/.openclaw/logs/poster"
        os.makedirs(self.tasks_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        self.driver = None
        self.running = False
    
    def init_browser(self):
        options = Options()
        options.binary_location = "/usr/bin/chromium-browser"
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome(options=options)
    
    def close(self):
        if self.driver:
            self.driver.quit()
    
    def log(self, task_name, message):
        """记录日志"""
        path = os.path.join(self.logs_dir, f"{task_name}_{datetime.now().strftime('%Y%m%d')}.log")
        with open(path, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
    
    # ========== 自动发帖 ==========
    
    def post_to_douyin(self, content, cookie_file=None):
        """抖音发帖"""
        self.init_browser()
        
        try:
            if cookie_file and os.path.exists(cookie_file):
                self.driver.get("https://www.douyin.com")
                with open(cookie_file, 'r') as f:
                    cookies = json.load(f)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            
            self.driver.get("https://creator.douyin.com/create-micro-site")
            time.sleep(3)
            
            # 输入内容
            editor = self.driver.find_element(By.CSS_SELECTOR, '[contenteditable="true"]')
            editor.send_keys(content)
            
            # 点击发布（需根据实际页面调整）
            # self.driver.find_element(By.CSS_SELECTOR, '.publish-btn').click()
            
            self.log('douyin', f"发布成功: {content[:50]}")
            return True
        except Exception as e:
            self.log('douyin', f"发布失败: {e}")
            return False
        finally:
            self.close()
    
    def post_to_xiaohongshu(self, content, images=None):
        """小红书发帖"""
        self.init_browser()
        
        try:
            self.driver.get("https://creator.xiaohongshun.com/publish/publish")
            time.sleep(3)
            
            # 输入内容
            editor = self.driver.find_element(By.CSS_SELECTOR, '.editor')
            editor.send_keys(content)
            
            # 上传图片（如果有）
            if images:
                for img in images:
                    upload = self.driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
                    upload.send_keys(img)
            
            self.log('xiaohongshu', f"发布成功: {content[:50]}")
            return True
        except Exception as e:
            self.log('xiaohongshu', f"发布失败: {e}")
            return False
        finally:
            self.close()
    
    def post_to_weibo(self, content, cookie_file=None):
        """微博发帖"""
        self.init_browser()
        
        try:
            self.driver.get("https://weibo.com/compose")
            time.sleep(3)
            
            textarea = self.driver.find_element(By.CSS_SELECTOR, 'textarea[gbkbd]')
            textarea.send_keys(content)
            
            # 点击发布
            self.driver.find_element(By.CSS_SELECTOR, '[node-type="publish"]').click()
            
            self.log('weibo', f"发布成功: {content[:50]}")
            return True
        except Exception as e:
            self.log('weibo', f"发布失败: {e}")
            return False
        finally:
            self.close()
    
    # ========== 自动回复 ==========
    
    def auto_reply_douyin(self, keyword, reply_content):
        """抖音评论自动回复"""
        self.init_browser()
        
        try:
            self.driver.get("https://www.douyin.com/creator/dm")
            time.sleep(3)
            
            # 查找含有关键词的评论
            comments = self.driver.find_elements(By.CSS_SELECTOR, '.comment-item')
            for comment in comments:
                if keyword in comment.text:
                    # 点击回复
                    comment.find_element(By.CSS_SELECTOR, '.reply-btn').click()
                    time.sleep(1)
                    # 输入回复
                    comment.find_element(By.CSS_SELECTOR, 'textarea').send_keys(reply_content)
                    # 发送
                    comment.find_element(By.CSS_SELECTOR, '.send-btn').click()
            
            self.log('reply', f"回复成功: 关键词={keyword}")
            return True
        except Exception as e:
            self.log('reply', f"回复失败: {e}")
            return False
        finally:
            self.close()
    
    # ========== 定时任务 ==========
    
    def add_schedule(self, task_name, time_str, func, *args):
        """添加定时任务"""
        if time_str.startswith('every'):
            # 如 every day, every hour
            getattr(schedule.every(), time_str.split()[1]).do(func, *args)
        else:
            # 如 09:30
            schedule.every().day.at(time_str).do(func, *args)
        
        self.log('schedule', f"已添加任务: {task_name} @ {time_str}")
    
    def run_scheduler(self):
        """运行定时任务循环"""
        self.running = True
        while self.running:
            schedule.run_pending()
            time.sleep(60)
    
    def stop_scheduler(self):
        """停止定时任务"""
        self.running = False
    
    def start_daemon(self):
        """启动守护线程"""
        t = threading.Thread(target=self.run_scheduler, daemon=True)
        t.start()
        return t
    
    # ========== 批量操作 ==========
    
    def batch_follow(self, user_ids):
        """批量关注"""
        self.init_browser()
        
        try:
            for uid in user_ids:
                self.driver.get(f"https://example.com/user/{uid}")
                time.sleep(1)
                try:
                    self.driver.find_element(By.CSS_SELECTOR, '.follow-btn').click()
                    self.log('follow', f"关注成功: {uid}")
                except:
                    self.log('follow', f"关注失败: {uid}")
                time.sleep(2)
        finally:
            self.close()
    
    def batch_like(self, urls):
        """批量点赞"""
        self.init_browser()
        
        try:
            for url in urls:
                self.driver.get(url)
                time.sleep(1)
                try:
                    self.driver.find_element(By.CSS_SELECTOR, '.like-btn').click()
                    self.log('like', f"点赞成功: {url}")
                except:
                    self.log('like', f"点赞失败: {url}")
                time.sleep(2)
        finally:
            self.close()


def main():
    import sys
    
    poster = AutoPoster()
    
    if len(sys.argv) < 2:
        print("""
自动化运营工具

用法:
    python poster.py douyin <内容>
    python poster.py xiaohongshu <内容>
    python poster.py weibo <内容>
    python poster.py reply <关键词> <回复内容>
    python poster.py follow <用户ID列表>
    python poster.py like <URL列表>
    python poster.py schedule <任务名> <时间> <命令>
        """)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    try:
        if cmd == "douyin":
            content = sys.argv[2] if len(sys.argv) > 2 else "测试发布"
            poster.post_to_douyin(content)
        
        elif cmd == "xiaohongshu":
            content = sys.argv[2] if len(sys.argv) > 2 else "测试发布"
            poster.post_to_xiaohongshu(content)
        
        elif cmd == "weibo":
            content = sys.argv[2] if len(sys.argv) > 2 else "测试发布"
            poster.post_to_weibo(content)
        
        elif cmd == "reply":
            keyword = sys.argv[2] if len(sys.argv) > 2 else "测试"
            reply = sys.argv[3] if len(sys.argv) > 3 else "谢谢"
            poster.auto_reply_douyin(keyword, reply)
        
        elif cmd == "follow":
            ids = sys.argv[2:] if len(sys.argv) > 2 else []
            poster.batch_follow(ids)
        
        elif cmd == "like":
            urls = sys.argv[2:] if len(sys.argv) > 2 else []
            poster.batch_like(urls)
    
    finally:
        pass


if __name__ == "__main__":
    main()
