"""
question3_1_central_tendency_evaluator.py
Mean, Median, Mode by Gender (GPA & IQ)
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter


class CW3_1Evaluator(BaseEvaluator):
    """
    Evaluator for Central Tendency (Mean, Median, Mode) split by gender.

    Evaluates student's understanding of these three central tendency measures
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
            "name": False,
            "title": False,
            "task_description": False,
            "autoformatting": False,
        }

        evidence = []

        # STEP 1 - Check for student name (strict)
        name_patterns = [
            r'name\s*:\s*[A-Z][a-z]+',
            r'student\s*:\s*[A-Z][a-z]+',
            r'by\s+[A-Z][a-z]+',
            r'^[A-Z][a-z]+\s+[A-Z][a-z]+'
        ]
        for pattern in name_patterns:
            if re.search(pattern, student_answer):
                elements_found["name"] = True
                evidence.append("Name found")
                break
            if not elements_found["name"]:
                evidence.append("Name NOT found")

        # STEP 2 - Check for paper title
        title_patterns = [
            r'classwork\s*3',
            r'homework\s*3',
            r'hw\s*3',
            r'exercise\s*3',
            r'assignment\s*3'
        ]
        for pattern in title_patterns:
            if re.search(pattern, text_lower):
                elements_found["title"] = True
                evidence.append("Title found")
                break
            if not elements_found["title"]:
                evidence.append("Title NOT found")

        # STEP 3 - Check for task statement
        task_keywords = [
            r'central limit theorem',
            r'clt',
            r'standard error',
            r'sample size',
            r'sample mean'
        ]
        task_keyword_count = sum(1 for pattern in task_keywords if re.search(pattern, text_lower))
        if task_keyword_count >= 2:
            elements_found["task_description"] = True
            evidence.append(f"Task description found {task_keyword_count} task keywords")
        else:
            evidence.append("Task description NOT found")

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

        # STEP 4 — Autoformatting (no bullet points, no excessive bold/headers)
        autoformat_violations = len(re.findall(r'^\s*[-•*]\s', student_answer, re.MULTILINE))
        bold_violations = len(re.findall(r'\*\*|__', student_answer))
        if autoformat_violations <= 2 and bold_violations <= 2:
            elements_found["autoformatting"] = True
            evidence.append("No excessive autoformatting detected")
        else:
            evidence.append(
                f"Autoformatting detected: {autoformat_violations} bullets, {bold_violations} bold markers")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

        # checks = {
        #     "mean": bool(re.search(r"\bmean\b", text)),
        #     "median": bool(re.search(r"\bmedian\b", text)),
        #     "mode": bool(re.search(r"\bmode\b", text)),
        #     "gpa": bool(re.search(r"\bgpa\b", text)),
        #     "iq": bool(re.search(r"\biq\b", text)),
        #     "gender_split": bool(re.search(r"\bmale\b|\bfemale\b", text))
        # }

        # return {
        #     "checks": checks,
        #     "all_present": all(checks.values())
        # }

    # def check_intro_phrase_position(self, student_answer: str) -> dict:
    #     """
    #     Check if an introductory phrase appears BEFORE any table/data.
    #     Returns whether intro phrase is present and correctly positioned.
    #     """
    #     text = student_answer.strip()
    #
    #     # Look for table reference patterns
    #     table_ref_patterns = [
    #         r'table\s+\d+\s+presents',
    #         r'table\s+\d+\s+shows',
    #         r'as\s+shown\s+in\s+table\s+\d+',
    #         r'see\s+table\s+\d+'
    #     ]
    #
    #     # Look for table start markers (common patterns)
    #     table_markers = [
    #         r'\t',  # Tab character (tables often have tabs)
    #         r'male\s+female',  # Gender columns
    #         r'iq\s+gpa',  # Column headers
    #         r'\|\s+',  # Pipe separators
    #     ]
    #
    #     intro_phrase_pos = -1
    #     table_start_pos = -1
    #
    #     # Find first intro phrase position
    #     for pattern in table_ref_patterns:
    #         match = re.search(pattern, text.lower())
    #         if match:
    #             intro_phrase_pos = match.start()
    #             break
    #
    #     # Find first table marker position
    #     for pattern in table_markers:
    #         match = re.search(pattern, text)
    #         if match:
    #             table_start_pos = match.start()
    #             break
    #
    #     has_intro_phrase = intro_phrase_pos != -1
    #     intro_before_table = False
    #
    #     if has_intro_phrase and table_start_pos != -1:
    #         intro_before_table = intro_phrase_pos < table_start_pos
    #     elif has_intro_phrase and table_start_pos == -1:
    #         # Has intro phrase but no clear table marker - assume acceptable
    #         intro_before_table = True
    #
    #     return {
    #         "has_intro_phrase": has_intro_phrase,
    #         "intro_before_table": intro_before_table,
    #         "intro_phrase_position": intro_phrase_pos,
    #         "table_start_position": table_start_pos
    #     }

    def grade_question_cw3_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 3.1: Mean, Median, Mode by Gender.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """
        # Test mode for verification without API
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 4,
                    "component_2_score": 4,
                    "component_3_score": 4,
                    "component_4_score": 4,
                    "component_5_score": 4
                },
                max_points=20,
                feedback="Excellent work calculating and interpreting mean, median, and mode for GPA and IQ split by gender.",
                vibe="Strong and confident use of descriptive statistics in JASP",
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
        # formatting_check = self.check_formatting_elements(student_answer)
        # formatting_summary = formatting_check["elements_found"]
        # stat_check = self.check_required_elements(student_answer)
        # intro_check = self.check_intro_phrase_position(student_answer)

        prompt = f"""You are grading a statistics assignment using a **HYBRID grading approach with originality checking**.

        **TASK DESCRIPTION (20 points):**
        Students must calculate mean, median, and mode for GPA and IQ variables split by gender,
        present results in a properly formatted APA table, and introduce it correctly.
        
        Expected table structure (both variables, both genders):
                 GPA              IQ
                 Male   Female    Male    Female
        Mode     ...    ...       ...     ...
        Median   ...    ...       ...     ...
        Mean     ...    ...       ...     ...

        Total: 20 points.
        
        **IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Reasoning is required; no calculations are necessary
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

**RUBRIC:**
        
Component 1: Formatting (4 points total)
- Student name present: 1 point
- Paper title present (e.g., "Classwork 5"): 1 point
- Task is copied correctly from assignment: 1 point
- No autoformatting: 1 point

Component 2: Table 1 Formatting (4 points total)     
- Introductory phrase present (e.g., "Table 1 presents the mean, median, and mode...")
- Reference to table number in introductory phrase (e.g., "...as shown in Table 1")
- Table number present (e.g., "Table 1")
- Table title present and descriptive (e.g., "Mean, Median, and Mode of GPA and IQ by Gender")

Component 3: Mean (4 points total)
Evaluate whether mean is reported for BOTH GPA and IQ, split by BOTH Male and Female:
- 4 points: Both GPA and IQ present, both split by Male and Female correctly
- 3 points: Both variables present but gender split missing or incomplete for one of them
- 2 points: Only one variable present with correct gender split, OR both variables present but no gender split
- 1 point: Mean mentioned but neither variable split nor gender split is clear
- 0 points: Mean absent entirely

**Component 4: Median (4 points total)
Evaluate whether median is reported for BOTH GPA and IQ, split by BOTH Male and Female:
- 4 points: Both GPA and IQ present, both split by Male and Female correctly
- 3 points: Both variables present but gender split missing or incomplete for one of them
- 2 points: Only one variable present with correct gender split, OR both variables present but no gender split
- 1 point: Median mentioned but neither variable split nor gender split is clear
- 0 points: Median absent entirely

Component 5: Mode (4 points total)
Evaluate whether mode is reported for BOTH GPA and IQ, split by BOTH Male and Female:
- 4 points: Both GPA and IQ present, both split by Male and Female correctly
- 3 points: Both variables present but gender split missing or incomplete for one of them
- 2 points: Only one variable present with correct gender split, OR both variables present but no gender split
- 1 point: Mode mentioned but neither variable split nor gender split is clear
- 0 points: Mode absent entirely

STUDENT ANSWER:
{student_answer}

Return grading in this exact JSON format:
{{
  "component_1_score": <0-4>,
  "component_1_explanation": "<brief explanation for task setup>",
  "component_2_score": <0-4>,
  "component_2_explanation": "<if score < 4: one sentence explaining what's missing; if score = 4 AND extra good work: one sentence of praise; otherwise empty string>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<if score < 4: one sentence explaining what's missing; if score = 4 AND extra good work: one sentence of praise; otherwise empty string>",
  "component_4_score": <0-4>,
  "component_4_explanation": "<if score < 4: one sentence explaining what's missing; if score = 4 AND extra good work: one sentence of praise; otherwise empty string>",
  "component_5_score": <0-4>,
  "component_5_explanation": "<if score < 4: one sentence explaining what's missing; if score = 4 AND extra good work: one sentence of praise; otherwise empty string>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment, not an invitation for further discussion>",
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
                "component_3_score",
                "component_4_score",
                "component_5_score",
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
            "component_1_score": "Component 1 (Document formatting)",
            "component_2_score": "Component 2 (Table 1 formatting)",
            "component_3_score": "Component 3 (Mean - GPA and IQ by gender)",
            "component_4_score": "Component 4 (Median - GPA and IQ by gender)",
            "component_5_score": "Component 5 (Mode - GPA and IQ by gender)"
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT",
            "component_5_score": "STRICT"
        }

        max_scores = {
            "component_1_score": 4,
            "component_2_score": 4,
            "component_3_score": 4,
            "component_4_score": 4,
            "component_5_score": 4
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 3_1",
            question_description="Central Tendency - Mean, Median, Mode by Gender",
            component_labels=component_labels,
            max_score=4,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )
