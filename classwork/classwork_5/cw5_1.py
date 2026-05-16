"""
cw5_1_evaluator.py
Central Limit Theorem - Standard Error True/False Question
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter


class CW5_1Evaluator(BaseEvaluator):
    """
    Evaluator for Central Limit Theorem True/False Question.

    Evaluates student's understanding of how sample size affects standard error
    according to the central limit theorem.

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    def __init__(self):
        """Initialize evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1200
        )
        # Initialize output formatter
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
        """
           Check formatting elements in the student's answer.

           Args:
               student_answer: The student's response text

           Returns:
               Dictionary with elements_found (dict of bools) and evidence (list of str)
       """

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

        # title patterns for classwork 5
        title_patterns = [
            r'^\s*final\s*exam\s*(variant\s*)?2\b',
            r'^\s*fin\s*v?\b',
            r'^\s*class\s*work\s*(week\s*)?5\b',
            r'^\s*in.?class\s*5\b'
        ]

        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["paper_title"] = True
                evidence.append("Title found")
                break

        if not elements_found["paper_title"]:
            evidence.append("Title NOT found")

        # pedagogical marker for task description
        pedagogical_markers = [
            "true or false?",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # autoformatting
        # catches bullet points: - item, • item, * item
        autoformat_violations = len(re.findall(r'^\s*[-•*]\s', student_answer, re.MULTILINE))
        print(f"DEBUG autoformat_violations: {autoformat_violations}")
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

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check if required elements are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        evidence = []

        elements_found = {
            "has_explicit_answer": False,
            "has_reasoning": False,
        }

        answer_patterns = [
            r'\btrue\b',
            r'\bfalse\b',
            r'\bcorrect\b',
            r'\bincorrect\b'
        ]
        for pattern in answer_patterns:
            if re.search(pattern, text_lower):
                elements_found["has_explicit_answer"] = True
                evidence.append(f"Found answer indicator")
                break

        # Check for reasoning
        reasoning_indicators = [
            r'\bbecause\b',
            r'\bsince\b',
            r'\bas\b.*\bincreases\b',
            r'\bformula\b',
            r'\bse\b.*=',
            r'σ',
            r'\bsqrt\b',
            r'√',
            r'\bn\b.*\bincreases\b'
        ]
        reasoning_count = sum(1 for pattern in reasoning_indicators if re.search(pattern, text_lower))
        if reasoning_count >= 2 or len(student_answer) > 100:
            elements_found["has_reasoning"] = True
            evidence.append(f"Found {reasoning_count} reasoning indicators")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_question_cw5_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 5.1: Central Limit Theorem True/False Question.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        # Test mode for verification without API
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 3,
                    "component_2_score": 17,
                },
                max_points=20,
                feedback="[TEST MODE] Excellent understanding of CLT and standard error.",
                vibe="Student demonstrates clear grasp of central limit theorem concepts",
                additional_data={
                    "originality_check": {
                        "is_suspicious": False,
                        "assessment": "Appears original"
                    },
                    "element_check": {
                        "elements_found": {
                            "name": False,
                            "title": False,
                            "task_description": False,
                            "autoformatting": False,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        # Check originality first
        originality_check = self.check_originality(student_answer)

        # If originality concern detected, return 0 with freeze message
        if originality_check["is_suspicious"]:
            return {
                "component_1_score": 0,
                "component_1_explanation": "Task setup not evaluated due to originality concern",
                "component_2_score": 0,
                "component_2_explanation": "Reasoning not evaluated due to originality concern",
                "total_points": 0,
                "max_points": 20,
                "percentage": 0.0,
                "feedback": "Due to originality concern, your points are frozen. You can get them back if you provide oral explanation for this paper.",
                "vibe": "Originality concern detected - evaluation stopped",
                "originality_check": originality_check,
                "evaluation_stopped": True
            }

        prompt = f"""You are grading a statistics homework using a **STRICT rubric-based approach** with originality checking.

**TASK DESCRIPTION:**
Students must answer: True or False? According to the central limit theorem, the standard error for a sample mean becomes smaller as the sample size increases.

Total: 20 points.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Reasoning is required; no calculations are necessary
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

**RUBRIC:**

**Component 1: Formatting (4 points total)**
- Student name present: 1 point
- Paper title present (e.g., "Classwork 5"): 1 point
- Task is copied correctly from assignment: 1 point
- No autoformatting: 1 point

**Component 2: Direct Answer (8 points total)**
- Explicit True/False answer present: 8 points
- No answer present: 0 points

**TYPICAL MISTAKES AND PENALTIES:**
- No explicit True/False conclusion: −5 points from Component 2
- Irrelevant or incorrect reasoning: up to −10 points from Component 2

Component 3: Explanation (8 points total)
- Reasoning references SE = σ/√n or equivalent logic: 4 points
- Reasoning is complete, logical, and clearly explained: 4 points

**CORRECT ANSWER GUIDANCE:**
The statement is TRUE. Standard error = σ/√n, so as n increases, SE decreases.

STUDENT ANSWER:
{student_answer}

Return grading in this exact JSON format:
{{
  "component_1_score": <0-4>,
  "component_1_explanation": "<brief explanation for task setup>",
  "component_2_score": <0-8>,
  "component_2_explanation": "<brief explanation for direct answer>",
  "component_3_score": <0-8>,
  "component_3_explanation": "<brief explanation for explanation quality>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression>"
}}"""

        # Check for required elements
        element_check = self.check_required_elements(student_answer)

        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "originality_check": originality_check,
                "element_check": element_check
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
        """
        Display grading results using OutputFormatter.

        Args:
            grading: Grading result dictionary
        """
        component_labels = {
            "component_1_score": "Task Setup (Name/Title/Task/Formatting)",
            "component_2_score": "Direct Answer (True/False)",
            "component_3_score": "Explanation (Reasoning Quality)"
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID"
        }

        # Define max scores for each component
        max_scores = {
            "component_1_score": 4,
            "component_2_score": 8,
            "component_3_score": 8
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 5_1",
            question_description="Central Limit Theorem - Standard Error True/False",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )
