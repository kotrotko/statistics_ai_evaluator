"""
hw10_1.py
One-Way ANOVA - Understanding Null Hypothesis Rejection
Evaluation method name: def grade_hw10_1_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW10_1Evaluator(BaseEvaluator):
    """
    Evaluator for One-Way ANOVA Null Hypothesis Understanding (HW10_1).

    Task: What does rejecting the null hypothesis in ANOVA tell us?
    What does it not tell us?

    Evaluates student's understanding of ANOVA null hypothesis rejection
    and its limitations.

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
            "paper_title": False,
            "task_description": False,
            "no_autoformatting": True,
        }

        evidence = []

        # STEP 2 — Title (strict)
        # STEP 2 — Title (strict)
        title_patterns = [
            r'^\s*homework\s*,?\s*(week)?\s*10',
            r'^\s*home\s*work\s*,?\s*(week)?\s*10',
            r'^\s*hw\s*10\b',
            r'^\s*assignment\s*10',
            r'^\s*paper\s*10'
        ]
        for pattern in title_patterns:
            if re.search(pattern, student_answer,
                         re.IGNORECASE | re.MULTILINE):  # ← use student_answer, not first_lines
                elements_found["paper_title"] = True
                evidence.append("Title found")
                break


        # STEP 3 — Task description (strict)
        task_patterns = [
            r'rejecting\s+the\s+null\s+hypothesis\s+in\s+anova',
            r'what\s+does\s+it\s+not\s+tell',
            r'null\s+hypothesis.*anova',
            r'anova.*null\s+hypothesis'
        ]
        if any(re.search(pattern, text_lower) for pattern in task_patterns):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # STEP 4 — No autoformatting (strict)
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

    def grade_hw10_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 10_1: ANOVA null hypothesis rejection understanding.
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
                    "component_1_score": 4,
                    "component_1_name_score": 1,
                    "component_1_title_score": 1,
                    "component_1_task_score": 1,
                    "component_1_autoformat_score": 1,
                    "component_2_score": 8,
                    "component_3_score": 8,
                },
                max_points=20,
                feedback="[TEST MODE] All formatting elements present. Strong understanding of ANOVA null hypothesis.",
                vibe="Student demonstrates solid grasp of what ANOVA tells us and its limitations.",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "student_name": True,
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

        paper_title_present = {formatting_summary["paper_title"]}
        task_description_present = {formatting_summary["task_description"]}
        no_autoformatting_present = {formatting_summary["no_autoformatting"]}

        You MUST deduct points in Component 1 strictly according to these values.
        If paper_title_present = False, you MUST deduct 1 point.
        If task_description_present = False, you MUST deduct 1 point.
        If no_autoformatting_present = False, you MUST deduct 1 point.
        """

        prompt = f"""{formatting_block}
        You are grading a statistics assignment where a student must answer:
"What does rejecting the null hypothesis in ANOVA tell us? What does it not tell us?"

Use a **STRICT rubric-based approach**. Total score MUST be exactly 20 points.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. 0 only if completely blank
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. For low-scoring answers, use encouraging language: "Credit for trying, but..."

---

**RUBRIC:**

**Component 1: Header & Structural Integrity (4 points)**

Start at 4 points.

Deduct 1 point for each missing element:

STEP 1 - Name [STRICT]
- CRITICAL: "Answer:", "Hypothesis:", "Question:", "H0:", "H1:", "Problem:", "Method:" are NOT names
- Look ONLY in the first 1-2 lines of the submission
- A valid student name is: Two words, each starting with a capital letter, like "John Doe" or "Jane Smith"
- The name must appear BEFORE any assignment content (before "Answer:", "Hypothesis:", etc.)
- If you see "Answer:" or "Hypothesis:" in the first line, there is NO name
- If name found: component_1_name_score = 1
- If NO name found: component_1_name_score = 0

STEP 2 - Title [STRICT]
Use paper_title_present.
If False: deduct 1 point. Add: "Title is missing. -1 point."

STEP 3 - Task Description [STRICT]
Use task_description_present.
If False: deduct 1 point. Add: "Task description is missing. -1 point."

STEP 4 - No autoformatting [STRICT]
Use no_autoformatting_present.
If False: deduct 1 point. Add: "Autoformatting detected. -1 point."

---

**Component 2: What Rejecting the Null Hypothesis TELLS US (8 points)**

The student must explain what we can conclude when we reject the null hypothesis in ANOVA.

**KEY CONCEPTS THAT SHOULD BE PRESENT:**

1. **At least one group mean differs** (CORE - 3 points)
   - Student must state that rejection means at least one group mean is different from the others
   - Accept variations: "at least one mean differs", "not all means are equal", "at least one group is different"
   - DO NOT accept vague statements like "there are differences" without specifying "group means" or "at least one"

2. **Statistical significance** (2 points)
   - Student mentions that the difference is statistically significant
   - Accept: "significant difference", "p < α", "reject at significance level"

3. **Overall effect exists** (2 points)
   - Student indicates that there IS an effect of the independent variable
   - Accept: "the independent variable has an effect", "the factor matters", "groups are not all the same"

4. **Clarity and coherence** (1 point)
   - Explanation is clear and well-organized
   - Uses appropriate statistical terminology

**SCORING GUIDE:**
- 8 points: All key concepts present with clear explanation
- 6-7 points: Most key concepts present, minor gaps
- 4-5 points: Core concept present but incomplete or unclear
- 2-3 points: Vague or partially correct understanding
- 1 point: Minimal effort or fundamental misunderstanding
- 0 points: Blank or completely incorrect

---

**Component 3: What Rejecting the Null Hypothesis DOES NOT TELL US (8 points)**

The student must explain the LIMITATIONS of rejecting the null hypothesis in ANOVA.

**KEY CONCEPTS THAT SHOULD BE PRESENT:**

1. **Does NOT tell us WHICH specific groups differ** (CORE - 3 points)
   - This is the MOST IMPORTANT limitation
   - Student must explicitly state that ANOVA doesn't identify which pairs of groups are different
   - Accept: "doesn't tell us which groups differ", "need post-hoc tests", "can't identify specific differences"
   - DO NOT accept vague statements like "need more tests" without mentioning post-hoc or pairwise comparisons

2. **Does NOT tell us the magnitude/effect size** (2 points)
   - Student mentions that rejection doesn't indicate how large or important the difference is
   - Accept: "doesn't show effect size", "doesn't tell us practical significance", "doesn't show magnitude"

3. **Does NOT tell us the direction of differences** (2 points)
   - Student notes that we don't know which group has higher/lower values
   - Accept: "doesn't show which group is higher", "need to examine means to see direction"

4. **Clarity and coherence** (1 point)
   - Explanation is clear and well-organized
   - Uses appropriate statistical terminology

**SCORING GUIDE:**
- 8 points: All key concepts present with clear explanation
- 6-7 points: Most key concepts present, core limitation clearly stated
- 4-5 points: Core limitation present but other limitations missing
- 2-3 points: Vague understanding or missing core limitation
- 1 point: Minimal effort or fundamental misunderstanding
- 0 points: Blank or completely incorrect

---

**COMMON MISTAKES TO WATCH FOR:**

❌ Saying "we reject H0" without explaining what that means
❌ Saying "there are differences" without specifying "between group means"
❌ Not mentioning that ANOVA doesn't identify WHICH groups differ (this is critical!)
❌ Confusing statistical significance with practical significance
❌ Not mentioning post-hoc tests when discussing limitations

✓ Good answer structure: "Rejecting H0 tells us [concept 1], [concept 2]... However, it does NOT tell us [limitation 1], [limitation 2]..."

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

For component_1_name_score:
- CRITICAL: "Answer:", "Hypothesis:", "Question:", "H0:", "H1:", "Problem:", "Method:" are NOT names
- Look ONLY in the first 1-2 lines of the submission
- A valid student name is: Two words, each starting with a capital letter, like "John Doe" or "Jane Smith"
- The name must appear BEFORE any assignment content (before "Answer:", "Hypothesis:", etc.)
- If you see "Answer:" or "Hypothesis:" in the first line, there is NO name
- If name found: component_1_name_score = 1
- If NO name found: component_1_name_score = 0

For component_1_title_score: use paper_title_present (1 if True, 0 if False)
For component_1_task_score: use task_description_present (1 if True, 0 if False)
For component_1_autoformat_score: use no_autoformatting_present (1 if True, 0 if False)

Return grading in this exact JSON format:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-4>,
  "component_1_name_score": <0-1>,
  "component_1_title_score": <0-1>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief explanation for header>",
  "component_2_score": <0-8>,
  "component_2_explanation": "<brief explanation for what rejection tells us>",
  "component_3_score": <0-8>,
  "component_3_explanation": "<brief explanation for what rejection does NOT tell us>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of ANOVA null hypothesis rejection>"
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
        print("GRADING RESULTS - HW10_1")
        print("ANOVA Null Hypothesis Rejection Understanding")
        print("=" * 60)

        if 'component_1_score' in grading:
            # Originality check result
            if grading.get("originality_concern"):
                print("\n⚠️  ORIGINALITY CONCERN DETECTED")
                print("   All points frozen. See feedback below.")

            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Header): {grading.get('component_1_score', 'N/A')}/4")
            print(f"    • Student name:        {grading.get('component_1_name_score', 'N/A')}/1 (LLM)")
            print(f"    • Paper title:         {grading.get('component_1_title_score', 'N/A')}/1 (regex)")
            print(f"    • Task description:    {grading.get('component_1_task_score', 'N/A')}/1 (regex)")
            print(f"    • No autoformatting:   {grading.get('component_1_autoformat_score', 'N/A')}/1 (regex)")
            if grading.get('component_1_explanation'):
                print(f"   → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (What Rejection TELLS Us): {grading.get('component_2_score', 'N/A')}/8")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (What Rejection DOES NOT Tell Us): {grading.get('component_3_score', 'N/A')}/8")
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
    evaluator = HW10_1Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("HOMEWORK 10.1 EVALUATOR")
    print("ANOVA Null Hypothesis Rejection Understanding")
    print("=" * 60)
    print("\nPlease enter the student's answer to HOMEWORK 10_1.")
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
    grading = evaluator.grade_hw10_1_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)
