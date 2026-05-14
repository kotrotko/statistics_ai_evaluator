"""
tests/tests_classworks/tests_cw5/test_cw5_1.py
Unit tests for CW5_1Evaluator.check_formatting_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from classwork.classwork_5.cw5_1 import CW5_1Evaluator

evaluator = CW5_1Evaluator()

# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: name present in first two lines
TEXT_NAME_PRESENT = """
John Doe
Class Work 5
"""

# TRUE NEGATIVE: no name in first two lines
TEXT_NAME_ABSENT = """
Class Work 5
Task 1. Central Limit Theorem
"""

# TRUE POSITIVE: student pasted the full task text before their own answer
TEXT_TASK_DESCRIPTION_PRESENT = """
True or False?
"""

# TRUE NEGATIVE: well-written answer, no task text pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
John Doe
Class Work 5

The statement is true.
"""

# TRUE POSITIVE: title present
TEXT_TITLE_PRESENT = """
John Doe
Class Work 5

Some content.
"""

# TRUE NEGATIVE: no title
TEXT_TITLE_ABSENT = """
John Doe

Some content.
"""

# TRUE NEGATIVE: autoformatting detected (bullet points)
TEXT_AUTOFORMATTING_PRESENT = """
John Doe
Class Work 5

- The standard error decreases.
- The sample size increases.
"""

# TRUE POSITIVE: no autoformatting
TEXT_AUTOFORMATTING_ABSENT = """
John Doe
Class Work 5

The statement is true.
"""


# ---------------------------------------------------------------------------
# Tests: student_name
# ---------------------------------------------------------------------------

def test_name_present():
    result = evaluator.check_formatting_elements(TEXT_NAME_PRESENT)
    assert result["elements_found"]["student_name"] is True


def test_name_absent():
    result = evaluator.check_formatting_elements(TEXT_NAME_ABSENT)
    assert result["elements_found"]["student_name"] is False


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
# Tests: paper_title
# ---------------------------------------------------------------------------

def test_title_present():
    result = evaluator.check_formatting_elements(TEXT_TITLE_PRESENT)
    assert result["elements_found"]["paper_title"] is True


def test_title_absent():
    result = evaluator.check_formatting_elements(TEXT_TITLE_ABSENT)
    assert result["elements_found"]["paper_title"] is False


# ---------------------------------------------------------------------------
# Tests: autoformatting
# ---------------------------------------------------------------------------

def test_autoformatting_detected():
    result = evaluator.check_formatting_elements(TEXT_AUTOFORMATTING_PRESENT)
    assert result["elements_found"]["autoformatting"] is False


def test_no_autoformatting():
    result = evaluator.check_formatting_elements(TEXT_AUTOFORMATTING_ABSENT)
    assert result["elements_found"]["autoformatting"] is True