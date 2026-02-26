"""
question5_1_evaluator.py
Central Limit Theorem - Standard Error True/False Question
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter


class Question5_1Evaluator(BaseEvaluator):
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
            max_tokens=1500
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

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check if required elements are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "has_student_name": False,
            "has_paper_title": False,
            "has_task_statement": False,
            "has_explicit_answer": False,
            "has_reasoning": False
        }

        evidence = []

        # Check for student name
        name_patterns = [
            r'name\s*:\s*[A-Z][a-z]+',
            r'student\s*:\s*[A-Z][a-z]+',
            r'by\s+[A-Z][a-z]+',
            r'^[A-Z][a-z]+\s+[A-Z][a-z]+'
        ]
        for pattern in name_patterns:
            if re.search(pattern, student_answer):
                elements_found["has_student_name"] = True
                evidence.append(f"Found name pattern")
                break

        # Check for paper title
        title_patterns = [
            r'classwork\s*5',
            r'homework\s*5',
            r'hw\s*5',
            r'exercise\s*5',
            r'assignment\s*5'
        ]
        for pattern in title_patterns:
            if re.search(pattern, text_lower):
                elements_found["has_paper_title"] = True
                evidence.append(f"Found title pattern")
                break

        # Check for task statement
        task_keywords = [
            r'central limit theorem',
            r'clt',
            r'standard error',
            r'sample size',
            r'sample mean'
        ]
        task_keyword_count = sum(1 for pattern in task_keywords if re.search(pattern, text_lower))
        if task_keyword_count >= 2:
            elements_found["has_task_statement"] = True
            evidence.append(f"Found {task_keyword_count} task keywords")

        # Check for explicit True/False answer
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

    def grade_question5_1_answer(self, student_answer: str, test_mode: bool = False):
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
                            "has_student_name": True,
                            "has_paper_title": True,
                            "has_task_statement": True,
                            "has_explicit_answer": True,
                            "has_reasoning": True
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

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Reasoning is required; no calculations are necessary
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. Award partial credit where reasoning is mostly correct but incomplete

**RUBRIC:**

Component 1: Task Setup (3 points total)
- Student name present: 1 point
- Paper title present (e.g., "Classwork 5", "Homework 5"): 1 point
- Task is copied correctly from assignment: 1 point

Component 2: Reasoning (17 points total)
- Question answered (True/False with explicit conclusion): 5 points
- Reasoning is relevant to question and demonstrates understanding of CLT: 5 points
- Reasoning is complete, logical, and clearly explained: 3 points
- Vibe/partial credit for mostly correct but incomplete reasoning: 4 points

**TYPICAL MISTAKES AND PENALTIES:**
- No explicit True/False conclusion: −5 points from Component 2
- Irrelevant or incorrect reasoning: up to −10 points from Component 2

**CORRECT ANSWER GUIDANCE:**
The statement is TRUE. Standard error = σ/√n, so as n increases, SE decreases.

STUDENT ANSWER:
{student_answer}

Return grading in this exact JSON format:
{{
  "component_1_score": <0-3>,
  "component_1_explanation": "<brief explanation for task setup>",
  "component_2_score": <0-17>,
  "component_2_explanation": "<brief explanation for reasoning>",
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
                "component_2_score"
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """
        Display grading results using OutputFormatter.

        Args:
            grading: Grading result dictionary
        """
        # Check if evaluation was stopped due to originality
        if grading.get("evaluation_stopped", False):
            self.formatter.print_section_header(
                "QUESTION 5_1",
                "Central Limit Theorem - Standard Error True/False",
                width=60
            )
            print("\n" + "=" * 60)
            print("⚠️  ORIGINALITY CONCERN DETECTED")
            print("=" * 60)
            print(f"\nAssessment: {grading['originality_check']['assessment']}")
            if grading['originality_check']['suspicious_patterns']:
                print(f"Suspicious patterns: {grading['originality_check']['suspicious_patterns']}")
            print(f"\n{grading['feedback']}")
            print(f"\nScore: {grading['total_points']}/{grading['max_points']} (0%)")
            print("=" * 60 + "\n")
            return

        component_labels = {
            "component_1_score": "Task Setup (Name/Title/Task)",
            "component_2_score": "Reasoning (Answer/Logic/Clarity)"
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID"
        }

        # Define max scores for each component
        max_scores = {
            "component_1_score": 3,
            "component_2_score": 17
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
            mode="STRICT"
        )