# MARELE TODO - 4 RUNDE
**Data:** 2026-03-29
**Sursa:** Consolidare din 20 review-uri BMAD + backlog Petru
**Ultima actualizare:** 2026-03-29

---

## RUNDA 1: CONVERSION BLOCKERS

| # | Task | Status |
|---|------|--------|
| 1.1 | **MEETING_LINK setat** pe Render: `https://calendar.app.google/eHH7fDyWcbYNLpk29` | DONE |
| 1.2 | **Email template v8-final-mix** - VALIDAT de Petru | DONE |
| ~~1.3~~ | ~~Formatter prompt rewrite~~ - SE FACE IN ALT CHAT (in lucru) | ALT CHAT |
| ~~1.3b~~ | ~~Deep Research directive review~~ | NU INCA |
| 1.4 | **FinalCTA** `/audit` -> `/marketing-pentru-turism#audit-form` | DONE |
| 1.5 | **Services page CTAs** - platite duc la `mailto:contact@audit-turism.ro` | DONE |
| 1.6 | **Branding** - deja OK in config.py (`Audit Digital Turism`) | DONE |

---

## RUNDA 2: WEBSITE CONVERSION OPTIMIZATION

| # | Task | Status |
|---|------|--------|
| 2.1 | **Social proof** - counter proprietati analizate | PENDING (needs decision) |
| 2.2 | **Pain points rescrisi** | ALEXANDRU (text) |
| 2.3 | **Inconsistenta timp** "5 min" -> "2 min formular, 30-90 min raport" | ALEXANDRU (text) |
| 2.4 | **Hero subtitle** "Afla" x2 | ALEXANDRU (text) |
| 2.5 | **WhyUs rescris** | ALEXANDRU (text) |
| 2.6 | **Mid-page CTA** dupa ProcessSection | PENDING (needs decision) |
| 2.7 | **Audience section** boutique -> pensiuni, case de vacanta | ALEXANDRU (text) |
| 2.8 | **CUI/J number in footer** | DONE |
| 2.9 | **PDF preview langa formular** | PENDING (needs asset) |
| 2.10 | **Editorial prose fixes** 15 rewrites | ALEXANDRU (text) |
| 2.11 | **FAQ reorder** - "Care e smecheria?" | DONE (deja prima) |

---

## RUNDA 3: TECH RELIABILITY

| # | Task | Status |
|---|------|--------|
| 3.1 | **Fire-and-forget timeout** 10s -> 60s | DONE |
| 3.2 | **RUNNING_THREADS cleanup** | DONE |
| 3.3 | **Global concurrency semaphore** max 3 | DONE |
| 3.4 | **Stale audit cleanup** healthz resets status=1 >120 min | DONE |
| 3.5 | **Bug: IndexError** empty outputs guard | DONE |
| 3.6 | **Bug: Double HTML encoding** scos escapeHtml(), Jinja2 autoescape se ocupa | DONE |
| 3.7 | **Bug: Case-sensitive parser** "Legenda status:" case-insensitive | DONE |
| 3.8 | **Bug: XSS in alert emails** html.escape() pe error_context | DONE |
| 3.9 | **CORS fallback** `["*"]` -> `[]` | DONE |
| 3.10 | **30 teste automate** pytest + vitest | SESIUNE SEPARATA |

---

## RUNDA 4: DOCS & INFRASTRUCTURE

| # | Task | Status |
|---|------|--------|
| 4.1 | **CLAUDE.md stale fixes** FROM_EMAIL, Resend domain, Known Limitations, pg_cron | DONE |
| 4.2 | **README.md** | DONE |
| 4.3 | **RUNBOOK.md** 10 proceduri | DONE |
| 4.4 | **.env.example** FROM_EMAIL actualizat (frontend + backend) | DONE |
| ~~4.5~~ | ~~Render paid upgrade~~ | SCOS (nu se face) |
| ~~4.6~~ | ~~Healthz real~~ | SCOS (UptimeRobot monitorizeaza) |
| ~~4.7~~ | ~~Status page~~ | SCOS (UptimeRobot) |

---

## NU ACUM (post-primii-10-clienti)

- Instant Snapshot (30 sec, fara Deep Research)
- Competitor Benchmark Report (49-99 RON, primul produs platit)
- Follow-up email sequence (Day 3, 7, 14)
- WhatsApp button pe site
- Nr. telefon pe site
- Cold outreach Instantly (marketing-turism.ro)
- Door-to-door Bran Corridor Blitz
- ANTREC partnership
- Facebook Groups value-first
- Reactivare 7 V1 clienti
- Task queue Celery + Redis (pt 100+/zi)
- "Pensiune OS" dashboard SaaS
