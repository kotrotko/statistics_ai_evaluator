"""
tests/test_hw13_1.py
Unit tests for HW13_1Evaluator.check_formatting_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from homework.homework_13.hw13_1 import HW13_1Evaluator

evaluator = HW13_1Evaluator()


# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: student pasted the task text before their own answer
TEXT_TASK_DESCRIPTION_PRESENT = """
Homework 13
John Doe
Task 1. What is a residual?

In linear regression, a residual is the difference between the observed value
and the predicted value from the regression line.
Formula: Residual = Y − Ŷ
A positive residual means the actual value is higher than predicted.
A negative residual means the actual value is lower than predicted.
"""

# TRUE NEGATIVE: well-written answer, no task text pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
Homework 13
John Doe

In linear regression, a residual is the difference between the observed value
and the predicted value from the regression line.
Formula: Residual = Y − Ŷ
A positive residual means the actual value is higher than predicted.
A negative residual means the actual value is lower than predicted.
"""

# TRUE POSITIVE: title present
TEXT_TITLE_PRESENT = """
Homework 13
John Doe
Task 1. What is a residual?

Some answer here.
"""

# TRUE NEGATIVE: no title
TEXT_TITLE_ABSENT = """
John Doe
Task 1. What is a residual?

Some answer here.
"""

# TRUE NEGATIVE: autoformatting detected (bullet points)
TEXT_AUTOFORMATTING_PRESENT = """
Homework 13
John Doe
Task 1. What is a residual?

- A residual is the difference between observed and predicted values.
- Formula: Residual = Y − Ŷ
- Positive residual: actual value is higher than predicted.
"""

# TRUE NEGATIVE: no autoformatting
TEXT_AUTOFORMATTING_ABSENT = """
Homework 13
John Doe
Task 1. What is a residual?

A residual is the difference between observed and predicted values.
Formula: Residual = Y − Ŷ
A positive residual means the actual value is higher than predicted.
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