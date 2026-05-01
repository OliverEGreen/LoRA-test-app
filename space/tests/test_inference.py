"""Smoke tests for the pure logic in ``inference``.

The fal.ai network call is intentionally *not* tested — it requires a real
API key and burns credits. We test the only piece of logic that's worth
covering: prompt formatting / trigger-word handling.
"""

import pytest

from inference import _format_prompt


def test_prepends_trigger_when_missing():
    assert _format_prompt("a brick rowhouse", "kodachrome") == "kodachrome, a brick rowhouse"


def test_skips_when_trigger_already_present():
    assert (
        _format_prompt("kodachrome, a brick rowhouse", "kodachrome")
        == "kodachrome, a brick rowhouse"
    )


def test_trigger_match_is_case_insensitive():
    # User-typed capitalisation is preserved; we just don't double-prepend.
    assert (
        _format_prompt("Kodachrome, a brick rowhouse", "kodachrome")
        == "Kodachrome, a brick rowhouse"
    )


def test_strips_surrounding_whitespace():
    assert _format_prompt("  a brick rowhouse  ", "kodachrome") == "kodachrome, a brick rowhouse"


@pytest.mark.parametrize("empty", ["", "   ", "\n\t"])
def test_empty_prompt_raises(empty: str):
    with pytest.raises(ValueError, match="empty"):
        _format_prompt(empty, "kodachrome")
