"""
cw9_1.py
Classwork 9: Independent groups comparison
Evaluation method name: def grade_question_cw9_1_answer
"""

import re
import textwrap
from config import BaseEvaluator


class CW9_1Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 9_1.

    Task:
    State the problem (5 points).
    Formulate the main Research Question (5 points).
    Name the statistical method appropriate for this research design (5 points).
    Explain why this method is suitable based on the research design (5 points).
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
            r'^\s*classwork\s*9',
            r'^\s*cw\s*9\b',
            r'^\s*class\s*work\s*9',
            r'^\s*in.?class\s*9'
        ]

        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["paper_title"] = True
                evidence.append("Title found")
                break

        if re.search(r'task|assignment|research\s+question|statistical\s+method|state\s+the\s+problem', text_lower):
            elements_found["task_description"] = True
            evidence.append("Task description found")

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

    def grade_question_cw9_1_answer(self, student_answer: str):

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

Student must:

• State the problem (5 points)  
• Formulate the Research Question (5 points)  
• Name the statistical method appropriate for this research design (5 points)  
• Explain why this method is suitable based on the research design (5 points)

Total score MUST be exactly 20 points.

---

**RUBRIC**

**Layer 1: Header & Formatting (Deductions Only)**
Start with 0 deductions.

STEP 1 - Name [STRICT]
- If NO valid student name found: deduct 1 point
- Valid name: Two words, each capitalized, appearing BEFORE content

STEP 2 - Title [STRICT]
Use paper_title_present.
If False: deduct 1 point

STEP 3 - Task Description [STRICT]
Use task_description_present.
If False: deduct 1 point

STEP 4 - No autoformatting [STRICT]
Use no_autoformatting_present.
If False: deduct 1 point

**Layer 2: Content Components (5 points each)**

**Component 1: Problem Statement (5 points)**
- 5 points: Clear, specific, well-defined problem with appropriate context
- 4 points: Problem stated with minor clarity issues
- 3 points: Problem present but vague or lacks specificity
- 2 points: Problem poorly articulated but shows some understanding
- 1 point: Attempted but unclear or off-topic
- 0 points: Completely blank

**Component 2: Research Question (5 points)**
- 5 points: Clear, testable question directly addressing the problem
- 4 points: Good question with minor precision issues
- 3 points: Question present but vague or partially addresses problem
- 2 points: Question unclear or poorly formulated
- 1 point: Attempted but not testable or irrelevant
- 0 points: Completely blank

**Component 3: Statistical Method Named (5 points)**
- 5 points: Correct method clearly identified (independent-samples t-test)
- 4 points: Correct method with minor naming issues
- 3 points: Method identified but may be incorrect or unclear
- 2 points: Method named but incorrect for the design
- 1 point: Attempted but wrong method or unclear
- 0 points: Completely blank

**Component 4: Justification Based on Research Design (5 points)**
Justification should reference design properties:
- Independent groups
- Two groups comparison
- Quantitative outcome variable
- Comparison of means

- 5 points: Clear, logical justification referencing all key design properties
- 4 points: Good justification with most design properties mentioned
- 3 points: Justification present but missing key design properties
- 2 points: Weak justification or incomplete reasoning
- 1 point: Attempted but illogical or irrelevant
- 0 points: Completely blank

The justification should refer to design properties such as:
- independent groups
- two groups comparison
- quantitative outcome variable
- comparison of means

---

EXAMPLE OF A COMPLETE ANSWER

Problem:
We want to determine whether directed reading activity improves comprehension scores compared to traditional instruction.

Research Question:
Do students who complete the directed reading activity obtain different comprehension scores than students who receive traditional instruction?

Statistical Method:
Using the step system, this requires an independent-samples t-test.

Justification:
This method is appropriate because two separate groups of students are compared on a quantitative outcome variable. The independent-samples t-test is designed to compare mean scores between independent groups.

---

STUDENT ANSWER:
{student_answer}

Return grading in this exact JSON format:
{{
  "originality_concern": <true/false>,
  "formatting_deductions": <0-4>,
  "formatting_name_deduction": <0-1>,
  "formatting_title_deduction": <0-1>,
  "formatting_task_deduction": <0-1>,
  "formatting_autoformat_deduction": <0-1>,
  "formatting_explanation": "<brief explanation for deductions>",
  "component_1_score": <0-5>,
  "component_1_explanation": "<brief explanation for problem statement>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<brief explanation for research question>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief explanation for method named>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief explanation for justification>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression>"
}}

SCORING INSTRUCTIONS:

For formatting_name_deduction:
- If valid name found: 0
- If NO name found: 1

For formatting_title_deduction: use paper_title_present (0 if True, 1 if False)
For formatting_task_deduction: use task_description_present (0 if True, 1 if False)
For formatting_autoformat_deduction: use no_autoformatting_present (0 if True, 1 if False)

formatting_deductions = sum of all four deduction values (0-4)

total_points = (component_1_score + component_2_score + component_3_score + component_4_score) - formatting_deductions

"""
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "formatting_check": formatting_check
            }
        )

        # If grading succeeded, validate component scores
        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score"
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results."""
        print("=" * 60)
        print("GRADING RESULTS - CW9_1")
        print("Independent Groups Comparison")
        print("=" * 60)

        if 'component_1_score' in grading:
            # Originality check result
            if grading.get("originality_concern"):
                print("\n⚠️  ORIGINALITY CONCERN DETECTED")
                print("   All points frozen. See feedback below.")

            print("\nFORMATTING DEDUCTIONS:")
            print(f"  Total Deductions: -{grading.get('formatting_deductions', 0)}/4")
            print(f"    • Student name:        -{grading.get('formatting_name_deduction', 0)}/1")
            print(f"    • Paper title:         -{grading.get('formatting_title_deduction', 0)}/1 (regex)")
            print(f"    • Task description:    -{grading.get('formatting_task_deduction', 0)}/1 (regex)")
            print(f"    • No autoformatting:   -{grading.get('formatting_autoformat_deduction', 0)}/1 (regex)")
            if grading.get('formatting_explanation'):
                print(f"    → {grading.get('formatting_explanation')}")

            print("\nCONTENT COMPONENTS:")
            print(f"  Component 1 (Problem Statement): {grading.get('component_1_score', 'N/A')}/5")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Research Question): {grading.get('component_2_score', 'N/A')}/5")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Method Named): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Justification): {grading.get('component_4_score', 'N/A')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

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

    evaluator = CW9_1Evaluator()

    print("CLASSWORK 9.1 EVALUATOR")
    print("=" * 60)

    print("Enter student's answer (type END to finish):")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    student_answer = "\n".join(lines)

    grading = evaluator.grade_question_cw9_1_answer(student_answer)

    evaluator.print_grading_results(grading)
