"""
test_cw2_4.py

SAVE LOCATION: tests/tests_classworks/tests_cw2/test_cw2_4.py

RUN WITH: pytest tests/tests_classworks/tests_cw2/test_cw2_4.py -v

Regression tests for the deterministic Component 1 (Formatting) override
in classwork/classwork_2/cw2_4.py's grade_cw2_4_answer method.

Verifies that component_1_score is forced from
check_formatting_elements_type2's elements_found (task_description,
autoformatting), not left to the LLM to assign - same pattern as
classwork/classwork_8/cw8_4.py.

Only the network call (call_groq_api) is mocked; everything else runs
against the real code. If the override is missing or broken, these
tests fail.
"""

import sys
import os
import json
from unittest.mock import patch
import pytest

# tests/tests_classworks/tests_cw2/test_cw2_4.py -> project root is 3 levels up
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from classwork.classwork_2.cw2_4 import CW2_4Evaluator


@pytest.fixture
def evaluator():
    """Deterministic fixture providing a clean evaluator instance for every test."""
    return CW2_4Evaluator()


def _mock_llm_json(component_1_score, component_1_task_score, component_1_autoformat_score):
    """
    Builds a fake LLM JSON response with a deliberately WRONG component_1_score,
    to verify the deterministic override in grade_cw2_4_answer corrects it
    regardless of what the LLM returns.
    """
    return json.dumps({
        "originality_concern": False,
        "component_1_score": component_1_score,
        "component_1_task_score": component_1_task_score,
        "component_1_autoformat_score": component_1_autoformat_score,
        "component_1_explanation": "mock",
        "component_2_score": 4,
        "component_2_explanation": "mock",
        "component_3_score": 5,
        "component_3_explanation": "mock",
        "component_4_score": 5,
        "component_4_explanation": "mock",
        "component_5_score": 4,
        "component_5_explanation": "mock",
        "total_points": 20,
        "max_points": 20,
        "percentage": 100.0,
        "feedback": "mock feedback",
        "vibe": "mock vibe"
    })


def test_component1_forced_when_td_absent(evaluator):
    """
    LLM hallucinates component_1_score=2 (claims TD present), but the marker
    "does your histogram" is absent from the student answer. The deterministic
    override must correct this to 1.
    """
    student_answer = "no marker here, and no bullet lines in this text."

    fake_response = _mock_llm_json(component_1_score=2, component_1_task_score=1, component_1_autoformat_score=1)

    with patch.object(evaluator, "call_groq_api", return_value=fake_response):
        result = evaluator.grade_cw2_4_answer(student_answer)

    assert result["component_1_task_score"] == 0, "TD marker is absent; task score must be forced to 0"
    assert result["component_1_autoformat_score"] == 1, "No bullets present; autoformat score should be 1"
    assert result["component_1_score"] == 1, "component_1_score must be forced to 1, not the LLM's 2"


def test_component1_forced_when_autoformat_violated(evaluator):
    """
    LLM falsely claims full 2/2 even though the student's answer contains
    bullet-style lines (autoformatting violation).
    """
    student_answer = "does your histogram\n\n- first item\n- second item"

    fake_response = _mock_llm_json(component_1_score=2, component_1_task_score=1, component_1_autoformat_score=1)

    with patch.object(evaluator, "call_groq_api", return_value=fake_response):
        result = evaluator.grade_cw2_4_answer(student_answer)

    assert result["component_1_task_score"] == 1, "TD marker is present; task score should be 1"
    assert result["component_1_autoformat_score"] == 0, "Bullets present; autoformat score must be forced to 0"
    assert result["component_1_score"] == 1, "component_1_score must be forced to 1, not the LLM's 2"


def test_component1_correct_when_both_present(evaluator):
    """
    Sanity check: when TD is present and no autoformatting violations exist,
    the deterministic override should agree with a correctly-scoring LLM (2/2).
    """
    student_answer = "does your histogram\n\nPlain sentence with no bullet lines."

    fake_response = _mock_llm_json(component_1_score=2, component_1_task_score=1, component_1_autoformat_score=1)

    with patch.object(evaluator, "call_groq_api", return_value=fake_response):
        result = evaluator.grade_cw2_4_answer(student_answer)

    assert result["component_1_score"] == 2
