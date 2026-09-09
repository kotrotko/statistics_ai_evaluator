"""
hw13_1.py
Homework 13: Linear Regression
Residuals: name, definition, formula, interpretation
Evaluation method name: def grade_hw13_1_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2


class HW13_1Evaluator(BaseEvaluator):
    """
    Evaluator for Homework 13 Task 1.

    Task: What is a residual?

    Formatting (4 points: name, paper title, task description, no
    autoformatting).
    Definition (6 points: residual as the difference between observed and
    predicted value).
    Formula (5 points: Residual = Y − Ŷ).
    Interpretation (5 points: positive residual, negative residual,
    residual = 0).

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
            "definition": False,
            "formula": False,
            "positive_residual": False,
            "negative_residual": False,
            "zero_residual": False,
        }

        evidence = []

        # Checkpoint 1 — Definition
        if re.search(r'difference\s*between.*observed.*predicted|difference\s*between.*actual.*predicted|observed\s*value.*predicted\s*value', text_lower):
            elements_found["definition"] = True
            evidence.append("Definition found")
        else:
            evidence.append("Definition NOT found")

        # Checkpoint 2 — Formula
        if re.search(r'residual\s*=\s*y|y\s*-\s*ŷ|y\s*−\s*ŷ|y\s*minus\s*ŷ', text_lower):
            elements_found["formula"] = True
            evidence.append("Formula found")
        else:
            evidence.append("Formula NOT found")

        # Checkpoint 3 — Positive residual
        if re.search(r'positive\s*residual', text_lower):
            elements_found["positive_residual"] = True
            evidence.append("Positive residual interpretation found")
        else:
            evidence.append("Positive residual interpretation NOT found")

        # Checkpoint 4 — Negative residual
        if re.search(r'negative\s*residual', text_lower):
            elements_found["negative_residual"] = True
            evidence.append("Negative residual interpretation found")
        else:
            evidence.append("Negative residual interpretation NOT found")

        # Checkpoint 5 — Residual = 0
        if re.search(r'residual\s*=\s*0|residual.{0,15}zero|exact\s*prediction|prediction\s*is\s*exact', text_lower):
            elements_found["zero_residual"] = True
            evidence.append("Residual = 0 interpretation found")
        else:
            evidence.append("Residual = 0 interpretation NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_hw13_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Homework 13.1: Residual definition, formula, and interpretation.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 4,
                    "component_1_name_score": 1,
                    "component_1_title_score": 1,
                    "component_1_task_score": 1,
                    "component_1_autoformat_score": 1,
                    "component_2_score": 6,
                    "component_3_score": 5,
                    "component_4_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Complete and accurate answer.",
                vibe="Student correctly defines residuals, states the formula, and interprets all three cases.",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "definition": True,
                            "formula": True,
                            "positive_residual": True,
                            "negative_residual": True,
                            "zero_residual": True,
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

        prompt = f"""You are grading a statistics assignment about residuals in linear regression using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
What is a residual?

Total: 20 points

STUDENT ANSWER:
{student_answer}

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Feedback should be SHORT, written as a teacher's comment
3. Feedback CANNOT be an invitation for further discussion
4. Explanations must be SPECIFIC and ACTIONABLE - avoid vague phrases like "lacks depth", "could be better", "needs improvement". Instead, point to what is actually missing or what was done well.

**HYBRID GRADING APPROACH:**

**AUTOMATIC FORMATTING DETECTION RESULT:**
Task description correctly formatted (1 point if True): {formatting_check['elements_found']['task_description']}
Proper autoformatting and structure (1 point if True): {formatting_check['elements_found']['autoformatting']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC DETECTION:**
{element_check['elements_found']}

**RUBRIC:**

**Component 1: Formatting (4 points):**
- 1 point: Name present
- 1 point: Paper title present
- 1 point: Task description correctly formatted (use AUTOMATIC FORMATTING DETECTION RESULT, task_description)
- 1 point: Proper autoformatting and structure (use AUTOMATIC FORMATTING DETECTION RESULT, autoformatting)
- CRITICAL: Name and paper title cannot be verified by automatic detection; judge directly from the submitted text

**Component 2: Definition (6 points, all-or-nothing):**
Use AUTOMATIC DETECTION above (definition).
- 6 points: Residual correctly defined as the difference between the observed value of the dependent variable and the predicted value from the regression line
- 0 points: Definition absent or incorrect
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Formula (5 points, all-or-nothing):**
Use AUTOMATIC DETECTION above (formula).
- 5 points: Formula Residual = Y − Ŷ correctly stated
- 0 points: Formula absent or incorrect
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Interpretation (5 points):**
Use AUTOMATIC DETECTION above.
- 2 points: Positive residual explained — actual value is higher than predicted (use positive_residual)
- 2 points: Negative residual explained — actual value is lower than predicted (use negative_residual)
- 1 point: Residual = 0 explained — the prediction is exact (use zero_residual)
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**FEEDBACK RULES**
- Identify which components were completed correctly
- Point out missing or incomplete elements explicitly
- Maintain supportive tone

---

Return JSON only:
{{
  "component_1_score": <0-4>,
  "component_1_name_score": <0-1>,
  "component_1_title_score": <0-1>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0 or 6>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0 or 5>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief>",
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
            "component_1_score": "Formatting (Name / Title / Task desc / Autoformatting)",
            "component_2_score": "Definition",
            "component_3_score": "Formula",
            "component_4_score": "Interpretation",
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT",
        }

        max_scores = {
            "component_1_score": 4,
            "component_2_score": 6,
            "component_3_score": 5,
            "component_4_score": 5,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="HOMEWORK 13_1",
            question_description="Residual: Definition, Formula, and Interpretation",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="STRICT"
        )