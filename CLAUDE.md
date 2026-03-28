# CLAUDE.md - Tourism Audit V2 (Cazare-Audit)

## Identity

```yaml
PROJECT: Cazare-Audit (Tourism Audit V2)
PRODUCT_OF: DeviDevs Agency (sub-brand of DeviDevs Technologies S.R.L.)
TYPE: Free digital marketing audit for Romanian accommodation businesses
GOAL: Lead magnet → strategic consultation → paid services (€149/€699/€2499/month)
WEBSITE: audit-turism.ro
PARENT: devidevs-agency.com → devidevs.com

COMPANY:
  legal_name: "DeviDevs Technologies S.R.L."
  cui: 48553919
  j_number: "J40/13982/2023"
  administrator: "Constantin Petrut (SOLE signer for ALL official documents)"
  team:
    - "Petru Constantin - CEO (MLOps, DevOps)"
    - "Nicu Constantin - CTO Consultant (AI Security)"
    - "Alexandru Damian Mihaila - Partner (Libernote S.R.L., Marketing)"

TARGET: ~8,000 independent Romanian accommodation operators (pensiuni, case vacanta, tiny houses, A-frames)
```

---

## Golden Rules

### RULE 0: LEARN FROM MISTAKES
```
BEFORE any action → READ knowledge/learned/mistakes.yaml
AFTER any mistake → ADD to mistakes.yaml with:
  id, date, category, what happened, root cause, fix, rule added

Self-learning cycle:
  Mistake → Document → Add rule → Never repeat
  Win → Extract pattern → Apply everywhere
```

### RULE 1: ANALYZE x10 → VERIFY x10 → TEST
```
Do NOT guess. Do NOT assume. Do NOT hallucinate.
1. READ the actual code before making claims about it
2. VERIFY every fact against the real files (versions, models, configs)
3. TEST changes with real services before declaring done
4. If unsure → read the file. If still unsure → read it again.

NEVER claim something exists without checking the file.
NEVER claim a version without reading package.json / requirements.txt.
NEVER reference OpenAI in this project — it's Gemini (READ config.py).
```

### RULE 2: REAL DATA ONLY
**NEVER create mock data for testing.** Always use real Supabase, real Gemini API, real Resend.
```python
from dotenv import load_dotenv
load_dotenv()
# Test with REAL calls, REAL database, REAL APIs — no exceptions
```

### RULE 3: ALL USER-FACING CONTENT IN ROMANIAN
Headers, form labels, error messages, emails, SEO text, audit output — ALL in Romanian.
Professional, confident, friendly tone. NO defensive language ("nu am putut", "nu s-a putut", "limitari de acces") — always reframe as actionable recommendations.

### RULE 4: THINK BEFORE CHANGING
```
Before making ANY change:
1. What works well? KEEP IT.
2. What doesn't work? WHY?
3. What's the MINIMAL change to fix without breaking what works?
NEVER rewrite a file from scratch if adjustments suffice.
NEVER cut anything without putting something BETTER in its place.
```

### RULE 5: NO SECRETS IN GIT
v1 had secrets committed to git — NEVER AGAIN.
NEVER commit: `.env`, `.env.local`, API keys, tokens, service role keys.
Use Vercel env vars (frontend) and Render dashboard (backend).

### RULE 6: THIS IS GEMINI, NOT OPENAI
```
AI ENGINE: Google Gemini (NOT OpenAI, NOT GPT-4, NOT ChatGPT)
  Phase 1: deep-research-pro-preview-12-2025 (google-genai library)
  Phase 2: gemini-3-pro-preview (google-genai library)
  Env var: GOOGLE_API_KEY (NOT OPENAI_API_KEY)

The old/ directory references OpenAI — that was V1. IGNORE IT completely.
```

### RULE 7: READ PROJECT-CONTEXT BEFORE IMPLEMENTING
```
MANDATORY READ: _bmad-output/project-context.md
Contains 87 implementation rules covering:
  TypeScript, React, forms, API routes, Supabase clients,
  styling, email templates, security, SEO, anti-patterns.
READ IT before writing any code. Follow ALL rules exactly.
```

### RULE 8: NO MONOLITHIC COMPONENTS
v1 had 778-line homepage and 679-line form page. Extract sections into separate components.
Max ~200 lines per component. If it's getting big, split it.

### RULE 9: DON'T ASK — EXECUTE
```
Take decisions autonomously. Analyze, verify, test.
ASK only for: strategy changes, financial decisions, irreversible actions.
Everything else: just do it.
```

### RULE 10: GANDESTE DE LA REZULTAT INAPOI (REVERSE ENGINEERING)
```
Nu pune numere arbitrare. Nu "ajusteaza" din feeling. GANDESTE:

1. CE REZULTAT VREAU? (ex: <3% bounce rate pe landing page)
2. CE PRODUCE REZULTATUL? (ex: load time <2s, above-fold CTA, clear value prop)
3. CE ACTIUNI CONCRETE? (ex: compress images, lazy load below fold, rewrite H1)
4. FA ALEA. Masoara. Ajusteaza.

Aplica la ORICE decizie:
- "Cat de mare sa fie componenta?" → Cat e nevoie ca sa fie citibila si testabila
- "Cate retry-uri pe email?" → Cat e nevoie ca deliverability sa fie >99%
- "Ce scor reCAPTCHA?" → Cat e nevoie ca sa blochezi boti fara sa pierzi useri reali
- "Cate campuri in form?" → Cat e nevoie ca auditul sa fie relevant (minim 4)

Numarul serveste REZULTATUL, nu invers.
Daca nu stii DE CE faci o actiune → NU o face.
Daca stii DE CE dar nu stii CATE → estimeaza, masoara, ajusteaza.
```

### RULE 11: FINISH WHAT YOU START — TARGET NOT MINIMUM
```
MINIMUM = esec partial. TARGET = succes. Half-done = tech debt.

NICIODATA nu te opri la "merge si asa". TARGET e obiectivul.

Applies to:
- Bug fix: nu doar fix-ul, ci si root cause + regression prevention
- Feature: nu doar happy path, ci si error states + edge cases
- Refactor: nu doar split fisierul, ci si verifica ca totul functioneaza
- Deploy: nu doar push, ci si verify in production

SELF-CHECK inainte de "done":
1. Am rezolvat CE s-a cerut? (nu ce am crezut eu ca s-a cerut)
2. Am verificat ca nu am spart altceva?
3. Build trece? Lint trece?
4. Daca e user-facing: arata bine PE MOBIL?
5. Mai am ceva recuperabil ACUM? Da → fa-l. Nu → raporteaza GAP-ul.

NU raporta "done" cu gap-uri recuperabile.
```

### RULE 12: SESSION STRUCTURE (PRE-FLIGHT → EXECUTE → POST-FLIGHT)
```
Fiecare sesiune de lucru urmeaza structura:

PRE-FLIGHT (obligatoriu):
  1. READ knowledge/learned/mistakes.yaml (RULE 0)
  2. READ knowledge/state/session-state.yaml (ce s-a facut ultima data)
  3. VERIFY: ce e deploy-at acum functioneaza? (healthz, build status)
  4. IDENTIFY: ce e prioritar azi? (din session-state TODO list)

EXECUTE:
  - Lucreaza pe task-uri in ordinea prioritatii
  - Dupa fiecare task completat → UPDATE session-state.yaml
  - Daca descoperi o problema noua → adaug-o in TODO, nu o ignora
  - Daca faci o greseala → IMEDIAT in mistakes.yaml (RULE 0)

POST-FLIGHT (obligatoriu cand sesiunea se termina):
  1. UPDATE session-state.yaml cu: ce s-a facut, ce ramane, blockers
  2. UPDATE mistakes.yaml daca au fost greseli
  3. VERIFY: build trece? Ce am deploy-at functioneaza?
  4. HANDOFF: scrie clar ce trebuie facut la urmatoarea sesiune
```

### RULE 13: STATE TRACKING — YAML BRAIN
```
SSOT files (Single Source of Truth):
  knowledge/state/session-state.yaml  — ultima sesiune, TODO, blockers, next steps
  knowledge/learned/mistakes.yaml     — greseli si lectii (RULE 0)

session-state.yaml format:
  last_session:
    date: "YYYY-MM-DD"
    what_was_done: [list of completed items]
    blockers: [list of unresolved issues]
    next_steps: [prioritized TODO for next session]
  production:
    frontend_status: "ok/broken/deploying"
    backend_status: "ok/broken/deploying"
    last_verified: "YYYY-MM-DD"
    known_issues: [list]

UPDATE session-state.yaml at END of every session.
READ session-state.yaml at START of every session.
This is how you REMEMBER between conversations.
```

### RULE 14: GATE CHECKS — NU TRECE FARA SA VERIFICI
```
Before marking ANY task as done, pass the gate:

CODE CHANGE GATE:
  □ Am citit codul INAINTE sa-l modific? (RULE 1)
  □ Build trece local?
  □ Lint trece?
  □ Am verificat pe mobil daca e user-facing?
  □ Nu am introdus vulnerabilitati? (OWASP top 10)
  □ Nu am spart alt feature?

DEPLOY GATE:
  □ Build trece in CI?
  □ Healthz OK dupa deploy?
  □ Am testat flow-ul end-to-end?
  □ Am verificat ca email-urile ajung?

PR GATE:
  □ Commit message explica DE CE, nu doar CE
  □ Schimbarile sunt reviewable (nu monolith diff)
  □ Tests trec

Daca un gate FAIL → FIX inainte sa treci mai departe.
NICIODATA nu skip-ui un gate "ca e urgent".
```

---

## Architecture

### Product Flow

```
User → /marketing-pentru-turism → 3-step form wizard
  → POST /api/audit/submit
  → Rate limit → Honeypot → reCAPTCHA → Zod → Supabase insert → Backend trigger
  → Gemini Deep Research (30-90 min async)
  → Quality filter (remove defensive language)
  → Gemini template formatter (3-section structure)
  → PDF generation (fpdf2, DeviDevs branding)
  → Email delivery (Resend, HTML + PDF attachment)
  → CTA: book strategic consultation (HubSpot/Calendly)
```

### Backend Pipeline (3 Phases)

| Phase | What | Model/Tool | Duration |
|-------|------|-----------|----------|
| 1. Research | 60-120+ web searches, raw Romanian audit | `deep-research-pro-preview-12-2025` (google-genai) | 30-90 min |
| 2. Format | Structure into 3 sections + 11-category scoring | `gemini-3-pro-preview` (google-genai) | 10-20 sec |
| 3. Deliver | PDF generation + HTML email with retry | fpdf2 + Resend (3 retries, 2s→4s→8s backoff) | 5-10 sec |

**Output structure:**
```
AUDIT DIGITAL – [Property Name]
  1. Evaluarea Prezentei Online si Vizibilitatii
  2. Continut, Reputatie si Comunitate
  3. Oportunitati si Plan de Actiune
  Status icons: ✅ Bine / ⚠️ Necesita imbunatatiri / ❌ Lipsa/absent
  Scoring: 11 categories × 0-10 = 110 total
  Actiuni Prioritare: numbered action plan
```

Quality filter (`quality_filter.py`) removes defensive language via regex patterns — replaces with actionable recommendations.

### Status State Machine

```
[Form Submit] → 10 (pending)
                  ↓
          [Backend API trigger]
                  ↓
              1 (running)       ← blocks new requests (409 Conflict)
              /          \
         [success]    [any error]
            ↓              ↓
        99 (success)    0 (failed)  ← allows retry
```

---

## Tech Stack

### Frontend (Vercel)

| Tech | Version | Purpose |
|------|---------|---------|
| Next.js | 16.x | App Router, Turbopack, ISR |
| React | 19.x | Server Components by default |
| TypeScript | ^5 | Strict mode, no `any`, no `@ts-ignore` |
| Tailwind CSS | ^4 | CSS variables in globals.css, light mode only |
| shadcn/ui | Latest | Radix UI primitives (Button, Input, Card, etc.) |
| react-hook-form + Zod | ^4.x | Form validation, shared schemas client/server |
| Supabase JS | 2.x | 3 client patterns: browser, server, service role |
| Upstash Redis | Latest | Rate limiting (3/hour for audit submit) |
| reCAPTCHA v3 | Latest | Bot protection (score >= 0.5, disabled for MVP) |
| Sentry | ^10.x | Error tracking (10% traces, 100% replay on error) |
| GA4 | - | Analytics, scroll depth, UTM tracking, conversions |
| Fonts | - | Plus Jakarta Sans (display) + Inter (body) |

### Backend (Render)

| Tech | Version | Purpose |
|------|---------|---------|
| Python | 3.13+ | Runtime |
| Flask | >=3.1 | API server |
| Gunicorn | >=23.0 | WSGI: 1 worker, 4 threads, timeout=0 (long audits) |
| google-genai | >=1.0 | Gemini Deep Research + Gemini 3 Pro formatter |
| Pydantic | >=2.8 | Data models (PropertyData) |
| Supabase | >=2.0 | Database CRUD |
| Resend | >=2.0 | Email delivery with retry |
| Jinja2 | >=3.1 | Email HTML templates (dark theme, responsive) |
| fpdf2 | >=2.8 | PDF generation (cover page, content, CTA) |
| Sentry SDK | >=2.0 | Error tracking |

### Infrastructure

| Service | Purpose | Notes |
|---------|---------|-------|
| Vercel | Frontend hosting | ISR caching 7-30 days |
| Render | Backend hosting | Free tier, spins down after 15 min inactivity |
| Supabase | PostgreSQL database | Schema: `tourism_audit_v2`, RLS enabled |
| Resend | Transactional email | Domain: devidevs.com |
| Google Gemini | AI audit generation | Deep Research Pro + Gemini 3 Pro |
| Upstash Redis | Rate limiting | Sliding window, per-IP |
| Sentry | Error tracking | Frontend + backend |
| GA4 | Analytics | Page views, scroll depth, UTM, conversions |
| HubSpot/Calendly | Meeting CTA | Post-audit consultation booking |

**Render keep-alive:** pg_cron should ping `/healthz` every 10 min to prevent spin-down (Render free tier stops after 15 min inactivity). Documented in `PRODUCTION-DEPLOY-PLAN.md` but **migration not deployed yet** — only daily report cron (06:00 UTC) is active.

---

## Database (Supabase)

**Schema:** `tourism_audit_v2` | **RLS:** Enabled on all tables

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `properties` | Form submissions + status | id (UUID), owner_name, owner_email, property_name, property_address, website_url, booking_platform_links (JSONB), social_media_links (JSONB), google_my_business_link, business_description, status (INT), status_text |
| `audit_results` | AI-generated audit output | id, property_id (FK), raw_data (TEXT), formatted_data (TEXT) |
| `audit_logs` | Pipeline event trail | id, property_id, message, status_text, inserted_at |
| `report_subscribers` | Internal team BCC | id, email, rate_limit_exempt (BOOL) |
| `blocked_emails` | Spam domain blocklist | email (domain), reason |
| `audit_cold_emails` | Outreach tracking | id, email_0, email_1, email_2, subscribed (BOOL) |

**Supabase client patterns (frontend):**
- `lib/supabase/client.ts` — browser (anon key, client components)
- `lib/supabase/server.ts` — SSR (cookies, server components/route handlers)
- `lib/supabase/service.ts` — service role (admin only, NEVER in client code)

---

## Key Files

### Backend

| File | Purpose |
|------|---------|
| `backend/app.py` | Flask factory, Sentry init, env validation, SIGTERM handler (waits 90 min) |
| `backend/config.py` | All env vars with defaults (GOOGLE_API_KEY, models, Supabase, Resend) |
| `backend/src/routes.py` | Endpoints: GET /healthz, POST /api/generate-audit, POST /api/daily-report |
| `backend/src/pipeline.py` | 3-phase orchestrator, non-daemon threads, error cascade |
| `backend/src/audit_generator.py` | GeminiAuditor: Deep Research API + polling (30s interval, 90 min max) |
| `backend/src/template_processor.py` | Gemini formatter → parse to 3-section structure |
| `backend/src/quality_filter.py` | Regex removal of defensive language |
| `backend/src/pdf_generator.py` | fpdf2: cover page (dark, teal/amber), content, CTA page |
| `backend/src/email_service.py` | Resend: HTML + PDF attachment, 3 retries, seasonal urgency |
| `backend/src/database_service.py` | Supabase CRUD for properties, audit_results, audit_logs |
| `backend/src/models.py` | Pydantic PropertyData with validators |
| `backend/templates/audit_email.html` | Jinja2 email template (dark theme, responsive) |
| `backend/Dockerfile` | Python 3.13-slim, gunicorn 1 worker / 4 threads / timeout=0 |
| `backend/Procfile` | Render deployment: gunicorn with graceful-timeout 5500s |

### Frontend

| File | Purpose |
|------|---------|
| `frontend/src/app/layout.tsx` | Root layout: fonts, GA4, JSON-LD schemas (Organization, Service, WebApp) |
| `frontend/src/app/marketing-pentru-turism/page.tsx` | PRIMARY landing page (Hero + Audience + Process + FAQ + CTA) |
| `frontend/src/app/audit/page.tsx` | Standalone form wizard page |
| `frontend/src/app/servicii/page.tsx` | 3 service tiers with pricing |
| `frontend/src/app/despre-noi/page.tsx` | Team bios (Petru, Nicu, Alexandru) |
| `frontend/src/app/privacy-policy/page.tsx` | GDPR compliance |
| `frontend/src/app/terms-and-conditions/page.tsx` | Terms of service |
| `frontend/src/app/api/audit/submit/route.ts` | Form endpoint: rate limit → honeypot → reCAPTCHA → Zod → blocklist → Supabase → backend trigger |
| `frontend/src/app/api/health/route.ts` | Health check |
| `frontend/src/components/form/FormWizardClient.tsx` | 3-step form orchestrator |
| `frontend/src/components/form/StepOneBasic.tsx` | Step 1: name, email, property, county (required) |
| `frontend/src/components/form/StepTwoDetails.tsx` | Step 2: website, booking links, social, GMB, description (optional) |
| `frontend/src/components/form/StepThreeReview.tsx` | Step 3: review all fields + submit |
| `frontend/src/components/form/CountyAutocomplete.tsx` | Searchable dropdown, 42 counties grouped by region |
| `frontend/src/schemas/audit-form.ts` | Zod schemas + TypeScript types (shared client/server) |
| `frontend/src/lib/rate-limit.ts` | Upstash Redis rate limiting profiles |
| `frontend/src/lib/constants.ts` | Counties (42), team members, brand, nav links |
| `frontend/src/lib/supabase/` | 3 client patterns: browser, server, service role |
| `frontend/src/middleware.ts` | CSP nonce generation per request |
| `frontend/src/components/CookieConsentBanner.tsx` | Cookie consent + analytics opt-in |
| `frontend/src/components/ExitIntentPopup.tsx` | Desktop: mouse leave, mobile: 45s idle |

### Project Root

| File | Purpose |
|------|---------|
| `PRODUCTION-DEPLOY-PLAN.md` | 7-phase deployment plan (v5), keep-alive strategy, known issues |
| `_bmad-output/project-context.md` | **87 implementation rules — MANDATORY READ before coding** |
| `_bmad-output/planning-artifacts/` | PRD (668 lines), architecture (1261), epics (1615), UX design (1654) |
| `supabase/migrations/` | 3 migrations: schema creation, v1 cleanup, daily report cron |

---

## API Endpoints

### Backend (Flask)

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/healthz` | GET | None | Liveness probe (pg_cron pings every 10 min — migration pending) |
| `/api/generate-audit` | POST | X-API-Key header | Trigger 3-phase pipeline for `{property_id}` |
| `/api/daily-report` | POST | X-API-Key header | Email yesterday's audit metrics to subscribers |

### Frontend (Next.js)

| Endpoint | Method | Security | Purpose |
|----------|--------|----------|---------|
| `/api/audit/submit` | POST | Rate limit + honeypot + reCAPTCHA + Zod + blocklist | Form submission → Supabase → backend trigger |
| `/api/health` | GET | None | Health check |

---

## Environment Variables

### Backend (Render)

```bash
# Gemini AI — THIS IS GOOGLE, NOT OPENAI
GOOGLE_API_KEY=
GEMINI_DEEP_RESEARCH_MODEL=deep-research-pro-preview-12-2025
GEMINI_FORMATTER_MODEL=gemini-3-pro-preview

# Supabase
SUPABASE_URL=
SUPABASE_KEY=                      # Service role key

# Email
RESEND_API_KEY=
FROM_EMAIL=Digital Audit <no-reply@devidevs.com>

# API Auth
BACKEND_API_KEY=

# Meeting CTA
MEETING_LINK=

# CORS
ALLOWED_ORIGINS=                   # Comma-separated origins

# Error Tracking
SENTRY_DSN=

# Pipeline Tuning
AUDIT_POLL_INTERVAL=30             # Seconds between Deep Research polls
AUDIT_MAX_WAIT_MINUTES=90          # Max wait before timeout
```

### Frontend (Vercel)

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=         # Server-only! NEVER expose to client

# Backend API (server-only — NOT NEXT_PUBLIC!)
BACKEND_API_URL=
BACKEND_API_KEY=

# Rate Limiting (Upstash)
UPSTASH_REDIS_REST_URL=
UPSTASH_REDIS_REST_TOKEN=

# reCAPTCHA v3 (disabled for MVP)
NEXT_PUBLIC_RECAPTCHA_SITE_KEY=
RECAPTCHA_SECRET_KEY=

# Analytics & Error Tracking
NEXT_PUBLIC_GA_ID=
NEXT_PUBLIC_SENTRY_DSN=

# Site
NEXT_PUBLIC_SITE_URL=https://audit-turism.ro
NEXT_PUBLIC_HONEYPOT_FIELD_NAME=_hp_website
MEETING_LINK=
```

---

## Form Validation Chain (STRICT ORDER)

```
1. Rate limit check (Upstash Redis, 3 requests/hour per IP)
2. Honeypot check (if filled → silent fake success, bot doesn't know it was rejected)
3. reCAPTCHA v3 verify (score >= 0.5 — disabled for MVP, honeypot + rate limit only)
4. Zod schema validation (shared between client and server)
5. Email domain blocklist check (if blocked → silent fake success)
6. HTML escape user input (owner_name, property_name, address, description)
7. Supabase insert (status=10 pending) + backend fire-and-forget trigger (10s timeout)
```

**3-step wizard:**
- Step 1 (required): owner name, email, property name, county (42 counties with autocomplete)
- Step 2 (optional): website URL, booking platform links, social media links, GMB link, business description
- Step 3: review all fields + submit

---

## Error Handling

### Frontend
- 6 route-level error boundaries + `global-error.tsx` + custom `not-found.tsx`
- Sentry: 10% traces, 100% replay on error, filters browser extensions
- Per-field Romanian error messages with `aria-invalid` + `aria-describedby`
- Rate limit: 429 with Romanian message
- reCAPTCHA fail: 403

### Backend Pipeline Cascade
```
Phase fails → catch exception
  → Update property status to 0 (failed) + log to audit_logs
  → Send client notification (friendly Romanian, no technical details)
  → Send team failure alert (HTML email with property name, owner, error context)
```

**4 custom exceptions:** `DatabaseError`, `AuditGenerationError`, `TemplateProcessingError`, `EmailError`

**Retry logic:**
| Service | Retries | Backoff |
|---------|---------|---------|
| Gemini Deep Research | Poll every 30s, max 90 min | Linear (poll until done/timeout) |
| Email (Resend) | 3 attempts | Exponential: 2s → 4s → 8s |

---

## Security

- CSP headers via Next.js middleware (nonce-based script loading)
- Security headers: X-Frame-Options: DENY, X-Content-Type-Options: nosniff, HSTS, Referrer-Policy
- HTML escaping for all user content in emails
- No `dangerouslySetInnerHTML` except trusted first-party scripts (GA)
- CORS with env-configurable origins (backend)
- `require_api_key` decorator on all backend API routes
- RLS enabled on all Supabase tables
- Service role key NEVER exposed to client-side code
- Honeypot + rate limiting on all public forms

---

## SEO (Critical for V2)

- Primary slug: `/marketing-pentru-turism`
- Target keywords: "marketing pentru turism", "promovare turistica", "audit digital", "marketing turistic", "marketing pentru unitati de cazare"
- H1 includes primary keyword, first 100-150 words include primary keyword
- JSON-LD on marketing pages: Organization, ProfessionalService, BreadcrumbList, FAQPage
- Metadata + canonical URL on every page
- Sitemap (`sitemap.ts`) + robots (`robots.ts`)
- Separate pages: Despre Noi (`/despre-noi`), Servicii (`/servicii`) — NOT bundled into landing page
- OpenGraph + Twitter cards on all pages

---

## Development

```bash
# Frontend
cd frontend && npm run dev           # Dev server (polling for Docker/VM)
cd frontend && npm run dev:turbo     # Turbopack (faster rebuilds)
cd frontend && npm run build         # Production build
cd frontend && npm run lint          # ESLint check

# Backend
cd backend && pip install -r requirements.txt
cd backend && python -m flask run    # Dev server (port 5000)
cd backend && gunicorn app:app --bind 0.0.0.0:5000 --workers 1 --threads 4

# E2E test (uses REAL services — Supabase + Gemini + Resend)
cd backend && python tests/test_e2e_local.py

# Chrome for testing
# Port: 9224, Profile: ~/.config/chrome-tourism-audit
```

---

## Known Limitations (Post-MVP Backlog)

1. **Render free tier spin-down** — pg_cron keep-alive every 10 min is planned (`PRODUCTION-DEPLOY-PLAN.md`) but migration not deployed yet. Only daily report cron (06:00 UTC) is active.
2. **No frontend status polling** — user can't see audit progress after form submit
3. **No stale audit cleanup** — stuck at status=1 or status=10 requires manual DB reset
4. **Fire-and-forget** — if backend trigger fails after form submit, user sees "success" but no audit generated
5. **reCAPTCHA disabled** — MVP relies on honeypot + rate limit only
6. **Single gunicorn worker** — CPU/RAM limited for concurrent audits
7. **/healthz always 200** — returns OK even if Supabase/Resend/Gemini are down

---

## Anti-Patterns (V1 Mistakes — NEVER REPEAT)

| V1 Problem | V2 Rule |
|------------|---------|
| 778-line homepage, 679-line form | Max ~200 lines/component, extract sections |
| .env committed to git | .env in .gitignore, use Vercel/Render dashboards |
| 22MB page weight | <100KB budget, compress everything |
| OpenAI Deep Research + GPT-4 | Google Gemini only (google-genai library) |
| Defensive AI language in output | quality_filter.py + prompt engineering |
| English in user-facing content | ALL Romanian, no exceptions |
| console.log everywhere | Sentry for errors, remove console.log |
| Unoptimized images | next/image with AVIF/WebP, lazy loading |
| No error handling | 6 error boundaries, Sentry, pipeline cascade |
| No anti-bot protection | Rate limit + honeypot + reCAPTCHA (post-MVP) |
| Growth messaging ("creste rezervarile") | Loss-prevention ("afla ce te costa vizibilitatea slaba") |

---

## BMAD Method (Planning — COMPLETE)

BMAD v6.0.0 was used to plan this project. **All planning is done.** Artifacts:

| Artifact | Location | Lines |
|----------|----------|-------|
| Product Brief | `_bmad-output/planning-artifacts/product-brief-*.md` | 471 |
| PRD | `_bmad-output/planning-artifacts/prd.md` | 668 |
| Architecture | `_bmad-output/planning-artifacts/architecture.md` | 1261 |
| UX Design | `_bmad-output/planning-artifacts/ux-design-specification.md` | 1654 |
| Epics & Stories | `_bmad-output/planning-artifacts/epics.md` | 1615 (47 MVP stories) |
| Implementation Rules | `_bmad-output/project-context.md` | 87 rules |
| Research | `_bmad-output/planning-artifacts/research/` | 4 docs |

**BMAD agents** available as slash commands (`.claude/commands/bmad-*.md`):
- `/bmad-agent-bmm-dev` — Implementation & coding (Amelia)
- `/bmad-agent-bmm-pm` — Product requirements (John)
- `/bmad-agent-bmm-architect` — System design
- `/bmad-agent-bmm-analyst` — Research & analysis (Mary)
- `/bmad-agent-bmm-sm` — Sprint planning (Bob)
- `/bmad-agent-bmm-qa` — Quality assurance
- `/bmad-agent-bmm-tech-writer` — Documentation
- `/bmad-agent-tea-tea` — Test engineering
- And 90+ more workflows for planning, building, testing

**Use BMAD agents for structured planning/dev workflows. For quick fixes and bug fixes, work directly.**
