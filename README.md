# Audit Digital Turism (Tourism Audit V2)

Audit digital gratuit pentru pensiuni, case de vacanta si unitati de cazare din Romania.

Produs de [DeviDevs Agency](https://devidevs-agency.com) (DeviDevs Technologies S.R.L.)

**Site:** [audit-turism.ro](https://audit-turism.ro)

## Ce face

Userul completeaza un formular (2 min). In 30-90 de minute primeste pe email un raport detaliat cu recomandari personalizate, generat de Gemini Deep Research (60-120+ cautari web).

## Stack

| Component | Tech | Hosting |
|-----------|------|---------|
| Frontend | Next.js 16, React 19, Tailwind 4, shadcn/ui | Vercel |
| Backend | Python 3.13, Flask, Gunicorn | Render |
| AI | Google Gemini Deep Research + Gemini 3 Pro | Google AI |
| Database | PostgreSQL (schema: `tourism_audit_v2`) | Supabase |
| Email | Resend (domain: audit-turism.ro) | Resend |
| Rate Limit | Upstash Redis | Upstash |

## Structura

```
frontend/     Next.js app (Vercel)
backend/      Flask API (Render)
supabase/     Migrari SQL
knowledge/    Reviews, state, mistakes
_bmad-output/ Planificare BMAD (complet)
```

## Development

### Frontend

```bash
cd frontend
npm install
npm run dev          # Dev server
npm run build        # Production build
npm run lint         # ESLint
```

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m flask run  # Dev server (port 5000)
```

### Environment

Copiaza `.env.example` in `.env.local` (frontend) si `.env` (backend). Vezi fisierele pentru variabilele necesare.

## Pipeline

```
Form submit -> Supabase insert (status=10)
            -> Backend trigger (fire-and-forget, 60s timeout)
            -> Gemini Deep Research (30-90 min, polling la 30s)
            -> Gemini Formatter (structureaza in 3 sectiuni)
            -> Quality Filter (scoate limbaj defensiv)
            -> PDF (fpdf2) + Email HTML (Jinja2)
            -> Resend delivery (3 retry, backoff exponential)
            -> Status 99 (success) sau 0 (failed)
```

## Documentatie

- `CLAUDE.md` - Reguli de proiect si arhitectura detaliata
- `RUNBOOK.md` - Proceduri operationale
- `PRODUCTION-DEPLOY-PLAN.md` - Plan de deploy
- `_bmad-output/project-context.md` - 87 reguli de implementare
