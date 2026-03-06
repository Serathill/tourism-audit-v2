-- Daily report cron job: calls Render backend every day at 09:00 Bucharest time.
-- Uses pg_cron + pg_net (both enabled on Supabase by default).
--
-- The backend API key must match BACKEND_API_KEY env var on Render.
-- If the key changes, update this cron job via:
--   SELECT cron.alter_job(jobid, ...) FROM cron.job WHERE jobname = 'daily-audit-report';

SELECT cron.schedule(
  'daily-audit-report',
  '0 6 * * *',  -- 06:00 UTC = 09:00 Europe/Bucharest (EET, UTC+3)
  $$
  SELECT net.http_post(
    url := 'https://api.tourism-audit.devidevs.com/api/daily-report',
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'X-API-Key', 'HVKpMqzrUPVBQ-NTCDe94Mqdl_npHZyc0eVRH8DHnHKNxZeMt190WC7oZ-BsS2Cw'
    ),
    body := '{}'::jsonb
  );
  $$
);
