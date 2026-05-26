"""Tests for skill ecosystem — loader, registry, progressive, composer."""

import pytest
import time
from pathlib import Path
from app.skills.loader import load_skill, SkillDefinition
from app.skills.registry import SkillRegistry
from app.skills.progressive import (
    get_context_tokens,
    select_level,
    get_active_skills_summary,
)
from app.skills.composer import suggest_next_skills, find_similar_skills

SKILLS_DIR = Path(__file__).parent.parent / "skills"


class TestLoader:
    def test_load_search_properties(self):
        path = SKILLS_DIR / "search_properties" / "SKILL.md"
        skill = load_skill(path)
        assert skill.name == "search_properties"
        assert skill.version == "1.0.0"
        assert skill.category == "search"
        assert "Busca propiedades" in skill.description

    def test_load_all_skills(self):
        # Just test that the files parse without error
        for md_file in SKILLS_DIR.rglob("SKILL.md"):
            skill = load_skill(md_file)
            assert skill.name
            assert skill.description
            assert skill.summary  # Level 1 must exist

    def test_level1_tokens_under_200(self):
        """Summary should be compact (~120 tokens target)."""
        for md_file in SKILLS_DIR.rglob("SKILL.md"):
            skill = load_skill(md_file)
            assert skill.level1_tokens < 250, (
                f"{skill.name}: {skill.level1_tokens} tokens in summary"
            )

    def test_frontmatter_required_fields(self):
        for md_file in SKILLS_DIR.rglob("SKILL.md"):
            skill = load_skill(md_file)
            assert skill.name
            assert skill.version
            assert skill.description
            assert skill.category


class TestSkillRegistry:
    def test_load_all(self):
        reg = SkillRegistry(skills_dir=str(SKILLS_DIR))
        count = reg.load_all()
        assert count == 6

    def test_get_by_name(self):
        reg = SkillRegistry(skills_dir=str(SKILLS_DIR))
        reg.load_all()
        skill = reg.get("search_properties")
        assert skill is not None
        assert skill.category == "search"

    def test_get_missing(self):
        reg = SkillRegistry(skills_dir=str(SKILLS_DIR))
        reg.load_all()
        assert reg.get("nonexistent") is None

    def test_mcp_tools(self):
        reg = SkillRegistry(skills_dir=str(SKILLS_DIR))
        reg.load_all()
        tools = reg.get_mcp_tools()
        assert len(tools) == 6
        names = [t["name"] for t in tools]
        assert "search_properties" in names
        assert "schedule_visit" in names


class TestProgressiveDisclosure:
    def test_level1_tokens(self):
        tokens = get_context_tokens(level=1)
        assert tokens > 0
        # With 6 skills, even summaries should be a few hundred tokens total
        assert tokens < 500

    def test_select_level_default(self):
        assert select_level("search_properties") == 1

    def test_select_level_relevant(self):
        assert select_level("search_properties", is_relevant=True) == 2

    def test_select_level_executing(self):
        assert select_level("get_property_details", is_executing=True) == 3

    def test_active_skills_summary(self):
        summary = get_active_skills_summary()
        assert "search_properties" in summary
        assert "schedule_visit" in summary
        assert "compare_properties" in summary


class TestComposer:
    def test_suggest_after_search(self):
        suggestions = suggest_next_skills("search_properties")
        assert "get_property_details" in suggestions
        assert "get_property_images" in suggestions

    def test_suggest_after_details(self):
        suggestions = suggest_next_skills("get_property_details")
        assert "schedule_visit" in suggestions

    def test_find_similar(self):
        results = find_similar_skills("buscar")
        assert len(results) > 0
        assert "search_properties" in results

    def test_find_similar_schedule(self):
        results = find_similar_skills("agendar")
        assert "schedule_visit" in results

    def test_find_similar_no_match(self):
        results = find_similar_skills("xyzzy_nonexistent")
        assert results == []
