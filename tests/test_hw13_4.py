"""
tests/test_hw13_4.py
Unit tests for HW13_4Evaluator.check_formatting_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from homework.homework_13.hw13_4 import HW13_4Evaluator

evaluator = HW13_4Evaluator()


# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: student pasted the task text before their own answer
TEXT_TASK_DESCRIPTION_PRESENT = """
Using the line of best fit equation created in problem 7, predict the scores for how successful people will be based on how much they study:
a. X = 1.20
b. X = 3.33
c. X = 0.71
d. X = 4.00

a. Ŷ = 2.025 + 0.5746 * 1.20 = 2.714
b. Ŷ = 2.025 + 0.5746 * 3.33 = 3.938
c. Ŷ = 2.025 + 0.5746 * 0.71 = 2.433
d. Ŷ = 2.025 + 0.5746 * 4.00 = 4.323
"""

# TRUE NEGATIVE: well-written answer, no task text pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
a. Ŷ = 2.025 + 0.5746 * 1.20 = 2.714
b. Ŷ = 2.025 + 0.5746 * 3.33 = 3.938
c. Ŷ = 2.025 + 0.5746 * 0.71 = 2.433
d. Ŷ = 2.025 + 0.5746 * 4.00 = 4.323
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
