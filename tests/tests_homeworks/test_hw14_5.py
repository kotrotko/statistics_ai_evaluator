"""
tests/tests_homeworks/test_hw14_5.py
Unit tests for HW14_5Evaluator.check_formatting_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from homework.homework_14.hw14_5 import HW14_5Evaluator

evaluator = HW14_5Evaluator()

# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: student pasted the full task text before their own answer
TEXT_TASK_DESCRIPTION_PRESENT = """
A company you work for wants to make sure that they are not discriminating against anyone in their promotion process.
You have been asked to look across gender to see if there are differences in promotion rate.
The following data should be assessed at the normal level of significance.
"""

# TRUE NEGATIVE: well-written answer, no task text pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
The chi-square test for independence is appropriate because there are two categorical variables: gender and promotion status.
H₀: Gender and promotion are independent. H₁: Gender and promotion are associated.
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
    