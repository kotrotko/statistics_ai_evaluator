"""
tests/test_cw14_4.py
Unit tests for CW14_4Evaluator.check_required_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classwork.classwork_14.cw14_4 import CW14_4Evaluator

evaluator = CW14_4Evaluator()


# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: student pasted task wording and gave a full answer
TEXT_TASK_DESCRIPTION_PRESENT = """
Do you need to calculate the Effect Size? Explain why do you think so.
If yes, calculate the Effect Size using Statistics > Nominal > Phi and Cramér's V.

Yes, it is necessary to calculate the effect size. A chi-square test only tells us
whether an association is statistically significant, not how strong it is. With a
large sample size, even trivial differences can reach significance. Reporting
Cramér's V helps assess the practical importance of the result.

Table 3. Effect Size (Cramér's V) for the Association between Physical Activity Level
and Fruit Consumption among College Students

Nominal
              Value
Cramér's V    0.077

Table 3 shows that Cramér's V = 0.077, indicating a weak association between
physical activity level and fruit consumption. Although the chi-square test was
statistically significant, the practical strength of the relationship is small.
"""

# TRUE NEGATIVE: no task wording at all
TEXT_TASK_DESCRIPTION_ABSENT = """
Yes, effect size should be calculated because chi-square does not indicate strength.

Table 3. Effect Size (Cramér's V)

Nominal
              Value
Cramér's V    0.077

The effect size is weak (V = 0.077), meaning the association between the variables
has little practical significance despite being statistically significant.
"""

# TRUE POSITIVE: table with number and title present
TEXT_NOMINAL_TABLE_PRESENT = """
For a chi-square test with more than two categories, Cramér's V should be used (Table 3).

Table 3. Effect Size (Cramér's V) for the Association between Physical Activity Level
and Fruit Consumption among College Students

Nominal
              Value
Cramér's V    0.077
"""

# TRUE NEGATIVE: no table, no mention of Nominal/Phi/Cramér
TEXT_NOMINAL_TABLE_ABSENT = """
Yes, we should calculate the effect size because chi-square does not show strength.
With a large N, even small effects can be significant, so practical importance matters.
"""

# TRUE POSITIVE: Cramér's V value explicitly reported
TEXT_CRAMER_V_VALUE_PRESENT = """
Table 3 shows that the effect size was Cramér's V = 0.077, indicating a weak
association between the variables.
"""

# TRUE NEGATIVE: no numeric value and no mention of Cramér/Phi
TEXT_CRAMER_V_VALUE_ABSENT = """
Yes, effect size should be calculated to assess practical significance.
The chi-square result was statistically significant, but we need to know the strength.
"""

# TRUE POSITIVE: interpretation with magnitude label
TEXT_EFFECT_SIZE_INTERPRETATION_PRESENT = """
Table 3 shows that Cramér's V = 0.077, indicating a weak association between
physical activity level and fruit consumption. Although the chi-square test found
a statistically significant relationship, the practical strength of that
relationship is small.
"""

# TRUE NEGATIVE: value reported with no interpretation at all
TEXT_EFFECT_SIZE_INTERPRETATION_ABSENT = """
Table 3. Nominal

Cramér's V    0.077
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
# Tests: nominal_table
# ---------------------------------------------------------------------------

def test_nominal_table_present():
    result = evaluator.check_required_elements(TEXT_NOMINAL_TABLE_PRESENT)
    assert result["elements_found"]["nominal_table"] is True

def test_nominal_table_absent():
    result = evaluator.check_required_elements(TEXT_NOMINAL_TABLE_ABSENT)
    assert result["elements_found"]["nominal_table"] is False


# ---------------------------------------------------------------------------
# Tests: cramer_v_value
# ---------------------------------------------------------------------------

def test_cramer_v_value_present():
    result = evaluator.check_required_elements(TEXT_CRAMER_V_VALUE_PRESENT)
    assert result["elements_found"]["cramer_v_value"] is True

def test_cramer_v_value_absent():
    result = evaluator.check_required_elements(TEXT_CRAMER_V_VALUE_ABSENT)
    assert result["elements_found"]["cramer_v_value"] is False


# ---------------------------------------------------------------------------
# Tests: effect_size_interpretation
# ---------------------------------------------------------------------------

def test_effect_size_interpretation_present():
    result = evaluator.check_required_elements(TEXT_EFFECT_SIZE_INTERPRETATION_PRESENT)
    assert result["elements_found"]["effect_size_interpretation"] is True

def test_effect_size_interpretation_absent():
    result = evaluator.check_required_elements(TEXT_EFFECT_SIZE_INTERPRETATION_ABSENT)
    assert result["elements_found"]["effect_size_interpretation"] is False
