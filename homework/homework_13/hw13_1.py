"""
hw13_1.py
Linear Regression - Residual
Evaluation method name: def grade_hw13_1_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW13_1Evaluator(BaseEvaluator):
    """
    Evaluator for Homework 13 Task 1.

    Task: What is a residual?

    Rubric:
    Formatting (4 points: name, title, task description, no autoformatting)
    Definition (6 points)
    Formula (5 points)
    Interpretation (5 points)
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

        # Title
        title_patterns = [
            r'^\s*homework\s*13',
            r'^\s*hw\s*13\b',
            r'^\s*home\s*work\s*(week\s*)?13',
        ]
        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["paper_title"] = True
                evidence.append("Title found")
                break

        # Task description (pedagogical marker — student cannot ask "what is a residual?" about themselves)
        pedagogical_markers = [
            "what is a residual?",
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

    def grade_hw13_1_answer(self, student_answer: str, test_mode: bool = False):
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 4,
                    "component_1_name_score": 1,
                    "component_1_title_score": 1,
                    "component_1_task_score": 1,
                    "component_1_autoformat_score": 1,
                    "component_2_score": 6,
                    "component_3_score": 5,
                    "component_4_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Complete and accurate answer.",
                vibe="Student understands residuals correctly."
            )

        formatting_check = self.check_formatting_elements(student_answer)
        fs = formatting_check["elements_found"]

        formatting_block = f"""
HEADER DETECTION RESULTS (USE AS FACTS):

paper_title_present = {fs["paper_title"]}
task_description_present = {fs["task_description"]}
no_autoformatting_present = {fs["no_autoformatting"]}
"""

        prompt = f"""{formatting_block}

You are grading a statistics assignment.

TASK:
"What is a residual?"

Use STRICT rubric-based grading. Total score MUST be exactly 20 points.

RUBRIC

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

Component 2: Definition (6 points)
Expected idea:
Residual = difference between observed value of dependent variable and predicted value from regression line.

Full credit requires:
- mentions observed/actual value
- mentions predicted value
- states difference/error
- links to regression

Component 3: Formula (5 points)
Expected:
Residual = Y - Ŷ
Accept:
Y - Yhat
observed - predicted

Component 4: Interpretation (5 points)
Expected ideas:
- prediction error for each case
- positive residual = actual > predicted
- negative residual = actual < predicted
- zero residual = exact prediction

ORIGINALITY CHECK:
If copied/AI-generated with suspiciously generic style, set all scores to 0 and set feedback to EXACTLY:
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
  "component_2_score": <0-6>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-5>,
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
        print("GRADING RESULTS - HW13_1")
        print("Residual")
        print("=" * 60)

        if "component_1_score" in grading:
            if grading.get("originality_concern"):
                print("\n⚠️  ORIGINALITY CONCERN DETECTED")
                print("   All points frozen. See feedback below.")

            print(f"\nFormatting: {grading.get('component_1_score')}/4")
            print(f"  • Student name:      {grading.get('component_1_name_score')}/1 (LLM)")
            print(f"  • Paper title:       {grading.get('component_1_title_score')}/1 (regex)")
            print(f"  • Task description:  {grading.get('component_1_task_score')}/1 (string match)")
            print(f"  • No autoformatting: {grading.get('component_1_autoformat_score')}/1 (regex)")
            if grading.get('component_1_explanation'):
                print(f"   → {grading.get('component_1_explanation')}")

            print(f"\nDefinition: {grading.get('component_2_score')}/6")
            if grading.get('component_2_explanation'):
                print(f"  → {grading.get('component_2_explanation')}")

            print(f"Formula: {grading.get('component_3_score')}/5")
            if grading.get('component_3_explanation'):
                print(f"  → {grading.get('component_3_explanation')}")

            print(f"Interpretation: {grading.get('component_4_score')}/5")
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

    evaluator = HW13_1Evaluator()

    print("=" * 60)
    print("HOMEWORK 13.1 EVALUATOR")
    print("Residual")
    print("=" * 60)
    print("\nPlease enter the student's answer to HOMEWORK 13_1.")
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

    grading = evaluator.grade_hw13_1_answer(student_answer)

    evaluator.print_grading_results(grading)