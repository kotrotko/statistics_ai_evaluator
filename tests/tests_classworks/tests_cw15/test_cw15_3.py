"""
tests/tests_classworks/tests_cw15/test_cw15_3.py
Unit tests for CW15_3Evaluator.check_formatting_elements()
TDD: these tests are written before the evaluator exists.
Tests are isolated — no LLM calls are made.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from classwork.classwork_15.cw15_3 import CW15_3Evaluator

evaluator = CW15_3Evaluator()

# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

# FULL CORRECT ANSWER — used as the baseline "everything present" text
TEXT_FULL_CORRECT = """
Class Work 15
Jane Doe

As shown in Table 5, the communalities and uniqueness values for all items derived
from the promax-rotated exploratory factor analysis indicate the extent to which
each item is explained by the extracted factor structure.

Table 5. Communalities and Uniqueness Values for Items Based on Promax-Rotated Exploratory Factor Analysis

Variable\tUniqueness\tCommunality
x1\t0.523\t0.477
x2\t0.745\t0.255
x3\t0.547\t0.453
x4\t0.272\t0.728
x5\t0.246\t0.754
x6\t0.309\t0.691
x7\t0.481\t0.519
x8\t0.480\t0.520
x9\t0.540\t0.460

Variable with low communality (< .40): x2 (0.255)

Interpretation: Item x2 is poorly explained by the extracted factor structure,
meaning the three-factor model does not adequately capture its variance. This
suggests x2 may not fit well with the underlying constructs and could be a weak
or problematic item in the scale.
"""

# --- task description ---

# TRUE POSITIVE: student pasted the task question before their answer
TEXT_TASK_DESCRIPTION_PRESENT = """
Class Work 15
John Doe
In the Factor Loadings table, find the Uniqueness column. Use it to compute Communality = 1 − Uniqueness for each variable.
"""

# TRUE NEGATIVE: no task text pasted, just the student's own answer
TEXT_TASK_DESCRIPTION_ABSENT = """
Class Work 15
Jane Doe

As shown in Table 5, the communalities and uniqueness values for all items indicate
the extent to which each item is explained by the extracted factor structure.
"""

# --- autoformatting ---

# TRUE NEGATIVE: bullet points detected
TEXT_AUTOFORMATTING_PRESENT = """
Class Work 15
John Doe

- x1: Uniqueness = 0.523, Communality = 0.477
- x2: Uniqueness = 0.745, Communality = 0.255
"""

# TRUE POSITIVE: no bullet points
TEXT_AUTOFORMATTING_ABSENT = TEXT_FULL_CORRECT

# --- introductory phrase ---

# TRUE POSITIVE: answer begins with "As shown in Table 5, ..."
TEXT_INTRO_PHRASE_PRESENT = TEXT_FULL_CORRECT

# TRUE NEGATIVE: table appears without any introductory sentence
TEXT_INTRO_PHRASE_ABSENT = """
Class Work 15
Jane Doe

Table 5. Communalities and Uniqueness Values for Items Based on Promax-Rotated Exploratory Factor Analysis

Variable\tUniqueness\tCommunality
x1\t0.523\t0.477
"""

# --- table number reference in introductory phrase ---

# TRUE POSITIVE: the intro phrase explicitly references "Table 5"
TEXT_TABLE_REF_IN_INTRO_PRESENT = TEXT_FULL_CORRECT

# TRUE NEGATIVE: intro phrase exists but does not mention table number
TEXT_TABLE_REF_IN_INTRO_ABSENT = """
Class Work 15
Jane Doe

The communalities and uniqueness values for all items indicate the extent to which
each item is explained by the extracted factor structure.

Table 5. Communalities and Uniqueness Values for Items Based on Promax-Rotated Exploratory Factor Analysis

Variable\tUniqueness\tCommunality
x1\t0.523\t0.477
"""

# --- table number label ---

# TRUE POSITIVE: text contains "Table 5" as a standalone table label
TEXT_TABLE_NUMBER_PRESENT = TEXT_FULL_CORRECT

# TRUE NEGATIVE: no "Table N" label before the table body
TEXT_TABLE_NUMBER_ABSENT = """
Class Work 15
Jane Doe

As shown in Table 5, the communalities are listed below.

Variable\tUniqueness\tCommunality
x1\t0.523\t0.477
"""

# --- table title ---

# TRUE POSITIVE: table is preceded by a descriptive title line
TEXT_TABLE_TITLE_PRESENT = TEXT_FULL_CORRECT

# TRUE NEGATIVE: "Table 5" label exists but has no title text after it
TEXT_TABLE_TITLE_ABSENT = """
Class Work 15
Jane Doe

As shown in Table 5, the communalities are listed below.

Table 5

Variable\tUniqueness\tCommunality
x1\t0.523\t0.477
"""

# --- table itself (all 9 variables with correct communality values) ---

# TRUE POSITIVE: all 9 rows present with correct Communality = 1 − Uniqueness
TEXT_TABLE_COMPLETE = TEXT_FULL_CORRECT

# TRUE NEGATIVE: only a subset of rows provided
TEXT_TABLE_INCOMPLETE = """
Class Work 15
Jane Doe

As shown in Table 5, the communalities and uniqueness values for all items derived
from the promax-rotated exploratory factor analysis indicate the extent to which
each item is explained by the extracted factor structure.

Table 5. Communalities and Uniqueness Values for Items Based on Promax-Rotated Exploratory Factor Analysis

Variable\tUniqueness\tCommunality
x1\t0.523\t0.477
x2\t0.745\t0.255

Variable with low communality (< .40): x2 (0.255)

Interpretation: Item x2 is poorly explained by the extracted factor structure.
"""

# TRUE NEGATIVE: all 9 rows present but communality values are wrong
TEXT_TABLE_WRONG_VALUES = """
Class Work 15
Jane Doe

As shown in Table 5, the communalities and uniqueness values for all items derived
from the promax-rotated exploratory factor analysis indicate the extent to which
each item is explained by the extracted factor structure.

Table 5. Communalities and Uniqueness Values for Items Based on Promax-Rotated Exploratory Factor Analysis

Variable\tUniqueness\tCommunality
x1\t0.523\t0.500
x2\t0.745\t0.300
x3\t0.547\t0.400
x4\t0.272\t0.700
x5\t0.246\t0.700
x6\t0.309\t0.600
x7\t0.481\t0.500
x8\t0.480\t0.500
x9\t0.540\t0.400

Variable with low communality (< .40): x2 (0.300)

Interpretation: Item x2 is poorly explained by the extracted factor structure.
"""

# --- low communality identification ---

# TRUE POSITIVE: x2 correctly identified as the variable with low communality (< .40)
TEXT_LOW_COMMUNALITY_CORRECT = TEXT_FULL_CORRECT

# TRUE NEGATIVE: low communality section is missing entirely
TEXT_LOW_COMMUNALITY_ABSENT = """
Class Work 15
Jane Doe

As shown in Table 5, the communalities and uniqueness values for all items derived
from the promax-rotated exploratory factor analysis indicate the extent to which
each item is explained by the extracted factor structure.

Table 5. Communalities and Uniqueness Values for Items Based on Promax-Rotated Exploratory Factor Analysis

Variable\tUniqueness\tCommunality
x1\t0.523\t0.477
x2\t0.745\t0.255
x3\t0.547\t0.453
x4\t0.272\t0.728
x5\t0.246\t0.754
x6\t0.309\t0.691
x7\t0.481\t0.519
x8\t0.480\t0.520
x9\t0.540\t0.460

Interpretation: Item x2 is poorly explained by the extracted factor structure.
"""

# TRUE NEGATIVE: wrong variable identified as low communality
TEXT_LOW_COMMUNALITY_WRONG_VAR = """
Class Work 15
Jane Doe

As shown in Table 5, the communalities and uniqueness values for all items derived
from the promax-rotated exploratory factor analysis indicate the extent to which
each item is explained by the extracted factor structure.

Table 5. Communalities and Uniqueness Values for Items Based on Promax-Rotated Exploratory Factor Analysis

Variable\tUniqueness\tCommunality
x1\t0.523\t0.477
x2\t0.745\t0.255
x3\t0.547\t0.453
x4\t0.272\t0.728
x5\t0.246\t0.754
x6\t0.309\t0.691
x7\t0.481\t0.519
x8\t0.480\t0.520
x9\t0.540\t0.460

Variable with low communality (< .40): x1 (0.477)

Interpretation: Item x1 is poorly explained by the extracted factor structure.
"""

# --- interpretation ---

# TRUE POSITIVE: interpretation paragraph is present
TEXT_INTERPRETATION_PRESENT = TEXT_FULL_CORRECT

# TRUE NEGATIVE: no interpretation paragraph
TEXT_INTERPRETATION_ABSENT = """
Class Work 15
Jane Doe

As shown in Table 5, the communalities and uniqueness values for all items derived
from the promax-rotated exploratory factor analysis indicate the extent to which
each item is explained by the extracted factor structure.

Table 5. Communalities and Uniqueness Values for Items Based on Promax-Rotated Exploratory Factor Analysis

Variable\tUniqueness\tCommunality
x1\t0.523\t0.477
x2\t0.745\t0.255
x3\t0.547\t0.453
x4\t0.272\t0.728
x5\t0.246\t0.754
x6\t0.309\t0.691
x7\t0.481\t0.519
x8\t0.480\t0.520
x9\t0.540\t0.460

Variable with low communality (< .40): x2 (0.255)
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
# Tests: no_autoformatting
# ---------------------------------------------------------------------------

def test_autoformatting_detected():
    result = evaluator.check_formatting_elements(TEXT_AUTOFORMATTING_PRESENT)
    assert result["elements_found"]["no_autoformatting"] is False


def test_no_autoformatting():
    result = evaluator.check_formatting_elements(TEXT_AUTOFORMATTING_ABSENT)
    assert result["elements_found"]["no_autoformatting"] is True


# ---------------------------------------------------------------------------
# Tests: introductory phrase
# ---------------------------------------------------------------------------

def test_intro_phrase_present():
    result = evaluator.check_formatting_elements(TEXT_INTRO_PHRASE_PRESENT)
    assert result["elements_found"]["intro_phrase"] is True


def test_intro_phrase_absent():
    result = evaluator.check_formatting_elements(TEXT_INTRO_PHRASE_ABSENT)
    assert result["elements_found"]["intro_phrase"] is False


# ---------------------------------------------------------------------------
# Tests: table number referenced in introductory phrase
# ---------------------------------------------------------------------------

def test_table_ref_in_intro_present():
    result = evaluator.check_formatting_elements(TEXT_TABLE_REF_IN_INTRO_PRESENT)
    assert result["elements_found"]["table_ref_in_intro"] is True


def test_table_ref_in_intro_absent():
    result = evaluator.check_formatting_elements(TEXT_TABLE_REF_IN_INTRO_ABSENT)
    assert result["elements_found"]["table_ref_in_intro"] is False


# ---------------------------------------------------------------------------
# Tests: table number label ("Table 5" appearing before the table body)
# ---------------------------------------------------------------------------

def test_table_number_present():
    result = evaluator.check_formatting_elements(TEXT_TABLE_NUMBER_PRESENT)
    assert result["elements_found"]["table_number"] is True


def test_table_number_absent():
    result = evaluator.check_formatting_elements(TEXT_TABLE_NUMBER_ABSENT)
    assert result["elements_found"]["table_number"] is False


# ---------------------------------------------------------------------------
# Tests: table title (descriptive title following the table number)
# ---------------------------------------------------------------------------

def test_table_title_present():
    result = evaluator.check_formatting_elements(TEXT_TABLE_TITLE_PRESENT)
    assert result["elements_found"]["table_title"] is True


def test_table_title_absent():
    result = evaluator.check_formatting_elements(TEXT_TABLE_TITLE_ABSENT)
    assert result["elements_found"]["table_title"] is False


# ---------------------------------------------------------------------------
# Tests: table completeness (all 9 variables with correct communality values)
# ---------------------------------------------------------------------------

def test_table_complete_and_correct():
    result = evaluator.check_formatting_elements(TEXT_TABLE_COMPLETE)
    assert result["elements_found"]["table_complete"] is True


def test_table_incomplete():
    result = evaluator.check_formatting_elements(TEXT_TABLE_INCOMPLETE)
    assert result["elements_found"]["table_complete"] is False


def test_table_wrong_values():
    result = evaluator.check_formatting_elements(TEXT_TABLE_WRONG_VALUES)
    assert result["elements_found"]["table_complete"] is False


# ---------------------------------------------------------------------------
# Tests: low communality identification
# ---------------------------------------------------------------------------

def test_low_communality_correct():
    result = evaluator.check_formatting_elements(TEXT_LOW_COMMUNALITY_CORRECT)
    assert result["elements_found"]["low_communality"] is True


def test_low_communality_absent():
    result = evaluator.check_formatting_elements(TEXT_LOW_COMMUNALITY_ABSENT)
    assert result["elements_found"]["low_communality"] is False


def test_low_communality_wrong_variable():
    result = evaluator.check_formatting_elements(TEXT_LOW_COMMUNALITY_WRONG_VAR)
    assert result["elements_found"]["low_communality"] is False


# ---------------------------------------------------------------------------
# Tests: interpretation paragraph
# ---------------------------------------------------------------------------

def test_interpretation_present():
    result = evaluator.check_formatting_elements(TEXT_INTERPRETATION_PRESENT)
    assert result["elements_found"]["interpretation"] is True


def test_interpretation_absent():
    result = evaluator.check_formatting_elements(TEXT_INTERPRETATION_ABSENT)
    assert result["elements_found"]["interpretation"] is False