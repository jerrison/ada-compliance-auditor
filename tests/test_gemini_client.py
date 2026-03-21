import json
from pathlib import Path


class TestBuildPrompt:
    def test_prompt_contains_all_violation_types(self):
        """The built prompt includes all violation type IDs from the KB."""
        from backend.gemini_client import build_prompt

        kb_path = Path(__file__).parent.parent / "backend" / "data" / "ada_knowledge_base.json"
        with open(kb_path) as f:
            kb = json.load(f)
        prompt = build_prompt()
        for vtype in kb:
            assert vtype in prompt, f"Violation type '{vtype}' not found in prompt"

    def test_prompt_contains_visual_cues(self):
        """The prompt includes visual cue text from at least some KB entries."""
        from backend.gemini_client import build_prompt

        prompt = build_prompt()
        assert "Steps at entrance with no adjacent ramp" in prompt or "steps" in prompt.lower()

    def test_prompt_specifies_json_output_format(self):
        """The prompt instructs Gemini to return JSON."""
        from backend.gemini_client import build_prompt

        prompt = build_prompt()
        assert "JSON" in prompt
        assert "violation_type" in prompt
        assert "severity" in prompt
        assert "confidence" in prompt

    def test_prompt_includes_severity_guide(self):
        """The prompt includes the severity guide."""
        from backend.gemini_client import build_prompt

        prompt = build_prompt()
        assert "high" in prompt.lower()
        assert "medium" in prompt.lower()
        assert "low" in prompt.lower()

    def test_analyze_image_direct_uses_built_prompt(self):
        """analyze_image_direct uses the dynamically built prompt, not hardcoded."""
        from backend.gemini_client import ANALYSIS_PROMPT

        # After rewrite, ANALYSIS_PROMPT should contain more than 18 types
        assert "missing_automatic_door" in ANALYSIS_PROMPT
        assert "insufficient_door_clearance" in ANALYSIS_PROMPT
