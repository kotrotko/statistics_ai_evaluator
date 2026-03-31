"""
hw9_1.py
Independent-Samples T-Test Research Questions
Evaluation method name: def grade_question_hw9_1_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW9_1Evaluator(BaseEvaluator):
    """
    Evaluator for Independent-Samples T-Test Research Questions (HW9_1).

    Task: Describe 3 research questions that could be tested using an
    independent-samples t-test.

    Evaluates student's ability to formulate appropriate research questions
    for independent-samples t-test with justification.

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
        title_patterns = [
            r'^\s*homework\s*9',
            r'^\s*home\s*work\s*(week)?\s*9',
            r'^\s*hw\s*9\b',
            r'^\s*assignment\s*9',
            r'^\s*paper\s*9'
        ]
        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["paper_title"] = True
                evidence.append("Title found")
                break
        if not elements_found["paper_title"]:
            evidence.append("Title NOT found")

        # STEP 3 — Task description (strict)
        if re.search(r'task|assignment|instructions?|question\s*:|three\s+research\s+questions|3\s+research\s+questions|independent.?samples\s+t.?test', text_lower):
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

    def grade_hw9_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 9_1: Describe 3 research questions for independent-samples t-test.
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
                feedback="[TEST MODE] All formatting elements present. Research questions show understanding of independent t-test concept.",
                vibe="Student demonstrates good grasp of independent groups design with room for improvement in justifications.",
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
        You are grading a statistics assignment where a student must:
"Describe 3 research questions that could be tested using an independent-samples t-test."

Use a **STRICT rubric-based approach**. Total score MUST be exactly 20 points.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. 0 only if completely blank
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. For 1-point answers, use encouraging language: "Credit for trying, but..."

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

**Component 2: Research Question 1 (6 points)**

The student must provide a research question appropriate for independent-samples t-test AND a justification.

**EVALUATION STEPS:**

STEP 1: Does the question compare TWO SEPARATE/INDEPENDENT GROUPS?
- Look for: different people, different conditions, mutually exclusive categories
- Examples: men vs women, treatment vs control, public school vs private school
- If YES → proceed to STEP 2
- If NO (compares same people twice) → maximum 1 point for effort

STEP 2: Is the outcome variable CONTINUOUS/MEASURABLE?
- Look for: scores, times, heights, weights, rates, amounts
- Examples: test scores, reaction time, blood pressure, satisfaction ratings
- If YES → proceed to STEP 3
- If NO (categorical outcome like yes/no) → maximum 2 points

STEP 3: Quality of justification
- Does student explain WHY it requires independent-samples t-test?
- Key elements: mentions two separate groups, explains independence, identifies continuous outcome
- Strong justification → full points possible
- Weak/missing justification → deduct 2 points

**SCORING:**
- 6 points: Perfect question + clear, comprehensive justification
- 4 points: Good question but weak justification OR minor issues with question clarity
- 2 points: Correct independent groups structure but significant quality issues
- 1 point: Wrong (compares same people twice) but attempted
- 0 points: Completely blank

---

**Component 3: Research Question 2 (5 points)**

Same evaluation process as Component 2, but maximum 5 points.

**SCORING:**
- 5 points: Perfect question + clear justification
- 3 points: Good question but weak/missing justification
- 2 points: Correct independent groups structure but quality issues
- 1 point: Wrong (compares same people twice) but attempted
- 0 points: Completely blank

---

**Component 4: Research Question 3 (5 points)**

Same evaluation process as Component 2, but maximum 5 points.

**SCORING:**
- 5 points: Perfect question + clear justification
- 3 points: Good question but weak/missing justification
- 2 points: Correct independent groups structure but quality issues
- 1 point: Wrong (compares same people twice) but attempted
- 0 points: Completely blank

---

**GOOD EXAMPLES OF RESEARCH QUESTIONS:**

Example 1 (Group Comparison):
"Do male students have higher average math test scores than female students?"
Justification: "This requires an independent-samples t-test because we're comparing two separate groups (males and females) on a continuous outcome variable (test scores). Each student belongs to only one group."

Example 2 (Treatment vs Control):
"Does a new drug reduce average blood pressure more than a placebo?"
Justification: "This requires an independent-samples t-test because participants are randomly assigned to either the drug group OR the placebo group (not both), and we're comparing a continuous measure (blood pressure) between these two independent groups."

Example 3 (Condition Comparison):
"Do children from single-parent households have different average self-esteem scores compared to children from two-parent households?"
Justification: "This requires an independent-samples t-test because the two groups (single-parent vs two-parent households) are mutually exclusive, and we're measuring a continuous variable (self-esteem scores) across these independent groups."

---

**BAD EXAMPLES (These are DEPENDENT samples, NOT independent):**

Example 1 (Before-After):
"Does exercise reduce heart rate?" — WRONG if measuring same people before/after
This is a dependent-samples t-test because the same participants are measured twice.

Example 2 (Repeated Measures):
"Do students perform better in morning classes vs afternoon classes?" — WRONG if same students tested both times
This is a dependent-samples t-test because each student provides data for both conditions.

Example 3 (Matched Pairs):
"Do twins have similar IQ scores?" — WRONG
This is a dependent-samples t-test because twins are naturally paired.

---

**KEY DISTINCTION:**
- INDEPENDENT samples: Two DIFFERENT groups of people (Group A vs Group B)
- DEPENDENT samples: SAME people measured twice OR naturally paired individuals

---

**FEEDBACK EXAMPLES FOR 1-POINT ANSWERS:**

If student compares same people twice:
- "Credit for effort, but this question measures the same people twice (before/after). Independent t-test requires two separate groups."
- "Good attempt, but independent t-test is for comparing DIFFERENT people in two groups, not the same people under two conditions."
- "Thanks for trying, but your question uses paired/dependent data. Independent t-test needs two mutually exclusive groups."

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
        print("GRADING RESULTS - HW9_1")
        print("Independent-Samples T-Test Research Questions")
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
    evaluator = HW9_1Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("QUESTION 9.1 EVALUATOR")
    print("Independent-Samples T-Test Research Questions")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION 9_1.")
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
    grading = evaluator.grade_hw9_1_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)