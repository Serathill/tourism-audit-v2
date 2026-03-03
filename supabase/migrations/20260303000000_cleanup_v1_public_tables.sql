-- ═══════════════════════════════════════════════════════════════════════════
-- Tourism Audit V2 — V1 Cleanup Migration
-- Copies real V1 client data to V2 schema, then drops V1 tables from public
--
-- KEEPS: public.blocked_emails (1,097 domains — shared reference)
-- DROPS: properties, audit_results, audit_logs, report_subscribers, audit_cold_emails
-- ═══════════════════════════════════════════════════════════════════════════

BEGIN;

-- ───────────────────────────────────────────────────────
-- 1. Copy 7 real V1 properties → tourism_audit_v2.properties
--    Status set to 0 (failed) so they can receive a fresh V2 audit
--    Only columns that exist in V2 schema are mapped
-- ───────────────────────────────────────────────────────

INSERT INTO tourism_audit_v2.properties (
  id, owner_name, owner_email, phone_number, property_name, property_address,
  website_url, booking_platform_links, social_media_links, google_my_business_link,
  primary_marketing_goal, business_description, status, status_text,
  inserted_at, last_status_update_at
)
SELECT
  gen_random_uuid(),  -- new UUID (avoid V1 ID collision)
  p.owner_name,
  p.owner_email,
  p.phone_number,
  p.property_name,
  p.property_address,
  p.website_url,
  COALESCE(p.booking_platform_links, '[]'::jsonb),
  COALESCE(p.social_media_links, '[]'::jsonb),
  p.google_my_business_link,
  p.primary_marketing_goal,
  p.business_description,
  0,                          -- status = failed (eligible for V2 re-audit)
  'migrated_from_v1',         -- mark origin
  p.inserted_at,
  now()
FROM public.properties p
WHERE p.id IN (
  '514d6031-4c3a-4c0a-a24d-59c82f6e72bc',  -- Pensiunea Rozeclas
  'de15bb7f-f429-4e4a-8d41-d8662769d332',  -- Amont Chalet
  '23bbc7bf-7fcf-4c16-8d4c-54f55ab74694',  -- Pensiunea Casa Stan
  '6bcfea65-58e7-4b24-b66d-c9ece264eb14',  -- Resort Hanul Pescarilor Crișan
  'db0f87ae-442a-42b8-bdf9-a34f8da2c99d',  -- Casa Ria
  '6dc29993-1fa5-41f9-85b1-c3d15707c1b3',  -- LINIȘTEA PĂDURII NĂMAEȘTI
  '48110d67-c8a7-45da-973e-df669b00aa13'   -- Cabana La Nuc
)
AND NOT EXISTS (
  -- Skip if email already exists in V2 (prevent duplicates)
  SELECT 1 FROM tourism_audit_v2.properties v2
  WHERE v2.owner_email = p.owner_email
);


-- ───────────────────────────────────────────────────────
-- 2. DROP V1 tables from public schema (FK order)
-- ───────────────────────────────────────────────────────

DROP TABLE IF EXISTS public.audit_results CASCADE;
DROP TABLE IF EXISTS public.audit_logs CASCADE;
DROP TABLE IF EXISTS public.audit_cold_emails CASCADE;
DROP TABLE IF EXISTS public.report_subscribers CASCADE;
DROP TABLE IF EXISTS public.properties CASCADE;

-- blocked_emails STAYS in public — explicit instruction


-- ───────────────────────────────────────────────────────
-- 3. Cleanup orphaned cazare_audit schema (if exists)
--    Migration 09 was never applied, but schema might exist
-- ───────────────────────────────────────────────────────

DROP SCHEMA IF EXISTS cazare_audit CASCADE;


COMMIT;

-- ═══════════════════════════════════════════════════════════════════════════
-- 4. VERIFICATION (run after migration)
-- ═══════════════════════════════════════════════════════════════════════════
--
-- SELECT count(*) AS v2_properties FROM tourism_audit_v2.properties;
-- Expected: 10 (3 existing + 7 migrated)
--
-- SELECT schemaname, tablename FROM pg_tables
-- WHERE schemaname = 'public'
--   AND tablename NOT LIKE 'pg_%'
-- ORDER BY tablename;
-- Expected: only blocked_emails (+ any Supabase system tables)
--
-- SELECT count(*) AS blocked_domains FROM public.blocked_emails;
-- Expected: 1097
--
-- SELECT owner_name, owner_email, property_name, status_text
-- FROM tourism_audit_v2.properties
-- WHERE status_text = 'migrated_from_v1';
-- Expected: 7 rows
