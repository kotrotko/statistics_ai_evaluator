"""
tests/test_hw14_1.py
Unit tests for HW14_1Evaluator.check_formatting_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from homework.homework_14.hw14_1 import HW14_1Evaluator

evaluator = HW14_1Evaluator()

# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: student pasted the full task text before their own answer
TEXT_TASK_DESCRIPTION_PRESENT = """
Home Work 14
John Doe
Task 1. What does a goodness-of-fit test assess?

A goodness-of-fit test assesses how well the observed data match a theoretical
or expected distribution. It evaluates whether differences between observed
and expected frequencies are due to chance or indicate a poor fit.
"""

# TRUE NEGATIVE: well-written answer, no task text pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
Home Work 14
Jane Doe

A goodness-of-fit test assesses how well the observed data match a theoretical
or expected distribution. It evaluates whether differences between observed
and expected frequencies are due to chance or indicate a poor fit.
"""

# TRUE POSITIVE: title present
TEXT_TITLE_PRESENT = """
Homework 14
John Doe
Task 1. What does a goodness-of-fit test assess?

Some answer here.
"""

# TRUE NEGATIVE: no title
TEXT_TITLE_ABSENT = """
John Doe
Task 1. What does a goodness-of-fit test assess?

Some answer here.
"""

# TRUE NEGATIVE: autoformatting detected (bullet points)
TEXT_AUTOFORMATTING_PRESENT = """
Homework 14
John Doe
Task 1. What does a goodness-of-fit test assess?

- A goodness-of-fit test compares observed and expected frequencies.
- It determines whether the data follow a specified distribution.
"""

# TRUE NEGATIVE: no autoformatting
TEXT_AUTOFORMATTING_ABSENT = """
Homework 14
John Doe
Task 1. What does a goodness-of-fit test assess?

A goodness-of-fit test compares observed and expected frequencies.
It determines whether the data follow a specified distribution.
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