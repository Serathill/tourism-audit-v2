# RUNBOOK - Proceduri Operationale

## 1. Audit stuck la status=1 mai mult de 3 ore

Healthz reseteaza automat audituri stuck >120 min (la fiecare ping de pg_cron, ~10 min).

Daca trebuie manual:

```sql
UPDATE tourism_audit_v2.properties
SET status = 0, status_text = 'failed_manual_reset',
    last_status_update_at = now()
WHERE status = 1
  AND last_status_update_at < now() - interval '3 hours';
```

## 2. Emailuri nu se mai livreaza

1. Verifica Resend dashboard: https://resend.com/emails
2. Verifica API key pe Render: `RESEND_API_KEY`
3. Verifica domain verification: `send.audit-turism.ro` (DKIM + SPF + MX)
4. Verifica `audit_logs` pentru erori recente:

```sql
SELECT * FROM tourism_audit_v2.audit_logs
WHERE status_text LIKE '%email%'
ORDER BY inserted_at DESC LIMIT 20;
```

## 3. Adauga report subscriber nou

```sql
INSERT INTO tourism_audit_v2.report_subscribers (email, rate_limit_exempt)
VALUES ('email@example.com', false);
```

## 4. Deploy backend change

Push to `main` branch. Render auto-deploy:

```bash
git push origin main
```

Verifica: `https://api.audit-turism.ro/healthz`

## 5. Blocheaza spam domain

```sql
INSERT INTO public.blocked_emails (email, reason)
VALUES ('spam-domain.com', 'Spam submissions');
```

Nota: `blocked_emails` e in schema `public` (shared), nu `tourism_audit_v2`.

## 6. Re-run audit esuat

```sql
-- Reset status la pending
UPDATE tourism_audit_v2.properties
SET status = 10, status_text = 'pending_retry',
    last_status_update_at = now()
WHERE id = 'PROPERTY_UUID_HERE';
```

Apoi trigger manual:

```bash
curl -X POST https://api.audit-turism.ro/api/generate-audit \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_BACKEND_API_KEY" \
  -d '{"property_id": "PROPERTY_UUID_HERE"}'
```

## 7. Update Gemini model

Pe Render dashboard, schimba env var:
- `GEMINI_DEEP_RESEARCH_MODEL` (default: `deep-research-pro-preview-12-2025`)
- `GEMINI_FORMATTER_MODEL` (default: `gemini-3-pro-preview`)

Render face auto-redeploy la env var change.

## 8. Check production health

```bash
# Backend
curl https://api.audit-turism.ro/healthz

# Frontend
curl -s https://audit-turism.ro/api/health

# Recent audit activity
# In Supabase SQL Editor:
SELECT status, status_text, count(*)
FROM tourism_audit_v2.properties
WHERE inserted_at > now() - interval '7 days'
GROUP BY status, status_text;
```

UptimeRobot monitorizeaza ambele endpoints.

## 9. Adauga pensiune manual in DB

```sql
INSERT INTO tourism_audit_v2.properties (
  owner_name, owner_email, property_name, property_address, status
) VALUES (
  'Nume Proprietar',
  'email@example.com',
  'Pensiunea Exemplu',
  'Brasov',
  10  -- pending
);
```

Apoi trigger audit cu procedura de la punctul 6.

## 10. Update pg_cron jobs

In Supabase SQL Editor:

```sql
-- Vezi joburi active
SELECT * FROM cron.job;

-- Modifica interval keep-alive (acum: 10 min)
SELECT cron.alter_job(9, schedule := '*/5 * * * *');  -- schimba la 5 min

-- Sterge job
SELECT cron.unschedule(JOB_ID);
```

Joburi active:
- `keep-render-alive` (jobid=9): healthz ping every 10 min
- `daily-audit-report` (jobid=10): 06:00 UTC daily report
