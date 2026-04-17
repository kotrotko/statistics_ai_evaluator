"""
tests/test_hw13_3.py
Unit tests for HW13_3Evaluator.check_formatting_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from homework.homework_13.hw13_3 import HW13_3Evaluator

evaluator = HW13_3Evaluator()


# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: student pasted the task text before their own answer
TEXT_TASK_DESCRIPTION_PRESENT = """
Fill out the rest of the ANOVA tables below for simple linear regressions:
 
a. SS Model = 34.21, SS Total = 66.12, df Total = 54
df Model = 1, df Error = 53, SS Error = 31.91, MS Model = 34.21, MS Error = 0.602, F = 56.83
 
b. MS Model = 6.03, df Error = 16, SS Total = 19.98
df Model = 1, df Total = 17, SS Model = 6.03, SS Error = 13.95, MS Error = 0.872, F = 6.91
 
Both models are significant at α = 0.05 because F exceeds the critical value.
"""

# TRUE NEGATIVE: well-written answer, no task text pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
a. df Model = 1, df Error = 53, SS Error = 31.91, MS Model = 34.21, MS Error = 0.602, F = 56.83
 
b. df Model = 1, df Total = 17, SS Model = 6.03, SS Error = 13.95, MS Error = 0.872, F = 6.91
 
Both models are significant at α = 0.05 because F exceeds the critical value.
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