"""
cw8_1.py
Classwork 8: Paired t-test
Problem statement, RQ, method, and justification.
Evaluation method name: def grade_question_cw8_1_answer
"""
import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter


class CW8_1Evaluator(BaseEvaluator):
    """
    Evaluator for Paired t-test (CW8_1).

    Task: State the problem (5 points).
    Formulate the main Research question (5 points).
    Name the statistical method you use (5 points) and explain why this
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
            max_tokens=1200
        )
        self.formatter = OutputFormatter(default_width=60)

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check if required structural and content elements are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()
        first_lines = student_answer[:200]

        # Regex-based checks only — elements verifiable by rules, not AI
        elements_found = {
            "name": False,
            "title": False,
            "task_description": False,
            "autoformatting": False,
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
                elements_found["name"] = True
                evidence.append("Name found")
                break
        if not elements_found["name"]:
            evidence.append("Name NOT found")

        # STEP 2 — Title (strict)
        title_patterns = [
            r'^\s*classwork\s*8',
            r'^\s*cw\s*8\b',
            r'^\s*class\s*work\s*8',
            r'^\s*in.?class\s*8'
        ]
        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["title"] = True
                evidence.append("Title found")
                break
        if not elements_found["title"]:
            evidence.append("Title NOT found")

        # STEP 3 — Task description (strict)
        if re.search(r'task|assignment|instructions?|question\s*:|state\s+the\s+problem|research\s+question|statistical\s+method', text_lower):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # STEP 4 — Autoformatting (no bullet points)
        autoformat_violations = len(re.findall(r'^\s*[-•*]\s', student_answer, re.MULTILINE))
        bold_violations = len(re.findall(r'\*\*|__', student_answer))
        if autoformat_violations <= 2 and bold_violations <= 2:
            elements_found["autoformatting"] = True
            evidence.append("No excessive autoformatting detected")
        else:
            evidence.append(f"Autoformatting detected: {autoformat_violations} bullets, {bold_violations} bold markers")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear formatting indicators found"]
        }

    def grade_question_cw8_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 8_1: Paired t-test.
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
                            "title": True,
                            "task_description": True,
                            "autoformatting": True,
                        },
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        prompt = f"""You are grading a statistics classwork assignment using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
Students must state the problem, formulate a research question, name the statistical method, and explain why this method is suitable based on research design.

Total: 20 points.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. For components 2-5: ONLY scores 4, 2, or 0 are allowed. Score of 3 is FORBIDDEN.
3. Award 1 point minimum for ANY attempt (even if wrong), 0 only if completely blank
4. Feedback should be SHORT, written as a teacher's comment
5. Feedback CANNOT be an invitation for further discussion
6. For 2-point answers, use encouraging language: "Credit for trying, but..."

---

**RUBRIC:**

**Component 1: Formatting (4 points total)**
- Student name present: 1 point
- Paper title present (e.g., "Class Work 8 Repeated Measures"): 1 point
- Task description copied correctly from assignment: 1 point
- No autoformatting: 1 point

**Component 2: Problem Statement (4 points)**
STEP 1 — Search the student answer for this exact phrase or its direct paraphrase: "we do not know whether there are any differences between the lunar cycle". If found, award 4 points immediately. Do not evaluate further. Do not write any critique.

- Award 4 points if the student identifies a research gap related to the lunar cycle and dementia — even if wording differs from the example.
- Only award 2 if the student states a conclusion instead of a gap.
- Completely blank: 0 points

Example of a 4-point answer: "We do not know whether there are any differences between the lunar cycle (full moon days) and normal days in human behavior, especially in the behavior of dementia patients."
Example of a 2-point answer: "The full moon affects dementia patients negatively." — This is a conclusion, not a research gap.

**Component 3: Research Question (4 points)**
IMPORTANT: If the answer matches or closely matches the example below, you MUST award 4 points.
- Phrased as a clear question with question mark, references lunar cycle and dementia patients, and includes directionality word (e.g. "any") that allows to determine one- or two-tailed hypothesis: 4 points
Example of a full-score answer: "Does the frequency of the Lunar cycle compare to the normal days has any impact on the behavior of the dementia patients?"
- Present but weakly formulated: 2 points
- Completely blank: 0 points

**Component 4: Statistical Method Named (4 points)**
- Correctly names paired sample t-test (or dependent samples t-test): 4 points
- Names a related but imprecise method: 2 points
- Attempted but incorrect: 1 point
- Completely blank: 0 points

**Component 5: Justification Based on Research Design (4 points)**
- Explains paired/dependent design AND links it to the method: 4 points
- Mentions paired design but weak link to method: 2 points
- Attempted but justification is unclear or irrelevant: 1 point
- Completely blank: 0 points

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. For components 2-5: ONLY scores 4, 2, 1, or 0 are allowed.
3. You MUST choose strictly from {4, 2, 1, 0}. Other score (3) is invalid.
4. If the answer is not blank but totally wrong, you MUST assign 1. Use 2 for partially correct, 4 for fully correct. Use 0 only if completely blank.
5. Feedback should be SHORT, written as a teacher's comment
6. Feedback CANNOT be an invitation for further discussion
7. For 1-point answer, use encouraging language: "Credit for trying, but..."

**CORRECT ANSWER GUIDANCE:**

Problem Statement:
We do not know whether there are any differences between the lunar cycle (full moon days) and normal days in human behavior, especially in the behavior of dementia patients.

Research Question: 
Does the frequency of the lunar cycle have any impact on the behavior of dementia patients?

Research Question:
Do college students with insomnia report higher sleep quality scores after completing a 4-week sleep intervention compared to before the intervention?

Statistical Method:
Paired sample t-test

Justification:
Because we have the paired design for the same participants, we use the paired t-test; the samples are dependent by design.

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
                "element_check": element_check
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
        """Display grading results using OutputFormatter."""

        component_labels = {
            "component_1_score": "Formatting (Name/Title/Task/Autoformat)",
            "component_2_score": "Problem Statement",
            "component_3_score": "Research Question",
            "component_4_score": "Statistical Method",
            "component_5_score": "Justification",
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
            "component_4_score": "HYBRID",
            "component_5_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 4,
            "component_2_score": 4,
            "component_3_score": 4,
            "component_4_score": 4,
            "component_5_score": 4,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="CW8_1",
            question_description="Paired t-test: Problem / RQ / Method / Justification",
            component_labels=component_labels,
            max_score=4,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="STRICT"
        )

