"""
hw13_5.py
Linear Regression - Line of best fit and hypothesis testing
Evaluation method name: def grade_hw13_5_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW13_5Evaluator(BaseEvaluator):
    """
    Evaluator for Line of Best Fit and Hypothesis Testing (HW13_5).

    Task: You have summary data for two variables: how extroverted someone is (X)
    and how often someone volunteers (Y). Using these values, calculate the line of
    best fit predicting volunteering from extroversion then test for a statistically
    significant relation using the hypothesis testing procedure:
    X= 12.58, sX =4.65, Y= 7.44, sY = 2.12, r = 0.34, N = 67, SSM = 19.79, SSE = 215.77.

    Correct values:
    b = 0.1550, a = 5.490, Ŷ = 5.490 + 0.155X
    df Model = 1, df Error = 65, MS Model = 19.79, MS Error = 3.320, F = 5.962
    Critical value F(1, 65) ≈ 3.99 at α = 0.05 → reject H0

    Rubric:
    - Task description (1 point)
    - Problem statement (4 points)
    - Research question + hypotheses (5 points)
    - Line of best fit calculations and equation (5 points)
    - Hypothesis test, ANOVA table, and statistical inference (5 points)
    Total (strictly) 20 points.

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
            "using these values, calculate the line of best fit predicting volunteering from extroversion",
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

    def grade_hw13_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Homework 13.5: Line of best fit and hypothesis testing.
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
                    "component_2_score": 4,
                    "component_3_score": 5,
                    "component_4_score": 5,
                    "component_5_score": 4,
                },
                max_points=20,
                feedback="[TEST MODE] All components present. Problem statement, RQ, hypotheses, equation, and inference all correct.",
                vibe="Student demonstrates solid understanding of linear regression and hypothesis testing.",
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
        You are grading a statistics assignment where a student must calculate the line
        of best fit and test for a statistically significant relationship between
        extroversion (X) and volunteering (Y).

Use a **STRICT rubric-based approach**. Total score MUST be exactly 20 points.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. 0 only if completely blank
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. For low-scoring answers, use encouraging language: "Credit for trying, but..."

---

**CORRECT ANSWERS:**

Given: X̄ = 12.58, sX = 4.65, Ȳ = 7.44, sY = 2.12, r = 0.34, N = 67, SSM = 19.79, SSE = 215.77

b = 0.34 × (2.12 / 4.65) = 0.1550
a = 7.44 − 0.1550 × 12.58 = 5.490
Equation: Ŷ = 5.490 + 0.155X

ANOVA table:
df Model = 1, df Error = 65, df Total = 66
MS Model = 19.79, MS Error = 3.320, F = 5.962
SST = 235.56

Critical value F(1, 65) ≈ 3.99 at α = 0.05
Since F = 5.962 > 3.99, reject H0.

Accept minor rounding differences of ±0.05.

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

**Component 2: Problem Statement (3 points)**

Student must describe the research problem in their own words, connected to the
context of extroversion and volunteering.

- 4 points: Clear, specific, well-articulated problem in own words, connected to
  the variables (extroversion, volunteering) and the goal (predicting volunteering
  from extroversion)
- 3 points: Problem present but vague or missing variable context
- 2 points: Problem poorly articulated but shows some understanding
- 1 point: Attempted but unclear or off-topic
- 0 points: Completely absent

CRITICAL: Do NOT accept a restatement of the research question as a problem statement.

---

**Component 3: Research Question and Hypotheses (5 points)**

Student must formulate a clear research question AND state both H0 and H1 correctly.

Breaking down the 5 points:
- 2 points: Clear, testable research question connecting extroversion and volunteering
- 3 points: Both hypotheses correctly stated
  H0: β = 0 (extroversion does not significantly predict volunteering)
  H1: β ≠ 0 (extroversion significantly predicts volunteering)

- 2 points (RQ): Clear and testable question / 1 point: vague or partially correct / 0: absent
- 3 points (hypotheses): Both correct / 2 points: one correct / 1 point: attempted but wrong / 0: absent

Accept symbolic or verbal forms for hypotheses.

---

**Component 4: Line of Best Fit Calculations and Equation (5 points)**

Student must calculate b and a correctly and write the regression equation.

Breaking down the 5 points:
- 2 points: b calculated correctly (0.155, accept ±0.005)
- 2 points: a calculated correctly (5.490, accept ±0.05)
- 1 point: Equation written correctly in the form Ŷ = a + bX

CRITICAL: Both b and a must be shown with calculation steps, not just stated.

---

**Component 5: Hypothesis Test, ANOVA Table, and Statistical Inference (5 points)**

Student must present the ANOVA table, state α and critical value, and make a formal inference.

Breaking down the 5 points:
- 1 point: α = 0.05 stated
- 1 point: df correctly calculated (df Model = 1, df Error = 65)
- 1 point: F value correctly calculated (5.962, accept ±0.05)
- 1 point: Critical value correctly identified (≈ 3.99)
- 1 point: Correct formal inference stated
  e.g. "F(1, 65) = 5.962 > 3.99, reject H0 — there is a statistically significant
  linear relationship between extroversion and volunteering"

CRITICAL: Inference must explicitly state the decision about H0.
CRITICAL: Direction must match the reported F value.

---

**COMMON MISTAKES TO WATCH FOR:**

❌ Confusing b and a in the equation
❌ Using df = N − 1 instead of N − 2 for df Error
❌ Computing F = MS Error / MS Model instead of MS Model / MS Error
❌ Stating result is not significant when F = 5.962 > critical value
❌ Missing the ANOVA table entirely

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
  "component_2_score": <0-3>,
  "component_2_explanation": "<brief explanation for problem statement>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief explanation for research question and hypotheses>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief explanation for line of best fit calculations>",
  "component_5_score": <0-5>,
  "component_5_explanation": "<brief explanation for hypothesis test and inference>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of linear regression>"
}}"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "formatting_check": formatting_check
            }
        )

        # Enforcement: component_1_score calculated in Python, never trusted from LLM
        if "error" not in result:
            task_score = 1 if formatting_summary["task_description"] else 0
            autoformat_score = 1 if formatting_summary["no_autoformatting"] else 0
            result["component_1_task_score"] = task_score
            result["component_1_autoformat_score"] = autoformat_score
            result["component_1_score"] = task_score + autoformat_score

        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score",
                "component_5_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results."""
        print("=" * 60)
        print("GRADING RESULTS - HW13_5")
        print("Line of Best Fit and Hypothesis Testing")
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

            print(f"  Component 2 (Problem Statement): {grading.get('component_2_score', 'N/A')}/3")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Research Question and Hypotheses): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Line of Best Fit Calculations): {grading.get('component_4_score', 'N/A')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Hypothesis Test and Inference): {grading.get('component_5_score', 'N/A')}/5")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

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

    evaluator = HW13_5Evaluator()

    print("=" * 60)
    print("HOMEWORK 13.5 EVALUATOR")
    print("Line of Best Fit and Hypothesis Testing")
    print("=" * 60)
    print("\nPlease enter the student's answer to HOMEWORK 13_5.")
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

    grading = evaluator.grade_hw13_5_answer(student_answer)

    evaluator.print_grading_results(grading)