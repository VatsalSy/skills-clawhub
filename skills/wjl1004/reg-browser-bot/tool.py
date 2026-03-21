#!/usr/bin/env python3
"""
浏览器自动化工具箱
整合：浏览器控制、数据采集、账号管理、自动化运营、验证码识别
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

def main():
    if len(sys.argv) < 2:
        print("""
🤖 浏览器自动化工具箱

=== 基础功能 ===
browser.py navigate <URL>     打开网页
browser.py click <选择器>      点击元素
browser.py input <选择器> <内容>  输入文本
browser.py screenshot [名称]   截图

=== 验证码识别 ===
captcha.py recognize <图片>   识别数字字母
captcha.py number <图片>      识别纯数字
captcha.py chinese <图片>     识别中文

=== 数据采集 ===
collector.py taobao <关键词> [页数]  采集淘宝
collector.py jd <关键词> [页数]      采集京东
collector.py douyin <关键词>        采集抖音
collector.py monitor <URL> <选择器>  监控价格

=== 账号管理 ===
account.py add <名称> <平台> <用户名> <密码>
account.py list [平台]
account.py login <名称> <URL> <选择器>

=== 自动化运营 ===
poster.py douyin <内容>         发抖音
poster.py xiaohongshu <内容>    发小红书
poster.py weibo <内容>          发微博
poster.py reply <关键词> <回复>  自动回复
poster.py follow <用户ID...>    批量关注
poster.py like <URL...>         批量点赞

=== 快速开始 ===
python browser.py navigate https://www.baidu.com
python captcha.py test
python collector.py taobao 白酒 3
        """)
        sys.exit(1)
    
    module = sys.argv[1]
    args = sys.argv[2:]
    
    if module == "browser":
        from browser import Browser
        b = Browser()
        if len(args) > 0:
            if args[0] == "navigate" and len(args) > 1:
                b.navigate(args[1])
            elif args[0] == "screenshot":
                path = b.screenshot(args[1] if len(args) > 1 else "screenshot.png")
                print(f"截图: {path}")
        b.close()
    
    elif module == "captcha":
        from captcha import CaptchaSolver
        s = CaptchaSolver()
        if len(args) > 0:
            if args[0] == "test":
                from PIL import Image, ImageDraw
                img = Image.new('RGB', (150, 50), 'white')
                draw = ImageDraw.Draw(img)
                draw.text((10, 10), "ABC123", fill='black')
                path = "/root/.openclaw/screenshots/test.png"
                img.save(path)
                result = s.recognize_simple(path)
                print(f"测试结果: {result}")
        s.close()
    
    elif module == "collector":
        from collector import DataCollector
        c = DataCollector()
        c.init_browser()
        if len(args) > 0:
            if args[0] == "taobao":
                keyword = args[1] if len(args) > 1 else "白酒"
                pages = int(args[2]) if len(args) > 2 else 3
                path = c.collect_taobao_products(keyword, pages)
                print(f"已保存: {path}")
            elif args[0] == "jd":
                keyword = args[1] if len(args) > 1 else "白酒"
                pages = int(args[2]) if len(args) > 2 else 3
                path = c.collect_jd_products(keyword, pages)
                print(f"已保存: {path}")
        c.close()
    
    elif module == "account":
        from account import AccountManager
        mgr = AccountManager()
        if len(args) > 0:
            if args[0] == "list":
                accounts = mgr.list_accounts(args[1] if len(args) > 1 else None)
                for a in accounts:
                    print(f"- {a['name']}: {a['username']} ({a['platform']})")
            elif args[0] == "add" and len(args) >= 5:
                path = mgr.add_account(args[1], args[2], args[3], args[4])
                print(f"已添加: {path}")
        mgr.close()
    
    elif module == "poster":
        from poster import AutoPoster
        p = AutoPoster()
        if len(args) > 0:
            if args[0] == "douyin":
                p.post_to_douyin(args[1] if len(args) > 1 else "测试")
            elif args[0] == "weibo":
                p.post_to_weibo(args[1] if len(args) > 1 else "测试")
        p.close()
    
    else:
        print(f"未知模块: {module}")
        print("使用: python tool.py help 查看帮助")


if __name__ == "__main__":
    main()
