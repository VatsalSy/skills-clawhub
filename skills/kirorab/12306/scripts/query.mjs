#!/usr/bin/env node
// Query 12306 train tickets: schedule, remaining tickets, prices
import { loadStations, resolveStation } from './stations.mjs';
import { parseArgs } from 'node:util';

const { values, positionals } = parseArgs({
  options: {
    date: { type: 'string', short: 'd' },
    type: { type: 'string', short: 't', default: '' }, // G/D/Z/T/K or combo
    json: { type: 'boolean', default: false },
  },
  allowPositionals: true,
  strict: false,
});

const [fromName, toName] = positionals;
if (!fromName || !toName) {
  console.error('Usage: query.mjs <from> <to> [-d YYYY-MM-DD] [-t G|D|Z|T|K]');
  console.error('Example: query.mjs 揭阳 杭州 -d 2026-02-24 -t G');
  process.exit(1);
}

// Default to today (Shanghai timezone)
const date = values.date || new Date().toLocaleDateString('sv-SE', { timeZone: 'Asia/Shanghai' });
const trainTypeFilter = (values.type || '').toUpperCase();

// Load stations
const stationData = await loadStations();
const fromStation = resolveStation(stationData, fromName);
const toStation = resolveStation(stationData, toName);

if (!fromStation) { console.error(`Station not found: ${fromName}`); process.exit(1); }
if (!toStation) { console.error(`Station not found: ${toName}`); process.exit(1); }

console.error(`Querying: ${fromStation.station_name}(${fromStation.station_code}) → ${toStation.station_name}(${toStation.station_code}) on ${date}`);

// Get cookie first
async function getCookie() {
  const res = await fetch('https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc', {
    headers: { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36' },
    redirect: 'manual',
  });
  const cookies = res.headers.getSetCookie?.() || [];
  return cookies.map(c => c.split(';')[0]).join('; ');
}

// Query tickets
async function queryTickets() {
  const cookie = await getCookie();
  const url = `https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=${date}&leftTicketDTO.from_station=${fromStation.station_code}&leftTicketDTO.to_station=${toStation.station_code}&purpose_codes=ADULT`;

  const res = await fetch(url, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
      'Cookie': cookie,
      'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc',
    },
  });

  const json = await res.json();
  if (!json.data?.result) {
    console.error('No data returned. Response:', JSON.stringify(json).slice(0, 500));
    process.exit(1);
  }
  return json.data;
}

// Parse ticket data
// Fields: https://blog.csdn.net/a460550542/article/details/86302597
function parseTicket(raw, stationMap) {
  const f = raw.split('|');
  return {
    trainNo: f[2],           // 车次编号
    trainCode: f[3],         // 车次代号 G902
    fromCode: f[6],          // 出发站代码
    toCode: f[7],            // 到达站代码
    fromStation: stationMap[f[6]]?.station_name || f[6],
    toStation: stationMap[f[7]]?.station_name || f[7],
    departTime: f[8],        // 出发时间
    arriveTime: f[9],        // 到达时间
    duration: f[10],         // 历时
    canBuy: f[11],           // 能否购买 Y/N
    date: f[13],             // 日期
    // Seat availability
    swz: f[32] || '--',      // 商务座/特等座
    tz: f[25] || '--',       // 特等座
    zy: f[31] || '--',       // 一等座
    ze: f[30] || '--',       // 二等座
    gr: f[21] || '--',       // 高级软卧
    rw: f[23] || '--',       // 软卧/一等卧
    dw: f[33] || '--',       // 动卧
    yw: f[28] || '--',       // 硬卧/二等卧
    rz: f[24] || '--',       // 软座
    yz: f[29] || '--',       // 硬座
    wz: f[26] || '--',       // 无座
  };
}

function formatSeat(name, val) {
  if (!val || val === '--' || val === '' || val === '无') return null;
  return `${name}:${val}`;
}

const data = await queryTickets();
const stationMap = stationData.STATIONS;
const tickets = data.result.map(r => parseTicket(r, stationMap));

// Filter by train type
const filtered = trainTypeFilter
  ? tickets.filter(t => trainTypeFilter.split('').some(f => t.trainCode.startsWith(f)))
  : tickets;

if (values.json) {
  console.log(JSON.stringify(filtered, null, 2));
} else {
  if (filtered.length === 0) {
    console.log(`No trains found for ${fromStation.station_name} → ${toStation.station_name} on ${date}`);
    process.exit(0);
  }

  console.log(`\n${fromStation.station_name} → ${toStation.station_name} | ${date} | ${filtered.length} trains\n`);
  console.log('| 车次 | 出发→到达 | 耗时 | 商务/特等 | 一等座 | 二等座 | 软卧/动卧 | 硬卧 | 硬座 | 无座 | 可买 |');
  console.log('|------|-----------|------|-----------|--------|--------|-----------|------|------|------|------|');

  for (const t of filtered) {
    const swzDisplay = t.swz !== '--' ? t.swz : (t.tz !== '--' ? t.tz : '--');
    const rwDisplay = t.rw !== '--' ? t.rw : (t.dw !== '--' ? t.dw : '--');
    console.log(`| ${t.trainCode} | ${t.departTime}→${t.arriveTime} | ${t.duration} | ${swzDisplay} | ${t.zy} | ${t.ze} | ${rwDisplay} | ${t.yw} | ${t.yz} | ${t.wz} | ${t.canBuy === 'Y' ? '✅' : '❌'} |`);
  }
}
