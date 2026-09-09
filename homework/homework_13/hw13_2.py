"""
hw13_2.py
Homework 13: Linear Regression
Two Parameters of the Line of Best Fit
Evaluation method name: def grade_hw13_2_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2


class HW13_2Evaluator(BaseEvaluator):
    """
    Evaluator for Homework 13 Task 2.

    Task: What are the two parameters of the line of best fit, and what do
    they represent?

    Formatting (2 points: task description, no autoformatting).
    Slope (7 points: 3 for parameter name, 2 for positive slope, 2 for
    negative slope).
    Intercept (6 points: 3 for parameter name, 3 for interpretation).
    Regression equation (5 points, all-or-nothing).

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
            "slope_named": False,
            "positive_slope_interpretation": False,
            "negative_slope_interpretation": False,
            "intercept_named": False,
            "intercept_interpretation": False,
            "regression_equation": False,
        }

        evidence = []

        # Checkpoint 1 — Slope parameter named
        if re.search(r'slope|b\s*1|b₁|regression\s*coefficient|unstandardized\s*coefficient', text_lower):
            elements_found["slope_named"] = True
            evidence.append("Slope parameter name found")
        else:
            evidence.append("Slope parameter name NOT found")

        # Checkpoint 2 — Positive slope interpretation
        if re.search(r'positive\s*slope|slope.*positive|increas', text_lower):
            elements_found["positive_slope_interpretation"] = True
            evidence.append("Positive slope interpretation found")
        else:
            evidence.append("Positive slope interpretation NOT found")

        # Checkpoint 3 — Negative slope interpretation
        if re.search(r'negative\s*slope|slope.*negative|decreas', text_lower):
            elements_found["negative_slope_interpretation"] = True
            evidence.append("Negative slope interpretation found")
        else:
            evidence.append("Negative slope interpretation NOT found")

        # Checkpoint 4 — Intercept parameter named
        if re.search(r'intercept|b\s*0|b₀|constant|y-intercept', text_lower):
            elements_found["intercept_named"] = True
            evidence.append("Intercept parameter name found")
        else:
            evidence.append("Intercept parameter name NOT found")

        # Checkpoint 5 — Intercept interpretation
        if re.search(r'(when|if).{0,40}(x|independent variable).{0,20}(0|zero)|predicted\s*value.{0,20}(0|zero)', text_lower):
            elements_found["intercept_interpretation"] = True
            evidence.append("Intercept interpretation found")
        else:
            evidence.append("Intercept interpretation NOT found")

        # Checkpoint 6 — Regression equation
        if re.search(r'ŷ|y-hat|y\s*hat|=\s*a\s*\+\s*b|=\s*b\s*0\s*\+\s*b\s*1|regression\s*equation', text_lower):
            elements_found["regression_equation"] = True
            evidence.append("Regression equation found")
        else:
            evidence.append("Regression equation NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_hw13_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Homework 13.2: Two parameters of the line of best fit.
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
                    "component_2_score": 7,
                    "component_3_score": 6,
                    "component_4_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Complete and accurate answer.",
                vibe="Student understands the two parameters of the line of best fit correctly.",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "slope_named": True,
                            "positive_slope_interpretation": True,
                            "negative_slope_interpretation": True,
                            "intercept_named": True,
                            "intercept_interpretation": True,
                            "regression_equation": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)
        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["what do they"]
        )

        prompt = f"""You are grading a statistics assignment about the two parameters of the line of best fit using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
What are the two parameters of the line of best fit, and what do they represent?

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

**Component 1: Formatting (2 points):**
Use AUTOMATIC FORMATTING DETECTION RESULT above.
- 1 point: Task description correctly formatted
- 1 point: Proper autoformatting and structure

**Component 2: Slope (7 points):**
Use AUTOMATIC DETECTION above.
- 3 points: Parameter correctly named and labeled (use slope_named)
  Accept: slope, b1, b₁, regression coefficient, unstandardized coefficient
- 2 points: Positive slope correctly interpreted (use positive_slope_interpretation)
  Expected: positive slope = increasing relationship / Y increases as X increases
- 2 points: Negative slope correctly interpreted (use negative_slope_interpretation)
  Expected: negative slope = decreasing relationship / Y decreases as X increases
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Intercept (6 points):**
Use AUTOMATIC DETECTION above.
- 3 points: Parameter correctly named and labeled (use intercept_named)
  Accept: intercept, b0, b₀, constant, y-intercept
- 3 points: Intercept correctly explained (use intercept_interpretation)
  Expected: predicted value of Y when X equals 0 / value of Y when X = 0
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Regression Equation (5 points, all-or-nothing):**
Use AUTOMATIC DETECTION above (regression_equation).
- 5 points: Equation written correctly: ŷ = b₀ + b₁x or equivalent standard notation (ŷ = b0 + b1x, Y = a + bX, Ŷ = intercept + slope*X)
- 0 points: Equation absent, incomplete, or incorrect
- CRITICAL: This component is all-or-nothing. No partial credit.

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
  "component_2_score": <0-7>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-6>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0 or 5>,
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
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Slope",
            "component_3_score": "Intercept",
            "component_4_score": "Regression Equation",
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 7,
            "component_3_score": 6,
            "component_4_score": 5,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="HOMEWORK 13_2",
            question_description="Two Parameters of the Line of Best Fit",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="STRICT"
        )