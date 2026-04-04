"""
hw12_3.py
Correlational Analysis - Direction and Magnitude of Correlation Coefficients
Evaluation method name: def grade_hw12_3_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW12_3Evaluator(BaseEvaluator):
    """
    Evaluator for Correlation Coefficient Direction and Magnitude (HW12_3).

    Task: What is the direction and magnitude of the following correlation coefficients?
    a. -0.81
    b. 0.40
    c. 0.15
    d. -0.08
    e. 0.29

    Evaluates student's ability to correctly identify direction and magnitude
    for five given correlation coefficients.

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

        # Task description (strict)
        # Only phrases a student would NOT write as part of their answer
        task_patterns = [
            r'direction\s+and\s+magnitude\s+of\s+the\s+following',
            r'what\s+is\s+the\s+direction\s+and\s+magnitude',
            r'-0\.81.*0\.40.*0\.15',
            r'0\.40.*0\.15.*-0\.08',
        ]
        if any(re.search(pattern, text_lower) for pattern in task_patterns):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # No autoformatting (strict)
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

    def grade_hw12_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 12_3: Direction and magnitude of five correlation coefficients.
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
                feedback="[TEST MODE] All formatting elements present. Correct direction and magnitude for all coefficients.",
                vibe="Student demonstrates solid understanding of correlation coefficient interpretation.",
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
        You are grading a statistics assignment where a student must answer:
"What is the direction and magnitude of the following correlation coefficients?
a. -0.81
b. 0.40
c. 0.15
d. -0.08
e. 0.29"

Use a **STRICT rubric-based approach**. Total score MUST be exactly 20 points.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. 0 only if completely blank
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. For low-scoring answers, use encouraging language: "Credit for trying, but..."

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

**CORRECT ANSWERS:**

Use the following classification guidelines for magnitude:
- 0.00 to 0.10: negligible
- 0.10 to 0.29: weak (small)
- 0.30 to 0.49: moderate
- 0.50 to 0.69: strong (large)  — accept also "moderate to strong"
- 0.70 to 1.00: very strong

Direction: negative if r < 0, positive if r > 0.

a. r = -0.81 → negative direction, very strong magnitude
b. r = 0.40  → positive direction, moderate magnitude
c. r = 0.15  → positive direction, weak (small) magnitude
d. r = -0.08 → negative direction, negligible magnitude
e. r = 0.29  → positive direction, weak (small) magnitude

Accept reasonable label variants: "strong" for "very strong" on -0.81 if justified;
"small" for "weak"; "low" for "negligible". Do NOT accept wrong direction under any circumstances.

---

**Component 2: Coefficients a and b (6 points)**

COEFFICIENT a: r = -0.81 (3 points)
- Direction (1.5 pts): negative — STRICT, no partial credit for wrong direction
- Magnitude (1.5 pts): very strong (accept "strong")

COEFFICIENT b: r = 0.40 (3 points)
- Direction (1.5 pts): positive — STRICT, no partial credit for wrong direction
- Magnitude (1.5 pts): moderate

**Scoring Guide:**
- 6 points: Both direction and magnitude correct for both coefficients
- 5 points: Three out of four elements correct
- 4 points: Two out of four elements correct
- 2-3 points: One coefficient fully correct or partial credit across both
- 1 point: Minimal correct elements
- 0 points: Blank or completely wrong

---

**Component 3: Coefficients c and d (6 points)**

COEFFICIENT c: r = 0.15 (3 points)
- Direction (1.5 pts): positive — STRICT, no partial credit for wrong direction
- Magnitude (1.5 pts): weak (accept "small")

COEFFICIENT d: r = -0.08 (3 points)
- Direction (1.5 pts): negative — STRICT, no partial credit for wrong direction
- Magnitude (1.5 pts): negligible (accept "very weak", "near zero")

**Scoring Guide:**
- 6 points: Both direction and magnitude correct for both coefficients
- 5 points: Three out of four elements correct
- 4 points: Two out of four elements correct
- 2-3 points: One coefficient fully correct or partial credit across both
- 1 point: Minimal correct elements
- 0 points: Blank or completely wrong

---

**Component 4: Coefficient e and Overall Quality (6 points)**

COEFFICIENT e: r = 0.29 (3 points)
- Direction (1.5 pts): positive — STRICT, no partial credit for wrong direction
- Magnitude (1.5 pts): weak (accept "small")

OVERALL QUALITY (3 points):
- 3 points: All five coefficients addressed, consistent use of correct terminology throughout
- 2 points: All five addressed, minor terminology inconsistencies
- 1 point: Not all five addressed or major terminology problems
- 0 points: Fewer than three coefficients addressed

**Scoring Guide:**
- 6 points: Coefficient e fully correct, all five addressed with consistent terminology
- 5 points: Coefficient e correct, minor quality issue
- 4 points: Coefficient e correct, quality concerns or not all five addressed
- 2-3 points: Coefficient e partially correct or quality issues
- 1 point: Minimal attempt
- 0 points: Missing or completely wrong

---

**COMMON MISTAKES TO WATCH FOR:**

❌ Confusing direction: calling -0.81 positive or 0.40 negative
❌ Calling -0.81 "moderate" or "weak" (it is very strong)
❌ Calling 0.40 "strong" (it is moderate)
❌ Calling -0.08 "weak" rather than "negligible"
❌ Confusing 0.15 and 0.29 as moderate (both are weak)
❌ Not stating direction at all, only magnitude

---

**FEEDBACK EXAMPLES:**

For wrong direction:
- "Direction is the sign of r — negative means negative, positive means positive. Check coefficients a and d."

For wrong magnitude on -0.81:
- "r = -0.81 is very strong, not moderate. Review the magnitude classification scale."

For missing direction:
- "Credit for trying, but you need to state both direction and magnitude for each coefficient."

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
  "component_2_explanation": "<brief explanation for coefficients a and b>",
  "component_3_score": <0-6>,
  "component_3_explanation": "<brief explanation for coefficients c and d>",
  "component_4_score": <0-6>,
  "component_4_explanation": "<brief explanation for coefficient e and overall quality>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of correlation coefficient interpretation>"
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
        print("GRADING RESULTS - HW12_3")
        print("Direction and Magnitude of Correlation Coefficients")
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

            print(f"  Component 2 (Coefficients a and b): {grading.get('component_2_score', 'N/A')}/6")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Coefficients c and d): {grading.get('component_3_score', 'N/A')}/6")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Coefficient e and Overall Quality): {grading.get('component_4_score', 'N/A')}/6")
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
    evaluator = HW12_3Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("HOMEWORK 12.3 EVALUATOR")
    print("Direction and Magnitude of Correlation Coefficients")
    print("=" * 60)
    print("\nPlease enter the student's answer to HOMEWORK 12_3.")
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
    grading = evaluator.grade_hw12_3_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)

