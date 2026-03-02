"""
hw5_1.py
Sampling Distributions: CLT and LLN Evaluator
Evaluation method name: def grade_question_hw5_1_answer
"""

import re
import textwrap

from config import BaseEvaluator


class HW5_1Evaluator(BaseEvaluator):
    """
    Evaluator for Sampling Distributions Question (HW5_1).
    Task: What are the two mathematical facts that describe how sampling distributions work?

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    def __init__(self):
        """Initialize evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1400
        )

    def check_formatting_elements(self, student_answer: str) -> dict:
        """
        Check if student includes required formatting elements.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()
        first_lines = student_answer[:200]

        elements_found = {
            "student_name": False,
            "paper_title": None,
            "task_description": False,
            "no_autoformatting": True,   # Assumed True; detected False if lists found
            "clt_mentioned": False,
            "lln_mentioned": False
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

        # Check for paper title (e.g., "Homework 5", "HW5", "HW 5")
        title_patterns = [
            r'homework\s*5',
            r'\bhw\s*5\b',
            r'assignment\s*5',
            r'paper\s*5'
        ]
        for pattern in title_patterns:
            if re.search(pattern, text_lower):
                elements_found["paper_title"] = True
                evidence.append(f"Found paper title: {pattern}")
                break

        # Check for task description
        task_patterns = [
            r'two\s+mathematical\s+facts',
            r'sampling\s+distribution',
            r'task\s*:',
            r'question\s*:'
        ]
        for pattern in task_patterns:
            if re.search(pattern, text_lower):
                elements_found["task_description"] = True
                evidence.append(f"Found task description: {pattern}")
                break

        # Check for autoformatting (numbered or bullet lists)
        autoformat_patterns = [
            r'(?m)(?:^\s*\d+[\.\)]\s+\S.*\n){2,}',  # only 2+ consecutive numbered lines
            r'^\s*[-•*]\s+\S',              # bullet list: -, •, *
        ]
        for pattern in autoformat_patterns:
            if re.search(pattern, student_answer, re.MULTILINE):
                elements_found["no_autoformatting"] = False
                evidence.append(f"Autoformatting detected: {pattern}")
                break

        # Check if CLT is mentioned
        clt_patterns = [r'\bclt\b', r'central\s+limit\s+theorem']
        for pattern in clt_patterns:
            if re.search(pattern, text_lower):
                elements_found["clt_mentioned"] = True
                evidence.append("Central Limit Theorem (CLT) is mentioned")
                break

        # Check if LLN is mentioned
        lln_patterns = [r'\blln\b', r'law\s+of\s+large\s+numbers']
        for pattern in lln_patterns:
            if re.search(pattern, text_lower):
                elements_found["lln_mentioned"] = True
                evidence.append("Law of Large Numbers (LLN) is mentioned")
                break

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear formatting elements found"]
        }

    def grade_question_hw5_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade the Sampling Distributions question (HW5_1).
        Task: What are the two mathematical facts that describe how sampling distributions work?

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API

        Returns:
            Detailed grading breakdown dictionary
        """
        # Test mode - use base class method
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 3,
                    "component_2_score": 5,
                    "component_3_score": 6
                },
                max_points=20,
                feedback="Test mode feedback for HW5_1 sampling distributions task.",
                vibe="Test mode vibe assessment",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "student_name": True,
                            "paper_title": True,
                            "task_description": True,
                            "no_autoformatting": True,
                            "clt_mentioned": True,
                            "lln_mentioned": True
                        },
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        # Check for formatting elements
        formatting_check = self.check_formatting_elements(student_answer)
        formatting_summary = formatting_check["elements_found"]

        formatting_block = f"""
        HEADER DETECTION RESULTS (DO NOT RE-EVALUATE — USE AS FACTS):

        student_name_present = {formatting_summary["student_name"]}
        paper_title_present = {formatting_summary["paper_title"]}
        task_description_present = {formatting_summary["task_description"]}

        You MUST deduct points in Component 1 strictly according to these values.
        If student_name_present = False, you MUST deduct 1 point.
        If paper_title_present = False, you MUST deduct 1 point.
        If task_description_present = False, you MUST deduct 1 point.
        """

        # Build the grading prompt
        prompt = f"""{formatting_block}
        You are grading a statistics homework assignment where students must identify and explain the two mathematical facts (the Central Limit Theorem and the Law of Large Numbers) that describe how sampling distributions work.

**TASK DESCRIPTION:**
What are the two mathematical facts that describe how sampling distributions work?

**RUBRIC (20 points total):**

**Component 1: Header & Structural Integrity (5 points)**

Start at 5 points.

PART A — Formal header elements (3 points total)
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

PART B — Content quality elements (2 points total)
Deduct 1 point for each missing element:

STEP 4 - No autoformatting
If the answer uses numbered lists (1. 2. 3.) or bullet points (-, •, *): deduct 1 point.
Add: "Autoformatting detected. -1 point."

STEP 5 - Both theorems mentioned
If either CLT or LLN is completely missing from the answer: deduct 1 point.
Add: "One theorem missing. -1 point."

**Component 2: Central Limit Theorem - named AND explained (8 points)**
- 8 points: CLT is correctly named AND described correctly
  * A correct description includes: the sampling distribution of the sample mean
    approaches a normal distribution as sample size (n) increases / for sufficiently large n
- 4 points: CLT is named and described in at least one sentence, but description is not full or not correct
- 1 point: CLT is named but not described at all
- 0 points: CLT is neither named nor described

**Component 3: Law of Large Numbers - named AND explained (8 points)**
- 8 points: LLN is correctly named AND described correctly
  * A correct description includes: as sample size increases, the sample mean
    converges to / approaches the population mean (larger samples produce more
    accurate estimates of the population parameter)
- 4 points: LLN is named and described in at least one sentence, but description is not full or not correct
- 1 point: LLN is named but not described at all
- 0 points: LLN is neither named nor described

**STUDENT ANSWER:**
{student_answer}

**AUTOMATIC FORMATTING DETECTION RESULT:**
Elements Found: {formatting_check['elements_found']}
Evidence: {formatting_check['evidence']}

**GRADING GUIDELINES:**

For Component 1 (Header & Structural Integrity):
- PART A is evaluated STRICTLY using the boolean flags provided above
- Do NOT re-evaluate name, title, or task description presence
- PART B requires your judgment on autoformatting and theorem coverage
- Total deductions from 5 points; minimum score is 0

For Component 2 (CLT):
- CORRECT ANSWER: CLT states that the sampling distribution of the sample mean
  approaches normality as n increases
- Must discuss BOTH the conclusion (normal distribution) AND the condition (large n)
- Simply naming CLT with a citation but no explanation = 1 point
- Partial explanation (normality mentioned but not large n, or vice versa) = 4 points
- Full correct explanation = 8 points

# ============================================================
# SECTION: Component 3 Grading Guidelines
# ============================================================
For Component 3 (LLN):
- CORRECT ANSWER: LLN states that as sample size increases, the sample mean
  converges to the population mean
- Must explain the convergence/accuracy aspect, not just name the law
- Simply naming LLN with a citation but no explanation = 1 point
- Partial explanation = 4 points
- Full correct explanation = 8 points

**ORIGINALITY CHECK:**
Before finalizing scores, assess whether the answer appears to be AI-generated or copied.
Signs include: textbook-perfect phrasing with no personal voice, unnaturally polished
structure, or language that reads like a Wikipedia/ChatGPT excerpt rather than a student explanation.
- If originality concern detected: set all component scores to 0, set originality_concern to true,
  and set feedback to EXACTLY: "Due to originality concern, your points are frozen. You can get them back if you provide oral explanation for this paper."
- If original student work: set originality_concern to false and proceed normally.

**CRITICAL RULES:**
1. Explanation and reasoning are required; it is not enough just to name CLT and LLN
2. Simply naming a theorem, even with a citation, does not demonstrate sufficient understanding
3. Be strict on Component 1 sub-points (each is independently 0 or 1)
4. For Components 2-3: award 8 points only if both the theorem is correctly named AND the explanation is complete and correct

**SCORING PROCESS:**
1. Check originality - if concern detected, freeze all scores and stop
2. Score Component 1 (Task Setup): __/4
3. Score Component 2 (CLT): __/8
4. Score Component 3 (LLN): __/8
5. Total = sum of components 1-3 (max 20)

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- Notes any originality concern if detected
- Identifies which Task Setup sub-points are missing
- Assesses accuracy and completeness of CLT explanation separately
- Assesses accuracy and completeness of LLN explanation separately
- Remains constructive and educational

Return your grading in this exact JSON format:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-4>,
  "component_1_name_score": <0-1>,
  "component_1_title_score": <0-1>,
  "component_1_task_score": <0-1>,
  "component_1_noformat_score": <0-1>,
  "component_1_explanation": "<if score < 4: one sentence explaining which sub-points are missing; if full points AND exceptional work: one sentence of praise; otherwise empty string>",
  "component_2_score": <0-8>,
  "component_2_explanation": "<if score < 8: one sentence explaining what is missing or incorrect about the CLT explanation; if full points AND exceptional work: one sentence of praise; otherwise empty string>",
  "component_3_score": <0-8>,
  "component_3_explanation": "<if score < 8: one sentence explaining what is missing or incorrect about the LLN explanation; if full points AND exceptional work: one sentence of praise; otherwise empty string>",
  "total_points": <sum of components 1-3, 0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<narrative explanation covering originality check, formatting compliance, and accuracy of CLT and LLN explanations>",
  "vibe": "<one-sentence overall impression of the student's understanding of sampling distributions and the two key mathematical theorems>"
}}"""

        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"formatting_check": formatting_check}
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

    def print_grading_results(self, grading, **kwargs):
        """Helper function to display grading results"""
        print("=" * 60)
        print("GRADING RESULTS - HW5_1")
        print("Sampling Distributions: CLT and LLN")
        print("=" * 60)

        # Originality check result
        if grading.get("originality_concern"):
            print("\n⚠️  ORIGINALITY CONCERN DETECTED")
            print("   All points frozen. See feedback below.")

        # Print component breakdown if available
        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Header & Structural Integrity): {grading.get('component_1_score', 'N/A')}/5")
            print(f"    • Student name:        {grading.get('component_1_name_score', 'N/A')}/1")
            print(f"    • Paper title:         {grading.get('component_1_title_score', 'N/A')}/1")
            print(f"    • Task description:    {grading.get('component_1_task_score', 'N/A')}/1")
            print(f"    • No autoformatting:   {grading.get('component_1_noformat_score', 'N/A')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (CLT): {grading.get('component_2_score', 'N/A')}/8")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (LLN): {grading.get('component_3_score', 'N/A')}/8")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print("=" * 60)

        print(f"\nTOTAL SCORE: {grading.get('total_points', 'N/A')}/{grading.get('max_points', 20)}")
        print(f"PERCENTAGE: {grading.get('percentage', 'N/A')}%")

        print("\n" + "=" * 60)
        print("FEEDBACK:")
        print("=" * 60)
        feedback_text = grading.get('feedback', 'No feedback available')
        wrapped_feedback = textwrap.fill(feedback_text, width=60)
        print(wrapped_feedback)

        print("\n" + "=" * 60)
        print("THE VIBE:")
        print("=" * 60)
        vibe_text = grading.get('vibe', 'N/A')
        wrapped_vibe = textwrap.fill(vibe_text, width=60)
        print(wrapped_vibe)

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
    evaluator = HW5_1Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("HOMEWORK 5 - QUESTION 5_1 EVALUATOR")
    print("Sampling Distributions: CLT and LLN")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION 5_1.")
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
    grading = evaluator.grade_question_hw5_1_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)