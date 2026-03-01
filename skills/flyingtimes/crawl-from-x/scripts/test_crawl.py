#!/usr/bin/env python3
"""
测试版：修复后的 crawl 脚本
"""

import subprocess
import json
import time
from typing import Optional, Dict

class TestCrawler:
    def __init__(self):
        self.target_id = None

    def run_command(self, cmd: list, timeout: int = 30) -> subprocess.CompletedProcess:
        """运行命令"""
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result

    def parse_output(self, output: str) -> Optional[Dict]:
        """解析浏览器命令输出 - 修复版"""
        lines = output.split('\n')

        # 找到第一个 JSON 行（以 { 开头）
        json_start = None
        for i, line in enumerate(lines):
            if line.strip().startswith('{'):
                json_start = i
                break

        if json_start is None:
            # 处理纯 true/false
            output_stripped = output.strip()
            if output_stripped == "true":
                return {"ok": True, "result": True}
            if output_stripped == "false":
                return {"ok": True, "result": False}

            print(f"DEBUG: 无法解析输出。最后 500 字符:\n{output[-500:]}")
            return None

        # 从 JSON 开始行合并后面的所有行
        json_text = '\n'.join(lines[json_start:])

        try:
            response = json.loads(json_text)
            # 标准化返回格式
            if isinstance(response, dict):
                if response.get("ok"):
                    return response
                elif "result" in response:
                    return response
                else:
                    return {"ok": True, "result": response}
            elif isinstance(response, str):
                return {"ok": True, "result": response}
            else:
                return {"ok": True, "result": response}
        except json.JSONDecodeError as e:
            print(f"DEBUG: JSON 解析失败: {e}")
            print(f"JSON 开头 200 字符:\n{json_text[:200]}")
            return None

    def navigate(self, url: str) -> bool:
        """导航到 URL"""
        # 先导航
        cmd = ['openclaw', 'browser', 'navigate', url]
        result = self.run_command(cmd, timeout=20)

        if result.returncode != 0:
            print(f"❌ 导航失败: {result.stderr}")
            return False

        print(f"✅ 导航成功: {url}")

        # 然后获取 snapshot 来获取 targetId
        # 等待页面完全加载
        print("⏳ 等待页面加载...")
        time.sleep(5)

        cmd = ['openclaw', 'browser', 'snapshot', '--json']
        result = self.run_command(cmd, timeout=10)

        if result.returncode != 0:
            print(f"❌ snapshot 失败: {result.stderr}")
            return False

        response = self.parse_output(result.stdout)
        if response and response.get("ok"):
            self.target_id = response.get("targetId")
            print(f"✅ 获取 targetId: {self.target_id}")
            return True

        print(f"❌ snapshot 响应无效")
        return False

    def evaluate(self, js: str, timeout: int = 10) -> Optional[str]:
        """执行 JavaScript"""
        if not self.target_id:
            print("❌ 没有 targetId")
            return None

        # 使用 --fn 参数传递 JavaScript
        cmd = ['openclaw', 'browser', 'evaluate',
               '--target-id', self.target_id,
               '--fn', js]

        result = self.run_command(cmd, timeout=timeout)

        if result.returncode != 0:
            print(f"❌ evaluate 失败: {result.stderr}")
            return None

        # 清理输出：去掉开头的调试信息
        output = result.stdout
        lines = output.split('\n')

        # 找到实际结果（跳过调试信息）
        for i, line in enumerate(lines):
            if line.strip().startswith(('[', '{', '"', "'")):
                # 找到结果，合并后面的行
                result_text = '\n'.join(lines[i:])
                return result_text.strip()

        # 如果没有找到 JSON，直接返回清理后的输出
        return output.strip()

    def crawl_karpathy(self):
        """测试抓取 Karpathy"""
        print("=" * 60)
        print("开始测试抓取 @karpathy")
        print("=" * 60)

        # 检查 json 模块
        print(f"🔍 json 模块: {json}")
        print(f"🔍 json.loads: {json.loads}")

        # 导航
        if not self.navigate("https://x.com/karpathy"):
            return

        # 等待页面加载
        time.sleep(3)

        # 执行 JavaScript 提取 URL
        js_code = """(() => {
            const articles = document.querySelectorAll('article');
            const now = new Date();
            const oneDayAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000);
            const result = [];

            articles.forEach(article => {
                try {
                    const timeElement = article.querySelector('time');
                    if (!timeElement) return;

                    const datetime = timeElement.getAttribute('datetime');
                    if (!datetime) return;

                    const tweetDate = new Date(datetime);
                    if (tweetDate < oneDayAgo) return;

                    const links = article.querySelectorAll('a[href*="/status/"]');
                    for (const link of links) {
                        const href = link.getAttribute('href');
                        if (href && href.includes('/status/')) {
                            const statusId = href.split('/status/')[1].split('/')[0];
                            const fullUrl = 'https://x.com' + href.split('/status/')[0] + '/status/' + statusId;
                            if (!result.includes(fullUrl)) {
                                result.push(fullUrl);
                            }
                            break;
                        }
                    }
                } catch (e) {
                    // Skip this article
                }
            });

            return JSON.stringify(result);
        })()"""

        result = self.evaluate(js_code, timeout=15)

        print(f"\n🔍 调试: result 类型={type(result)}, 长度={len(result)}")
        print(f"🔍 result 前 100 字符: {result[:100]}")

        if result:
            try:
                print(f"🔍 尝试 JSON 解析...")
                print(f"🔍 原始 result: {result}")

                # 测试 json.loads
                test_json = '["test1","test2"]'
                test_result = json.loads(test_json)
                print(f"🔍 测试 json.loads: 输入={test_json}, 输出类型={type(test_result)}, 输出={test_result}")

                urls = json.loads(result)
                print(f"✅ JSON 解析成功！")
                print(f"🔍 urls 类型={type(urls)}, id={id(urls)}")
                print(f"🔍 urls 长度={len(urls)}")
                print(f"🔍 urls 是列表? {isinstance(urls, list)}")
                print(f"🔍 urls 是字符串? {isinstance(urls, str)}")
                print(f"🔍 urls 内容: {urls}")
                print(f"\n{'=' * 60}")
                print(f"✅ 成功抓取到 {len(urls)} 条帖子")
                print(f"{'=' * 60}")
                for i, url in enumerate(urls, 1):
                    print(f"{i}. {url}")
                return urls
            except json.JSONDecodeError as e:
                print(f"❌ JSON 解析失败: {e}")
                print(f"原始结果（前 200 字符）: {result[:200]}")
                return []
        else:
            print(f"\n❌ 没有抓取到帖子")
            return []

if __name__ == "__main__":
    crawler = TestCrawler()
    crawler.crawl_karpathy()
