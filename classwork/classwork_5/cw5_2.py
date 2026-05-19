"""
cw5_2.py
Classwork 5
Standard Error Calculation Improving Task
Evaluation method name: def grade_question_cw5_2_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2


class CW5_2Evaluator(BaseEvaluator):
    """
    Evaluator for Standard Error Calculation Question.

    Evaluates student's ability to calculate standard error using the formula
    SE = σ / √n with given population parameters.

    Inherits common functionality from BaseEvaluator.
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
            "has_formula": False,
            "has_calculation": False,
            "has_result_statement": False,
            "has_reasoning": False
        }

        evidence = []

        # Check for formula
        formula_patterns = [
            r'se\s*=\s*σ\s*/\s*√n',
            r'se\s*=\s*sigma\s*/\s*sqrt',
            r'σ\s*/\s*√n',
            r'standard error\s*=.*sigma.*sqrt',
            r'se.*formula'
        ]
        for pattern in formula_patterns:
            if re.search(pattern, text_lower):
                elements_found["has_formula"] = True
                evidence.append(f"Found formula pattern")
                break

                # Check for calculation (must show actual computation steps)
                has_computation_step = bool(re.search(r'36\s*/\s*√4|36\s*/\s*2', text_lower))
                has_intermediate_or_final = bool(re.search(r'=\s*18|=\s*36\s*/\s*2', text_lower))

                if has_computation_step and has_intermediate_or_final:
                    elements_found["has_calculation"] = True
                    evidence.append("Found actual calculation steps with computation")
                else:
                    evidence.append("No complete calculation steps found")

        # Check for result statement
        result_patterns = [
            r'standard error.*is.*18',
            r'se\s*=\s*18',
            r'result.*18',
            r'answer.*18',
            r'therefore.*18'
        ]
        for pattern in result_patterns:
            if re.search(pattern, text_lower):
                elements_found["has_result_statement"] = True
                evidence.append(f"Found result statement")
                break

        # Check for reasoning
        reasoning_indicators = [
            r'\bbecause\b',
            r'\bsince\b',
            r'\bclt\b',
            r'central limit theorem',
            r'sample size',
            r'population',
            r'distribution',
            r'\bexplain',
            r'\binterpret'
        ]
        reasoning_count = sum(1 for pattern in reasoning_indicators if re.search(pattern, text_lower))
        if reasoning_count >= 2 or len(student_answer) > 150:
            elements_found["has_reasoning"] = True
            evidence.append(f"Found {reasoning_count} reasoning indicators")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_question_cw5_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 5.2: Standard Error Calculation Question.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        # Test mode for verification without API
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_2_score": 4,
                    "component_3_score": 5,
                    "component_4_score": 4,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Excellent calculation and reasoning for standard error.",
                vibe="Student demonstrates clear understanding of standard error formula and application",
                additional_data={
                    "originality_check": {
                        "is_suspicious": False,
                        "assessment": "Appears original"
                    },
                    "element_check": {
                        "elements_found": {
                            "has_formula": True,
                            "has_calculation": True,
                            "has_result_statement": True,
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

        # Check formatting elements (task description)
        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["how would you like"]
        )

        # Check for required elements
        element_check = self.check_required_elements(student_answer)

        prompt = f"""You are grading a statistics homework using a **hybrid rubric approach**: strict technical scoring, flexible reasoning assessment.

**TASK DESCRIPTION:**
If random samples, each with n = 4 scores, are selected from a normal population with µ = 80 and σ = 36, then what is the standard error for the distribution of sample means? How would you like to improve the problem statement?	Use rubrics Given, Calculation, Answer.

STUDENT ANSWER:
{student_answer}
        
**IMPORTANT NOTES:**
- Students submit text descriptions of their work since visual elements (actual diagrams, screenshots, formatted documents) cannot be captured in text
- If student REFERENCES or DESCRIBES the required elements (e.g., "I used APA format to describe findings", "I inserted the frequency distribution diagram"), ASSUME they completed it in their actual document
- DO NOT penalize for "missing" visual elements if they clearly describe what they did

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Reasoning is required; calculations are mandatory
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. Award partial credit where reasoning is mostly correct but incomplete
6. It is expected to see both student's logic and calculations, not only the final answer
7. Explanations must be SPECIFIC and ACTIONABLE - avoid vague phrases like "lacks depth", "could be better", "needs improvement". Instead, point to what is actually missing or what was done well.

**HYBRID GRADING APPROACH:**

**AUTOMATIC FORMATTING DETECTION RESULT:**
Task description present (1 point if True): {formatting_check['elements_found']['task_description']}
No autoformatting (1 point if True): 
{formatting_check['elements_found']['autoformatting']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC DETECTION:**
{element_check['elements_found']}

**RUBRIC:**

**Component 1: Formatting (2 points)**
Step 1 Task description (1 point)
Use task_description_present.

Step 2 No autoformatting (1 point)
Use autoformatting_present.

**Component 2: Given (0-4 points)**
- 1 point: Population mean (μ = 80) present
- 1 point: Population SD (σ = 36) present
- 2 points: Sample size (n = 4) present

**Component 3: Calculation (0-5 points)**
- 1 point: Word "Calculation" included
- 1 point: Correct formula provided (SE = σ / √n)
- 1 point: Correct values substituted (36 / √4 or equivalent, e.g. 36 / √n = 36 / 2)
- 1 point: Correct calculation result (SE = 18)
- 1 point: Calculation is clearly shown step by step

**Component 4: Answer (0-4 points)**
- 1 point: Word "Answer" included
- 2 points: Answer value stated (SE = 18)
- 1 point: Answer is correct

**Component 5: Correction (0-5 points)**
- 5 points: Meaningful and clearly explained improvement to the problem statement
- 3-4 points: Improvement suggested but explanation is minimal
- 1-2 points: Vague or barely relevant suggestion
- 0 points: Not present

**FEEDBACK RULES:**
- Identify which rubric elements were present (Given, Calculation, Answer, Correction)
- Point out missing elements explicitly
- Encourage interpretation of what standard error tells us about the distribution of sample means
- Maintain supportive tone

Return JSON only:
{{
  "component_1_score": <0-2>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-4>,
  "component_4_explanation": "<brief>",
  "component_5_score": <0-5>,
  "component_5_explanation": "<brief>",
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative feedback>",
  "vibe": "<one-sentence overall impression>"
}}"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"originality_check": originality_check, "formatting_check": formatting_check,
                               "element_check": element_check}
        )

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
        # Define component labels
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Given",
            "component_3_score": "Calculation",
            "component_4_score": "Answer",
            "component_5_score": "Correction",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT",
            "component_5_score": "STRICT",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 4,
            "component_3_score": 5,
            "component_4_score": 4,
            "component_5_score": 5,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 5_2",
            question_description="Standard Error Calculation (Problem Description Improvement)",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )