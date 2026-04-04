"""
hw12_2.py
Correlational Analysis - Importance of Scatterplot Visualization
Evaluation method name: def grade_hw12_2_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW12_2Evaluator(BaseEvaluator):
    """
    Evaluator for Scatterplot Visualization Importance (HW12_2).

    Task: Why is it important to visualize correlational data in a scatterplot
    before performing analyses?

    Evaluates student's understanding of why scatterplot visualization is
    essential before correlational analysis.

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
            r'why\s+is\s+it\s+important\s+to\s+visualize',
            r'visualize\s+correlational\s+data\s+in\s+a\s+scatterplot\s+before',
            r'before\s+performing\s+anal',
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

    def grade_hw12_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 12_2: Importance of scatterplot visualization before correlational analysis.
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
                feedback="[TEST MODE] All formatting elements present. Strong understanding of scatterplot importance.",
                vibe="Student demonstrates solid understanding of why visualization precedes correlational analysis.",
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
"Why is it important to visualize correlational data in a scatterplot before performing analyses?"

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

**Component 2: Detecting Non-Linearity and Assumption Checking (9 points)**

The student must explain why a scatterplot helps verify assumptions before correlational analysis.

**KEY CONCEPTS THAT SHOULD BE PRESENT:**

1. **Detecting non-linear relationships** (CORE - 3 points)
   - Student must state that a scatterplot reveals whether the relationship is linear or not
   - Pearson's r assumes linearity; if the relationship is curved, r is misleading
   - Accept: "non-linear relationship", "curved pattern", "linearity assumption", "Pearson assumes linearity"
   - DO NOT accept vague statements like "see the data" without mentioning linearity or assumption

2. **Identifying outliers** (3 points)
   - Student mentions that a scatterplot reveals outliers that can distort the correlation
   - Accept: "outliers", "extreme values", "influential points", "distort r", "affect the result"
   - DO NOT accept vague statements like "unusual data" without connecting to correlation distortion

3. **Assessing direction and form visually** (2 points)
   - Student notes that the scatterplot gives a visual sense of direction and pattern before computing r
   - Accept: "positive or negative trend", "direction of relationship", "form of the relationship", "visual pattern"

4. **Clarity and coherence** (1 point)
   - Explanation is clear and well-organized
   - Uses appropriate statistical terminology

**KEY CONCEPTS TO LOOK FOR:**
✓ Linearity assumption mentioned
✓ Outliers and their effect on r mentioned
✓ Visual inspection of direction or form
✓ Connection between what the plot reveals and the choice of analysis

**COMMON MISTAKES:**
❌ Saying "to see the data" without explaining what specifically to look for
❌ Not mentioning the linearity assumption
❌ Not mentioning outliers or their distorting effect
❌ Vague statements like "it helps understand the data" with no specific reasoning

**Scoring Guide:**
- 9 points: Linearity, outliers, and direction/form all clearly addressed with good reasoning
- 7-8 points: Two of three key concepts well addressed, minor gaps
- 5-6 points: Core concept (linearity or outliers) present but incomplete
- 3-4 points: Vague or partial understanding, missing key concepts
- 1-2 points: Minimal effort or fundamental misunderstanding
- 0 points: Blank or completely incorrect

---

**Component 3: Choosing the Appropriate Analysis (9 points)**

The student must explain how scatterplot inspection informs the choice of correlational method.

**KEY CONCEPTS THAT SHOULD BE PRESENT:**

1. **Selecting parametric vs. non-parametric method** (CORE - 3 points)
   - Student must state that the scatterplot helps decide between Pearson and Spearman (or other alternatives)
   - If linearity holds: Pearson; if not: Spearman or other non-parametric alternative
   - Accept: "choose between Pearson and Spearman", "parametric vs non-parametric", "select appropriate test"
   - DO NOT accept vague statements like "choose the right method" without naming the methods

2. **Avoiding misleading results** (3 points)
   - Student explains that running Pearson on non-linear data produces a misleading or incorrect r
   - Accept: "misleading correlation", "incorrect r", "underestimate the relationship", "r does not capture curve"
   - DO NOT accept vague statements like "wrong result" without explaining why

3. **Connecting visualization to analytical decision** (2 points)
   - Student explicitly links what is seen in the scatterplot to the decision of which statistic to use
   - Accept: "if the plot shows a curve, use Spearman", "based on the plot we can decide", "visual check guides the choice"

4. **Clarity and coherence** (1 point)
   - Explanation is clear and well-organized
   - Uses appropriate statistical terminology

**KEY CONCEPTS TO LOOK FOR:**
✓ Pearson vs. Spearman decision mentioned
✓ Consequence of wrong choice explained
✓ Explicit link between scatterplot observation and method selection

**COMMON MISTAKES:**
❌ Not naming specific methods (Pearson, Spearman)
❌ Saying "choose the right test" without explaining the logic
❌ Not explaining what happens if the wrong method is chosen
❌ Treating visualization as optional or purely aesthetic

**Scoring Guide:**
- 9 points: Method selection logic clear, consequence of wrong choice explained, explicit link to scatterplot
- 7-8 points: Method selection mentioned, minor gaps in reasoning
- 5-6 points: Partial understanding of method selection, missing consequence or link
- 3-4 points: Vague method selection, no consequence discussed
- 1-2 points: Attempted but fundamentally incorrect or too vague
- 0 points: No attempt or completely wrong

---

**FEEDBACK EXAMPLES:**

For good linearity explanation but missing outliers:
- "Good explanation of the linearity assumption, but don't forget that scatterplots also help detect outliers that can distort r."

For good outlier discussion but missing method selection:
- "You correctly identified outliers as a concern, but you should also explain how the scatterplot guides the choice between Pearson and Spearman."

For vague answers:
- "Credit for trying, but 'seeing the data' is not specific enough. Focus on linearity, outliers, and method selection."

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
  "component_2_explanation": "<brief explanation for assumption checking and non-linearity>",
  "component_3_score": <0-9>,
  "component_3_explanation": "<brief explanation for method selection reasoning>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of scatterplot importance>"
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
        print("GRADING RESULTS - HW12_2")
        print("Importance of Scatterplot Visualization")
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

            print(f"  Component 2 (Non-Linearity and Assumption Checking): {grading.get('component_2_score', 'N/A')}/9")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Choosing the Appropriate Analysis): {grading.get('component_3_score', 'N/A')}/9")
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
    evaluator = HW12_2Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("HOMEWORK 12.2 EVALUATOR")
    print("Importance of Scatterplot Visualization")
    print("=" * 60)
    print("\nPlease enter the student's answer to HOMEWORK 12_2.")
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
    grading = evaluator.grade_hw12_2_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)