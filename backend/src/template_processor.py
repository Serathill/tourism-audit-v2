"""Gemini template processor — formats raw audit into structured HTML email.
Uses google.genai SDK (unified with audit_generator). Stateful parser for sections.
"""

import logging
import re
from datetime import datetime

from google import genai
from google.genai import types
from jinja2 import Environment, FileSystemLoader

from config import GOOGLE_API_KEY, MEETING_LINK, GEMINI_FORMATTER_MODEL
from src.models import PropertyData

logger = logging.getLogger(__name__)


class TemplateProcessingError(Exception):
    pass


class TemplateProcessor:
    """Format raw audit text → structured dict → HTML email."""

    def __init__(self) -> None:
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY must be set.")

        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        logger.info(
            "Gemini formatter initialized — model: %s", GEMINI_FORMATTER_MODEL
        )

        self.jinja_env = Environment(
            loader=FileSystemLoader("templates"), autoescape=True
        )

    # ── Urgency messaging ────────────────────────────────────

    def _generate_urgency_message(self) -> dict:
        """Seasonal urgency messaging based on current month."""
        month = datetime.now().month

        if 1 <= month <= 3:
            return {
                "icon": "⏰",
                "title": "Sezonul de vârf se apropie rapid",
                "message": (
                    "Proprietățile care optimizează prezența online cu 2-3 luni "
                    "înaintea sezonului capturează cu 70% mai multe rezervări "
                    "early-bird. Concurența investește deja în optimizări."
                ),
            }
        elif 4 <= month <= 6:
            return {
                "icon": "🔥",
                "title": "Concurența pentru rezervări estivale este la maxim",
                "message": (
                    "73% din călători fac cercetări active pentru vacanțele de "
                    "vară. Fiecare zi de întârziere în optimizare înseamnă "
                    "vizibilitate pierdută în favoarea concurenței."
                ),
            }
        elif 7 <= month <= 9:
            return {
                "icon": "📈",
                "title": "Sezonul de vârf este în plină desfășurare",
                "message": (
                    "Chiar și în plin sezon, optimizările pot aduce creșteri "
                    "imediate. Proprietățile care răspund rapid la recenzii și "
                    "mențin social media activ văd cu 40% mai multe rezervări "
                    "last-minute."
                ),
            }
        else:
            return {
                "icon": "🎯",
                "title": "Perioada ideală pentru optimizări strategice",
                "message": (
                    "Sezonul off-peak este momentul perfect pentru "
                    "implementarea îmbunătățirilor. Proprietățile care "
                    "pregătesc fundația acum încep sezonul viitor cu avantaj "
                    "competitiv de 3-6 luni."
                ),
            }

    # ── Stateful parser ──────────────────────────────────────

    @staticmethod
    def _parse_item_line(line: str) -> dict:
        """Parse a single bullet-point line into {icon, title, details}."""
        line = line.strip("- ").strip()
        icon = ""
        for status_icon in ("✅", "⚠️", "❌"):
            if status_icon in line:
                icon = status_icon
                line = line.replace(status_icon, "", 1).strip()
                break
        parts = line.split(":", 1)
        title = parts[0].strip()
        details = (
            parts[1].strip().replace("[", "").replace("]", "")
            if len(parts) > 1
            else ""
        )
        return {"icon": icon, "title": title, "details": details}

    def parse_formatted_content_to_dict(self, formatted_content: str) -> dict:
        """Parse AI structured text → Python dict using stateful line-by-line approach.

        Handles the V2 richer format: 3 main sections with many subsections,
        scoring data, gaps, and prioritized actions.
        """
        logger.info("Parsing formatted text into sections...")
        audit_data: dict = {"sections": []}

        try:
            # Case-insensitive split on "Legenda status:" marker
            lower_content = formatted_content.lower()
            marker = "legenda status:"
            marker_pos = lower_content.find(marker)
            if marker_pos == -1:
                raise TemplateProcessingError(
                    "Could not find 'Legenda status:' marker in content."
                )
            content_body = formatted_content[marker_pos + len(marker):]
        except TemplateProcessingError:
            raise
        except Exception:
            raise TemplateProcessingError(
                "Could not find 'Legenda status:' marker in content."
            )

        current_section = None
        current_subsection = None
        parsing_context = None  # 'subsections', 'gaps', 'actions', 'scoring'

        for line in content_body.strip().split("\n"):
            line = line.strip()
            if not line:
                continue

            # Main section title (e.g. "1. Evaluarea..." / "2. Conținut..." / "3. Oportunități...")
            main_section_match = re.match(r"^(1\.|2\.|3\.)\s.*", line)
            if main_section_match:
                title = main_section_match.group(0)
                is_action_plan = "Oportunități" in title or "Plan de Acțiune" in title
                current_section = {
                    "title": title,
                    "is_action_plan": is_action_plan,
                    "subsections": [],
                    "gaps": None,
                    "actions": None,
                }
                audit_data["sections"].append(current_section)
                current_subsection = None
                parsing_context = "subsections"
                continue

            if not current_section:
                continue

            # Section 3 special titles — gaps and actions
            if current_section["is_action_plan"]:
                if "Lipsuri" in line and ("Gaps" in line or "Identificate" in line):
                    current_section["gaps"] = {"title": line, "item_list": []}
                    parsing_context = "gaps"
                    current_subsection = None
                    continue
                if "Acțiuni Prioritare" in line:
                    current_section["actions"] = {
                        "title": line,
                        "item_list": [],
                    }
                    parsing_context = "actions"
                    current_subsection = None
                    continue
                # Scoring data in section 3 — treat as regular subsection
                if "Scorul Tău Digital" in line or "TOTAL:" in line:
                    current_subsection = {"title": line, "item_list": []}
                    current_section["subsections"].append(current_subsection)
                    parsing_context = "subsections"
                    continue

            # Numbered action items (01, 02, etc.)
            action_match = re.match(r"(\d+)\s+(.*)", line)
            if parsing_context == "actions" and action_match:
                num, text = action_match.groups()
                # Stop capturing actions if we hit the closing message
                if text.startswith("Implementarea"):
                    parsing_context = None
                    continue
                current_section["actions"]["item_list"].append(
                    {
                        "number": f"{int(num):02d}",
                        "text_bold": text.strip(),
                        "text_regular": "",
                    }
                )
                continue

            # Bullet point items
            if line.startswith("-"):
                item = self._parse_item_line(line)
                if parsing_context == "gaps":
                    if not current_section["gaps"]:
                        current_section["gaps"] = {
                            "title": "Lipsuri (Gaps) Identificate",
                            "item_list": [],
                        }
                    current_section["gaps"]["item_list"].append(item)
                elif current_subsection:
                    current_subsection["item_list"].append(item)
                continue

            # Skip lines that are part of the closing message after actions
            if parsing_context is None:
                continue

            # Subsection title — any non-bullet, non-empty line in subsections context
            if parsing_context == "subsections":
                current_subsection = {"title": line, "item_list": []}
                current_section["subsections"].append(current_subsection)
                continue

        logger.info(
            "Parsed content into %d sections.", len(audit_data["sections"])
        )
        return audit_data

    # ── Gemini formatting ────────────────────────────────────

    def process_audit_content(
        self, raw_audit: str, property_data: PropertyData
    ) -> str:
        """Use Gemini to format raw audit into structured Romanian template."""
        logger.info(
            "Formatting audit for '%s' with Gemini %s",
            property_data.property_name,
            GEMINI_FORMATTER_MODEL,
        )

        prompt = self._build_template_prompt(raw_audit, property_data)

        system_instruction = (
            "You are a formatting expert. Your only task is to transform "
            "raw text into the structured Romanian template provided. "
            "Follow the structure, headings, and status icons exactly. "
            "Do not add any extra text, explanations, or markdown code blocks."
        )

        try:
            response = self.client.models.generate_content(
                model=GEMINI_FORMATTER_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    max_output_tokens=16000,
                    temperature=0.1,
                ),
            )

            formatted_content = response.text.strip() if response.text else ""

            if not formatted_content:
                raise TemplateProcessingError(
                    "Gemini returned empty content for formatted audit."
                )

            self._validate_formatted_content(formatted_content)
            logger.info("Template processing complete.")
            return formatted_content

        except TemplateProcessingError:
            raise
        except Exception as e:
            logger.error("Gemini template processing failed: %s", e)
            raise TemplateProcessingError(
                f"Failed to process audit template with Gemini: {e}"
            )

    # ── HTML email generation ────────────────────────────────

    def generate_html_email(
        self, formatted_content: str, property_data: PropertyData
    ) -> str:
        """Parse formatted content → render Jinja2 HTML email."""
        logger.info("Generating HTML email...")
        audit_data_dict = self.parse_formatted_content_to_dict(formatted_content)
        urgency_data = self._generate_urgency_message()
        template = self.jinja_env.get_template("audit_email.html")

        return template.render(
            property_name=property_data.property_name,
            audit_data=audit_data_dict,
            property_data=property_data,
            meeting_link=MEETING_LINK,
            urgency=urgency_data,
        )

    # ── Template prompt ──────────────────────────────────────

    def _build_template_prompt(
        self, raw_audit: str, property_data: PropertyData
    ) -> str:
        return f"""
=== YOUR MISSION ===
You are an EXPERT in digital marketing for Romanian accommodation businesses with 10+ years of SEO and social media audit experience. Transform the RAW AUDIT below into a structured Romanian report following the EXACT template structure.

=== PRECISE TASK ===
Analyze the RAW AUDIT and transform it into the structured Romanian template below. Follow the structure strictly, but analyze intelligently to assign the correct status icons based on the audit data.

=== GOLDEN RULES (MANDATORY) ===

STATUS ICONS — How to decide:
✅ GOOD = Audit shows the element works EXCELLENTLY, no major issues
⚠️ NEEDS IMPROVEMENT = Element EXISTS but has concrete problems or limitations
❌ MISSING/ABSENT = Element DOES NOT EXIST at all or is completely non-functional

EXACT FORMATTING:
- Each bullet line: "- [ICON] TITLE: Short, concrete explanation based on audit data"
- Actions: "01 Specific action with period."
- NO extra text, NO explanations outside the structure

INTELLIGENT FLEXIBILITY:
- FOLLOW the section/subsection structure (MANDATORY)
- INCLUDE the base elements specified (MANDATORY)
- ADD any additional information found in the audit (RECOMMENDED)
- If the audit has more details — INCLUDE THEM
- If the audit doesn't mention something — MARK as ❌ with explanation
- INCLUDE scores (X/10) from the audit for each subsection when available
- INCLUDE competitor comparison data when found in the audit
- INCLUDE review quotes when found in the audit
- INCLUDE community/forum findings when found in the audit
- INCLUDE business registry findings when found in the audit

=== MANDATORY STRUCTURE ===

AUDIT DIGITAL - {property_data.property_name}

Legenda status:
- ✅ Bine: Elementul este optimizat și funcționează corespunzător.
- ⚠️ Necesită îmbunătățiri: Elementul există, dar necesită optimizări.
- ❌ Lipsă/absent: Elementul nu există și este recomandată implementarea sa.

1. Evaluarea Prezenței Online și Vizibilității

Profil Digital

- [DECIDE ✅/⚠️/❌] Prezență generală: [Summarize all digital touchpoints found]
[ADD lines for each platform discovered with its status and key metric]

Site web

- [DECIDE ✅/⚠️/❌] Existență & funcționalitate: [Details from audit]
- [DECIDE ✅/⚠️/❌] Certificat SSL: [HTTPS status from audit]
- [DECIDE ✅/⚠️/❌] Viteză de încărcare (PageSpeed): [Numeric score from audit]
- [DECIDE ✅/⚠️/❌] Optimizare mobil (responsive): [Mobile-specific findings]
- [DECIDE ✅/⚠️/❌] CTA "Rezervă acum": [Visibility and effectiveness]
- [DECIDE ✅/⚠️/❌] Structură URL & navigație: [Clean URLs, navigation clarity]
- [DECIDE ✅/⚠️/❌] Motor de rezervare directă: [Direct booking vs OTA redirect]
[ADD any other technical issues from audit — hosting, performance, etc.]

SEO Tehnic

- [DECIDE ✅/⚠️/❌] Title tag & meta descriere: [Exact tags found or missing]
- [DECIDE ✅/⚠️/❌] Heading-uri (H1, H2 etc.): [Hierarchy assessment]
- [DECIDE ✅/⚠️/❌] Alt text imagini: [X din Y imagini au alt text - percentage]
- [DECIDE ✅/⚠️/❌] Schema.org (date structurate): [Type found or missing]
- [DECIDE ✅/⚠️/❌] Sitemap.xml: [Found or missing]
- [DECIDE ✅/⚠️/❌] Multilingual: [Languages available]

Vizibilitate Google & SEO Local

- [DECIDE ✅/⚠️/❌] Poziționare "cazare [tip] [localitate]": [Position from audit]
- [DECIDE ✅/⚠️/❌] Poziționare brand name: [What appears when searching property name]
- [DECIDE ✅/⚠️/❌] Google Business Profile: [Rating X.X/5, N recenzii, completeness]
- [DECIDE ✅/⚠️/❌] Google Local Pack / Hotel Pack: [Appears or not]
[ADD GMB specific details — photos count, categories, recent posts]

Platforme de rezervări

- [DECIDE ✅/⚠️/❌] Booking.com: [Rating X.X/10, N recenzii, photos, badges]
- [DECIDE ✅/⚠️/❌] TripAdvisor: [Rating X.X/5, N recenzii, ranking #X in area]
- [DECIDE ✅/⚠️/❌] Airbnb: [Rating X.X/5, Superhost status]
[ADD any other platforms found — Pensiuni.info, Travelminit, etc.]

2. Conținut, Reputație și Comunitate

Social Media & Conținut

- [DECIDE ✅/⚠️/❌] Facebook: [Followers, posting frequency, engagement rate]
- [DECIDE ✅/⚠️/❌] Instagram: [Followers, posts, Reels, Stories, engagement rate]
- [DECIDE ✅/⚠️/❌] TikTok: [Found or missing]
- [DECIDE ✅/⚠️/❌] Fotografii & Video: [Quality assessment - professional/amateur]
- [DECIDE ✅/⚠️/❌] Conținut UGC (de la oaspeți): [Found or missing]
[ADD any other social platforms found — YouTube, etc.]

Reputație Online & Recenzii

- [DECIDE ✅/⚠️/❌] Total recenzii: [N total across all platforms, aggregate rating]
- [DECIDE ✅/⚠️/❌] Răspuns la recenzii: [Response rate XX%, tone assessment]
- [DECIDE ✅/⚠️/❌] Trend recenzii: [Improving / Stable / Declining]
- [DECIDE ✅/⚠️/❌] Ce spun oaspeții (pozitiv): [Top 3 positive themes with quotes]
- [DECIDE ✅/⚠️/❌] Ce spun oaspeții (de îmbunătățit): [Top 3 negative themes with quotes]

Comunitate & Forumuri

- [DECIDE ✅/⚠️/❌] Reddit & forumuri RO: [Mentions found or absent]
- [DECIDE ✅/⚠️/❌] Blog-uri de călătorie: [Featured in X blogs or not found]
- [DECIDE ✅/⚠️/❌] Grupuri Facebook: [Mentioned/recommended or absent]
- [DECIDE ✅/⚠️/❌] Liste "Top X" locale: [Appears in X lists or absent]

Calitatea Conținutului

- [DECIDE ✅/⚠️/❌] Fotografii (calitate): [Professional / Amateur / Phone]
- [DECIDE ✅/⚠️/❌] Fotografii (cantitate): [N total, seasonal coverage]
- [DECIDE ✅/⚠️/❌] Descrieri (calitate): [Compelling / Generic / Minimal]
- [DECIDE ✅/⚠️/❌] Blog / Conținut marketing: [Active / Inactive / Missing]

3. Oportunități și Plan de Acțiune

Analiza Competiției

[INCLUDE competitor comparison data from audit — top 3-5 competitors with their ratings, review counts, social media]
- [ICON] [Competitor name]: [Key metrics and how they compare]
[INCLUDE "Unde ești mai bine" and "Unde poți îmbunătăți" from audit]

Conformitate & Înregistrare

- [DECIDE ✅/⚠️/❌] Firmă înregistrată: [Registration status, CUI if found]
- [DECIDE ✅/⚠️/❌] Clasificare turism: [Margarete/stele or not found]
- [DECIDE ✅/⚠️/❌] Membru ANTREC/FPTR: [Found or not]
- [DECIDE ✅/⚠️/❌] Consistență date: [Cross-reference findings]

Scorul Tău Digital

[INCLUDE the 11-category scoring table from audit]
- Prezență Digitală: X/10
- Website Tehnic: X/10
- SEO Tehnic: X/10
- Vizibilitate Google: X/10
- Platforme Booking: X/10
- Social Media: X/10
- Reputație & Recenzii: X/10
- Conținut & Fotografii: X/10
- Poziție Competitivă: X/10
- Comunitate & Forumuri: X/10
- Conformitate Turism: X/10
- TOTAL: XX/110 (XX%)

Lipsuri (Gaps) Identificate

[GENERATE 3-5 MAJOR PROBLEMS from audit with COMPETITIVE CONTEXT]

- [ICON] [Problem area]: [Specific problem] + [Competitive context with percentages]
- [ICON] [Problem area]: [Specific problem] + [Competitive context]
- [ICON] [Problem area]: [Specific problem] + [Competitive context]
- [ICON] [Problem area]: [Specific problem] + [Competitive context]
- [ICON] [Problem area]: [Specific problem] + [Competitive context]

Acțiuni Prioritare

[GENERATE 8-10 SPECIFIC ACTIONS organized by timeframe]

01 [Immediate action — this week, with impact estimate].
02 [Immediate action — this week, with impact estimate].
03 [Immediate action — this week, with impact estimate].
04 [Short-term action — this month, with impact estimate].
05 [Short-term action — this month, with impact estimate].
06 [Short-term action — this month, with impact estimate].
07 [Strategic action — next 3 months, with impact estimate].
08 [Strategic action — next 3 months, with impact estimate].

Implementarea acestor acțiuni poate părea complexă, dar nu trebuie să faci totul singur. Dacă vrei să discutăm despre un plan personalizat de implementare adaptat bugetului și obiectivelor tale, suntem aici să te ajutăm.

=== DECISION EXAMPLES ===

BAD: "- ✅ Facebook: Active presence" (when audit says they haven't posted in months)
GOOD: "- ❌ Facebook: Nu există postări recente, cont inactiv de 6+ luni"

BAD: "- ❌ Website: Not working" (when audit says it exists but is slow)
GOOD: "- ⚠️ Website: Funcționează dar PageSpeed mobil este 35/100, sub media de 70/100"

=== RAW AUDIT TO ANALYZE ===
```
{raw_audit}
```

=== PROPERTY DATA ===
Name: {property_data.property_name}
County: {property_data.property_address}
Website: {property_data.website_url or "Not available"}

=== YOUR RESPONSE (ONLY THE STRUCTURED TEXT, NO MARKDOWN CODE BLOCKS) ===
"""

    def _validate_formatted_content(self, content: str) -> None:
        required = [
            "AUDIT DIGITAL",
            "Legenda status",
            "1.",
            "2.",
            "3.",
            "Acțiuni Prioritare",
        ]
        if any(s not in content for s in required):
            raise TemplateProcessingError(
                f"Formatted audit is missing required sections. "
                f"Content:\n{content[:500]}"
            )
        logger.info("Formatted audit content validation passed.")
