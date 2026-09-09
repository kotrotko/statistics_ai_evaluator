"""
hw14_3.py
Homework 14: Chi-Square
Chi-square significance testing and effect sizes across three problems
Evaluation method name: def grade_hw14_3_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.constants import (
    IMPORTANT_NOTES,
    IMPORTANT_GRADING_RULES,
    FEEDBACK_RULES,
)
from config.formatting_checks import check_formatting_elements_type2

class HW14_3Evaluator(BaseEvaluator):
    """
    Evaluator for Chi-Square Significance Testing and Effect Sizes.

    Task 3. Test significance and find effect sizes (if significant) for
    the following tests:
    a. N = 19, R = 3, C = 2, χ2 (2) = 7.89, α = .05
    b. N = 12, R = 2, C = 2, χ2 (1) = 3.12, α = .05
    c. N = 74, R = 3, C = 3, χ2 (4) = 28.41, α = .01

    Inherits common functionality from BaseEvaluator.
    """

    def __init__(self):
        """Initialize the evaluator with API handler."""
        super().__init__()
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
            "problem_a_significance_stated": False,
            "problem_a_threshold_justified": False,
            "problem_a_effect_size_stated": False,
            "problem_b_significance_stated": False,
            "problem_b_critical_value_stated": False,
            "problem_b_effect_not_reported": False,
            "problem_c_significance_stated": False,
            "problem_c_threshold_justified": False,
            "problem_c_effect_size_stated": False,
        }

        evidence = []

        # Problem A — significance decision (χ² = 7.89, df 2, N 19, significant)
        if re.search(r'7\.89', text_lower) and re.search(
            r'significant(?!\s*ly\s*not)|statistically\s*significant', text_lower
        ):
            elements_found["problem_a_significance_stated"] = True
            evidence.append("Problem A significance decision found")
        else:
            evidence.append("Problem A significance decision NOT found")

        # Problem A — threshold justification (p < .05)
        if re.search(r'p\s*<\s*\.?0?5', text_lower):
            elements_found["problem_a_threshold_justified"] = True
            evidence.append("Problem A p-value threshold found")
        else:
            evidence.append("Problem A p-value threshold NOT found")

        # Problem A — effect size (Cramer's V ≈ .644, large)
        if re.search(r'\.644|cramer', text_lower):
            elements_found["problem_a_effect_size_stated"] = True
            evidence.append("Problem A effect size found")
        else:
            evidence.append("Problem A effect size NOT found")

        # Problem B — significance decision (χ² = 3.12, not significant)
        if re.search(r'3\.12', text_lower) and re.search(r'not\s*(statistically\s*)?significant', text_lower):
            elements_found["problem_b_significance_stated"] = True
            evidence.append("Problem B significance decision found")
        else:
            evidence.append("Problem B significance decision NOT found")

        # Problem B — critical value (3.841)
        if re.search(r'3\.84', text_lower):
            elements_found["problem_b_critical_value_stated"] = True
            evidence.append("Problem B critical value found")
        else:
            evidence.append("Problem B critical value NOT found")

        # Problem B — effect size not reported
        if re.search(r'not\s*report|no\s*effect\s*size', text_lower):
            elements_found["problem_b_effect_not_reported"] = True
            evidence.append("Problem B effect size correctly omitted")
        else:
            evidence.append("Problem B effect size omission NOT found")

        # Problem C — significance decision (χ² = 28.41, significant)
        if re.search(r'28\.41', text_lower) and re.search(
            r'significant(?!\s*ly\s*not)|statistically\s*significant', text_lower
        ):
            elements_found["problem_c_significance_stated"] = True
            evidence.append("Problem C significance decision found")
        else:
            evidence.append("Problem C significance decision NOT found")

        # Problem C — threshold justification (p < .01)
        if re.search(r'p\s*<\s*\.?0?1', text_lower):
            elements_found["problem_c_threshold_justified"] = True
            evidence.append("Problem C p-value threshold found")
        else:
            evidence.append("Problem C p-value threshold NOT found")

        # Problem C — effect size (Cramer's V ≈ .438, medium to large)
        if re.search(r'\.438|cramer', text_lower):
            elements_found["problem_c_effect_size_stated"] = True
            evidence.append("Problem C effect size found")
        else:
            evidence.append("Problem C effect size NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_hw14_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Homework 14.3: Chi-Square Significance Testing and Effect
        Sizes across three problems.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_2_score": 6,
                    "component_3_score": 6,
                    "component_4_score": 6,
                },
                max_points=20,
                feedback="[TEST MODE] All three problems correctly tested for significance, with critical values/thresholds justified and effect sizes correctly calculated or correctly identified as not reported.",
                vibe="Student demonstrates solid understanding of chi-square significance testing and effect sizes",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "problem_a_significance_stated": True,
                            "problem_a_threshold_justified": True,
                            "problem_a_effect_size_stated": True,
                            "problem_b_significance_stated": True,
                            "problem_b_critical_value_stated": True,
                            "problem_b_effect_not_reported": True,
                            "problem_c_significance_stated": True,
                            "problem_c_threshold_justified": True,
                            "problem_c_effect_size_stated": True,
                        },
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)
        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=[
                "Test significance and find effect sizes (if significant) "
                "for the following tests: a. N = 19, R = 3, C = 2, "
                "χ2 (2) = 7.89, α = .05 b. N = 12, R = 2, C = 2, "
                "χ2 (1) = 3.12, α = .05 c. N = 74, R = 3, C = 3, "
                "χ2 (4) = 28.41, α = .01"
            ]
        )

        prompt = f"""You are grading a statistics assignment about chi-square significance testing and effect sizes using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
Task 3. Test significance and find effect sizes (if significant) for the
following tests:
a. N = 19, R = 3, C = 2, χ2 (2) = 7.89, α = .05
b. N = 12, R = 2, C = 2, χ2 (1) = 3.12, α = .05
c. N = 74, R = 3, C = 3, χ2 (4) = 28.41, α = .01

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

**RUBRIC:**

**Component 1: Formatting (2 points total):**
Use AUTOMATIC FORMATTING DETECTION RESULT above.
- 1 point: Task description present
- 1 point: Lack of auto-formatting

**Component 2: Problem A (6 points total):**
Use AUTOMATIC DETECTION above for supporting evidence.
- 2 points: Significance decision correctly stated — χ² value (7.89),
  df, and N reported and compared to α, concluding statistically
  significant
- 2 points: Critical value or p-value threshold correctly justifying
  the decision (p < .05)
- 2 points: Effect size (Cramer's V) correctly calculated (≈ .644) and
  its magnitude correctly interpreted as large

**Component 3: Problem B (6 points total):**
Use AUTOMATIC DETECTION above for supporting evidence.
- 2 points: Significance decision correctly stated — χ² value (3.12),
  df, and N reported and compared to α, concluding not statistically
  significant
- 2 points: Critical value correctly stated (3.841) as justification
  for the decision
- 2 points: Effect size correctly identified as not reported, since
  the result is not significant
- CRITICAL: Do NOT award effect size points if the student calculates
  and reports a Cramer's V value here, since the result is not
  significant and an effect size should not be reported

**Component 4: Problem C (6 points total):**
Use AUTOMATIC DETECTION above for supporting evidence.
- 2 points: Significance decision correctly stated — χ² value
  (28.41), df, and N reported and compared to α, concluding
  statistically significant
- 2 points: Critical value or p-value threshold correctly justifying
  the decision (p < .01)
- 2 points: Effect size (Cramer's V) correctly calculated (≈ .438)
  and its magnitude correctly interpreted as medium to large

{FEEDBACK_RULES}

---

Return JSON only:
{{
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-6>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-6>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-6>,
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
            "component_2_score": "Problem A",
            "component_3_score": "Problem B",
            "component_4_score": "Problem C",
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
            "component_4_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 6,
            "component_3_score": 6,
            "component_4_score": 6,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="HOMEWORK 14_3",
            question_description="Chi-Square Significance Testing and Effect Sizes",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )