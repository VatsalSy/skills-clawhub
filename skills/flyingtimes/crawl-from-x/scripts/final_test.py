#!/usr/bin/env python3
import subprocess
import json

def test_evaluate():
    """测试 evaluate 命令并解析结果"""
    cmd = ['openclaw', 'browser', 'evaluate',
           '--target-id', '8AA6A8899E6D8DD1A866A5EFFDD38B9F',
           '--fn', """(() => {
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
            })()"""]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)

    # 清理输出
    lines = result.stdout.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith(('[', '{', '"', "'")):
            result_text = '\n'.join(lines[i:])
            print(f"原始结果类型: {type(result_text)}")
            print(f"原始结果长度: {len(result_text)}")
            print(f"原始结果前 100 字符: {result_text[:100]}")

            # 解析 JSON（需要两次，因为输出被转义）
            print(f"\n✅ 开始 JSON 解析...")
            print(f"json 模块: {json}")

            # 第一次解析：去除转义，得到 JSON 字符串
            parsed1 = json.loads(result_text)
            print(f"第一次解析后类型: {type(parsed1)}")

            # 第二次解析：解析 JSON 字符串为 Python 对象
            urls = json.loads(parsed1)
            print(f"第二次解析后类型: {type(urls)}")
            print(f"最终结果是列表? {isinstance(urls, list)}")
            print(f"最终结果长度: {len(urls)}")

            print(f"\n{'=' * 60}")
            print(f"✅ 成功抓取到 {len(urls)} 条帖子")
            print(f"{'=' * 60}")
            for i, url in enumerate(urls, 1):
                print(f"{i}. {url}")
            return urls

    print("❌ 未找到 JSON 结果")
    return []

if __name__ == "__main__":
    test_evaluate()
