"""
hw9_2.py
Standard Error Calculation
Evaluation method name: def grade_hw9_2_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW9_2Evaluator(BaseEvaluator):
    """
    Evaluator for Standard Error Calculation (HW9_2).

    Task: Calculate the standard error from the following descriptive statistics
    a. s1 = 24, s2 = 21, n1 = 36, n2 = 49
    b. s1 = 15.40, s2 = 14.80, n1 = 20, n2 = 23
    c. s1 = 12, s2 = 10, n1 = 25, n2 = 25

    Evaluates student's ability to calculate standard error correctly
    using the formula for independent samples.

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
        first_lines = student_answer[:200]

        elements_found = {
            "task_description": False,
            "no_autoformatting": True,
        }

        evidence = []

        # STEP 2 — Task description (strict)
        if re.search(r'calculate.*standard\s+error.*from.*following|a\.\s*s1\s*=\s*24|s1\s*=\s*24.*s2\s*=\s*21.*n1\s*=\s*36', text_lower):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # STEP 3 — No autoformatting (strict)
        autoformat_patterns = [
            r'(?m)(?:^\s*\d+[\.\)]\s+\S.*\n){2,}',  # only 2+ consecutive numbered lines
            r'^\s*[-•*]\s+\S',  # bullet list: -, •, *
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

    def grade_hw9_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 9_2: Calculate standard error from descriptive statistics.
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
                    "component_1_title_score": 1,
                    "component_1_task_score": 1,
                    "component_1_autoformat_score": 1,
                    "component_2_score": 6,
                    "component_3_score": 6,
                    "component_4_score": 6,
                },
                max_points=20,
                feedback="[TEST MODE] All formatting elements present. Calculations demonstrate understanding of standard error formula.",
                vibe="Student shows competence in applying the standard error formula with minor computational issues.",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "paper_title": True,
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
        If paper_title_present = False, you MUST deduct 1 point.
        If task_description_present = False, you MUST deduct 1 point.
        If no_autoformatting_present = False, you MUST deduct 1 point.
        """

        prompt = f"""{formatting_block}
        You are grading a statistics assignment where a student must:
"Calculate the standard error from the following descriptive statistics
a. s1 = 24, s2 = 21, n1 = 36, n2 = 49
b. s1 = 15.40, s2 = 14.80, n1 = 20, n2 = 23
c. s1 = 12, s2 = 10, n1 = 25, n2 = 25"

Use a **STRICT rubric-based approach**. Total score MUST be exactly 20 points.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. 0 only if completely blank
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. For 1-point answers, use encouraging language: "Credit for trying, but..."

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

**Component 2: Part (a) Standard Error Calculation (6 points)**

Given: s1 = 24, s2 = 21, n1 = 36, n2 = 49

The student must calculate the standard error using the formula:
SE = sqrt((s1²/n1) + (s2²/n2))

**CORRECT ANSWER:**
SE = sqrt((24²/36) + (21²/49))
SE = sqrt((576/36) + (441/49))
SE = sqrt(16 + 9)
SE = sqrt(25)
SE = 5.00

**EVALUATION STEPS:**

STEP 1: Is the formula shown or implied? (2 points)
- Full credit: SE = sqrt((s1²/n1) + (s2²/n2)) or equivalent shown
- Partial: Formula implied through correct calculations
- None: No formula or incorrect formula used

STEP 2: Are calculations shown and correct? (2 points)
- Full credit (2 pts): All intermediate steps shown correctly
- Partial (1 pt): Some steps shown but with minor errors
- None (0 pts): No work shown or major computational errors

STEP 3: Is the final answer correct? (2 points)
- Full credit: SE ≈ 5.00 (accept 5, 5.0, 5.00)
- Partial: Close answer due to rounding (4.9-5.1)
- None: Incorrect answer

**Scoring:**
- 6 points: Formula shown, all work correct, correct answer
- 4 points: Formula shown, minor computational error, close answer
- 3 points: Formula shown, major computational error 
- 1 point: Attempted calculation but incorrect approach
- 0 points: Correct answer with no work or no attempt or completely wrong

---

**Component 3: Part (b) Standard Error Calculation (6 points)**

Given: s1 = 15.40, s2 = 14.80, n1 = 20, n2 = 23

**CORRECT ANSWER:**
SE = sqrt((15.40²/20) + (14.80²/23))
SE = sqrt((237.16/20) + (219.04/23))
SE = sqrt(11.858 + 9.524)
SE = sqrt(21.382)
SE ≈ 4.62

**EVALUATION STEPS:**

STEP 1: Is the formula shown and applied correctly? (2 points)
- Full credit: Correct formula application with correct values
- None: Incorrect formula or wrong values substituted

STEP 2: Are calculations shown and correct? (2 points)
- Full credit (2 pts): All intermediate steps shown correctly
- Partial (1 pt): Some steps shown but with minor errors
- None (0 pts): No work shown or major computational errors

STEP 3: Is the final answer correct? (2 points)
- Full credit: SE ≈ 4.62 (accept 4.6, 4.62, 4.624)
- Partial: Close answer due to rounding (4.5-4.7)
- None: Incorrect answer

**Scoring:**
- 6 points: Formula shown, all work correct, correct answer
- 4 points: Formula shown, minor computational error, close answer
- 3 points: Formula shown, major computational error 
- 1 point: Attempted calculation but incorrect approach
- 0 points: Correct answer with no work or no attempt or completely wrong

---

**Component 4: Part (c) Standard Error Calculation (6 points)**

Given: s1 = 12, s2 = 10, n1 = 25, n2 = 25

**CORRECT ANSWER:**
SE = sqrt((12²/25) + (10²/25))
SE = sqrt((144/25) + (100/25))
SE = sqrt(5.76 + 4)
SE = sqrt(9.76)
SE ≈ 3.12

**EVALUATION STEPS:**

STEP 1: Is the formula applied correctly? (2 points)
- Full credit: Correct formula application with correct values
- None: Incorrect formula or wrong values substituted

STEP 2: Are calculations shown and correct? (2 points)
- Full credit (2 pts): All intermediate steps shown correctly
- Partial (1 pt): Some steps shown but with minor errors
- None (0 pts): No work shown or major computational errors

STEP 3: Is the final answer correct? (2 points)
- Full credit: SE ≈ 3.12 (accept 3.1, 3.12, 3.124)
- Partial: Close answer due to rounding (3.0-3.2)
- None: Incorrect answer

**Scoring:**
- 6 points: Formula shown, all work correct, correct answer
- 4 points: Formula shown, minor computational error, close answer
- 3 points: Formula shown, major computational error 
- 1 point: Attempted calculation but incorrect approach
- 0 points: Correct answer with no work or no attempt or completely wrong

---

**COMMON MISTAKES TO WATCH FOR:**

1. **Wrong formula**: Using SE = s/sqrt(n) instead of pooled formula
2. **Forgetting to square**: Using s1/n1 instead of s1²/n1
3. **Forgetting square root**: Calculating variance instead of SE
4. **Calculation errors**: Simple arithmetic mistakes in intermediate steps
5. **Rounding too early**: Leading to slightly incorrect final answers
6. **No work shown**: Just providing final answers without calculations

---

**FEEDBACK EXAMPLES FOR 1-POINT ANSWERS:**

If student uses wrong formula:
- "Credit for effort, but the formula used is incorrect. Standard error for two groups requires: SE = sqrt((s1²/n1) + (s2²/n2))."

If student forgets to show work:
- "You need to show your calculations step-by-step. Just providing answers isn't sufficient."

If student makes consistent computational errors:
- "Good attempt at applying the formula, but check your arithmetic carefully in the intermediate steps."

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

For component_1_title_score: use paper_title_present (1 if True, 0 if False)
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
  "component_2_explanation": "<brief explanation for Part (a)>",
  "component_3_score": <0-6>,
  "component_3_explanation": "<brief explanation for Part (b)>",
  "component_4_score": <0-6>,
  "component_4_explanation": "<brief explanation for Part (c)>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of standard error calculations>"
}}"""

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
        print("GRADING RESULTS - HW9_2")
        print("Standard Error Calculation")
        print("=" * 60)

        if 'component_1_score' in grading:
            # Originality check result
            if grading.get("originality_concern"):
                print("\n⚠️  ORIGINALITY CONCERN DETECTED")
                print("   All points frozen. See feedback below.")

            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Header): {grading.get('component_1_score', 'N/A')}/2")
            print(f"    • Task description:    {grading.get('component_1_task_score', 'N/A')}/1 (regex)")
            print(f"    • No autoformatting:   {grading.get('component_1_autoformat_score', 'N/A')}/1 (regex)")
            if grading.get('component_1_explanation'):
                print(f"   → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Part a): {grading.get('component_2_score', 'N/A')}/6")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Part b): {grading.get('component_3_score', 'N/A')}/6")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Part c): {grading.get('component_4_score', 'N/A')}/6")
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

    # Initialize evaluator
    evaluator = HW9_2Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("QUESTION 9.2 EVALUATOR")
    print("Standard Error Calculation")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION 9_2.")
    print("(Press Enter twice when finished, or type 'END' on a new line)\n")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        lines.append(line)
        # Check if last two lines are empty (double Enter)
        if len(lines) >= 2 and lines[-1] == '' and lines[-2] == '':
            lines = lines[:-2]  # Remove the two empty lines
            break

    student_answer = '\n'.join(lines)

    # Validate input
    if not student_answer.strip():
        print("\n❌ Error: No answer provided. Exiting.")
        exit(1)

    print("\n" + "=" * 60)
    print("EVALUATING...")
    print("=" * 60)

    # Grade with Groq API
    grading = evaluator.grade_hw9_2_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)
