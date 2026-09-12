"""
cw3_5.py
Classwork 3: Distributions and graphs
Summarize
Evaluation method name: def grade_cw3_5_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW3_5Evaluator(BaseEvaluator):
    """
    Evaluator for Question 3_5: Frequency Distribution definition,
    Central Tendency Measures (list + explain), Variability Measures (list + explain).

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    def __init__(self):
        """Initialize evaluator with API handler."""
        super().__init__()
        # Initialize output formatter
        self.formatter = OutputFormatter(default_width=60)

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check if required elements (frequency distribution explanation,
        central tendency measures, variability measures) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "frequency_distribution_mentioned": False,
            "central_tendency_mentioned": False,
            "mean_listed": False,
            "median_listed": False,
            "mode_listed": False,
            "variability_mentioned": False,
            "range_listed": False,
            "variance_listed": False,
            "standard_deviation_listed": False,
        }

        evidence = []

        # Checkpoint 1 — frequency distribution term present
        if re.search(r'frequency\s+distribution', text_lower):
            elements_found["frequency_distribution_mentioned"] = True
            evidence.append("Frequency distribution term found")
        else:
            evidence.append("Frequency distribution term NOT found")

        # Checkpoint 2 — central tendency term present
        if re.search(r'central\s+tendency', text_lower):
            elements_found["central_tendency_mentioned"] = True
            evidence.append("Central tendency term found")
        else:
            evidence.append("Central tendency term NOT found")

        # Checkpoint 3 — mean listed
        if re.search(r'\bmean\b', text_lower):
            elements_found["mean_listed"] = True
            evidence.append("Mean listed")
        else:
            evidence.append("Mean NOT listed")

        # Checkpoint 4 — median listed
        if re.search(r'\bmedian\b', text_lower):
            elements_found["median_listed"] = True
            evidence.append("Median listed")
        else:
            evidence.append("Median NOT listed")

        # Checkpoint 5 — mode listed
        if re.search(r'\bmode\b', text_lower):
            elements_found["mode_listed"] = True
            evidence.append("Mode listed")
        else:
            evidence.append("Mode NOT listed")

        # Checkpoint 6 — variability term present
        if re.search(r'variability', text_lower):
            elements_found["variability_mentioned"] = True
            evidence.append("Variability term found")
        else:
            evidence.append("Variability term NOT found")

        # Checkpoint 7 — range listed
        if re.search(r'\brange\b', text_lower):
            elements_found["range_listed"] = True
            evidence.append("Range listed")
        else:
            evidence.append("Range NOT listed")

        # Checkpoint 8 — variance listed
        if re.search(r'\bvariance\b', text_lower):
            elements_found["variance_listed"] = True
            evidence.append("Variance listed")
        else:
            evidence.append("Variance NOT listed")

        # Checkpoint 9 — standard deviation listed
        if re.search(r'standard\s+deviation', text_lower):
            elements_found["standard_deviation_listed"] = True
            evidence.append("Standard deviation listed")
        else:
            evidence.append("Standard deviation NOT listed")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_cw3_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 3_5: Frequency Distribution, Central Tendency Measures,
        Variability Measures.
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
                    "component_2_score": 2,
                    "component_3_score": 8,
                    "component_4_score": 8,
                },
                max_points=20,
                feedback="[TEST MODE] Frequency distribution, central tendency, and variability measures all correctly presented.",
                vibe="Student demonstrates solid understanding of frequency distributions, central tendency, and variability",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "frequency_distribution_mentioned": True,
                            "central_tendency_mentioned": True,
                            "mean_listed": True,
                            "median_listed": True,
                            "mode_listed": True,
                            "variability_mentioned": True,
                            "range_listed": True,
                            "variance_listed": True,
                            "standard_deviation_listed": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["write please"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 5. Summarize: What is frequency distribution? (2 points). What are central tendency measures? List three most important ones and explain what each one shows (9 points). What is variability measures? List three most important ones and explain what each one shows (9 points).

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
- 1 point: correct task description formatting
- 1 point: proper autoformatting and structure in the solution

**Component 2: Frequency Distribution (2 points):**
- 2 points: correctly explaining what a frequency distribution is
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Central Tendency Measures (8 points):**
- 2 points: correctly describing what central tendency measures represent
- 1 point: listing mean
- 1 point: explaining what mean shows
- 1 point: listing median
- 1 point: explaining what median shows
- 1 point: listing mode
- 1 point: explaining what mode shows
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Variability Measures (8 points):**
- 2 points: correctly describing what variability measures represent
- 1 point: listing range
- 1 point: explaining what range shows
- 1 point: listing variance
- 1 point: explaining what variance shows
- 1 point: listing standard deviation
- 1 point: explaining what standard deviation shows
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
A frequency distribution shows how often each value, or range of values, occurs in a dataset. It organizes raw scores into categories and reports the count (or percentage) of cases falling into each category, which makes patterns in the data much easier to see than scanning a long list of individual scores. Central tendency measures describe the typical or most representative score in a dataset — a single value that summarizes where the center of the data lies. The three most important central tendency measures are: Mean — the arithmetic average, found by adding up all the scores and dividing by the number of scores. Median — the middle score when all values are arranged in order from lowest to highest. Mode — the value that occurs most frequently in the dataset. Variability measures describe how spread out, or dispersed, the scores in a dataset are around the center. The three most important variability measures are: Range — the difference between the highest and lowest scores in the dataset. Variance — the average of the squared differences between each score and the mean, describing how spread out the scores are, expressed in squared units. Standard deviation — the square root of the variance, representing the typical distance of scores from the mean, expressed in the original units of measurement.

{FEEDBACK_RULES}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-2>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-8>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-8>,
  "component_4_explanation": "<brief>",
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

        # Force Component 1 (Formatting) deterministically from the regex-based
        # check instead of trusting the LLM's own component_1_score
        if "error" not in result:
            result["component_1_task_score"] = 1 if formatting_check["elements_found"]["task_description"] else 0
            result["component_1_autoformat_score"] = 1 if formatting_check["elements_found"]["autoformatting"] else 0
            result["component_1_score"] = result["component_1_task_score"] + result["component_1_autoformat_score"]

        # If grading succeeded, validate component scores
        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results using OutputFormatter."""
        # Define component labels
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Frequency Distribution",
            "component_3_score": "Central Tendency Measures",
            "component_4_score": "Variability Measures",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
            "component_4_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 2,
            "component_3_score": 8,
            "component_4_score": 8,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 3_5",
            question_description="Frequency Distribution, Central Tendency Measures, Variability Measures",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )