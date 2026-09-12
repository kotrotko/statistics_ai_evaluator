"""
cw4_4.py
Classwork 4: Normal Distribution
Percentage of students, standard deviations
Evaluation method name: def grade_cw4_4_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW4_4Evaluator(BaseEvaluator):
    """
    Evaluator for Question 4_4: Percentage of students, standard deviations.

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
        Check if required elements (Part a percentage/context, Part b percentage/context) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "part_a_percentage_stated": False,
            "part_a_gpa_context_stated": False,
            "part_b_percentage_stated": False,
            "part_b_gpa_context_stated": False,
        }

        evidence = []

        # Checkpoint 1 — Part a percentage (2.15%)
        if re.search(r'2\.15', text_lower):
            elements_found["part_a_percentage_stated"] = True
            evidence.append("Part a percentage (2.15%) found")
        else:
            evidence.append("Part a percentage (2.15%) NOT found")

        # Checkpoint 2 — Part a GPA context
        if re.search(r'gpa', text_lower):
            elements_found["part_a_gpa_context_stated"] = True
            evidence.append("GPA context found (Part a)")
        else:
            evidence.append("GPA context NOT found (Part a)")

        # Checkpoint 3 — Part b percentage (0.13%)
        if re.search(r'0\.13', text_lower):
            elements_found["part_b_percentage_stated"] = True
            evidence.append("Part b percentage (0.13%) found")
        else:
            evidence.append("Part b percentage (0.13%) NOT found")

        # Checkpoint 4 — Part b GPA context
        if re.search(r'gpa', text_lower):
            elements_found["part_b_gpa_context_stated"] = True
            evidence.append("GPA context found (Part b)")
        else:
            evidence.append("GPA context NOT found (Part b)")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_cw4_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 4_4: Percentage of students, standard deviations.
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
                    "component_2_score": 9,
                    "component_3_score": 9,
                },
                max_points=20,
                feedback="[TEST MODE] Both percentages correctly calculated and stated in context.",
                vibe="Student demonstrates solid understanding of standard normal distribution proportions",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "part_a_percentage_stated": True,
                            "part_a_gpa_context_stated": True,
                            "part_b_percentage_stated": True,
                            "part_b_gpa_context_stated": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["please find"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 4. Percentage of students, standard deviations. Please find, what percentage of students theoretically should have a GPA, according to theoretical distribution: a. between 2 and 3 standard deviations? b. between 3 and 4?

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

**Component 2: Part a (2–3 SD) (9 points):**
- 5 points: the correct percentage calculated using the correct mean-to-2-SD and mean-to-3-SD proportions
- 4 points: a complete sentence stating the result in context of GPA
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Part b (3–4 SD) (9 points):**
- 5 points: the correct percentage calculated using the correct mean-to-3-SD and mean-to-4-SD proportions
- 4 points: a complete sentence stating the result in context of GPA
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
We use the known percentages of scores that fall under different portions of a theoretical (normal) distribution. These percentages come from the standard normal distribution table, which tells us what proportion of scores falls between the mean and a given number of standard deviations away from it. The relevant proportions (from the mean out to each point) are: mean to 2 standard deviations away: 47.72%; mean to 3 standard deviations away: 49.87%; mean to 4 standard deviations away: approximately 49.997%. For Part a, subtracting the smaller area from the larger one: 49.87% − 47.72% = 2.15%. So, theoretically, about 2.15% of students should have a GPA that falls between 2 and 3 standard deviations from the mean. For Part b, using the same approach: 49.997% − 49.87% = 0.13%. So, theoretically, about 0.13% of students should have a GPA that falls between 3 and 4 standard deviations from the mean.

{FEEDBACK_RULES}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-9>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-9>,
  "component_3_explanation": "<brief>",
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
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results using OutputFormatter."""
        # Define component labels
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Part a (2-3 SD)",
            "component_3_score": "Part b (3-4 SD)",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 9,
            "component_3_score": 9,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 4_4",
            question_description="Percentage of students, standard deviations",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )