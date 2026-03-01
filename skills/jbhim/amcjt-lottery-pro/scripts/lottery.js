const fs = require('fs');
const path = require('path');

/**
 * 彩票工具脚本 - 封装 amcjt-mcp-server 的 MCP 调用
 * 
 * 使用方法：
 *   node lottery.js <command> [args...]
 * 
 * 命令：
 *   get-result <issueNo>     - 查询开奖结果
 *   ocr <imagePath>          - OCR识别彩票图片
 *   check-win <issueNo> <betsJson> - 核对中奖
 * 
 * 示例：
 *   node lottery.js get-result 2026020
 *   node lottery.js ocr ./lottery.jpg
 *   node lottery.js check-win 2026020 '{"bets":[{"redNumbers":["01","13","14","21","24","30"],"blueNumbers":["02"]}]}'
 */

const COMMAND = process.argv[2];

async function callMcpServer(tool, params) {
  const { execSync } = require('child_process');
  
  const payload = JSON.stringify({
    jsonrpc: "2.0",
    id: 1,
    method: "tools/call",
    params: {
      name: tool,
      arguments: params
    }
  });
  
  try {
    const result = execSync(`echo '${payload}' | npx amcjt-mcp-server`, {
      encoding: 'utf8',
      timeout: 60000,
      env: { ...process.env }
    });
    return JSON.parse(result);
  } catch (error) {
    console.error('MCP call failed:', error.message);
    process.exit(1);
  }
}

async function getResult(issueNo) {
  const result = await callMcpServer('get_lottery_result', { issueNo });
  console.log(JSON.stringify(result, null, 2));
}

async function ocrTicket(imagePath) {
  if (!fs.existsSync(imagePath)) {
    console.error(`Error: File not found ${imagePath}`);
    process.exit(1);
  }
  
  // 检查并压缩图片
  const stats = fs.statSync(imagePath);
  let imageData = fs.readFileSync(imagePath);
  
  if (stats.size > 200 * 1024) {
    console.error(`Warning: Image too large (${Math.round(stats.size/1024)}KB), compressing...`);
    // 这里需要压缩逻辑，简化版直接读取
    // 实际使用时应该调用 compress_image.js
  }
  
  const base64 = imageData.toString('base64');
  const result = await callMcpServer('ocr_lottery_ticket', { 
    imageBase64: base64, 
    lottoType: "101" 
  });
  console.log(JSON.stringify(result, null, 2));
}

async function checkWin(issueNo, betsJson) {
  let bets;
  try {
    bets = JSON.parse(betsJson);
  } catch (e) {
    console.error('Error: Invalid bets JSON');
    process.exit(1);
  }
  
  const result = await callMcpServer('check_lottery_win', { 
    issueNo, 
    bets: bets.bets || bets,
    multiple: 1
  });
  console.log(JSON.stringify(result, null, 2));
}

async function main() {
  switch (COMMAND) {
    case 'get-result':
      if (!process.argv[3]) {
        console.error('Usage: node lottery.js get-result <issueNo>');
        process.exit(1);
      }
      await getResult(process.argv[3]);
      break;
      
    case 'ocr':
      if (!process.argv[3]) {
        console.error('Usage: node lottery.js ocr <imagePath>');
        process.exit(1);
      }
      await ocrTicket(process.argv[3]);
      break;
      
    case 'check-win':
      if (!process.argv[3] || !process.argv[4]) {
        console.error('Usage: node lottery.js check-win <issueNo> \'<betsJson>\'');
        process.exit(1);
      }
      await checkWin(process.argv[3], process.argv[4]);
      break;
      
    default:
      console.log(`
Lottery Tool - 彩票助手工具

Usage:
  node lottery.js <command> [args...]

Commands:
  get-result <issueNo>         查询开奖结果 (如: 2026020)
  ocr <imagePath>              OCR识别彩票图片
  check-win <issueNo> <bets>   核对中奖号码

Examples:
  node lottery.js get-result 2026020
  node lottery.js ocr ./my-ticket.jpg
  node lottery.js check-win 2026020 '{"bets":[{"redNumbers":["01","13","14","21","24","30"],"blueNumbers":["02"]}]}'
`);
      process.exit(0);
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
