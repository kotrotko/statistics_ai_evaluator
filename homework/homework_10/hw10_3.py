"""
hw10_3.py
One-Way ANOVA - Complete Table and Hypothesis Testing
Evaluation method name: def grade_hw10_3_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW10_3Evaluator(BaseEvaluator):
    """
    Evaluator for One-Way ANOVA Table Completion and Hypothesis Testing (HW10_3).

    Task: You know that stores tend to charge different prices for similar or identical
    products, and you want to test whether or not these differences are, on
    average, statistically significantly different. You go online and collect data
    from 3 different stores, gathering information on 15 products at each store.
    You find that the average prices at each store are: Store 1 xbar = $27.82,
    Store 2 xbar = $38.96, and Store 3 xbar = $24.53. Based on the overall
    variability in the products and the variability within each store, you find the
    following values for the Sums of Squares: SST = 683.22, SSW = 441.19.
    Complete the ANOVA table and use the 4 step hypothesis testing procedure
    to see if there are systematic price differences between the stores.

    Evaluates student's ability to complete ANOVA table and conduct hypothesis testing.

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
            r'3\s+different\s+stores',
            r'15\s+products\s+at\s+each\s+store',
            r'sst\s*=\s*683\.22',
            r'ssw\s*=\s*441\.19',
            r'store\s+1.*27\.82',
            r'store\s+2.*38\.96',
            r'store\s+3.*24\.53'
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

    def grade_hw10_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 10_3: ANOVA table completion and 4-step hypothesis testing.
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
                feedback="[TEST MODE] All formatting elements present. ANOVA table mostly correct with strong hypothesis testing.",
                vibe="Student demonstrates solid understanding of ANOVA with minor computational issues.",
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
"You know that stores tend to charge different prices for similar or identical products, and you want to test whether or not these differences are, on average, statistically significantly different. You go online and collect data from 3 different stores, gathering information on 15 products at each store. You find that the average prices at each store are: Store 1 xbar = $27.82, Store 2 xbar = $38.96, and Store 3 xbar = $24.53. Based on the overall variability in the products and the variability within each store, you find the following values for the Sums of Squares: SST = 683.22, SSW = 441.19. Complete the ANOVA table and use the 4 step hypothesis testing procedure to see if there are systematic price differences between the stores."

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

**Component 2: ANOVA Table Completion (6 points)**

The student must complete the ANOVA table with correct calculations.

**GIVEN DATA:**
- k = 3 stores
- n per group = 15 products
- N total = 45 products
- Store means: $27.82, $38.96, $24.53
- SST = 683.22
- SSW = 441.19

**CORRECT ANOVA TABLE:**

Source      SS      df    MS       F
Between    242.03   2    121.015  11.52
Within     441.19   42   10.505
Total      683.22   44

**CALCULATIONS:**
1. SSB = SST - SSW = 683.22 - 441.19 = 242.03
2. df_between = k - 1 = 3 - 1 = 2
3. df_within = N - k = 45 - 3 = 42
4. df_total = N - 1 = 45 - 1 = 44
5. MSB = SSB / df_between = 242.03 / 2 = 121.015 (or 121.02)
6. MSW = SSW / df_within = 441.19 / 42 = 10.505 (or 10.51)
7. F = MSB / MSW = 121.015 / 10.505 = 11.52 (accept 11.5-11.6)

**EVALUATION STEPS:**

STEP 1: Is SSB calculated correctly? (1 point)
- Full credit: SSB = 242.03
- Accept: 242.0, 242
- None: Incorrect or missing

STEP 2: Are degrees of freedom correct? (1 point)
- Full credit: df_between = 2, df_within = 42, df_total = 44
- Partial (0.5 pt): 2 out of 3 correct
- None: Less than 2 correct or missing

STEP 3: Are Mean Squares calculated correctly? (2 points)
- Full credit (2 pts): MSB ≈ 121.02 AND MSW ≈ 10.51
- Partial (1.5 pts): Both calculated but minor rounding differences
- Partial (1 pt): One correct, one incorrect
- Partial (0.5 pt): Both attempted but with calculation errors
- None: Missing or completely wrong

STEP 4: Is F-statistic calculated correctly? (1 point)
- Full credit: F ≈ 11.52 (accept 11.5-11.6)
- Partial: Close value due to rounding (11.0-12.0)
- None: Incorrect or missing

STEP 5: Is the table properly formatted? (1 point)
- Full credit: Table with proper labels (Source, SS, df, MS, F)
- Partial: Table present but missing some labels
- None: No table or extremely poor formatting

**Scoring Guide:**
- 6 points: Complete table, all calculations correct, proper formatting
- 5 points: All major values correct with minor rounding differences
- 4 points: Most calculations correct but missing one component
- 3 points: Several values correct but major errors present
- 2 points: Attempted table but multiple calculation errors
- 1 point: Minimal attempt with mostly incorrect values
- 0 points: No table or completely wrong

---

**Component 3: 4-Step Hypothesis Testing - Steps 1 & 2 (6 points)**

The student must state hypotheses and set up the test parameters.

**STEP 1: State the Hypotheses (3 points)**

Null Hypothesis (H0):
- μ1 = μ2 = μ3 (all population means are equal)
- OR: There is no difference in mean prices across the three stores
- OR: The store has no effect on mean prices

Alternative Hypothesis (H1 or Ha):
- At least one μi differs from the others
- OR: Not all population means are equal
- OR: There is a difference in mean prices across stores

**Evaluation for Step 1:**
- 3 points: Both hypotheses correctly stated in proper format
- 2 points: Hypotheses stated but with minor notation issues
- 1 point: Hypotheses attempted but unclear or incomplete
- 0 points: Hypotheses missing or completely wrong

**STEP 2: Set the Significance Level and Find Critical Value (3 points)**

Significance Level:
- α = 0.05 (standard if not specified, though student should state it)

Degrees of Freedom:
- df1 = 2 (between groups)
- df2 = 42 (within groups)

Critical Value:
- F_critical(2, 42, α=0.05) ≈ 3.22

**Evaluation for Step 2:**
- 3 points: α stated, df correct, critical value correct (≈ 3.22)
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

The student must calculate the test statistic and make a decision.

**STEP 3: Calculate the Test Statistic (2 points)**

Test Statistic:
- F = MSB / MSW = 121.015 / 10.505 = 11.52

This should already be in the ANOVA table from Component 2.

**Evaluation for Step 3:**
- 2 points: F = 11.52 stated as test statistic
- 1 point: F stated but with calculation error
- 0 points: Test statistic missing or wrong

**STEP 4: Make a Decision and Interpret (4 points)**

Decision:
- Since F = 11.52 > F_critical = 3.22, we REJECT the null hypothesis
- OR: p-value < 0.05, reject H0

Interpretation:
- There is a statistically significant difference in mean prices across the three stores
- At least one store has significantly different prices from the others
- The data provide sufficient evidence that not all stores charge the same average prices

**Evaluation for Step 4:**

Decision (2 points):
- 2 points: Clear "reject H0" with correct reasoning (F > F_crit or p < α)
- 1 point: Correct decision but weak or unclear reasoning
- 0 points: Wrong decision or no decision

Interpretation (2 points):
- 2 points: Clear interpretation in context (mentions stores, prices, significant difference)
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

1. **SSB calculation**: Forgetting SSB = SST - SSW
2. **Degrees of freedom**: Using wrong formulas (n-1 instead of k-1, etc.)
3. **Mean Squares**: Dividing by wrong df values
4. **F-statistic**: Not dividing MSB by MSW
5. **Hypothesis format**: Not stating "at least one mean differs" for Ha
6. **Critical value**: Using wrong df or wrong α level
7. **Decision**: Failing to reject when should reject (or vice versa)
8. **Interpretation**: Not relating results back to stores and prices

---

**FEEDBACK EXAMPLES:**

For incomplete ANOVA table:
- "Good start on the table, but you need to calculate SSB = SST - SSW first, then proceed with MS and F."

For wrong hypothesis format:
- "Your alternative hypothesis should state that 'at least one mean differs,' not that 'all means are different.'"

For correct calculation but wrong decision:
- "Your F-statistic is correct, but check your comparison: F = 11.52 is much larger than F_crit = 3.22, so you should reject H0."

For missing interpretation:
- "You made the correct decision, but you need to interpret what this means in the context of the store prices."

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
  "component_2_explanation": "<brief explanation for ANOVA table completion>",
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
        print("GRADING RESULTS - HW10_3")
        print("ANOVA Table Completion and Hypothesis Testing")
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

            print(f"  Component 2 (ANOVA Table Completion): {grading.get('component_2_score', 'N/A')}/6")
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
    evaluator = HW10_3Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("HOMEWORK 10.3 EVALUATOR")
    print("ANOVA Table Completion and Hypothesis Testing")
    print("=" * 60)
    print("\nPlease enter the student's answer to HOMEWORK 10_3.")
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
    grading = evaluator.grade_hw10_3_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)
