"""
hw13_4.py
Homework 13: Linear Regression
Predicting scores from the line of best fit
Evaluation method name: def grade_hw13_4_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2


class HW13_4Evaluator(BaseEvaluator):
    """
    Evaluator for Homework 13 Task 4.

    Task: Using the line of best fit equation created in problem 7, predict
    the scores for how successful people will be based on how much they
    study: a. X = 1.20 b. X = 3.33 c. X = 0.71 d. X = 4.00

    Formatting (2 points: task description, no autoformatting).
    Formula application (2 points: Ŷ = 2.024 + 0.575X correctly applied).
    Solution a (4 points: X = 1.20, Ŷ ≈ 2.714).
    Solution b (4 points: X = 3.33, Ŷ ≈ 3.939).
    Solution c (4 points: X = 0.71, Ŷ ≈ 2.432).
    Solution d (4 points: X = 4.00, Ŷ ≈ 4.324).

    Inherits common functionality from BaseEvaluator.
    """

    def __init__(self):
        """Initialize the evaluator with API handler."""
        super().__init__()
        self.formatter = OutputFormatter(default_width=60)

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check if required content elements are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "formula_applied": False,
            "solution_a_present": False,
            "solution_b_present": False,
            "solution_c_present": False,
            "solution_d_present": False,
        }

        evidence = []

        # Checkpoint 1 — Formula application
        if re.search(r'2\.024|0\.575|ŷ\s*=|y-hat\s*=|y\s*hat\s*=', text_lower):
            elements_found["formula_applied"] = True
            evidence.append("Formula application found")
        else:
            evidence.append("Formula application NOT found")

        # Checkpoint 2 — Solution a (X = 1.20)
        if re.search(r'1\.20|1\.2\b', text_lower):
            elements_found["solution_a_present"] = True
            evidence.append("Solution a found")
        else:
            evidence.append("Solution a NOT found")

        # Checkpoint 3 — Solution b (X = 3.33)
        if re.search(r'3\.33', text_lower):
            elements_found["solution_b_present"] = True
            evidence.append("Solution b found")
        else:
            evidence.append("Solution b NOT found")

        # Checkpoint 4 — Solution c (X = 0.71)
        if re.search(r'0\.71\b', text_lower):
            elements_found["solution_c_present"] = True
            evidence.append("Solution c found")
        else:
            evidence.append("Solution c NOT found")

        # Checkpoint 5 — Solution d (X = 4.00)
        if re.search(r'4\.00|4\.0\b', text_lower):
            elements_found["solution_d_present"] = True
            evidence.append("Solution d found")
        else:
            evidence.append("Solution d NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_hw13_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Homework 13.4: Predicting scores from the line of best fit.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_1_task_score": 1,
                    "component_1_autoformat_score": 1,
                    "component_2_score": 2,
                    "component_3_score": 4,
                    "component_4_score": 4,
                    "component_5_score": 4,
                    "component_6_score": 4,
                },
                max_points=20,
                feedback="[TEST MODE] Formula correctly applied, all four predictions correct.",
                vibe="Student correctly applies the line of best fit equation to all four predictions.",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "formula_applied": True,
                            "solution_a_present": True,
                            "solution_b_present": True,
                            "solution_c_present": True,
                            "solution_d_present": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)
        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=[]
        )

        prompt = f"""You are grading a statistics assignment about applying a line of best fit equation to predict scores using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
Using the line of best fit equation created in problem 7, predict the scores for how successful people will be based on how much they study: a. X = 1.20 b. X = 3.33 c. X = 0.71 d. X = 4.00

Total: 20 points

STUDENT ANSWER:
{student_answer}

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Reasoning is required; calculations are mandatory
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. It is expected to see both student's logic and calculations, not only the final answer
6. Explanations must be SPECIFIC and ACTIONABLE - avoid vague phrases like "lacks depth", "could be better", "needs improvement". Instead, point to what is actually missing or what was done well.
7. Allow reasonable rounding freedom when checking numeric answers; do not penalize minor rounding differences.

**HYBRID GRADING APPROACH:**

**AUTOMATIC FORMATTING DETECTION RESULT:**
Task description correctly formatted (1 point if True): {formatting_check['elements_found']['task_description']}
Proper autoformatting and structure (1 point if True): {formatting_check['elements_found']['autoformatting']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC DETECTION:**
{element_check['elements_found']}

**RUBRIC:**

**Component 1: Formatting (2 points):**
Use AUTOMATIC FORMATTING DETECTION RESULT above.
- 1 point: Task description correctly formatted
- 1 point: Proper autoformatting and structure

**Component 2: Formula Application (2 points):**
Use AUTOMATIC DETECTION above (formula_applied).
- 2 points: Line of best fit formula Ŷ = 2.024 + 0.575X correctly applied
- 0 points: Formula not applied or applied incorrectly
- Rounding freedom allowed on coefficients

**Component 3: Solution a (4 points):**
Use AUTOMATIC DETECTION above (solution_a_present).
- 4 points: X = 1.20, Ŷ ≈ 2.714 (rounding freedom allowed)
- 0 points: Incorrect or absent

**Component 4: Solution b (4 points):**
Use AUTOMATIC DETECTION above (solution_b_present).
- 4 points: X = 3.33, Ŷ ≈ 3.939 (rounding freedom allowed)
- 0 points: Incorrect or absent

**Component 5: Solution c (4 points):**
Use AUTOMATIC DETECTION above (solution_c_present).
- 4 points: X = 0.71, Ŷ ≈ 2.432 (rounding freedom allowed)
- 0 points: Incorrect or absent

**Component 6: Solution d (4 points):**
Use AUTOMATIC DETECTION above (solution_d_present).
- 4 points: X = 4.00, Ŷ ≈ 4.324 (rounding freedom allowed)
- 0 points: Incorrect or absent

**FEEDBACK RULES**
- Identify which components were completed correctly
- Point out missing or incomplete elements explicitly
- Maintain supportive tone

---

Return JSON only:
{{
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-2>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-4>,
  "component_4_explanation": "<brief>",
  "component_5_score": <0-4>,
  "component_5_explanation": "<brief>",
  "component_6_score": <0-4>,
  "component_6_explanation": "<brief>",
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative feedback>",
  "vibe": "<one-sentence overall impression>"
}}
"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "element_check": element_check,
                "formatting_check": formatting_check
            }
        )

        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score",
                "component_5_score",
                "component_6_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """
        Display grading results using OutputFormatter.

        Args:
            grading: Grading result dictionary
        """
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Formula Application",
            "component_3_score": "Solution a",
            "component_4_score": "Solution b",
            "component_5_score": "Solution c",
            "component_6_score": "Solution d",
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT",
            "component_5_score": "STRICT",
            "component_6_score": "STRICT",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 2,
            "component_3_score": 4,
            "component_4_score": 4,
            "component_5_score": 4,
            "component_6_score": 4,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="HOMEWORK 13_4",
            question_description="Predicting Scores from the Line of Best Fit",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="STRICT"
        )