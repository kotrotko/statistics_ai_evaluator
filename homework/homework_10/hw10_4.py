"""
hw10_4.py
One-Way ANOVA - Extroversion Across Majors
Evaluation method name: def grade_hw10_4_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW10_4Evaluator(BaseEvaluator):
    """
    Evaluator for One-Way ANOVA: Extroversion Across Majors (HW10_4).

    Task: Administrators at a university want to know if students in different majors
    are more or less extroverted than others. They provide you with data they have for
    English majors (X= 3.78, n = 45), History majors (X= 2.23, n =40), Psychology majors
    (X = 4.41, n = 51), and Math majors (X= 1.15, n =28). You find the SSB = 75.80 and
    SSW = 47.40 and test at α = 0.05.

    Evaluates student's ability to conduct ANOVA hypothesis testing.

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
        task_patterns = [
            r'english.*3\.78',
            r'history.*2\.23',
            r'psychology.*4\.41',
            r'math.*1\.15',
            r'ssb\s*=\s*75\.80',
            r'ssw\s*=\s*47\.40',
            r'extrovert'
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

    def grade_hw10_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 10_4: ANOVA hypothesis testing for extroversion across majors.
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
                    "component_2_score": 5,
                    "component_3_score": 6,
                    "component_4_score": 7,
                },
                max_points=20,
                feedback="[TEST MODE] All formatting elements present. ANOVA calculations correct with strong hypothesis testing.",
                vibe="Student demonstrates solid understanding of ANOVA with minor issues.",
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
"Administrators at a university want to know if students in different majors are more or less extroverted than others. They provide you with data they have for English majors (X= 3.78, n = 45), History majors (X= 2.23, n =40), Psychology majors (X = 4.41, n = 51), and Math majors (X= 1.15, n =28). You find the SSB = 75.80 and SSW = 47.40 and test at α = 0.05."

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

**Component 2: ANOVA Calculations (6 points)**

The student must calculate df, MS, and F-statistic.

**GIVEN DATA:**
- k = 4 majors (English, History, Psychology, Math)
- Sample sizes: n1=45, n2=40, n3=51, n4=28
- N total = 45 + 40 + 51 + 28 = 164
- Means: X̄₁=3.78, X̄₂=2.23, X̄₃=4.41, X̄₄=1.15
- SSB = 75.80
- SSW = 47.40
- α = 0.05

**CORRECT CALCULATIONS:**

1. df_between = k - 1 = 4 - 1 = 3
2. df_within = N - k = 164 - 4 = 160
3. df_total = N - 1 = 164 - 1 = 163
4. MSB = SSB / df_between = 75.80 / 3 = 25.267 (or 25.27)
5. MSW = SSW / df_within = 47.40 / 160 = 0.296 (or 0.2963)
6. F = MSB / MSW = 25.267 / 0.296 = 85.36 (accept 85.0-86.0)

**EVALUATION STEPS:**

STEP 1: Are degrees of freedom correct? (1.5 points)
- Full credit: df_between = 3 AND df_within = 160
- Partial (1 pt): One correct, one incorrect
- Partial (0.5 pt): Both attempted but with errors
- None: Missing or completely wrong

STEP 2: Are Mean Squares calculated correctly? (2.5 points)
- Full credit (2.5 pts): MSB ≈ 25.27 AND MSW ≈ 0.296
- Partial (2 pts): Both calculated but with minor rounding differences
- Partial (1.5 pts): One correct, one incorrect
- Partial (1 pt): Both attempted but with calculation errors
- Partial (0.5 pt): Minimal attempt
- None: Missing or completely wrong

STEP 3: Is F-statistic calculated correctly? (2 points)
- Full credit (2 pts): F ≈ 85.36 (accept 85.0-86.0)
- Partial (1.5 pts): Close value due to rounding (83-87)
- Partial (1 pt): Calculation attempted but with error
- Partial (0.5 pt): Minimal attempt
- None: Missing or completely wrong

**Scoring Guide:**
- 6 points: All calculations correct
- 5 points: All major values correct with minor rounding differences
- 4 points: Most calculations correct but one component with errors
- 3 points: Several values correct but major errors present
- 2 points: Attempted calculations but multiple errors
- 1 point: Minimal attempt with mostly incorrect values
- 0 points: No calculations or completely wrong

---

**Component 3: 4-Step Hypothesis Testing - Steps 1 & 2 (6 points)**

The student must state hypotheses and set up the test parameters.

**STEP 1: State the Hypotheses (3 points)**

Null Hypothesis (H0):
- μ₁ = μ₂ = μ₃ = μ₄ (all population means are equal)
- OR: There is no difference in mean extroversion across majors
- OR: Major has no effect on extroversion

Alternative Hypothesis (H1 or Ha):
- At least one μᵢ differs from the others
- OR: Not all population means are equal
- OR: There is a difference in mean extroversion across majors

**Evaluation for Step 1:**
- 3 points: Both hypotheses correctly stated in proper format
- 2 points: Hypotheses stated but with minor notation issues
- 1 point: Hypotheses attempted but unclear or incomplete
- 0 points: Hypotheses missing or completely wrong

**STEP 2: Set the Significance Level and Find Critical Value (3 points)**

Significance Level:
- α = 0.05 (given in problem)

Degrees of Freedom:
- df1 = 3 (between groups)
- df2 = 160 (within groups)

Critical Value:
- F_critical(3, 160, α=0.05) ≈ 2.66 (accept 2.65-2.67)

**Evaluation for Step 2:**
- 3 points: α stated, df correct, critical value correct (≈ 2.66)
- 2 points: α and df correct, critical value missing or slightly off
- 1 point: Some elements present but incomplete
- 0 points: Step missing or completely wrong

**Scoring Guide for Component 3:**
- 6 points: Hypotheses clear and correct, α/df/critical value all correct
- 5 points: Hypotheses correct, minor issue with critical value
- 4 points: Hypotheses correct, missing or incorrect critical value
- 3 points: Hypotheses attempted, test setup incomplete
- 2 points: Major issues but shows understanding of hypothesis testing
- 1 point: Minimal attempt
- 0 points: Missing or completely wrong

---

**Component 4: 4-Step Hypothesis Testing - Steps 3 & 4 (6 points)**

The student must make a decision and interpret the results.

**STEP 3: Calculate the Test Statistic (2 points)**

Test Statistic:
- F = MSB / MSW = 25.267 / 0.296 = 85.36

This should already be calculated in Component 2.

**Evaluation for Step 3:**
- 2 points: F ≈ 85.36 stated as test statistic
- 1 point: F stated but with calculation error
- 0 points: Test statistic missing or wrong

**STEP 4: Make a Decision and Interpret (4 points)**

Decision:
- Since F = 85.36 > F_critical = 2.66, we REJECT the null hypothesis
- OR: p-value < 0.05, reject H0

Interpretation:
- There is a statistically significant difference in mean extroversion across the four majors
- At least one major has significantly different extroversion from the others
- The data provide sufficient evidence that not all majors have the same mean extroversion

**Evaluation for Step 4:**

Decision (2 points):
- 2 points: Clear "reject H0" with correct reasoning (F > F_crit or p < α)
- 1 point: Correct decision but weak or unclear reasoning
- 0 points: Wrong decision or no decision

Interpretation (2 points):
- 2 points: Clear interpretation in context (mentions majors, extroversion, significant difference)
- 1 point: Interpretation attempted but lacks context or clarity
- 0 points: No interpretation or completely incorrect

**Scoring Guide for Component 4:**
- 6 points: Test statistic correct, decision correct with reasoning, clear interpretation
- 5 points: All correct but interpretation could be clearer
- 4 points: Decision correct, interpretation weak or missing
- 3 points: Some components correct
- 2 points: Major errors but shows understanding
- 1 point: Minimal attempt
- 0 points: Missing or completely wrong

---

**COMMON MISTAKES TO WATCH FOR:**

1. **N calculation**: Forgetting to sum all sample sizes (164 total)
2. **Degrees of freedom**: Using wrong formulas (n-1 instead of k-1, etc.)
3. **MSW calculation**: Dividing by wrong df value
4. **F-statistic**: Not dividing MSB by MSW or dividing backwards
5. **Hypothesis format**: Not stating "at least one mean differs" for Ha
6. **Critical value**: Using wrong df or wrong α level
7. **Decision**: Failing to reject when F is huge (85.36 >> 2.66)
8. **Interpretation**: Not relating results back to majors and extroversion

---

**FEEDBACK EXAMPLES:**

For df calculation errors:
- "Good start, but remember N = 45+40+51+28 = 164, so df_within = N - k = 160."

For wrong hypothesis format:
- "Your alternative hypothesis should state that 'at least one mean differs,' not that 'all means are different.'"

For correct calculation but wrong decision:
- "Your F-statistic is correct, but check your comparison: F = 85.36 is much larger than F_crit = 2.66, so you should reject H0."

For missing interpretation:
- "You made the correct decision, but you need to interpret what this means in the context of majors and extroversion."

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
  "component_2_explanation": "<brief explanation for ANOVA calculations>",
  "component_3_score": <0-6>,
  "component_3_explanation": "<brief explanation for Steps 1 & 2 of hypothesis testing>",
  "component_4_score": <0-6>,
  "component_4_explanation": "<brief explanation for Steps 3 & 4 of hypothesis testing>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of ANOVA>"
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
        print("GRADING RESULTS - HW10_4")
        print("ANOVA: Extroversion Across Majors")
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

            print(f"  Component 2 (ANOVA Calculations): {grading.get('component_2_score', 'N/A')}/6")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Hypotheses & Test Setup): {grading.get('component_3_score', 'N/A')}/6")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Test Statistic & Decision): {grading.get('component_4_score', 'N/A')}/6")
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
    evaluator = HW10_4Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("HOMEWORK 10.4 EVALUATOR")
    print("ANOVA: Extroversion Across Majors")
    print("=" * 60)
    print("\nPlease enter the student's answer to HOMEWORK 10_4.")
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
    grading = evaluator.grade_hw10_4_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)
