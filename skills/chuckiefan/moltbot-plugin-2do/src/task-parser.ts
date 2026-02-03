import type { ParsedTask } from "./types.js";

// 任务前缀（含列表）模式：匹配 "添加任务到X列表：" 等
const TASK_PREFIX_WITH_LIST = /^(?:添加任务|创建待办|提醒我|记录任务|新建任务|加个任务)\s*到\s*(.+?)\s*列表\s*[：:]\s*/;

// 任务前缀模式：匹配 "添加任务："、"创建待办：" 等
const TASK_PREFIX_PATTERN = /^(?:添加任务|创建待办|提醒我|记录任务|新建任务|加个任务)\s*[：:]\s*/;

// 列表提取模式：匹配 "列表是X"、"到X列表" 等
const LIST_PATTERNS = [
    /[，,]\s*列表(?:是|为)\s*(.+?)(?=[，,]|$)/,
    /到\s*(.+?)\s*列表\s*[：:]\s*/,
    /到\s*(.+?)\s*列表(?=[，,]|$)/,
];

// 标签提取模式：匹配 "标签是X和Y"、"标记为X"、"标签X,Y" 等
const TAG_PATTERNS = [
    /[，,]\s*标签(?:是|为)\s*(.+?)(?=[，,](?!.*(?:标签|标记))|$)/,
    /[，,]\s*标记(?:为|是)\s*(.+?)(?=[，,](?!.*(?:标签|标记))|$)/,
];

// 标签分隔符
const TAG_SEPARATORS = /[、和,，\s]+/;

/** 从自然语言输入中解析任务信息 */
export function parseTask(input: string): ParsedTask {
    let text = input.trim();

    // 先尝试匹配包含列表信息的前缀（如 "添加任务到工作列表："）
    let list: string | undefined;
    const prefixListMatch = text.match(TASK_PREFIX_WITH_LIST);
    if (prefixListMatch) {
        list = prefixListMatch[1].trim();
        text = text.replace(prefixListMatch[0], "").trim();
    } else {
        // 移除普通任务前缀
        text = text.replace(TASK_PREFIX_PATTERN, "");
    }
    // 从正文中提取列表（仅在前缀中未提取到时）
    if (!list) {
        for (const pattern of LIST_PATTERNS) {
            const match = text.match(pattern);
            if (match) {
                list = match[1].trim();
                text = text.replace(match[0], "").trim();
                break;
            }
        }
    }

    // 提取标签
    let tags: string[] | undefined;
    for (const pattern of TAG_PATTERNS) {
        const match = text.match(pattern);
        if (match) {
            tags = match[1]
                .split(TAG_SEPARATORS)
                .map((t) => t.trim())
                .filter(Boolean);
            text = text.replace(match[0], "").trim();
            break;
        }
    }

    // 清理标题末尾的标点
    const title = text.replace(/[，,]+$/, "").trim();

    if (!title) {
        throw new Error("无法解析任务标题，请提供有效的任务描述");
    }

    return {
        title,
        ...(list && { list }),
        ...(tags && tags.length > 0 && { tags }),
    };
}

/** 构造 2Do 邮件主题 */
export function buildEmailSubject(task: ParsedTask): string {
    let subject = task.title;

    if (task.list) {
        subject += ` list(${task.list})`;
    }

    if (task.tags && task.tags.length > 0) {
        subject += ` tag(${task.tags.join(", ")})`;
    }

    return subject;
}

/** 构造邮件正文 */
export function buildEmailBody(_task: ParsedTask, rawInput?: string): string {
    const lines: string[] = [];

    if (rawInput) {
        lines.push(`任务详情：${rawInput}`);
        lines.push("");
    }

    lines.push(`创建时间：${new Date().toISOString()}`);
    lines.push("来源：Moltbot 2Do Task Email Skill");

    return lines.join("\n");
}
