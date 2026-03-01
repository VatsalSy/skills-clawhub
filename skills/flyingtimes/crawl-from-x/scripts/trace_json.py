#!/usr/bin/env python3
import json
import sys

# 重新定义 json.loads 来追踪调用
original_loads = json.loads

def tracked_loads(s, **kwargs):
    print(f"🔶 json.loads 被调用！")
    print(f"    输入类型: {type(s)}")
    print(f"    输入长度: {len(s)}")
    print(f"    输入前 50 字符: {s[:50]}")

    result = original_loads(s, **kwargs)

    print(f"    输出类型: {type(result)}")
    print(f"    输出长度: {len(result)}")
    print(f"    输出是列表? {isinstance(result, list)}")
    print(f"    输出是字符串? {isinstance(result, str)}")

    return result

# 替换 json.loads
json.loads = tracked_loads

print(f"json.loads 已被替换: {json.loads}")

# 测试
test_str = '["test1","test2"]'
result = json.loads(test_str)

print(f"\n最终结果类型: {type(result)}")
print(f"最终结果: {result}")
print(f"最终结果是列表? {isinstance(result, list)}")
