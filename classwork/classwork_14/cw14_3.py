"""
cw14_3.py
Classwork 14: Chi-Square Test of Independence
Chi-square test table and statistical inference
Evaluation method name: def grade_question_cw14_3_answer
"""

import re
from config import BaseEvaluator


class CW14_3Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 14_3.

    Task: Using JASP, perform the χ² test of independence.
    Include the table "Chi-Squared Test", number and name it (10 points).
    Make the statistical inference (10 points).
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
            "chi_square_table": False,
            "statistical_inference": False,
        }

        evidence = []

        # Task description — full phrase from task wording, student cannot reproduce without pasting
        pedagogical_markers = [
            'using jasp, perform',
            'include the table "chi-squared test", number and name it',
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Chi-square table: must have values 14.152 for chi square and 1184 for N
        has_chi_square_table = bool(re.search(r'14\.152', text_lower)) and \
                               bool(re.search(r'\b1184\b', text_lower))

        if has_chi_square_table:
            elements_found["chi_square_table"] = True
            evidence.append("Chi-square table found")
        else:
            evidence.append("Chi-square table NOT found")

        # Statistical inference: H₀ rejection language
        if re.search(
            r'h₀|h0|null\s*hypothesis|reject|rejected',
            text_lower
        ):
            elements_found["statistical_inference"] = True
            evidence.append("Statistical inference found")
        else:
            evidence.append("Statistical inference NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def grade_question_cw14_3_answer(self, student_answer: str, test_mode: bool = False):

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 1,
                    "component_2_score": 1,
                    "component_3_score": 9,
                    "component_4_score": 9,
                },
                max_points=20,
                feedback="[TEST MODE] Table present and correctly formatted. Statistical inference complete.",
                vibe="Well-structured chi-square report with correct inference",
            )

        prompt = f"""You are grading a statistics assignment using a STRICT rubric.

TASK:
Students must perform a chi-square test of independence in JASP, include a properly
formatted table, and make a statistical inference.

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

- 1 point: Response is written in complete sentences and structured paragraphs; table is introduced in context
- 0 points: Unstructured, bullet-point only, or raw JASP output pasted without any written framing

Component 3: Table 2 — Chi-Square Test (9 points)
Student must include the Chi-Squared Tests table from JASP, properly numbered and titled.

Sub-scoring (10 points total):
- Introductory phrase (1 point): Student writes a sentence introducing the table before presenting it
- Reference to table number in introductory phrase (1 point): The introductory phrase explicitly mentions the table by number (e.g., "Table 2 presents...")
- Table number (1 point): The table has a number label (e.g., "Table 2")
- Table title (1 point): The table has a descriptive title naming both variables and the test
- Table content (4 points):
    - 5 points: Table includes χ² value, df, p-value, and N; footnote about continuity correction is present
    - 4 points: Table includes χ² value, df, p-value, and N but footnote is missing
    - 2 points: Table is present but key values are missing or clearly wrong
    - 1 point: Minimal attempt — only column headers or label without data
    - 0 points: No table at all

CRITICAL: The table title must name both variables (physical activity and fruit consumption).
CRITICAL: You MUST award full marks for table content unless you can name the SPECIFIC missing or wrong element in component_3_explanation. Vague deductions are not acceptable.
CRITICAL: Do NOT deduct points for cosmetic differences in whitespace or plain-text formatting.

Component 4: Statistical Inference (9 points)
Student must state whether H₀ should be rejected and justify that decision.

- 9 points: Clear rejection (or non-rejection) of H₀ with BOTH of the following justifications:
  (a) p-value compared to significance level (α = 0.05): p = 0.007 < 0.05;
  OR observed χ² (14.152) compared to critical value (9.488) at df = 4, α = 0.05
  (b) conclusion explicitly states a statistically significant association between the variables
- 8 points: Correct decision with only one justification method, or both present but one underdeveloped
- 6 points: Correct decision stated with p-value or critical value referenced but no explicit conclusion about association
- 4 points: Correct decision stated but reasoning is vague or incomplete
- 2 points: H₀ mentioned but decision is unclear or reasoning is confused
- 0 points: Completely absent

CRITICAL: Accept either the p-value method OR the critical value method as valid justification.
CRITICAL: Student must explicitly mention H₀ or "null hypothesis".
CRITICAL: Conclusion must reference the specific variables (physical activity and fruit consumption).

---

STUDENT ANSWER:
{student_answer}

Return JSON in this exact format:
{{
  "component_1_score": 0,
  "component_1_explanation": "Handled externally",
  "component_2_score": <0-1>,
  "component_2_explanation": "<brief explanation>",
  "component_3_score": <0-10>,
  "component_3_explanation": "<brief explanation>",
  "component_4_score": <0-10>,
  "component_4_explanation": "<brief explanation>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment>",
  "vibe": "<one-sentence overall impression>"
}}

SCORING INSTRUCTIONS:
total_points = component_1_score + component_2_score + component_3_score + component_4_score
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
                ],
                20
            )

        return result

    def print_grading_results(self, grading):
        import textwrap

        print("=" * 60)
        print("GRADING RESULTS - CLASSWORK 14.3")
        print("Chi-Square Test Table and Statistical Inference")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Task Description): {grading.get('component_1_score')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Autoformatting): {grading.get('component_2_score')}/1")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Table 2 — Chi-Square Test): {grading.get('component_3_score')}/9")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Statistical Inference): {grading.get('component_4_score')}/9")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points')}/20")
        print(f"PERCENTAGE: {grading.get('percentage')}%")

        print("\nFEEDBACK:")
        print(textwrap.fill(grading.get('feedback', ''), width=60))


if __name__ == "__main__":
    evaluator = CW14_3Evaluator()

    from config import InputHandler
    input_handler = InputHandler()

    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 14.3",
        question_description="Chi-Square Test Table and Statistical Inference",
        min_length=10
    )

    if student_answer:
        grading = evaluator.grade_question_cw14_3_answer(student_answer)
        evaluator.print_grading_results(grading)