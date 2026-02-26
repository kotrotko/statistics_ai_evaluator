"""
question5_2_evaluator.py
Standard Error Calculation Question
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter


class Question5_2Evaluator(BaseEvaluator):
    """
    Evaluator for Standard Error Calculation Question.

    Evaluates student's ability to calculate standard error using the formula
    SE = σ / √n with given population parameters.

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
            "has_task_description": False,
            "has_formula": False,
            "has_calculation": False,
            "has_result_statement": False,
            "has_reasoning": False
        }

        evidence = []

        # Check for task description (must be copied with at least 90% accuracy)
        expected_task = "if random samples, each with n = 4 scores, are selected from a normal population with μ = 80 and σ = 36, then what is the standard error for the distribution of sample means? how would you like to improve the problem statement?"

        # Normalize both texts: remove extra spaces, parentheses, normalize whitespace
        normalized_expected = re.sub(r'[^\w\s]', '', expected_task.lower())
        normalized_student = re.sub(r'[^\w\s]', '', text_lower)
        expected_words = normalized_expected.split()
        matched_words = sum(1 for word in expected_words if word in normalized_student)
        match_percentage = (matched_words / len(expected_words)) * 100
        if match_percentage >= 90:
            elements_found["has_task_description"] = True
            evidence.append(f"Task description present ({match_percentage:.1f}% match)")
        else:
            evidence.append(f"Task description missing or incomplete ({match_percentage:.1f}% match, need ≥90%)")

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

    def grade_question_hw5_2_answer(self, student_answer: str, test_mode: bool = False):
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
                    "component_1_score": 5,
                    "component_2_score": 15,
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
                            "has_task_description": True,
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

        # Check for required elements
        element_check = self.check_required_elements(student_answer)

        # Calculate Component 1 score based on strict elements (Python decides, not AI)
        component_1_score = 0
        component_1_breakdown = []

        if element_check['elements_found']['has_task_description']:
            component_1_score += 1
            component_1_breakdown.append("Task description (1pt)")

        if element_check['elements_found']['has_formula']:
            component_1_score += 1
            component_1_breakdown.append("Formula (1pt)")

        if element_check['elements_found']['has_calculation']:
            component_1_score += 2
            component_1_breakdown.append("Calculation (2pts)")

        if element_check['elements_found']['has_result_statement']:
            component_1_score += 1
            component_1_breakdown.append("Result statement (1pt)")

        component_1_explanation = "Found: " + ", ".join(
            component_1_breakdown) if component_1_breakdown else "Missing all required elements"

        prompt = f"""You are grading a statistics homework using a **hybrid rubric approach**: strict technical scoring, flexible reasoning assessment.

        **TASK DESCRIPTION:**
        Students must solve: If random samples, each with n=4 scores, are selected from a normal population with μ=80 and σ=36, then what is the standard error for the distribution of sample means? Include the formula for SE, manual calculation details, and a clear statement of the result.

        **IMPORTANT GRADING RULES:**
        1. Total score MUST be exactly 20 points
        2. Reasoning is required; calculations are mandatory
        3. Feedback should be SHORT, written as a teacher's comment
        4. Feedback CANNOT be an invitation for further discussion
        5. Award partial credit where reasoning is mostly correct but incomplete
        6. It is expected to see both student's logic and calculations, not only the final answer
        7. Explanations must be SPECIFIC and ACTIONABLE - avoid vague phrases like "lacks depth", "could be better", "needs improvement". Instead, point to what is actually missing or what was done well.

        **RUBRIC:**

        Component 1: Task Setup (5 points total) - ALREADY SCORED BY SYSTEM
        The system has detected and scored these elements:
        {component_1_explanation}
        Component 1 Score: {component_1_score}/5

        YOU ONLY GRADE Component 2.

        Component 2: Reasoning Quality (15 points total) - YOUR JOB
        Award points based on what reasoning IS present, not what's missing:

        Base reasoning (0-7 points):
        - 0 pts: No reasoning at all
        - 3 pts: Minimal reasoning attempt (mentions SE but no depth)
        - 5 pts: Solid reasoning (explains SE concept clearly)
        - 7 pts: Strong reasoning (explains SE + connects to CLT or sample size effect)

        Additional insights (0-8 points):
        Award points for ANY of these insights the student provides:
        - Explains why μ=80 doesn't affect SE: +2 pts
        - Discusses how n affects SE: +2 pts
        - Mentions CLT context: +2 pts
        - Suggests improvements to problem statement: +2 pts
        - Any other relevant statistical insight: +2 pts

        YOUR EXPLANATION MUST:
        - State what reasoning IS present (not what's "lacking")
        - If awarding less than full points, name the specific insights that would earn more points
        - Example: "Explained SE clearly (5pts base). Mentioned CLT (+2pts). Did not discuss why μ=80 is irrelevant or how n affects SE."

        **TYPICAL MISTAKES AND PENALTIES:**
        - Formula missing or calculation wrong: deduct points from Component 1
        - Irrelevant or incorrect reasoning: deduct points from Component 2
        - Only final answer without calculation steps: −2 points from Component 1
        - No reasoning provided: 0 points for Component 2

        **CORRECT ANSWER GUIDANCE:**
        Formula: SE = σ / √n
        Calculation: SE = 36 / √4 = 36 / 2 = 18
        The standard error is 18.

        STUDENT ANSWER:
        {student_answer}

        **FEEDBACK EXAMPLES (specific, not vague):**
        GOOD: "Correctly applied formula but didn't mention why μ=80 is not needed in SE calculation"
        GOOD: "Explained CLT connection clearly with reference to sample size effect"
        BAD: "Lacks depth" ❌
        BAD: "Could be improved" ❌
        BAD: "Needs more detail" ❌

        Return grading in this exact JSON format:
        {{
          "component_1_score": <0-5>,
          "component_1_explanation": "<brief explanation for task setup>",
          "component_2_score": <0-15>,
          "component_2_explanation": "<what reasoning IS present, and what specific insights would earn more points>",
          "feedback": "<SHORT teacher's comment about the reasoning quality>"
          "total_points": <0-20>,
          "max_points": 20,
          "percentage": <percentage>,
          "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
          "vibe": "<one-sentence overall impression>"
        }}"""

        # Add element check results to prompt
        element_status = f"""
        **PRE-COMPUTED ELEMENT CHECK (use these findings):**
        - Task description present: {"YES" if element_check['elements_found']['has_task_description'] else "NO"}
        - Formula present: {"YES" if element_check['elements_found']['has_formula'] else "NO"}
        - Calculation present: {"YES" if element_check['elements_found']['has_calculation'] else "NO"}
        - Result statement present: {"YES" if element_check['elements_found']['has_result_statement'] else "NO"}
        - Reasoning present: {"YES" if element_check['elements_found']['has_reasoning'] else "NO"}

        Evidence: {', '.join(element_check['evidence'])}
        """

        # Update the prompt to include element check
        prompt = prompt.replace("STUDENT ANSWER:", f"{element_status}\n\nSTUDENT ANSWER:")

        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "originality_check": originality_check,
                "element_check": element_check
            }
        )

        # If grading succeeded, add Component 1 score (which Python already calculated)
        if "error" not in result:
            result["component_1_score"] = component_1_score
            result["component_1_explanation"] = component_1_explanation
            result["total_points"] = component_1_score + result.get("component_2_score", 0)
            result["max_points"] = 20
            result["percentage"] = (result["total_points"] / 20) * 100

            # Validate that Component 2 is in range
            if result.get("component_2_score", 0) > 15:
                result["component_2_score"] = 15
                result["total_points"] = component_1_score + 15
                result["percentage"] = (result["total_points"] / 20) * 100

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
                "QUESTION 5_2",
                "Standard Error Calculation",
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
            "component_1_score": "Task Setup (Description/Formula/Calculation/Result)",
            "component_2_score": "Reasoning (Logic/Relevance/Clarity)"
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID"
        }

        # Define max scores for each component
        max_scores = {
            "component_1_score": 5,
            "component_2_score": 15
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 5_2",
            question_description="Standard Error Calculation",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="STRICT"
        )