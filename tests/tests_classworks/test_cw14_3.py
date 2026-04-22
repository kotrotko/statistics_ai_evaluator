"""
tests/test_cw14_3.py
Unit tests for CW14_3Evaluator.check_required_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from classwork.classwork_14.cw14_3 import CW14_3Evaluator

evaluator = CW14_3Evaluator()


# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: student pasted task wording
TEXT_TASK_DESCRIPTION_PRESENT = """
Using JASP, perform the χ^2 test of independence. Include the table "Chi-Squared Test", number and name it (10 points).
Make the statistical inference (10 points).

Table 2 presents the results of a chi-square test of independence examining the relationship
between physical activity level and fruit consumption among college students.

Table 2
Chi-Square Test of Independence for Physical Activity Level and Fruit Consumption among College Students

Chi-Squared Tests
          Value   df    p
Χ²        14.152  4     0.007
N         1184

Note. Continuity correction is available only for 2x2 tables.

H₀ should be rejected, because the p-value (p = 0.007) is less than the significance level (α = 0.05).
"""

# TRUE NEGATIVE: student answer only, no task wording pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
Table 2 presents the results of a chi-square test of independence examining the relationship
between physical activity level and fruit consumption among college students.

Table 2
Chi-Square Test of Independence for Physical Activity Level and Fruit Consumption among College Students

Chi-Squared Tests
          Value   df    p
Χ²        14.152  4     0.007
N         1184

Note. Continuity correction is available only for 2x2 tables.

H₀ should be rejected, because the p-value (p = 0.007) is less than the significance level (α = 0.05).
"""

# TRUE POSITIVE: table present with number, title, and chi-square values
TEXT_CHI_SQUARE_TABLE_PRESENT = """
Table 2 presents the results of a chi-square test of independence examining the relationship
between physical activity level and fruit consumption among college students.

Table 2
Chi-Square Test of Independence for Physical Activity Level and Fruit Consumption among College Students

Chi-Squared Tests
          Value   df    p
Χ²        14.152  4     0.007
N         1184

Note. Continuity correction is available only for 2x2 tables.
"""

# TRUE NEGATIVE: no table, no chi-square values
TEXT_CHI_SQUARE_TABLE_ABSENT = """
H₀ should be rejected, because the p-value (p = 0.007) is less than the significance level (α = 0.05).
Therefore, there is a statistically significant association between the variables.
"""

# TRUE POSITIVE: H₀ rejection stated
TEXT_STATISTICAL_INFERENCE_PRESENT = """
H₀ should be rejected, because the p-value (p = 0.007) is less than the significance level (α = 0.05).
"""

# TRUE NEGATIVE: no inference language at all
TEXT_STATISTICAL_INFERENCE_ABSENT = """
Table 2
Chi-Square Test of Independence for Physical Activity Level and Fruit Consumption

Chi-Squared Tests
          Value   df    p
Χ²        14.152  4     0.007
N         1184
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
    # Verify the positive case works too, proving the matcher is not simply always-False
    result_positive = evaluator.check_required_elements(TEXT_TASK_DESCRIPTION_PRESENT)
    assert result_positive["elements_found"]["task_description"] is True


# ---------------------------------------------------------------------------
# Tests: chi_square_table
# ---------------------------------------------------------------------------

def test_chi_square_table_present():
    result = evaluator.check_required_elements(TEXT_CHI_SQUARE_TABLE_PRESENT)
    assert result["elements_found"]["chi_square_table"] is True

def test_chi_square_table_absent():
    result = evaluator.check_required_elements(TEXT_CHI_SQUARE_TABLE_ABSENT)
    assert result["elements_found"]["chi_square_table"] is False


# ---------------------------------------------------------------------------
# Tests: statistical_inference
# ---------------------------------------------------------------------------

def test_statistical_inference_present():
    result = evaluator.check_required_elements(TEXT_STATISTICAL_INFERENCE_PRESENT)
    assert result["elements_found"]["statistical_inference"] is True

def test_statistical_inference_absent():
    result = evaluator.check_required_elements(TEXT_STATISTICAL_INFERENCE_ABSENT)
    assert result["elements_found"]["statistical_inference"] is False
