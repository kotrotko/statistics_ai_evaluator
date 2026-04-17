"""
hw13_4.py
Linear Regression - Predicting scores using the line of best fit
Evaluation method name: def grade_hw13_4_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW13_4Evaluator(BaseEvaluator):
    """
    Evaluator for Predicting Scores Using Line of Best Fit (HW13_4).

    Task: Using the line of best fit equation created in problem 7, predict the scores
    for how successful people will be based on how much they study:
    a. X = 1.20
    b. X = 3.33
    c. X = 0.71
    d. X = 4.00

    Equation from problem 7: Ŷ = 1.79 + 0.575X

    Evaluates student's ability to correctly apply the regression equation
    to predict scores for four given X values.

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    def __init__(self):
        """Initialize the evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1500
        )

    def check_formatting_elements(self, student_answer: str) -> dict:
        """
        Check if required structural and content elements are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "no_autoformatting": True,
        }

        evidence = []

        # Task description (pedagogical marker — unique phrase from the task)
        pedagogical_markers = [
            "using the line of best fit equation created in problem 7, predict",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # No autoformatting (strict)
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
            "evidence": evidence if evidence else ["No clear formatting indicators found"]
        }

    def grade_hw13_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Homework 13.4: Predicting scores using the line of best fit.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API

        Returns:
            Detailed grading breakdown dictionary
        """

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
                feedback="[TEST MODE] All formatting elements present. All four predictions correctly calculated.",
                vibe="Student demonstrates solid understanding of applying the regression equation.",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "task_description": True,
                            "no_autoformatting": True,
                        },
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        formatting_check = self.check_formatting_elements(student_answer)
        formatting_summary = formatting_check["elements_found"]

        formatting_block = f"""
        HEADER DETECTION RESULTS (DO NOT RE-EVALUATE — USE AS FACTS):

        task_description_present = {formatting_summary["task_description"]}
        no_autoformatting_present = {formatting_summary["no_autoformatting"]}

        You MUST deduct points in Component 1 strictly according to these values.
        If task_description_present = False, you MUST deduct 1 point.
        If no_autoformatting_present = False, you MUST deduct 1 point.
        """

        prompt = f"""{formatting_block}
        You are grading a statistics assignment where a student must predict scores
        using the line of best fit equation Ŷ = 1.79 + 0.575X for four given X values.

Use a **STRICT rubric-based approach**. Total score MUST be exactly 20 points.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. 0 only if completely blank
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. For low-scoring answers, use encouraging language: "Credit for trying, but..."

---

**CORRECT ANSWERS:**

Equation from problem 7: Ŷ = 2.025 + 0.5746X
(b = 0.65 × (0.99 / 1.12) = 0.5746, a = 2.95 − 0.5746 × 1.61 = 2.025)

a. X = 1.20 → Ŷ = 2.025 + 0.5746 × 1.20 = **2.714**
b. X = 3.33 → Ŷ = 2.025 + 0.5746 × 3.33 = **3.938**
c. X = 0.71 → Ŷ = 2.025 + 0.5746 × 0.71 = **2.433**
d. X = 4.00 → Ŷ = 2.025 + 0.5746 × 4.00 = **4.323**

Accept minor rounding differences of ±0.05 to account for intermediate rounding.
Accept any answer that is internally consistent with the student's own problem 7 equation.
Award full marks if the student applies their own equation correctly and consistently.

Note: The textbook uses b = 0.72 and a = 1.79, which contains an arithmetic error.
If a student uses Ŷ = 1.79 + 0.72X consistently, accept:
a. 2.65, b. 4.19, c. 2.30, d. 4.67

---

**RUBRIC:**

**Component 1: Header & Structural Integrity (2 points)**

Start at 2 points.

Deduct 1 point for each missing element:

STEP 1 - Task Description [STRICT]
Use task_description_present.
If False: deduct 1 point. Add: "Task description is missing. -1 point."

STEP 2 - No autoformatting [STRICT]
Use no_autoformatting_present.
If False: deduct 1 point. Add: "Autoformatting detected. -1 point."

---

**Component 2: Predictions a and b (6 points)**

PREDICTION a: X = 1.20 (3 points)
- Correct substitution shown (1 pt): Ŷ = 2.025 + 0.5746 × 1.20 or equivalent
- Correct final answer (2 pts): 2.714 (accept 2.65–2.75)

PREDICTION b: X = 3.33 (3 points)
- Correct substitution shown (1 pt): Ŷ = 2.025 + 0.5746 × 3.33 or equivalent
- Correct final answer (2 pts): 3.938 (accept 3.88–3.99)

---

**Component 3: Predictions c and d (6 points)**

PREDICTION c: X = 0.71 (3 points)
- Correct substitution shown (1 pt): Ŷ = 2.025 + 0.5746 × 0.71 or equivalent
- Correct final answer (2 pts): 2.433 (accept 2.38–2.48)

PREDICTION d: X = 4.00 (3 points)
- Correct substitution shown (1 pt): Ŷ = 2.025 + 0.5746 × 4.00 or equivalent
- Correct final answer (2 pts): 4.323 (accept 4.27–4.37)

---

**Component 4: Overall Quality (6 points)**

- 6 points: All four predictions correct, equation clearly applied, work shown
- 5 points: Three correct, or all four correct but no work shown
- 4 points: Two correct
- 2-3 points: One correct or partial work shown
- 1 point: Minimal attempt — equation referenced but no correct predictions
- 0 points: Blank or completely wrong

---

**COMMON MISTAKES TO WATCH FOR:**

❌ Using the wrong equation (not from problem 7)
❌ Mixing b = 0.575 and b = 0.72 inconsistently across predictions
❌ Correct substitution but arithmetic error in final answer
❌ Using X values in wrong order (e.g. swapping a and b)

---

**ORIGINALITY CHECK:**
Before finalizing scores, assess whether the answer appears to be AI-generated or copied.
Signs include: textbook-perfect phrasing with no personal voice, unnaturally polished
structure, or language that reads like a Wikipedia/ChatGPT excerpt rather than a student explanation.
- If originality concern detected: set all component scores to 0, set originality_concern to true,
  and set feedback to EXACTLY: "Due to originality concern, your points are frozen. You can get them back if you provide oral explanation for this paper."
- If original student work: set originality_concern to false and proceed normally.

---

**STUDENT ANSWER:**
{student_answer}

**SCORING INSTRUCTIONS FOR SUB-SCORES:**

For component_1_task_score: use task_description_present (1 if True, 0 if False)
For component_1_autoformat_score: use no_autoformatting_present (1 if True, 0 if False)

Return grading in this exact JSON format:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief explanation for header>",
  "component_2_score": <0-6>,
  "component_2_explanation": "<brief explanation for predictions a and b>",
  "component_3_score": <0-6>,
  "component_3_explanation": "<brief explanation for predictions c and d>",
  "component_4_score": <0-6>,
  "component_4_explanation": "<brief explanation for overall quality>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of regression prediction>"
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
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results."""
        print("=" * 60)
        print("GRADING RESULTS - HW13_4")
        print("Predicting Scores Using Line of Best Fit")
        print("=" * 60)

        if 'component_1_score' in grading:
            if grading.get("originality_concern"):
                print("\n⚠️  ORIGINALITY CONCERN DETECTED")
                print("   All points frozen. See feedback below.")

            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Header): {grading.get('component_1_score', 'N/A')}/2")
            print(f"    • Task description:    {grading.get('component_1_task_score', 'N/A')}/1 (string match)")
            print(f"    • No autoformatting:   {grading.get('component_1_autoformat_score', 'N/A')}/1 (regex)")
            if grading.get('component_1_explanation'):
                print(f"   → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Predictions a and b): {grading.get('component_2_score', 'N/A')}/6")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Predictions c and d): {grading.get('component_3_score', 'N/A')}/6")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Overall Quality): {grading.get('component_4_score', 'N/A')}/6")
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
            if 'raw_response' in grading:
                print("\nRaw Response:")
                print(grading['raw_response'][:500])


if __name__ == "__main__":
    print("Welcome to the Homework AI Evaluator System!")
    print("=" * 60)

    evaluator = HW13_4Evaluator()

    print("=" * 60)
    print("HOMEWORK 13.4 EVALUATOR")
    print("Predicting Scores Using Line of Best Fit")
    print("=" * 60)
    print("\nPlease enter the student's answer to HOMEWORK 13_4.")
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

    grading = evaluator.grade_hw13_4_answer(student_answer)

    evaluator.print_grading_results(grading)
