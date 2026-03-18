#!/usr/bin/env node
/**
 * 数据库重构脚本 v4.0.0
 * 1. 添加 role 字段区分 user/assistant
 * 2. 删除无用字段
 * 3. 清理历史数据标记
 */

const { getPool } = require('../core/db.cjs');

async function migrate() {
  const pool = getPool();
  console.log('=== 数据库重构 v4.0.0 ===\n');
  
  // 1. 添加 role 字段
  console.log('1. 添加 role 字段...');
  await pool.query(`
    ALTER TABLE episodes 
    ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'user'
  `);
  console.log('   ✅ role 字段已添加');
  
  // 2. 给现有数据打上 role=user 标记
  console.log('2. 标记现有数据...');
  await pool.query(`
    UPDATE episodes 
    SET role = 'user' 
    WHERE role IS NULL
  `);
  const updated = await pool.query(`SELECT COUNT(*) FROM episodes WHERE role = 'user'`);
  console.log(`   ✅ ${updated.rows[0].count} 条记录标记为 user`);
  
  // 3. 删除无用字段（先保留，仅标记为废弃）
  console.log('3. 检查可删除字段...');
  const columns = await pool.query(`
    SELECT column_name FROM information_schema.columns
    WHERE table_name = 'episodes' AND column_name IN (
      'source_session', 'access_count', 'last_accessed', 'tags'
    )
  `);
  console.log('   可删除字段:', columns.rows.map(r => r.column_name).join(', '));
  console.log('   ⚠️  如需删除，请手动执行 DROP COLUMN');
  
  // 4. 创建 role 索引
  console.log('4. 创建 role 索引...');
  await pool.query(`
    CREATE INDEX IF NOT EXISTS idx_episodes_role 
    ON episodes(role)
  `);
  console.log('   ✅ role 索引已创建');
  
  // 5. 更新统计
  console.log('\n5. 更新后统计:');
  const stats = await pool.query(`
    SELECT 
      role,
      source_channel,
      COUNT(*) as count
    FROM episodes
    GROUP BY role, source_channel
    ORDER BY role, count DESC
  `);
  
  console.log('  role  | channel      | count');
  console.log('  ------|--------------|------');
  stats.rows.forEach(row => {
    const ch = (row.source_channel || 'null').padEnd(12);
    console.log(`  ${row.role.padEnd(5)} | ${ch} | ${row.count}`);
  });
  
  await pool.end();
  console.log('\n✅ 重构完成');
}

migrate().catch(err => {
  console.error('❌ 重构失败:', err.message);
  process.exit(1);
});

