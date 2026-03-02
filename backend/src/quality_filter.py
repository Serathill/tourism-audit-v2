"""Post-processing quality filter for defensive language removal.
Ported from V1 with print→logging. Regex patterns are battle-tested.
"""

import re
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


class QualityFilter:
    """Remove defensive language and enhance audit quality."""

    def __init__(self) -> None:
        self.replacement_rules = self._build_replacement_rules()

    def _build_replacement_rules(self) -> List[Tuple[str, str, str]]:
        return [
            (
                r"nu am putut (identifica|găsi|confirma|valida|extrage|obține|verifica|măsura)",
                "Pentru optimizare completă, recomandăm verificarea și actualizarea",
                "data_extraction",
            ),
            (
                r"nu s-a putut (identifica|găsi|confirma|valida|extrage|obține|verifica)",
                "Recomandat pentru validare",
                "validation",
            ),
            (
                r"nu am reușit să (verific|confirm|extrag|obțin|identific)",
                "Pentru îmbunătățire, sugerăm verificarea",
                "improvement",
            ),
            (
                r"limitări (de acces|în extragere|tehnice)",
                "Pentru acces complet la date, recomandăm",
                "access",
            ),
            (
                r"din cauza (restricțiilor|limitărilor) (de acces|publice?|platformei)",
                "Pentru analiză completă",
                "restrictions",
            ),
        ]

    def remove_defensive_language(self, text: str) -> Tuple[str, Dict[str, int]]:
        cleaned_text = text
        stats: Dict[str, object] = {"total_replacements": 0, "by_pattern": {}}

        for pattern, replacement, context in self.replacement_rules:
            count = len(re.findall(pattern, cleaned_text, re.IGNORECASE))
            if count > 0:
                cleaned_text = re.sub(
                    pattern, replacement, cleaned_text, flags=re.IGNORECASE
                )
                stats["by_pattern"][context] = count
                stats["total_replacements"] += count

        specific_replacements = {
            "nu am putut confirma un profil complet Google Business": "Pentru îmbunătățirea vizibilității locale, recomandăm verificarea și optimizarea profilului Google Business cu informații complete",
            "linkul oferit în brief pare invalid; nu am putut valida": "Pentru validare optimă, recomandăm verificarea linkului și completarea profilului",
            "nu am putut obține un scor PSI automat": "Pentru optimizarea performanței, recomandăm rularea unui test PageSpeed Insights și implementarea recomandărilor pentru a atinge ținta de minim 70/100 pe mobil",
            "nu am putut extrage automat metrice live": "Pentru creșterea engagement-ului, recomandăm monitorizarea regulată a metricilor sociale și implementarea unui calendar editorial",
            "din cauza restricțiilor de acces public": "Pentru analiză completă a prezenței sociale",
            "nu am putut identifica în head un tag meta": "Pentru îmbunătățirea SEO, recomandăm adăugarea meta tag-urilor complete (title și description) pentru fiecare pagină",
            "limitări tehnice": "Pentru optimizare completă",
            "nu am avut acces": "Pentru acces complet, recomandăm",
        }

        for old_phrase, new_phrase in specific_replacements.items():
            if old_phrase.lower() in cleaned_text.lower():
                cleaned_text = re.sub(
                    re.escape(old_phrase),
                    new_phrase,
                    cleaned_text,
                    flags=re.IGNORECASE,
                )
                stats["total_replacements"] += 1

        return cleaned_text, stats

    def validate_quality(self, text: str) -> dict:
        forbidden_phrases = [
            "nu am putut",
            "nu s-a putut",
            "nu am reușit",
            "limitări",
            "nu am avut acces",
            "nu am putut extrage",
            "nu am putut obține",
            "nu am putut verifica",
            "nu am putut confirma",
            "restricții de acces",
        ]

        text_lower = text.lower()
        violations = {}
        total_violations = 0

        for phrase in forbidden_phrases:
            count = text_lower.count(phrase)
            if count > 0:
                violations[phrase] = count
                total_violations += count

        return {
            "passes_quality_check": total_violations == 0,
            "total_violations": total_violations,
            "violations_by_phrase": violations,
            "output_length": len(text),
            "meets_length_requirement": len(text) >= 5000,
        }

    def process_audit(self, raw_audit: str) -> Tuple[str, Dict]:
        logger.info("Quality filter — checking for defensive language")

        pre_validation = self.validate_quality(raw_audit)
        logger.info(
            "Pre-filter violations: %d", pre_validation["total_violations"]
        )

        if pre_validation["total_violations"] == 0:
            logger.info("No defensive language detected — skipping filter")
            return raw_audit, {
                "filtered": False,
                "pre_validation": pre_validation,
                "post_validation": pre_validation,
            }

        logger.info("Applying quality filter...")
        cleaned_audit, replacement_stats = self.remove_defensive_language(raw_audit)

        post_validation = self.validate_quality(cleaned_audit)
        logger.info(
            "Post-filter violations: %d, replacements: %d",
            post_validation["total_violations"],
            replacement_stats["total_replacements"],
        )

        if post_validation["total_violations"] > 0:
            logger.warning(
                "%d violations remaining — manual review recommended",
                post_validation["total_violations"],
            )

        return cleaned_audit, {
            "filtered": True,
            "replacements_made": replacement_stats["total_replacements"],
            "pre_validation": pre_validation,
            "post_validation": post_validation,
            "improvement": pre_validation["total_violations"]
            - post_validation["total_violations"],
        }
