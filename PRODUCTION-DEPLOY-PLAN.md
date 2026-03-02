# Tourism Audit V2 — Production Deployment Plan v5

**Data:** 2026-03-02 (updated: 2026-03-02)
**Reviewed by:** John (PM), Winston (Architect), Barry (Dev), Murat (QA), Dr. Quinn (Problem Solver)
**v4 changes:** Fix env var leak (P1), stuck audit safety net (P2), fetch timeout (P3), reCAPTCHA (P4), .env.example completeness (P5), config.py alignment (P7)
**v5 changes:** CORS downgrade CRITICAL→MEDIUM (P9), SupabaseService singleton noted (P11), minor code hygiene (P10, P12, P13)

---

## Render Free Tier Keep-Alive: Supabase pg_cron

Render free tier spins down after 15 min of no HTTP traffic. Audit pipeline = 30-90 min.
**Solutie:** Supabase `pg_cron` + `pg_net` — ping `/healthz` la fiecare 4 min din baza de date.

```sql
-- Enable extensions (once, via Supabase dashboard or migration)
create extension if not exists pg_cron;
create extension if not exists pg_net;

-- Cron job: ping Render every 4 minutes
select cron.schedule(
  'keep-render-alive',
  '*/4 * * * *',
  $$select net.http_get('https://<render-url>/healthz')$$
);
```

**Avantaje:** zero cost, zero servicii externe, ruleaza 24/7 in Supabase existent.
**Fallback:** Daca pierdem audituri -> upgrade Render la Starter ($7/mo, no spin-down).

---

## Property Status State Machine

```
[Form Submit] --> 10 (pending)
                   |
          [API: generate-audit]
                   |
                   v
               1 (running)  <-- blocks new requests (409)
              /          \
         [success]    [any error]
            |              |
            v              v
        99 (success)    0 (failed)
```

**Block rules for /api/generate-audit:**
- status=10 (pending) -> allow (normal flow)
- status=1 (running) -> 409 "Audit already in progress"
- status=99 (success) -> 409 "Audit already completed"
- status=0 (failed) -> allow (retry)

---

## Faza 1: Fix-uri critice backend

### 1.1 REVERT: PDF attachment format
**Fisier:** `backend/src/email_service.py`
- **V2 "fix" era un REGRESSION.** Resend SDK accepta `List[int]` nativ: `content: Union[List[int], str]`
- `list(pdf_bytes)` era CORECT de la inceput
- **Status:** REVERTED — cod restaurat la `list(pdf_bytes)`, `import base64` sters

### 1.2 MEDIUM: Adauga CORS (downgraded in v5 — server-to-server call nu necesita CORS)
**Fisiere:** `backend/app.py`, `backend/requirements.txt`, `backend/config.py`
- **Nota v5:** Browser-ul NU cheama Flask direct — Next.js API route face fetch server-side. CORS nu e strict necesar pentru flow-ul actual, dar il adaugam ca safety net si buna practica.
- `flask-cors` cu origins din env var `ALLOWED_ORIGINS`
- **Origins permise:**
  - `ALLOWED_ORIGINS` env var (production Vercel URL, comma-separated)
  - `http://localhost:3000` adaugat automat in dev (FLASK_ENV=development)
- Allow headers: `Content-Type`, `X-API-Key`
- Allow methods: `GET`, `POST`, `OPTIONS`
- **`config.py`:** Adauga `ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "")` pentru consistenta cu celelalte env vars

### 1.3 CRITICAL: Fix daemon thread + graceful shutdown
**Fisiere:** `backend/src/pipeline.py`, `backend/app.py`
- `daemon=True` = thread-ul moare instant la shutdown
- **Fix:**
  1. `pipeline.py`: `daemon=True` -> `daemon=False`
  2. `pipeline.py`: Track threads in module-level `RUNNING_THREADS` list
  3. `app.py`: SIGTERM handler waits for running threads (max 5400s)
- **Nota:** Pe Render free tier, spin-down nu trimite SIGTERM — kill direct. Dar fix-ul protejaza la redeploy (care FACE SIGTERM) si la Render paid tier.

### 1.4 HIGH: Duplicate submission guard
**Fisier:** `backend/src/routes.py`
- Check `property_data.status` inainte de `start_pipeline_thread()`:
  - `status in (1, 99)` -> 409 Conflict
  - `status in (10, 0)` -> allow

### 1.5 HIGH: Validare env vars la startup
**Fisier:** `backend/app.py`
- Check in `create_app()`, raise ValueError daca lipsesc:
  - `GOOGLE_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`
  - `RESEND_API_KEY`, `BACKEND_API_KEY`, `MEETING_LINK`
- Nu valida: `SENTRY_DSN` (optional), `FROM_EMAIL` (has default), model names (have defaults), `ALLOWED_ORIGINS` (optional in dev)

### 1.6 Update config files
- `backend/.env.example`: Adauga `ALLOWED_ORIGINS=` si `FLASK_ENV=production`
- `backend/Procfile`: `--workers 2` -> `--workers 1` (un worker = thread-uri nu se pierd la recycle)
- `backend/Dockerfile`: Mirror Procfile change

### 1.7 MEDIUM: Keep-alive endpoint (pentru Render free tier)
**Fisier:** `backend/src/routes.py`
- `/healthz` existent e suficient — pg_cron il va pinga la 4 min
- Adauga logging: `logger.debug("Health check pinged")` (sa vedem daca keep-alive functioneaza)

---

## Faza 1B: Fix-uri critice frontend (NOU in v4)

### 1B.1 CRITICAL: Rename `NEXT_PUBLIC_BACKEND_API_URL` -> `BACKEND_API_URL`
**Fisiere:** `frontend/src/app/api/audit/submit/route.ts`, `frontend/.env.example`, `frontend/.env.local`
- Prefixul `NEXT_PUBLIC_` expune URL-ul backend-ului in browser bundle JS
- Variabila e folosita DOAR server-side (in API route handler), deci NU are nevoie de prefix
- **Fix:** Rename la `BACKEND_API_URL` (fara `NEXT_PUBLIC_`)
- **Vercel:** Update env var name in dashboard (Faza 6)

### 1B.2 MEDIUM: Adauga timeout pe backend fetch
**Fisier:** `frontend/src/app/api/audit/submit/route.ts`
- `fetch()` catre backend nu are timeout — poate hang indefinit pe Render cold start
- **Fix:** `AbortController` cu timeout de 10s
- Fire-and-forget ramane, dar fetch-ul nu va leak resurse
- Daca timeout -> log warning (audit inca poate porni daca Render raspunde dupa)

### 1B.3 LOW: Adauga TODO comment pentru reCAPTCHA
**Fisier:** `frontend/src/app/api/audit/submit/route.ts`
- `react-google-recaptcha-v3` e instalat dar validarea server-side e dezactivata
- **Decizie:** NU activam reCAPTCHA acum (MVP, honeypot + rate limit suficiente)
- **Fix:** Adauga TODO comment explicit cu prioritate post-MVP
- **Risc acceptat:** Bot sofisticat poate spam Gemini API requests (costisitor)

---

## Faza 2: Teste locale

### 2.1 Re-run e2e test
- `cd backend && source .venv/bin/activate && python tests/test_e2e_local.py`
- **Verificare:** Email primit cu PDF valid (list[int] format, neschimbat)
- **Gate:** PASS obligatoriu

### 2.2 Test HTTP endpoint (NOU)
- Flask test client (fara server real):
  - POST fara API key -> 401
  - POST cu API key + property_id valid (status=10) -> 202
  - POST cu property_id inexistent -> 404
  - POST cu property_id status=1 -> 409 "already in progress"
  - POST cu property_id status=99 -> 409 "already completed"
  - POST cu property_id status=0 -> 202 (retry allowed)
  - OPTIONS request -> CORS headers prezente
- **Gate:** PASS obligatoriu

### 2.3 Test env var validation
- Sterge temporar GOOGLE_API_KEY -> `create_app()` -> ValueError
- **Gate:** PASS obligatoriu

### 2.4 Test graceful shutdown (manual, quick)
- Porneste app, verifica SIGTERM handler e registered
- **Gate:** Handler inregistrat (no crash la import)

---

## Faza 3: Verify .gitignore + commit + push

### 3.1 Verify .gitignore
- **Deja verificat:** `.gitignore` existent acopera: `.env`, `.env.local`, `__pycache__/`, `.venv/`, `node_modules/`, `.next/`
- Run `git status` — confirma ca nu apar fisiere sensibile
- **Gate:** Clean status

### 3.2 Commit
- `git add backend/ supabase/ frontend/ .gitignore PRODUCTION-DEPLOY-PLAN.md`
- Commit descriptiv

### 3.3 Push
- `git push origin main`
- **Gate:** Push reusit

---

## Faza 4: Deploy backend pe Render (via agent-browser port 9224)

### 4.1 Create Render Web Service
- https://dashboard.render.com -> New Web Service -> Connect GitHub repo
- Repo: `Serathill/tourism-audit-v2`
- Root directory: `backend`
- Runtime: Python 3
- Build command: `pip install -r requirements.txt`
- Start command: autodetect din Procfile
- **Workers=1** in Procfile

### 4.2 Set env vars pe Render
```
GOOGLE_API_KEY=<din .env.local>
GEMINI_DEEP_RESEARCH_MODEL=deep-research-pro-preview-12-2025
GEMINI_FORMATTER_MODEL=gemini-3-pro-preview
SUPABASE_URL=<din .env.local NEXT_PUBLIC_SUPABASE_URL>
SUPABASE_KEY=<din .env.local SUPABASE_SERVICE_ROLE_KEY>
RESEND_API_KEY=<din .env.local>
FROM_EMAIL=Digital Audit <no-reply@devidevs.com>
BACKEND_API_KEY=<din .env.local>
MEETING_LINK=<din .env.local>
SENTRY_DSN=<din .env.local>
ALLOWED_ORIGINS=<Vercel production URL>
FLASK_ENV=production
```

### 4.3 Smoke test backend
1. `curl https://<render-url>/healthz` -> 200 OK
2. Check Render logs — fara erori la startup
3. Check Sentry — fara erori noi
- **Gate:** Toate 3 OK

### 4.4 Setup Supabase pg_cron keep-alive
- Supabase SQL Editor -> run:
  ```sql
  select cron.schedule(
    'keep-render-alive',
    '*/4 * * * *',
    $$select net.http_get('https://<render-url>/healthz')$$
  );
  ```
- **Verificare:** `select * from cron.job;` -> job exists
- **Gate:** Cron job activ

### 4.5 Setup UptimeRobot (monitoring + alerting ONLY)
- https://uptimerobot.com -> Add monitor -> HTTP(s)
- URL: `https://<render-url>/healthz`
- Interval: 5 minute
- Alert contacts: owner email
- **Scop:** DOAR notificari/alerting cand Render e down. Keep-alive e handled de pg_cron (4.4).
- **Gate:** Monitor activ, first ping OK

---

## Faza 5: Supabase Exposed Schemas (via agent-browser port 9224)

### 5.1 Supabase Dashboard
- API Settings -> Exposed Schemas -> adauga `tourism_audit_v2`

### 5.2 Verificare
- Query `tourism_audit_v2.properties` via Supabase client -> date returnate
- **Gate:** Query OK

---

## Faza 6: Update frontend env + redeploy (via agent-browser port 9224)

### 6.1 Vercel Dashboard
- Set `BACKEND_API_URL` = URL-ul Render din Faza 4 **(FARA prefix NEXT_PUBLIC_ — server-only)**
- Set `BACKEND_API_KEY` = acelasi ca in .env.local (folosit de Next.js API route server-side)
- Trigger redeploy

### 6.2 Verificare frontend
- Site se incarca fara erori console
- **Gate:** Site functional

---

## Faza 7: Integration test end-to-end (via agent-browser port 9224)

### 7.1 Test form submit
1. Deschide site-ul Vercel in agent-browser (port 9224!)
2. Submit form cu date de test (email: judocky21@gmail.com)
3. Check Supabase: property cu status=10
4. Check Render logs: pipeline started, status -> 1
5. Asteapta completare (30-90 min) — check periodic Supabase status
6. Check final: status -> 99 (success)
7. Check email: HTML + PDF primit

### 7.2 Test duplicate prevention
- Re-submit acelasi form din browser -> 409 (sau frontend previne)

### 7.3 Verify audit data
- Query `audit_logs` -> toate fazele logate
- Query `audit_results` -> raw_audit + formatted_data prezente

---

## Fisiere de modificat

| Fisier | Modificare | Status |
|--------|-----------|--------|
| `backend/src/email_service.py` | REVERT base64 -> list(pdf_bytes) | DONE |
| `backend/app.py` | CORS + env var validation + SIGTERM handler | DONE |
| `backend/config.py` | + ALLOWED_ORIGINS (v4) | DONE |
| `backend/src/pipeline.py` | daemon=False + RUNNING_THREADS | DONE |
| `backend/src/routes.py` | Duplicate guard (status check) + healthz log | DONE |
| `backend/requirements.txt` | + flask-cors | DONE |
| `backend/.env.example` | + ALLOWED_ORIGINS + FLASK_ENV (v4) | DONE |
| `backend/Procfile` | workers 2 -> 1 | DONE |
| `backend/Dockerfile` | workers 2 -> 1 | DONE |
| `frontend/src/app/api/audit/submit/route.ts` | Rename env var + fetch timeout + reCAPTCHA TODO (v4) | DONE |
| `frontend/.env.example` | Rename NEXT_PUBLIC_BACKEND_API_URL -> BACKEND_API_URL (v4) | DONE |

---

## Rollback plan per faza

### Faza 4 (Render) fail:
1. Check Render logs
2. Fix -> commit -> push -> auto-redeploy
3. Daca nu se rezolva: delete service, revert commit, recreate

### Faza 5 (Supabase) fail:
1. PostgREST restart din dashboard
2. Backend foloseste Python client direct, nu depinde de exposed schema

### Faza 6 (Vercel) fail:
1. Revert env var -> redeploy
2. Frontend fara BACKEND_API_URL -> form nu triggereaza audit, dar site merge

### Faza 7 (Integration) fail:
1. Check audit_logs pentru ultimul status_text
2. Fix componenta specifica -> redeploy

### Audit stuck la status=1:
1. Manual: Supabase dashboard -> update status=0
2. Re-trigger: POST generate-audit

---

## Known limitations (post-MVP backlog)

1. **Render free tier risk** — pg_cron keep-alive e workaround, nu solutie. Upgrade la $7/mo cand avem clienti.
2. **No status polling in frontend** — user-ul nu vede progress, doar asteapta email 30-90 min.
3. **No stale audit cleanup** — property stuck la status=10 sau status=1 necesita fix manual. **Post-MVP:** pg_cron job care reseteaza status=0 daca status=10 > 15 min sau status=1 > 120 min.
4. **No checkpoint/resume** — daca pipeline moare mid-execution, audit-ul e pierdut.
5. **Frontend fire-and-forget** — backend call fail = user vede "success" dar audit nu porneste. Mitigat partial cu fetch timeout (v4). **Post-MVP:** verificare raspuns backend + retry sau notificare user.
6. **Single worker** — un audit = un thread. Multiple simultane = OK dar CPU/RAM limitat pe free tier (0.1 CPU, 512 MB).
7. **No dependency health check** — `/healthz` returneaza 200 chiar daca Supabase/Resend/Gemini sunt down.
8. **reCAPTCHA dezactivat** — honeypot + rate limit (5 req/60s) sunt singurele protectii. Bot sofisticat poate spam Gemini API. **Post-MVP:** activare reCAPTCHA v3 server-side validation.
9. **SupabaseService instantiated per-request** (v5) — `SupabaseService()` creaza un nou httpx client la fiecare call. Functional, dar ineficient. **Post-MVP:** singleton pattern sau module-level instance.
10. **`booking_platform_links` null vs []** (v5) — Frontend trimite `null`, backend asteapta `list`. Fallback existent (`or []`) functioneaza, dar inconsistent in DB. **Post-MVP:** normalizare la `[]` la insert.
11. **Error notification HTML unescaped** (v5) — `error_message` inserat direct in HTML fara escaping in `email_service.py`. Nu e exploatabil (mesaje hardcoded), dar pattern fragil. **Post-MVP:** escape cu `html.escape()`.

---

## Changelog v3 -> v4 -> v5

### v4 (review round 1)
| # | Problema | Severitate | Fix |
|---|---------|-----------|-----|
| P1 | `NEXT_PUBLIC_BACKEND_API_URL` expus in browser bundle | CRITICAL | Rename -> `BACKEND_API_URL` (Faza 1B.1, 6.1) |
| P2 | Properties stuck la status=10 silent forever | HIGH | Documentat in Known Limitations #3 cu propunere pg_cron cleanup post-MVP |
| P3 | Fetch fara timeout in route.ts | MEDIUM | AbortController cu 10s timeout (Faza 1B.2) |
| P4 | reCAPTCHA dezactivat, risc spam Gemini API | MEDIUM | Acceptat ca risc MVP, documentat in Known Limitations #8 |
| P5 | `.env.example` lipsea `FLASK_ENV` | LOW | Adaugat in Faza 1.6 |
| P6 | UptimeRobot vs pg_cron rol neclar | LOW | Clarificat in Faza 4.5: "DOAR notificari/alerting" |
| P7 | `config.py` fara `ALLOWED_ORIGINS` | INFO | Adaugat in Faza 1.2 |
| P8 | Test HTTP endpoint inexistent | INFO | Ramas ca in v3 — testul trebuie scris de la zero |

### v5 (review round 2)
| # | Problema | Severitate | Fix |
|---|---------|-----------|-----|
| P9 | CORS marcat CRITICAL dar server-to-server nu necesita CORS | HIGH->MEDIUM | Downgrade severitate Faza 1.2, ramane ca safety net |
| P10 | `require_api_key` blocheaza cand `BACKEND_API_KEY=""` | INFO | OK ca protectie, redundant cu env var validation (1.5) |
| P11 | `SupabaseService()` instantiat per-request | MEDIUM | Known Limitation #9 (post-MVP singleton) |
| P12 | `booking_platform_links` null vs [] inconsistenta | LOW | Known Limitation #10 (post-MVP normalizare) |
| P13 | HTML injection in error notification email | LOW | Known Limitation #11 (post-MVP html.escape) |

---

## Gate summary

| # | Gate | Criteriu | Blocker? |
|---|------|----------|----------|
| G1 | E2E test local | Email + PDF primit, status=99 | DA |
| G2 | HTTP endpoint test | 401/202/404/409 + CORS | DA |
| G3 | Env var validation | ValueError on missing | DA |
| G4 | .gitignore clean | No secrets in git status | DA |
| G5 | Render healthz | 200 OK, no startup errors | DA |
| G6 | pg_cron keep-alive | Cron job activ, pings every 4 min | DA |
| G7 | UptimeRobot monitoring | Monitor activ + alert contacts | DA |
| G8 | Supabase schema | Query returns data | DA |
| G9 | Frontend loads | No console errors | DA |
| G10 | Integration test | Form -> email primit | DA |
