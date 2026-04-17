"""
hw13_2.py
Linear Regression - Two parameters of the line of best fit
Evaluation method name: def grade_hw13_2_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW13_2Evaluator(BaseEvaluator):
    """
    Evaluator for Homework 13 Task 2.

    Task: What are the two parameters of the line of best fit, and what do they represent?

    Rubric:
    Formatting (2 points: task description, no autoformatting)
    Slope (7 points: 3 for parameter name, 2 for positive slope, 2 for negative slope)
    Intercept (6 points: 3 for parameter name, 3 for explanation)
    Regression equation (5 points)
    Total (strictly) 20 points.
    """

    def __init__(self):
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1200
        )

    def check_formatting_elements(self, student_answer: str) -> dict:
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "no_autoformatting": True,
        }

        evidence = []

        # Task description (pedagogical marker)
        pedagogical_markers = [
            "Visually check both the homoscedasticity and linearity",
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

    def grade_hw13_2_answer(self, student_answer: str, test_mode: bool = False):
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_1_task_score": 1,
                    "component_1_autoformat_score": 1,
                    "component_2_score": 7,
                    "component_3_score": 6,
                    "component_4_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Complete and accurate answer.",
                vibe="Student understands the two parameters of the line of best fit correctly."
            )

        formatting_check = self.check_formatting_elements(student_answer)
        fs = formatting_check["elements_found"]

        formatting_block = f"""
HEADER DETECTION RESULTS (USE AS FACTS):

task_description_present = {fs["task_description"]}
no_autoformatting_present = {fs["no_autoformatting"]}

You MUST deduct points in Component 1 strictly according to these values.
If task_description_present = False: deduct 1 point.
If no_autoformatting_present = False: deduct 1 point.
"""

        prompt = f"""{formatting_block}

You are grading a statistics assignment.

TASK:
"What are the two parameters of the line of best fit, and what do they represent?"

Use STRICT rubric-based grading. Total score MUST be exactly 20 points.

RUBRIC

Component 1: Formatting (2 points)
Start with 2 points.

Step 1 Task description (1 point)
Use task_description_present.
If False: deduct 1 point.

Step 2 No autoformatting (1 point)
Use no_autoformatting_present.
If False: deduct 1 point.

Component 2: Slope (7 points)
Breaking down the 7 points:
- 3 points: Parameter correctly named and labeled
  Accept: slope, b1, b₁, regression coefficient, unstandardized coefficient
- 2 points: Positive slope correctly interpreted
  Expected: positive slope = increasing relationship / Y increases as X increases
- 2 points: Negative slope correctly interpreted
  Expected: negative slope = decreasing relationship / Y decreases as X increases

Component 3: Intercept (6 points)
Breaking down the 6 points:
- 3 points: Parameter correctly named and labeled
  Accept: intercept, b0, b₀, constant, y-intercept
- 3 points: Intercept correctly explained
  Expected: predicted value of Y when X equals 0 / value of Y when X = 0

Component 4: Regression Equation (5 points)
Student must write the regression equation correctly.
- 5 points: Equation written correctly: ŷ = b₀ + b₁x or equivalent
- 4 points: Equation present but one element mislabeled or missing hat
- 3 points: Equation attempted but partially incorrect
- 1 point: Equation referenced but not written out
- 0 points: Completely absent

Accept any standard notation: ŷ = b0 + b1x, Y = a + bX, Ŷ = intercept + slope*X.

ORIGINALITY CHECK:
If copied/AI-generated with suspiciously generic style, set all scores to 0 and set feedback to EXACTLY:
"Due to originality concern, your points are frozen. You can get them back if you provide oral explanation for this paper."

STUDENT ANSWER:
{student_answer}

For component_1_task_score: use task_description_present (1 if True, 0 if False)
For component_1_autoformat_score: use no_autoformatting_present (1 if True, 0 if False)

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-7>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-6>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief>",
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
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        print("=" * 60)
        print("GRADING RESULTS - HW13_2")
        print("Two Parameters of the Line of Best Fit")
        print("=" * 60)

        if "component_1_score" in grading:
            if grading.get("originality_concern"):
                print("\n⚠️  ORIGINALITY CONCERN DETECTED")
                print("   All points frozen. See feedback below.")

            print(f"\nFormatting: {grading.get('component_1_score')}/2")
            print(f"  • Task description:  {grading.get('component_1_task_score')}/1 (string match)")
            print(f"  • No autoformatting: {grading.get('component_1_autoformat_score')}/1 (regex)")
            if grading.get('component_1_explanation'):
                print(f"   → {grading.get('component_1_explanation')}")

            print(f"\nSlope: {grading.get('component_2_score')}/7")
            if grading.get('component_2_explanation'):
                print(f"  → {grading.get('component_2_explanation')}")

            print(f"Intercept: {grading.get('component_3_score')}/6")
            if grading.get('component_3_explanation'):
                print(f"  → {grading.get('component_3_explanation')}")

            print(f"Regression Equation: {grading.get('component_4_score')}/5")
            if grading.get('component_4_explanation'):
                print(f"  → {grading.get('component_4_explanation')}")

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

    evaluator = HW13_2Evaluator()

    print("=" * 60)
    print("HOMEWORK 13.2 EVALUATOR")
    print("Two Parameters of the Line of Best Fit")
    print("=" * 60)
    print("\nPlease enter the student's answer to HOMEWORK 13_2.")
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

    grading = evaluator.grade_hw13_2_answer(student_answer)

    evaluator.print_grading_results(grading)
