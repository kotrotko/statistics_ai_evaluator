"""
cw8_1.py
Classwork 8: Statistical Method Selection and Justification
Evaluation method name: def grade_question_cw8_1_answer
"""
import re
import textwrap

from config import BaseEvaluator


class CW8_1Evaluator(BaseEvaluator):
    """
    Evaluator for Statistical Method Selection (CW8_1).

    Task: In class, state the problem (5 points), and formulate Research question (5 points).
    Using OUR step system, name the statistical method you use (5 points) and explain why this
    method is suitable for our problem solving, based on research design (5 points).

    Evaluates student's ability to state a problem, formulate a research question,
    identify the appropriate statistical method, and justify the choice based on research design.

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
            r'^\s*classwork\s*8',
            r'^\s*cw\s*8\b',
            r'^\s*class\s*work\s*8',
            r'^\s*in.?class\s*8'
        ]
        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["paper_title"] = True
                evidence.append("Title found")
                break
        if not elements_found["paper_title"]:
            evidence.append("Title NOT found")

        # STEP 3 — Task description (strict)
        if re.search(r'task|assignment|instructions?|question\s*:|state\s+the\s+problem|research\s+question|statistical\s+method', text_lower):
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

    def grade_question_cw8_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 8_1: Statistical Method Selection and Justification.
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
                    "component_2_score": 4,
                    "component_3_score": 4,
                    "component_4_score": 4,
                    "component_5_score": 4,
                },
                max_points=20,
                feedback="[TEST MODE] All formatting elements present. Problem stated clearly, research question formulated, method identified with good justification.",
                vibe="Student demonstrates solid understanding of research design and statistical method selection.",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            # "student_name": True,
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
        You are grading a statistics classwork assignment where a student must:
"In class, state the problem (5 points), and formulate Research question (5 points). 
Using OUR step system, name the statistical method you use (5 points) and explain why this 
method is suitable for our problem solving, based on research design (5 points)."

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
- CRITICAL: "Answer:", "Hypothesis:", "Question:", "H0:", "H1:", "Problem:", "Method:" are NOT names
- Look ONLY in the first 1-2 lines of the submission
- A valid student name is: Two words, each starting with a capital letter, like "John Doe" or "Jane Smith"
- The name must appear BEFORE any assignment content (before "Answer:", "Hypothesis:", etc.)
- If you see "Answer:" or "Hypothesis:" in the first line, there is NO name
- If NO name found: deduct 1 point and add feedback: "Your name is expected here. -1 point."

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

**Component 2: Problem Statement (4 points)**

The student must clearly state the problem being addressed.

**EVALUATION:**

STEP 1: Is there ANY problem statement provided?
- If completely blank/missing → 0 points, feedback: "No problem statement provided."
- If ANY attempt exists → Continue to STEP 2 (minimum 1 point)

STEP 2: Evaluate problem statement quality:
- Is the problem clearly articulated?
- Does it identify what needs to be investigated?
- Is it specific and focused?

**SCORING:**
- 4 points: Clear, specific problem statement that identifies exactly what needs to be investigated
- 3 points: Problem stated but lacks some clarity or specificity
- 2 points: Vague or poorly articulated problem statement
- 1 point: Attempted but unclear or confused
- 0 points: Completely blank

---

**Component 3: Research Question (4 points)**

The student must formulate a clear research question.

**EVALUATION:**

STEP 1: Is there ANY research question provided?
- If completely blank/missing → 0 points, feedback: "No research question provided."
- If ANY attempt exists → Continue to STEP 2 (minimum 1 point)

STEP 2: Evaluate research question quality:
- Is it phrased as a question?
- Is it specific and answerable?
- Does it follow from the problem statement?
- Does it specify variables or conditions being compared?

**SCORING:**
- 4 points: Well-formulated research question that is specific, answerable, and clearly related to the problem
- 3 points: Research question present but lacks some clarity or specificity
- 2 points: Vague or poorly formulated research question
- 1 point: Attempted but unclear or not properly structured as a research question
- 0 points: Completely blank

---

**Component 4: Statistical Method Named (4 points)**

The student must name the appropriate statistical method using the step system taught in class.

**EVALUATION:**

STEP 1: Is there ANY statistical method named?
- If completely blank/missing → 0 points, feedback: "No statistical method named."
- If ANY attempt exists → Continue to STEP 2 (minimum 1 point)

STEP 2: Evaluate method identification:
- Is a specific statistical method named (e.g., dependent-samples t-test, independent-samples t-test, ANOVA, correlation, chi-square, etc.)?
- Is the method appropriate for the research question stated?
- Does the student reference the step system used in class?

**SCORING:**
- 4 points: Correct statistical method named and appropriate for the research question; step system referenced
- 3 points: Correct method named but step system not clearly referenced
- 2 points: Method named but not clearly appropriate, or method selection unclear
- 1 point: Attempted but method unclear, wrong, or missing key details
- 0 points: Completely blank

---

**Component 5: Justification Based on Research Design (4 points)**

The student must explain WHY the chosen statistical method is appropriate based on the research design.

**EVALUATION:**

STEP 1: Is there ANY justification provided?
- If completely blank/missing → 0 points, feedback: "No justification provided."
- If ANY attempt exists → Continue to STEP 2 (minimum 1 point)

STEP 2: Evaluate justification quality:
- Does the justification explain WHY this method is appropriate?
- Does it reference key features of the research design (e.g., independent vs dependent samples, number of groups, type of variables)?
- Is the reasoning logically sound?

**SCORING:**
- 4 points: Clear, well-reasoned justification that explicitly connects the research design features to the chosen method
- 3 points: Justification present but lacks some detail or clarity in connecting design to method
- 2 points: Weak or vague justification that doesn't clearly explain the connection
- 1 point: Attempted but justification is unclear, illogical, or irrelevant
- 0 points: Completely blank

---

**EXAMPLE OF A COMPLETE ANSWER:**

Problem Statement:
"We want to determine whether a new sleep intervention improves sleep quality in college students who suffer from insomnia."

Research Question:
"Do college students with insomnia report higher sleep quality scores after completing a 4-week sleep intervention compared to before the intervention?"

Statistical Method:
"Using the step system, this requires a dependent-samples t-test."

Justification:
"This method is appropriate because we are comparing the same group of students at two different time points (before and after the intervention), which creates paired observations. The dependent-samples t-test is designed for this type of within-subjects design where we measure the same individuals twice."

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
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief explanation for problem statement>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief explanation for research question>",
  "component_4_score": <0-4>,
  "component_4_explanation": "<brief explanation for method named>",
  "component_5_score": <0-4>,
  "component_5_explanation": "<brief explanation for justification>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of statistical method selection and research design>"
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
                "component_4_score",
                "component_5_score"
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results."""
        print("=" * 60)
        print("GRADING RESULTS - CW8_1")
        print("Statistical Method Selection and Justification")
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
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Problem Statement): {grading.get('component_2_score', 'N/A')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Research Question): {grading.get('component_3_score', 'N/A')}/4")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Method Named): {grading.get('component_4_score', 'N/A')}/4")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Justification): {grading.get('component_5_score', 'N/A')}/4")
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

    # Initialize evaluator
    evaluator = CW8_1Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("CLASSWORK 8.1 EVALUATOR")
    print("Statistical Method Selection and Justification")
    print("=" * 60)
    print("\nPlease enter the student's answer to CLASSWORK 8_1.")
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
    grading = evaluator.grade_question_cw8_1_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)