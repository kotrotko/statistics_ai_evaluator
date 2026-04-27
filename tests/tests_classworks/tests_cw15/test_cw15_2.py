"""
tests/tests_classworks/tests_cw15/test_cw15_2.py
Unit tests for CW15_2Evaluator.check_formatting_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from classwork.classwork_15.cw15_2 import CW15_2Evaluator

evaluator = CW15_2Evaluator()

# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: student pasted the full task text before their own answer
TEXT_TASK_DESCRIPTION_PRESENT = """
Class Work 15
John Doe
What is proportion of items (just high or low) shows strong factor loading?
How many factors do you see?
"""

# TRUE NEGATIVE: well-written answer, no task text pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
Class Work 15
Jane Doe

The promax rotation identified a three-factor structure with most items
showing strong factor loadings above .40.
"""

# TRUE NEGATIVE: autoformatting detected (bullet points)
TEXT_AUTOFORMATTING_PRESENT = """
Class Work 15
John Doe

- Factor 1 was mainly defined by x5, x4, and x6.
- Factor 2 by x7, x8, and x9.
"""

# TRUE POSITIVE: no autoformatting
TEXT_AUTOFORMATTING_ABSENT = """
Class Work 15
John Doe

Factor 1 was mainly defined by x5, x4, and x6.
Factor 2 by x7, x8, and x9.
"""


# ---------------------------------------------------------------------------
# Tests: task_description
# ---------------------------------------------------------------------------

def test_task_description_present():
    result = evaluator.check_formatting_elements(TEXT_TASK_DESCRIPTION_PRESENT)
    assert result["elements_found"]["task_description"] is True


def test_task_description_absent():
    result = evaluator.check_formatting_elements(TEXT_TASK_DESCRIPTION_ABSENT)
    assert result["elements_found"]["task_description"] is False


# ---------------------------------------------------------------------------
# Tests: no_autoformatting
# ---------------------------------------------------------------------------

def test_autoformatting_detected():
    result = evaluator.check_formatting_elements(TEXT_AUTOFORMATTING_PRESENT)
    assert result["elements_found"]["no_autoformatting"] is False


def test_no_autoformatting():
    result = evaluator.check_formatting_elements(TEXT_AUTOFORMATTING_ABSENT)
    assert result["elements_found"]["no_autoformatting"] is True