"""
tests/test_cw15_1.py
Unit tests for CW15_1Evaluator.check_formatting_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classwork.classwork_15.cw15_1 import CW15_1Evaluator

evaluator = CW15_1Evaluator()


# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: student pasted the task text before their own answer
TEXT_TASK_DESCRIPTION_PRESENT = """
Classwork 15
John Smith
We would like to know if these 9 variables could be shrunk down into a number of factors, and hopefully fewer than 9. We would like to see some correlations between these items and, as a result, a much smaller number of factors.

The KMO value was 0.85, indicating sampling adequacy.
Bartlett's test was significant (p < .001), confirming sufficient correlations.
The model fit Chi Square was significant, suggesting the factor structure fits the data.
"""

# TRUE NEGATIVE: well-written answer, no task text pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
Classwork 15
Jane Doe

The KMO value was 0.85, indicating sampling adequacy.
Bartlett's test was significant (p < .001), confirming sufficient correlations.
The model fit Chi Square was significant, suggesting the factor structure fits the data.
"""

# TRUE POSITIVE: title present
TEXT_TITLE_PRESENT = """
Classwork 15
John Smith
We would like to know if these 9 variables could be shrunk down into a number of factors, and hopefully fewer than 9. We would like to see some correlations between these items and, as a result, a much smaller number of factors.

Some answer here.
"""

# TRUE NEGATIVE: no title
TEXT_TITLE_ABSENT = """
John Smith
We would like to know if these 9 variables could be shrunk down into a number of factors, and hopefully fewer than 9. We would like to see some correlations between these items and, as a result, a much smaller number of factors.

Some answer here.
"""

# TRUE NEGATIVE: autoformatting detected (bullet points)
TEXT_AUTOFORMATTING_PRESENT = """
Classwork 15
John Smith
We would like to know if these 9 variables could be shrunk down into a number of factors, and hopefully fewer than 9. We would like to see some correlations between these items and, as a result, a much smaller number of factors.

- KMO value was 0.85, indicating sampling adequacy.
- Bartlett's test was significant (p < .001).
- The model fit Chi Square was significant.
"""

# TRUE NEGATIVE: no autoformatting
TEXT_AUTOFORMATTING_ABSENT = """
Classwork 15
John Smith
We would like to know if these 9 variables could be shrunk down into a number of factors, and hopefully fewer than 9. We would like to see some correlations between these items and, as a result, a much smaller number of factors.

The KMO value was 0.85, indicating sampling adequacy.
Bartlett's test was significant (p < .001), confirming sufficient correlations.
The model fit Chi Square was significant, suggesting the factor structure fits the data.
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
