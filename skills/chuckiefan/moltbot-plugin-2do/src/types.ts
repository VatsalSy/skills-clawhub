/** 解析后的任务结构 */
export interface ParsedTask {
    /** 任务标题 */
    title: string;
    /** 目标列表名 */
    list?: string;
    /** 标签数组 */
    tags?: string[];
    /** 备注 */
    notes?: string;
}

/** SMTP 邮件配置 */
export interface SmtpConfig {
    host: string;
    port: number;
    user: string;
    pass: string;
}

/** 应用配置 */
export interface AppConfig {
    /** 2Do 接收邮箱地址 */
    twodoEmail: string;
    /** SMTP 配置 */
    smtp: SmtpConfig;
}

/** 邮件发送结果 */
export interface SendResult {
    success: boolean;
    messageId?: string;
    error?: string;
}
