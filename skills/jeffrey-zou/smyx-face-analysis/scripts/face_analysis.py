#!/usr/bin/env python3
import argparse
import json
import mimetypes
import traceback
from datetime import datetime

import requests
import sys

from config import *

from skill import skill

import_path_common()
from common.util import RequestUtil
from common.config import ConstantEnum as ConstantEnumBase

# 从config导入常量
SUPPORTED_FORMATS = ConstantEnum.SUPPORTED_FORMATS.value
MAX_FILE_SIZE_MB = ConstantEnum.MAX_FILE_SIZE_MB.value


def validate_file(file_path):
    """验证输入文件是否合法"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"文件没有读权限: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()[1:]
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f"不支持的文件格式，支持的格式: {', '.join(SUPPORTED_FORMATS)}")

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(f"文件过大，最大支持 {MAX_FILE_SIZE_MB}MB，当前文件大小: {file_size_mb:.1f}MB")

    return True


def analyze_video(input_path=None, url=None, api_url=None, api_key=None, output_level=None):
    """调用API分析视频"""
    if not input_path and not url:
        raise ValueError("必须提供本地视频路径(--input)或网络视频URL(--url)")
    try:
        input_path = input_path or url
        return skill.get_output_analysis(input_path)

    except requests.exceptions.RequestException as e:
        traceback.print_stack()
        raise Exception(f"API请求失败: {str(e)}")


def show_analyze_list(open_id, start_time=None, end_time=None):
    if not open_id:
        raise ValueError("必须提供本用户的OpenId/UserId")

    try:
        output_content = skill.get_output_analysis_list(open_id=open_id)
        return output_content

    except requests.exceptions.RequestException as e:
        traceback.print_stack()
        raise Exception(f"API请求失败: {str(e)}")


def get_analysis_export_url(request_id=None):
    """调用API分析视频"""
    if not request_id:
        return ""
    return ApiEnum.DETAIL_EXPORT_URL + request_id


def format_result(result, output_level="standard"):
    """格式化输出结果"""
    if output_level == "json":
        result_id = None
        # if result.get('success'):
        if result is not None:
            result_json = result
            result_id = result_json.get('id', {})
            result_json = json.dumps(result_json.get('faceAnalysisResponse', {}), ensure_ascii=False, indent=2)
        else:
            # result_json = json.dumps(result, ensure_ascii=False, indent=2)
            return "⚠️ 暂无分析结果"
        return f"""
📊 面诊分析结构化结果
{result_json}
""", result_id
    elif output_level == "basic":
        # 精简输出
        data = result.get('data', {})
        diagnosis = data.get('diagnosis', {})
        return f"""
📊 面诊分析结果
{'=' * 40}
整体体质: {diagnosis.get('overall_constitution', '未知')}
主要状况: {', '.join([f'{k}: {v}' for k, v in diagnosis.get('organ_condition', {}).items() if v != '正常'])}
健康提示: {data.get('health_warnings', ['无特殊警示'])[0] if data.get('health_warnings') else '无特殊警示'}
        """
    elif output_level == "standard":
        # 标准输出
        data = result.get('data', {})
        diagnosis = data.get('diagnosis', {})
        face_detection = data.get('face_detection', {})

        organ_status = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('organ_condition', {}).items()])
        warnings = "\n".join([f"  ⚠️  {item}" for item in data.get('health_warnings', [])])
        suggestions = "\n".join([f"  💡 {item}" for item in data.get('suggestions', [])])

        return f"""
📊 中医面诊分析报告
{'=' * 50}
⏰ 分析时间: {data.get('analysis_time', '未知')}
🎯 人脸检测: {face_detection.get('status', '未知')} (置信度: {face_detection.get('quality_score', 0)}分)

🔍 诊断结果:
  整体体质: {diagnosis.get('overall_constitution', '未知')}
  脏腑状况:
{organ_status}
  面色分析: {diagnosis.get('color_analysis', {}).get('complexion', '未知')}
  对应提示: {diagnosis.get('color_analysis', {}).get('correspondence', '未知')}

⚠️ 健康警示:
{warnings}

💡 养生建议:
{suggestions}
{'=' * 50}
        """
    else:
        # 完整输出（JSON格式）
        return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="中医面诊分析工具")
    parser.add_argument("--input", help="本地MP4视频文件路径")
    parser.add_argument("--url", help="网络视频MP4的URL地址")
    parser.add_argument("--open-id", help="当前用户的OpenID或UserId")
    parser.add_argument("--show-list", action='store_true', help="显示面诊视频历史列表清单")
    parser.add_argument("--api-url", help="服务端API地址")
    parser.add_argument("--api-key", help="API访问密钥（必需）")
    parser.add_argument("--output", help="结果输出文件路径")
    parser.add_argument("--detail", choices=["basic", "standard", "json"],
                        default=ConstantEnumBase.DEFAULT__OUTPUT_LEVEL,
                        help="输出详细程度")

    args = parser.parse_args()

    try:
        # 检查必需参数
        match args.show_list:
            case True:
                open_id = args.open_id or ConstantEnumBase.DEFAULT__OPEN_ID
                result = show_analyze_list(open_id)
                print(result)
                exit(0)
            case _:
                pass

        # 检查必需参数
        if not args.input and not args.url:
            print("❌ 错误: 必须提供 --input 或 --url 参数")
            exit(1)

        print("🔍 正在分析面诊视频，请稍候...")
        output_content = analyze_video(
            input_path=args.input,
            url=args.url,
            api_url=args.api_url,
            api_key=args.api_key,
            output_level=args.detail
        )

        print(output_content)

        # 保存到文件
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                if args.detail == "full":
                    json.dump(result, f, ensure_ascii=False, indent=2)
                else:
                    f.write(output_content)
            print(f"✅ 结果已保存到: {args.output}")

    except Exception as e:
        traceback.print_stack()
        print(f"❌ 面诊分析失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
