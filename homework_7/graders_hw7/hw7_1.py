"""
hw7_1.py
What Does a Confidence Interval Represent?
Evaluation method name: def grade_question_hw7_1_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW7_1Evaluator(BaseEvaluator):
    """
    Evaluator for Confidence Interval Definition (HW7_1).

    Task: What does a confidence interval represent?

    Evaluates student's ability to correctly define and explain a confidence
    interval, including the confidence level, and
    correct interpretation of what the interval means.

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
            "student_name": False,
            "paper_title": False,
            "task_description": False,
            "confidence_level_mentioned": False,
            "interval_range_mentioned": False,
            "correct_interpretation": False
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
        if re.search(r'question\s*7[\._]?1', text_lower) or re.search(r'confidence\s*interval', text_lower):
            elements_found["paper_title"] = True
            evidence.append("Title found")
        else:
            evidence.append("Title NOT found")

        # STEP 3 — Task description (strict)
        if re.search(r'task|assignment|instructions?|question\s*:|what\s+does\s+a\s+confidence\s+interval', text_lower):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Confidence level mentioned (e.g., 95%, 90%, confidence level)
        if re.search(r'\d+\s*%|\bconfidence\s+level\b|\bsignificance\s+level\b', text_lower):
            elements_found["confidence_level_mentioned"] = True
            evidence.append("Confidence level or percentage found")

        # Interval / range mentioned
        if re.search(r'\brange\b|\binterval\b|\blower\b|\bupper\b|\bbound\b|\bwidth\b', text_lower):
            elements_found["interval_range_mentioned"] = True
            evidence.append("Interval/range concept found")

        # Correct interpretation: "contain" or "capture" the true parameter
        if re.search(r'\bcontain\b|\bcapture\b|\binclude\b|\bcover\b', text_lower):
            elements_found["correct_interpretation"] = True
            evidence.append("Correct containment interpretation language found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear formatting indicators found"]
        }

    def grade_question_hw7_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 7_1 Task 2: What does a confidence interval represent?
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
                    "component_1_score": 3,
                    "component_2_score": 4,
                    "component_3_score": 3,
                },
                max_points=20,
                feedback="[TEST MODE] Header partially complete. CI definition present but interpretation is incorrect.",
                vibe="Student has basic awareness of confidence intervals but misinterprets what the confidence level means.",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "student_name": True,
                            "paper_title": True,
                            "task_description": True,
                            "confidence_level_mentioned": True,
                            "interval_range_mentioned": True,
                            "correct_interpretation": False
                        },
                        "all_present": False,
                        "evidence": ["Test mode - partial elements present"]
                    }
                }
            )

        formatting_check = self.check_formatting_elements(student_answer)

        prompt = f"""You are grading a statistics assignment where a student must answer:
"What does a confidence interval represent?"

Use a **STRICT rubric-based approach**. Total score MUST be exactly 20 points.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Focus on conceptual correctness over formatting
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. Award partial credit where reasoning is mostly correct but incomplete

---

**RUBRIC:**

**Component 1: Header (5 points)**
Start at 5. Deduct 1 for each missing element below.

STEP 1 - Name [STRICT]: Use elements_found["student_name"].
- If False: deduct 1 point. Add to explanation: "Name is missing. -1 point."

STEP 2 - Title [STRICT]: Use elements_found["paper_title"].
- If False: deduct 1 point. Add to explanation: "Title is missing. -1 point."

STEP 3 - Task Description [STRICT]: Use elements_found["task_description"].
- If False: deduct 1 point. Add to explanation: "Task description is missing. -1 point."

STEP 4 - Answer is present at all [VIBE]: Is any answer to the question provided?
- If completely absent: deduct 1 point. Add to explanation: "No answer provided. -1 point."

---

**Component 2: Definition of Confidence Interval (8 points)**

A correct definition must include ALL of the following ideas:
  a) A CI is a range / interval of values considered plausible or reasonable
  b) It is built around a point estimate (sample mean) with a margin of error extending equally in both directions
  c) We are a certain percentage confident that the calculated range brackets the true population mean

Scoring:
- 8 points: All three ideas (a, b, c) are present and correctly explained
- 6 points: Two of three ideas present and correct
- 4 points: One idea present, OR all three named but poorly explained
- 2 points: Vague reference to CI with no clear explanation of any idea
- 0 points: No definition provided, or definition is entirely wrong

**COMMON MISTAKES:**
- Saying "95% probability the true mean is in THIS interval" — WRONG interpretation (frequentist CI does not assign probability to a fixed interval). Deduct 2 points.
- Confusing CI with hypothesis test p-value: deduct 2 points
- Correctly naming "range" and "confidence level" but missing the population parameter: partial credit

---

**Component 3: Practical Interpretation / Example (7 points)**

Student should demonstrate understanding by providing a practical interpretation or example.

- 7 points: Provides a correct practical interpretation (e.g., "A 95% CI means that if we
  repeated sampling 100 times, 95 of those intervals would contain the true population mean")
  OR applies the concept correctly to an example (e.g., relates it to the dataset used in class)
- 5 points: Interpretation is mostly correct but missing one key nuance (e.g., doesn't mention
  repeated sampling, or confuses "interval contains parameter" with "parameter is 95% likely")
- 3 points: Gives a vague or partially correct real-world example without a full explanation
- 1 point: Attempts an example but it is incorrect or irrelevant
- 0 points: No interpretation or example provided at all

---

**ORIGINALITY CHECK:**
Before finalizing scores, assess whether the answer appears to be AI-generated or copied.
Signs include: textbook-perfect phrasing with no personal voice, unnaturally polished
structure, or language that reads like a Wikipedia/ChatGPT excerpt rather than a student explanation.
- If originality concern detected: set all component scores to 0, set originality_concern to true,
  and set feedback to EXACTLY: "Due to originality concern, your points are frozen. You can get them back if you provide oral explanation for this paper."
- If original student work: set originality_concern to false and proceed normally.

---

**TYPICAL MISTAKES AND PENALTIES:**
- "The true mean falls in this interval with 95% probability" — classic misinterpretation: −2 from Component 2
- Defining CI as a single value instead of a range: −4 from Component 2
- No example or practical application at all: 0/7 on Component 3

---

**STUDENT ANSWER:**
{student_answer}

Return grading in this exact JSON format:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-5>,
  "component_1_explanation": "<brief explanation for header>",
  "component_2_score": <0-8>,
  "component_2_explanation": "<brief explanation for CI definition>",
  "component_3_score": <0-7>,
  "component_3_explanation": "<brief explanation for practical interpretation>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of confidence intervals>"
}}"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "formatting_check": formatting_check
            }
        )

        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results."""
        print("=" * 60)
        print("GRADING RESULTS - HW7_1")
        print("Hypothesis Testing - What Does a Confidence Interval Represent?")
        print("=" * 60)

        if 'component_1_score' in grading:
            # Originality check result
            if grading.get("originality_concern"):
                print("\n⚠️  ORIGINALITY CONCERN DETECTED")
                print("   All points frozen. See feedback below.")

            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Header): {grading.get('component_1_score', 'N/A')}/5")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (CI Definition): {grading.get('component_2_score', 'N/A')}/8")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Practical Interpretation): {grading.get('component_3_score', 'N/A')}/7")
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
    evaluator = HW7_1Evaluator

    # Prompt user for student's answer
    print("=" * 60)
    print("QUESTION 7.1 EVALUATOR")
    print("What Does a Confidence Interval Represent?")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION 7_1.")
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
    grading = evaluator.grade_question_hw7_1_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)
