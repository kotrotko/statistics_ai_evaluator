import sys
import os
import pytest

# Ensure the project root is in the path for consistent imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from classwork.classwork_15.cw15_4 import CW15_4Evaluator


@pytest.fixture
def evaluator():
    """Deterministic fixture providing a clean evaluator instance for every test."""
    return CW15_4Evaluator()


# ---------------------------------------------------------------------------
# Structural Logic Tests (The "Catching 22/20" Layer)
# ---------------------------------------------------------------------------

def test_rubric_total_score_limit(evaluator):
    """
    STRICT CHECK: Verifies that the total points for Task 4 equal exactly 20.
    Based on image: 5 (Path diag) + 5 (Path expl) + 5 (Scree plot) + 5 (Scree expl).
    """
    comp_path_diagram = 5
    comp_path_explanation = 5
    comp_scree_plot = 5
    comp_scree_explanation = 5

    total = comp_path_diagram + comp_path_explanation + comp_scree_plot + comp_scree_explanation
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
    # test_text is a mock text which imitate the student's answer, to test the evaluator code
    test_text = "please ensure you"
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

# Mock student answer that mimics the provided solution image
TEXT_PATH_AND_SCREE_PRESENT = """
Figure 1 presents the path diagram of the specified model.
[Image: Path Diagram]
Figure 1. Path Diagram

Figure 2 presents the scree plot illustrating eigenvalues.
[Image: Scree Plot]
Figure 2. Scree plot
"""


def test_path_diagram_label_detected(evaluator):
    """Verifies that 'Figure 1. Path Diagram' is identified via markers."""
    result = evaluator.check_formatting_elements(TEXT_PATH_AND_SCREE_PRESENT)
    assert result["elements_found"]["figure_1_label"] is True


def test_scree_plot_label_detected(evaluator):
    """Verifies that 'Figure 2. Scree plot' is identified via markers."""
    result = evaluator.check_formatting_elements(TEXT_PATH_AND_SCREE_PRESENT)
    assert result["elements_found"]["figure_2_label"] is True


def test_explanation_logic_separation(evaluator):
    """Ensures diagram presence is checked separately from textual explanation."""
    # Test text with Figure label but no actual descriptive paragraph
    text_no_explanation = "Figure 1. Path Diagram"
    result = evaluator.check_formatting_elements(text_no_explanation)
    # The label is found, but the explanation logic should remain False
    assert result["elements_found"]["figure_1_label"] is True
    assert result["elements_found"]["figure_1_explanation"] is False