import json
import subprocess

cmd = ['openclaw', 'browser', 'evaluate',
       '--target-id', '8AA6A8899E6D8DD1A866A5EFFDD38B9F',
       '--fn', '(() => { return JSON.stringify(["test1","test2"]); })()']

result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

# 清理输出
lines = result.stdout.split('\n')
result_text = None
for line in lines:
    if line.strip().startswith(('[', '{', '"', "'")):
        result_text = line.strip()
        break

if result_text:
    print(f"result_text: {result_text}")
    print(f"result_text 类型: {type(result_text)}")
    print(f"json 模块: {json}")
    print(f"json.loads: {json.loads}")

    # 直接调用 json.loads 并打印类型
    parsed = json.loads(result_text)
    print(f"parsed: {parsed}")
    print(f"parsed 类型: {type(parsed)}")
    print(f"parsed 是列表? {isinstance(parsed, list)}")

    # 测试一个简单的 JSON
    simple_json = '["a","b"]'
    simple_parsed = json.loads(simple_json)
    print(f"\n简单测试:")
    print(f"  输入: {simple_json}")
    print(f"  输出: {simple_parsed}")
    print(f"  输出类型: {type(simple_parsed)}")
    print(f"  输出是列表? {isinstance(simple_parsed, list)}")
