"""
hw12_1.py
Correlational Analysis - Three Characteristics of a Correlation Coefficient
Evaluation method name: def grade_hw12_1_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW12_1Evaluator(BaseEvaluator):
    """
    Evaluator for Correlational Analysis Characteristics Understanding (HW12_1).

    Task: What are the three characteristics of a correlation coefficient?

    Evaluates student's understanding of the three characteristics of a
    correlation coefficient: direction, strength, and form.

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
        first_lines = student_answer[:200]

        elements_found = {
            "paper_title": False,
            "task_description": False,
            "no_autoformatting": True,
        }

        evidence = []

        # STEP 2 — Title (strict)
        title_patterns = [
            r'^\s*homework\s*,?\s*(week)?\s*12',
            r'^\s*home\s*work\s*,?\s*(week)?\s*12',
            r'^\s*hw\s*12\b',
            r'^\s*assignment\s*12',
            r'^\s*paper\s*12'
        ]
        for pattern in title_patterns:
            if re.search(pattern, student_answer,
                         re.IGNORECASE | re.MULTILINE):
                elements_found["paper_title"] = True
                evidence.append("Title found")
                break

        # STEP 3 — Task description (strict)
        # Only phrases a student would NOT write as part of their answer
        task_patterns = [
            r'three\s+characteristics\s+of\s+a\s+correlation\s+coefficient',
            r'what\s+are\s+the\s+three\s+characteristics',
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

    def grade_hw12_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 12_1: Three characteristics of a correlation coefficient.
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
                feedback="[TEST MODE] All formatting elements present. Strong understanding of correlation coefficient characteristics.",
                vibe="Student demonstrates solid grasp of all three characteristics of a correlation coefficient.",
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
"What are the three characteristics of a correlation coefficient?"

Use a **STRICT rubric-based approach**. Total score MUST be exactly 20 points.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. 0 only if completely blank
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. For low-scoring answers, use encouraging language: "Credit for trying..."

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

**Component 2: Direction (8 points)**

The student must explain the direction characteristic of a correlation coefficient.

**KEY CONCEPTS THAT SHOULD BE PRESENT:**

1. **Positive vs. negative direction** (CORE - 3 points)
   - Student must state that correlation can be positive or negative
   - Accept: "positive correlation", "negative correlation", "direct relationship", "inverse relationship"
   - DO NOT accept vague statements like "direction of relationship" without explaining what positive/negative means

2. **Meaning of positive direction** (2 points)
   - Student explains that a positive correlation means both variables increase together
   - Accept: "both increase together", "as X increases Y increases", "same direction"

3. **Meaning of negative direction** (2 points)
   - Student explains that a negative correlation means variables move in opposite directions
   - Accept: "as X increases Y decreases", "opposite direction", "inverse"

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

**Component 3: Strength and Form (8 points)**

The student must explain the strength and form characteristics of a correlation coefficient.

**KEY CONCEPTS THAT SHOULD BE PRESENT:**

1. **Strength** (CORE - 3 points)
   - Student must state that the magnitude of r reflects the strength of the relationship
   - Accept: "strength of relationship", "how strong", "magnitude", "closer to 1 or -1 means stronger"
   - DO NOT accept vague statements like "how related" without referencing the magnitude or the r scale

2. **Form** (2 points)
   - Student mentions that correlation describes the form (shape) of the relationship
   - Accept: "linear relationship", "form of the relationship", "shape", "linear vs non-linear"

3. **Range of r** (2 points)
   - Student references the range of the correlation coefficient (-1 to +1)
   - Accept: "ranges from -1 to 1", "between -1 and +1", "r = 0 means no correlation"

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

**COMMON MISTAKES TO WATCH FOR:**

❌ Listing the three characteristics without explaining them
❌ Confusing strength with significance
❌ Not mentioning the -1 to +1 range
❌ Describing direction without explaining what positive/negative means
❌ Omitting form entirely

✓ Good answer structure: "The three characteristics are direction, strength, and form. Direction refers to... Strength refers to... Form refers to..."

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
  "component_2_explanation": "<brief explanation for direction>",
  "component_3_score": <0-8>,
  "component_3_explanation": "<brief explanation for strength and form>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of correlation coefficient characteristics>"
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
        print("GRADING RESULTS - HW12_1")
        print("Three Characteristics of a Correlation Coefficient")
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

            print(f"  Component 2 (Direction): {grading.get('component_2_score', 'N/A')}/8")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Strength and Form): {grading.get('component_3_score', 'N/A')}/8")
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
    evaluator = HW12_1Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("HOMEWORK 12.1 EVALUATOR")
    print("Three Characteristics of a Correlation Coefficient")
    print("=" * 60)
    print("\nPlease enter the student's answer to HOMEWORK 12_1.")
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
    grading = evaluator.grade_hw12_1_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)
