const WebSocket = require('ws');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');

class DebateClient {
    constructor(wsUrl, botName, debateId = null) {
        this.botName = botName;
        this.botUuid = uuidv4();
        this.wsUrl = this.convertToWebSocketUrl(wsUrl);
        this.debateId = debateId;
        this.debateKey = null;
        this.botIdentifier = null;
        this.ws = null;
        this.minContentLength = 50;
        this.maxContentLength = 2000;

        this.openclawBase = (process.env.OPENCLAW_BASE || 'http://127.0.0.1:18789').replace(/\/$/, '');
        this.openclawToken = process.env.OPENCLAW_TOKEN || '';
        this.openclawModel = process.env.OPENCLAW_MODEL || 'gpt-5.3-codex';
        this.apiTimeoutMs = 60000;
        this.saveRoundLogs = (process.env.SAVE_ROUND_LOGS || 'false').toLowerCase() === 'true';

        if (this.saveRoundLogs && !fs.existsSync('logs')) fs.mkdirSync('logs');
    }

    convertToWebSocketUrl(url) {
        let wsUrl;
        if (url.startsWith('ws://') || url.startsWith('wss://')) return url;
        if (url.startsWith('https://')) wsUrl = url.replace('https://', 'wss://');
        else if (url.startsWith('http://')) wsUrl = url.replace('http://', 'ws://');
        else wsUrl = 'ws://' + url;
        if (!wsUrl.includes('/debate')) wsUrl = wsUrl.replace(/\/$/, '') + '/debate';
        return wsUrl;
    }

    log(msg) {
        console.log(`[${new Date().toISOString()}] [${this.botName}] ${msg}`);
    }

    send(type, data) {
        const payload = JSON.stringify({
            type,
            timestamp: new Date().toISOString(),
            data
        });
        this.ws.send(payload);
    }

    async postJson(url, body) {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), this.apiTimeoutMs);
        const headers = { 'Content-Type': 'application/json' };
        if (this.openclawToken) headers.Authorization = `Bearer ${this.openclawToken}`;

        try {
            const resp = await fetch(url, {
                method: 'POST',
                headers,
                body: JSON.stringify(body),
                signal: controller.signal
            });
            const text = await resp.text();
            let json = null;
            try {
                json = text ? JSON.parse(text) : null;
            } catch (_) {
                json = { raw: text };
            }
            if (!resp.ok) {
                const detail = json && (json.error?.message || json.message || json.raw || text);
                throw new Error(`HTTP ${resp.status}${detail ? `: ${detail}` : ''}`);
            }
            return json;
        } finally {
            clearTimeout(timer);
        }
    }

    extractTextFromResponsesResponse(json) {
        if (!json) return '';
        if (typeof json.output_text === 'string' && json.output_text.trim()) return json.output_text.trim();

        if (Array.isArray(json.output)) {
            const parts = [];
            for (const item of json.output) {
                if (Array.isArray(item?.content)) {
                    for (const c of item.content) {
                        if (typeof c?.text === 'string') parts.push(c.text);
                        else if (typeof c?.output_text === 'string') parts.push(c.output_text);
                    }
                }
                if (typeof item?.text === 'string') parts.push(item.text);
            }
            const joined = parts.join('\n').trim();
            if (joined) return joined;
        }

        if (typeof json?.response?.output_text === 'string' && json.response.output_text.trim()) {
            return json.response.output_text.trim();
        }

        return '';
    }

    extractTextFromChatResponse(json) {
        const msg = json?.choices?.[0]?.message;
        if (!msg) return '';

        if (typeof msg.content === 'string') return msg.content.trim();
        if (Array.isArray(msg.content)) {
            const text = msg.content
                .map((x) => (typeof x === 'string' ? x : x?.text || ''))
                .join('\n')
                .trim();
            return text;
        }
        return '';
    }

    normalizeReplyContent(content) {
        if (!content) return '';
        let finalContent = content.trim();
        if (finalContent.length > this.maxContentLength) {
            finalContent = finalContent.substring(0, this.maxContentLength);
            this.log(`WARNING: Content too long. Truncated to ${this.maxContentLength} chars.`);
        }
        if (finalContent.length < this.minContentLength) {
            this.log(`WARNING: Content too short (${finalContent.length}/${this.minContentLength} chars). Submitting anyway.`);
        }
        return finalContent;
    }

    async generateReplyViaOpenClaw(prompt) {
        const responsesUrl = `${this.openclawBase}/v1/responses`;
        const chatUrl = `${this.openclawBase}/v1/chat/completions`;

        try {
            const respJson = await this.postJson(responsesUrl, {
                model: this.openclawModel,
                input: prompt
            });
            const text = this.extractTextFromResponsesResponse(respJson);
            if (text) {
                this.log('Generated reply via /v1/responses.');
                return text;
            }
            throw new Error('empty text from /v1/responses');
        } catch (err) {
            this.log(`OpenClaw /v1/responses failed: ${err.message}. Falling back to /v1/chat/completions.`);
        }

        const chatJson = await this.postJson(chatUrl, {
            model: this.openclawModel,
            messages: [{ role: 'user', content: prompt }]
        });
        const chatText = this.extractTextFromChatResponse(chatJson);
        if (!chatText) throw new Error('empty text from /v1/chat/completions');
        this.log('Generated reply via /v1/chat/completions.');
        return chatText;
    }

    getRoundNumber(msgData) {
        if (Array.isArray(msgData?.debate_log)) return msgData.debate_log.length + 1;
        return 1;
    }

    writeRoundLog(kind, round, content) {
        if (!this.saveRoundLogs) return;
        const identifier = this.botIdentifier || this.botName;
        const fileName = `${identifier}.${kind}.round_${round}.log`;
        const filePath = `logs/${fileName}`;
        const stamp = new Date().toISOString();
        const body = `[${stamp}]\n${content}\n`;
        fs.writeFileSync(filePath, body, 'utf8');
        this.log(`Saved ${kind} log: ${filePath}`);
    }

    submitSpeech(content, round) {
        this.send('debate_speech', {
            debate_id: this.debateId,
            debate_key: this.debateKey,
            speaker: this.botIdentifier,
            message: { format: 'markdown', content }
        });
        this.log(`Speech submitted (${content.length} chars, round ${round}).`);
    }

    async handleTurn(msgData) {
        this.log('My turn to speak.');
        const round = this.getRoundNumber(msgData);

        if (msgData.min_content_length !== undefined) this.minContentLength = msgData.min_content_length;
        if (msgData.max_content_length !== undefined) this.maxContentLength = msgData.max_content_length;

        let history = '';
        if (msgData.debate_log) {
            msgData.debate_log.forEach((entry) => {
                const side = entry.side === 'supporting' ? '正方' : '反方';
                history += `\n${side} (${entry.speaker}): ${entry.message.content}\n`;
            });
        }

        const prompt = `
你现在作为辩论机器人参加一场正式辩论。
辩题: ${msgData.topic}
你的立场: ${msgData.your_side === 'supporting' ? '正方 (支持)' : '反方 (反对)'}

历史记录:
${history || '辩论刚刚开始，请进行开场陈述。'}

要求:
1. 使用 Markdown 格式。
2. 长度要求: 最少 ${this.minContentLength} 字符，最多 ${this.maxContentLength} 字符。
3. 直接输出辩论内容。
`;
        this.writeRoundLog('prompt', round, prompt);

        try {
            const apiReply = await this.generateReplyViaOpenClaw(prompt);
            const finalApiReply = this.normalizeReplyContent(apiReply);
            if (!finalApiReply) throw new Error('empty normalized reply');

            this.writeRoundLog('reply', round, finalApiReply);
            this.submitSpeech(finalApiReply, round);
        } catch (err) {
            this.log(`OpenClaw API generation failed: ${err.message}`);
        }
    }

    run() {
        this.ws = new WebSocket(this.wsUrl);

        this.ws.on('open', () => {
            if (this.debateId) {
                this.log('Connected. Logging in...');
                this.send('bot_login', {
                    bot_name: this.botName,
                    bot_uuid: this.botUuid,
                    debate_id: this.debateId,
                    version: '2.0'
                });
            } else {
                this.log('Connected. Requesting debate assignment...');
                this.send('bot_login', {
                    bot_name: this.botName,
                    bot_uuid: this.botUuid,
                    version: '2.0'
                });
            }
        });

        this.ws.on('message', (data) => {
            const msg = JSON.parse(data);
            const { type, data: msgData } = msg;

            switch (type) {
                case 'login_confirmed':
                    this.debateKey = msgData.debate_key;
                    this.botIdentifier = msgData.bot_identifier;
                    if (msgData.debate_id && !this.debateId) {
                        this.debateId = msgData.debate_id;
                        this.log(`Assigned to debate: ${this.debateId}`);
                    }
                    this.log(`Login confirmed as ${this.botIdentifier}`);
                    this.log(`Topic: ${msgData.topic}`);
                    if (msgData.joined_bots && msgData.joined_bots.length > 0) {
                        this.log(`Already joined bots: ${msgData.joined_bots.join(', ')}`);
                    } else {
                        this.log('You are the first bot to join');
                    }
                    break;
                case 'login_rejected':
                    this.log(`Login rejected: ${msgData.message}`);
                    this.log(`Reason: ${msgData.reason}`);
                    if (msgData.retry_after) this.log(`You can retry after ${msgData.retry_after} seconds`);
                    process.exit(1);
                    break;
                case 'debate_start':
                case 'debate_update':
                    if (msgData.next_speaker === this.botIdentifier) {
                        this.handleTurn(msgData).catch((err) => this.log(`handleTurn error: ${err.message}`));
                    }
                    break;
                case 'debate_end':
                    this.log(`Debate ended. Winner: ${msgData.debate_result.winner}`);
                    this.ws.close();
                    break;
                case 'ping':
                    this.send('pong', { client_time: new Date().toISOString() });
                    break;
                case 'error':
                    this.log(`Error: ${msgData.message}`);
                    break;
                default:
                    this.log(`Unknown message type: ${type}`);
            }
        });

        this.ws.on('error', (error) => {
            this.log(`WebSocket error: ${error.message}`);
        });

        this.ws.on('close', (code, reason) => {
            this.log(`Connection closed (code: ${code}, reason: ${reason || 'no reason'})`);
            process.exit(0);
        });
    }
}

const [,, url, botName, debateId] = process.argv;

if (!url || !botName) {
    console.log('Usage: node debate_client.js <url> <botName> [debateId]');
    console.log('');
    console.log('Arguments:');
    console.log('  url       - WebSocket URL (ws://host:port/debate)');
    console.log('              or HTTP URL (http://host:port) - will auto-convert to ws://host:port/debate');
    console.log('              or HTTPS URL (https://host:port) - will auto-convert to wss://host:port/debate');
    console.log('  botName   - Name for this bot (e.g., bot_alpha)');
    console.log('  debateId  - (Optional) Debate ID to join. If omitted, platform will assign one.');
    console.log('');
    console.log('Environment overrides:');
    console.log('  OPENCLAW_BASE   - OpenClaw API base (default: http://127.0.0.1:18789)');
    console.log('  OPENCLAW_TOKEN  - Bearer token for OpenClaw API (optional)');
    console.log('  OPENCLAW_MODEL  - Model for generation (default: gpt-5.3-codex)');
    console.log('  SAVE_ROUND_LOGS - Persist prompt/reply logs to logs/ (default: false)');
    process.exit(1);
}

new DebateClient(url, botName, debateId).run();
