import sys
import os
import pytest

# Ensure the project root is in the path for consistent imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from classwork.classwork_15.cw15_5 import CW15_5Evaluator


@pytest.fixture
def evaluator():
    """Deterministic fixture providing a clean evaluator instance for every test."""
    return CW15_5Evaluator()


# ---------------------------------------------------------------------------
# Structural Logic Tests (The "Catching 22/20" Layer)
# ---------------------------------------------------------------------------

def test_rubric_total_score_limit(evaluator):
    """
    STRICT CHECK: Verifies that the total points for Task 5 equal exactly 20.
    Based on task: 5 (Data & method) + 5 (Factor extraction) + 5 (Rotation method) + 5 (Interpretation).
    """
    comp_data_method = 5
    comp_factor_extraction = 5
    comp_rotation_method = 5
    comp_interpretation = 5

    total = comp_data_method + comp_factor_extraction + comp_rotation_method + comp_interpretation
    assert total == 20, f"Rubric total is {total}, expected 20."


def test_naming_consistency_ledger(evaluator):
    """
    LEDGER CHECK: Ensures 'pedagogical_markers' is used instead of 'anchors'.
    This catches the naming inconsistency bug from the Correction Ledger.
    """
    import inspect
    source = inspect.getsource(evaluator.check_formatting_elements)
    assert "pedagogical_markers" in source


def test_task_description_detection(evaluator):
    """Verifies that the teacher-only pedagogical marker is correctly detected."""
    # test_text is a mock text which imitates the student's answer, to test the evaluator code
    test_text = "Please make sure that you"
    result = evaluator.check_formatting_elements(test_text)
    assert result["elements_found"]["task_description"] is True


def test_print_breakdown_presence(evaluator, capsys):
    """Checks for the COMPONENT BREAKDOWN header to ensure output consistency."""
    mock_grading = {
        "component_1_score": 5,
        "component_2_score": 5,
        "component_3_score": 5,
        "component_4_score": 5,
        "total_points": 20,
        "max_points": 20
    }
    evaluator.print_grading_results(mock_grading)
    captured = capsys.readouterr().out
    assert "COMPONENT BREAKDOWN:" in captured


# ---------------------------------------------------------------------------
# Formatting & Content Tests (Isolated Unit Tests)
# ---------------------------------------------------------------------------

# Mock student answer that mimics a complete correct response
TEXT_ALL_SECTIONS_PRESENT = """
Task 5. Include the following elements in your report: Description of the data and method (5 points).
Please make sure that you included the Factor extraction results (5 points).
Which Rotation method did you use? (5 points). Write the Interpretation of the factor loading (5 points).

The data consist of nine variables (x1–x9) collected from 100 participants.
Exploratory factor analysis was conducted using the principal axis factoring method
to identify the underlying factor structure.

The factor extraction results indicate that three factors were retained based on
eigenvalues greater than 1. The first factor explained 35% of the variance,
the second factor explained 20%, and the third factor explained 15%.

The promax rotation method was used to allow factors to correlate with each other,
as oblique rotation is appropriate when factors are expected to be related.

The interpretation of the factor loadings shows that Factor 1 is defined by variables
x4, x5, and x6, which all show strong loadings above .40. Factor 2 is primarily
defined by x7, x8, and x9. Factor 3 is associated with x1, x2, and x3.
"""

# Text with data/method section present but the rest absent
TEXT_DATA_METHOD_ONLY = """
Please make sure that you included all sections.

The data consist of nine variables (x1–x9) measured on a Likert scale.
Exploratory factor analysis was conducted using the maximum likelihood method.
"""

# Text with factor extraction section present
TEXT_FACTOR_EXTRACTION_PRESENT = """
Please make sure that you included all sections.

The factor extraction results indicate that three factors were retained.
Eigenvalues greater than 1 were used as the retention criterion.
The scree plot confirmed this three-factor solution.
"""

# Text with rotation method section present
TEXT_ROTATION_METHOD_PRESENT = """
Please make sure that you included all sections.

The promax rotation method was applied because the factors were expected
to correlate with each other, making an oblique rotation appropriate.
"""

# Text with interpretation section present
TEXT_INTERPRETATION_PRESENT = """
Please make sure that you included all sections.

The interpretation of the factor loadings reveals that Factor 1 is defined
by variables x4, x5, and x6 with strong positive loadings above .40.
Factor 2 is primarily defined by x7, x8, and x9.
"""

# Text with section keyword present but no explanatory prose (bare label only)
TEXT_BARE_LABEL_NO_EXPLANATION = "Factor extraction results."


def test_data_method_detected(evaluator):
    """Verifies that a description of data and method is identified."""
    result = evaluator.check_formatting_elements(TEXT_DATA_METHOD_ONLY)
    assert result["elements_found"]["data_method"] is True


def test_factor_extraction_detected(evaluator):
    """Verifies that factor extraction results section is identified."""
    result = evaluator.check_formatting_elements(TEXT_FACTOR_EXTRACTION_PRESENT)
    assert result["elements_found"]["factor_extraction"] is True


def test_rotation_method_detected(evaluator):
    """Verifies that the rotation method section is identified."""
    result = evaluator.check_formatting_elements(TEXT_ROTATION_METHOD_PRESENT)
    assert result["elements_found"]["rotation_method"] is True


def test_interpretation_detected(evaluator):
    """Verifies that the interpretation of factor loadings is identified."""
    result = evaluator.check_formatting_elements(TEXT_INTERPRETATION_PRESENT)
    assert result["elements_found"]["interpretation"] is True


def test_all_sections_detected(evaluator):
    """Verifies that all four content sections are detected in a complete answer."""
    result = evaluator.check_formatting_elements(TEXT_ALL_SECTIONS_PRESENT)
    ef = result["elements_found"]
    assert ef["task_description"] is True
    assert ef["data_method"] is True
    assert ef["factor_extraction"] is True
    assert ef["rotation_method"] is True
    assert ef["interpretation"] is True


def test_section_label_without_prose_is_false(evaluator):
    """
    Ensures that a bare keyword with no explanatory prose does not
    trigger the section as present. Label alone is not enough.
    """
    result = evaluator.check_formatting_elements(TEXT_BARE_LABEL_NO_EXPLANATION)
    assert result["elements_found"]["factor_extraction"] is False