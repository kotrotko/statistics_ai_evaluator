"""
tests/test_cw14_2.py
Unit tests for CW14_2Evaluator.check_required_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classwork.classwork_14.cw14_2 import CW14_2Evaluator

evaluator = CW14_2Evaluator()


# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: student pasted the task text before their own answer
TEXT_TASK_DESCRIPTION_PRESENT = """
Classwork 14
John Smith
Following our Step system, on: Step 1. Name the method you choose and justify it based on the data level (5 points). Step 2. State the hypotheses in needed form (5 points). Step 3. State the significance level α, calculate df, find the critical value. (5 points). Step 4. Using JASP, calculate the χ^2. Make the statistical inference (5 points).

Step 1. Chi-square test of independence was chosen because both variables are categorical (nominal level).
Step 2. H0: Physical activity and fruit consumption are independent. H1: They are not independent.
Step 3. α = 0.05, df = (3-1)(3-1) = 4, critical value = 9.488.
Step 4. χ²(4) = 14.152, p = .007. Since p < .05, we reject H0.
"""

# TRUE NEGATIVE: well-written answer, no task text pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
Classwork 14
Jane Doe

Step 1. Chi-square test of independence was chosen because both variables are categorical (nominal level).
Step 2. H0: Physical activity and fruit consumption are independent. H1: They are not independent.
Step 3. α = 0.05, df = (3-1)(3-1) = 4, critical value = 9.488.
Step 4. χ²(4) = 14.152, p = .007. Since p < .05, we reject H0.
"""

# TRUE POSITIVE: title present
TEXT_TITLE_PRESENT = """
Classwork 14
John Smith
Name the method you choose and justify it based on the data level (5 points). Step 2. State the hypotheses in needed form (5 points).

Some answer here.
"""

# TRUE NEGATIVE: no title
TEXT_TITLE_ABSENT = """
John Smith
Name the method you choose and justify it based on the data level (5 points). Step 2. State the hypotheses in needed form (5 points).

Some answer here.
"""

# TRUE NEGATIVE: autoformatting detected (bullet points)
TEXT_AUTOFORMATTING_PRESENT = """
Classwork 14
John Smith
Name the method you choose and justify it based on the data level (5 points). Step 2. State the hypotheses in needed form (5 points).

- Chi-square test was chosen because variables are categorical.
- H0: Variables are independent.
- α = 0.05, df = 4, critical value = 9.488.
"""

# TRUE NEGATIVE: no autoformatting
TEXT_AUTOFORMATTING_ABSENT = """
Classwork 14
John Smith
Name the method you choose and justify it based on the data level (5 points). Step 2. State the hypotheses in needed form (5 points).

Chi-square test was chosen because variables are categorical.
H0: Variables are independent. H1: They are not independent.
α = 0.05, df = 4, critical value = 9.488.
"""


# ---------------------------------------------------------------------------
# Tests: task_description
# ---------------------------------------------------------------------------

def test_task_description_present():
    result = evaluator.check_required_elements(TEXT_TASK_DESCRIPTION_PRESENT)
    assert result["elements_found"]["task_description"] is True

def test_task_description_absent():
    result = evaluator.check_required_elements(TEXT_TASK_DESCRIPTION_ABSENT)
    assert result["elements_found"]["task_description"] is False


# ---------------------------------------------------------------------------
# Tests: paper_title
# ---------------------------------------------------------------------------

def test_title_present():
    result = evaluator.check_required_elements(TEXT_TITLE_PRESENT)
    assert result["elements_found"]["paper_title"] is True

def test_title_absent():
    result = evaluator.check_required_elements(TEXT_TITLE_ABSENT)
    assert result["elements_found"]["paper_title"] is False


# ---------------------------------------------------------------------------
# Tests: no_autoformatting
# ---------------------------------------------------------------------------

def test_autoformatting_detected():
    result = evaluator.check_required_elements(TEXT_AUTOFORMATTING_PRESENT)
    assert result["elements_found"]["no_autoformatting"] is False

def test_no_autoformatting():
    result = evaluator.check_required_elements(TEXT_AUTOFORMATTING_ABSENT)
    assert result["elements_found"]["no_autoformatting"] is True