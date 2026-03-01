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
    print(f"原始 result_text: {result_text}")
    print(f"原始 result_text repr: {repr(result_text)}")

    # 第一次解析（返回字符串）
    parsed1 = json.loads(result_text)
    print(f"\n第一次解析: {parsed1}")
    print(f"类型: {type(parsed1)}")

    # 第二次解析（应该返回列表）
    parsed2 = json.loads(parsed1)
    print(f"\n第二次解析: {parsed2}")
    print(f"类型: {type(parsed2)}")
    print(f"是列表? {isinstance(parsed2, list)}")

    # 简化版：使用 json.loads(json.loads(result_text))
    final = json.loads(json.loads(result_text))
    print(f"\n最终结果: {final}")
    print(f"类型: {type(final)}")
    print(f"是列表? {isinstance(final, list)}")
