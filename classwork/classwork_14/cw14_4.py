"""
cw14_4.py
Classwork 14: Chi-Square Test of Independence
Effect size (Cramer's V): decision, calculation, and interpretation
Evaluation method name: def grade_cw14_4_answer
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

class CW14_4Evaluator(BaseEvaluator):
    """
    Evaluator for Chi-Square Effect Size (Cramer's V).

    Task 4. Do you need to calculate the Effect Size? Explain why do
    you think so (5 points). If no, skip this step. If yes, calculate
    the Effect Size. Find the needed option in Statistics > Nominal >
    Phi and Cramer's V. Include the table "Nominal", make sure that
    you numbered and titled it (10 points). Interpret it (5 points).

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
            "need_conclusion_stated": False,
            "cramers_v_or_phi_named": False,
            "table_reference": False,
            "interpretation_stated": False,
        }

        evidence = []

        # Checkpoint 1 — Explicit need conclusion with justification
        has_yes_no = bool(re.search(r'\byes\b|\bno\b', text_lower))
        has_justification = bool(re.search(
            r'sample\s*size|practical|statistical\s*significance|large\s*sample|strength',
            text_lower
        ))
        if has_yes_no and has_justification:
            elements_found["need_conclusion_stated"] = True
            evidence.append("Need conclusion with justification found")
        else:
            evidence.append(
                f"Need conclusion incomplete (yes/no={has_yes_no}, "
                f"justification={has_justification})"
            )

        # Checkpoint 2 — Cramer's V or Phi named
        if re.search(r"cram[ée]r|phi\s*coefficient|\bphi\b", text_lower):
            elements_found["cramers_v_or_phi_named"] = True
            evidence.append("Cramer's V / Phi named")
        else:
            evidence.append("Cramer's V / Phi NOT named")

        # Checkpoint 3 — Table reference
        if re.search(r'table\s*3|nominal', text_lower):
            elements_found["table_reference"] = True
            evidence.append("Table 3 / Nominal table reference found")
        else:
            evidence.append("Table 3 / Nominal table reference NOT found")

        # Checkpoint 4 — Interpretation of the effect size
        if re.search(
            r'weak\s*association|moderate\s*association|strong\s*association|'
            r'small\s*effect|large\s*effect|weak\s*effect|moderate\s*effect|strong\s*effect',
            text_lower
        ):
            elements_found["interpretation_stated"] = True
            evidence.append("Effect size interpretation found")
        else:
            evidence.append("Effect size interpretation NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_cw14_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 14.4: Need for effect size, Cramer's V table,
        and interpretation.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_2_score": 3,
                    "component_3_score": 10,
                    "component_4_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Need for effect size justified. Cramer's V table numbered and titled. Interpretation correctly stated.",
                vibe="Student demonstrates solid understanding of effect size and its interpretation",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "need_conclusion_stated": True,
                            "cramers_v_or_phi_named": True,
                            "table_reference": True,
                            "interpretation_stated": True,
                        },
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)
        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["do you need", "why do you think"]
        )

        prompt = f"""You are grading a statistics assignment about the effect size (Cramer's V) for a chi-square test of independence in JASP using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
Task 4. Do you need to calculate the Effect Size? Explain why do
you think so (5 points). If no, skip this step. If yes, calculate
the Effect Size. Find the needed option in Statistics > Nominal >
Phi and Cramer's V. Include the table "Nominal", make sure that you
numbered and titled it (10 points). Interpret it (5 points).

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

**Component 2: Need for Effect Size (3 points total):**
Unbroken block, no sub-points. Award full credit only if the
student states whether the effect size is needed AND explains why,
grounded in a correct statistical reason (e.g., statistical
significance alone does not indicate the strength/practical
importance of an association, especially with a large sample size).

**Component 3: Table for Effect Size (10 points total):**
Use AUTOMATIC DETECTION above.
- 1 point: Introductory phrase for the effect size table is present
- 1 point: Introductory phrase references the table number (e.g., "...see Table 3")
- 1 point: Standalone table number present in APA style (e.g., "Table 3")
- 1 point: Descriptive table title present in APA style
- 6 points: The table itself is present and reports Cramer's V (or Phi, only if applicable to a 2x2 table)
- CRITICAL: Do NOT award table points if no table is present
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Table Interpretation (5 points total):**
Unbroken block, no sub-points. Award full credit only if the
student correctly interprets the effect size value using accepted
strength categories (e.g., weak/small, moderate, strong/large) and
connects this to the practical importance of the association.

{FEEDBACK_RULES}

---

Return JSON only:
{{
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-3>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-10>,
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
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Need for Effect Size",
            "component_3_score": "Table for Effect Size",
            "component_4_score": "Table Interpretation",
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "STRICT",
            "component_4_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 3,
            "component_3_score": 10,
            "component_4_score": 5,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="CLASSWORK 14_4",
            question_description="Chi-Square Effect Size (Cramer's V)",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )