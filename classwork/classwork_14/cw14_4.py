"""
cw14_4.py
Classwork 14: Chi-Square Test of Independence
Effect Size (Phi / Cramér's V): decision, calculation, and interpretation
Evaluation method name: def grade_question_cw14_4_answer
"""

import re
from config import BaseEvaluator


class CW14_4Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 14_4.

    Task: Do you need to calculate the Effect Size? Explain why do you think so (5 points).
    If no, skip this step. If yes, calculate the Effect Size.
    Find the needed option in Statistics > Nominal > Phi and Cramer's V.
    Include the table "Nominal", make sure that you numbered and titled it (10 points).
    Interpret it (5 points).
    Total (strictly) 20 points.
    """

    def __init__(self):
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1200
        )

    def check_required_elements(self, student_answer: str) -> dict:
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "effect_size_decision": False,
            "nominal_table": False,
            "cramer_v_value": False,
            "effect_size_interpretation": False,
        }

        evidence = []

        # Task description (pedagogical anchors matching the task wording)
        pedagogical_markers = [
            "explain why do you think so",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Decision on whether to calculate effect size
        if re.search(
            r'yes|no|need|necessary|should|must|better|important|'
            r'practical|significance|sample\s*size|large\s*n|'
            r'statistically\s*significant|strength',
            text_lower
        ):
            elements_found["effect_size_decision"] = True
            evidence.append("Effect size decision found")
        else:
            evidence.append("Effect size decision NOT found")

        # Nominal table (Table X with title)
        if re.search(
            r'table\s*\d|nominal|phi|cramer|cramér',
            text_lower
        ):
            elements_found["nominal_table"] = True
            evidence.append("Nominal table found")
        else:
            evidence.append("Nominal table NOT found")

        # Cramér's V (or Phi) value reported
        if re.search(
            r"cramer|cramér|phi|v\s*=|φ\s*=|\.\d{2,}",
            text_lower
        ):
            elements_found["cramer_v_value"] = True
            evidence.append("Cramér's V / Phi value found")
        else:
            evidence.append("Cramér's V / Phi value NOT found")

        # Interpretation of effect size
        if re.search(
            r'weak|small|moderate|strong|large|negligible|trivial|'
            r'practical|association|strength|interpret|effect',
            text_lower
        ):
            elements_found["effect_size_interpretation"] = True
            evidence.append("Effect size interpretation found")
        else:
            evidence.append("Effect size interpretation NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def grade_question_cw14_4_answer(self, student_answer: str, test_mode: bool = False):

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 1,
                    "component_2_score": 1,
                    "component_3_score": 3,
                    "component_4_score": 10,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Effect size decision present. Nominal table included and titled. Cramér's V found and interpreted.",
                vibe="Clear effect size reasoning with properly formatted table",
            )

        prompt = f"""You are grading a statistics assignment using a STRICT rubric.

TASK:
Students must complete 4 components related to effect size in a chi-square test of independence.

IMPORTANT GRADING RULES:
1. Total score MUST be exactly 20 points
2. Focus on conceptual understanding over formatting
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

RUBRIC:

Component 1: Task Description (1 point)
DO NOT SCORE — handled externally. Leave component_1_score as 0.

Component 2: Autoformatting (1 point)
Student must demonstrate correct academic document formatting.

- 1 point: Response is formatted as a coherent academic answer (complete sentences, structured paragraphs, no raw JASP output dumped without context)
- 0 points: Unstructured, bullet-point only, or raw output without any written framing

Component 3: Conclusion on the Need for Effect Size (3 points)
Student must decide YES or NO — whether effect size should be calculated — and justify that decision.

- 3 points: Correct YES/NO decision with a full justification that references at least TWO of the following:
  (a) chi-square only tells us whether an association exists, not its strength;
  (b) large sample size can make even trivial effects statistically significant;
  (c) effect size reports practical importance of the result
- 2 points: Correct decision with only one reason provided, or correct decision with vague reasoning
- 1 point: Correct decision stated without any reasoning
- 0 points: Completely absent or clearly wrong decision

CRITICAL: Student must go beyond restating "effect size is useful" — reasoning must be specific and grounded.

Component 4: Table 3 — Nominal Effect Size (10 points)
Student must include the Nominal table from JASP (Phi and/or Cramér's V), properly numbered and titled.

Sub-scoring (10 points total):
- Introductory phrase (1 point): Student writes a sentence introducing the table before presenting it
- Reference to table number in introductory phrase (1 point): The introductory phrase explicitly mentions the table by number (e.g., "Table 3 shows...")
- Table number (1 point): The table has a number label (e.g., "Table 3")
- Table title (1 point): The table has a descriptive title that names the variables and the measure
- Table content (6 points):
    - 6 points: Table includes Cramér's V (or Phi where appropriate) with a correct numeric value; footnote about Phi limitation (2×2 only) is present
    - 5 points: Table includes Cramér's V with a correct numeric value but footnote is missing
    - 4 points: Table includes the value but labeling or structure has minor errors
    - 3 points: Table is present but value is absent or clearly wrong
    - 2 points: Table structure is present but mostly empty or misidentified
    - 1 point: Minimal attempt — only the word "Nominal" or a column header without data
    - 0 points: No table at all

CRITICAL: Accept Cramér's V OR Phi as the reported effect size statistic.
CRITICAL: The table title must reference the two variables being studied (not generic).

Component 5: Interpretation of Effect Size (5 points)
Student must interpret the numeric effect size in plain language.

- 5 points: Interpretation states the specific value (e.g., V = 0.077), labels its magnitude (weak/small/moderate/strong),
  explicitly names both variables, and explains what the result means for the practical significance of the chi-square finding
- 4 points: Correct interpretation with the value and magnitude label but one variable name missing, or practical significance implication not stated
- 3 points: Value mentioned and labeled (e.g., "weak"), but interpretation is generic and not connected to the specific variables
- 2 points: Magnitude label given without any numeric value, or value given without any label or explanation
- 1 point: Minimal attempt — only restates the number without any interpretation
- 0 points: Completely absent

CRITICAL: Interpretation must explicitly connect the effect size magnitude to whether the chi-square result has practical importance.
CRITICAL: Student must name the variables (not just say "the variables").

---

STUDENT ANSWER:
{student_answer}

Return JSON in this exact format:
{{
  "component_1_score": 0,
  "component_1_explanation": "Handled externally",
  "component_2_score": <0-1>,
  "component_2_explanation": "<brief explanation>",
  "component_3_score": <0-3>,
  "component_3_explanation": "<brief explanation>",
  "component_4_score": <0-10>,
  "component_4_explanation": "<brief explanation>",
  "component_5_score": <0-5>,
  "component_5_explanation": "<brief explanation>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment>",
  "vibe": "<one-sentence overall impression>"
}}

SCORING INSTRUCTIONS:
total_points = component_1_score + component_2_score + component_3_score + component_4_score + component_5_score
"""

        element_check = self.check_required_elements(student_answer)

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"element_check": element_check}
        )

        # Enforcement: task description check (plain string matching, overrides LLM)
        if "error" not in result:
            if not element_check["elements_found"]["task_description"]:
                result["component_1_score"] = 0
                result["component_1_explanation"] = "Task description NOT found (instructional phrasing missing)"
            else:
                result["component_1_score"] = 1
                result["component_1_explanation"] = "Task description found"

        if "error" not in result:
            result = self.validate_component_scores(
                result,
                [
                    "component_1_score",
                    "component_2_score",
                    "component_3_score",
                    "component_4_score",
                    "component_5_score",
                ],
                20
            )

        return result

    def print_grading_results(self, grading):
        import textwrap

        print("=" * 60)
        print("GRADING RESULTS - CLASSWORK 14.4")
        print("Effect Size: Phi and Cramér's V")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Task Description): {grading.get('component_1_score')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Autoformatting): {grading.get('component_2_score')}/1")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Conclusion on Need for Effect Size): {grading.get('component_3_score')}/3")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Table 3 — Nominal Effect Size): {grading.get('component_4_score')}/10")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Interpretation of Effect Size): {grading.get('component_5_score')}/5")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points')}/20")
        print(f"PERCENTAGE: {grading.get('percentage')}%")

        print("\nFEEDBACK:")
        print(textwrap.fill(grading.get('feedback', ''), width=60))


if __name__ == "__main__":
    evaluator = CW14_4Evaluator()

    from config import InputHandler
    input_handler = InputHandler()

    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 14.4",
        question_description="Effect Size: Phi and Cramér's V",
        min_length=10
    )

    if student_answer:
        grading = evaluator.grade_question_cw14_4_answer(student_answer)
        evaluator.print_grading_results(grading)
