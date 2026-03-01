#!/usr/bin/env python3
import json

class Test:
    def __init__(self):
        pass

    def test(self):
        print(f"json 模块: {json}")
        print(f"json.loads: {json.loads}")

        test_str = '["test1","test2"]'
        print(f"\n输入: {test_str}")
        print(f"输入类型: {type(test_str)}")

        result = json.loads(test_str)
        print(f"\n输出类型: {type(result)}")
        print(f"输出是列表? {isinstance(result, list)}")
        print(f"输出: {result}")

t = Test()
t.test()
