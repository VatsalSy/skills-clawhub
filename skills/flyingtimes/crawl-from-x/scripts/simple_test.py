#!/usr/bin/env python3
import subprocess
import json

# 直接测试 evaluate 命令
cmd = ['openclaw', 'browser', 'evaluate',
       '--target-id', '8AA6A8899E6D8DD1A866A5EFFDD38B9F',
       '--fn', '(() => { return JSON.stringify(["test1","test2"]); })()']

result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

print(f"返回码: {result.returncode}")
print(f"stderr: {result.stderr}")
print(f"stdout（原始）:")
print(result.stdout)
print(f"\n{'='*60}")

# 清理输出
lines = result.stdout.split('\n')
for i, line in enumerate(lines):
    if line.strip().startswith(('[', '{', '"', "'")):
        result_text = '\n'.join(lines[i:])
        print(f"清理后的结果: {result_text}")
        print(f"类型: {type(result_text)}")

        # 解析
        try:
            parsed = json.loads(result_text)
            print(f"✅ 解析成功！")
            print(f"类型: {type(parsed)}")
            print(f"内容: {parsed}")
            print(f"是列表? {isinstance(parsed, list)}")
        except Exception as e:
            print(f"❌ 解析失败: {e}")
        break
