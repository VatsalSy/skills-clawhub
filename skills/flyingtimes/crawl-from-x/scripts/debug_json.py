#!/usr/bin/env python3
import json

test_str = '["https://x.com/karpathy/status/2027521323275325622","https://x.com/karpathy/status/2027501331125239822"]'

print(f"输入字符串: {test_str}")
print(f"输入类型: {type(test_str)}")
print(f"输入长度: {len(test_str)}")

result = json.loads(test_str)

print(f"\n输出类型: {type(result)}")
print(f"输出长度: {len(result)}")
print(f"输出 repr: {repr(result)}")
print(f"输出 str: {str(result)}")
print(f"输出是列表? {isinstance(result, list)}")

# 打印每个字符（调试）
if isinstance(result, str):
    print(f"\n🔴 输出是字符串！逐字符打印:")
    for i, char in enumerate(result, 1):
        print(f"{i:3d}. '{char}'")
