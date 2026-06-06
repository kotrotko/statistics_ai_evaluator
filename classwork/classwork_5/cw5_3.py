"""
cw5_3.py
Classwork 5: Z-scores
Z-Score Definition + Formula + Given + Solution + Answer
Evaluation method name: def grade_question_cw5_3_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW5_3Evaluator(BaseEvaluator):
    """
    Evaluator for Question 5_3: Z-Score Definition, Formula, Given/Solution/Answer structure.

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

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check if required elements (z-score definition, formula, given, solution, answer) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "zscore_definition": False,
            "zscore_formula": False,
            "given_section": False,
            "solution_word": False,
            "answer_section": False,
            "correct_answer": False,
        }

        evidence = []

        # Checkpoint 1 — Z-score definition
        definition_patterns = [
            r'\bz.score\b', r'\bstandardized\b', r'\bstandard deviation\b',
            r'\bstandard deviations\b', r'\bbelow\b.*\bmean\b', r'\babove\b.*\bmean\b'
        ]
        definition_count = sum(1 for p in definition_patterns if re.search(p, text_lower))
        if definition_count >= 2:
            elements_found["zscore_definition"] = True
            evidence.append("Z-score definition found")
        else:
            evidence.append("Z-score definition NOT found")

        # Checkpoint 2 — Z-score formula
        formula_patterns = [
            r'z\s*=', r'σ\s*/\s*√', r'sigma', r'sqrt\s*\(', r'√\s*n',
            r'\bformula\b', r'm\s*[-−]\s*μ', r'sample mean'
        ]
        formula_count = sum(1 for p in formula_patterns if re.search(p, text_lower))
        if formula_count >= 2:
            elements_found["zscore_formula"] = True
            evidence.append("Z-score formula found")
        else:
            evidence.append("Z-score formula NOT found")

        # Checkpoint 3 — Given section present
        if re.search(r'\bgiven\b', text_lower):
            elements_found["given_section"] = True
            evidence.append("Given section found")
        else:
            evidence.append("Given section NOT found")

        # Checkpoint 4 — Solution word present
        if re.search(r'\bsolution\b', text_lower):
            elements_found["solution_word"] = True
            evidence.append("Solution word found")
        else:
            evidence.append("Solution word NOT found")

        # Checkpoint 5 — Answer section present
        answer_patterns = [r'\banswer\b', r'\bn\s*=\s*25\b', r'\b25\s*scores?\b']
        answer_count = sum(1 for p in answer_patterns if re.search(p, text_lower))
        if answer_count >= 1:
            elements_found["answer_section"] = True
            evidence.append("Answer section found")
        else:
            evidence.append("Answer section NOT found")

        # Checkpoint 6 — Correct answer value (n = 25)
        correct_answer_patterns = [r'\bn\s*=\s*25\b', r'\b25\s*scores?\b']
        correct_answer_count = sum(1 for p in correct_answer_patterns if re.search(p, text_lower))
        if correct_answer_count >= 1:
            elements_found["correct_answer"] = True
            evidence.append("Correct answer (n = 25) found")
        else:
            evidence.append("Correct answer NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_question_cw5_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 5_3: Z-score definition, formula, Given/Solution/Answer structure.
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
                    "component_3_score": 4,
                    "component_4_score": 5,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Good z-score definition and structured solution. Minor improvements needed in formula notation.",
                vibe="Student demonstrates solid understanding of z-scores and sample size calculation",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "zscore_definition": True,
                            "zscore_formula": True,
                            "given_section": True,
                            "solution_word": True,
                            "answer_section": True,
                            "correct_answer": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["please use", "z = 2.00"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 3. What is a z-score? A sample from a population with μ=40 and σ=10 has a mean of M = 44.
If the sample mean corresponds to a z = 2.00, then how many scores are in the sample?
Please use rubrics Given, Solution, Answer.

Total: 20 points

STUDENT ANSWER:
{student_answer}

{IMPORTANT_NOTES}

{IMPORTANT_GRADING_RULES}

**HYBRID GRADING APPROACH:**

**AUTOMATIC FORMATTING DETECTION RESULT:**
Task description correctly formatted (1 point if True): {formatting_check['elements_found']['task_description']}
Proper autoformatting and structure (1 point if True): {formatting_check['elements_found']['autoformatting']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC DETECTION:**
{element_check['elements_found']}

**RUBRIC**

**Component 1: Formatting (2 points):**
Use AUTOMATIC FORMATTING DETECTION RESULT above.
- 1 point: Task description correctly formatted
- 1 point: Proper autoformatting and structure

**Component 2: Z-Score Definition (4 points):**
- 2 points: Definition of z-score (standardized value expressing how many standard deviations
  a data point or sample mean lies above or below the population mean)
- 2 points: Formula for z-score of a sample mean: z = (M − μ) / (σ / √n)
  with correct identification of all variables (M, μ, σ, n)
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Given (4 points):**
- 1 point: Population mean (μ = 40) stated
- 1 point: Population SD (σ = 10) stated
- 1 point: Sample mean (M = 44) stated
- 1 point: Z-score (z = 2.00) stated
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Solution (5 points):**
- 1 point: The word "Solution" is present as a section header — use solution_word from AUTOMATIC DETECTION
- 2 points: Known values substituted into the formula (2.00 = (44 − 40) / (10 / √n))
- 1 point: Step solving for √n shown (√n = 5)
- 1 point: Step squaring both sides shown (n = 25)
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: Answer (5 points):**
- 1 point: The word "Answer" is present as a section header
- 2 points: Answer value is stated (n = 25 or "25 scores")
- 2 points: Stated answer is correct (n = 25)
- CRITICAL: Do NOT give the correctness points if the stated answer is wrong
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
Task 3. What is a z-score? A sample from a population with μ=40 and σ=10 has a mean of M = 44.
If the sample mean corresponds to a z = 2.00, then how many scores are in the sample?
Please use rubrics Given, Solution, Answer.

z-Score definition. A z-score is a standardized value that expresses how many standard deviations
a data point (or sample mean) lies above or below the population mean. For a sample mean, the
formula is: z = (M − μ) / (σ / √n) where M = sample mean, μ = population mean, σ = population SD,
n = sample size.

Given:
Population mean (μ) = 40
Population SD (σ) = 10
Sample mean (M) = 44
Z-score (z) = 2.00
Find n = ?

Solution:
Substitute the known values: 2.00 = (44 − 40) / (10 / √n)
2.00 = 4 / (10 / √n)
Solve for √n: 10 / √n = 4 / 2.00 = 2 → √n = 10 / 2 = 5
Square both sides: n = 5² = 25

Answer: The sample contains n = 25 scores.

This model answer scores 20/20.

{FEEDBACK_RULES}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief>",
  "component_5_score": <0-5>,
  "component_5_explanation": "<brief>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression>"
}}"""

        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "element_check": element_check,
                "formatting_check": formatting_check
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
        """Display grading results using OutputFormatter."""
        # Define component labels
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Z-Score Definition",
            "component_3_score": "Given",
            "component_4_score": "Solution",
            "component_5_score": "Answer",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
            "component_4_score": "HYBRID",
            "component_5_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 4,
            "component_3_score": 4,
            "component_4_score": 5,
            "component_5_score": 5,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 5_3",
            question_description="Z-Score Definition + Formula + Given + Solution + Answer",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )