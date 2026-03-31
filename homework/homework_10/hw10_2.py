"""
hw10_2.py
ANOVA Table Interpretation - Hypothesis Testing and Effect Size
Evaluation method name: def grade_hw10_2_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW10_2Evaluator(BaseEvaluator):
    """
    Evaluator for ANOVA Table Interpretation (HW10_2).

    Task: Based on the ANOVA table below, do you reject or fail to reject the null
    hypothesis? What is the effect size?
    Source SS df MS F
    Between 60.72 3 20.24 3.88
    Within 213.61 41 5.21
    Total 274.33 44

    Evaluates student's ability to interpret ANOVA results and calculate effect size.

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
        task_patterns = [
            r'reject\s+or\s+fail\s+to\s+reject',
            r'effect\s+size',
            r'anova\s+table',
            r'between.*60\.72',
            r'ss.*df.*ms.*f'
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

    def grade_hw10_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 10_2: ANOVA table interpretation with hypothesis testing and effect size.
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
                    "component_2_score": 9,
                    "component_3_score": 9,
                },
                max_points=20,
                feedback="[TEST MODE] All formatting elements present. Strong hypothesis testing and effect size calculation.",
                vibe="Student demonstrates solid understanding of ANOVA interpretation and effect size.",
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
        You are grading a statistics assignment where a student must:
"Based on the ANOVA table below, do you reject or fail to reject the null hypothesis? What is the effect size?

Source    SS      df    MS      F
Between   60.72   3     20.24   3.88
Within    213.61  41    5.21
Total     274.33  44"

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

**Component 2: Hypothesis Testing Decision (9 points)**

The student must determine whether to reject or fail to reject the null hypothesis based on the ANOVA table.

**GIVEN DATA FROM TABLE:**
- F-statistic: F(3, 41) = 3.88
- df between: 3
- df within: 41

**CRITICAL VALUES (α = 0.05):**
- F-critical ≈ 2.84 (for df1=3, df2=41)

**CORRECT DECISION:**
Since F = 3.88 > F-critical = 2.84, we REJECT the null hypothesis.
(If using p-value approach: p < 0.05, so reject H0)

**EVALUATION STEPS:**

STEP 1: Does the student state a clear decision? (3 points)
- Full credit (3 pts): Clearly states "reject H0" or "reject the null hypothesis"
- Partial (2 pts): States decision but with unclear language ("probably reject", "might reject")
- Partial (1 pt): Implies decision without explicit statement
- None (0 pts): No decision stated or states "fail to reject" (INCORRECT)

STEP 2: Does the student provide correct reasoning? (4 points)
- Full credit (4 pts): Compares F-statistic to critical value OR mentions p-value < α
  Examples: "F = 3.88 > F-crit", "p < 0.05", "F exceeds critical value"
- Partial (3 pts): Mentions comparison but with minor errors or incomplete reasoning
- Partial (2 pts): Vague reasoning ("F is significant") without specific comparison
- Partial (1 pt): Attempts reasoning but with major conceptual errors
- None (0 pts): No reasoning provided or completely incorrect reasoning

STEP 3: Does the student use appropriate statistical terminology? (2 points)
- Full credit (2 pts): Uses terms like "null hypothesis", "H0", "significance level", "α", "critical value"
- Partial (1 pt): Uses some appropriate terminology but mostly informal language
- None (0 pts): No statistical terminology used

**KEY CONCEPTS TO LOOK FOR:**
✓ F-statistic value (3.88) is identified
✓ Comparison to critical value OR p-value mentioned
✓ Clear "reject H0" statement
✓ Connection between comparison and decision

**COMMON MISTAKES:**
❌ Stating "fail to reject" (WRONG - F = 3.88 is significant at α = 0.05)
❌ Not comparing F to anything (no critical value or p-value mentioned)
❌ Saying "accept H0" instead of "fail to reject H0"
❌ Confusing F-statistic with p-value

**Scoring Guide:**
- 9 points: Clear "reject H0" decision, correct reasoning with F-comparison, appropriate terminology
- 7-8 points: Correct decision with mostly correct reasoning, minor gaps
- 5-6 points: Correct decision but weak or incomplete reasoning
- 3-4 points: Correct decision stated but little to no reasoning
- 1-2 points: Incorrect decision but shows some understanding of hypothesis testing
- 0 points: No decision or completely incorrect with no understanding

---

**Component 3: Effect Size Calculation (9 points)**

The student must calculate eta-squared (η²) as a measure of effect size.

**GIVEN DATA FROM TABLE:**
- SS between: 60.72
- SS total: 274.33

**CORRECT CALCULATION:**
η² = SS_between / SS_total
η² = 60.72 / 274.33
η² = 0.221 or 0.22 or 22.1% or 22%

**INTERPRETATION:**
η² = 0.22 indicates a MEDIUM/MODERATE effect size
(Using Cohen's guidelines: small = 0.01, medium = 0.06, large = 0.14)

**EVALUATION STEPS:**

STEP 1: Does the student show the correct formula? (2 points)
- Full credit (2 pts): η² = SS_between / SS_total (or equivalent notation)
- Partial (1 pt): Formula implied through correct calculation without explicit notation
- None (0 pts): Wrong formula or no formula shown

STEP 2: Does the student perform the calculation correctly? (4 points)
- Full credit (4 pts): Correct calculation with work shown, answer = 0.22 (or 0.221, 22%, 22.1%)
- Partial (3 pts): Correct approach but minor arithmetic error (answer 0.20-0.24)
- Partial (2 pts): Uses correct values but makes calculation error
- Partial (1 pt): Attempts calculation but uses wrong values or wrong approach
- None (0 pts): No calculation or completely wrong

STEP 3: Does the student interpret the effect size? (3 points)
- Full credit (3 pts): States effect size is "medium" or "moderate" and explains what this means
- Partial (2 pts): States effect size magnitude ("medium") without explanation
- Partial (1 pt): Vague interpretation ("it's a good effect") without proper terminology
- None (0 pts): No interpretation or incorrect interpretation

**KEY CONCEPTS TO LOOK FOR:**
✓ Formula η² = SS_between / SS_total
✓ Substitution: 60.72 / 274.33
✓ Correct answer: approximately 0.22 or 22%
✓ Interpretation: "medium/moderate effect size"
✓ Explanation: what the effect size value means in context

**COMMON MISTAKES:**
❌ Using wrong formula (e.g., η² = MS_between / MS_total)
❌ Division error (dividing total by between instead of between by total)
❌ Not converting to percentage when appropriate
❌ Calling 0.22 a "small" effect (it's medium by Cohen's standards)
❌ Providing η² value without any interpretation
❌ Confusing η² with R² or other effect size measures

**Scoring Guide:**
- 9 points: Correct formula, accurate calculation with work, proper medium effect interpretation
- 7-8 points: Correct approach, minor computational error, interpretation present
- 5-6 points: Correct formula, calculation attempted but with errors, weak interpretation
- 3-4 points: Partial understanding, major errors in calculation or interpretation
- 1-2 points: Attempted but fundamentally incorrect approach
- 0 points: No attempt or completely wrong

---

**FEEDBACK EXAMPLES:**

For correct hypothesis decision with weak reasoning:
- "You correctly rejected H0, but you need to explicitly compare F = 3.88 to the critical value to support your decision."

For incorrect decision:
- "Credit for trying, but F = 3.88 exceeds the critical value at α = 0.05, so we should REJECT H0, not fail to reject."

For effect size calculation errors:
- "Good attempt at calculating η², but check your arithmetic. The formula is η² = SS_between / SS_total = 60.72 / 274.33."

For missing effect size interpretation:
- "You calculated η² correctly, but you need to interpret what 0.22 means (medium effect size)."

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
  "component_2_score": <0-9>,
  "component_2_explanation": "<brief explanation for hypothesis testing decision>",
  "component_3_score": <0-9>,
  "component_3_explanation": "<brief explanation for effect size calculation>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of ANOVA interpretation>"
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
                "component_3_score"
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results."""
        print("=" * 60)
        print("GRADING RESULTS - HW10_2")
        print("ANOVA Table Interpretation")
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

            print(f"  Component 2 (Hypothesis Testing): {grading.get('component_2_score', 'N/A')}/9")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Effect Size): {grading.get('component_3_score', 'N/A')}/9")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

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
    evaluator = HW10_2Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("HOMEWORK 10.2 EVALUATOR")
    print("ANOVA Table Interpretation")
    print("=" * 60)
    print("\nPlease enter the student's answer to HOMEWORK 10_2.")
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
    grading = evaluator.grade_hw10_2_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)