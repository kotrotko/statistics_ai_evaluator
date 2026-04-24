"""
hw14_3.py
Chi-Square - Test Significance and Find Effect Sizes
Evaluation method name: def grade_hw14_3_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW14_3Evaluator(BaseEvaluator):
    """
    Evaluator for Homework 14 Task 3.

    Task: Test significance and find effect sizes (if significant) for the following tests:
    a. N = 19, R = 3, C = 2, χ2 (2) = 7.89, α = .05
    b. N = 12, R = 2, C = 2, χ2 (1) = 3.12, α = .05
    c. N = 74, R = 3, C = 3, χ2 (4) = 28.41, α = .01

    Rubric:
    Formatting (2 points: task description, no autoformatting)
    Problem a (6 points)
    Problem b (6 points)
    Problem c (6 points)
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

        # Task description
        pedagogical_markers = [
            "find effect sizes (if significant)",
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

    def grade_hw14_3_answer(self, student_answer: str, test_mode: bool = False):
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_1_task_score": 1,
                    "component_1_autoformat_score": 1,
                    "component_2_score": 6,
                    "component_3_score": 6,
                    "component_4_score": 6,
                },
                max_points=20,
                feedback="[TEST MODE] All three problems solved correctly.",
                vibe="Student demonstrates solid understanding of chi-square significance testing and effect sizes."
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
"Test significance and find effect sizes (if significant) for the following tests:
a. N = 19, R = 3, C = 2, χ2 (2) = 7.89, α = .05
b. N = 12, R = 2, C = 2, χ2 (1) = 3.12, α = .05
c. N = 74, R = 3, C = 3, χ2 (4) = 28.41, α = .01"

Use STRICT rubric-based grading. Total score MUST be exactly 20 points.

CORRECT ANSWERS:

Problem a: N = 19, df = 2, χ2 = 7.89, α = .05
- Critical value at df = 2, α = .05 is 5.991
- χ²(2, N = 19) = 7.89, p < .05. Result is statistically significant.
- min(R-1, C-1) = min(2, 1) = 1
- Cramer's V = √(7.89 / (19 × 1)) = √(.4153) = .644
- Effect size is large (V ≥ .50 for df* = 1)

Problem b: N = 12, df = 1, χ2 = 3.12, α = .05
- Critical value at df = 1, α = .05 is 3.841
- χ²(1, N = 12) = 3.12, p > .05. Result is NOT statistically significant.
- Effect size is not reported (only report when significant)

Problem c: N = 74, df = 4, χ2 = 28.41, α = .01
- Critical value at df = 4, α = .01 is 13.277
- χ²(4, N = 74) = 28.41, p < .01. Result is statistically significant.
- min(R-1, C-1) = min(2, 2) = 2
- Cramer's V = √(28.41 / (74 × 2)) = √(.1920) = .438
- Effect size is medium to large (accept either "medium", "large", or "medium to large" for df* = 2)

RUBRIC:

Component 1: Formatting (2 points)
Start with 2 points.

Step 1 Task description (1 point)
Use task_description_present. If False: deduct 1 point.

Step 2 No autoformatting (1 point)
Use no_autoformatting_present. If False: deduct 1 point.

Component 2: Problem a (6 points)
- Correctly states result is significant: 2 points
- Correct Cramer's V calculation (accept .64–.65): 2 points
- Correct effect size interpretation (large): 2 points

Component 3: Problem b (6 points)
- Correctly states result is NOT significant: 3 points
- Correctly states effect size is not reported: 3 points

Component 4: Problem c (6 points)
- Correctly states result is significant: 2 points
- Correct Cramer's V calculation (accept .43–.44): 2 points
- Correct effect size interpretation (medium, large, or medium to large): 2 points

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
  "component_2_score": <0-6>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-6>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-6>,
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
        print("GRADING RESULTS - HW14_3")
        print("Chi-Square: Test Significance and Effect Sizes")
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

            print(f"\nProblem a: {grading.get('component_2_score')}/6")
            if grading.get('component_2_explanation'):
                print(f"  → {grading.get('component_2_explanation')}")

            print(f"\nProblem b: {grading.get('component_3_score')}/6")
            if grading.get('component_3_explanation'):
                print(f"  → {grading.get('component_3_explanation')}")

            print(f"\nProblem c: {grading.get('component_4_score')}/6")
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

    evaluator = HW14_3Evaluator()

    print("=" * 60)
    print("HOMEWORK 14.3 EVALUATOR")
    print("Chi-Square: Test Significance and Effect Sizes")
    print("=" * 60)
    print("\nPlease enter the student's answer to HOMEWORK 14_3.")
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

    grading = evaluator.grade_hw14_3_answer(student_answer)

    evaluator.print_grading_results(grading)