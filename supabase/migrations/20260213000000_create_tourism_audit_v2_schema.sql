-- ═══════════════════════════════════════════════════════════════════════════
-- Tourism Audit V2 — Schema Migration (Story 0.1)
-- Creates tourism_audit_v2 schema with all tables, RLS, indexes, and seed data
--
-- Prerequisites:
--   1. Run this migration in the Supabase SQL Editor
--   2. After running, add "tourism_audit_v2" to API Settings → Exposed Schemas
--
-- Tables created:
--   - properties          (form submissions + status workflow)
--   - audit_results       (AI-generated audit output)
--   - audit_logs          (pipeline event logging)
--   - report_subscribers  (internal BCC list)
--   - blocked_emails      (spam domain blocklist)
--   - audit_cold_emails   (outreach tracking, post-MVP)
-- ═══════════════════════════════════════════════════════════════════════════

-- ───────────────────────────────────────────────────────
-- 1. CREATE SCHEMA
-- ───────────────────────────────────────────────────────

CREATE SCHEMA IF NOT EXISTS tourism_audit_v2;

-- Grant usage to all Supabase roles
GRANT USAGE ON SCHEMA tourism_audit_v2 TO anon;
GRANT USAGE ON SCHEMA tourism_audit_v2 TO authenticated;
GRANT USAGE ON SCHEMA tourism_audit_v2 TO service_role;

-- Grant full table/sequence access to service_role
GRANT ALL ON ALL TABLES IN SCHEMA tourism_audit_v2 TO service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA tourism_audit_v2 TO service_role;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA tourism_audit_v2
  GRANT ALL ON TABLES TO service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA tourism_audit_v2
  GRANT ALL ON SEQUENCES TO service_role;

-- Grant limited access to anon (PostgREST needs SELECT/INSERT per RLS)
ALTER DEFAULT PRIVILEGES IN SCHEMA tourism_audit_v2
  GRANT SELECT, INSERT ON TABLES TO anon;


-- ───────────────────────────────────────────────────────
-- 2. PROPERTIES TABLE (form submissions)
-- ───────────────────────────────────────────────────────
-- Status workflow: 10=pending → 1=running → 99=success | 0=failed

CREATE TABLE tourism_audit_v2.properties (
  id                     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_name             TEXT NOT NULL,
  owner_email            TEXT NOT NULL,
  phone_number           TEXT,  -- post-MVP (deferred to reduce friction)
  property_name          TEXT NOT NULL,
  property_address       TEXT NOT NULL,  -- county (judet)
  website_url            TEXT,
  booking_platform_links JSONB DEFAULT '[]'::jsonb,
  social_media_links     JSONB DEFAULT '[]'::jsonb,
  google_my_business_link TEXT,
  primary_marketing_goal TEXT,
  business_description   TEXT,
  status                 SMALLINT NOT NULL DEFAULT 10,
  status_text            TEXT,
  inserted_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
  last_status_update_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE tourism_audit_v2.properties IS 'Audit form submissions with processing status workflow';
COMMENT ON COLUMN tourism_audit_v2.properties.status IS '10=pending, 1=running, 99=success, 0=failed';
COMMENT ON COLUMN tourism_audit_v2.properties.property_address IS 'County (judet) — one of 41 judete + Bucuresti';
COMMENT ON COLUMN tourism_audit_v2.properties.phone_number IS 'Post-MVP field — deferred to reduce form friction';


-- ───────────────────────────────────────────────────────
-- 3. AUDIT_RESULTS TABLE (AI output)
-- ───────────────────────────────────────────────────────

CREATE TABLE tourism_audit_v2.audit_results (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  property_id    UUID NOT NULL REFERENCES tourism_audit_v2.properties(id) ON DELETE CASCADE,
  raw_data       TEXT,
  formatted_data TEXT,
  inserted_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE tourism_audit_v2.audit_results IS 'Raw and formatted AI-generated audit reports';


-- ───────────────────────────────────────────────────────
-- 4. AUDIT_LOGS TABLE (pipeline events)
-- ───────────────────────────────────────────────────────

CREATE TABLE tourism_audit_v2.audit_logs (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  property_id UUID REFERENCES tourism_audit_v2.properties(id) ON DELETE SET NULL,
  message     TEXT NOT NULL,
  status_text TEXT,
  inserted_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE tourism_audit_v2.audit_logs IS 'Audit pipeline processing events and status changes';
COMMENT ON COLUMN tourism_audit_v2.audit_logs.property_id IS 'Nullable — allows system-level logs not tied to a specific property';


-- ───────────────────────────────────────────────────────
-- 5. REPORT_SUBSCRIBERS TABLE (internal BCC list)
-- ───────────────────────────────────────────────────────

CREATE TABLE tourism_audit_v2.report_subscribers (
  id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email              TEXT NOT NULL UNIQUE,
  rate_limit_exempt  BOOLEAN NOT NULL DEFAULT false,
  inserted_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE tourism_audit_v2.report_subscribers IS 'Internal team members who receive BCC copies of audit emails';
COMMENT ON COLUMN tourism_audit_v2.report_subscribers.rate_limit_exempt IS 'If true, this subscriber is BCCd on every audit email';


-- ───────────────────────────────────────────────────────
-- 6. BLOCKED_EMAILS TABLE (spam domain blocklist)
-- ───────────────────────────────────────────────────────

CREATE TABLE tourism_audit_v2.blocked_emails (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email      TEXT NOT NULL UNIQUE,  -- domain only (e.g., tempmail.com)
  reason     TEXT NOT NULL DEFAULT 'manual_block',
  blocked_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  blocked_by TEXT NOT NULL DEFAULT 'system'
);

COMMENT ON TABLE tourism_audit_v2.blocked_emails IS 'Blocked email domains for spam prevention (stores domains, not full addresses)';
COMMENT ON COLUMN tourism_audit_v2.blocked_emails.email IS 'Domain to block (e.g., tempmail.com, guerrillamail.com)';
COMMENT ON COLUMN tourism_audit_v2.blocked_emails.reason IS 'manual_block | honeypot_detected | blacklisted_domain | abuse_reported';
COMMENT ON COLUMN tourism_audit_v2.blocked_emails.blocked_by IS 'system (automated) or admin email address';


-- ───────────────────────────────────────────────────────
-- 7. AUDIT_COLD_EMAILS TABLE (post-MVP outreach)
-- ───────────────────────────────────────────────────────

CREATE TABLE tourism_audit_v2.audit_cold_emails (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email_0    TEXT,
  email_1    TEXT,
  email_2    TEXT,
  subscribed BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE tourism_audit_v2.audit_cold_emails IS 'Post-MVP: Cold email outreach tracking for lead generation';


-- ═══════════════════════════════════════════════════════════════════════════
-- 8. ROW LEVEL SECURITY (RLS)
-- ═══════════════════════════════════════════════════════════════════════════
-- V1 had ZERO RLS policies. V2 enables RLS on ALL tables from day one.
--
-- Access pattern:
--   - Browser client (anon key): Only INSERT into properties (form submission)
--   - Server API routes (service_role): Full access (bypasses RLS)
--   - Backend Python (service_role): Full access (bypasses RLS)

-- Enable RLS on all tables
ALTER TABLE tourism_audit_v2.properties ENABLE ROW LEVEL SECURITY;
ALTER TABLE tourism_audit_v2.audit_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE tourism_audit_v2.audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE tourism_audit_v2.report_subscribers ENABLE ROW LEVEL SECURITY;
ALTER TABLE tourism_audit_v2.blocked_emails ENABLE ROW LEVEL SECURITY;
ALTER TABLE tourism_audit_v2.audit_cold_emails ENABLE ROW LEVEL SECURITY;

-- Properties: anon can INSERT (form submission from browser)
CREATE POLICY "anon_insert_properties"
  ON tourism_audit_v2.properties
  FOR INSERT
  TO anon
  WITH CHECK (
    -- Only allow inserting with pending status
    status = 10
    -- Prevent setting admin-only fields
    AND status_text IS NULL
  );

-- Properties: anon cannot SELECT/UPDATE/DELETE
-- (service_role bypasses RLS for all read/write operations)

-- Blocked emails: anon can SELECT (for potential client-side domain check)
CREATE POLICY "anon_select_blocked_emails"
  ON tourism_audit_v2.blocked_emails
  FOR SELECT
  TO anon
  USING (true);

-- All other tables: no anon access (service_role only)
-- No policies needed — RLS enabled with no permissive policies = deny all for anon


-- ═══════════════════════════════════════════════════════════════════════════
-- 9. INDEXES
-- ═══════════════════════════════════════════════════════════════════════════

-- Properties indexes
CREATE INDEX idx_properties_owner_email
  ON tourism_audit_v2.properties(owner_email);

CREATE INDEX idx_properties_status
  ON tourism_audit_v2.properties(status);

CREATE INDEX idx_properties_last_status_update
  ON tourism_audit_v2.properties(last_status_update_at DESC);

CREATE INDEX idx_properties_email_status
  ON tourism_audit_v2.properties(owner_email, status);

CREATE INDEX idx_properties_status_updated
  ON tourism_audit_v2.properties(status, last_status_update_at DESC);

-- Audit results index
CREATE INDEX idx_audit_results_property_id
  ON tourism_audit_v2.audit_results(property_id);

-- Audit logs indexes
CREATE INDEX idx_audit_logs_property_id
  ON tourism_audit_v2.audit_logs(property_id)
  WHERE property_id IS NOT NULL;

CREATE INDEX idx_audit_logs_inserted_at
  ON tourism_audit_v2.audit_logs(inserted_at DESC);

-- Report subscribers index
CREATE INDEX idx_report_subscribers_rate_limit
  ON tourism_audit_v2.report_subscribers(rate_limit_exempt)
  WHERE rate_limit_exempt = true;

-- Blocked emails index
CREATE INDEX idx_blocked_emails_email
  ON tourism_audit_v2.blocked_emails(email);


-- ═══════════════════════════════════════════════════════════════════════════
-- 10. SEED DATA — Copy blocked_emails from V1 (public schema)
-- ═══════════════════════════════════════════════════════════════════════════
-- V1 has ~1,097 blocked email domains in public.blocked_emails
-- This copies them to the new schema. If the source table doesn't exist,
-- this will fail gracefully — run the manual insert below instead.

INSERT INTO tourism_audit_v2.blocked_emails (email, reason, blocked_at, blocked_by)
SELECT
  email,
  COALESCE(reason, 'manual_block'),
  COALESCE(inserted_at, now()),  -- V1 uses 'inserted_at', not 'blocked_at'
  'system'                        -- V1 has no 'blocked_by' column
FROM public.blocked_emails
ON CONFLICT (email) DO NOTHING;


-- ═══════════════════════════════════════════════════════════════════════════
-- 11. VERIFICATION QUERIES (run after migration to confirm)
-- ═══════════════════════════════════════════════════════════════════════════

-- Uncomment and run these to verify:
--
-- SELECT schemaname, tablename
-- FROM pg_tables
-- WHERE schemaname = 'tourism_audit_v2'
-- ORDER BY tablename;
--
-- SELECT count(*) AS blocked_domains_copied
-- FROM tourism_audit_v2.blocked_emails;
--
-- SELECT tablename, rowsecurity
-- FROM pg_tables
-- WHERE schemaname = 'tourism_audit_v2';
