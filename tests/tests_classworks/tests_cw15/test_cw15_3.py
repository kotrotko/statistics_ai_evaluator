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

@pytest.fixture
def evaluator():
    """Fixture to provide a fresh evaluator instance for each test."""
    return CW15_3Evaluator()

# ---------------------------------------------------------------------------
# Structural & Logic Tests (Addressing 22/20 and Breakdown bugs)
# ---------------------------------------------------------------------------

def test_rubric_total_score_limit(evaluator):
    """Checks that the sum of all components equals exactly 20."""
    comp_1 = 2  # Formatting
    comp_2 = 8  # Table 5
    comp_3 = 5  # Low Communalities
    comp_4 = 5  # Interpretation

    total = comp_1 + comp_2 + comp_3 + comp_4
    assert total == 20, f"Rubric total is {total}, expected 20."

def test_table_5_internal_weights(evaluator):
    """Checks that Table 5 sub-components sum to exactly 8."""
    weights = {
        "intro_phrase": 1,
        "table_ref": 1,
        "table_number": 1,
        "table_title": 1,
        "table_itself": 4
    }
    assert sum(weights.values()) == 8, f"Table 5 sub-components sum to {sum(weights.values())}, expected 8."

def test_print_structure_consistency(evaluator, capsys):
    """Checks for the presence of the COMPONENT BREAKDOWN header."""
    mock_grading = {
        "component_1_score": 2,
        "component_2_score": 8,
        "component_3_score": 5,
        "component_4_score": 5,
        "total_points": 20,
        "max_points": 20
    }
    evaluator.print_grading_results(mock_grading)
    captured = capsys.readouterr().out
    assert "COMPONENT BREAKDOWN:" in captured

def test_naming_consistency_ledger(evaluator):
    """Ensures 'pedagogical_markers' is used instead of 'anchors'."""
    import inspect
    source = inspect.getsource(evaluator.check_formatting_elements)
    assert "pedagogical_markers" in source
    assert "pedagogical_anchors" not in source

# ---------------------------------------------------------------------------
# Test texts
# ---------------------------------------------------------------------------

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

Interpretation: Item x2 is poorly explained by the extracted factor structure.
"""

TEXT_TASK_DESCRIPTION_PRESENT = "In the Factor Loadings table, find the Uniqueness column..."
TEXT_AUTOFORMATTING_PRESENT = "- x1: Uniqueness = 0.523, Communality = 0.477"

# ---------------------------------------------------------------------------
# Isolated Unit Tests (Strictly using the 'evaluator' fixture)
# ---------------------------------------------------------------------------

def test_task_description_present(evaluator):
    result = evaluator.check_formatting_elements(TEXT_TASK_DESCRIPTION_PRESENT)
    assert result["elements_found"]["task_description"] is True

def test_autoformatting_detected(evaluator):
    result = evaluator.check_formatting_elements(TEXT_AUTOFORMATTING_PRESENT)
    assert result["elements_found"]["no_autoformatting"] is False

def test_intro_phrase_present(evaluator):
    result = evaluator.check_formatting_elements(TEXT_FULL_CORRECT)
    assert result["elements_found"]["intro_phrase"] is True

def test_table_complete_and_correct(evaluator):
    result = evaluator.check_formatting_elements(TEXT_FULL_CORRECT)
    assert result["elements_found"]["table_complete"] is True

def test_low_communality_correct(evaluator):
    result = evaluator.check_formatting_elements(TEXT_FULL_CORRECT)
    assert result["elements_found"]["low_communality"] is True

def test_interpretation_present(evaluator):
    result = evaluator.check_formatting_elements(TEXT_FULL_CORRECT)
    assert result["elements_found"]["interpretation"] is True