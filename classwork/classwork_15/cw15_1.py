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

Student must:

• A. Include the main research question statement verbatim (5 points)
• B. Check sample adequacy using the KMO test and interpret it (5 points)
• C. Add Bartlett's test result and interpret whether correlations are sufficient (5 points)
• D. Include the Chi Squared model fit table and interpret whether the model fits (5 points)

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

**Layer 2: Content Components (4 points each, after formatting deductions)**

**Component A: Main Research Question Statement (4 points)**
Student must include the following statement verbatim or near-verbatim in their paper:
"We would like to know if these 9 variables could be shrunk down into a number of factors,
and hopefully fewer than 9. We would like to see some correlations between these items and,
as a result, a much smaller number of factors."

- 4 points: Statement included fully and correctly, clearly presented as the research question
- 3 points: Statement mostly present but slightly paraphrased or incomplete
- 2 points: Statement partially present — key ideas mentioned but significant parts missing
- 1 point: Only a vague reference to factor reduction without the actual statement
- 0 points: Completely absent

CRITICAL: This is not a student-formulated question — it must be the exact statement from the task.

**Component B: KMO Test and Sample Adequacy (4 points)**
Student must report the KMO value from JASP and interpret whether the sample is adequate
for factor analysis.

- 4 points: KMO value reported and correctly interpreted
  (KMO ≥ 0.6 = adequate; KMO ≥ 0.8 = good; KMO ≥ 0.9 = excellent)
- 3 points: KMO value reported but interpretation vague or incomplete
- 2 points: KMO mentioned but value not reported or interpretation missing
- 1 point: Sample adequacy mentioned without KMO value or any interpretation
- 0 points: Completely absent

Accept: any KMO value between 0 and 1 with an adequacy judgment.
Do NOT accept interpretation without a reported value.

**Component C: Bartlett's Test (4 points)**
Student must report Bartlett's test result from JASP and interpret whether correlations
are sufficient to proceed with factor analysis.

- 4 points: Bartlett's test result reported (χ², df, p-value) and correctly interpreted —
  significant result (p < .05) means correlations are sufficient to proceed
- 3 points: Result reported but interpretation incomplete or p-value missing
- 2 points: Bartlett's test mentioned but result not clearly reported
- 1 point: Only mentions that correlations were checked without Bartlett's test result
- 0 points: Completely absent

CRITICAL: A significant Bartlett's test (p < .05) means proceed; non-significant means stop.
Student must explicitly state this conclusion.

**Component D: Chi Squared Model Fit Table and Interpretation (4 points)**
Student must include the Chi Squared test table from JASP in APA style (numbered and titled)
and interpret whether the model fits the data.

- 4 points: Table present in APA style (numbered and titled) and interpretation correct —
  non-significant χ² (p > .05) indicates good model fit; significant χ² indicates poor fit
- 3 points: Table present but APA formatting incomplete, or interpretation vague
- 2 points: Table present but not in APA style and no interpretation, or interpretation
  present but no table
- 1 point: Chi Squared result mentioned without table or interpretation
- 0 points: Completely absent

CRITICAL: Model fit interpretation is the opposite of Bartlett's — here a NON-significant
result is desirable (indicates the model fits).
CRITICAL: Table must be numbered and titled in APA style to receive full marks.

---

EXAMPLE OF A COMPLETE ANSWER

A. Research Question:
We would like to know if these 9 variables could be shrunk down into a number of factors,
and hopefully fewer than 9. We would like to see some correlations between these items and,
as a result, a much smaller number of factors.

B. KMO Test:
The Kaiser-Meyer-Olkin measure of sampling adequacy was KMO = 0.85, which is considered
good, indicating that the sample is adequate for factor analysis.

C. Bartlett's Test:
Bartlett's test of sphericity was significant, χ²(36) = 1245.67, p < .001, indicating
that the correlations among items are sufficient to proceed with factor analysis.

Table 1.
Bartlett's Test of Sphericity
[table content]

D. Model Fit:
Table 2.
Chi Squared Test of Model Fit
[table content]

The Chi Squared test was non-significant, χ²(18) = 24.31, p = .114, indicating that
the model fits the data adequately.

---

ORIGINALITY CHECK:

IMPORTANT:
Students are required to copy the following task description into their answer.
This exact text is NEVER an originality concern and must be fully excluded before evaluation:

--- TASK DESCRIPTION START ---
We would like to know if these 9 variables could be shrunk down into a number of factors,
and hopefully fewer than 9. We would like to see some correlations between these items and,
as a result, a much smaller number of factors.
--- TASK DESCRIPTION END ---

STEP 1: Remove any text matching or paraphrasing the block above.
STEP 2: Evaluate ONLY what remains — the student's own KMO interpretation, Bartlett's result,
and model fit interpretation.
STEP 3: Set originality_concern = true ONLY if the remaining text is AI-generated, generic,
and contains no personal reasoning connected to the specific EFA output values.

Otherwise set originality_concern = false.

DO NOT modify or override component scores based on originality_concern.

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
  "component_1_explanation": "<brief explanation for formatting>",
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief explanation for research question statement>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief explanation for KMO test>",
  "component_4_score": <0-4>,
  "component_4_explanation": "<brief explanation for Bartlett's test>",
  "component_5_score": <0-4>,
  "component_5_explanation": "<brief explanation for Chi Squared model fit>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression>"
}}

SCORING INSTRUCTIONS:

component_1_name_score = 1 if valid name found, else 0
component_1_title_score = 1 if paper_title_present else 0
component_1_task_score = 1 if task_description_present else 0
component_1_autoformat_score = 1 if no_autoformatting_present else 0
component_1_score = component_1_name_score + component_1_title_score + component_1_task_score + component_1_autoformat_score

total_points = component_1_score + component_2_score + component_3_score + component_4_score + component_5_score
"""
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
            print(f"  Component 1 (Header): {4 - grading.get('formatting_deductions', 0)}/4")
            print(f"    • Student name:        {1 - grading.get('formatting_name_deduction', 0)}/1 (LLM)")
            print(f"    • Paper title:         {1 - grading.get('formatting_title_deduction', 0)}/1 (regex)")
            print(f"    • Task description:    {1 - grading.get('formatting_task_deduction', 0)}/1 (string match)")
            print(f"    • No autoformatting:   {1 - grading.get('formatting_autoformat_deduction', 0)}/1 (regex)")
            if grading.get('formatting_explanation'):
                print(f"   → {grading.get('formatting_explanation')}")

            print("\nCONTENT COMPONENTS:")
            print(f"  Component A (Research Question Statement): {grading.get('component_2_score', 'N/A')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component B (KMO Test): {grading.get('component_3_score', 'N/A')}/4")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component C (Bartlett's Test): {grading.get('component_4_score', 'N/A')}/4")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component D (Chi Squared Model Fit): {grading.get('component_5_score', 'N/A')}/4")
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