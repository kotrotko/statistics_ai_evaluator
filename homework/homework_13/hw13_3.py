"""
hw13_3.py
Linear Regression - Fill out ANOVA tables for simple linear regressions
Evaluation method name: def grade_hw13_3_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW13_3Evaluator(BaseEvaluator):
    """
    Evaluator for ANOVA Tables for Simple Linear Regression (HW13_3).

    Task: Fill out the rest of the ANOVA tables below for simple linear regressions:
    a. SS Model = 34.21, SS Total = 66.12, df Total = 54
    b. MS Model = 6.03, df Error = 16, SS Total = 19.98
    Is the model significant at α = 0.05? How do you know?

    Evaluates student's ability to correctly complete ANOVA tables for simple
    linear regression and interpret model significance.

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

        # Task description (pedagogical markers)
        pedagogical_markers = [
            "fill out the rest of the anova tables",
            "simple linear regressions",
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

    def grade_hw13_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Homework 13.3: ANOVA tables for simple linear regression.
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
                    "component_2_score": 8,
                    "component_3_score": 8,
                    "component_4_score": 2,
                },
                max_points=20,
                feedback="[TEST MODE] Both ANOVA tables completed correctly. Model significance correctly interpreted.",
                vibe="Student demonstrates solid understanding of ANOVA table structure for simple linear regression.",
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
        You are grading a statistics assignment where a student must complete two ANOVA tables
        for simple linear regressions and interpret model significance.

Use a **STRICT rubric-based approach**. Total score MUST be exactly 20 points.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. 0 only if completely blank
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. For low-scoring answers, use encouraging language: "Credit for trying, but..."

---

**CORRECT ANSWERS:**

**Table a:** Given: SS Model = 34.21, SS Total = 66.12, df Total = 54
- df Model = 1 (simple linear regression always has df Model = 1)
- df Error = 53 (df Total − df Model = 54 − 1)
- SS Error = 31.91 (SS Total − SS Model = 66.12 − 34.21)
- MS Model = 34.21 (SS Model / df Model = 34.21 / 1)
- MS Error = 0.602 (SS Error / df Error = 31.91 / 53)
- F = 56.83 (MS Model / MS Error = 34.21 / 0.602)

**Table b:** Given: MS Model = 6.03, df Error = 16, SS Total = 19.98
- df Model = 1 (simple linear regression)
- df Total = 17 (df Model + df Error = 1 + 16)
- SS Model = 6.03 (MS Model × df Model = 6.03 × 1)
- SS Error = 13.95 (SS Total − SS Model = 19.98 − 6.03)
- MS Error = 0.872 (SS Error / df Error = 13.95 / 16)
- F = 6.91 (MS Model / MS Error = 6.03 / 0.872)

**Significance interpretation:**
- Table a: F(1, 53) = 56.83 exceeds critical value ≈ 4.03 at α = 0.05, so model is significant
- Table b: F(1, 16) = 6.91 exceeds critical value ≈ 4.49 at α = 0.05, so model is significant

Accept minor rounding differences (e.g. F = 56.8 or 56.84 for table a; F = 6.9 or 6.92 for table b).

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

**Component 2: Table a — Completed Correctly (8 points)**

Award points for each correctly computed cell:
- df Model = 1: 1 point
- df Error = 53: 1 point
- SS Error = 31.91: 1 point
- MS Model = 34.21: 1 point
- MS Error = 0.602 (accept 0.60): 2 points
- F = 56.83 (accept 56.8–56.9): 2 points

---

**Component 3: Table b — Completed Correctly (8 points)**

Award points for each correctly computed cell:
- df Model = 1: 1 point
- df Total = 17: 1 point
- SS Model = 6.03: 1 point
- SS Error = 13.95: 1 point
- MS Error = 0.872 (accept 0.87): 2 points
- F = 6.91 (accept 6.9–6.92): 2 points

---

**Component 4: Significance Interpretation (2 points)**

Student must state whether each model is significant at α = 0.05 and explain how they know
(by comparing F to critical value, or p < .05).

- 2 points: Both tables interpreted correctly with reasoning
- 1 point: One table interpreted correctly, or both stated without reasoning
- 0 points: No interpretation or completely wrong

CRITICAL: Both models are significant. Any answer stating otherwise is wrong.

---

**COMMON MISTAKES TO WATCH FOR:**

❌ Using df Model > 1 (for simple linear regression df Model is always 1)
❌ Computing MS = SS × df instead of SS / df
❌ Computing F = MS Error / MS Model instead of MS Model / MS Error
❌ Forgetting to compute SS Error before MS Error
❌ Stating models are not significant

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
  "component_2_score": <0-8>,
  "component_2_explanation": "<brief explanation for table a>",
  "component_3_score": <0-8>,
  "component_3_explanation": "<brief explanation for table b>",
  "component_4_score": <0-2>,
  "component_4_explanation": "<brief explanation for significance interpretation>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of ANOVA tables>"
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
        print("GRADING RESULTS - HW13_3")
        print("ANOVA Tables for Simple Linear Regression")
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

            print(f"  Component 2 (Table a): {grading.get('component_2_score', 'N/A')}/8")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Table b): {grading.get('component_3_score', 'N/A')}/8")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Significance Interpretation): {grading.get('component_4_score', 'N/A')}/2")
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

    evaluator = HW13_3Evaluator()

    print("=" * 60)
    print("HOMEWORK 13.3 EVALUATOR")
    print("ANOVA Tables for Simple Linear Regression")
    print("=" * 60)
    print("\nPlease enter the student's answer to HOMEWORK 13_3.")
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

    grading = evaluator.grade_hw13_3_answer(student_answer)

    evaluator.print_grading_results(grading)
