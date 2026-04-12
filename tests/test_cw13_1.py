"""
tests/test_cw13_1.py
Unit tests for CW13_1Evaluator.check_formatting_elements()
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classwork.classwork_13.cw13_1 import CW13_1Evaluator

evaluator = CW13_1Evaluator()


# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: student pasted the full task text before their own answer
TEXT_TASK_DESCRIPTION_PRESENT = """
Classwork 13
John Smith
State the problem with your own words (5 points) and formulate Research question (5 points). What is a predictor? What is criterion (outcome) variable? (5 points) For Linear Regression in JASP tab, which variable is Dependent? Which one is Predictor (independent Variable)? (5 points).

We are investigating whether study hours predict exam scores.
Research question: Does the number of study hours significantly predict exam scores?
The predictor is the independent variable used to predict the outcome.
The criterion is the dependent variable we are trying to explain.
In JASP, the criterion goes into the Dependent box and the predictor into Covariates.
"""

# TRUE NEGATIVE: well-written answer, no task text pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
Classwork 13
Jane Doe

We are investigating whether hours of sleep predict academic performance.
Research question: Does sleep duration significantly predict GPA?
The predictor is the variable that explains variance in the outcome.
The criterion is what we are trying to predict.
In JASP, the criterion variable goes into the Dependent box and the predictor into Covariates.
"""

# TRUE POSITIVE: title present
TEXT_TITLE_PRESENT = """
Classwork 13
John Smith
State the problem with your own words (5 points) and formulate Research question (5 points). What is a predictor? What is criterion (outcome) variable? (5 points) For Linear Regression in JASP tab, which variable is Dependent? Which one is Predictor (independent Variable)? (5 points).

Some answer here.
"""

# TRUE NEGATIVE: no title
TEXT_TITLE_ABSENT = """
John Smith
State the problem with your own words (5 points) and formulate Research question (5 points). What is a predictor? What is criterion (outcome) variable? (5 points) For Linear Regression in JASP tab, which variable is Dependent? Which one is Predictor (independent Variable)? (5 points).

Some answer here.
"""

# TRUE NEGATIVE: autoformatting detected (bullet points)
TEXT_AUTOFORMATTING_PRESENT = """
Classwork 13
John Smith
State the problem with your own words (5 points) and formulate Research question (5 points). What is a predictor? What is criterion (outcome) variable? (5 points) For Linear Regression in JASP tab, which variable is Dependent? Which one is Predictor (independent Variable)? (5 points).

- The predictor is the independent variable.
- The criterion is the dependent variable.
- In JASP, criterion goes to Dependent box.
"""

# TRUE NEGATIVE: no autoformatting
TEXT_AUTOFORMATTING_ABSENT = """
Classwork 13
John Smith
State the problem with your own words (5 points) and formulate Research question (5 points). What is a predictor? What is criterion (outcome) variable? (5 points) For Linear Regression in JASP tab, which variable is Dependent? Which one is Predictor (independent Variable)? (5 points).

The predictor is the independent variable. The criterion is the dependent variable.
In JASP, the criterion goes into the Dependent box and the predictor into Covariates.
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
