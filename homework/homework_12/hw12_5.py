"""
hw12_5.py
Correlational Analysis - Hypothesis Testing for Significant Relation
Evaluation method name: def grade_hw12_5_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW12_5Evaluator(BaseEvaluator):
    """
    Evaluator for Correlation Hypothesis Testing (HW12_5).

    Task: A researcher collects data from 100 people to assess whether there is
    any relation between level of education and levels of civic engagement.
    The researcher finds the following descriptive values: X= 4.02, sx = 1.15,
    Y= 15.92, sy = 5.01, SSX = 130.93, SSY = 2484.91, SP = 159.39.
    Test for a significant relation using the four step hypothesis testing procedure.

    Evaluates student's ability to calculate Pearson's r and conduct
    four-step hypothesis testing for a significant correlation.

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
        # Only exact lowercase substrings from the task that a student
        # would never write as part of their own answer
        pedagogical_markers = [
            "level of education and levels of civic engagement",
            "test for a significant relation using the four step",
            "four step hypothesis testing procedure",
        ]
        if any(marker in text_lower for marker in pedagogical_markers):
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

    def grade_hw12_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 12_5: Four-step hypothesis testing for significant correlation.
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
                feedback="[TEST MODE] All formatting elements present. Correct r calculation and hypothesis testing.",
                vibe="Student demonstrates solid understanding of correlation hypothesis testing.",
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
"A researcher collects data from 100 people to assess whether there is any relation between level of education and levels of civic engagement. The researcher finds the following descriptive values: X= 4.02, sx = 1.15, Y= 15.92, sy = 5.01, SSX = 130.93, SSY = 2484.91, SP = 159.39. Test for a significant relation using the four step hypothesis testing procedure."

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

**CORRECT CALCULATIONS:**

r = SP / sqrt(SSX * SSY)
r = 159.39 / sqrt(130.93 * 2484.91)
r = 159.39 / sqrt(324,899.63)
r = 159.39 / 570.00
r = 0.2796 (accept 0.27 to 0.28)

t = r * sqrt(n - 2) / sqrt(1 - r²)
df = n - 2 = 100 - 2 = 98
r² = 0.0782
t = 0.2796 * sqrt(98) / sqrt(1 - 0.0782)
t = 0.2796 * 9.899 / sqrt(0.9218)
t = 0.2796 * 9.899 / 0.9601
t = 2.769 / 0.9601
t ≈ 2.884 (accept 2.80 to 2.90)

Critical value: t_crit(98, α=0.05, two-tailed) ≈ 1.984 (accept 1.98 to 1.99)
Decision: Since t ≈ 2.884 > t_crit ≈ 1.984, REJECT H0.

---

**Component 2: r Calculation and Step 1 — Hypotheses (6 points)**

STEP 1: Pearson's r calculation (3 points)
- Full credit (3 pts): r = SP / sqrt(SSX * SSY) with correct result ≈ 0.28
- Partial (2 pts): Correct formula but minor arithmetic error, result in range 0.24–0.32
- Partial (1 pt): Formula attempted but with major error or wrong formula
- None (0 pts): No calculation or completely wrong

STEP 2: Hypotheses stated (3 points)
- Full credit (3 pts): H0: ρ = 0 (no correlation) AND H1: ρ ≠ 0 (significant correlation), both clearly stated
- Partial (2 pts): Both hypotheses present but with minor notation issues
- Partial (1 pt): One hypothesis stated or both vague
- None (0 pts): Hypotheses missing or completely wrong

**KEY CONCEPTS TO LOOK FOR:**
✓ Formula r = SP / sqrt(SSX * SSY)
✓ Correct substitution of values
✓ Result approximately 0.28
✓ H0 states no correlation (ρ = 0)
✓ H1 states significant correlation (ρ ≠ 0)

**COMMON MISTAKES:**
❌ Using wrong formula for r (e.g., dividing SP by SSX only)
❌ Not showing substitution of given values
❌ Stating H1 as one-tailed without justification
❌ Using r instead of ρ in hypotheses

**Scoring Guide:**
- 6 points: r correct, both hypotheses correctly stated
- 5 points: r correct, minor hypothesis notation issue
- 4 points: r correct, hypotheses incomplete
- 3 points: r has minor error, hypotheses correct
- 2 points: r has major error or hypotheses missing
- 1 point: Minimal attempt
- 0 points: Blank or completely wrong

---

**Component 3: Step 2 — Significance Level, df, and Critical Value (6 points)**

STEP 1: Significance level (2 points)
- Full credit (2 pts): α = 0.05 stated (standard if not specified)
- Partial (1 pt): α mentioned but not clearly stated
- None (0 pts): Missing

STEP 2: Degrees of freedom (2 points)
- Full credit (2 pts): df = n - 2 = 100 - 2 = 98
- Partial (1 pt): Formula correct but arithmetic error
- None (0 pts): Missing or wrong formula

STEP 3: Critical value (2 points)
- Full credit (2 pts): t_crit(98) ≈ 1.984 (accept 1.98 to 1.99)
- Partial (1 pt): Critical value present but slightly off due to df rounding or table reading
- None (0 pts): Missing or completely wrong

**KEY CONCEPTS TO LOOK FOR:**
✓ α = 0.05 stated
✓ df = n - 2 = 98
✓ t_crit ≈ 1.984

**COMMON MISTAKES:**
❌ Using df = n - 1 instead of n - 2
❌ Using z-critical instead of t-critical
❌ Using one-tailed critical value without justification

**Scoring Guide:**
- 6 points: α, df, and critical value all correct
- 5 points: All correct with minor rounding on critical value
- 4 points: α and df correct, critical value missing or off
- 3 points: Two out of three elements correct
- 2 points: One element correct
- 1 point: Minimal attempt
- 0 points: Missing or completely wrong

---

**Component 4: Steps 3 & 4 — Test Statistic, Decision, and Interpretation (6 points)**

STEP 3: t-statistic calculation (2 points)
- Full credit (2 pts): t ≈ 2.884 (accept 2.80 to 2.90), formula shown
- Partial (1 pt): Correct formula but arithmetic error, or correct value without formula
- None (0 pts): Missing or completely wrong

STEP 4: Decision and interpretation (4 points)

Decision (2 points):
- 2 points: Clear "reject H0" with correct reasoning (t > t_crit or p < α)
- 1 point: Correct decision but weak or unclear reasoning
- 0 points: Wrong decision or no decision

Interpretation (2 points):
- 2 points: Clear interpretation in context (mentions education, civic engagement, significant relation)
- 1 point: Interpretation attempted but lacks context or clarity
- 0 points: No interpretation or completely incorrect

**KEY CONCEPTS TO LOOK FOR:**
✓ t = r * sqrt(n-2) / sqrt(1 - r²)
✓ t ≈ 2.884
✓ t > t_crit → reject H0
✓ Conclusion mentions education and civic engagement

**COMMON MISTAKES:**
❌ Not showing the t formula
❌ Failing to reject when t = 2.884 > t_crit = 1.984
❌ Not interpreting results in context of education and civic engagement
❌ Saying "accept H0" instead of "fail to reject H0"

**Scoring Guide for Component 4:**
- 6 points: t correct, decision correct with reasoning, clear contextual interpretation
- 5 points: All correct but interpretation could be clearer
- 4 points: Decision correct, interpretation weak or missing
- 3 points: Some components correct
- 2 points: Major errors but shows understanding
- 1 point: Minimal attempt
- 0 points: Missing or completely wrong

---

**FEEDBACK EXAMPLES:**

For wrong r formula:
- "The formula for r is SP / sqrt(SSX * SSY). Check your substitution of the given values."

For wrong df:
- "For correlation, df = n - 2 = 98, not n - 1."

For correct t but wrong decision:
- "t = 2.884 exceeds t_crit = 1.984, so you should reject H0, not fail to reject."

For missing interpretation:
- "You made the correct decision, but you need to state what this means for the relation between education and civic engagement."

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
  "component_2_explanation": "<brief explanation for r calculation and hypotheses>",
  "component_3_score": <0-6>,
  "component_3_explanation": "<brief explanation for significance level, df, and critical value>",
  "component_4_score": <0-6>,
  "component_4_explanation": "<brief explanation for test statistic, decision, and interpretation>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of correlation hypothesis testing>"
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
        print("GRADING RESULTS - HW12_5")
        print("Correlation Hypothesis Testing")
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

            print(f"  Component 2 (r Calculation and Hypotheses): {grading.get('component_2_score', 'N/A')}/6")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Significance Level, df, Critical Value): {grading.get('component_3_score', 'N/A')}/6")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Test Statistic, Decision, Interpretation): {grading.get('component_4_score', 'N/A')}/6")
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
    evaluator = HW12_5Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("HOMEWORK 12.5 EVALUATOR")
    print("Correlation Hypothesis Testing")
    print("=" * 60)
    print("\nPlease enter the student's answer to HOMEWORK 12_5.")
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
    grading = evaluator.grade_hw12_5_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)
