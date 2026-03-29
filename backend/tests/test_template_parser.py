"""Tests for template_processor.py — stateful parser and content validation."""

import os
os.environ.setdefault("GOOGLE_API_KEY", "test-key-for-parser")

import pytest
from unittest.mock import patch
from src.template_processor import TemplateProcessor, TemplateProcessingError
import config


@pytest.fixture
def tp():
    with patch("src.template_processor.GOOGLE_API_KEY", "test-key-for-parser"):
        return TemplateProcessor()


VALID_FORMATTED = """AUDIT DIGITAL - Pensiunea Test

Legenda status:
- ✅ Bine: Elementul este optimizat.
- ⚠️ Necesita imbunatatiri: Elementul exista dar necesita optimizari.
- ❌ Lipsa/absent: Elementul nu exista.

1. Evaluarea Prezentei Online si Vizibilitatii

Profil Digital

- ✅ Prezenta generala: Site activ, Facebook, Booking.com
- ⚠️ TripAdvisor: Profil existent dar neoptimizat

Site web

- ✅ Existenta & functionalitate: Site functional pe WordPress
- ⚠️ Viteza de incarcare: PageSpeed mobil 45/100

2. Continut, Reputatie si Comunitate

Social Media & Continut

- ✅ Facebook: 1200 followers, 2 postari/saptamana
- ❌ Instagram: Nu exista profil

Reputatie Online & Recenzii

- ✅ Total recenzii: 87 recenzii, rating mediu 8.9/10

3. Oportunități și Plan de Acțiune

Scorul Tau Digital

- Prezenta Digitala: 7/10
- Website Tehnic: 5/10
- TOTAL: 62/110 (56%)

Lipsuri (Gaps) Identificate

- ❌ Instagram: Lipsa completa
- ⚠️ SEO: Meta descriptions lipsesc

Acțiuni Prioritare

01 Creaza profil Instagram cu fotografii profesionale.
02 Adauga meta descriptions pe toate paginile site-ului.
03 Optimizeaza PageSpeed mobil sub 70/100.

Implementarea acestor actiuni poate parea complexa, dar nu trebuie sa faci totul singur.
"""


class TestParseFormattedContent:
    def test_parses_3_sections(self, tp):
        result = tp.parse_formatted_content_to_dict(VALID_FORMATTED)
        assert len(result["sections"]) == 3

    def test_section_titles(self, tp):
        result = tp.parse_formatted_content_to_dict(VALID_FORMATTED)
        assert "Evaluarea" in result["sections"][0]["title"]
        assert "Continut" in result["sections"][1]["title"]
        assert "Oportunități" in result["sections"][2]["title"]

    def test_section3_is_action_plan(self, tp):
        result = tp.parse_formatted_content_to_dict(VALID_FORMATTED)
        assert result["sections"][2]["is_action_plan"] is True
        assert result["sections"][0]["is_action_plan"] is False

    def test_subsections_parsed(self, tp):
        result = tp.parse_formatted_content_to_dict(VALID_FORMATTED)
        section1 = result["sections"][0]
        assert len(section1["subsections"]) >= 2

    def test_items_have_icons(self, tp):
        result = tp.parse_formatted_content_to_dict(VALID_FORMATTED)
        items = result["sections"][0]["subsections"][0]["item_list"]
        assert any(item["icon"] == "✅" for item in items)

    def test_gaps_parsed(self, tp):
        result = tp.parse_formatted_content_to_dict(VALID_FORMATTED)
        section3 = result["sections"][2]
        assert section3["gaps"] is not None
        assert len(section3["gaps"]["item_list"]) >= 1

    def test_actions_parsed(self, tp):
        result = tp.parse_formatted_content_to_dict(VALID_FORMATTED)
        section3 = result["sections"][2]
        assert section3["actions"] is not None
        assert len(section3["actions"]["item_list"]) >= 2
        assert section3["actions"]["item_list"][0]["number"] == "01"

    def test_case_insensitive_legenda(self, tp):
        """Bug fix 3.7 — parser should handle 'Legenda Status:' with capital S."""
        content = VALID_FORMATTED.replace("Legenda status:", "Legenda Status:")
        result = tp.parse_formatted_content_to_dict(content)
        assert len(result["sections"]) == 3


class TestValidateFormattedContent:
    def test_valid_content_passes(self, tp):
        tp._validate_formatted_content(VALID_FORMATTED)

    def test_missing_sections_fails(self, tp):
        bad_content = "Some random text without structure."
        with pytest.raises(TemplateProcessingError):
            tp._validate_formatted_content(bad_content)

    def test_missing_legenda_fails(self, tp):
        bad_content = "AUDIT DIGITAL - Test\n1.\n2.\n3.\nAcțiuni Prioritare"
        with pytest.raises(TemplateProcessingError):
            tp._validate_formatted_content(bad_content)


class TestParseItemLine:
    def test_with_check_icon(self):
        result = TemplateProcessor._parse_item_line("- ✅ Facebook: 1200 followers")
        assert result["icon"] == "✅"
        assert result["title"] == "Facebook"
        assert "1200" in result["details"]

    def test_with_warning_icon(self):
        result = TemplateProcessor._parse_item_line("- ⚠️ TripAdvisor: Neoptimizat")
        assert result["icon"] == "⚠️"

    def test_with_missing_icon(self):
        result = TemplateProcessor._parse_item_line("- ❌ Instagram: Nu exista")
        assert result["icon"] == "❌"

    def test_no_icon(self):
        result = TemplateProcessor._parse_item_line("- Prezenta Digitala: 7/10")
        assert result["icon"] == ""
        assert result["title"] == "Prezenta Digitala"
