#!/usr/bin/env python3
"""
验证码识别模块
支持：数字、字母、汉字、滑块、点选
"""

import os
import base64
import time
from PIL import Image
import pytesseract
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class CaptchaSolver:
    def __init__(self):
        self.driver = None
        self.screenshot_dir = "/root/.openclaw/screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def init_browser(self):
        """初始化浏览器"""
        options = Options()
        options.binary_location = "/usr/bin/chromium-browser"
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome(options=options)
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
    
    def screenshot_captcha(self, selector=None, filename="captcha.png"):
        """截图验证码"""
        if selector:
            # 截图指定元素
            elem = self.driver.find_element(By.CSS_SELECTOR, selector)
            elem.screenshot(os.path.join(self.screenshot_dir, filename))
        else:
            # 截全屏
            self.driver.save_screenshot(os.path.join(self.screenshot_dir, filename))
        return os.path.join(self.screenshot_dir, filename)
    
    def recognize_simple(self, image_path=None):
        """简单OCR识别（数字+字母）"""
        if image_path is None:
            image_path = os.path.join(self.screenshot_dir, "captcha.png")
        
        # 图像预处理
        img = Image.open(image_path)
        
        # 转为灰度
        img = img.convert('L')
        
        # 二值化
        threshold = 128
        img = img.point(lambda x: 255 if x > threshold else 0)
        
        # 识别
        result = pytesseract.image_to_string(img, config='--psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
        
        return result.strip()
    
    def recognize_number(self, image_path=None):
        """识别纯数字"""
        if image_path is None:
            image_path = os.path.join(self.screenshot_dir, "captcha.png")
        
        img = Image.open(image_path)
        img = img.convert('L')
        
        result = pytesseract.image_to_string(img, config='--psm 7 -c tessedit_char_whitelist=0123456789')
        return result.strip()
    
    def recognize_chinese(self, image_path=None):
        """识别中文"""
        if image_path is None:
            image_path = os.path.join(self.screenshot_dir, "captcha.png")
        
        img = Image.open(image_path)
        img = img.convert('L')
        
        result = pytesseract.image_to_string(img, lang='chi_sim')
        return result.strip()
    
    def get_position(self, image_path=None):
        """获取滑块位置（需要背景图和缺口图）"""
        # 后续实现
        pass
    
    def recognize_slider(self, background_path, gap_path):
        """识别滑块缺口距离"""
        # 后续实现
        pass


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("""
验证码识别工具

用法:
    python captcha.py recognize <图片路径>     识别数字字母
    python captcha.py number <图片路径>       识别纯数字
    python captcha.py chinese <图片路径>      识别中文
    python captcha.py test                  测试OCR
        """)
        sys.exit(1)
    
    cmd = sys.argv[1]
    solver = CaptchaSolver()
    
    if cmd == "recognize":
        path = sys.argv[2] if len(sys.argv) > 2 else "captcha.png"
        result = solver.recognize_simple(path)
        print(f"识别结果: {result}")
    
    elif cmd == "number":
        path = sys.argv[2] if len(sys.argv) > 2 else "captcha.png"
        result = solver.recognize_number(path)
        print(f"识别结果: {result}")
    
    elif cmd == "chinese":
        path = sys.argv[2] if len(sys.argv) > 2 else "captcha.png"
        result = solver.recognize_chinese(path)
        print(f"识别结果: {result}")
    
    elif cmd == "test":
        # 创建测试图片
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (150, 50), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), "ABC123", fill='black')
        test_path = "/root/.openclaw/screenshots/test_captcha.png"
        img.save(test_path)
        
        result = solver.recognize_simple(test_path)
        print(f"测试识别: {result}")


if __name__ == "__main__":
    main()
