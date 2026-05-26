"""Tests for Argentine Spanish NLP quality."""

import pytest
from app.nlp.argentine_spanish import (
    check_response_quality,
    is_argentine_term,
    get_preferred_term,
    enrich_with_argentinisms,
    ARGENTINE_TERMS,
    AVOID_TERMS,
)
from app.nlp.empathy import detect_emotion, get_empathetic_prefix, adjust_tone
from app.nlp.formality import detect_formality, get_formality_guidance


class TestArgentineSpanish:
    def test_depto_is_argentine(self):
        assert is_argentine_term("depto")

    def test_depa_is_argentine(self):
        assert is_argentine_term("depa")

    def test_apartamento_is_not_argentine(self):
        assert not is_argentine_term("apartamento")

    def test_get_preferred_term(self):
        assert get_preferred_term("depto") == "departamento"

    def test_check_quality_clean(self):
        issues = check_response_quality("Busco un depto en alquiler por Centro")
        assert issues["foreign_terms"] == []

    def test_check_quality_foreign(self):
        issues = check_response_quality("Busco un apartamento en renta")
        assert len(issues["foreign_terms"]) >= 1

    def test_check_quality_tuteo(self):
        issues = check_response_quality("¿Tú querés alquilar?")
        assert issues["score"] <= 8  # Tuteo penalized (10 - 2 = 8)

    def test_enrich_with_argentinisms(self):
        text = "Busco un apartamento en renta"
        result = enrich_with_argentinisms(text)
        assert "apartamento" not in result
        assert "departamento" in result

    def test_vocabulary_has_all_categories(self):
        assert "departamento" in ARGENTINE_TERMS
        assert "alquiler" in ARGENTINE_TERMS
        assert "dormitorios" in ARGENTINE_TERMS
        assert "lucas" in ARGENTINE_TERMS

    def test_avoid_terms_list(self):
        assert "apartamento" in AVOID_TERMS
        assert "renta" in AVOID_TERMS


class TestEmpathy:
    def test_detect_frustration(self):
        emotion = detect_emotion("ya te dije tres veces que busco en centro")
        assert emotion.primary == "frustrated"
        assert emotion.intensity > 0

    def test_detect_excited(self):
        emotion = detect_emotion("genial, me encanta ese depto")
        assert emotion.primary == "excited"

    def test_detect_uncertain(self):
        emotion = detect_emotion("no sé, no estoy seguro si me conviene")
        assert emotion.primary == "uncertain"

    def test_detect_rushed(self):
        emotion = detect_emotion("necesito algo urgente ya")
        assert emotion.primary == "rushed"

    def test_detect_neutral(self):
        emotion = detect_emotion("busco departamento en alquiler")
        assert emotion.primary == "neutral"

    def test_empathetic_prefix_frustrated(self):
        prefix = get_empathetic_prefix("ya te dije que no")
        assert "Entiendo" in prefix or "Disculp" in prefix

    def test_adjust_tone_frustrated(self):
        emotion = detect_emotion("ya te dije tres veces")
        result = adjust_tone("Buscá en Centro.", emotion)
        assert "Entiendo" in result or "Disculp" in result


class TestFormality:
    def test_detect_formal(self):
        level = detect_formality("buenos días, quisiera consultar por favor")
        assert level == "formal"

    def test_detect_casual(self):
        level = detect_formality("che dale joya busco un depto")
        assert level == "casual"

    def test_detect_neutral(self):
        level = detect_formality("hola, busco departamento en alquiler")
        assert level == "neutral"

    def test_formality_guidance(self):
        guidance = get_formality_guidance("formal")
        assert "usted" in guidance.lower()
