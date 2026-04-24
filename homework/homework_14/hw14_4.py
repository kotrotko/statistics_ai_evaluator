"""
hw14_4.py
Chi-Square Goodness-of-Fit - Pizza Company Frequency Table
Evaluation method name: def grade_hw14_4_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW14_4Evaluator(BaseEvaluator):
    """
    Evaluator for Homework 14 Task 4.

    Task: A pizza company wants to know if people order the same number of different
    toppings. Fill out the rest of the frequency table and test for a difference.

    Rubric:
    Formatting (2 points: task description, no autoformatting)
    Problem Statement (2 points)
    Research Question (2 points)
    Method justification chi-square (1 point)
    Method justification Goodness-of-Fit (1 point)
    Hypotheses (2 points)
    Alpha, df, CV (4 points)
    Calculation Observed total (1 point)
    Calculation chi-square (1 point)
    Statistical inference (2 points)
    Research Question answer (2 points)
    Total (strictly) 20 points.
    """

    def __init__(self):
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1500
        )

    def check_formatting_elements(self, student_answer: str) -> dict:
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "no_autoformatting": True,
        }

        evidence = []

        # Task description
        pedagogical_markers = [
            "a pizza company wants to know",
            "fill out the rest of the frequency table",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Autoformatting
        autoformat_patterns = [
            r'(?m)(?:^\s*\d+[\.\)]\s+\S.*\n){2,}',
            r'^\s*[-•*]\s+\S',
        ]
        for pattern in autoformat_patterns:
            if re.search(pattern, student_answer, re.MULTILINE):
                elements_found["no_autoformatting"] = False
                evidence.append("Autoformatting detected")
                break

        if elements_found["no_autoformatting"]:
            evidence.append("No autoformatting found")

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def grade_hw14_4_answer(self, student_answer: str, test_mode: bool = False):
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_1_task_score": 1,
                    "component_1_autoformat_score": 1,
                    "component_2_score": 2,
                    "component_3_score": 2,
                    "component_4_score": 1,
                    "component_5_score": 1,
                    "component_6_score": 2,
                    "component_7_score": 4,
                    "component_8_score": 1,
                    "component_9_score": 1,
                    "component_10_score": 2,
                    "component_11_score": 2,
                },
                max_points=20,
                feedback="[TEST MODE] Complete and accurate answer.",
                vibe="Student demonstrates solid understanding of chi-square goodness-of-fit."
            )

        formatting_check = self.check_formatting_elements(student_answer)
        fs = formatting_check["elements_found"]

        formatting_block = f"""
HEADER DETECTION RESULTS (USE AS FACTS):

task_description_present = {fs["task_description"]}
no_autoformatting_present = {fs["no_autoformatting"]}
"""

        prompt = f"""{formatting_block}

You are grading a statistics assignment.

TASK:
"A pizza company wants to know if people order the same number of different toppings.
Fill out the rest of the frequency table and test for a difference."

Use STRICT rubric-based grading. Total score MUST be exactly 20 points.

CORRECT ANSWER:

Problem statement: To determine whether observed numbers of pepperoni, sausage, and
cheese pizza orders differ significantly from an equal distribution.

Research question: Do customers order equal numbers of pepperoni, sausage, and cheese
pizzas, or is there a significant difference in their preferences?

Method justification: Chi-square goodness-of-fit test, because there is one categorical
variable (pizza topping) and the goal is to compare observed frequencies to an expected
equal distribution.

Hypotheses:
H₀: Orders are equally distributed (pepperoni = sausage = cheese)
H₁: Orders are not equally distributed

df = C − 1 = 3 − 1 = 2
α = 0.05
Critical value at α = 0.05, df = 2: CV ≈ 5.991

Observed frequencies: Pepperoni = 320, Sausage = 275, Cheese = 251, Total = 846
Expected frequency: 846 / 3 = 282 for each category

Chi-square calculation:
Pepperoni: (320 − 282)² / 282 = 1444 / 282 ≈ 5.12
Sausage:   (275 − 282)² / 282 = 49 / 282 ≈ 0.17
Cheese:    (251 − 282)² / 282 = 961 / 282 ≈ 3.41
χ² ≈ 8.70

Since 8.70 > 5.991, reject H₀.
Conclusion: There is a significant difference in pizza orders by topping.

RUBRIC:

Component 1: Formatting (2 points)
Start with 2 points.
Use task_description_present: if False, deduct 1 point.
Use no_autoformatting_present: if False, deduct 1 point.

Component 2: Problem Statement (2 points)
Student identifies the goal: to determine whether observed pizza orders differ
significantly from equal distribution.
- 2 points: clear and accurate
- 1 point: vague or partially correct
- 0 points: missing or wrong

Component 3: Research Question (2 points)
Student frames a testable research question about equal distribution of pizza orders.
- 2 points: clear and accurate
- 1 point: vague or partially correct
- 0 points: missing or wrong

Component 4: Method justification — chi-square (1 point)
Student identifies chi-square as the method.
- 1 point: yes
- 0 points: no

Component 5: Method justification — Goodness-of-Fit (1 point)
Student specifically identifies goodness-of-fit (not just "chi-square").
- 1 point: yes
- 0 points: no

Component 6: Hypotheses (2 points)
- 1 point: correct H₀ (equal distribution)
- 1 point: correct H₁ (not equally distributed)

Component 7: Alpha, df, CV (4 points)
- 1 point: α = 0.05
- 1 point: df = 2
- 2 points: CV ≈ 5.991 (accept 5.99 or 5.991)

Component 8: Calculation — Observed total (1 point)
Student correctly computes total = 846 and expected = 282 per category.
- 1 point: both correct
- 0 points: missing or wrong

Component 9: Calculation — chi-square (1 point)
Student correctly computes χ² ≈ 8.70 (accept 8.6–8.8).
- 1 point: correct
- 0 points: missing or wrong

Component 10: Statistical inference (2 points)
Student compares χ² to CV and makes correct rejection decision.
- 2 points: correct comparison and correct rejection of H₀
- 1 point: correct decision without comparison, or comparison without decision
- 0 points: wrong or missing

Component 11: Research Question answer (2 points)
Student concludes that orders are not equally distributed / there is a significant difference.
- 2 points: clear and correct
- 1 point: vague or partially correct
- 0 points: missing or wrong

ORIGINALITY CHECK:
If copied/AI-generated with suspiciously generic style, set all scores to 0 and set feedback to EXACTLY:
"Due to originality concern, your points are frozen. You can get them back if you provide oral explanation for this paper."

STUDENT ANSWER:
{student_answer}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-2>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-2>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-1>,
  "component_4_explanation": "<brief>",
  "component_5_score": <0-1>,
  "component_5_explanation": "<brief>",
  "component_6_score": <0-2>,
  "component_6_explanation": "<brief>",
  "component_7_score": <0-4>,
  "component_7_explanation": "<brief>",
  "component_8_score": <0-1>,
  "component_8_explanation": "<brief>",
  "component_9_score": <0-1>,
  "component_9_explanation": "<brief>",
  "component_10_score": <0-2>,
  "component_10_explanation": "<brief>",
  "component_11_score": <0-2>,
  "component_11_explanation": "<brief>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <number>,
  "feedback": "<short teacher comment>",
  "vibe": "<one sentence overall impression>"
}}"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"formatting_check": formatting_check}
        )

        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score",
                "component_5_score",
                "component_6_score",
                "component_7_score",
                "component_8_score",
                "component_9_score",
                "component_10_score",
                "component_11_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        print("=" * 60)
        print("GRADING RESULTS - HW14_4")
        print("Chi-Square Goodness-of-Fit: Pizza Company")
        print("=" * 60)

        if "component_1_score" in grading:
            if grading.get("originality_concern"):
                print("\n⚠️  ORIGINALITY CONCERN DETECTED")
                print("   All points frozen. See feedback below.")

            print(f"\nFormatting: {grading.get('component_1_score')}/2")
            print(f"  • Task description:  {grading.get('component_1_task_score')}/1 (string match)")
            print(f"  • No autoformatting: {grading.get('component_1_autoformat_score')}/1 (regex)")

            print(f"\nProblem Statement: {grading.get('component_2_score')}/2")
            print(f"Research Question: {grading.get('component_3_score')}/2")
            print(f"Method — chi-square: {grading.get('component_4_score')}/1")
            print(f"Method — Goodness-of-Fit: {grading.get('component_5_score')}/1")
            print(f"Hypotheses: {grading.get('component_6_score')}/2")
            print(f"Alpha, df, CV: {grading.get('component_7_score')}/4")
            print(f"Observed total: {grading.get('component_8_score')}/1")
            print(f"Chi-square calculation: {grading.get('component_9_score')}/1")
            print(f"Statistical inference: {grading.get('component_10_score')}/2")
            print(f"Research Question answer: {grading.get('component_11_score')}/2")
            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points')}/{grading.get('max_points', 20)}")
        print(f"PERCENTAGE: {grading.get('percentage')}%")

        print("\n" + "=" * 60)
        print("FEEDBACK:")
        print("=" * 60)
        print(textwrap.fill(grading.get("feedback", ""), width=60))

        print("\n" + "=" * 60)
        print("THE VIBE:")
        print("=" * 60)
        print(textwrap.fill(grading.get("vibe", ""), width=60))

        if 'error' in grading:
            print("\n" + "=" * 60)
            print("ERROR:")
            print("=" * 60)
            print(grading.get('error'))


if __name__ == "__main__":
    print("Welcome to the Homework AI Evaluator System!")
    print("=" * 60)

    evaluator = HW14_4Evaluator()

    print("=" * 60)
    print("HOMEWORK 14.4 EVALUATOR")
    print("Chi-Square Goodness-of-Fit: Pizza Company")
    print("=" * 60)
    print("\nPlease enter the student's answer to HOMEWORK 14_4.")
    print("(Press Enter twice when finished, or type 'END' on a new line)\n")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        lines.append(line)
        if len(lines) >= 2 and lines[-1] == '' and lines[-2] == '':
            lines = lines[:-2]
            break

    student_answer = '\n'.join(lines)

    if not student_answer.strip():
        print("\n❌ Error: No answer provided. Exiting.")
        exit(1)

    print("\n" + "=" * 60)
    print("EVALUATING...")
    print("=" * 60)

    grading = evaluator.grade_hw14_4_answer(student_answer)

    evaluator.print_grading_results(grading)