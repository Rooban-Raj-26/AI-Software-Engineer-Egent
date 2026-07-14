"""
Unit tests for the JSON-extraction helper shared by Generator/Reviewer/Debugger.
Tests the markdown-fence-stripping logic without calling any LLM.
"""
import json
import pytest
from app.agents.generator_agent import _extract_json


def test_extract_json_plain():
    raw = '[{"filepath": "a.py", "content": "print(1)"}]'
    result = _extract_json(raw)
    assert result == [{"filepath": "a.py", "content": "print(1)"}]


def test_extract_json_strips_markdown_fences():
    raw = '```json\n[{"filepath": "a.py", "content": "x"}]\n```'
    result = _extract_json(raw)
    assert result == [{"filepath": "a.py", "content": "x"}]


def test_extract_json_invalid_raises():
    with pytest.raises(json.JSONDecodeError):
        _extract_json("this is not json at all")