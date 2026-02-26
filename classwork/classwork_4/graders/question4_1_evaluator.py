"""
question4_1_evaluator.py
Multiple Comparisons Error Probability Calculation
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter


class Question4_1Evaluator(BaseEvaluator):
    """
    Evaluator for Multiple Comparisons Probability Question.

    Evaluates student's calculation of the probability of making at least one
    Type I error when performing multiple independent statistical comparisons.

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

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check if required elements (problem setup, formula, calculation, probability) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "identifies_six_comparisons": False,
            "mentions_error_rate": False,
            "shows_formula": False,
            "shows_calculation": False,
            "states_final_probability": False
        }

        evidence = []

        # Check for identification of 6 comparisons
        comparison_patterns = [r'\bsix\b', r'\b6\b.*\bcomparison', r'\b6\b.*\btest']
        for pattern in comparison_patterns:
            if re.search(pattern, text_lower):
                elements_found["identifies_six_comparisons"] = True
                evidence.append(f"Found comparison identifier: {pattern}")
                break

        # Check for error rate mention
        error_patterns = [r'\b5\s*%\b', r'\b0\.05\b', r'\balpha\b', r'\berror rate\b']
        for pattern in error_patterns:
            if re.search(pattern, text_lower):
                elements_found["mentions_error_rate"] = True
                evidence.append(f"Found error rate indicator: {pattern}")
                break

        # Check for formula
        formula_patterns = [r'\b1\s*-', r'\bcomplement\b', r'\^', r'\*\*']
        for pattern in formula_patterns:
            if re.search(pattern, student_answer):
                elements_found["shows_formula"] = True
                evidence.append(f"Found formula indicator: {pattern}")
                break

        # Check for calculation steps
        calculation_patterns = [r'\b0\.95\b', r'\b0\.73', r'\bcalculat', r'\=']
        for pattern in calculation_patterns:
            if re.search(pattern, text_lower):
                elements_found["shows_calculation"] = True
                evidence.append(f"Found calculation indicator: {pattern}")
                break

        # Check for final probability statement
        probability_patterns = [r'\b0\.26', r'\b0\.27', r'\b26\s*%', r'\b27\s*%', r'\bprobability\b']
        for pattern in probability_patterns:
            if re.search(pattern, text_lower):
                elements_found["states_final_probability"] = True
                evidence.append(f"Found probability statement: {pattern}")
                break

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_question4_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 4.1: Multiple Comparisons Error Probability Calculation.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        # Test mode for verification without API
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 10,
                    "component_2_score": 10,
                    "component_3_score": 10,
                    "component_4_score": 10,
                },
                max_points=40,
                feedback="[TEST MODE] Excellent understanding of probability calculations.",
                vibe="Student demonstrates strong grasp of familywise error rate and probability concepts",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "identifies_six_comparisons": True,
                            "mentions_error_rate": True,
                            "shows_formula": True,
                            "shows_calculation": True,
                            "states_final_probability": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Students must solve: A researcher wants to compare the mean anxiety levels across four therapy groups: CBT, psychoanalysis, anxiolytics, and control. They plan to perform six separate comparisons between the groups. If the chance of making a mistake in one comparison is 5%, and the comparisons are independent, what is the probability of making at least one mistake across all six?

Components:
1. Problem Understanding (10 points)
2. Formula/Approach (10 points)
3. Calculations (10 points)
4. Interpretation (10 points)

Total: 40 points

STUDENT ANSWER:
{student_answer}

**HYBRID GRADING APPROACH:**
- Components 2 and 3 are STRICT: formula and calculations
- Components 1 and 4 are VIBE: holistic assessment
- Full points if correct; praise for extra insights

Return grading in this exact JSON format:
{{
  "component_1_score": <0-10>,
  "component_1_explanation": "",
  "component_2_score": <0-10>,
  "component_2_explanation": "",
  "component_3_score": <0-10>,
  "component_3_explanation": "",
  "component_4_score": <0-10>,
  "component_4_explanation": "",
  "total_points": <0-40>,
  "max_points": 40,
  "percentage": <percentage>,
  "feedback": "<narrative explanation>",
  "vibe": "<one-sentence overall impression>"
}}"""

        # Check for required elements
        element_check = self.check_required_elements(student_answer)

        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"element_check": element_check}
        )

        # If grading succeeded, validate component scores
        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score"
            ]
            result = self.validate_component_scores(result, component_keys, 40)

        return result

    def print_grading_results(self, grading):
        """
        Display grading results using OutputFormatter.

        Args:
            grading: Grading result dictionary
        """
        component_labels = {
            "component_1_score": "Problem Understanding",
            "component_2_score": "Formula/Approach",
            "component_3_score": "Calculations",
            "component_4_score": "Interpretation"
        }

        component_types = {
            "component_1_score": "VIBE",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT",
            "component_4_score": "VIBE"
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 4_1",
            question_description="Multiple Comparisons Error Probability Calculation",
            component_labels=component_labels,
            max_score=10,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )
