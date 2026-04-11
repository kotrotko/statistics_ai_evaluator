"""
cw13_1.py
Classwork 13: Linear Regression
Evaluation method name: def grade_question_cw13_1_answer
"""

import re
import textwrap
from config import BaseEvaluator


class CW13_1Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 13_1.

    Task: State the problem with your own words (5 points) and formulate Research question (5 points).
    What is a predictor? What is criterion (outcome) variable? (5 points)
    For Linear Regression in JASP tab, which variable is Dependent? Which one is Predictor
    (independent Variable)? (5 points).
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
            r'^\s*classwork\s*13',
            r'^\s*cw\s*13\b',
            r'^\s*class\s*work\s*(week\s*)?13',
            r'^\s*in.?class\s*13'
        ]

        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["paper_title"] = True
                evidence.append("Title found")
                break

        if re.search(
                r'linear\s*regression|predictor|criterion|outcome\s*variable|dependent\s*variable|jasp|research\s+question|state\s+the\s+problem|problem\s+statement',
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

    def grade_question_cw13_1_answer(self, student_answer: str):

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

• State the problem with your own words (5 points)
• Formulate the main Research question (5 points)
• Explain what a predictor and criterion (outcome) variable are (5 points)
• Identify which variable is Dependent and which is Predictor in the JASP Linear Regression tab (5 points)

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

**Layer 2: Content Components (4 points each)**

**Component 2: Problem Statement (4 points)**
Student must describe the research problem in their own words, connected to the context of linear regression.

- 4 points: Clear, specific, well-articulated problem in own words
- 3 points: Problem present but vague or lacks context
- 2 points: Problem poorly articulated but shows some understanding
- 1 point: Attempted but unclear or off-topic
- 0 points: Completely blank

**Component 3: Research Question (4 points)**
Student must formulate a clear, testable Research Question appropriate for linear regression analysis.

- 4 points: Clear, testable question directly addressing the problem
- 3 points: Question present but vague or partially addresses problem
- 2 points: Question unclear or poorly formulated
- 1 point: Attempted but not testable or irrelevant
- 0 points: Completely blank

**Component 4: Predictor and Criterion Variable Definitions (4 points)**
Student must correctly define both the predictor (independent) variable and the criterion (outcome) variable.

- 4 points: Both defined correctly with clear explanation of their roles in regression
- 3 points: One defined correctly, other vague or missing
- 2 points: Both attempted but definitions unclear or partially wrong
- 1 point: Minimal attempt
- 0 points: Completely blank

Accept: "predictor predicts the outcome", "criterion is what we are trying to predict",
"independent variable", "dependent variable", "outcome variable".
Do NOT accept definitions that confuse predictor with criterion.

**Component 5: JASP Variable Assignment (4 points)**
Student must correctly identify which variable goes in the Dependent box and which goes in the Predictor box in the JASP Linear Regression tab.

- 4 points: Correctly states criterion/outcome = Dependent, predictor/independent = Predictor (Covariates), with clear reasoning
- 3 points: One assignment correct, other missing or wrong
- 2 points: Both attempted but with confusion between the two
- 1 point: Minimal attempt
- 0 points: Completely blank

Accept: "the criterion variable goes into the Dependent box", "the predictor goes into Covariates or Predictor box".
Do NOT accept reversed assignments.

---

EXAMPLE OF A COMPLETE ANSWER

Problem Statement:
This study investigates whether a predictor variable can significantly explain variance in a criterion (outcome) variable using linear regression. The goal is to determine the direction and strength of the linear relationship between the two variables.

Research Question:
Does the predictor variable significantly predict the criterion variable in a linear regression model?

Predictor and Criterion Definitions:
The predictor (independent) variable is the variable used to predict or explain changes in another variable. The criterion (outcome) variable is the dependent variable — the one we are trying to predict or explain.

JASP Variable Assignment:
In the JASP Linear Regression tab, the criterion (outcome) variable is placed in the Dependent box, and the predictor (independent) variable is placed in the Covariates (Predictor) box.

---
ORIGINALITY CHECK:

IMPORTANT:
Students are required to copy the following task description into their answer.
This exact text is NEVER an originality concern and must be fully excluded before evaluation:

--- TASK DESCRIPTION START ---
State the problem with your own words (5 points) and formulate Research question (5 points).
What is a predictor? What is criterion (outcome) variable? (5 points)
For Linear Regression in JASP tab, which variable is Dependent? Which one is Predictor (independent Variable)? (5 points).
--- TASK DESCRIPTION END ---

STEP 1: Remove any text matching or paraphrasing the block above.
STEP 2: Evaluate ONLY what remains — the student's own problem statement, research question, definitions, and JASP variable assignment.
STEP 3: Set originality_concern = true ONLY if the remaining text is AI-generated, generic, and contains no personal reasoning connected to the task.

Otherwise set originality_concern = false.

DO NOT modify or override component scores based on originality_concern.

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
  "component_1_score": <0-4>,
  "component_1_explanation": "<brief explanation for problem statement>",
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief explanation for research question>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief explanation for predictor and criterion definitions>",
  "component_4_score": <0-4>,
  "component_4_explanation": "<brief explanation for JASP variable assignment>",
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
                "component_4_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results."""
        print("=" * 60)
        print("GRADING RESULTS - CW13_1")
        print("Linear Regression - Problem, RQ, Variables")
        print("=" * 60)

        if 'component_1_score' in grading:
            # Originality check result
            if grading.get("originality_concern"):
                print("\n⚠️  ORIGINALITY CONCERN DETECTED")
                print("   All points frozen. See feedback below.")

            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Header): {4 - grading.get('formatting_deductions', 0)}/4")
            print(f"    • Student name:        {1 - grading.get('formatting_name_deduction', 0)}/1 (LLM)")
            print(f"    • Paper title:         {1 - grading.get('formatting_title_deduction', 0)}/1 (regex)")
            print(f"    • Task description:    {1 - grading.get('formatting_task_deduction', 0)}/1 (regex)")
            print(f"    • No autoformatting:   {1 - grading.get('formatting_autoformat_deduction', 0)}/1 (regex)")
            if grading.get('formatting_explanation'):
                print(f"   → {grading.get('formatting_explanation')}")

            print("\nCONTENT COMPONENTS:")
            print(f"  Component 2 (Problem Statement): {grading.get('component_1_score', 'N/A')}/4")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 3 (Research Question): {grading.get('component_2_score', 'N/A')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 4 (Predictor and Criterion Definitions): {grading.get('component_3_score', 'N/A')}/4")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 5 (JASP Variable Assignment): {grading.get('component_4_score', 'N/A')}/4")
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

    evaluator = CW13_1Evaluator()

    print("CLASSWORK 13.1 EVALUATOR")
    print("=" * 60)

    print("Enter student's answer (type END to finish):")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    student_answer = "\n".join(lines)

    grading = evaluator.grade_question_cw13_1_answer(student_answer)

    evaluator.print_grading_results(grading)

