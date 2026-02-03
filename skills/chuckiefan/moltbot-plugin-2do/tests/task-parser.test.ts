import { describe, expect, it } from "vitest";
import { buildEmailBody, buildEmailSubject, parseTask } from "../src/task-parser.js";

describe("parseTask", () => {
    it("应解析基本任务", () => {
        const result = parseTask("添加任务：买牛奶");
        expect(result).toEqual({ title: "买牛奶" });
    });

    it("应解析不同前缀的任务", () => {
        expect(parseTask("创建待办：写报告").title).toBe("写报告");
        expect(parseTask("提醒我：打电话").title).toBe("打电话");
        expect(parseTask("记录任务：开会").title).toBe("开会");
    });

    it("应解析无前缀的输入", () => {
        const result = parseTask("明天去超市买东西");
        expect(result.title).toBe("明天去超市买东西");
    });

    it("应提取列表信息 - '到X列表' 格式", () => {
        const result = parseTask("添加任务到工作列表：完成项目报告");
        expect(result.title).toBe("完成项目报告");
        expect(result.list).toBe("工作");
    });

    it("应提取列表信息 - '列表是X' 格式", () => {
        const result = parseTask("添加任务：完成报告，列表是工作");
        expect(result.title).toBe("完成报告");
        expect(result.list).toBe("工作");
    });

    it("应提取标签信息 - '标签是X和Y' 格式", () => {
        const result = parseTask("添加任务：买菜，标签是家务和购物");
        expect(result.title).toBe("买菜");
        expect(result.tags).toEqual(["家务", "购物"]);
    });

    it("应同时提取列表和标签", () => {
        const result = parseTask("添加任务：完成季度报告，列表是工作，标签是紧急和财务");
        expect(result.title).toBe("完成季度报告");
        expect(result.list).toBe("工作");
        expect(result.tags).toEqual(["紧急", "财务"]);
    });

    it("应抛出错误当标题为空时", () => {
        expect(() => parseTask("添加任务：")).toThrow("无法解析任务标题");
    });
});

describe("buildEmailSubject", () => {
    it("应构造纯标题主题", () => {
        const subject = buildEmailSubject({ title: "买牛奶" });
        expect(subject).toBe("买牛奶");
    });

    it("应包含列表信息", () => {
        const subject = buildEmailSubject({ title: "买牛奶", list: "购物" });
        expect(subject).toBe("买牛奶 list(购物)");
    });

    it("应包含标签信息", () => {
        const subject = buildEmailSubject({ title: "买牛奶", tags: ["家务", "购物"] });
        expect(subject).toBe("买牛奶 tag(家务, 购物)");
    });

    it("应同时包含列表和标签", () => {
        const subject = buildEmailSubject({
            title: "完成报告",
            list: "工作",
            tags: ["紧急", "财务"],
        });
        expect(subject).toBe("完成报告 list(工作) tag(紧急, 财务)");
    });
});

describe("buildEmailBody", () => {
    it("应包含创建时间和来源", () => {
        const body = buildEmailBody({ title: "测试任务" });
        expect(body).toContain("创建时间：");
        expect(body).toContain("来源：Moltbot 2Do Task Email Skill");
    });

    it("应包含原始输入", () => {
        const body = buildEmailBody({ title: "买牛奶" }, "添加任务：买牛奶");
        expect(body).toContain("任务详情：添加任务：买牛奶");
    });
});
