"""
cw4_5.py
Classwork 4: Probability and Normal Distribution
Familywise Error
Evaluation method name: def grade_cw4_5_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW4_5Evaluator(BaseEvaluator):
    """
    Evaluator for Question 4_5: Familywise Error, Independence Explanation,
    Probability Calculation Steps.

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
        Check if required elements (Step 1, Step 2, Step 3 values) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "step1_value_stated": False,
            "step2_value_stated": False,
            "step3_value_stated": False,
        }

        evidence = []

        # Checkpoint 1 — Step 1 value (.95)
        if re.search(r'0?\.95\b', text_lower):
            elements_found["step1_value_stated"] = True
            evidence.append("Step 1 value (.95) found")
        else:
            evidence.append("Step 1 value (.95) NOT found")

        # Checkpoint 2 — Step 2 value (.735)
        if re.search(r'0?\.735\b', text_lower):
            elements_found["step2_value_stated"] = True
            evidence.append("Step 2 value (.735) found")
        else:
            evidence.append("Step 2 value (.735) NOT found")

        # Checkpoint 3 — Step 3 value (.265 or 26.5%)
        if re.search(r'0?\.265\b', text_lower) or re.search(r'26\.5', text_lower):
            elements_found["step3_value_stated"] = True
            evidence.append("Step 3 value (.265 / 26.5%) found")
        else:
            evidence.append("Step 3 value (.265 / 26.5%) NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_cw4_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 4_5: Familywise Error — Independence Explanation and
        Probability Calculation Steps.
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
                    "component_4_score": 4,
                    "component_5_score": 4,
                },
                max_points=20,
                feedback="[TEST MODE] Independence explanation and all calculation steps correctly presented.",
                vibe="Student demonstrates solid understanding of independence and the complement rule",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "step1_value_stated": True,
                            "step2_value_stated": True,
                            "step3_value_stated": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["please explain"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 5. Familywise Error. A researcher wants to compare the mean anxiety levels across four therapy groups: CBT, psychoanalysis, anxiolytics, and control group. They plan to perform six pairwise comparisons between the groups. If the chance of making a mistake in one comparison is 5%, and the comparisons are independent, what is the probability of making at least one mistake across all six comparisons?
Before solving, please explain the concept of independence of the pairwise comparisons (5 points). Then, show your logic in the following steps, briefly stating what each calculation represents before performing it — a stated explanation of what the number represents is valued over a bare calculation alone: Step 1. Find the probability of making no mistake in one comparison (5 points). Step 2. Find the probability of making no mistakes across all six comparisons (5 points). Step 3. Find the probability of making at least one mistake, using the complement of Step 2 (5 points).

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

**Component 2: Independence Explanation (5 points):**
- 5 points: correctly explaining the concept of independence of the pairwise comparisons
- CRITICAL: Do NOT assume the explanation is present if not explicitly written in the student's text

**Component 3: Step 1 (5 points):**
- 3 points: stating what the calculation represents before performing it
- 2 points: correctly finding the probability of making no mistake in one comparison
- Use AUTOMATIC DETECTION above (step1_value_stated) as evidence for the calculation sub-point
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Step 2 (4 points):**
- 2 points: stating what the calculation represents before performing it
- 2 points: correctly finding the probability of making no mistakes across all six comparisons
- Use AUTOMATIC DETECTION above (step2_value_stated) as evidence for the calculation sub-point
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: Step 3 (4 points):**
- 2 points: stating what the calculation represents before performing it
- 2 points: correctly finding the probability of making at least one mistake using the complement of Step 2
- Use AUTOMATIC DETECTION above (step3_value_stated) as evidence for the calculation sub-point
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
The pairwise comparisons are independent when the outcome of one comparison does not affect or change the probability of any other comparison resulting in an error. Knowing whether one comparison contains an error gives no information about whether another comparison does. Step 1. The probability of making no mistake in one comparison is 1 – .05 = .95. Step 2. Since the comparisons are independent, the probability of making no mistakes across all six comparisons is .95⁶ = .735. Step 3. The probability of making at least one mistake is the complement of Step 2: 1 – .735 = .265, or 26.5%.

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
  "component_4_score": <0-4>,
  "component_4_explanation": "<brief>",
  "component_5_score": <0-4>,
  "component_5_explanation": "<brief>",
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
                "component_5_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results using OutputFormatter."""
        # Define component labels
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Independence Explanation",
            "component_3_score": "Step 1",
            "component_4_score": "Step 2",
            "component_5_score": "Step 3",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
            "component_4_score": "HYBRID",
            "component_5_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 5,
            "component_3_score": 5,
            "component_4_score": 4,
            "component_5_score": 4,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 4_5",
            question_description="Familywise Error, Independence Explanation, Probability Calculation Steps",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )