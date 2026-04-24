"""
tests/test_cw14_1.py
Unit tests for CW14_1Evaluator.check_formatting_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classwork.classwork_14.cw14_1 import CW14_1Evaluator

evaluator = CW14_1Evaluator()

# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: student pasted the full task text before their own answer
TEXT_TASK_DESCRIPTION_PRESENT = """
Classwork 14
John Smith
State the problem with your own words (10 points) and formulate Research question (10 points).

We are investigating whether anxiety levels predict academic performance.
Research question: Does anxiety level significantly predict exam scores?
"""

# TRUE NEGATIVE: well-written answer, no task text pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
Classwork 14
Jane Doe

We are investigating whether anxiety levels predict academic performance.
Research question: Does anxiety level significantly predict exam scores?
"""

# TRUE POSITIVE: title present
TEXT_TITLE_PRESENT = """
Classwork 14
John Smith
State the problem with your own words (10 points) and formulate Research question (10 points).

Some answer here.
"""

# TRUE NEGATIVE: no title
TEXT_TITLE_ABSENT = """
John Smith
State the problem with your own words (10 points) and formulate Research question (10 points).

Some answer here.
"""

# TRUE NEGATIVE: autoformatting detected (bullet points)
TEXT_AUTOFORMATTING_PRESENT = """
Classwork 14
John Smith
State the problem with your own words (10 points) and formulate Research question (10 points).

- The problem is that anxiety may affect performance.
- Research question: Does anxiety predict exam scores?
"""

# TRUE NEGATIVE: no autoformatting
TEXT_AUTOFORMATTING_ABSENT = """
Classwork 14
John Smith
State the problem with your own words (10 points) and formulate Research question (10 points).

The problem is that anxiety may affect performance.
Research question: Does anxiety predict exam scores?
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
