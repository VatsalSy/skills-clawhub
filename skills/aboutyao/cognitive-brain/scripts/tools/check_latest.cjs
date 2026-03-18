#!/usr/bin/env node
const { getPool } = require('../core/db.cjs');

async function check() {
  const pool = getPool();
  console.log('=== 最新记录检查 ===\n');
  
  // 按 role 统计
  const byRole = await pool.query(`
    SELECT role, COUNT(*) as count 
    FROM episodes 
    GROUP BY role
  `);
  console.log('按 role 统计:');
  byRole.rows.forEach(r => console.log('  -', r.role, ':', r.count));
  
  // 最新的5条记录
  console.log('\n最新5条记录:');
  const latest = await pool.query(`
    SELECT content, role, source_channel, created_at 
    FROM episodes 
    ORDER BY created_at DESC 
    LIMIT 5
  `);
  latest.rows.forEach((r, i) => {
    const content = (r.content || 'N/A').substring(0, 40);
    console.log(`${i+1}. [${r.role}] ${content}... (${r.source_channel})`);
  });
  
  await pool.end();
}
check().catch(console.error);

