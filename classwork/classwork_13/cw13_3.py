"""
cw13_3.py
Classwork 13: Linear Regression
Step system: Hypotheses, significance level, coefficients, and statistical inference
Evaluation method name: def grade_question_cw13_3_answer
"""

import re
from config import BaseEvaluator


class CW13_3Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 13_3.

    Task: Continue with Step system.
    Step 2. State the hypotheses in needed form (5 points).
    Step 3. Follow the textbook, state the significance level α, calculate df,
    find the critical value. (5 points)
    Step 4. Using JASP, find the coefficients a and b
    (Statistics > Coefficients > Estimates) (5 points).
    Look at p. Is your result significant? Make a statistical inference by standard way:
    If p < 0.05, reject H0: there is a significant linear effect (5 points).
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
            "hypotheses": False,
            "significance_setup": False,
            "coefficients": False,
            "inference": False
        }

        evidence = []

        # Task description (pedagogical anchors matching the step system)
        pedagogical_markers = [
            "Do you see the 𝑒𝑥𝑝𝑙𝑎𝑛𝑎𝑡𝑜𝑟𝑦 𝑟𝑒𝑙𝑎𝑡𝑖𝑜𝑛 𝑏𝑒𝑡𝑤𝑒𝑒𝑛 v𝑎𝑟𝑖𝑎𝑏𝑙𝑒𝑠?"
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Hypotheses (Step 2)
        if re.search(
            r'h[0o]\s*:|h[1a]\s*:|null\s*hypothesis|alternative\s*hypothesis|'
            r'β\s*=\s*0|b\s*=\s*0|no\s*(significant\s*)?linear|linear\s*effect|'
            r'slope|there\s*is\s*(a\s*)?significant',
            text_lower
        ):
            elements_found["hypotheses"] = True
            evidence.append("Hypotheses found")
        else:
            evidence.append("Hypotheses NOT found")

        # Significance level, df, critical value (Step 3)
        if re.search(
            r'α|alpha|significance\s*level|df\s*=|\bdf\b|degrees\s*of\s*freedom|'
            r'critical\s*value|t\s*crit|f\s*crit|t[\s_]?critical|f[\s_]?critical',
            text_lower
        ):
            elements_found["significance_setup"] = True
            evidence.append("Significance setup found")
        else:
            evidence.append("Significance setup NOT found")

        # Coefficients a and b from JASP (Step 4a)
        if re.search(
            r'\ba\s*=|\bb\s*=|intercept|coefficient|estimate|unstandardized|'
            r'β|slope\s*=|jasp|b\s*\(|a\s*\(',
            text_lower
        ):
            elements_found["coefficients"] = True
            evidence.append("Coefficients found")
        else:
            evidence.append("Coefficients NOT found")

        # p-value and statistical inference (Step 4b)
        if re.search(
            r'p\s*[<>=]\s*0\.\d+|p[\s-]?value|reject|fail\s*to\s*reject|'
            r'significant|conclude|linear\s*effect|h0',
            text_lower
        ):
            elements_found["inference"] = True
            evidence.append("Inference found")
        else:
            evidence.append("Inference NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def grade_question_cw13_3_answer(self, student_answer: str, test_mode: bool = False):

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 1,
                    "component_2_score": 4,
                    "component_3_score": 5,
                    "component_4_score": 5,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Strong structured answer with all steps present.",
                vibe="Clear linear regression step-system reasoning",
            )

        prompt = f"""You are grading a statistics assignment using a STRICT rubric.

TASK:
Students must complete 5 components following the Step system for linear regression.

IMPORTANT GRADING RULES:
1. Total score MUST be exactly 20 points
2. Focus on conceptual understanding over formatting
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

RUBRIC:

Component 1: Task Description (1 point)
DO NOT SCORE — handled externally. Leave component_1_score as 0.

Component 2: Step 2 — State the Hypotheses (4 points)
Student must state both H0 and H1 (or Ha) in correct form for linear regression.

- 4 points: Both hypotheses stated correctly and in proper form
  H0: β = 0 (or: there is no significant linear effect / slope equals zero)
  H1: β ≠ 0 (or: there is a significant linear effect / slope does not equal zero)
- 3 points: Both hypotheses present but one is imprecise or uses informal language
- 2 points: Only one hypothesis stated, or both present but incorrectly formulated
- 1 point: Hypotheses attempted but substantially wrong or incomplete
- 0 points: Completely absent

Accept symbolic (β = 0) or verbal ("there is no significant linear relationship") forms.
Do NOT accept hypotheses borrowed from correlation (H0: ρ = 0) without adaptation.

Component 3: Step 3 — Significance Level, df, Critical Value (5 points)
Student must state α, calculate the degrees of freedom, and identify the critical value.

- 5 points: All three elements present and correct
  α stated (typically 0.05), df calculated correctly (df = n − 2 for simple linear regression),
  critical value identified (t-critical or F-critical from table or JASP)
- 4 points: All three present but one contains a minor error or imprecision
- 3 points: Two of the three elements present and correct
- 2 points: Only one element present, or all three present but with significant errors
- 1 point: Minimal attempt (e.g., only mentions α without df or critical value)
- 0 points: Completely absent

CRITICAL: df for simple linear regression = n − 2. Accept df expressed as a number if n is known.
Accept t-critical or F-critical depending on student's approach.

Component 4: Step 4a — Find Coefficients a and b in JASP (5 points)
Student must report the intercept (a) and slope (b) from JASP
(Statistics > Coefficients > Estimates).

- 5 points: Both coefficients reported with correct labels and values from JASP output
- 4 points: Both coefficients present but one is mislabeled or value unclear
- 3 points: Only one coefficient reported, or both present without values
- 2 points: Coefficients mentioned but not clearly identified or reported from JASP
- 1 point: Minimal attempt (e.g., only mentions "coefficients" without reporting values)
- 0 points: Completely absent

Accept: a = intercept, b = slope / unstandardized coefficient B.
Accept any reasonable notation (a, b, β0, β1, intercept, slope).

Component 5: Step 4b — p-value Check and Statistical Inference (5 points)
Student must look at the p-value, compare it to α = 0.05, and state a formal inference.

- 5 points: p-value reported, compared to 0.05, and correct formal inference stated
  e.g. "p < 0.05, therefore reject H0: there is a significant linear effect"
  or "p > 0.05, therefore fail to reject H0: there is no significant linear effect"
- 4 points: Correct decision (reject/fail to reject) made but inference statement is incomplete
- 3 points: p-value reported and direction of decision correct but no formal inference written
- 2 points: p-value mentioned but comparison to α or inference is missing or wrong
- 1 point: Minimal attempt (e.g., only states "result is significant" without p-value or reasoning)
- 0 points: Completely absent

CRITICAL: Inference must explicitly state the decision about H0 using standard language.
CRITICAL: Direction of the decision must match the reported p-value.

---

STUDENT ANSWER:
{student_answer}

Return JSON in this exact format:
{{
  "component_1_score": 0,
  "component_1_explanation": "Handled externally",
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief explanation>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief explanation>",
  "component_4_score": <0-5>,
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
        print("GRADING RESULTS - CLASSWORK 13.3")
        print("Linear Regression — Step System")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Task Description): {grading.get('component_1_score')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Step 2: Hypotheses): {grading.get('component_2_score')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Step 3: α, df, Critical Value): {grading.get('component_3_score')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Step 4a: Coefficients a and b): {grading.get('component_4_score')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Step 4b: p-value and Inference): {grading.get('component_5_score')}/5")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points')}/20")
        print(f"PERCENTAGE: {grading.get('percentage')}%")

        print("\nFEEDBACK:")
        print(textwrap.fill(grading.get('feedback', ''), width=60))


if __name__ == "__main__":
    evaluator = CW13_3Evaluator()

    from config import InputHandler
    input_handler = InputHandler()

    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 13"
                      ".3",
        question_description="Linear Regression — Step System",
        min_length=10
    )

    if student_answer:
        grading = evaluator.grade_question_cw13_3_answer(student_answer)
        evaluator.print_grading_results(grading)