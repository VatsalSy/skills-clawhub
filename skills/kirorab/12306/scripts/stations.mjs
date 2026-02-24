#!/usr/bin/env node
// Fetch and cache 12306 station data
import { writeFileSync, readFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CACHE_FILE = join(__dirname, '..', 'data', 'stations.json');

// Additional stations sometimes missing from 12306
const MISSING_STATIONS = {
  "XGN": { station_name: "香港西九龙", city: "香港" },
};

export async function loadStations(forceRefresh = false) {
  // Try cache first
  if (!forceRefresh && existsSync(CACHE_FILE)) {
    const cached = JSON.parse(readFileSync(CACHE_FILE, 'utf-8'));
    if (Date.now() - cached.ts < 7 * 24 * 3600 * 1000) return cached.data;
  }

  console.error('Fetching station data from 12306...');
  // Get the station_name.js URL from 12306 homepage
  const homeRes = await fetch('https://www.12306.cn/index/', {
    headers: { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)' }
  });
  const homeHtml = await homeRes.text();
  const jsMatch = homeHtml.match(/station_name\.js\?station_version=([\d.]+)/);
  const jsUrl = jsMatch
    ? `https://www.12306.cn/index/script/station_name.js?station_version=${jsMatch[1]}`
    : 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js';

  const jsRes = await fetch(jsUrl, {
    headers: { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)' }
  });
  const jsText = await jsRes.text();

  // Parse: @bjb|北京北|VAP|beijingbei|bjb|0
  const raw = jsText.match(/'([^']+)'/)?.[1] || '';
  const entries = raw.split('@').filter(Boolean);

  const STATIONS = {};       // code -> info
  const CITY_STATIONS = {};  // city -> [{code, name}]
  const NAME_STATIONS = {};  // name -> {code, name}
  const CITY_CODES = {};     // city -> {code, name} (city-named station)

  for (const entry of entries) {
    const parts = entry.split('|');
    if (parts.length < 5) continue;
    const [short, name, code, pinyin, shortPy, idx] = parts;
    // Guess city from name (remove suffixes)
    const city = name.replace(/(东|西|南|北|站|机场|西九龙)$/, '') || name;

    const info = { station_name: name, station_code: code, station_pinyin: pinyin, station_short: shortPy, city };
    STATIONS[code] = info;
    NAME_STATIONS[name] = { station_code: code, station_name: name };

    if (!CITY_STATIONS[city]) CITY_STATIONS[city] = [];
    CITY_STATIONS[city].push({ station_code: code, station_name: name });

    if (name === city) {
      CITY_CODES[city] = { station_code: code, station_name: name };
    }
  }

  // Add missing stations
  for (const [code, info] of Object.entries(MISSING_STATIONS)) {
    if (!STATIONS[code]) {
      STATIONS[code] = { station_name: info.station_name, station_code: code, city: info.city };
      NAME_STATIONS[info.station_name] = { station_code: code, station_name: info.station_name };
      const city = info.city;
      if (!CITY_STATIONS[city]) CITY_STATIONS[city] = [];
      CITY_STATIONS[city].push({ station_code: code, station_name: info.station_name });
    }
  }

  const data = { STATIONS, CITY_STATIONS, NAME_STATIONS, CITY_CODES };

  // Cache
  const { mkdirSync } = await import('node:fs');
  mkdirSync(dirname(CACHE_FILE), { recursive: true });
  writeFileSync(CACHE_FILE, JSON.stringify({ ts: Date.now(), data }));
  console.error(`Cached ${Object.keys(STATIONS).length} stations`);

  return data;
}

// Resolve city/station name to station code
export function resolveStation(data, name) {
  // Exact station name match
  if (data.NAME_STATIONS[name]) return data.NAME_STATIONS[name];
  // City code match
  if (data.CITY_CODES[name]) return data.CITY_CODES[name];
  // Fuzzy: first station in city
  if (data.CITY_STATIONS[name]) return data.CITY_STATIONS[name][0];
  // Try removing common suffixes
  const trimmed = name.replace(/(市|站)$/, '');
  if (data.CITY_CODES[trimmed]) return data.CITY_CODES[trimmed];
  if (data.CITY_STATIONS[trimmed]) return data.CITY_STATIONS[trimmed][0];
  return null;
}

// CLI: node stations.mjs [stationName]
if (process.argv[1] && process.argv[1].includes('stations.mjs') && process.argv[2]) {
  const data = await loadStations();
  const name = process.argv[2];
  const result = resolveStation(data, name);
  if (result) {
    console.log(JSON.stringify(result));
    // Also show all stations in city
    const city = data.STATIONS[result.station_code]?.city || name;
    if (data.CITY_STATIONS[city]) {
      console.log(`\nAll stations in ${city}:`);
      for (const s of data.CITY_STATIONS[city]) console.log(`  ${s.station_name} (${s.station_code})`);
    }
  } else {
    console.error(`Station not found: ${name}`);
    process.exit(1);
  }
}
