"""Tests for flexible scheduling flow — parsed in ONE turn."""

import re
import pytest


# Replicate the scheduling extraction logic for testing
def extract_scheduling_info(message: str) -> dict:
    """Extract scheduling details from a free-form message."""
    info = {"property_id": None, "name": None, "phone": None, "day": None, "time": None}

    msg = message.lower()

    # Property ID
    id_match = re.search(r"\b(?:depto|departamento|propiedad|casa|ph|terreno|el|la|id)\s*#?\s*(\d+)\b", msg)
    if id_match:
        info["property_id"] = int(id_match.group(1))

    # Phone
    phone_match = re.search(r"\b(\d{3,4}[\s-]?\d{6,8})\b", msg)
    if phone_match:
        info["phone"] = phone_match.group(1).replace(" ", "-")

    # Day
    days = ["lunes", "martes", "miércoles", "miercoles", "jueves", "viernes", "sábado", "sabado", "domingo"]
    for day in days:
        if day in msg:
            info["day"] = day
            break

    # Time (must be preceded by "a las", "a la", or followed by "hs", "horas", or be a standalone hour-like number at end)
    time_match = re.search(r"\b(?:a las?|a la)\s*(\d{1,2})(?::(\d{2}))?\b", msg)
    if not time_match:
        time_match = re.search(r"\b(\d{1,2})(?::(\d{2}))?\s*(?:hs|horas|am|pm)\b", msg)
    if not time_match:
        # Bare number at end (e.g., "martes 11")
        time_match = re.search(r"\b(\d{1,2})\s*$", msg)
    if time_match:
        hour = time_match.group(1)
        info["time"] = f"{hour}:00"

    # Name (after "soy", "me llamo", "nombre")
    name_match = re.search(r"\b(?:soy|me llamo|nombre es|nombre:)\s+(\w+)", msg)
    if name_match:
        info["name"] = name_match.group(1).capitalize()

    return info


class TestSchedulingExtraction:
    def test_full_single_turn(self):
        """'agendame para ver el depto 5 el martes a las 11, soy Juan'"""
        msg = "agendame para ver el depto 5 el martes a las 11, soy Juan, 3755-123456"
        info = extract_scheduling_info(msg)
        assert info["property_id"] == 5
        assert info["day"] == "martes"
        assert info["time"] == "11:00"
        assert info["name"] == "Juan"
        assert "3755" in info.get("phone", "")

    def test_another_format(self):
        msg = "quiero visitar la propiedad 3 el viernes a las 16hs, me llamo María, 3755-998877"
        info = extract_scheduling_info(msg)
        assert info["property_id"] == 3
        assert info["day"] == "viernes"
        assert info["time"] == "16:00"
        assert info["name"] == "María"

    def test_minimal_info(self):
        msg = "agendame para ver el 7"
        info = extract_scheduling_info(msg)
        assert info["property_id"] == 7
        assert info["name"] is None
        assert info["day"] is None

    def test_no_property(self):
        msg = "quiero agendar una visita el lunes"
        info = extract_scheduling_info(msg)
        assert info["property_id"] is None
        assert info["day"] == "lunes"

    def test_extraction_robustness(self):
        """Verify all extraction methods work on a variety of messages."""
        test_cases = [
            ("agendame depto 5 martes 11", {"property_id": 5, "day": "martes", "time": "11:00"}),
            ("visitar el 3 el viernes", {"property_id": 3, "day": "viernes"}),
            ("coordinamos para el lunes a las 10?", {"day": "lunes", "time": "10:00"}),
        ]
        for msg, expected in test_cases:
            info = extract_scheduling_info(msg)
            for key, val in expected.items():
                assert info[key] == val, f"Failed on '{msg}': {key} expected {val}, got {info[key]}"
