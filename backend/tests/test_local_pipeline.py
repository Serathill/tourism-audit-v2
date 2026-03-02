#!/usr/bin/env python3
"""Local pipeline test — generates HTML email + PDF from example audit output.

Usage:
    cd backend
    source .venv/bin/activate
    python tests/test_local_pipeline.py

Outputs:
    /tmp/audit-test-email.html  — Open in browser to preview email
    /tmp/audit-test-report.pdf  — Full PDF report
"""

import sys
import os

# Add backend root to path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import PropertyData
from src.pdf_generator import generate_audit_pdf

# Fake the config imports needed by template_processor
os.environ.setdefault("GOOGLE_API_KEY", "fake-for-local-test")
os.environ.setdefault("MEETING_LINK", "https://cal.com/devidevs/consultatie-gratuita")


def main():
    # Load example audit
    example_path = os.path.join(os.path.dirname(__file__), "example_audit_output.txt")
    with open(example_path, "r", encoding="utf-8") as f:
        raw_audit = f.read()

    print(f"Loaded example audit: {len(raw_audit)} chars")

    # Create test property data
    property_data = PropertyData(
        id="test-uuid-1234",
        owner_name="Ion Popescu",
        owner_email="ion@pensiuneabelvedere.ro",
        property_name="Pensiunea Belvedere",
        property_address="Brașov",
        website_url="https://belvedere-brasov.ro",
        booking_platform_links=["https://booking.com/hotel/ro/pensiunea-belvedere"],
        social_media_links=["https://facebook.com/PensiuneaBelvedere"],
        google_my_business_link="https://maps.google.com/maps/place/Pensiunea+Belvedere+Brasov",
        business_description="Pensiune turistică 3 margarete cu vedere panoramică la munte, 12 camere.",
    )

    # ── Test 1: PDF Generation ───────────────────────────────
    print("\n--- TEST 1: PDF Generation ---")
    try:
        pdf_bytes = generate_audit_pdf(
            raw_audit=raw_audit,
            property_data=property_data,
            meeting_link="https://cal.com/devidevs/consultatie-gratuita",
        )
        pdf_path = "/tmp/audit-test-report.pdf"
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)
        print(f"  PDF generated: {len(pdf_bytes):,} bytes ({len(pdf_bytes)/1024:.1f} KB)")
        print(f"  Saved to: {pdf_path}")
        print("  PASS")
    except Exception as e:
        print(f"  FAIL: {e}")
        import traceback
        traceback.print_exc()

    # ── Test 2: HTML Email (template only, no Gemini call) ───
    print("\n--- TEST 2: HTML Email Template Rendering ---")
    try:
        from src.template_processor import TemplateProcessor

        tp = TemplateProcessor.__new__(TemplateProcessor)
        # Skip __init__ (needs real API key), manually set up Jinja
        from jinja2 import Environment, FileSystemLoader
        tp.jinja_env = Environment(
            loader=FileSystemLoader(
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
            ),
            autoescape=True,
        )

        # Create a mock formatted content (what Gemini would produce)
        mock_formatted = """AUDIT DIGITAL – Pensiunea Belvedere

Legenda status:
- ✅ Bine: Elementul este optimizat și funcționează corespunzător.
- ⚠️ Necesită îmbunătățiri: Elementul există, dar necesită optimizări.
- ❌ Lipsă/absent: Elementul nu există și este recomandată implementarea sa.

1. Evaluarea Prezenței Online și Vizibilității

Profil Digital

- ✅ Prezență generală: Proprietatea are prezență activă pe Booking.com (8.7/10), Google (4.3/5), TripAdvisor (4.0/5), Travelminit (9.1/10) și Pensiuni.info (8.9/10)
- ❌ Instagram: Nu există cont Instagram — 67% din călătorii 25-44 ani folosesc Instagram pentru cercetare cazare
- ❌ Airbnb: Lipsește de pe Airbnb — pierdere de 28% din turiști care caută exclusiv pe Airbnb

Site web

- ⚠️ Existență & funcționalitate: Site activ pe belvedere-brasov.ro, WordPress 6.4.2, dar plugins neactualizate
- ✅ Certificat SSL: HTTPS activ, Let's Encrypt valid până în mai 2026
- ❌ Viteză de încărcare: PageSpeed 38/100 mobil, LCP 4.2s — extrem de lent
- ⚠️ Optimizare mobil: Parțial responsive, header se suprapune pe iPhone SE
- ❌ CTA "Rezervă acum": Nu există buton de rezervare directă — doar telefon
- ❌ Motor de rezervare directă: Lipsește complet — se pierd 40-60% din rezervări

SEO Tehnic

- ⚠️ Title tag: Există dar generic — "Pensiunea Belvedere - Cazare Brașov"
- ❌ Meta descriere: Lipsește complet, Google generează automat din conținut
- ✅ H1: Prezent și corect — "Pensiunea Belvedere"
- ⚠️ Heading-uri H2-H6: Ierarhie incorectă, H3 folosit înainte de H2
- ❌ Alt text imagini: Doar 3 din 47 imagini au alt text (6%)
- ❌ Schema.org: Nu există markup structurat de niciun tip
- ❌ Sitemap.xml: Returnează 404

Vizibilitate Google & SEO Local

- ❌ Poziționare "pensiune brașov": Nu apare în top 50
- ✅ Poziționare brand: #1 pentru "pensiunea belvedere brașov"
- ⚠️ Google Business Profile: 4.3/5 din 89 recenzii, dar profil incomplet, ultimul post acum 7 luni
- ❌ Google Local Pack: Nu apare — concurența cu GMB optimizat domină

Platforme de rezervări

- ✅ Booking.com: 8.7/10 din 312 recenzii, dar doar 28 fotografii și 15% rată de răspuns
- ⚠️ TripAdvisor: 4.0/5 din 67 recenzii, #47 din 89 în Brașov, 8% rată de răspuns
- ✅ Travelminit.ro: 9.1/10 din 45 recenzii — cea mai bună performanță
- ⚠️ Pensiuni.info: 8.9/10, dar fotografii din 2021

2. Conținut, Reputație și Comunitate

Social Media & Conținut

- ⚠️ Facebook: 1,247 followeri, dar inactiv de 4 luni, engagement 1.0% sub benchmark-ul de 2.5%
- ❌ Instagram: Nu există cont — concurența medie are 3,875 followeri
- ❌ TikTok: Nu există prezență
- ⚠️ Fotografii & Video: Mix profesional (30%) și telefon (70%), doar vară, nicio fotografie iarnă/toamnă/primăvară
- ❌ Conținut UGC: Nu se partajează conținut de la oaspeți

Reputație Online & Recenzii

- ⚠️ Total recenzii: 536 recenzii pe toate platformele, 76% pozitive
- ❌ Răspuns la recenzii: 12% rată de răspuns — extrem de scăzut față de media competiției de 65%
- ⚠️ Trend recenzii: Stabil dar stagnant
- ✅ Ce spun oaspeții (pozitiv): Priveliștea (67%), curățenia (54%), micul dejun (41%)
- ⚠️ Ce spun oaspeții (de îmbunătățit): WiFi slab (23%), parcare limitată (18%), izolare fonică (12%)

Comunitate & Forumuri

- ❌ Reddit & forumuri RO: 0 mențiuni pe Reddit, 1 singură mențiune pe forum.pegas.ro din 2023
- ❌ Blog-uri de călătorie: Nu apare în niciun blog de călătorie din top 20 România
- ❌ Grupuri Facebook: 1 singură mențiune în "Pensiuni și Cabane România" (78K membri)
- ❌ Liste "Top X" locale: Nu apare în nicio listă de recomandări

Calitatea Conținutului

- ⚠️ Fotografii (calitate): Mix profesional/amateur, 70% făcute cu telefonul
- ⚠️ Fotografii (cantitate): ~85 total pe toate platformele, doar acoperire de vară
- ⚠️ Descrieri (calitate): Generice, 150 cuvinte pe site vs 300+ la concurență
- ❌ Blog / Conținut marketing: Nu există secțiune de blog

3. Oportunități și Plan de Acțiune

Analiza Competiției

- ⚠️ Casa Wagner: 4.6/5 Google, 9.2/10 Booking, 8,200 followeri Instagram — lider pe zona Brașov
- ⚠️ Pensiunea Casa Crăița: 4.7/5 Google, 9.0/10 Booking, 3,400 followeri Instagram
- ⚠️ Vila Katharina: 4.5/5 Google, 8.9/10 Booking, 2,100 followeri Instagram
- ✅ Avantaj Belvedere: Travelminit 9.1/10 (cel mai mare din setul competitiv)
- ✅ Avantaj Belvedere: Priveliștea panoramică — USP unic menționat în 67% din recenzii

Conformitate & Înregistrare

- ✅ Firmă înregistrată: CUI 28341567, S.C. BELVEDERE TURISM S.R.L.
- ✅ Clasificare turism: 3 margarete (pensiune turistică)
- ⚠️ Autorizație funcționare: Nu s-a putut confirma validitatea pentru anul curent
- ❌ Membru ANTREC: Nu este listat
- ❌ Membru FPTR: Nu este listat
- ⚠️ Consistență date: Adresa diferă ușor între Booking și Google

Scorul Tău Digital

- Prezență Digitală: 7/10
- Website Tehnic: 4/10
- SEO Tehnic: 3/10
- Vizibilitate Google: 5/10
- Platforme Booking: 8/10
- Social Media: 2/10
- Reputație & Recenzii: 7/10
- Conținut & Fotografii: 6/10
- Poziție Competitivă: 5/10
- Comunitate & Forumuri: 1/10
- Conformitate Turism: 6/10
- TOTAL: 54/110 (49%)

Lipsuri (Gaps) Identificate

- ❌ Social media inexistent: Zero strategie social media — fără Instagram (concurența: 3,875 followeri medie), Facebook mort de 4 luni, fără video. 67% din target folosesc Instagram pentru cercetare
- ❌ Rezervări directe imposibile: 100% din cererile directe necesită telefon/email — se pierd 40-60% din potențialii clienți care așteaptă rezervare online instantanee
- ❌ Website critic de lent: PageSpeed 38/100 mobil, LCP 4.2s — 53% din vizitatorii mobil pleacă înainte să se încarce pagina. Concurența medie: 72/100
- ❌ SEO fundamental rupt: Fără meta descrieri, fără Schema.org, fără sitemap, 6% acoperire alt text. Invizibil pe Google pentru cuvinte cheie comerciale
- ❌ Managementul recenziilor abandonat: 12% rată de răspuns vs 65% la concurență. 88% din recenzii rămân fără răspuns

Acțiuni Prioritare

01 Creează profil Instagram Business legat de Facebook, postează primele 15 fotografii cu priveliștea panoramică — diferențiatorul #1 menționat în 67% din recenzii. Target: 500 followeri în prima lună.
02 Răspunde la TOATE recenziile fără răspuns de pe Google (85 recenzii) și Booking.com cu mesaje personalizate. Prioritizează recenziile negative. Target: 100% rată de răspuns sub 48 ore.
03 Actualizează Google Business Profile: adaugă 3 categorii secundare, scrie descriere de 300 cuvinte cu cuvinte cheie, răspunde la cele 3 întrebări Q&A fără răspuns.
04 Comprimă toate imaginile de pe site în format WebP și activează lazy loading. Media de 2.3MB trebuie să scadă sub 100KB. Îmbunătățire PageSpeed estimată: +25-30 puncte.
05 Instalează un widget de rezervare directă (Beds24, Cloudbeds). Proprietățile cu rezervare directă convertesc 40-60% mai multe cereri decât cele doar cu telefon.
06 Creează și trimite sitemap.xml, adaugă meta descrieri la toate paginile, implementează Schema.org LodgingBusiness. Rezultat: indexarea completă în 2-4 săptămâni.
07 Dezvoltă un calendar de conținut: 4 postări Instagram/săptămână, 2 postări Facebook/săptămână, 1 Reel/săptămână cu experiențe oaspeți, priveliști la diferite ore, peisaje sezoniere.
08 Creează listing Airbnb pentru a captura 28% din turiștii care caută exclusiv pe Airbnb. Target: Superhost în 6 luni.

Implementarea acestor acțiuni poate părea complexă, dar nu trebuie să faci totul singur. Soluțiile moderne de automatizare AI pot prelua multe dintre aceste sarcini (social media, răspunsuri la recenzii, optimizare conținut), economisind timp și asigurând consistență. Dacă vrei să discutăm despre un plan personalizat de implementare adaptat bugetului și obiectivelor tale, suntem aici să te ajutăm.
"""

        html_content = tp.generate_html_email(
            formatted_content=mock_formatted, property_data=property_data
        )
        html_path = "/tmp/audit-test-email.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"  HTML email generated: {len(html_content):,} chars")
        print(f"  Saved to: {html_path}")
        print("  PASS")
    except Exception as e:
        print(f"  FAIL: {e}")
        import traceback
        traceback.print_exc()

    # ── Summary ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("LOCAL PIPELINE TEST COMPLETE")
    print("=" * 60)
    print(f"  Open email:  file:///tmp/audit-test-email.html")
    print(f"  Open PDF:    /tmp/audit-test-report.pdf")
    print()
    print("These files simulate what a real client would receive:")
    print("  - Email = summary/teaser (HTML)")
    print("  - PDF   = full detailed report (attachment)")


if __name__ == "__main__":
    main()
