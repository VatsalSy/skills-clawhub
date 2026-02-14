#!/usr/bin/env node

/**
 * Daily Briefing 脚本 2: 生成简报
 * - 读取临时文件（传入完整路径）
 * - 根据传入的 ids 筛选条目
 * - 输出每条目的详细信息（含摘要）供 Agent 加工
 * - 运行结束后删除该临时文件
 *
 * 用法: node scripts/02-generate.js <filepath> <id1> <id2> <id3>
 * 示例: node scripts/02-generate.js /path/to/temp/briefing-2026-02-14.json pr-xxx1 pr-xxx2 pr-xxx3
 */

import fs from 'fs';

function main() {
    const args = process.argv.slice(2);
    if (args.length < 2) {
        console.error('用法: node 02-generate.js <filepath> <id1> [id2] [id3] ...');
        console.error('示例: node 02-generate.js /path/to/temp/briefing-2026-02-14.json pr-xxx1 pr-xxx2 pr-xxx3');
        process.exit(1);
    }

    const filepath = args[0];
    const selectedIds = args.slice(1);

    if (!fs.existsSync(filepath)) {
        console.error(`错误: 找不到文件 ${filepath}`);
        process.exit(1);
    }

    let data;
    try {
        const raw = fs.readFileSync(filepath, 'utf8');
        data = JSON.parse(raw);
    } catch (err) {
        console.error(`错误: 无法读取或解析文件 ${filepath}`, err.message);
        process.exit(1);
    }
    if (!data || !Array.isArray(data.allItems)) {
        console.error('错误: 文件格式无效，缺少 allItems 数组');
        process.exit(1);
    }

    // 根据 id 筛选条目
    const selectedItems = [];
    for (const id of selectedIds) {
        let found = null;
        // 从 allItems 中查找
        for (const item of data.allItems) {
            if (item.id === id) {
                found = item;
                break;
            }
        }
        if (found) {
            selectedItems.push(found);
        } else {
            console.warn(`警告: 找不到 id=${id} 的条目`);
        }
    }

    if (selectedItems.length === 0) {
        console.error('错误: 没有找到匹配的条目');
        process.exit(1);
    }

    console.log('[CONTEXT]');
    console.log(`生成时间: ${data.generatedAt}`);
    console.log(`条目数: ${selectedItems.length}`);

    for (let i = 0; i < selectedItems.length; i++) {
        const item = selectedItems[i];
        const text = item.text ? item.text.trim() : '';
        console.log(`\n--- 条目 ${i + 1} ---`);
        console.log(`ID: ${item.id}`);
        console.log(`标题: ${item.translatedTitle||item.title}`);
        if (text) console.log(`摘要: ${text.length > 200 ? text.slice(0, 200) + '...' : text}`);
        console.log(`URL: ${item.url}`);
    }

    // 删除临时文件
    try {
        fs.unlinkSync(filepath);
    } catch (err) {
        console.warn(`警告: 删除临时文件失败 ${filepath}:`, err.message);
    }
}

main();