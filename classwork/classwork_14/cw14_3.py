"""

Classwork 14: Chi-Square
Chi-square test table and statistical inference
Evaluation method name: def grade_question_cw14_3_answer
Chi-square Test for independence table, statistical inference
Evaluation method name: def grade_cw14_3_answer
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

class CW14_3Evaluator(BaseEvaluator):
    """
    Evaluator for Chi-Square Test Table and Statistical Inference.

    Task 3. Using JASP, perform the chi-square test of independence.
    Include the table "Chi-Squared Test", number and name it
    (10 points). Make the statistical inference (10 points).

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
            "table_reference": False,
            "decision_rule_stated": False,
            "specific_values_stated": False,
            "decision_stated": False,
            "interpretation_stated": False,
        }

        evidence = []

        # Checkpoint 1 — Chi-Squared Test table reference
        if re.search(r'table\s*2|chi[\s-]?squared?\s*test', text_lower):
            elements_found["table_reference"] = True
            evidence.append("Chi-Squared Test table reference found")
        else:
            evidence.append("Chi-Squared Test table reference NOT found")

        # Checkpoint 2 — Decision rule stated in general form
        if re.search(
            r'decision\s*rule|reject.{0,20}(if|only\s*if).{0,30}(p\s*<|critical)',
            text_lower
        ):
            elements_found["decision_rule_stated"] = True
            evidence.append("Decision rule (general form) found")
        else:
            evidence.append("Decision rule (general form) NOT found")

        # Checkpoint 3 — Specific values stated (alpha/CV and p/observed value)
        has_alpha = bool(re.search(r'α\s*=|alpha\s*=|significance\s*level', text_lower))
        has_p_or_cv = bool(re.search(
            r'p\s*=\s*0|p[\s-]?value|critical\s*value|χ.{0,15}critical', text_lower
        ))
        has_observed = bool(re.search(r'χ.{0,20}=|observed\s*χ|χ²\s*=', text_lower))
        if has_alpha and has_p_or_cv and has_observed:
            elements_found["specific_values_stated"] = True
            evidence.append("Specific significance/p/critical/observed values found")
        else:
            evidence.append(
                f"Specific values incomplete (alpha={has_alpha}, "
                f"p_or_cv={has_p_or_cv}, observed={has_observed})"
            )

        # Checkpoint 4 — Decision stated (reject / fail to reject)
        if re.search(r'reject\s*(the\s*)?(null\s*)?h[\s_]?0|reject\s*h₀|fail\s*to\s*reject', text_lower):
            elements_found["decision_stated"] = True
            evidence.append("Decision (reject/fail to reject) found")
        else:
            evidence.append("Decision (reject/fail to reject) NOT found")

        # Checkpoint 5 — Interpretation in context
        if re.search(
            r'significant\s*association|not\s*significant|statistically\s*significant|independent',
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

    def grade_cw14_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 14.3: Chi-Squared Test table and statistical
        inference.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_2_score": 9,
                    "component_3_score": 9,
                },
                max_points=20,
                feedback="[TEST MODE] Chi-Squared Test table numbered and titled. Statistical inference correctly stated with decision rule, values, comparison, and interpretation.",
                vibe="Student demonstrates solid understanding of the chi-square test and statistical inference",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "table_reference": True,
                            "decision_rule_stated": True,
                            "specific_values_stated": True,
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
            pedagogical_markers=["make the statistical inference"]
        )

        prompt = f"""You are grading a statistics assignment about the chi-square test of independence and statistical inference in JASP using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
Task 3. Using JASP, perform the chi-square test of independence.
Include the table "Chi-Squared Test", number and name it
(10 points). Make the statistical inference (10 points).

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

**Component 2: Chi-Squared Test Table (9 points total):**
Use AUTOMATIC DETECTION above.
- 1 point: Introductory phrase for the Chi-Squared Test table is present
- 1 point: Introductory phrase references the table number (e.g., "...see Table 2")
- 1 point: Standalone table number present in APA style (e.g., "Table 2")
- 1 point: Descriptive table title present in APA style
- 5 points: The table itself is present and reports the chi-square value, df, and p-value
- CRITICAL: Do NOT award table points if no table is present
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Statistical Inference (9 points total):**
- 1 point: Decision rule stated in general form (either "reject H0 if
  p < alpha" or "reject H0 if the observed chi-square value exceeds
  the critical value" — either approach, or both, accepted)
- 2 points: Correct specific significance level/critical value stated
  (alpha, and the critical value if using that method)
- 2 points: Correct specific obtained value stated (p-value, or the
  observed chi-square value if using that method)
- 2 points: Correct comparison made and correct decision stated
  (reject or fail to reject H0)
- 2 points: Correct interpretation in context (statistically
  significant association between the variables, or lack thereof)
- CRITICAL: If the student presents both the p-value approach and the
  critical-value approach and both correctly reach the same
  conclusion, this is not duplication and should not be penalized —
  score based on whether the required elements are present, not on
  how many equivalent methods the student used to demonstrate them

{FEEDBACK_RULES}

---

Return JSON only:
{{
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-9>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-9>,
  "component_3_explanation": "<brief>",
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
            "component_2_score": "Chi-Squared Test Table",
            "component_3_score": "Statistical Inference",
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 9,
            "component_3_score": 9,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="CLASSWORK 14_3",
            question_description="Chi-Square Test Table and Statistical Inference",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )