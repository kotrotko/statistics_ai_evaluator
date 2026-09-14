"""
cw5_4.py
Classwork 5: Sampling Distribution
Section Proportion
Evaluation method name: def grade_cw5_4_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW5_4Evaluator(BaseEvaluator):
    """
    Evaluator for Question 5_4: Larger Section Proportion Under the Normal Curve.

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
        Check if required elements (larger section, z-table interpretation, final proportion) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "larger_section_stated": False,
            "z_table_interpretation_stated": False,
            "final_proportion_stated": False,
        }

        evidence = []

        # Checkpoint 1 — larger section is to the left of z = 0.50
        if re.search(r'left', text_lower) and \
                (re.search(r'0\.50|0\.5\b|z\s*=\s*\.?50', text_lower)):
            elements_found["larger_section_stated"] = True
            evidence.append("Larger section (left of z = 0.50) found")
        else:
            evidence.append("Larger section identification NOT found")

        # Checkpoint 2 — z-table values represent area to the left of the z-score
        if re.search(r'table', text_lower) and re.search(r'area', text_lower) and re.search(r'left', text_lower):
            elements_found["z_table_interpretation_stated"] = True
            evidence.append("z-table interpretation (area to the left) found")
        else:
            evidence.append("z-table interpretation NOT found")

        # Checkpoint 3 — final proportion (0.6915)
        if re.search(r'0\.6915', text_lower):
            elements_found["final_proportion_stated"] = True
            evidence.append("Final proportion (0.6915) found")
        else:
            evidence.append("Final proportion NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_cw5_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 5_4: Larger Section Proportion Under the Normal Curve.
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
                    "component_2_score": 18,
                },
                max_points=20,
                feedback="[TEST MODE] Larger section, z-table interpretation, and final proportion all correctly presented.",
                vibe="Student demonstrates solid understanding of locating proportions under the normal curve",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "larger_section_stated": True,
                            "z_table_interpretation_stated": True,
                            "final_proportion_stated": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["what proportion"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 4. A vertical line is drawn through a normal distribution at z = 0.50, and separates the distribution into two sections. What proportion of the distribution is in the larger section (20 points)?

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

**Component 2: Proportion Description (18 points):**
- 6 points: stating the larger section is to the left of z = 0.50
- 6 points: stating that table values represent area to the left of the z-score
- 6 points: correctly reporting the final proportion as 0.6915
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
Let's imagine that we plot the normal distribution and the vertical line on it. The larger section is to the left hand of z = 0.50. Then we look at the z-scores table. Values in the table represent areas under the curve to the left of Z quantiles along the margins. Let's find z = 0.50 in the table. Corresponding area is 0.6915.

{FEEDBACK_RULES}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-18>,
  "component_2_explanation": "<brief>",
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
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results using OutputFormatter."""
        # Define component labels
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Proportion Description",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 18,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 5_4",
            question_description="Larger Section Proportion Under the Normal Curve",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )