"""
hw8_1.py
Dependent-Samples T-Test Research Questions
Evaluation method name: def grade_question_hw8_1_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW8_1Evaluator(BaseEvaluator):
    """
    Evaluator for Dependent-Samples T-Test Research Questions (HW8_1).

    Task: Name 3 research questions that could be addressed using a dependent-
    samples t-test.

    Evaluates student's ability to formulate appropriate research questions
    for dependent-samples t-test with justification.

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
            "student_name": False,
            "paper_title": False,
            "task_description": False,
            "no_autoformatting": True,
        }

        evidence = []

        # STEP 1 — Name (strict)
        name_patterns = [
            r'name\s*:\s*\w+',
            r'student\s*:\s*\w+',
            r'by\s*:\s*\w+',
            r'^\s*[A-Z][a-z]+\s+[A-Z][a-z]+',
        ]
        for pattern in name_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["student_name"] = True
                evidence.append("Name found")
                break
        if not elements_found["student_name"]:
            evidence.append("Name NOT found")

        # STEP 2 — Title (strict)
        title_patterns = [
            r'^\s*homework\s*8',
            r'^\s*hw\s*8\b',
            r'^\s*assignment\s*8',
            r'^\s*paper\s*8'
        ]
        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["paper_title"] = True
                evidence.append("Title found")
                break
        if not elements_found["paper_title"]:
            evidence.append("Title NOT found")

        # STEP 3 — Task description (strict)
        if re.search(r'task|assignment|instructions?|question\s*:|three\s+research\s+questions|3\s+research\s+questions|dependent.?samples\s+t.?test', text_lower):
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

    def grade_question_hw8_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 8_1: Name 3 research questions for dependent-samples t-test.
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
                    "component_2_score": 5,
                    "component_3_score": 4,
                    "component_4_score": 3,
                },
                max_points=20,
                feedback="[TEST MODE] All formatting elements present. Research questions show understanding of dependent t-test concept.",
                vibe="Student demonstrates good grasp of paired/dependent design with room for improvement in justifications.",
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

        student_name_present = {formatting_summary["student_name"]}
        paper_title_present = {formatting_summary["paper_title"]}
        task_description_present = {formatting_summary["task_description"]}
        no_autoformatting_present = {formatting_summary["no_autoformatting"]}

        You MUST deduct points in Component 1 strictly according to these values.
        If student_name_present = False, you MUST deduct 1 point.
        If paper_title_present = False, you MUST deduct 1 point.
        If task_description_present = False, you MUST deduct 1 point.
        If no_autoformatting_present = False, you MUST deduct 1 point.
        """

        prompt = f"""{formatting_block}
        You are grading a statistics assignment where a student must:
"Name 3 research questions that could be addressed using a dependent-samples t-test."

Use a **STRICT rubric-based approach**. Total score MUST be exactly 20 points.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Award 1 point minimum for ANY attempt (even if wrong), 0 only if completely blank
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. For 1-point answers, use encouraging language: "Credit for trying, but..."

---

**RUBRIC:**

**Component 1: Header & Structural Integrity (4 points)**

Start at 4 points.

Deduct 1 point for each missing element:

STEP 1 - Name [STRICT]
Use student_name_present.
If False: deduct 1 point. Add: "Name is missing. -1 point."

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

**Component 2: Research Question 1 (6 points)**

The student must provide a research question appropriate for dependent-samples t-test AND a justification.

**EVALUATION STEPS:**

STEP 1: Is there ANY answer provided for Question 1?
- If completely blank/missing → 0 points, feedback: "No answer provided for Question 1."
- If ANY attempt exists → Continue to STEP 2 (minimum 1 point)

STEP 2: Does the question use dependent/paired structure?
- Same subjects measured twice (before/after, condition A vs B)? OR
- Matched pairs (twins, siblings, couples, etc.)?

If NO (compares independent groups):
→ 1 point, feedback: "Credit for trying, but this compares two separate groups. Dependent t-test requires the SAME people measured twice or matched pairs."

If YES → Continue to STEP 3

STEP 3: Check requirements:
- Exactly 2 conditions/time points?
- Continuous outcome variable (measurable, not categorical)?
- Question clearly worded?

STEP 4: Check justification:
- Does student explain WHY dependent t-test is needed?
- Does justification mention pairing ("same subjects," "matched pairs," "within-subject")?

**SCORING:**
- 6 points: Perfect question + clear justification explaining pairing
- 4 points: Good question but weak/missing justification
- 2-3 points: Correct paired structure but unclear wording OR questionable outcome variable OR poor justification
- 1 point: Wrong (compares independent groups) but attempted
- 0 points: Completely blank

---

**Component 3: Research Question 2 (5 points)**

Same evaluation criteria as Component 2.

**SCORING:**
- 5 points: Perfect question + clear justification
- 3 points: Good question but weak/missing justification
- 2 points: Correct paired structure but quality issues
- 1 point: Wrong (compares independent groups) but attempted
- 0 points: Completely blank

---

**Component 4: Research Question 3 (5 points)**

Same evaluation criteria as Component 2.

**SCORING:**
- 5 points: Perfect question + clear justification
- 3 points: Good question but weak/missing justification
- 2 points: Correct paired structure but quality issues
- 1 point: Wrong (compares independent groups) but attempted
- 0 points: Completely blank

---

**GOOD EXAMPLES OF RESEARCH QUESTIONS:**

Example 1 (Before-After):
"Does a 6-week exercise program reduce resting heart rate in adults?"
Justification: "This requires a dependent-samples t-test because the same participants are measured twice (before and after the program), creating paired observations."

Example 2 (Matched Pairs):
"Do identical twins raised together have more similar IQ scores than identical twins raised apart?"
Justification: "This requires a dependent-samples t-test because twins are naturally matched pairs, and we're comparing the difference in IQ within each twin pair."

Example 3 (Repeated Measures):
"Do drivers have faster reaction times in the morning versus evening?"
Justification: "This requires a dependent-samples t-test because each driver is tested twice (morning and evening), eliminating individual differences in baseline reaction time."

---

**FEEDBACK EXAMPLES FOR 1-POINT ANSWERS:**

If student compares independent groups:
- "Credit for effort, but this question compares two different groups (men vs women), not the same people measured twice."
- "Good attempt, but dependent t-test requires the SAME subjects measured under both conditions."
- "Thanks for trying, but your question involves independent groups. Dependent t-test is for paired data only."

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

Return grading in this exact JSON format:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-4>,
  "component_1_name_score": <0-1>,
  "component_1_title_score": <0-1>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief explanation for header>",
  "component_2_score": <0-6>,
  "component_2_explanation": "<brief explanation for Question 1>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief explanation for Question 2>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief explanation for Question 3>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of dependent-samples t-test>"
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
        print("GRADING RESULTS - HW8_1")
        print("Dependent-Samples T-Test Research Questions")
        print("=" * 60)

        if 'component_1_score' in grading:
            # Originality check result
            if grading.get("originality_concern"):
                print("\n⚠️  ORIGINALITY CONCERN DETECTED")
                print("   All points frozen. See feedback below.")

            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Header): {grading.get('component_1_score', 'N/A')}/4")
            print(f"    • Student name:        {grading.get('component_1_name_score', 'N/A')}/1")
            print(f"    • Paper title:         {grading.get('component_1_title_score', 'N/A')}/1")
            print(f"    • Task description:    {grading.get('component_1_task_score', 'N/A')}/1")
            print(f"    • No autoformatting:   {grading.get('component_1_autoformat_score', 'N/A')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Research Question 1): {grading.get('component_2_score', 'N/A')}/6")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Research Question 2): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Research Question 3): {grading.get('component_4_score', 'N/A')}/5")
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
    evaluator = HW8_1Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("QUESTION 8.1 EVALUATOR")
    print("Dependent-Samples T-Test Research Questions")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION 8_1.")
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
    grading = evaluator.grade_question_hw8_1_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)