const express = require('express');
const http = require('http');
const path = require('path');
const fs = require('fs');

async function startDashboard({ 
    port = 19195, 
    host = '127.0.0.1', 
    token = 'admin-token',
    inboxPath = process.env.INBOX_PATH || path.resolve(__dirname, '../data/inbox.jsonl'),
    sessionPath = process.env.SESSION_PATH || path.resolve(__dirname, '../data/session.json')
}) {
    const app = express();
    const server = http.createServer(app);

    // Auth middleware
    app.use((req, res, next) => {
        const authHeader = req.headers['authorization'];
        const bearerToken = authHeader && authHeader.startsWith('Bearer ') ? authHeader.split(' ')[1] : null;
        const queryToken = req.query.token || req.headers['x-dashboard-token'] || bearerToken;
        
        if (!token || queryToken !== token) {
            return res.status(403).send('Forbidden: Invalid dashboard token.');
        }
        next();
    });

    app.get('/', (req, res) => {
        const html = fs.readFileSync(path.resolve(__dirname, '../assets/index.html'), 'utf8');
        res.send(html);
    });

    // API: Get Emails
    app.get('/api/emails', (req, res) => {
        try {
            if (!fs.existsSync(inboxPath)) return res.json([]);
            const content = fs.readFileSync(inboxPath, 'utf8');
            const emails = content.trim().split('\n').filter(Boolean).map(line => JSON.parse(line));
            res.json(emails.reverse().slice(0, 50));
        } catch (e) {
            res.status(500).json({ error: e.message });
        }
    });

    // API: Get Session Status
    app.get('/api/session', (req, res) => {
        try {
            if (!fs.existsSync(sessionPath)) return res.json({ active: false });
            const stats = fs.statSync(sessionPath);
            res.json({ active: true, updatedAt: stats.mtime });
        } catch (e) {
            res.json({ active: false });
        }
    });

    server.listen(port, host, () => {
        console.log(`\n🏠 AI COMMANDER DASHBOARD READY`);
        console.log(`URL: http://${host === '0.0.0.0' ? 'YOUR_IP' : host}:${port}/\n`);
    });

    return server;
}

if (require.main === module) {
    const port = parseInt(process.env.PORT) || 19195;
    const host = process.env.DASHBOARD_HOST || '127.0.0.1';
    const token = process.env.DASHBOARD_TOKEN || 'test-admin';
    startDashboard({ port, host, token });
}

module.exports = { startDashboard };
