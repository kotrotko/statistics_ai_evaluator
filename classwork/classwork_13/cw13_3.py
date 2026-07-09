"""
cw13_3.py
Classwork 13: Linear Regression
Hypotheses, significance level, coefficients, and statistical inference
Evaluation method name: def grade_cw13_3_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2

class CW13_3Evaluator(BaseEvaluator):
    """
    Evaluator for Linear Regression Step System.

    Task 3. State the hypotheses in needed form (5 points). Following the textbook, state the significance level α, calculate df, find the critical value (5 points). Using JASP, find the coefficients a and b (Statistics > Coefficients > Estimates) (5 points). Look at p. Is your result significant? Make a statistical inference by standard way: If p < 0.05, reject H0: there is a significant linear effect (5 points).

    Inherits common functionality from BaseEvaluator.
    """

    def __init__(self):
        """Initialize the evaluator with API handler."""
        super().__init__()
        # Initialize output formatter
        self.formatter = OutputFormatter(default_width=60)

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check if required elements are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "hypotheses_present": False,
            "alpha_correct": False,
            "df_present": False,
            "critical_value_present": False,
            "coefficients_present": False,
            "p_value_present": False,
        }

        evidence = []

        # Checkpoint 1 — Hypotheses (β = 0 / β ≠ 0)
        if re.search(r'β\s*=\s*0', text_lower) and re.search(r'β\s*≠\s*0', text_lower):
            elements_found["hypotheses_present"] = True
            evidence.append("Hypotheses in math form (β = 0 / β ≠ 0) found")
        else:
            evidence.append("Hypotheses in math form (β = 0 / β ≠ 0) NOT found")

        # Checkpoint 2 — Alpha correct value
        if re.search(r'α\s*=\s*\.?0?\.05', text_lower) or re.search(r'alpha\s*=\s*\.?0?\.05', text_lower):
            elements_found["alpha_correct"] = True
            evidence.append("Correct α = .05 found")
        else:
            evidence.append("Correct α = .05 NOT found")

        # Checkpoint 3 — df₂ = 18
        if re.search(r'\b18\b', text_lower):
            elements_found["df_present"] = True
            evidence.append("df₂ = 18 found")
        else:
            evidence.append("df₂ = 18 NOT found")

        # Checkpoint 4 — Critical value 4.414
        if re.search(r'4\.414', text_lower):
            elements_found["critical_value_present"] = True
            evidence.append("Critical value 4.414 found")
        else:
            evidence.append("Critical value 4.414 NOT found")

        # Checkpoint 5 — Coefficients a = 73.662, b = 3.342
        if re.search(r'73\.662', text_lower) and re.search(r'3\.342', text_lower):
            elements_found["coefficients_present"] = True
            evidence.append("Coefficients a = 73.662 and b = 3.342 found")
        else:
            evidence.append("Coefficients a = 73.662 and b = 3.342 NOT found")

        # Checkpoint 6 — p < .001
        if re.search(r'p\s*<\s*\.?0?01', text_lower) or re.search(r'p\s*<\s*\.001', text_lower):
            elements_found["p_value_present"] = True
            evidence.append("p < .001 found")
        else:
            evidence.append("p < .001 NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_cw13_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 13.3: Hypotheses, significance level, coefficients, and statistical inference.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_2_score": 4,
                    "component_3_score": 4,
                    "component_4_score": 5,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Formatting present. Hypotheses stated in math form. Statistical parameters correctly linked. Coefficients reported and equation assembled. Inference correctly stated.",
                vibe="Student demonstrates solid understanding of linear regression hypothesis testing",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "hypotheses_present": True,
                            "alpha_correct": True,
                            "df_present": True,
                            "critical_value_present": True,
                            "coefficients_present": True,
                            "p_value_present": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)
        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["is your result significant"]
        )

        prompt = f"""You are grading a statistics assignment about linear regression hypothesis testing using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
Task 3. State the hypotheses in needed form (5 points). Following the textbook, state the significance level α, calculate df, find the critical value (5 points). Using JASP, find the coefficients a and b (Statistics > Coefficients > Estimates) (5 points). Look at p. Is your result significant? Make a statistical inference by standard way: If p < 0.05, reject H0: there is a significant linear effect (5 points).

Total: 20 points

STUDENT ANSWER:
{student_answer}

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Reasoning is required; calculations are mandatory
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. Award partial credit where reasoning is mostly correct but incomplete
6. It is expected to see both student's logic and calculations, not only the final answer
7. Explanations must be SPECIFIC and ACTIONABLE - avoid vague phrases like "lacks depth", "could be better", "needs improvement". Instead, point to what is actually missing or what was done well.

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

**Component 2: Hypotheses (4 points):**
Use AUTOMATIC DETECTION above.
- 1 point: H₀ stated
- 1 point: H₀ in math form β = 0
- 1 point: H₁ stated
- 1 point: H₁ in math form β ≠ 0
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Statistical Parameters (4 points):**
Use AUTOMATIC DETECTION above.
- 1 point: α = 0.05
- 1 point: df₁ = 1 and df₂ = 18 with correct calculation (n − 2 = 20 − 2 = 18)
- 1 point: correct critical value F(1, 18) = 4.414
- 1 point: linked to correct df₁, df₂ and α
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Coefficients (5 points):**
Use AUTOMATIC DETECTION above.
- 1 point: a = 73.662
- 1 point: b = 3.342
- 1 point: correct regression equation form Ŷ = a + b·X
- 1 point: assembled equation Ŷ = 73.662 + 3.342·X
- 1 point: correct identification of a as intercept and b as slope in M₁
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: Inference (5 points):**
Use AUTOMATIC DETECTION above.
- 1 point: p < .001
- 1 point: comparing p to α = 0.05
- 1 point: rejecting H₀
- 2 points: concluding there is a statistically significant linear effect of hours spent on statistics homework on final course score
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

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
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief>",
  "component_5_score": <0-5>,
  "component_5_explanation": "<brief>",
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
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """
        Display grading results using OutputFormatter.

        Args:
            grading: Grading result dictionary
        """
        # Define component labels
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Hypotheses",
            "component_3_score": "Statistical Parameters",
            "component_4_score": "Coefficients",
            "component_5_score": "Inference",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT",
            "component_5_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 4,
            "component_3_score": 4,
            "component_4_score": 5,
            "component_5_score": 5,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="CLASSWORK 13_3",
            question_description="Hypotheses, Significance Level, Coefficients, and Statistical Inference",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )