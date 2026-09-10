"""
cw2_5.py
Classwork 2: Distributions and graphs
Radar Chart
Evaluation method name: def grade_cw2_5_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW2_5Evaluator(BaseEvaluator):
    """
    Evaluator for Question 2_5: Dataset Description, Figure 4,
    Circular Scale Interpretation.

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    def __init__(self):
        """Initialize evaluator with API handler."""
        super().__init__()
        # Initialize output formatter
        self.formatter = OutputFormatter(default_width=60)

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check if required elements (figure introduction, radar naming) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "figure_introduced": False,
            "radar_named_correctly": False,
        }

        evidence = []

        # Checkpoint 1 — Figure 4 introduced
        if re.search(r'figure\s*4', text_lower) and \
                re.search(r'presents|shows|displays|below|following', text_lower):
            elements_found["figure_introduced"] = True
            evidence.append("Figure 4 introduction found")
        else:
            evidence.append("Figure 4 introduction NOT found")

        # Checkpoint 2 — diagram named correctly as radar chart
        if re.search(r'radar', text_lower):
            elements_found["radar_named_correctly"] = True
            evidence.append("Radar chart naming found")
        else:
            evidence.append("Radar chart naming NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_cw2_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 2_5: Dataset Description, Figure 4,
        Circular Scale Interpretation.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        # Test mode for verification without API
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_2_score": 5,
                    "component_3_score": 5,
                    "component_4_score": 8,
                },
                max_points=20,
                feedback="[TEST MODE] Dataset description, figure insertion, and interpretation all correctly presented.",
                vibe="Student demonstrates solid understanding of radar chart construction and circular-scale interpretation",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "figure_introduced": True,
                            "radar_named_correctly": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["find your way"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 5. Find your way intuitively: Open the dataset 2.3.1. Radar Chart.xlsx and find the dataset description (5 points). Use it for your introductory phrase and Figure description. Number and title your diagram as 4. Build the regular Radar diagram in Excel (5 points). How the radar diagram transforms a regular chart into a circular scale representation? (10 points).

Total: 20 points

STUDENT ANSWER:
{student_answer}

{IMPORTANT_NOTES}

{IMPORTANT_GRADING_RULES}

**HYBRID GRADING APPROACH:**

**AUTOMATIC FORMATTING DETECTION RESULT:**
Task description correctly formatted (1 point if True): {formatting_check['elements_found']['task_description']}
Proper autoformatting and structure (1 point if True): {formatting_check['elements_found']['autoformatting']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC DETECTION:**
{element_check['elements_found']}

**RUBRIC**

**Component 1: Formatting (2 points):**
Use AUTOMATIC FORMATTING DETECTION RESULT above.
- 1 point: correct task description formatting
- 1 point: proper autoformatting and structure in the solution

**Component 2: Dataset Description (5 points):**
- 3 points: correctly reflecting what the dataset compares (employees across performance dimensions)
- 2 points: stating that a radar chart was created in Excel to visualize and compare performance
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Figure 4 (5 points):**
- 1 point: introductory phrase itself
- 1 point: reference to the figure number in the introductory phrase
- 1 point: figure number
- 1 point: figure title
- 1 point: the figure itself
- NOTE: You cannot visually inspect the actual chart image. Base the "figure itself" point only on textual/structural evidence that a figure was included (e.g., an embedded image marker, caption, or explicit figure reference in the submission) — do not assume presence or correctness of chart content you cannot see.
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Interpretation (8 points):**
- 7 points: correctly explaining how the radar chart transforms a regular chart into a circular scale representation
- 1 point: the diagram being named correctly as a radar chart
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
The dataset compares the performance ratings of three employees (Graham, Barbara, Keith) across five dimensions: Knowledge, Delivery, Effectiveness, Helpful, Punctual. To visualize and compare their performance a radar chart was created in Excel. The diagram is shown in Figure 4. Figure 4 title: Radar Chart of Employee Performance Ratings Across Five Dimensions. A radar chart transforms a regular chart into a circular scale representation by placing each variable on the separate axis extending from the center. Values are connected to create a visual representation of the score patterns.

{FEEDBACK_RULES}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-8>,
  "component_4_explanation": "<brief>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression>"
}}"""

        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "element_check": element_check,
                "formatting_check": formatting_check
            }
        )

        # Force Component 1 (Formatting) deterministically from the regex-based
        # check instead of trusting the LLM's own component_1_score
        if "error" not in result:
            result["component_1_task_score"] = 1 if formatting_check["elements_found"]["task_description"] else 0
            result["component_1_autoformat_score"] = 1 if formatting_check["elements_found"]["autoformatting"] else 0
            result["component_1_score"] = result["component_1_task_score"] + result["component_1_autoformat_score"]

        # If grading succeeded, validate component scores
        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results using OutputFormatter."""
        # Define component labels
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Dataset Description",
            "component_3_score": "Figure 4",
            "component_4_score": "Interpretation",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
            "component_4_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 5,
            "component_3_score": 5,
            "component_4_score": 8,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 2_5",
            question_description="Dataset Description, Figure 4, Circular Scale Interpretation",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )