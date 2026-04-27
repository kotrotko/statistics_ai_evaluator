"""
hw14_5.py
Chi-Square Test for Independence - Gender and Promotion
Evaluation method name: def grade_hw14_5_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW14_5Evaluator(BaseEvaluator):
    """
    Evaluator for Homework 14 Task 5.

    Task: A company you work for wants to make sure that they are not discriminating
    against anyone in their promotion process. You have been asked to look across gender
    to see if there are differences in promotion rate (i.e. if gender and promotion rate
    are independent or not). The following data should be assessed at the normal level
    of significance.

    Rubric:
    Formatting (2 points: task description, no autoformatting)
    Problem Statement (2 points)
    Research Question (2 points)
    Method justification chi-square (1 point)
    Method justification Independence (1 point)
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
            "a company you work for",
            "you have been asked to look",
            "data should be assessed",
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

    def grade_hw14_5_answer(self, student_answer: str, test_mode: bool = False):
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
                vibe="Student demonstrates solid understanding of chi-square test for independence."
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
"A company you work for wants to make sure that they are not discriminating against
anyone in their promotion process. You have been asked to look across gender to see
if there are differences in promotion rate (i.e. if gender and promotion rate are
independent or not). The following data should be assessed at the normal level of
significance."

Use STRICT rubric-based grading. Total score MUST be exactly 20 points.

CORRECT ANSWER:

Problem statement: To determine whether promotion status differs by gender, i.e.,
whether the observed frequencies of promotion (Yes/No) across men and women indicate
a significant association.

Research question: Is there a significant relationship between gender and promotion
status, or are they independent?

Method justification: Chi-square test for independence, because there are two
categorical variables (gender and promotion status) and the goal is to assess whether
there is an association between them based on frequency counts. Goodness-of-fit is
not appropriate since it involves only one variable.

Hypotheses:
H₀: Gender and promotion are independent
H₁: Gender and promotion are associated

df = (R − 1)(C − 1) = (2 − 1)(2 − 1) = 1
α = 0.05
Critical value at α = 0.05, df = 1: CV ≈ 3.841

Observed frequencies:
Women–Yes = 8, Women–No = 5, Women Total = 13
Men–Yes = 9, Men–No = 7, Men Total = 16
Total = 29

Expected frequencies:
Women–Yes = (13×17)/29 ≈ 7.62
Women–No  = (13×12)/29 ≈ 5.38
Men–Yes   = (16×17)/29 ≈ 9.38
Men–No    = (16×12)/29 ≈ 6.62

Chi-square calculation:
Women–Yes: (8 − 7.62)² / 7.62 ≈ 0.019
Women–No:  (5 − 5.38)² / 5.38 ≈ 0.027
Men–Yes:   (9 − 9.38)² / 9.38 ≈ 0.015
Men–No:    (7 − 6.62)² / 6.62 ≈ 0.022
χ² ≈ 0.083

Since 0.083 < 3.841, fail to reject H₀.
Conclusion: No significant association between gender and promotion. They are independent.

RUBRIC:

Component 1: Formatting (2 points)
Start with 2 points.
Use task_description_present: if False, deduct 1 point.
Use no_autoformatting_present: if False, deduct 1 point.

Component 2: Problem Statement (2 points)
Student identifies the goal: to determine whether promotion status differs by gender.
- 2 points: clear and accurate
- 1 point: vague or partially correct
- 0 points: missing or wrong

Component 3: Research Question (2 points)
Student frames a testable question about the relationship between gender and promotion.
- 2 points: clear and accurate
- 1 point: vague or partially correct
- 0 points: missing or wrong

Component 4: Method justification — chi-square (1 point)
Student identifies chi-square as the method.
- 1 point: yes
- 0 points: no

Component 5: Method justification — Independence (1 point)
Student specifically identifies the test for independence (not just "chi-square").
- 1 point: yes
- 0 points: no

Component 6: Hypotheses (2 points)
- 1 point: correct H₀ (gender and promotion are independent)
- 1 point: correct H₁ (gender and promotion are associated)

Component 7: Alpha, df, CV (4 points)
- 1 point: α = 0.05
- 1 point: df = 1
- 2 points: CV ≈ 3.841 (accept 3.84 or 3.841)

Component 8: Calculation — Observed total (1 point)
Student correctly identifies observed frequencies and total N = 29.
- 1 point: correct
- 0 points: missing or wrong

Component 9: Calculation — chi-square (1 point)
Student correctly computes χ² ≈ 0.083 (accept 0.08–0.09).
- 1 point: correct
- 0 points: missing or wrong

Component 10: Statistical inference (2 points)
Student compares χ² to CV and makes correct fail-to-reject decision.
- 2 points: correct comparison and correct conclusion (fail to reject H₀)
- 1 point: correct decision without comparison, or comparison without decision
- 0 points: wrong or missing

Component 11: Research Question answer (2 points)
Student concludes there is no significant association between gender and promotion.
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
        print("GRADING RESULTS - HW14_5")
        print("Chi-Square Test for Independence: Gender and Promotion")
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
            print(f"Method — Independence: {grading.get('component_5_score')}/1")
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

    evaluator = HW14_5Evaluator()

    print("=" * 60)
    print("HOMEWORK 14.5 EVALUATOR")
    print("Chi-Square Test for Independence: Gender and Promotion")
    print("=" * 60)
    print("\nPlease enter the student's answer to HOMEWORK 14_5.")
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

    grading = evaluator.grade_hw14_5_answer(student_answer)

    evaluator.print_grading_results(grading)
