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

        Supports both p0 (score at end) and p1 (score/gaps/actions before detail sections).
        """
        logger.info("Parsing formatted text into sections...")

        # Strip markdown code fences if Gemini wraps output
        formatted_content = re.sub(r"^```\w*\n?", "", formatted_content)
        formatted_content = re.sub(r"\n?```$", "", formatted_content)

        audit_data: dict = {
            "sections": [],
            "score_summary": None,   # p1: score card at top
            "top_gaps": None,        # p1: gaps before detail sections
            "actions": None,         # p1: actions before detail sections
        }

        try:
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
        parsing_context = None  # 'subsections', 'gaps', 'actions', 'scoring', 'top_score', 'top_gaps', 'top_actions'

        for line in content_body.strip().split("\n"):
            line = line.strip()
            if not line:
                continue

            # Skip legend items, dividers, and decorative lines
            if line.startswith("- ✅ Bine") or line.startswith("- ⚠️ De") or line.startswith("- ❌ Lipsă") or line.startswith("- ✅ Bine") or line.startswith("- ⚠️ Necesită") or line.startswith("- ❌ Lipsă/absent"):
                continue
            if line.startswith("---"):
                continue

            # ── p1: Score summary at top (before any numbered section) ──
            if "Scorul Tău Digital" in line and not current_section:
                audit_data["score_summary"] = {"title": line, "interpretation": "", "scores": [], "total": ""}
                parsing_context = "top_score"
                continue

            if parsing_context == "top_score":
                # Score lines with dots alignment: "Prezență Digitală .......... 7/10"
                if "....." in line:
                    clean = re.sub(r"\.{3,}", ":", line).strip("- ").strip()
                    parts = clean.split(":", 1)
                    title = parts[0].strip()
                    score = parts[1].strip() if len(parts) > 1 else ""
                    priority = "← prioritate" in line
                    score = score.replace("← prioritate", "").strip()
                    audit_data["score_summary"]["scores"].append(
                        {"title": title, "score": score, "priority": priority}
                    )
                    continue
                if line.startswith("- TOTAL:") or line.startswith("TOTAL:"):
                    audit_data["score_summary"]["total"] = line.replace("- ", "").strip()
                    continue
                # Score lines without dots (p0 format): "- Prezență Digitală: X/10"
                if line.startswith("-") and "/" in line and any(cat in line for cat in ["Prezență", "Website", "SEO", "Vizibilitate", "Platforme", "Social", "Reputație", "Conținut", "Poziție", "Comunitate", "Conformitate"]):
                    item = self._parse_item_line(line)
                    audit_data["score_summary"]["scores"].append(
                        {"title": item["title"], "score": item["details"], "priority": False}
                    )
                    continue
                # Interpretation sentence (not a bullet, not a score)
                if not line.startswith("-") and "/" not in line and "Ce Te Cost" not in line and not re.match(r"^(1\.|2\.|3\.)\s", line):
                    audit_data["score_summary"]["interpretation"] = line
                    continue
                # Fall through if we hit something else — don't continue, let it be caught below

            # ── p1: Top gaps ("Ce Te Costă Cel Mai Mult") before sections ──
            if ("Ce Te Cost" in line or ("Lipsuri" in line and ("Gaps" in line or "Identificate" in line))) and not current_section:
                audit_data["top_gaps"] = {"title": line, "item_list": []}
                parsing_context = "top_gaps"
                continue

            if parsing_context == "top_gaps":
                if line.startswith("-"):
                    item = self._parse_item_line(line)
                    audit_data["top_gaps"]["item_list"].append(item)
                    continue
                # Non-bullet line means we left gaps section — fall through

            # ── p1: Top actions before detail sections ──
            if "Acțiuni Prioritare" in line and not current_section:
                audit_data["actions"] = {"title": line, "item_list": []}
                parsing_context = "top_actions"
                continue

            if parsing_context == "top_actions":
                # Timeframe headers — skip them (visual only)
                if line in ("Săptămâna Aceasta (impact imediat)", "Luna Aceasta", "Următoarele 3 Luni") or re.match(r"^(Săptămâna|Luna|Următoarele)\b", line):
                    continue
                # Numbered action items: "01." or "01 "
                action_match = re.match(r"(\d+)\.?\s+(.*)", line)
                if action_match:
                    num, text = action_match.groups()
                    # Closing message — stop actions
                    if text.startswith("Primele") or text.startswith("Implementarea"):
                        parsing_context = None
                        continue
                    audit_data["actions"]["item_list"].append(
                        {
                            "number": f"{int(num):02d}",
                            "text_bold": text.strip(),
                            "text_regular": "",
                        }
                    )
                    continue
                # Closing message without number
                if line.startswith("Primele") or line.startswith("Implementarea"):
                    parsing_context = None
                    continue
                # Non-action, non-timeframe line — fall through

            # ── Main section titles (1. / 2. / 3.) ──
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

            # ── Section 3 special titles (gaps/actions/scoring inside section 3) ──
            if current_section["is_action_plan"]:
                if "Lipsuri" in line and ("Gaps" in line or "Identificate" in line):
                    current_section["gaps"] = {"title": line, "item_list": []}
                    parsing_context = "gaps"
                    current_subsection = None
                    continue
                if "Ce Te Cost" in line:
                    current_section["gaps"] = {"title": line, "item_list": []}
                    parsing_context = "gaps"
                    current_subsection = None
                    continue
                if "Acțiuni Prioritare" in line:
                    current_section["actions"] = {"title": line, "item_list": []}
                    parsing_context = "actions"
                    current_subsection = None
                    continue
                if "Scorul Tău Digital" in line or "TOTAL:" in line:
                    current_subsection = {"title": line, "item_list": []}
                    current_section["subsections"].append(current_subsection)
                    parsing_context = "subsections"
                    continue

            # ── Numbered action items (01, 02, etc.) ──
            action_match = re.match(r"(\d+)\.?\s+(.*)", line)
            if parsing_context == "actions" and action_match:
                num, text = action_match.groups()
                if text.startswith("Implementarea") or text.startswith("Primele"):
                    parsing_context = None
                    continue
                # Skip timeframe headers that start with a number by accident
                if int(num) > 20:
                    continue
                current_section["actions"]["item_list"].append(
                    {
                        "number": f"{int(num):02d}",
                        "text_bold": text.strip(),
                        "text_regular": "",
                    }
                )
                continue

            # Skip timeframe headers in actions context
            if parsing_context == "actions" and re.match(r"^(Săptămâna|Luna|Următoarele)\b", line):
                continue

            # ── Bullet point items ──
            if line.startswith("-"):
                item = self._parse_item_line(line)
                if parsing_context == "gaps":
                    if not current_section["gaps"]:
                        current_section["gaps"] = {"title": "Lipsuri (Gaps) Identificate", "item_list": []}
                    current_section["gaps"]["item_list"].append(item)
                elif current_subsection:
                    current_subsection["item_list"].append(item)
                continue

            # ── Review quote lines (♥ / △) — treat as items in current subsection ──
            if line.startswith("♥") or line.startswith("△"):
                parts = line.lstrip("♥△ ").split(":", 1)
                title = parts[0].strip()
                details = parts[1].strip().strip('"') if len(parts) > 1 else ""
                icon = "♥" if line.startswith("♥") else "△"
                item = {"icon": icon, "title": title, "details": details}
                if current_subsection:
                    current_subsection["item_list"].append(item)
                continue

            # Skip lines that are part of the closing message after actions
            if parsing_context is None:
                continue

            # ── Skip verdict/intro lines that aren't subsection titles ──
            # "Ce faci bine:", "Ce spun oaspeții", single-sentence verdicts
            if line.startswith("Ce faci bine"):
                # Store as metadata on current section if desired, but skip as subsection
                continue
            if line.startswith("Ce spun oaspeți"):
                # Next lines will be ♥ items, keep current subsection
                continue
            if line.startswith("Ce vor oaspeți"):
                # Next lines will be △ items, keep current subsection
                continue

            # Score lines with dots in detail sections
            if "....." in line and parsing_context == "subsections":
                clean = re.sub(r"\.{3,}", ":", line).strip("- ").strip()
                parts = clean.split(":", 1)
                title = parts[0].strip()
                score = parts[1].strip().replace("← prioritate", "").strip() if len(parts) > 1 else ""
                item = {"icon": "", "title": title, "details": score}
                if current_subsection:
                    current_subsection["item_list"].append(item)
                continue

            # ── Subsection title vs verdict line ──
            if parsing_context == "subsections":
                # Known subsection titles (from p0 and p1 template)
                known_subsections = (
                    "Profil Digital", "Site web", "SEO Tehnic", "Vizibilitate Google",
                    "Platforme de rezerv", "Social Media", "Reputație Online",
                    "Comunitate & Forumuri", "Calitatea Conținut", "Analiza Competi",
                    "Conformitate", "Scorul Tău", "Ce Ai Tu", "Poziția Ta",
                    "Avantajele tale", "Unde pierzi",
                )
                is_known = any(line.startswith(k) or k in line for k in known_subsections)
                if is_known:
                    current_subsection = {"title": line, "item_list": []}
                    current_section["subsections"].append(current_subsection)
                else:
                    # Verdict/intro line — store as description on current subsection, don't create new one
                    if current_subsection and not current_subsection.get("description"):
                        current_subsection["description"] = line
                    # If no current subsection, skip
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
        # Load prompt from templates/prompts/p1-layered.txt
        import os
        prompt_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "templates", "prompts", "p1-layered.txt",
        )
        with open(prompt_path, encoding="utf-8") as f:
            template = f.read()

        return template.replace(
            "{PROPERTY_NAME}", property_data.property_name
        ).replace(
            "{PROPERTY_ADDRESS}", property_data.property_address or ""
        ).replace(
            "{WEBSITE_URL}", property_data.website_url or "Not available"
        ).replace(
            "{RAW_AUDIT}", raw_audit
        )

    def _validate_formatted_content(self, content: str) -> None:
        required = [
            "AUDIT DIGITAL",
            "Legenda status",
            "1.",
            "2.",
            "3.",
            "Acțiuni Prioritare",
        ]
        missing = [s for s in required if s not in content]
        if missing:
            raise TemplateProcessingError(
                f"Formatted audit is missing required sections: {missing}. "
                f"Content:\n{content[:500]}"
            )
        logger.info("Formatted audit content validation passed.")
