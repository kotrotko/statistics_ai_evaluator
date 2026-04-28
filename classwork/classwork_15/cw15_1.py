"""
cw15_1.py
Classwork 15: Exploratory Factor Analysis
Initial setup, assumption checks, and model fit
Evaluation method name: def grade_question_cw15_1_answer
"""

import re
import textwrap
from config import BaseEvaluator


class CW15_1Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 15_1.

    Task:
    A. Main research question: "We would like to know if these 9 variables could be shrunk
    down into a number of factors, and hopefully fewer than 9. We would like to see some
    correlations between these items and, as a result, a much smaller number of factors."
    Add this statement into your paper (5 points).
    B. Assumption checks. KMO test: Is the sample adequate for factor analysis? (5 points).
    C. Add the Bartlett's test. Is it significant? Are correlations sufficient to proceed? (5 points).
    D. Evaluation of Model fit. Include the Chi Squared Test table. Does our model fit? (5 points).
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
        first_lines = student_answer[:200]

        elements_found = {
            "paper_title": False,
            "task_description": False,
            "no_autoformatting": True,
        }

        evidence = []

        title_patterns = [
            r'^\s*classwork\s*15',
            r'^\s*cw\s*15\b',
            r'^\s*class\s*work\s*(week\s*)?15',
            r'^\s*in.?class\s*15'
        ]

        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["paper_title"] = True
                evidence.append("Title found")
                break

        pedagogical_markers = [
            "add this statement into your paper",
            "how do you know",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        autoformat_patterns = [
            r'(?m)(?:^\s*\d+[\.\)]\s+\S.*\n){2,}',
            r'^\s*[-•*]\s+\S',
        ]

        for pattern in autoformat_patterns:
            if re.search(pattern, student_answer, re.MULTILINE):
                elements_found["no_autoformatting"] = False
                evidence.append("Autoformatting detected")
                break

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def grade_question_cw15_1_answer(self, student_answer: str):

        formatting_check = self.check_formatting_elements(student_answer)
        formatting_summary = formatting_check["elements_found"]

        formatting_block = f"""
HEADER DETECTION RESULTS (DO NOT RE-EVALUATE):

paper_title_present = {formatting_summary["paper_title"]}
task_description_present = {formatting_summary["task_description"]}
no_autoformatting_present = {formatting_summary["no_autoformatting"]}
"""

        prompt = f"""{formatting_block}

You are grading a statistics classwork assignment.

TASK:

"Exploratory Factor Analysis: Initial setup, assumption checks, and model fit"

Use STRICT rubric-based grading. Total score MUST be exactly 20 points.

---

**RUBRIC**

Component 1: Formatting (4 points)
Start with 4 points.

Step 1 Name (1 point)
- Valid name = two capitalized words like John Doe
- Must appear in first two lines before content

Step 2 Title (1 point)
Use paper_title_present

Step 3 Task description (1 point)
Use task_description_present

Step 4 No autoformatting (1 point)
Use no_autoformatting_present

Component 2: Main Research Question (4 points)
Student must include the following statement verbatim or near-verbatim:
"We would like to know if these 9 variables could be shrunk down into a number of factors, and hopefully fewer than 9. We would like to see some correlations between these items and, as a result, a much smaller number of factors."

- 4 points: Statement included fully and correctly.
- 2 points: Statement partially present or heavily paraphrased.
- 0 points: Absent or unrelated.

Component 3: KMO Test and Sample Adequacy (4 points)
- 4 points: KMO value reported and correctly interpreted (Adequacy based on value).
- 2 points: KMO mentioned but value missing or interpretation incorrect.
- 0 points: Absent.

Component 4: Bartlett's Test (4 points)
- 4 points: Bartlett's test result reported (χ², df, p-value) and correctly interpreted (Significant = proceed).
- 2 points: Result reported but interpretation missing or incorrect.
- 0 points: Absent.

Component 5: Chi Squared Model Fit Table (4 points)
- 4 points: Table present in APA style (numbered/titled) and interpretation correct (Non-significant = good fit).
- 2 points: Table present but not APA, or interpretation incorrect.
- 0 points: Absent.

---

ORIGINALITY CHECK:
IMPORTANT: The "Task Description" (the research question statement) is required and should be excluded from originality concerns.
Evaluate ONLY the student's own interpretations. 
If remaining text is AI-generated/generic, set all scores to 0 and set feedback to EXACTLY:
"Due to originality concern, your points are frozen. You can get them back if you provide oral explanation for this paper."

STUDENT ANSWER:
{student_answer}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-4>,
  "component_1_name_score": <0-1>,
  "component_1_title_score": <0-1>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-4>,
  "component_4_explanation": "<brief>",
  "component_5_score": <0-4>,
  "component_5_explanation": "<brief>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <number>,
  "feedback": "<short teacher comment>",
  "vibe": "<one sentence overall impression>"
}}"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
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
        """Display grading results."""
        print("=" * 60)
        print("GRADING RESULTS - CW15_1")
        print("EFA - Initial Setup, Assumption Checks, and Model Fit")
        print("=" * 60)

        if 'component_1_score' in grading:
            if grading.get("originality_concern"):
                print("\n⚠️  ORIGINALITY CONCERN DETECTED")
                print("   All points frozen. See feedback below.")

            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Formatting): {grading.get('component_1_score')}/4")
            print(f"    • Student name:      {grading.get('component_1_name_score')}/1 (LLM)")
            print(f"    • Paper title:       {grading.get('component_1_title_score')}/1 (regex)")
            print(f"    • Task description:  {grading.get('component_1_task_score')}/1 (string match)")
            print(f"    • No autoformatting: {grading.get('component_1_autoformat_score')}/1 (regex)")
            if grading.get('component_1_explanation'):
                print(f"   → {grading.get('component_1_explanation')}")

            print(f"\nComponent 2 (Research Question): {grading.get('component_2_score', 'N/A')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"Component 3 (KMO Test): {grading.get('component_3_score', 'N/A')}/4")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"Component 4 (Bartlett's Test): {grading.get('component_4_score', 'N/A')}/4")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"Component 5 (Model Fit): {grading.get('component_5_score', 'N/A')}/4")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points', 'N/A')}/{grading.get('max_points', 20)}")
        print(f"PERCENTAGE: {grading.get('percentage', 'N/A')}%")

        print("\n" + "=" * 60)
        print("FEEDBACK:")
        print("=" * 60)
        print(textwrap.fill(grading.get('feedback', 'No feedback available'), width=60))

        print("\n" + "=" * 60)
        print("THE VIBE:")
        print("=" * 60)
        print(textwrap.fill(grading.get('vibe', 'N/A'), width=60))

        if 'error' in grading:
            print("\n" + "=" * 60)
            print("ERROR:")
            print("=" * 60)
            print(grading.get('error'))


if __name__ == "__main__":

    evaluator = CW15_1Evaluator()

    print("CLASSWORK 15.1 EVALUATOR")
    print("=" * 60)

    print("Enter student's answer (type END to finish):")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    student_answer = "\n".join(lines)

    grading = evaluator.grade_question_cw15_1_answer(student_answer)

    evaluator.print_grading_results(grading)