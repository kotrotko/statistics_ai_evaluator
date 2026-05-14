"""
cw15_2.py
Classwork 15: Exploratory Factor Analysis
Factor Creation and Rotation
Evaluation method name: def grade_question_cw15_2_answer
"""

import re
import textwrap
from config import BaseEvaluator


class CW15_2Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 15_2.

    Task: Factor Creation and Rotation.
    Factor Loadings table with promax rotation (3 points).
    A. Number of Factors — changes with eigenvalue (5 points) + most reasonable (5 points).
    B. Rotation — oblique vs orthogonal comparison (5 points).
    Formatting: task description (1 point) + no autoformatting (1 point).
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

        pedagogical_markers = [
            "what is proportion of items",
            "how many factors do you see",
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

        if elements_found["no_autoformatting"]:
            evidence.append("No autoformatting found")

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def grade_question_cw15_2_answer(self, student_answer: str):

        formatting_check = self.check_formatting_elements(student_answer)
        fs = formatting_check["elements_found"]

        formatting_block = f"""
HEADER DETECTION RESULTS (USE AS FACTS):

task_description_present = {fs["task_description"]}
no_autoformatting_present = {fs["no_autoformatting"]}
"""

        prompt = f"""{formatting_block}

You are grading a statistics classwork assignment on Exploratory Factor Analysis.

TASK: Factor Creation and Rotation.

Use STRICT rubric-based grading. Total score MUST be exactly 20 points.

RUBRIC

Component 1: Formatting (2 points)
Start with 2 points.

Step 1 Task description (1 point)
Use task_description_present

Step 2 No autoformatting (1 point)
Use no_autoformatting_present

Component 2: Factor Loadings Table (3 points)
Student must include the Factor Loadings table based on promax rotation and interpret it.

Sub-component 2a: Three-factor structure identification (1 point)
- 1 point: Student correctly identifies that the promax rotation produced a three-factor structure
- 0 points: Number of factors not identified or incorrectly stated

Sub-component 2b: Factor composition interpretation (1 point)
- 1 point: Student accurately describes which items load on each factor
  (Factor 1: x4, x5, x6; Factor 2: x7, x8, x9; Factor 3: x1, x2, x3)
  and links them to underlying constructs
- 0 points: Factor composition missing, incomplete, or incorrect

Sub-component 2c: Loading quality evaluation (1 point)
- 1 point: Student correctly evaluates loading quality (≥ .40 = acceptable/strong)
  AND appropriately identifies weaker items (x2, x9) with higher uniqueness
  as less representative of their factors
- 0 points: Loading quality not evaluated or weaker items not identified

Component 3: Changes in Number of Extracted Factors (5 points)
Student must describe what happens to the number of extracted factors
as eigenvalue cut-off changes (trying values 1, 2, 3, 4, and 0).

- 5 points: Clear explanation that higher eigenvalue cut-off = fewer factors retained,
  lower cut-off = more factors; mentions behavior at specific values tried
- 4 points: General direction correct but missing specific eigenvalue values or behavior at 0
- 3 points: Partial explanation — mentions change in number of factors but vague
- 2 points: Mentions eigenvalue and factors but relationship unclear
- 1 point: Only states that the number changes without any explanation
- 0 points: Completely absent

Component 4: Most Reasonable Number of Factors (5 points)
Student must identify the most reasonable eigenvalue setting and justify why.

- 5 points: Identifies eigenvalue > 1 as most reasonable AND provides clear justification
  (e.g., meaningful loadings, interpretable structure, stable factors)
- 4 points: Correct choice with partial justification
- 3 points: Reasonable choice but justification vague or missing
- 2 points: Incorrect choice but justification shows some understanding
- 1 point: States a preference without any reasoning
- 0 points: Completely absent

Component 5: Oblique Rotation Comparison (5 points)
Student must compare orthogonal (Varimax) and oblique rotation results and
justify which is more appropriate for their data.

Sub-component 5a: What changes (2 points)
- 2 points: Student describes specific changes in factor loadings or structure
  when switching from orthogonal to oblique rotation
- 1 point: Vague mention that something changes without specific description
- 0 points: No comparison made

Sub-component 5b: Better solution (3 points)
- 3 points: Student argues oblique is more appropriate AND provides clear reasoning
  (factors are likely correlated; more realistic interpretation; shares variance)
- 2 points: Correct choice with partial reasoning
- 1 point: States preference without reasoning
- 0 points: Completely absent or incorrect conclusion

---

EXAMPLE OF A COMPLETE ANSWER

Factor Loadings:
Table 4. Factor Loadings.
The promax rotation identified a three-factor structure. Factor 1 was mainly defined
by x5, x4, and x6; Factor 2 by x7, x8, and x9; Factor 3 by x3, x1, and x2.
Most items showed strong factor loadings (≥ .40), indicating meaningful clustering
into latent factors. However, x2 and x9 showed relatively weaker loadings and higher
uniqueness, indicating weaker representation within their factors.

A. Number of Factors:
As the eigenvalue cut-off increased from 1 to 2, 3, and 4, fewer factors were extracted
because only stronger factors were retained. Setting it to 0 allowed more factors or
produced an error. The eigenvalue criterion directly determines the number of extracted factors.
The most reasonable solution is eigenvalue > 1 because it retained three factors with
meaningful loadings and interpretable structure.

B. Rotation:
Under oblique rotation, some factor loadings changed in size and variables loaded more
clearly on specific factors. The oblique solution was more interpretable and realistic
because the latent factors were likely related rather than completely independent.

---

ORIGINALITY CHECK:

IMPORTANT:
Students are required to copy the following task description into their answer.
This exact text is NEVER an originality concern and must be fully excluded before evaluation:

--- TASK DESCRIPTION START ---
Include Factor Loadings table, based on promax rotation. How many factors do you see?
What is proportion of items (just high or low) shows strong factor loading (≥ .40)?
What does it mean in terms of clustering into latent factors?
Which items showed weaker loading and higher uniqueness?
A. Number of Factors. Play with different values for Eigenvalues: try 1, 2, 3, 4 and 0.
B. Rotation. Play with Rotation using Eigenvalues = 1. Apply orthogonal, then oblique rotation.
--- TASK DESCRIPTION END ---

STEP 1: Remove any text matching or paraphrasing the block above.
STEP 2: Evaluate ONLY what remains.
STEP 3: Set originality_concern = true ONLY if the remaining text is AI-generated, generic,
and contains no personal reasoning connected to the specific EFA output values.

Otherwise set originality_concern = false.

DO NOT modify or override component scores based on originality_concern.

STUDENT ANSWER:
{student_answer}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief explanation for formatting>",
  "component_2_score": <0-3>,
  "component_2a_score": <0-1>,
  "component_2b_score": <0-1>,
  "component_2c_score": <0-1>,
  "component_2_explanation": "<brief explanation for factor loadings table>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief explanation for changes in number of factors>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief explanation for most reasonable number of factors>",
  "component_5_score": <0-5>,
  "component_5a_score": <0-2>,
  "component_5b_score": <0-3>,
  "component_5_explanation": "<brief explanation for oblique rotation comparison>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression>"
}}

SCORING INSTRUCTIONS:

component_1_task_score = 1 if task_description_present else 0
component_1_autoformat_score = 1 if no_autoformatting_present else 0
component_1_score = component_1_task_score + component_1_autoformat_score

component_2_score = component_2a_score + component_2b_score + component_2c_score

component_5_score = component_5a_score + component_5b_score

total_points = component_1_score + component_2_score + component_3_score + component_4_score + component_5_score
"""

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
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results."""
        print("=" * 60)
        print("GRADING RESULTS - CW15_2")
        print("EFA - Factor Creation and Rotation")
        print("=" * 60)

        if "component_1_score" in grading:
            if grading.get("originality_concern"):
                print("\n⚠️  ORIGINALITY CONCERN DETECTED")
                print("   All points frozen. See feedback below.")

            print("\nCOMPONENT BREAKDOWN:")
            print(f"\nFormatting: {grading.get('component_1_score')}/2")
            print(f"  • Task description:  {grading.get('component_1_task_score')}/1 (string match)")
            print(f"  • No autoformatting: {grading.get('component_1_autoformat_score')}/1 (regex)")
            if grading.get('component_1_explanation'):
                print(f"   → {grading.get('component_1_explanation')}")

            print(f"\nFactor Loadings Table: {grading.get('component_2_score')}/3")
            print(f"  • Three-factor structure:       {grading.get('component_2a_score')}/1")
            print(f"  • Factor composition:           {grading.get('component_2b_score')}/1")
            print(f"  • Loading quality evaluation:   {grading.get('component_2c_score')}/1")
            if grading.get('component_2_explanation'):
                print(f"  → {grading.get('component_2_explanation')}")

            print(f"\nChanges in Number of Factors: {grading.get('component_3_score')}/5")
            if grading.get('component_3_explanation'):
                print(f"  → {grading.get('component_3_explanation')}")

            print(f"\nMost Reasonable Number of Factors: {grading.get('component_4_score')}/5")
            if grading.get('component_4_explanation'):
                print(f"  → {grading.get('component_4_explanation')}")

            print(f"\nOblique Rotation Comparison: {grading.get('component_5_score')}/5")
            print(f"  • What changes:    {grading.get('component_5a_score')}/2")
            print(f"  • Better solution: {grading.get('component_5b_score')}/3")
            if grading.get('component_5_explanation'):
                print(f"  → {grading.get('component_5_explanation')}")

            print(f"\n  {'─' * 40}")

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

    evaluator = CW15_2Evaluator()

    print("CLASSWORK 15.2 EVALUATOR")
    print("=" * 60)

    print("Enter student's answer (type END to finish):")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    student_answer = "\n".join(lines)

    grading = evaluator.grade_question_cw15_2_answer(student_answer)

    evaluator.print_grading_results(grading)
