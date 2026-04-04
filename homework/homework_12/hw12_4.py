"""
hw12_4.py
Correlational Analysis - Reading a Correlation Matrix
Evaluation method name: def grade_hw12_4_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW12_4Evaluator(BaseEvaluator):
    """
    Evaluator for Correlation Matrix Reading (HW12_4).

    Task: In the following correlation matrix, what is the relation (number, direction,
    and magnitude) between…
    a. Pay and Satisfaction
    b. Stress and Health

    Workplace  Pay   Satisfaction  Stress  Health
    Pay        1.00
    Satisfaction .68  1.00
    Stress     0.02  -0.23         1.00
    Health     0.05   0.15        -0.48    1.00

    Evaluates student's ability to read a correlation matrix and correctly
    identify the number, direction, and magnitude of given pairs.

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    def __init__(self):
        """Initialize the evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1200
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
            "what is the relation",
            "in the following correlation matrix",
        ]

        if any(marker in text_lower for marker in task_patterns):
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

    def grade_hw12_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 12_4: Reading direction and magnitude from a correlation matrix.
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
                feedback="[TEST MODE] All formatting elements present. Correct number, direction, and magnitude for both pairs.",
                vibe="Student demonstrates solid ability to read and interpret a correlation matrix.",
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
"In the following correlation matrix, what is the relation (number, direction, and magnitude) between…
a. Pay and Satisfaction
b. Stress and Health

Workplace    Pay    Satisfaction  Stress  Health
Pay          1.00
Satisfaction  .68   1.00
Stress       0.02  -0.23          1.00
Health       0.05   0.15         -0.48    1.00"

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
- 0.50 to 0.69: strong
- 0.70 to 1.00: very strong

a. Pay and Satisfaction: r = 0.68, positive direction, strong magnitude
b. Stress and Health: r = -0.48, negative direction, moderate magnitude

Accept reasonable label variants: "large" for "strong"; "medium" for "moderate";
"small" for "weak". Do NOT accept wrong number or wrong direction under any circumstances.

---

**Component 2: Pay and Satisfaction (6 points)**

The student must correctly identify three elements for the Pay–Satisfaction pair.

STEP 1: Correct number (2 points)
- Full credit (2 pts): r = 0.68 (accept .68)
- Partial (1 pt): Number present but incorrectly rounded or transcribed (e.g., 0.67, 0.69)
- None (0 pts): Wrong number or missing

STEP 2: Correct direction (2 points)
- Full credit (2 pts): positive — STRICT, no partial credit for wrong direction
- None (0 pts): Wrong direction or missing

STEP 3: Correct magnitude (2 points)
- Full credit (2 pts): strong (accept "large")
- Partial (1 pt): Reasonable adjacent label used (e.g., "moderate to strong")
- None (0 pts): Wrong magnitude label or missing

**Scoring Guide:**
- 6 points: Number, direction, and magnitude all correct
- 4-5 points: Two out of three elements correct
- 2-3 points: One element correct
- 1 point: Attempted but mostly incorrect
- 0 points: Blank or completely wrong

---

**Component 3: Stress and Health (6 points)**

The student must correctly identify three elements for the Stress–Health pair.

STEP 1: Correct number (2 points)
- Full credit (2 pts): r = -0.48 (accept -.48)
- Partial (1 pt): Number present but sign dropped or slightly off (e.g., 0.48, -0.47)
- None (0 pts): Wrong number or missing

STEP 2: Correct direction (2 points)
- Full credit (2 pts): negative — STRICT, no partial credit for wrong direction
- None (0 pts): Wrong direction or missing

STEP 3: Correct magnitude (2 points)
- Full credit (2 pts): moderate (accept "medium")
- Partial (1 pt): Reasonable adjacent label used (e.g., "moderate to strong")
- None (0 pts): Wrong magnitude label or missing

**Scoring Guide:**
- 6 points: Number, direction, and magnitude all correct
- 4-5 points: Two out of three elements correct
- 2-3 points: One element correct
- 1 point: Attempted but mostly incorrect
- 0 points: Blank or completely wrong

---

**Component 4: Overall Quality (6 points)**

The student must address both pairs completely and demonstrate understanding of how to read a correlation matrix.

STEP 1: Both pairs addressed (2 points)
- 2 points: Both a and b fully addressed
- 1 point: Only one pair addressed
- 0 points: Neither pair addressed

STEP 2: Correct use of all three required elements (number, direction, magnitude) for both pairs (2 points)
- 2 points: All three elements present for both pairs
- 1 point: All three elements present for one pair only
- 0 points: Missing elements across both pairs

STEP 3: Clarity and use of appropriate terminology (2 points)
- 2 points: Clear explanation using correct statistical language throughout
- 1 point: Mostly clear but with minor terminology issues
- 0 points: Unclear or no appropriate terminology

**Scoring Guide:**
- 6 points: Both pairs complete, all three elements present, clear terminology
- 5 points: Both pairs complete, minor terminology issue
- 4 points: Both pairs present, one element missing across pairs
- 3 points: One pair complete, other partially addressed
- 2 points: Major gaps but shows understanding of matrix reading
- 1 point: Minimal attempt
- 0 points: Missing or completely wrong

---

**COMMON MISTAKES TO WATCH FOR:**

❌ Reading the wrong cell from the matrix (e.g., confusing Stress–Satisfaction with Stress–Health)
❌ Dropping the negative sign for r = -0.48
❌ Calling r = 0.68 "very strong" (it is strong, not very strong)
❌ Calling r = -0.48 "strong" (it is moderate)
❌ Not stating the number, only direction and magnitude
❌ Stating direction without linking it to the sign of r

---

**FEEDBACK EXAMPLES:**

For wrong cell read:
- "Check the matrix carefully — Stress and Health intersect at r = -0.48, not the value you stated."

For dropped negative sign:
- "The correlation between Stress and Health is -0.48, not 0.48. The negative sign indicates direction."

For wrong magnitude on r = 0.68:
- "r = 0.68 falls in the strong range, not very strong. Review the magnitude classification scale."

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
  "component_2_explanation": "<brief explanation for Pay and Satisfaction>",
  "component_3_score": <0-6>,
  "component_3_explanation": "<brief explanation for Stress and Health>",
  "component_4_score": <0-6>,
  "component_4_explanation": "<brief explanation for overall quality>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's ability to read a correlation matrix>"
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
        print("GRADING RESULTS - HW12_4")
        print("Correlation Matrix: Direction and Magnitude")
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

            print(f"  Component 2 (Pay and Satisfaction): {grading.get('component_2_score', 'N/A')}/6")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Stress and Health): {grading.get('component_3_score', 'N/A')}/6")
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

    # Initialize evaluator
    evaluator = HW12_4Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("HOMEWORK 12.4 EVALUATOR")
    print("Correlation Matrix: Direction and Magnitude")
    print("=" * 60)
    print("\nPlease enter the student's answer to HOMEWORK 12_4.")
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
    grading = evaluator.grade_hw12_4_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)
