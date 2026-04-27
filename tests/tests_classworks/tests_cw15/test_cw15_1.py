"""
tests/tests_classworks/tests_cw15/test_cw15_1.py
Unit tests for CW15_1Evaluator.check_formatting_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from classwork.classwork_15.cw15_1 import CW15_1Evaluator

evaluator = CW15_1Evaluator()

# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: student pasted the full task text before their own answer
TEXT_TASK_DESCRIPTION_PRESENT = """
    add this statement into your paper,
    how do you know,
"""

# TRUE NEGATIVE: well-written answer, no task text pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
Class Work 15
Jane Doe

The KMO value is 0.752, indicating that the sample is adequate for factor analysis.
Bartlett's test was significant at p < .001.
"""

# TRUE POSITIVE: title present
TEXT_TITLE_PRESENT = """
Class Work 15
John Doe

Some answer here.
"""

# TRUE NEGATIVE: no title
TEXT_TITLE_ABSENT = """
John Doe

Some answer here.
"""

# TRUE NEGATIVE: autoformatting detected (bullet points)
TEXT_AUTOFORMATTING_PRESENT = """
Class Work 15
John Doe

- The KMO value is 0.752, indicating sampling adequacy.
- Bartlett's test is significant at p < .001.
"""

# TRUE POSITIVE: no autoformatting
TEXT_AUTOFORMATTING_ABSENT = """
Class Work 15
John Doe

The KMO value is 0.752, indicating sampling adequacy.
Bartlett's test is significant at p < .001.
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
# Tests: paper_title
# ---------------------------------------------------------------------------

def test_title_present():
    result = evaluator.check_formatting_elements(TEXT_TITLE_PRESENT)
    assert result["elements_found"]["paper_title"] is True


def test_title_absent():
    result = evaluator.check_formatting_elements(TEXT_TITLE_ABSENT)
    assert result["elements_found"]["paper_title"] is False


# ---------------------------------------------------------------------------
# Tests: no_autoformatting
# ---------------------------------------------------------------------------

def test_autoformatting_detected():
    result = evaluator.check_formatting_elements(TEXT_AUTOFORMATTING_PRESENT)
    assert result["elements_found"]["no_autoformatting"] is False


def test_no_autoformatting():
    result = evaluator.check_formatting_elements(TEXT_AUTOFORMATTING_ABSENT)
    assert result["elements_found"]["no_autoformatting"] is True