"""
tests/test_hw13_2.py
Unit tests for HW13_2Evaluator.check_formatting_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from homework.homework_13.hw13_2 import HW13_2Evaluator

evaluator = HW13_2Evaluator()


# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: student pasted the task text before their own answer
TEXT_TASK_DESCRIPTION_PRESENT = """
Homework 13
John Doe
Task 2. What are the two parameters of the line of best fit, and what do they represent?

The two parameters are slope and intercept.
Slope (b1) shows how much the dependent variable changes when the independent variable increases by 1 unit.
Positive slope means an increasing relationship. Negative slope means a decreasing relationship.
Intercept (b0) is the predicted value of the dependent variable when the independent variable equals 0.
Regression equation: ŷ = b0 + b1x
"""

# TRUE NEGATIVE: well-written answer, no task text pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
Homework 13
John Doe

The two parameters are slope and intercept.
Slope (b1) shows how much the dependent variable changes when the independent variable increases by 1 unit.
Positive slope means an increasing relationship. Negative slope means a decreasing relationship.
Intercept (b0) is the predicted value of the dependent variable when the independent variable equals 0.
Regression equation: ŷ = b0 + b1x
"""

# TRUE NEGATIVE: autoformatting detected (bullet points)
TEXT_AUTOFORMATTING_PRESENT = """
Homework 13
John Doe
Task 2. What are the two parameters of the line of best fit, and what do they represent?

- Slope (b1): shows how much Y changes when X increases by 1.
- Intercept (b0): predicted value of Y when X equals 0.
- Equation: ŷ = b0 + b1x
"""

# TRUE NEGATIVE: no autoformatting
TEXT_AUTOFORMATTING_ABSENT = """
Homework 13
John Doe
Task 2. What are the two parameters of the line of best fit, and what do they represent?

The slope (b1) shows how much Y changes when X increases by 1 unit.
The intercept (b0) is the predicted value of Y when X equals 0.
The regression equation is ŷ = b0 + b1x.
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
    