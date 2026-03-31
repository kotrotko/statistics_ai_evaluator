"""
cw10_1.py
Classwork 10: One-Way ANOVA
Evaluation method name: def grade_cw10_1_answer
"""

import re
import textwrap
from config import BaseEvaluator


class CW10_1Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 10_1.

    Task:
    What is the role of the 'Participant' variable? (5 points)
    Should it be included in your analysis? Why? (5 points)
    State the problem with your own words (5 points)
    Formulate the main Research question (5 points)
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
            r'^\s*classwork\s*10',
            r'^\s*cw\s*10\b',
            r'^\s*class\s*work\s*(week\s*)?10',
            r'^\s*in.?class\s*10'
        ]

        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["paper_title"] = True
                evidence.append("Title found")
                break

        if re.search(
                r'participant\s+variable|role\s+of|facebook\s+friends|should\s+it\s+be\s+included|state\s+the\s+problem|research\s+question|anova',
                text_lower):
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

    def grade_question_cw10_1_answer(self, student_answer: str):

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

• What is the role of the 'Participant' variable? (5 points)  
• Should it be included in your analysis? Why? (5 points)  
• State the problem with your own words (5 points)  
• Formulate the main Research question (5 points)

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

**Component 1: Role of Participant Variable (5 points)**
The 'Participant' variable is an identifier/ID variable that uniquely identifies each subject in the study.
- 5 points: Correctly identifies as ID/identifier variable with clear explanation
- 4 points: Correct identification with minor clarity issues
- 3 points: Partially correct (e.g., mentions uniqueness but lacks precision)
- 2 points: Shows some understanding but confused or incomplete
- 1 point: Attempted but mostly incorrect
- 0 points: Completely blank

**Component 2: Should It Be Included & Why (5 points)**
The Participant variable should NOT be included in the analysis because:
- It's an identifier, not a variable of interest
- It doesn't contain meaningful data for statistical analysis
- Including ID variables can cause errors or meaningless results

- 5 points: Correctly states NO with clear, logical reasoning
- 4 points: Correct answer with good reasoning, minor gaps
- 3 points: Correct answer but weak or incomplete reasoning
- 2 points: Incorrect answer OR correct answer with illogical reasoning
- 1 point: Attempted but mostly wrong
- 0 points: Completely blank

**Component 3: Problem Statement (5 points)**
Should describe the Facebook friends dataset context (examining relationship between personality characteristics and number of Facebook friends).
- 5 points: Clear, specific, well-articulated problem in own words
- 4 points: Good statement with minor clarity issues
- 3 points: Problem present but vague or lacks context
- 2 points: Problem poorly articulated but shows some understanding
- 1 point: Attempted but unclear or off-topic
- 0 points: Completely blank

**Component 4: Research Question (5 points)**
Should formulate a testable question about the relationship between groups/conditions and number of Facebook friends.
- 5 points: Clear, testable question directly addressing the problem
- 4 points: Good question with minor precision issues
- 3 points: Question present but vague or partially addresses problem
- 2 points: Question unclear or poorly formulated
- 1 point: Attempted but not testable or irrelevant
- 0 points: Completely blank

---

EXAMPLE OF A COMPLETE ANSWER

Role of Participant Variable:
The 'Participant' variable is an identifier variable that assigns a unique number to each participant in the study. It serves to distinguish between different subjects.

Should It Be Included:
No, the Participant variable should not be included in the analysis. It is merely an ID number and does not contain any meaningful data about the participants' characteristics or outcomes. Including it would be inappropriate as it's not a variable of theoretical or practical interest.

Problem Statement:
This study examines whether there is a relationship between personality characteristics and the number of Facebook friends people have. Researchers want to understand if different personality types are associated with different levels of social media connectivity.

Research Question:
Is there a significant difference in the number of Facebook friends across different personality characteristic groups?

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
  "component_1_explanation": "<brief explanation for participant variable role>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<brief explanation for inclusion decision>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief explanation for problem statement>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief explanation for research question>",
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
        print("GRADING RESULTS - CW10_1")
        print("ANOVA - Facebook Friends Analysis")
        print("=" * 60)

        if 'component_1_score' in grading:
            # Originality check result
            if grading.get("originality_concern"):
                print("\n⚠️  ORIGINALITY CONCERN DETECTED")
                print("   All points frozen. See feedback below.")

            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Header): {20 - grading.get('formatting_deductions', 0)}/4")
            print(f"    • Student name:        {1 - grading.get('formatting_name_deduction', 0)}/1 (LLM)")
            print(f"    • Paper title:         {1 - grading.get('formatting_title_deduction', 0)}/1 (regex)")
            print(f"    • Task description:    {1 - grading.get('formatting_task_deduction', 0)}/1 (regex)")
            print(f"    • No autoformatting:   {1 - grading.get('formatting_autoformat_deduction', 0)}/1 (regex)")
            if grading.get('formatting_explanation'):
                print(f"   → {grading.get('formatting_explanation')}")

            print("\nCONTENT COMPONENTS:")
            print(f"  Component 1 (Participant Variable Role): {grading.get('component_1_score', 'N/A')}/5")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Should Be Included & Why): {grading.get('component_2_score', 'N/A')}/5")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Problem Statement): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Research Question): {grading.get('component_4_score', 'N/A')}/5")
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

    evaluator = CW10_1Evaluator()

    print("CLASSWORK 10.1 EVALUATOR")
    print("=" * 60)

    print("Enter student's answer (type END to finish):")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    student_answer = "\n".join(lines)

    grading = evaluator.grade_question_cw10_1_answer(student_answer)

    evaluator.print_grading_results(grading)
