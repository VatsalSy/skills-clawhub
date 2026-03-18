/**
 * API 服务器
 * RESTful API for Cognitive Brain
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const { getBrain } = require('../index.js');
const { metrics } = require('../utils/metrics.cjs');
const { createLogger } = require('../utils/logger.cjs');
const { validateEncode, validateRecall, validateId } = require('../utils/validation.cjs');
const { WebSocketManager } = require('./websocket.js');
const { CONSTANTS } = require('../utils/constants.cjs');

// 简单的速率限制中间件
const rateLimitMap = new Map();

function rateLimitMiddleware(req, res, next) {
  const key = req.ip || 'unknown';
  const now = Date.now();

  if (!rateLimitMap.has(key)) {
    rateLimitMap.set(key, { count: 1, resetTime: now + CONSTANTS.API.RATE_LIMIT_WINDOW_MS });
    return next();
  }

  const data = rateLimitMap.get(key);

  if (now > data.resetTime) {
    // 重置窗口
    data.count = 1;
    data.resetTime = now + CONSTANTS.API.RATE_LIMIT_WINDOW_MS;
    return next();
  }

  if (data.count >= CONSTANTS.API.RATE_LIMIT_MAX_REQUESTS) {
    return res.status(429).json({
      error: 'Too many requests',
      retryAfter: Math.ceil((data.resetTime - now) / 1000)
    });
  }

  data.count++;
  next();
}

const logger = createLogger('api');

class ApiServer {
  constructor(port = CONSTANTS.API.DEFAULT_PORT) {
    this.app = express();
    this.port = port;
    this.brain = null;
    this.setupMiddleware();
    this.setupRoutes();
  }

  setupMiddleware() {
    // 安全头
    this.app.use(helmet());
    
    // CORS
    this.app.use(cors({
      origin: process.env.CORS_ORIGIN || '*',
      methods: ['GET', 'POST', 'PUT', 'DELETE'],
      allowedHeaders: ['Content-Type', 'Authorization']
    }));
    
    // 请求体限制
    this.app.use(express.json({ limit: CONSTANTS.API.REQUEST_BODY_LIMIT }));
    this.app.use(express.urlencoded({ extended: true, limit: CONSTANTS.API.REQUEST_BODY_LIMIT }));

    // 速率限制
    this.app.use(rateLimitMiddleware);

    // 请求日志和指标收集
    this.app.use((req, res, next) => {
      logger.info(`${req.method} ${req.path}`, {
        ip: req.ip,
        userAgent: req.get('user-agent')
      });

      const timer = metrics.startTimer('http_request_duration', {
        method: req.method,
        path: req.path
      });

      res.on('finish', () => {
        timer.end();
        metrics.inc('http_requests_total', {
          method: req.method,
          path: req.path,
          status: res.statusCode
        });
      });

      next();
    });
  }

  setupRoutes() {
    // 健康检查
    this.app.get('/health', async (req, res) => {
      try {
        const stats = await this.brain.stats();
        res.json({
          status: 'ok',
          version: require('../../package.json').version,
          stats
        });
      } catch (e) {
        res.status(503).json({
          status: 'error',
          message: e.message
        });
      }
    });

    // 编码记忆
    this.app.post('/api/memories', validateEncode, async (req, res) => {
      try {
        const { content, metadata = {} } = req.body;
        
        if (!content) {
          return res.status(400).json({ error: 'content is required' });
        }
        
        const timer = metrics.startTimer('encode_duration');
        const memory = await this.brain.memory.encode(content, metadata);
        timer.end();
        
        metrics.inc('memories_encoded_total');
        res.status(201).json(memory);
      } catch (e) {
        metrics.inc('encode_errors_total');
        res.status(500).json({ error: e.message });
      }
    });

    // 检索记忆
    this.app.get('/api/memories', validateRecall, async (req, res) => {
      try {
        const { q, limit = 10, type } = req.query;
        
        if (!q) {
          return res.status(400).json({ error: 'q (query) is required' });
        }
        
        const timer = metrics.startTimer('recall_duration');
        const memories = await this.brain.memory.recall(q, {
          limit: parseInt(limit),
          type
        });
        timer.end();
        
        metrics.inc('memories_recalled_total');
        res.json({
          query: q,
          count: memories.length,
          memories
        });
      } catch (e) {
        metrics.inc('recall_errors_total');
        res.status(500).json({ error: e.message });
      }
    });

    // 获取记忆详情
    this.app.get('/api/memories/:id', validateId, async (req, res) => {
      try {
        const memory = await this.brain.memory.memoryRepo.findById(req.params.id);
        if (!memory) {
          return res.status(404).json({ error: 'Memory not found' });
        }
        res.json(memory);
      } catch (e) {
        res.status(500).json({ error: e.message });
      }
    });

    // 获取统计
    this.app.get('/api/stats', async (req, res) => {
      try {
        const stats = await this.brain.stats();
        res.json(stats);
      } catch (e) {
        res.status(500).json({ error: e.message });
      }
    });

    // 获取概念
    this.app.get('/api/concepts', async (req, res) => {
      try {
        const { limit = 10 } = req.query;
        const concepts = await this.brain.concept.getTopConcepts(parseInt(limit));
        res.json(concepts);
      } catch (e) {
        res.status(500).json({ error: e.message });
      }
    });

    // 预测
    this.app.post('/api/predict', async (req, res) => {
      try {
        const { userId, messages = [] } = req.body;
        const result = await this.brain.memory.predictAndPreload(userId, messages);
        res.json(result);
      } catch (e) {
        res.status(500).json({ error: e.message });
      }
    });

    // Metrics 端点 (Prometheus 格式)
    this.app.get('/metrics', (req, res) => {
      res.set('Content-Type', 'text/plain');
      res.send(metrics.toPrometheus());
    });

    // 404
    this.app.use((req, res) => {
      res.status(404).json({ error: 'Not found' });
    });

    // 错误处理
    this.app.use((err, req, res, next) => {
      console.error('[API Error]', err);
      res.status(500).json({ error: 'Internal server error' });
    });
  }

  async start() {
    this.brain = getBrain ? getBrain() : new (require('../index.js').CognitiveBrain)();
    
    return new Promise((resolve) => {
      this.server = this.app.listen(this.port, () => {
        console.log(`🚀 API Server running on http://localhost:${this.port}`);
        console.log(`   Health: http://localhost:${this.port}/health`);
        console.log(`   Metrics: http://localhost:${this.port}/metrics`);
        console.log(`   WebSocket: ws://localhost:${this.port}`);
        resolve();
      });
      
      // 启动 WebSocket
      this.wsManager = new WebSocketManager(this.server);
    });
  }

  async stop() {
    logger.info('正在关闭服务...');

    // 关闭 WebSocket
    if (this.wsManager) {
      logger.info('关闭 WebSocket 连接...');
      await this.wsManager.close();
    }

    // 关闭 HTTP server
    if (this.server) {
      logger.info('关闭 HTTP 服务...');
      await new Promise((resolve, reject) => {
        this.server.close((err) => {
          if (err) reject(err);
          else resolve();
        });
      });
    }

    // 关闭数据库连接
    if (this.brain && this.brain.pool) {
      logger.info('关闭数据库连接池...');
      // 移除所有监听器避免泄漏
      this.brain.pool.removeAllListeners();
      await this.brain.pool.end();
    }

    // 清理 rate limit map
    rateLimitMap.clear();

    logger.info('服务已关闭');
  }
}

// 优雅关闭处理
process.on('SIGTERM', async () => {
  console.log('收到 SIGTERM 信号，开始优雅关闭...');
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('收到 SIGINT 信号，开始优雅关闭...');
  process.exit(0);
});

// CLI
if (require.main === module) {
  const port = process.env.PORT || 3000;
  const server = new ApiServer(parseInt(port));
  server.start().catch(console.error);
}

module.exports = { ApiServer };

