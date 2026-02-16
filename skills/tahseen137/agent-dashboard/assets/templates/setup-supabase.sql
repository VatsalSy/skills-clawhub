-- Mission Control Dashboard — Supabase Setup
-- Run this in your Supabase SQL Editor (Dashboard → SQL Editor → New Query)
--
-- This creates a table for storing dashboard state with:
-- - Realtime enabled for instant updates
-- - RLS policies: public read, service_role write only
--
-- Security: The anon key can only READ data (for the dashboard).
-- Only the service_role key (used by push script) can write.

-- 1. Create the dashboard_state table
CREATE TABLE IF NOT EXISTS dashboard_state (
    id TEXT PRIMARY KEY DEFAULT 'main',
    data JSONB NOT NULL DEFAULT '{}',
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Enable Row Level Security
ALTER TABLE dashboard_state ENABLE ROW LEVEL SECURITY;

-- 3. Allow anyone to read (dashboard visitors)
-- This is safe because the dashboard is PIN-protected client-side
CREATE POLICY "Allow public read access"
    ON dashboard_state
    FOR SELECT
    USING (true);

-- 4. Only service_role can insert/update/delete
-- The push script uses the service_role key
CREATE POLICY "Service role has full access"
    ON dashboard_state
    FOR ALL
    USING (auth.role() = 'service_role')
    WITH CHECK (auth.role() = 'service_role');

-- 5. Enable Realtime for instant updates
-- This allows the dashboard to receive websocket updates
ALTER PUBLICATION supabase_realtime ADD TABLE dashboard_state;

-- 6. Insert the initial row (required before first push)
INSERT INTO dashboard_state (id, data)
VALUES ('main', '{"actionRequired":[],"activeNow":[],"products":[],"crons":[],"recentActivity":[],"revenue":{"mrr":0}}')
ON CONFLICT (id) DO NOTHING;

-- Done! Your dashboard_state table is ready.
-- 
-- Next steps:
-- 1. Copy your SUPABASE_URL from Settings → API → Project URL
-- 2. Copy your SUPABASE_ANON_KEY from Settings → API → anon public
-- 3. Copy your SUPABASE_SERVICE_KEY from Settings → API → service_role (keep secret!)
-- 4. Update tier3-realtime.html with your URL and anon key
-- 5. Set SUPABASE_URL and SUPABASE_SERVICE_KEY as env vars for the push script
