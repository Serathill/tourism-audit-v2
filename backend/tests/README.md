# Testing & Preview Tools

## Email Template Variants

Template-urile de email stau în `templates/variants/`. Fiecare e un fișier HTML Jinja2
care folosește aceleași variabile ca template-ul de producție (`templates/audit_email.html`).

### Variante disponibile
| Varianta | Descriere | Status |
|----------|-----------|--------|
| v0-current-dark-full | Dark theme, tot auditul (versiunea veche) | Archived |
| v1-light-full | Light theme, tot auditul | Reference |
| v2-light-short | Light, doar summary | Reference |
| v3-semafor | Blocuri verde/galben/roșu | Reference |
| v4-scrisoare | 200 cuvinte, text simplu | Reference |
| v5-fisa-medicala | Score card + dots | Reference |
| v6-hibrid-bc | Score bars + findings + acțiuni | Reference |
| v7-dark-short | Dark premium dar scurt | Reference |
| v8-final-mix | Mix validat: v6 score + v1 detalii + v2 bottom | **PRODUCTION** |

### Cum generezi preview-uri
```bash
cd backend

# Generează TOATE variantele cu datele ultimului audit
python3 tests/preview_email.py --all

# Generează pentru o proprietate specifică
python3 tests/preview_email.py --all -p 5e9ebb6f-40be-46d7-8840-78f6093ee4f2

# Doar o variantă specifică
python3 tests/preview_email.py -t v8

# Vezi ce variante ai
python3 tests/preview_email.py --variants

# Vezi ce proprietăți au audituri în DB
python3 tests/preview_email.py --list
```

Output: `tests/previews/index.html` + un HTML per variantă. Deschizi index.html în browser.

### Cum adaugi o variantă nouă
1. Creează `templates/variants/v9-nume.html` (Jinja2 template)
2. Folosește aceleași variabile: `property_name`, `property_data`, `audit_data`, `meeting_link`, `urgency`
3. Rulează `python3 tests/preview_email.py --all` ca să generezi preview
4. Deschide `tests/previews/v9-nume.html` în browser
5. Când e validat, copiază peste `templates/audit_email.html`

### Zero cost Gemini
Preview-urile folosesc datele EXISTENTE din DB (formatted_data). Nu rulează Gemini.
Poți genera 100 de variante fără niciun API call.

---

## Formatter Prompt Versions

Prompt-urile pentru Gemini Formatter stau în `templates/prompts/`. Fiecare e un fișier
text cu placeholdere (`{PROPERTY_NAME}`, `{RAW_AUDIT}`, etc.).

### Variante disponibile
| Versiune | Descriere | Status |
|----------|-----------|--------|
| p0-current | Prompt-ul actual din producție (tehnic, jargon) | **PRODUCTION** |

### Cum testezi un prompt nou
```bash
cd backend

# Vezi ce prompt-uri ai
python3 tests/test_prompt.py

# Testează un prompt (1 Gemini API call, ~$0.02, ~10 sec)
python3 tests/test_prompt.py --prompt p0

# Testează pe o proprietate specifică
python3 tests/test_prompt.py --prompt p1 -i 5e9ebb6f-40be-46d7-8840-78f6093ee4f2

# Compară două output-uri
python3 tests/test_prompt.py --compare p0 p1
```

Output: `tests/prompt-outputs/<prompt>--<property>.txt` + `.html` (email preview cu output-ul generat)

### Cum adaugi un prompt nou
1. Creează `templates/prompts/p1-descriere.txt`
2. Folosește placeholdere: `{PROPERTY_NAME}`, `{PROPERTY_ADDRESS}`, `{WEBSITE_URL}`, `{RAW_AUDIT}`
3. Rulează `python3 tests/test_prompt.py --prompt p1`
4. Compară cu p0: `python3 tests/test_prompt.py --compare p0 p1`
5. Verifică output-ul text + email preview HTML
6. Când e validat, copiază conținutul în `src/template_processor.py` metoda `_build_template_prompt()`

### Cost per test
- **Email preview:** $0 (folosește date existente din DB)
- **Prompt test:** ~$0.02 per run (1 Gemini Formatter call, NU Deep Research)
- **Deep Research:** $0 (nu se rulează niciodată în teste)

---

## Structura fișiere

```
backend/
├── templates/
│   ├── audit_email.html          # PRODUCȚIE - template-ul activ
│   ├── variants/                 # Variante email (v0-v8+)
│   │   ├── v0-current-dark-full.html
│   │   ├── v1-light-full.html
│   │   ├── ...
│   │   └── v8-final-mix.html     # Validat, copiat în audit_email.html
│   └── prompts/                  # Variante prompt Formatter
│       └── p0-current.txt        # Prompt-ul actual din producție
├── tests/
│   ├── README.md                 # Acest fișier
│   ├── preview_email.py          # Generează email previews (zero Gemini cost)
│   ├── test_prompt.py            # Testează prompt versions (1 Gemini call/test)
│   ├── previews/                 # Output email previews (HTML)
│   │   ├── index.html
│   │   └── *.html
│   └── prompt-outputs/           # Output prompt tests (TXT + HTML)
│       └── *.txt, *.html
└── src/
    └── template_processor.py     # Prompt-ul ACTIV de producție (inline)
```

## Workflow

### Schimbare email template:
1. Creează variantă în `templates/variants/`
2. Preview cu `preview_email.py` (zero cost)
3. Iterează vizual
4. Validare de Petru/Alexandru
5. Copiază în `templates/audit_email.html`

### Schimbare Formatter prompt:
1. Creează versiune în `templates/prompts/`
2. Test cu `test_prompt.py` (~$0.02/test)
3. Compară output-uri
4. Verifică că parserul funcționează (email preview se generează OK)
5. Validare de Petru/Alexandru
6. Copiază în `template_processor.py` metoda `_build_template_prompt()`
