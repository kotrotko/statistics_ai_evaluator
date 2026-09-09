"""
cw14_2.py
Classwork 14: Chi Square
Method justification, test settings
Evaluation method name: def grade_cw14_2_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import (
    IMPORTANT_NOTES,
    IMPORTANT_GRADING_RULES,
    FEEDBACK_RULES,
)

class CW14_2Evaluator(BaseEvaluator):
    """
    Evaluator for Chi-Square Test of Independence Setup.

    Task 2. Name the method you choose and justify it based on the
    data level (5 points). State the hypotheses in needed form
    (5 points). State the significance level alpha, calculate df,
    find the critical value (5 points). Open the JASP > Frequencies
    > Contingency Tables tool. Make sure that you have Physical
    Activity on Rows and Fruit Consumption on Columns. Include the
    "Contingency Tables" table, number it, make sure that it is
    introduced, numbered, and named (5 points).

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
            "chi_square_named": False,
            "data_level_justification": False,
            "hypotheses_stated": False,
            "alpha_df_cv_stated": False,
            "contingency_table": False,
        }

        evidence = []

        # Checkpoint 1 — Chi-square method named
        if re.search(r'chi[\s-]?square|χ²|χ\^?2|χ_?2', text_lower):
            elements_found["chi_square_named"] = True
            evidence.append("Chi-square method named")
        else:
            evidence.append("Chi-square method NOT named")

        # Checkpoint 2 — Data level justification
        if re.search(r'nominal|categorical|ordinal', text_lower):
            elements_found["data_level_justification"] = True
            evidence.append("Data level justification found")
        else:
            evidence.append("Data level justification NOT found")

        # Checkpoint 3 — Hypotheses (H0 and H1)
        if re.search(
            r'h[\s_]?0|h₀|null\s*hypothesis', text_lower
        ) and re.search(
            r'h[\s_]?1|h₁|alternative\s*hypothesis', text_lower
        ):
            elements_found["hypotheses_stated"] = True
            evidence.append("H0 and H1 both found")
        else:
            evidence.append("H0 and/or H1 NOT found")

        # Checkpoint 4 — alpha, df, critical value
        has_alpha = bool(re.search(r'α\s*=|alpha\s*=|significance\s*level', text_lower))
        has_df = bool(re.search(r'\bdf\s*=|degrees\s*of\s*freedom', text_lower))
        has_cv = bool(re.search(r'critical\s*value|χ.{0,15}critical|cv\s*=', text_lower))
        if has_alpha and has_df and has_cv:
            elements_found["alpha_df_cv_stated"] = True
            evidence.append("Alpha, df, and critical value all found")
        else:
            evidence.append(
                f"Alpha/df/CV incomplete (alpha={has_alpha}, "
                f"df={has_df}, cv={has_cv})"
            )

        # Checkpoint 5 — Contingency table
        if re.search(r'contingency\s*table|table\s*1', text_lower):
            elements_found["contingency_table"] = True
            evidence.append("Contingency table reference found")
        else:
            evidence.append("Contingency table reference NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_cw14_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 14.2: Chi-square method justification, hypotheses,
        significance level/df/critical value, and contingency table.
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
                    "component_4_score": 4,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Method named and justified. Hypotheses stated. Alpha, df, and CV correct. Contingency table numbered and titled.",
                vibe="Student demonstrates solid understanding of chi-square test setup",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "chi_square_named": True,
                            "data_level_justification": True,
                            "hypotheses_stated": True,
                            "alpha_df_cv_stated": True,
                            "contingency_table": True,
                        },
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)
        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["name the method you choose"]
        )

        prompt = f"""You are grading a statistics assignment about setting up a chi-square test of independence in JASP using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
Task 2. Name the method you choose and justify it based on the data
level (5 points). State the hypotheses in needed form (5 points).
State the significance level alpha, calculate df, find the critical
value (5 points). Open the JASP > Frequencies > Contingency Tables
tool. Make sure that you have Physical Activity on Rows and Fruit
Consumption on Columns. Include the "Contingency Tables" table,
number it, make sure that it is introduced, numbered, and named
(5 points).

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

**Component 2: Chi-Square Method Justification (5 points total):**
- 2 points: Chi-square method explicitly named
- 2 points: Chi-square use justified based on nominal/categorical data level
- 1 point: Awarded only if the justification does not attach an
  unsupported specific chi-square variant (e.g., "of independence,"
  "goodness-of-fit") to the data-level reasoning alone
- CRITICAL: Data level (nominal/categorical) justifies the choice of
  a chi-square test in general, but does not by itself justify a
  specific variant like "of independence" — that requires reference
  to testing association between two categorical variables in one
  sample, not data level alone

**Component 3: Hypotheses (4 points total):**
- 2 points: H0 (null hypothesis) correctly stated
- 2 points: H1 (alternative hypothesis) correctly stated

**Component 4: Significance Level, df, and Critical Value (4 points total):**
- 1 point: Significance level (alpha) stated
- 2 points: Degrees of freedom correctly calculated
- 2 points: Critical value correctly stated

**Component 5: Contingency Table (5 points total):**
- 1 point: Introductory phrase for the contingency table is present
- 1 point: Introductory phrase references the table number (e.g., "...in Table 1")
- 1 point: Standalone table number present in APA style (e.g., "Table 1")
- 1 point: Descriptive table title present in APA style
- 1 point: The table itself is present
- CRITICAL: Do NOT award table formatting points if no table is present
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

{FEEDBACK_RULES}
---

Return JSON only:
{{
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-4>,
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
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Chi-Square Method Justification",
            "component_3_score": "Hypotheses (H0 / H1)",
            "component_4_score": "Significance Level, df, and Critical Value",
            "component_5_score": "Contingency Table",
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT",
            "component_5_score": "STRICT",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 5,
            "component_3_score": 4,
            "component_4_score": 4,
            "component_5_score": 5,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="CLASSWORK 14_2",
            question_description="Chi-Square Test of Independence Setup",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )