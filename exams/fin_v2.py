"""
fin_v2.py
Final Exam Variant 2: Mean, Median, and Distribution Shape
Evaluation method name: def grade_question_fin_v2_answer
"""
import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter

class FIN_V2_1Evaluator(BaseEvaluator):
    """
    Evaluator for Final Exam Variant 2.

    Task:
    Let’s assume the distribution is unimodal.  If the mean time to respond to a stimulus is much lower than the median time to respond, what can you say about the shape of the distribution of response times? Will your answer be the same if distribution is not unimodal?

    Formatting: 4 points (name 1pt, title 1pt, task description 1pt, no autoformatting 1pt).
    Total: 20 points.
    """

    def __init__(self):
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1200
        )
        self.formatter = OutputFormatter(default_width=60)

    def check_originality(self, student_answer: str) -> dict:
        """
        Check for potential AI-generated or copied text.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with originality assessment
        """
        text_lower = student_answer.lower()

        # Common AI text indicators
        ai_phrases = [
            r'as an ai',
            r'i don\'t have',
            r'i cannot',
            r'my knowledge cutoff',
            r'i\'m sorry, but',
            r'i apologize',
            r'as a language model',
            r'i\'m trained',
            r'according to my training'
        ]

        # Generic/template phrases
        template_phrases = [
            r'lorem ipsum',
            r'this is a sample',
            r'example answer',
            r'\[insert.*here\]'
        ]

        # Overly formal academic phrases
        formal_phrases = [
            r'it\'s important to note that',
            r'it is worth noting',
            r'in conclusion, it can be said'
        ]

        suspicious_patterns = []

        for pattern in ai_phrases + template_phrases + formal_phrases:
            if re.search(pattern, text_lower):
                suspicious_patterns.append(pattern)

        # Check for excessive formal transitions
        formal_indicators = len(re.findall(
            r'\b(thus|therefore|furthermore|moreover|consequently|hence)\b',
            text_lower
        ))

        is_suspicious = len(suspicious_patterns) > 0 or formal_indicators > 5

        return {
            "is_suspicious": is_suspicious,
            "suspicious_patterns": suspicious_patterns,
            "formal_indicator_count": formal_indicators,
            "assessment": "Potential originality concern" if is_suspicious else "Appears original"
        }

    def check_formatting_elements(self, student_answer: str) -> dict:
        text_lower = student_answer.lower()
        first_lines = student_answer[:200]

        elements_found = {
            "student_name": False,
            "paper_title": False,
            "task_description": False,
            "autoformatting": False,
        }

        evidence = []

        # isolated LLM call for name detection
        first_two_lines = "\n".join(student_answer.strip().splitlines()[:2])
        name_check = self.grade_with_prompt(
            student_answer=first_two_lines,
            prompt=f"""Does the following text contain a student name?
        A valid student name is exactly two words, each starting with a capital letter,
        like "John Doe". It must not be a title, heading, or course-related phrase.

        Text: {first_two_lines}

        Return JSON only:
        {{
          "student_name_present": <true/false>,
          "evidence": "<one phrase you found or 'none'>"
        }}"""
        )
        if name_check.get("student_name_present") is True:
            elements_found["student_name"] = True
            evidence.append(f"Name found: {name_check.get('evidence', '')}")
        else:
            evidence.append("Name NOT found")

        # Title patterns for Final Exam Variant 2
        title_patterns = [
            r'^\s*final\s*exam\s*(variant\s*)?2\b',
            r'^\s*fin\s*v?\.?\s*2\b',
            r'^\s*final\s*2\b',
            r'^\s*variant\s*2\b',
        ]

        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["paper_title"] = True
                evidence.append("Title found")
                break

        if not elements_found["paper_title"]:
            evidence.append("Title NOT found")

        # pedagogical markers for task description
        pedagogical_markers = [
            "what can you say",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # autoformatting

        # catches bullet points: - item, • item, * item
        autoformat_violations = len(re.findall(r'^\s*[-•*]\s', student_answer, re.MULTILINE))

        # catches numbered headings without bullets: Step 1:, Task 2., Question 3)
        step_violations = len(re.findall(r'^\s*\w+\s+\d+[:\.\)]\s*$', student_answer, re.MULTILINE))

        if autoformat_violations > 0 or step_violations >= 2:
            evidence.append("Autoformatting detected")
        else:
            elements_found["autoformatting"] = True
            evidence.append("No autoformatting detected")

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def check_required_elements(self, student_answer: str) -> dict://TODO: implement

    def grade_question_fin_v2_answer(self, student_answer: str):

        formatting_check = self.check_formatting_elements(student_answer)
        formatting_summary = formatting_check["elements_found"]

        formatting_block = f"""
HEADER DETECTION RESULTS (DO NOT RE-EVALUATE):

paper_title_present = {formatting_summary["paper_title"]}
task_description_present = {formatting_summary["task_description"]}
no_autoformatting_present = {formatting_summary["autoformatting"]}
"""

        prompt = f"""{formatting_block}

You are grading a statistics final exam paper.

TASK:

"Mean, Median, Symmetry, and Unimodality"

Use STRICT rubric-based grading. Total score MUST be exactly 20 points.

---

**RUBRIC**

Component 1: Formatting (4 points)
Start with 4 points.

Step 1 Name (1 point)
- Valid name = two capitalized words like John Doe
- Must appear in first two lines before any content

Step 2 Title (1 point)
Use paper_title_present

Step 3 Task description (1 point)
Use task_description_present

Step 4 No autoformatting (1 point)
Use no_autoformatting_present

Component 2: Symmetry Statement (14 points)
The student must include the following statement verbatim or near-verbatim:
"If the mean time to respond to a stimulus is equal to the median time to respond,
it indicates that the distribution of response times is symmetric."

Grading scale:
- 14 points: Statement fully present and correctly interpreted (explains WHY equal mean and median
  implies symmetry, e.g. no skew, balanced tails, mirror image around center).
- 7 points: Statement partially present or heavily paraphrased, with some correct interpretation.
- 0 points: Absent or completely unrelated.

Component 3: Unimodality Statement (2 points)
The student must include the following statement verbatim or near-verbatim:
"In a unimodal distribution, where there is only one peak, the equality of mean and median
suggests that the data is evenly distributed around the center."

Grading scale:
- 2 points: Statement fully present and correctly interpreted.
- 1 point: Statement partially present or interpretation is missing/incorrect.
- 0 points: Absent.

---

EXAMPLE OF A COMPLETE ANSWER

John Doe
Final Exam Variant 1

If the mean time to respond to a stimulus is equal to the median time to respond, it indicates that the distribution of response times is symmetric.

In a unimodal distribution, where there is only one peak, the equality of mean and median suggests that the data is evenly distributed around the center.

---

ORIGINALITY CHECK:
IMPORTANT: The two required statements (symmetry and unimodality) are assigned text and must be
excluded from originality concerns.
Evaluate ONLY the student's own interpretations and elaborations.
If the student's own writing (beyond the required statements) appears AI-generated or generic,
set all scores to 0 and set feedback to EXACTLY:
"Due to originality concern, your points are frozen. You can get them back if you provide oral explanation for this paper."

STUDENT ANSWER:
{student_answer}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-4>,
  "component_1_name_score": <0-1>,
  "component_1_title_score": <0-1>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-14>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-2>,
  "component_3_explanation": "<brief>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <number>,
  "feedback": "<short teacher comment>",
  "vibe": "<one sentence overall impression>"
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
        """Display grading results using OutputFormatter.

        Args:
            grading: Grading result dictionary
        """
        component_labels = {
            "component_1_score": "Formatting (Name/Title/Task/Autoformatting)",
            "component_2_score": "Symmetry Statement",
            "component_3_score": "Unimodality Statement",
        }

        component_types = {
            "component_1_score": "HYBRID",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 4,
            "component_2_score": 14,
            "component_3_score": 2,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="FIN_V2_1",
            question_description="Final Exam Variant 2 - Mean, Median, Symmetry, and Unimodality",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )
