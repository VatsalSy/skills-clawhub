#!/usr/bin/env node

/**
 * Daily Briefing 脚本 1: 获取数据
 * - 拉取 mixdao API
 * - 解析并扁平化（仅保留含正文的条目）
 * - 临时保存为 JSON 文件
 * - 输出临时文件路径及所有条目的 id、标题供挑选
 *
 * 用法: node scripts/01-fetch.js
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import https from 'https';

const __dirname = path.dirname(fileURLToPath(
    import.meta.url));
const API_URL = 'https://www.mixdao.world/api/latest';
const SKIP_KEYS = new Set(['sources', 'sourceLabels']);

function fetchRaw() {
    return new Promise((resolve, reject) => {
        const apiKey = process.env.MIXDAO_API_KEY;
        if (!apiKey) {
            reject(new Error('MIXDAO_API_KEY is not set.'));
            return;
        }
        const url = new URL(API_URL);
        const opts = {
            hostname: url.hostname,
            path: url.pathname + url.search,
            method: 'GET',
            headers: { Authorization: `Bearer ${apiKey}` },
        };
        const req = https.request(opts, (res) => {
            res.setTimeout(15000, () => {
                req.destroy();
                reject(new Error('API 请求超时'));
            });
            const chunks = [];
            res.on('data', (c) => chunks.push(c));
            res.on('end', () => {
                const body = Buffer.concat(chunks).toString('utf8');
                if (res.statusCode !== 200) {
                    reject(new Error(`API returned ${res.statusCode}: ${body.slice(0, 200)}`));
                    return;
                }
                try {
                    resolve(JSON.parse(body));
                } catch (e) {
                    reject(new Error('Invalid JSON from API: ' + e.message));
                }
            });
        });
        req.on('error', reject);
        req.end();
    });
}

function flatten(data) {
    const out = [];
    for (const key of Object.keys(data)) {
        if (SKIP_KEYS.has(key)) continue;
        const arr = Array.isArray(data[key]) ? data[key] : [];
        if (!arr.length) continue;
        for (const item of arr) {
            if (!item || (!item.title && !item.translatedTitle)) continue;
            const title = item.title || item.translatedTitle || '';
            const translatedTitle = item.translatedTitle || item.title || '';
            const url = item.url || item.link || '';
            if (!url && !title) continue;
            if (item.text && item.text.trim()) out.push({
                id: item.id || `${key}-${item.url || title}`.slice(0, 80),
                title: title.replace(/&#8217;/g, "'"),
                translatedTitle: (translatedTitle || '').replace(/&#8217;/g, "'"),
                text: item.text.trim(),
                url,
                score: typeof item.score === 'number' ? item.score : 0,
                descendants: typeof item.descendants === 'number' ? item.descendants : 0,
                source: key,
            });
        }
    }
    return out;
}

function main() {
    fetchRaw()
        .then((raw) => {
            const items = flatten(raw);
            if (!items.length) {
                console.error('01-fetch.js: no items from API');
                process.exit(1);
            }

            const timestamp = new Date().toISOString().slice(0, 10);
            const tempFileName = `briefing-${timestamp}.json`;
            const tempFilePath = path.join(__dirname, '..', 'temp', tempFileName);

            const tempDir = path.join(__dirname, '..', 'temp');
            if (!fs.existsSync(tempDir)) {
                fs.mkdirSync(tempDir, { recursive: true });
            }

            const outputData = {
                generatedAt: new Date().toISOString(),
                allItems: items,
            };

            fs.writeFileSync(tempFilePath, JSON.stringify(outputData, null, 2), 'utf8');

            console.log(`[FILE PATH] ${tempFilePath}`);
            console.log('[CANDIDATES]');

            for (const item of items) {
                const title = item.translatedTitle || item.title || '';
                console.log(`ID: ${item.id}`);
                console.log(`标题: ${title}`);
                console.log('-----');
            }
        })
        .catch((err) => {
            console.error('Error:', err.message);
            process.exit(1);
        });
}

main();