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
    print(f"result_text repr: {repr(result_text)}")
    print(f"result_text bytes: {result_text.encode('utf-8')}")
    print(f"result_text length: {len(result_text)}")

    # 逐字符打印
    print(f"\n逐字符（hex）:")
    for i, char in enumerate(result_text):
        hex_val = hex(ord(char))
        print(f"{i:2d}. '{char}' -> {hex_val}")

    # 尝试解析
    try:
        parsed = json.loads(result_text)
        print(f"\njson.loads 结果: {parsed}")
        print(f"类型: {type(parsed)}")
    except Exception as e:
        print(f"\njson.loads 失败: {e}")
