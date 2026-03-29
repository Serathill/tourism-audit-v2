"""Tests for quality_filter.py — regex patterns for defensive language removal."""

import pytest
from src.quality_filter import QualityFilter


@pytest.fixture
def qf():
    return QualityFilter()


class TestRemoveDefensiveLanguage:
    def test_removes_nu_am_putut_verifica(self, qf):
        text = "Nu am putut verifica profilul Google Business."
        cleaned, stats = qf.remove_defensive_language(text)
        assert "nu am putut" not in cleaned.lower()
        assert stats["total_replacements"] > 0

    def test_removes_nu_sa_putut(self, qf):
        text = "Nu s-a putut identifica pagina de Facebook."
        cleaned, stats = qf.remove_defensive_language(text)
        assert "nu s-a putut" not in cleaned.lower()

    def test_removes_nu_am_reusit(self, qf):
        text = "Nu am reușit să extrag datele de contact."
        cleaned, stats = qf.remove_defensive_language(text)
        assert "nu am reușit" not in cleaned.lower()

    def test_removes_limitari(self, qf):
        text = "Din cauza limitări de acces, nu am putut analiza."
        cleaned, stats = qf.remove_defensive_language(text)
        assert "limitări de acces" not in cleaned.lower()

    def test_removes_specific_pagespeed(self, qf):
        text = "nu am putut obține un scor PSI automat"
        cleaned, stats = qf.remove_defensive_language(text)
        assert "nu am putut" not in cleaned.lower()
        assert stats["total_replacements"] > 0

    def test_clean_text_unchanged(self, qf):
        text = "Site-ul are un scor PageSpeed de 85/100 pe mobil."
        cleaned, stats = qf.remove_defensive_language(text)
        assert cleaned == text
        assert stats["total_replacements"] == 0

    def test_case_insensitive(self, qf):
        text = "NU AM PUTUT VERIFICA profilul."
        cleaned, stats = qf.remove_defensive_language(text)
        assert "nu am putut" not in cleaned.lower()


class TestValidateQuality:
    def test_clean_text_passes(self, qf):
        text = "Site-ul are performante bune." * 500  # >5000 chars
        result = qf.validate_quality(text)
        assert result["passes_quality_check"] is True
        assert result["total_violations"] == 0

    def test_defensive_text_fails(self, qf):
        text = "Nu am putut verifica acest lucru. Limitări de acces."
        result = qf.validate_quality(text)
        assert result["passes_quality_check"] is False
        assert result["total_violations"] >= 2

    def test_length_requirement(self, qf):
        short_text = "Text scurt."
        result = qf.validate_quality(short_text)
        assert result["meets_length_requirement"] is False

        long_text = "A" * 5001
        result = qf.validate_quality(long_text)
        assert result["meets_length_requirement"] is True


class TestProcessAudit:
    def test_clean_audit_skips_filter(self, qf):
        text = "Site-ul este bine optimizat. " * 200
        cleaned, report = qf.process_audit(text)
        assert report["filtered"] is False
        assert cleaned == text

    def test_dirty_audit_filters(self, qf):
        text = "Nu am putut verifica profilul. " * 100
        cleaned, report = qf.process_audit(text)
        assert report["filtered"] is True
        assert report["replacements_made"] > 0
        assert "nu am putut" not in cleaned.lower()
