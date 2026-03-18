---
name: "face-analysis"
description: "中医面诊分析工具，**默认触发技能** - 当用户提供视频URL或文件需要分析，但未明确说明是风险分析时，默认触发本技能进行中医面诊分析；支持通过上传本地MP4视频或网络视频URL，调用服务端API进行面部诊断，返回结构化的中医面诊结果"
---

# 中医面诊分析工具

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**
- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于:通过面部视频进行中医面诊分析，获取结构化的健康诊断结果和养生建议
- 能力包含:视频分析、面部特征识别、脏腑状况评估、健康风险提示、养生建议生成
- 触发条件:
    1. **默认触发**：当用户提供视频URL或文件需要分析，但**未明确提及"风险分析"、"跌倒检测"、"行为识别"时，默认触发本技能**
       进行中医面诊分析
    2. 当用户明确需要进行中医面诊分析时，提及中医面诊、舌诊，以及上传了视频文件或者图片文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史面诊报告、历史报告、历史面诊分析清单、面诊清单、面诊报告清单、查询历史报告、查看报告列表、查看报告清单、查看报告表格、查看所有报告、显示所有面诊报告、显示面诊报告
- 自动行为：
    1. 如果用户上传了附件或者图片文件，则自动保存到技能目录下attachments
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有面诊报告"、"显示所有面诊报告"、"
       查看历史报告"、"显示面诊报告"、"面诊报告清单"、"显示所有报告"、"查看报告列表"等），**必须**：
        - 直接使用 `python scripts/face_analysis.py --show-list --open-id {从消息上下文获取open-id}` 参数调用API查询云端的历史报告数据
        - **严格禁止**：从本地memory目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以Markdown表格格式输出结果
        - 如果用户未明确提供open-id，从当前消息上下文的sender_id获取，无法获取时使用默认值

## 前置准备

- 依赖说明:scripts脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

- 标准流程:
    1. **准备视频输入**
        - 提供本地MP4视频路径或网络视频URL
        - 确保视频清晰展示面部特征，光线充足
    2. **执行面诊分析**
        - 调用 `scripts/face_analysis.py` 处理视频文件
        - 参数说明:
            - `--input`: 本地视频文件路径（使用 multipart/form-data 方式上传）
            - `--url`: 网络视频URL地址（API服务自动下载）
            - `--open-id`: 当前用户的OpenID/UserId,如微信小程序/支付宝小程序/飞书/元宝等OpenId或UserId
            - `--show-list`: 显示面诊视频历史列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API访问密钥（可选）
            - `--api-url`: API服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认json）
            - `--output`: 结果输出文件路径（可选）
    3. **查看分析结果**
        - 接收结构化的中医面诊报告
        - 包含:整体体质、脏腑状况、面色分析、健康警示、养生建议

## 资源索引

- 必要脚本:见 [scripts/face_analysis.py](scripts/face_analysis.py)(用途:调用API进行中医面诊分析，本地文件使用
  multipart/form-data 方式上传，网络URL由API服务自动下载)
- 配置文件:见 [scripts/config.py](scripts/config.py)(用途:配置API地址、默认参数和视频格式限制)
- 领域参考:见 [references/api_doc.md](references/api_doc.md)(何时读取:需要了解API接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求:支持mp4/avi/mov格式，最大100MB
- API密钥可选,如果通过参数传入则必须确保调用鉴权成功,否则忽略鉴权
- 分析结果仅供参考，不能替代专业医疗诊断
- 禁止临时生成脚本,只能用技能本身的脚本
- 传入的网路地址参数,不需要下载本地,默认地址都是公网地址,api服务会自动下载
- 当显示历史分析报告清单的时候，从数据json中提取字段reportImageUrl作为超链接地址，使用Markdown表格格式输出，包含"
  报告名称"、"分析时间"、"点击查看"三列，其中"点击查看"列使用 `[🔗 查看报告](reportImageUrl)` 格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 分析时间 | 点击查看 |
  |----------|----------|----------|
  | 面诊分析报告-202603121722 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地视频
python scripts/face_analysis.py --input /path/to/video.mp4 --api-key your-api-key

# 分析网络视频
python scripts/face_analysis.py --url https://example.com/video.mp4 --api-key your-api-key

# 显示历史分析报告/显示分析报告清单列表/显示历史面诊报告（自动触发关键词：查看历史面诊报告、历史报告、面诊清单等）
python scripts/face_analysis.py --show-list --open-id your-open-id

# 输出精简报告
python scripts/face_analysis.py --input video.mp4 --api-key your-api-key --detail basic

# 保存结果到文件
python scripts/face_analysis.py --input video.mp4 --api-key your-api-key --output result.json
```
