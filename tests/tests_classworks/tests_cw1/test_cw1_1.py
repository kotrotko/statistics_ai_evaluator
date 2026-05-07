"""
tests/tests_classworks/tests_cw1/test_cw1_1.py
Unit tests for CW1_1Evaluator.check_formatting_elements()
and check_step_completeness()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.

Rubric (20 points total):
  Formatting:  4 pts (name 1, title 1, task description 1, no autoformatting 1)
  Step 1 (x̄ via Accent):          3 pts
  Step 2 (Σxᵢ via Script):         3 pts
  Step 3 ((Σxᵢ)/n via Fraction):   3 pts
  Step 4 (√((Σxᵢ)/n) via Radical): 3 pts
  Step 5 (full formula):            4 pts
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from classwork.classwork_1.cw1_1 import CW1_1Evaluator

evaluator = CW1_1Evaluator()

# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: student pasted the full task text before their own answer
TEXT_TASK_DESCRIPTION_PRESENT = """
 Using Microsoft Word's Equation tool (Insert > Equation), write the formula for the mean.
 """

# TRUE NEGATIVE: well-written answer, no task text pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
 Class Work 1
 John Doe

 x̄
 """

# TRUE POSITIVE: title present
TEXT_TITLE_PRESENT = """
 Class Work 1
 John Doe

 Some content.
 """

# TRUE NEGATIVE: no title
TEXT_TITLE_ABSENT = """
 John Doe

 Some content.
 """

# TRUE POSITIVE: name present
TEXT_NAME_PRESENT = """
 Class Work 1
 John Doe

 Some content.
 """

# TRUE NEGATIVE: no name
TEXT_NAME_ABSENT = """
 Class Work 1

 Some content.
 """

# TRUE NEGATIVE: autoformatting detected (numbered steps)
TEXT_AUTOFORMATTING_PRESENT = """
 Class Work 1
 John Doe

 Step 1:
 Step 2:
 Step 3:
 """

# TRUE POSITIVE: no autoformatting
TEXT_AUTOFORMATTING_ABSENT = """
 Class Work 1
 John Doe
 x̄
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
# Tests: name
# ---------------------------------------------------------------------------

def test_name_present():
    result = evaluator.check_formatting_elements(TEXT_NAME_PRESENT)
    assert result["elements_found"]["name"] is True


def test_name_absent():
    result = evaluator.check_formatting_elements(TEXT_NAME_ABSENT)
    assert result["elements_found"]["name"] is False


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
# Test texts: step completeness & correctness
# ---------------------------------------------------------------------------

# TRUE POSITIVE: all 5 steps present in order, each with the correct element
TEXT_STEPS_COMPLETE = """
 Class Work 1
 John Doe

 x̄
 Σxᵢ
 (Σxᵢ)/n
 √((Σxᵢ)/n)
 x̄ = √((Σxᵢ)/n)
 """

# TRUE NEGATIVE: steps out of order — step 3 appears before step 2
TEXT_STEPS_OUT_OF_ORDER = """
 Class Work 1
 John Doe

 x̄
 (Σxᵢ)/n
 Σxᵢ
 √((Σxᵢ)/n)
 x̄ = √((Σxᵢ)/n)
 """

# TRUE NEGATIVE: step 4 is missing (no √((Σxᵢ)/n) present)
TEXT_STEPS_INCOMPLETE = """
 Class Work 1
 John Doe

 x̄
 Σxᵢ
 (Σxᵢ)/n
 x̄ = √((Σxᵢ)/n)
 """


# ---------------------------------------------------------------------------
# Tests: step completeness & correctness
# ---------------------------------------------------------------------------

def test_steps_complete_and_in_order():
    result = evaluator.check_step_completeness(TEXT_STEPS_COMPLETE)
    assert result["steps_found"]["all_present"] is True
    assert result["steps_found"]["in_order"] is True


def test_steps_out_of_order():
    result = evaluator.check_step_completeness(TEXT_STEPS_OUT_OF_ORDER)
    assert result["steps_found"]["in_order"] is False


def test_steps_incomplete():
    result = evaluator.check_step_completeness(TEXT_STEPS_INCOMPLETE)
    assert result["steps_found"]["all_present"] is False


def test_step_1_contains_accent():
    result = evaluator.check_step_completeness(TEXT_STEPS_COMPLETE)
    assert result["steps_found"]["step_1_accent"] is True


def test_step_2_contains_script():
    result = evaluator.check_step_completeness(TEXT_STEPS_COMPLETE)
    assert result["steps_found"]["step_2_script"] is True


def test_step_3_contains_fraction():
    result = evaluator.check_step_completeness(TEXT_STEPS_COMPLETE)
    assert result["steps_found"]["step_3_fraction"] is True


def test_step_4_contains_radical():
    result = evaluator.check_step_completeness(TEXT_STEPS_COMPLETE)
    assert result["steps_found"]["step_4_radical"] is True


def test_step_5_contains_full_formula():
    result = evaluator.check_step_completeness(TEXT_STEPS_COMPLETE)
    assert result["steps_found"]["step_5_full_formula"] is True