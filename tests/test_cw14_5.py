"""
tests/test_cw14_5.py
Unit tests for CW14_5Evaluator.check_required_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classwork.classwork_14.cw14_5 import CW14_5Evaluator

evaluator = CW14_5Evaluator()


# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# TRUE POSITIVE: student pasted task wording
TEXT_TASK_DESCRIPTION_PRESENT = """
Describe your output briefly. Follow the APA style you learned before. (5 points).
Answer the main research question: Are physical activity and fruit consumption independent?
What do you think about causation?

A chi-square test of independence showed a statistically significant association between
physical activity level and fruit consumption among college students,
χ²(4, N = 1184) = 14.15, p = .007. Therefore, physical activity level and fruit
consumption are not independent. No conclusion about causation can be made from this
analysis.
"""

# TRUE NEGATIVE: student answer only, no task wording pasted
TEXT_TASK_DESCRIPTION_ABSENT = """
A chi-square test of independence showed a statistically significant association between
physical activity level and fruit consumption among college students,
χ²(4, N = 1184) = 14.15, p = .007. Therefore, physical activity level and fruit
consumption are not independent. No conclusion about causation can be made from this
analysis.
"""

# TRUE POSITIVE: APA-style output with chi-square notation, df, N, and p-value
TEXT_APA_OUTPUT_PRESENT = """
A chi-square test of independence showed a statistically significant association between
physical activity level and fruit consumption among college students,
χ²(4, N = 1184) = 14.15, p = .007.
"""

# TRUE NEGATIVE: result described in plain language, no APA notation
TEXT_APA_OUTPUT_ABSENT = """
The test showed that there is a significant relationship between physical activity
and fruit consumption. The p-value was small so we reject the null hypothesis.
"""

# TRUE POSITIVE: research question answered with correct conclusion marker
TEXT_RESEARCH_QUESTION_PRESENT = """
Therefore, physical activity level and fruit consumption are not independent,
they are related, but the association is not strong among college students.
"""

# TRUE NEGATIVE: no conclusion marker present
TEXT_RESEARCH_QUESTION_ABSENT = """
The chi-square test showed a statistically significant result (p = .007).
We can conclude that there is an association between the two variables.
"""

# TRUE POSITIVE: causation conclusion present
TEXT_CAUSATION_PRESENT = """
No conclusion about causation can be made from this analysis. A chi-square test
identifies association, not cause-and-effect relationships.
"""

# TRUE NEGATIVE: no causation language present
TEXT_CAUSATION_ABSENT = """
Physical activity level and fruit consumption are not independent. The association
between the two variables was statistically significant, χ²(4, N = 1184) = 14.15, p = .007.
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
# Tests: apa_output
# ---------------------------------------------------------------------------

def test_apa_output_present():
    result = evaluator.check_required_elements(TEXT_APA_OUTPUT_PRESENT)
    assert result["elements_found"]["apa_output"] is True

def test_apa_output_absent():
    result = evaluator.check_required_elements(TEXT_APA_OUTPUT_ABSENT)
    assert result["elements_found"]["apa_output"] is False


# ---------------------------------------------------------------------------
# Tests: research_question
# ---------------------------------------------------------------------------

def test_research_question_present():
    result = evaluator.check_required_elements(TEXT_RESEARCH_QUESTION_PRESENT)
    assert result["elements_found"]["research_question"] is True

def test_research_question_absent():
    result = evaluator.check_required_elements(TEXT_RESEARCH_QUESTION_ABSENT)
    assert result["elements_found"]["research_question"] is False


# ---------------------------------------------------------------------------
# Tests: causation
# ---------------------------------------------------------------------------

def test_causation_present():
    result = evaluator.check_required_elements(TEXT_CAUSATION_PRESENT)
    assert result["elements_found"]["causation"] is True

def test_causation_absent():
    result = evaluator.check_required_elements(TEXT_CAUSATION_ABSENT)
    assert result["elements_found"]["causation"] is False
