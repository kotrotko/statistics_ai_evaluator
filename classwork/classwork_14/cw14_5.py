"""
cw14_5.py
Classwork 14: Chi-Square
Output description, research question answer, and causation conclusion
Evaluation method name: def grade_cw14_5_answer
"""

"""
cw14_5.py
Classwork 14: Chi-Square Test of Independence
APA-style output description, answer to the main research question,
and conclusion on causation for a chi-square test of independence
Evaluation method name: def grade_cw14_5_answer
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

class CW14_5Evaluator(BaseEvaluator):
    """
    Evaluator for Chi-Square Output Description, Research Question
    Answer, and Causation.

    Task 5. Describe your output briefly. Follow the APA style you
    learned before (5 points). Answer the main research question:
    Are physical activity and fruit consumption independent?
    (10 points). What do you think about causation? (5 points).

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
            "apa_output_description": False,
            "research_question_answered": False,
            "causation_addressed": False,
        }

        evidence = []

        # Checkpoint 1 — APA-style output description
        if re.search(
            r'χ.{0,10}\(\s*\d+.{0,15}n\s*=\s*\d+\s*\)\s*=|χ²\s*=.{0,20}p\s*=',
            text_lower
        ):
            elements_found["apa_output_description"] = True
            evidence.append("APA-style output description found")
        else:
            evidence.append("APA-style output description NOT found")

        # Checkpoint 2 — Research question answered (independence/association)
        if re.search(
            r'not\s*independent|are\s*independent|significant\s*association|'
            r'no\s*significant\s*association|are\s*related|no\s*relationship',
            text_lower
        ):
            elements_found["research_question_answered"] = True
            evidence.append("Research question answer found")
        else:
            evidence.append("Research question answer NOT found")

        # Checkpoint 3 — Causation addressed
        if re.search(
            r'causation|cause[\s-]and[\s-]effect|does\s*not\s*(imply|mean)\s*causation|'
            r'cannot\s*(be\s*made|conclude).{0,20}causation|correlation.{0,20}causation',
            text_lower
        ):
            elements_found["causation_addressed"] = True
            evidence.append("Causation discussion found")
        else:
            evidence.append("Causation discussion NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_cw14_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 14.5: APA-style output description, research
        question answer, and causation.
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
                feedback="[TEST MODE] Output described in APA style. Research question correctly answered. Causation correctly addressed.",
                vibe="Student demonstrates solid understanding of the results and their limitations",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "apa_output_description": True,
                            "research_question_answered": True,
                            "causation_addressed": True,
                        },
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)
        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["describe your output", "what do you think about causation"]
        )

        prompt = f"""You are grading a statistics assignment about interpreting the results of a chi-square test of independence using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
Task 5. Describe your output briefly. Follow the APA style you
learned before (5 points). Answer the main research question: Are
physical activity and fruit consumption independent? (10 points).
What do you think about causation? (5 points).

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

**Component 2: Output Description (3 points total):**
Unbroken block, no sub-points. Award full credit only if the
student briefly describes the chi-square output in APA style
(reporting chi-square value, df, N, and p-value in the conventional
format, e.g., "χ²(4, N = 1184) = 14.15, p = .007").

**Component 3: Answer to the Main Research Question (10 points total):**
Unbroken block, no sub-points. Award full credit only if the
student directly and correctly answers whether physical activity
level and fruit consumption are independent, based on the chi-square
result (i.e., states that they are not independent / are
associated, since the test was significant).

**Component 4: Conclusion on Causation (5 points total):**
Unbroken block, no sub-points. Award full credit only if the
student correctly states that a chi-square test identifies
association only, not causation, and that no causal conclusion can
be drawn from the result.

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
            "component_2_score": "Output Description",
            "component_3_score": "Answer to the Main Research Question",
            "component_4_score": "Conclusion on Causation",
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
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
            question_name="CLASSWORK 14_5",
            question_description="Chi-Square Output Description, Research Question Answer, and Causation",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )