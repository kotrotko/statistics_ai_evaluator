"""
tests/test_hw13_5.py
Unit tests for HW13_5Evaluator.check_formatting_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import inspect
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from homework.homework_13.hw13_5 import HW13_5Evaluator

evaluator = HW13_5Evaluator()


# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: student pasted the task text before their own answer
TEXT_TASK_DESCRIPTION_PRESENT = """
Using these values, calculate the line of best fit predicting volunteering from extroversion then test for a statistically significant relation using the hypothesis testing procedure: X= 12.58, sX =4.65, Y= 7.44, sY = 2.12, r = 0.34, N = 67, SSM = 19.79, SSE = 215.77.
 
Problem Statement:
This study examines whether there is a linear relationship between extroversion and volunteering behavior.
 
Research Question:
Does extroversion significantly predict volunteering behavior?
 
H0: β = 0 — extroversion does not significantly predict volunteering
H1: β ≠ 0 — extroversion significantly predicts volunteering
 
b = 0.1550, a = 5.490
Equation: Ŷ = 5.490 + 0.155X
 
F(1, 65) = 5.962, p < .05, reject H0.
"""

# TRUE NEGATIVE: well-written answer, no task text pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
Problem Statement:
This study examines whether there is a linear relationship between extroversion and volunteering behavior.
 
Research Question:
Does extroversion significantly predict volunteering behavior?
 
H0: β = 0 — extroversion does not significantly predict volunteering
H1: β ≠ 0 — extroversion significantly predicts volunteering
 
b = 0.1550, a = 5.490
Equation: Ŷ = 5.490 + 0.155X
 
F(1, 65) = 5.962, p < .05, reject H0.
"""

# AUTOFORMATTING: bullet points present
TEXT_AUTOFORMATTING_PRESENT = """
Using these values, calculate the line of best fit predicting volunteering from extroversion then test for a statistically significant relation using the hypothesis testing procedure: X= 12.58, sX =4.65, Y= 7.44, sY = 2.12, r = 0.34, N = 67, SSM = 19.79, SSE = 215.77.
 
- b = 0.1550
- a = 5.490
- F(1, 65) = 5.962, reject H0.
"""

# NO AUTOFORMATTING: clean prose
TEXT_AUTOFORMATTING_ABSENT = """
Using these values, calculate the line of best fit predicting volunteering from extroversion then test for a statistically significant relation using the hypothesis testing procedure: X= 12.58, sX =4.65, Y= 7.44, sY = 2.12, r = 0.34, N = 67, SSM = 19.79, SSE = 215.77.
 
b = 0.1550, a = 5.490. Equation: Ŷ = 5.490 + 0.155X. F(1, 65) = 5.962, reject H0.
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


# ---------------------------------------------------------------------------
# Tests: component_1_score enforcement
# ---------------------------------------------------------------------------

def test_component_1_score_full():
    """Both task description and no autoformatting present — expect score 2."""
    check = evaluator.check_formatting_elements(TEXT_TASK_DESCRIPTION_PRESENT)
    task_score = 1 if check["elements_found"]["task_description"] else 0
    autoformat_score = 1 if check["elements_found"]["no_autoformatting"] else 0
    assert task_score + autoformat_score == 2

def test_component_1_score_missing_task_description():
    """Task description absent — expect score 1."""
    check = evaluator.check_formatting_elements(TEXT_TASK_DESCRIPTION_ABSENT)
    task_score = 1 if check["elements_found"]["task_description"] else 0
    autoformat_score = 1 if check["elements_found"]["no_autoformatting"] else 0
    assert task_score + autoformat_score == 1

def test_component_1_score_autoformatting_detected():
    """Autoformatting present — expect score 1."""
    check = evaluator.check_formatting_elements(TEXT_AUTOFORMATTING_PRESENT)
    task_score = 1 if check["elements_found"]["task_description"] else 0
    autoformat_score = 1 if check["elements_found"]["no_autoformatting"] else 0
    assert task_score + autoformat_score == 1


# ---------------------------------------------------------------------------
# Tests: component_2 max score
# ---------------------------------------------------------------------------

def test_component_2_max_is_3():
    """Component 2 max must be 3 so that 2+3+5+5+5=20."""
    source = inspect.getsource(evaluator.grade_hw13_5_answer)
    assert '"component_2_score": <0-3>' in source
