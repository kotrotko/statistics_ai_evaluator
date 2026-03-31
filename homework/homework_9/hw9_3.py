"""
hw9_3.py
Independent-Samples T-Test Calculation
Evaluation method name: def grade_hw9_3_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW9_3Evaluator(BaseEvaluator):
    """
    Evaluator for Independent-Samples T-Test: Software Program Effect (HW9_3).

    Task: A professor is interested in whether or not the type of software program used
    in a statistics lab affects how well students learn the material. The professor
    teaches the same lecture material to two classes but has one class use a
    point-and-click software program in lab and has the other class use a basic
    programming language. The professor tests for a difference between the two
    classes on their final exam scores.
    Point-and-Click Programming
    83 86
    83 79
    63 100
    77 74
    86 70
    84 67
    78 83
    61 85
    65 74
    75 86
    100 87
    60 61
    90 76
    66 100
    54

    Evaluates student's ability to conduct a complete independent-samples t-test
    with hypothesis formulation, calculations, and interpretation.

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

        # STEP 1 — Task description (strict)
        if re.search(r'point.and.click\s+programming\s*\n|teaches.*same\s+lecture\s+material\s+to\s+two\s+classes', text_lower):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # STEP 2 — No autoformatting (strict)
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

    def grade_hw9_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 9_3: Independent-samples t-test for software program effect.
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
                    "component_3_score": 5,
                    "component_4_score": 6,
                },
                max_points=20,
                feedback="[TEST MODE] All formatting elements present. T-test demonstrates understanding of hypothesis testing.",
                vibe="Student shows competence in conducting independent-samples t-test with minor issues.",
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
"A professor is interested in whether or not the type of software program used
in a statistics lab affects how well students learn the material. The professor
teaches the same lecture material to two classes but has one class use a
point-and-click software program in lab and has the other class use a basic
programming language. The professor tests for a difference between the two
classes on their final exam scores.
Point-and-Click Programming
83 86
83 79
63 100
77 74
86 70
84 67
78 83
61 85
65 74
75 86
100 87
60 61
90 76
66 100
54"

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

**Component 2: Research Framework (6 points)**

The student must correctly define the research question, specify hypotheses (including tail direction), and determine test parameters (α, df, critical value) for an independent-samples t-test, with brief justification and calculations.

**DATA CONTEXT:**
Point-and-Click: 83, 83, 63, 77, 86, 84, 78, 61, 65, 75, 100, 60, 90, 66, 54 (n=15)
Programming: 86, 79, 100, 74, 70, 67, 83, 85, 74, 86, 87, 61, 76, 100 (n=14)

**CORRECT SPECIFICATION:**

Research Question:
- Is there a difference in mean final exam scores between students using point-and-click software and those using a programming language?

Hypotheses:
H₀: μ₁ = μ₂
H₁: μ₁ ≠ μ₂
- Two-tailed test (testing for any difference)

Test Parameters:
- α = 0.05 (standard unless otherwise stated)
- df = n₁ + n₂ − 2 = 15 + 14 − 2 = 27
- Critical value: t ≈ ±2.052 (from t-table, two-tailed, α = 0.05, df = 27)

**CRITICAL INSTRUCTION FOR COMPONENT 2:**
The Research Question is MANDATORY. If the student does not provide a clearly formulated research question (as described in STEP 1 criteria), you MUST deduct the full 2 points for STEP 1, regardless of how well they did on hypotheses and parameters.

**EVALUATION STEPS:**

STEP 1: Is the research question correctly identified and contextualized? (2 points)

**CRITICAL:** The student MUST explicitly state a Research Question. Hypotheses alone are NOT sufficient.

A valid Research Question MUST meet ALL these criteria:
1. Formulated as a question (ends with "?")
2. Contains directional indicators that reveal tail type:
   - Two-tailed indicators: "difference", "affect", "related to", "associated with", "different from"
   - One-tailed indicators: "greater than", "less than", "more than", "improved", "enhanced", "increased", "decreased", "reduced"
3. Specifies both groups being compared (point-and-click vs programming)
4. Specifies the outcome variable (final exam scores, performance, learning, etc.)

Evaluation:
- Full credit (2 pts): ALL four criteria met - question format, clear tail indicators, both groups specified, outcome variable stated
- Partial (1 pt): Question format present with 2-3 criteria met, but missing clarity on groups or outcome
- None (0 pts): Not formulated as a question, OR missing tail indicators, OR groups/outcome unclear/missing


STEP 2: Are hypotheses correctly specified with tail identification? (2 points)
- Full credit (2 pts):
  - H₀ and H₁ correctly stated (μ₁ = μ₂; μ₁ ≠ μ₂)
  - Two-tailed nature justified (testing for "difference," not direction)
- Partial (1 pt):
  - Hypotheses present but lack clear notation or explanation of tail direction, OR
  - Minor conceptual error (e.g., unclear wording)
- None (0 pts): Missing, incorrect, or one-tailed without justification

STEP 3: Are test parameters (α, df, CV) correctly stated and justified? (2 points)
- Full credit (2 pts):
  • α is stated and justified (e.g., α = 0.05 as standard level)
  • df is calculated with formula: df = n₁ + n₂ − 2 = 15 + 14 − 2 = 27
  • Critical value is obtained with method: from t-distribution table using df = 27 and two-tailed α = 0.05 → t ≈ ±2.052
- Partial (1 pt):
  • Parameters given but missing calculations or justification (e.g., df without formula, CV without source), OR
  • One element incorrect but reasoning partially shown
- None (0 pts): Parameters missing, incorrect, or no evidence of calculation/justification

**Scoring:**
- 6 points: All three steps correct with clear explanations
- 5 points: Minor errors or missing justification in one step
- 4 points: Two steps correct, one incomplete
- 3 points: One step fully correct, others attempted
- 2 points: Partial understanding shown across steps
- 1 point: Minimal attempt with some awareness
- 0 points: Missing or completely incorrect


**Component 3: Statistical Analysis (6 points)**

The student must present the test results in a properly formatted table with correct referencing.

**DATA CONTEXT:**
Point-and-Click: 83, 83, 63, 77, 86, 84, 78, 61, 65, 75, 100, 60, 90, 66, 54 (n=15)
Programming: 86, 79, 100, 74, 70, 67, 83, 85, 74, 86, 87, 61, 76, 100 (n=14)

**CORRECT VALUES**

**CORRECT VALUES (from JASP output):**
- t ≈ -1.04
- df = 27
- p > 0.05 (two-tailed)

**REQUIRED TABLE FORMAT:**

Introductory phrase with table reference (e.g., "Table 1 shows the results of the independent-samples t-test..." or "The statistical analysis results are presented in Table 1.")

Table 1
Independent-Samples T-Test Results (or similar descriptive title)

| t | df | p |
|-1.04 | 27 | 0.307 |

**EVALUATION STEPS:**

STEP 1: Introductory phrase and table reference (2 points)
- Full credit (2 pts): Introductory sentence that includes table number reference (e.g., "Table 1 shows...", "As presented in Table 1...", "Results in Table 1...")
- Partial (1 pt): Introductory phrase exists but does NOT reference table number
- None (0 pts): No introductory phrase

STEP 2: Table number (1 point)
- Full credit (1 pt): Table has a number (e.g., "Table 1", "Table 2")
- None (0 pts): No table number

STEP 3: Table title (2 points)
- Full credit (2 pts): Table has a descriptive title that is correctly formulated (e.g., "Independent-Samples T-Test Results", "Comparison of Point-and-Click vs Programming Groups", "Statistical Analysis of Software Effect on Exam Scores")
- Partial (1 pt): Table has a title but it's too generic, unclear, or poorly formulated (e.g., just "Results", "Data", "Table")
- None (0 pts): No table title

STEP 4: Statistical values (1 point)
- Full credit (1 pt): Table includes t, df, and p values with at least one value approximately correct (verifies JASP input was used)
- None (0 pts): Values missing, completely incorrect, or no table

**Scoring:**
- 6 points: Intro phrase with table ref (2) + table number (1) + correct title (2) + correct values (1)
- 5 points: Missing one 1-point element (table number OR values) OR title poorly formulated (1 instead of 2)
- 4 points: Intro without ref (1) + table number (1) + correct title (2) + values (1) OR missing two 1-point elements
- 3 points: Missing intro phrase (0) but has table number (1) + correct title (2) + values (1) OR intro with ref (2) but poor/missing title and missing other elements
- 2 points: Minimal table structure with some elements present
- 1 point: Values mentioned but no proper table structure
- 0 points: No table or analysis presented
---

**Component 4: Test Statistic Calculation (6 points)**

The student must calculate the t-statistic for independent-samples t-test.

**CORRECT CALCULATIONS:**

Point-and-Click group:
- M1 = 75.67
- s1 = 13.58
- n1 = 15

Programming group:
- M2 = 80.57
- s2 = 11.83
- n2 = 14

Standard Error:
SE = sqrt((s1²/n1) + (s2²/n2))
SE = sqrt((13.58²/15) + (11.83²/14))
SE = sqrt((184.42/15) + (139.95/14))
SE = sqrt(12.29 + 10.00)
SE = sqrt(22.29)
SE ≈ 4.72

t-statistic:
t = (M1 - M2) / SE
t = (75.67 - 80.57) / 4.72
t = -4.90 / 4.72
t ≈ -1.04

**EVALUATION STEPS:**

STEP 1: Are descriptive statistics calculated correctly? (2 points)
- Full credit (2 pts): Means, standard deviations, and sample sizes correct
- Partial (1 pt): Some descriptive statistics correct
- None (0 pts): Descriptive statistics missing or all incorrect

STEP 2: Is the standard error calculated correctly? (2 points)
- Full credit (2 pts): SE ≈ 4.72, formula and work shown
- Partial (1 pt): SE attempted but with errors
- None (0 pts): SE missing or completely incorrect

STEP 3: Is the t-statistic calculated correctly? (2 points)
- Full credit (2 pts): t ≈ -1.04 (accept -1.03 to -1.05), formula and work shown
- Partial (1 pt): t attempted but with errors
- None (0 pts): t missing or completely incorrect

**Scoring:**
- 6 points: All calculations correct with work shown
- 5 points: Minor computational errors, close answers
- 4 points: Some calculations correct, some errors
- 3 points: Major errors but reasonable attempt
- 2 points: Minimal calculations with understanding shown
- 1 point: Attempted but mostly incorrect
- 0 points: No calculations or completely wrong

---

**Component 5: Decision and Interpretation (6 points)**

The student must determine degrees of freedom, find critical value, make a decision, and interpret results.

**CORRECT ANALYSIS:**

Degrees of freedom:
df = n1 + n2 - 2 = 15 + 14 - 2 = 27

Critical value (α = 0.05, two-tailed):
t_critical = ±2.052

Decision:
|t| = 1.04 < 2.052
Fail to reject H0

Interpretation:
There is no significant difference in mean final exam scores between students using point-and-click software (M = 75.67, SD = 13.58) and students using programming language (M = 80.57, SD = 11.83), t(27) = -1.04, p > 0.05. The type of software program does not significantly affect how well students learn the material.

**EVALUATION STEPS:**

STEP 1: Are degrees of freedom calculated correctly? (1 point)
- Full credit (1 pt): df = 27
- None (0 pts): df incorrect or missing

STEP 2: Is the critical value identified correctly? (1 point)
- Full credit (1 pt): t_critical ≈ ±2.052 for two-tailed test at α = 0.05
- Partial: Close value or correct concept
- None (0 pts): Critical value incorrect or missing

STEP 3: Is the decision stated correctly? (2 points)
- Full credit (2 pts): Fail to reject H0 with clear reasoning
- Partial (1 pt): Decision stated but reasoning unclear
- None (0 pts): Decision incorrect or missing

STEP 4: Is the interpretation correct and complete? (2 points)
- Full credit (2 pts): Clear interpretation in context, mentions no significant difference, includes statistical notation
- Partial (1 pt): Interpretation attempted but lacks clarity or context
- None (0 pts): Interpretation missing or incorrect

**Scoring:**
- 6 points: All components correct, clear interpretation
- 5 points: Minor errors in critical value or notation
- 4 points: Decision correct but interpretation weak
- 3 points: Some components correct
- 2 points: Major errors but shows understanding
- 1 point: Minimal attempt
- 0 points: No decision/interpretation or completely wrong

---

**COMMON MISTAKES TO WATCH FOR:**

1. **One-tailed instead of two-tailed**: The question asks for "a difference," not "greater than" or "less than"
2. **Wrong formula**: Using paired-samples t-test formula instead of independent-samples
3. **Calculation errors**: Mistakes in means, standard deviations, or standard error
4. **Wrong degrees of freedom**: Using n-1 instead of n1+n2-2
5. **Incorrect decision**: Rejecting H0 when should fail to reject (or vice versa)
6. **Incomplete interpretation**: Not stating results in context of the research question
7. **Missing work**: Providing final answers without showing calculations

---

**FEEDBACK EXAMPLES FOR LOW SCORES:**

If student uses wrong test:
- "Credit for effort, but this requires an independent-samples t-test, not a paired-samples t-test."

If student makes calculation errors:
- "Good attempt at the process, but check your arithmetic in calculating the means and standard error."

If student has correct calculation but wrong interpretation:
- "Your calculations are correct, but your interpretation doesn't match your statistical decision."

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
  "component_2_explanation": "<brief explanation for research framework and hypotheses>",
  "component_3_score": <0-6>,
  "component_3_explanation": "<brief explanation for statistical analysis table>",
  "component_4_score": <0-6>,
  "component_4_explanation": "<brief explanation for decision and interpretation>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of independent-samples t-test>"
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
        print("GRADING RESULTS - HW9_3")
        print("Independent-Samples T-Test: Software Program Effect")
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



            print(f"  Component 2 (Research Framework): {grading.get('component_2_score', 'N/A')}/6")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Statistical Analysis): {grading.get('component_3_score', 'N/A')}/6")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Decision & Interpretation): {grading.get('component_4_score', 'N/A')}/6")
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
    evaluator = HW9_3Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("QUESTION 9.3 EVALUATOR")
    print("Independent-Samples T-Test: Software Program Effect")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION 9_3.")
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
    grading = evaluator.grade_hw9_3_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)