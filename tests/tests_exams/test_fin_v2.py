"""
tests/tests_finals/tests_fin_v2/test_fin_v2.py
Unit tests for FIN_V2Evaluator.check_formatting_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from exams.fin_v2 import FIN_V2Evaluator

evaluator = FIN_V2Evaluator()

# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: name present in first two lines
TEXT_NAME_PRESENT = """
John Doe
Final Exam Variant 2
"""

# TRUE NEGATIVE: no name in first two lines
TEXT_NAME_ABSENT = """
Final Exam Variant 2
Task 1. Some Task
"""

# TRUE POSITIVE: student pasted the full task text before their own answer
TEXT_TASK_DESCRIPTION_PRESENT = """
What can you say
"""

# TRUE NEGATIVE: well-written answer, no task text pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
John Doe
Final Exam Variant 2

The answer is here.
"""

# TRUE POSITIVE: title present
TEXT_TITLE_PRESENT = """
John Doe
Final Exam Variant 2

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
Final Exam Variant 2

- First point.
- Second point.
"""

# TRUE POSITIVE: no autoformatting
TEXT_AUTOFORMATTING_ABSENT = """
John Doe
Final Exam Variant 2

The answer is here.
"""
# TRUE POSITIVE: skewness statement present
TEXT_SKEWNESS_PRESENT = """
John Doe
Final Exam Variant 2

Task 1. If the mean time to respond to a stimulus is much lower than the median time to respond, what can you say about the shape of the distribution of response times? Let's assume the distribution is unimodal. If the mean is lower, that means it is further out into the left-hand tail of the distribution. Therefore, we know this distribution is negatively skewed.

If the distribution is not unimodal, the relationship between mean and median no longer reliably indicates skewness.
"""

# TRUE NEGATIVE: skewness statement absent
TEXT_SKEWNESS_ABSENT = """
John Doe
Final Exam Variant 2
"""

# TRUE POSITIVE: unimodality comment present
TEXT_UNIMODALITY_PRESENT = """
If the distribution is not unimodal, the relationship between mean and median no longer reliably indicates skewness.
"""

# TRUE NEGATIVE: unimodality comment absent
TEXT_UNIMODALITY_ABSENT = """
If the mean is lower, that means it is further out into the left-hand tail of the distribution. Therefore, we know this distribution is negatively skewed.
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

# ---------------------------------------------------------------------------
# Tests: required content
# ---------------------------------------------------------------------------
def test_skewness_present():
    result = evaluator.check_required_elements(TEXT_SKEWNESS_PRESENT)
    assert result["elements_found"]["skewness"] is True

def test_skewness_absent():
    result = evaluator.check_required_elements(TEXT_SKEWNESS_ABSENT)
    assert result["elements_found"]["skewness"] is False

def test_unimodality_present():
    result = evaluator.check_required_elements(TEXT_UNIMODALITY_PRESENT)
    assert result["elements_found"]["unimodality"] is True

def test_unimodality_absent():
    result = evaluator.check_required_elements(TEXT_UNIMODALITY_ABSENT)
    assert result["elements_found"]["unimodality"] is False
