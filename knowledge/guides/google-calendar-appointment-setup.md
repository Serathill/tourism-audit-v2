# Google Calendar Appointment Scheduling - Setup Guide

Alternativa gratuita la Calendly, inclusa in Google Calendar (Workspace sau personal).

## Ce face

- Genereaza un link public de booking (ex: `calendar.app.google/xyz`)
- Clientii vad doar sloturile libere (nu vad detalii din calendar)
- Cand cineva rezerva, apare automat in calendarul tau
- Primesti notificare pe email + reminder inainte de call
- Se sincronizeaza cu calendarul real (daca ai o intalnire, slotul dispare)

## Setup pas cu pas

### 1. Alege contul corect

- Trebuie sa fie contul Google pe care il folosesti zi de zi (calendarul real)
- Daca ai Google Workspace (business) - foloseste-l pe ala
- In cazul nostru: `devideviart` (Workspace, calendarul cu evenimente reale)

### 2. Creaza Appointment Schedule

1. Deschide [Google Calendar](https://calendar.google.com)
2. In stanga jos: **Booking pages** (sau "Pagini de rezervari")
3. Click pe butonul **+** ("Create appointment schedule" / "Creaza un program al intalnirilor")
4. Completeaza:
   - **Titlu:** ex. "Consultanta Strategica Gratuita - Audit Digital Turism"
   - **Durata:** 30 minute (recomandat pentru prima consultanta)
   - **Disponibilitate:** default Luni-Vineri 9:00-17:00 (ajusteaza dupa nevoie)
5. Click **Next**
6. Pe pagina 2 (Booking form): lasa default (First name, Last name, Email) - nu adauga campuri extra
7. Click **Save**
8. Copiaza link-ul generat (format: `https://calendar.app.google/xxxxx`)

### 3. Pune link-ul in productie

Link-ul trebuie setat ca env var `MEETING_LINK` pe toate platformele:

**Render (backend):**
```bash
curl -s -X PUT "https://api.render.com/v1/services/{SERVICE_ID}/env-vars" \
  -H "Authorization: Bearer {RENDER_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '[{"key": "MEETING_LINK", "value": "https://calendar.app.google/xxxxx"}]'
```

**Vercel (frontend):**
- Daca env var-ul nu exista: POST la `/v10/projects/{PROJECT_ID}/env`
- Daca exista deja: PATCH la `/v9/projects/{PROJECT_ID}/env/{ENV_ID}`

**.env.local (local dev):**
```
MEETING_LINK=https://calendar.app.google/xxxxx
```

### 4. Redeploy

- Render: trigger manual deploy sau push nou cod
- Vercel: redeploy sau push nou cod (env vars se aplica la urmatorul deploy)

## Unde se foloseste link-ul

| Loc | Fisier | Cum |
|-----|--------|-----|
| Email audit (CTA buton) | `backend/src/pipeline.py`, `backend/src/template_processor.py` | `meeting_link=MEETING_LINK` |
| PDF audit (CTA pagina) | `backend/src/pdf_generator.py` | Link in pagina finala |
| Hero section site | `frontend/src/components/sections/HeroSection.tsx` | `process.env.MEETING_LINK` |
| Pagina audit | `frontend/src/app/audit/page.tsx` | `process.env.MEETING_LINK` |
| Config backend | `backend/config.py` | `MEETING_LINK = os.getenv("MEETING_LINK", "")` |

## De retinut

- **Nu costa nimic** - inclus in Google Calendar (si personal si Workspace)
- **Se sincronizeaza automat** cu calendarul real - fara conflict de programari
- **Booking form simplu** - doar name + email, fara campuri extra (mai putine campuri = mai multe rezervari)
- **Link-ul e permanent** - nu se schimba daca modifici disponibilitatea sau durata
- **Reminder automat** - Google trimite reminder clientului inainte de call

## Setup actual (Tourism Audit V2)

- **Cont:** devideviart (Google Workspace)
- **Link:** `https://calendar.app.google/eHH7fDyWcbYNLpk29`
- **Durata:** 30 minute
- **Disponibilitate:** Luni-Vineri, bazata pe calendarul real
- **Data setup:** 2026-03-29
- **Env var:** `MEETING_LINK` setat pe Render, Vercel, .env.local
