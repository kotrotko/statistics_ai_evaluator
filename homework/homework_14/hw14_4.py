"""
hw14_4.py
Homework 14: Chi-Square
Chi-square goodness-of-fit test
Evaluation method name: def grade_hw14_4_answer
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

class HW14_4Evaluator(BaseEvaluator):
    """
    Evaluator for Chi-Square Goodness-of-Fit: Pizza Topping Orders.

    Exercise 14_4 Task 4. A pizza company wants to know if people order
    the same number of different toppings. They look at how many
    pepperoni, sausage, and cheese pizzas were ordered in the last week;
    fill out the rest of the frequency table and test for a difference.

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
            "goodness_of_fit_identified": False,
            "hypotheses_stated": False,
            "df_stated": False,
            "alpha_stated": False,
            "critical_value_stated": False,
            "observed_total_stated": False,
            "chi_square_emp_stated": False,
            "decision_rule_stated": False,
            "decision_stated": False,
            "interpretation_stated": False,
        }

        evidence = []

        # Checkpoint 1 — Goodness-of-fit identified
        if re.search(r'goodness[\s-]?of[\s-]?fit', text_lower):
            elements_found["goodness_of_fit_identified"] = True
            evidence.append("Goodness-of-fit identification found")
        else:
            evidence.append("Goodness-of-fit identification NOT found")

        # Checkpoint 2 — H0 and H1 both stated
        has_h0 = bool(re.search(r'h[\s_]?0\s*[:\-]|h₀\s*[:\-]', text_lower))
        has_h1 = bool(re.search(r'h[\s_]?1\s*[:\-]|h₁\s*[:\-]|h[\s_]?a\s*[:\-]', text_lower))
        if has_h0 and has_h1:
            elements_found["hypotheses_stated"] = True
            evidence.append("H0 and H1 both found")
        else:
            evidence.append(f"Hypotheses incomplete (H0={has_h0}, H1={has_h1})")

        # Checkpoint 3 — df = 2
        if re.search(r'df\s*=\s*2\b|df\s*=\s*c\s*[-−]\s*1', text_lower):
            elements_found["df_stated"] = True
            evidence.append("df = 2 found")
        else:
            evidence.append("df = 2 NOT found")

        # Checkpoint 4 — alpha = 0.05
        if re.search(r'α\s*=\s*0\.?05|alpha\s*=\s*0\.?05', text_lower):
            elements_found["alpha_stated"] = True
            evidence.append("α = 0.05 found")
        else:
            evidence.append("α = 0.05 NOT found")

        # Checkpoint 5 — critical value ≈ 5.99
        if re.search(r'(critical\s*value|cv|χ.{0,10}crit).{0,15}5\.99', text_lower):
            elements_found["critical_value_stated"] = True
            evidence.append("Critical value ≈ 5.99 found")
        else:
            evidence.append("Critical value ≈ 5.99 NOT found")

        # Checkpoint 6 — observed total = 846
        if re.search(r'846', text_lower):
            elements_found["observed_total_stated"] = True
            evidence.append("Observed total = 846 found")
        else:
            evidence.append("Observed total = 846 NOT found")

        # Checkpoint 7 — chi-square empirical ≈ 8.70
        if re.search(r'8\.7', text_lower):
            elements_found["chi_square_emp_stated"] = True
            evidence.append("χ²emp ≈ 8.70 found")
        else:
            evidence.append("χ²emp ≈ 8.70 NOT found")

        # Checkpoint 8 — decision rule stated in general form
        if re.search(
            r'decision\s*rule|reject.{0,20}(if|only\s*if).{0,30}(exceed|greater|critical|>)',
            text_lower
        ):
            elements_found["decision_rule_stated"] = True
            evidence.append("Decision rule (general form) found")
        else:
            evidence.append("Decision rule (general form) NOT found")

        # Checkpoint 9 — decision stated (reject / fail to reject)
        if re.search(r'reject\s*(the\s*)?(null\s*)?h[\s_]?0|reject\s*h₀|fail\s*to\s*reject', text_lower):
            elements_found["decision_stated"] = True
            evidence.append("Decision (reject/fail to reject) found")
        else:
            evidence.append("Decision (reject/fail to reject) NOT found")

        # Checkpoint 10 — interpretation in context
        if re.search(
            r'significant\s*difference|not\s*significant|equally\s*distributed|statistically\s*significant',
            text_lower
        ):
            elements_found["interpretation_stated"] = True
            evidence.append("Interpretation in context found")
        else:
            evidence.append("Interpretation in context NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_hw14_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Homework 14.4: Chi-Square Goodness-of-Fit test on pizza
        topping order frequencies.
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
                    "component_3_score": 5,
                    "component_4_score": 5,
                    "component_5_score": 4,
                },
                max_points=20,
                feedback="[TEST MODE] Problem statement, research question, method, hypotheses, alpha/df/CV/calculations, and statistical inference all correctly stated.",
                vibe="Student demonstrates solid understanding of the chi-square goodness-of-fit test",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "goodness_of_fit_identified": True,
                            "hypotheses_stated": True,
                            "df_stated": True,
                            "alpha_stated": True,
                            "critical_value_stated": True,
                            "observed_total_stated": True,
                            "chi_square_emp_stated": True,
                            "decision_rule_stated": True,
                            "decision_stated": True,
                            "interpretation_stated": True,
                        },
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)
        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=[
                "A pizza company wants to know if people order the same number "
                "of different toppings. They look at how many pepperoni, "
                "sausage, and cheese pizzas were ordered in the last week; "
                "fill out the rest of the frequency table and test for a "
                "difference."
            ]
        )

        prompt = f"""You are grading a statistics assignment about the chi-square goodness-of-fit test using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
Exercise 14_4 Task 4. A pizza company wants to know if people order the
same number of different toppings. They look at how many pepperoni,
sausage, and cheese pizzas were ordered in the last week; fill out the
rest of the frequency table and test for a difference.

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

**Component 2: Problem Statement and Research Question (4 points total):**
- 1 point: Problem statement correct (identifies that it is not known
  whether observed pepperoni, sausage, and cheese order counts differ
  significantly from an equal distribution)
- 1 point: Problem statement formulated in terms of a research gap
  (a gap in knowledge), not merely an aim or restatement of the task
- 1 point: Research question correct (asks whether customers order
  equal numbers of each topping, or whether preferences differ)
- 1 point: Research question allows determination of tails (any
  wording that signals directionality or the lack of it — e.g.
  two-tailed/one-tailed, "any difference," "more/less,"
  "increase/decrease" — is acceptable; do not require a specific
  phrasing)

**Component 3: Method and Hypotheses (5 points total):**
Use AUTOMATIC DETECTION above for supporting evidence.
- 1 point: Method (chi-square goodness-of-fit test) correctly
  identified and justified based on one categorical variable compared
  to an expected distribution
- 2 points: H₀ correctly stated (orders equally distributed across
  pepperoni, sausage, and cheese)
- 2 points: H₁ correctly stated (orders not equally distributed)
- CRITICAL: Do NOT require a separate mathematical form for H₀/H₁
  unless the student provides one; score based on what is present

**Component 4: Alpha, df, Critical Value, and Calculations (5 points total):**
Use AUTOMATIC DETECTION above for supporting evidence.
- 1 point: α = 0.05 correctly stated
- 1 point: df = 2 correctly calculated (df = C − 1 = 3 − 1 = 2)
- 1 point: χ²crit (critical value) ≈ 5.99 correctly stated, linked to
  the correct df and α
- 1 point: Observed total correctly calculated as 846
  (320 + 275 + 251)
- 1 point: χ²emp (empirical/obtained chi-square value) correctly
  calculated as ≈ 8.70
- CRITICAL: Do NOT award the χ²crit point if df or α is wrong, since
  the critical value is only correct when linked to correct df and α

**Component 5: Statistical Inference and Research Question Answer (4 points total):**
Use AUTOMATIC DETECTION above for supporting evidence.
- 1 point: General decision rule stated (reject H₀ if χ²emp > χ²crit)
- 1 point: Rule correctly applied to the specific values (χ²emp ≈ 8.70
  > χ²crit ≈ 5.99, therefore reject H₀)
- 1 point: Conclusion correctly states there is a significant
  difference in the number of pizzas ordered by topping
- 1 point: Conclusion correctly tied back to the research question
  (orders are not equally distributed across pepperoni, sausage, and
  cheese)

{FEEDBACK_RULES}

---

Return JSON only:
{{
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief>",
  "component_5_score": <0-4>,
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
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Problem Statement and Research Question",
            "component_3_score": "Method and Hypotheses",
            "component_4_score": "Alpha, df, Critical Value, and Calculations",
            "component_5_score": "Statistical Inference and Research Question Answer",
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
            "component_4_score": "HYBRID",
            "component_5_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 4,
            "component_3_score": 5,
            "component_4_score": 5,
            "component_5_score": 4,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="HOMEWORK 14_4",
            question_description="Chi-Square Goodness-of-Fit: Pizza Topping Orders",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )