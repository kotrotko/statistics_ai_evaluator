"""
cw1_1.py
Classwork 1: File management: Basic skills
General Skills: Mean Formula
Evaluation method name: def grade_question_cw1_1_answer
"""

"""
question1_1_evaluator.py
File Setup + Mean Formula with Equation Tools
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter


class CW1_1Evaluator(BaseEvaluator):
    """
    Evaluator for Question 1_1: File Setup and Mean Formula.

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

    def check_required_columns(self, student_answer: str) -> dict:
        """
        Check if required columns (frequencies, cumulative, percentiles) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found columns and evidence
        """
        text_lower = student_answer.lower()

        columns_found = {
            "accent": False,
            "fraction": False,
            "script": False,
            "radical": False
        }

        evidence = []

        # Check for accent-related terms
        accent_patterns = [r'\baccent\b', r'\bbar\b', r'\bx-bar\b', r'\bx̄\b']
        for pattern in accent_patterns:
            if re.search(pattern, text_lower):
                columns_found["accent"] = True
                evidence.append(f"Found accent indicator: {pattern}")
                break

        # Check for fraction-related terms
        fraction_patterns = [r'\bfraction\b', r'\bdivision\b', r'\bdivide\b']
        for pattern in fraction_patterns:
            if re.search(pattern, text_lower):
                columns_found["fraction"] = True
                evidence.append(f"Found fraction indicator: {pattern}")
                break

        # Check for script-related terms
        script_patterns = [r'\bscript\b', r'\bsubscript\b', r'\bsuperscript\b', r'\bsigma\b', r'\bΣ\b']
        for pattern in script_patterns:
            if re.search(pattern, text_lower):
                columns_found["script"] = True
                evidence.append(f"Found script indicator: {pattern}")
                break

        # Check for radical-related terms
        radical_patterns = [r'\bradical\b', r'\bsquare root\b', r'\bsqrt\b', r'\b√\b']
        for pattern in radical_patterns:
            if re.search(pattern, text_lower):
                columns_found["radical"] = True
                evidence.append(f"Found radical indicator: {pattern}")
                break

        return {
            "columns_found": columns_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(columns_found.values())
        }

    def grade_question_cw1_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 1_1: File setup and mean formula writing.
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
                    "component_3_score": 5,
                    "component_4_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Good formula writing with proper use of equation tools. Minor issues with accent placement.",
                vibe="Student demonstrates solid understanding of Word equation tools",
                additional_data={
                    "column_check": {
                        "columns_found": {"frequency": True, "cumulative": True, "percentile": True},
                        "all_present": True,
                        "evidence": ["Test mode - all columns present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

    **TASK DESCRIPTION:**
    Students must:
    1. Prepare classwork file and save in Google Drive folder named `yournameYourlastname_Statistics` (FILE SETUP - evaluated holistically)
    2. Write the mean formula using Word Equation tool with:
       - Use "Accent" for the bar over x (x̄) (5 points)
       - Use "Fraction" for division (5 points)
       - Use "Script" for subscript and superscript (Σ, n, i) (5 points)
       - Use "Radical" for square root (√) (5 points)
       - Expected formula: x̄ = (Σxᵢ)/√n

    Total: 20 points

    STUDENT ANSWER:
    {student_answer}

    **IMPORTANT NOTES:**
    - Students submit text descriptions of their work since visual elements (actual formatted equations, folder screenshots) cannot be captured in text
    - If student REFERENCES or DESCRIBES the equation elements (e.g., "I used the accent for x-bar", "I added the radical for square root"), ASSUME they completed it in their actual document
    - DO NOT penalize for "missing" visual elements if they clearly describe what they did

    **HYBRID GRADING APPROACH:**

    **Component 1: Accent (x̄) - STRICT (0-5 points)**
    - 5 points: Student correctly used the Accent tool for x̄
    - 4 points: Used Accent with minor issues
    - 2-3 points: Partial or unclear usage
    - 0 points: Did not use Accent tool

    **Component 2: Fraction (division) - STRICT (0-5 points)**
    - 5 points: Student correctly used the Fraction tool for division
    - 4 points: Used Fraction with minor issues
    - 2-3 points: Partial or unclear usage
    - 0 points: Did not use Fraction tool

    **Component 3: Script (subscript/superscript) - STRICT (0-5 points)**
    - 5 points: Student correctly used Script for Σ, subscripts, and superscripts
    - 4 points: Used Script with minor issues
    - 2-3 points: Partial use (only subscript OR only superscript)
    - 0 points: Did not use Script tool

    **Component 4: Radical (√) - STRICT (0-5 points)**
    - 5 points: Student correctly used the Radical tool for √n
    - 4 points: Used Radical with minor issues
    - 2-3 points: Partial or unclear usage
    - 0 points: Did not use Radical tool

    **CRITICAL RULES:**
    1. Each equation component is STRICT - must be present to earn points
    2. If student meets requirements exactly: 5/5 points
    3. If student does extra correct work beyond requirements: 5/5 points + praise in explanation
    4. Minor formatting issues are okay if the tool usage is correct

    **SCORING PROCESS:**
    1. Score Component 1 (Accent): __/5
    2. Score Component 2 (Fraction): __/5
    3. Score Component 3 (Script): __/5
    4. Score Component 4 (Radical): __/5
    5. Total = sum of four scores
    6. Consider file setup in overall feedback/vibe

    **FEEDBACK STRUCTURE:**
    Provide narrative feedback that:
    - Acknowledges what equation elements they successfully used
    - Points out any missing components specifically
    - Comments on file setup if mentioned
    - Explains what would improve their score
    - Remains encouraging and constructive

    Return your grading in this exact JSON format:
    {{
      "component_1_score": <0-5>,
      "component_1_explanation": "<if score < 5: one sentence explaining what's missing or problematic; if score = 5 AND student did good extra work beyond requirements (provided helpful examples, added clear explanations, showed original insight, caught errors): one sentence of praise; otherwise empty string>",
      "component_2_score": <0-5>,
      "component_2_explanation": "<if score < 5: one sentence explaining what's missing or problematic; if score = 5 AND student did good extra work beyond requirements (provided helpful examples, added clear explanations, showed original insight, caught errors): one sentence of praise; otherwise empty string>",
      "component_3_score": <0-5>,
      "component_3_explanation": "<if score < 5: one sentence explaining what's missing or problematic; if score = 5 AND student did good extra work beyond requirements (provided helpful examples, added clear explanations, showed original insight, caught errors): one sentence of praise; otherwise empty string>",
      "component_4_score": <0-5>,
      "component_4_explanation": "<if score < 5: one sentence explaining what's missing or problematic; if score = 5 AND student did good extra work beyond requirements (provided helpful examples, added clear explanations, showed original insight, caught errors): one sentence of praise; otherwise empty string>",
      "total_points": <sum of above, 0-20>,
      "max_points": 20,
      "percentage": <percentage>,
      "feedback": "<narrative explanation - which tools they used well, what's missing, how to improve>",
      "vibe": "<one-sentence overall impression of their equation tool mastery>"
    }}"""
        # Check for required columns
        column_check = self.check_required_columns(student_answer)

        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"column_check": column_check}
        )

        # If grading succeeded, validate component scores
        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score"
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
            "component_1_score": "Component 1 (Accent - x̄)",
            "component_2_score": "Component 2 (Fraction - division)",
            "component_3_score": "Component 3 (Script - Σ, subscripts)",
            "component_4_score": "Component 4 (Radical - √)"
        }

        # Define component types (all STRICT for this question)
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT"
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 1_1",
            question_description="File Setup + Mean Formula",
            component_labels=component_labels,
            max_score=5,
            component_types=component_types,
            check_configs=None,  # No automatic checks for this question
            width=60,
            mode="HYBRID"
        )