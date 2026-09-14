"""
cw5_5.py
Classwork 5: Sampling Distribution
Descriptive Statistics, Standard Error
Evaluation method name: def grade_cw5_5_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW5_5Evaluator(BaseEvaluator):
    """
    Evaluator for Question 5_5: Descriptive Statistics Report,
    Dataset Description, Standard Error.

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
        Check if required elements (table, mean, 1st quartile, SE mean) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "table_introduced": False,
            "mean_values_stated": False,
            "quartile_values_stated": False,
            "se_mean_values_stated": False,
        }

        evidence = []

        # Checkpoint 1 — Table 1 introduced
        if re.search(r'table\s*1', text_lower) and \
                re.search(r'presents|shows|displays|below|following', text_lower):
            elements_found["table_introduced"] = True
            evidence.append("Table 1 introduction found")
        else:
            evidence.append("Table 1 introduction NOT found")

        # Checkpoint 2 — Mean values (0.750, 2.330)
        if re.search(r'0\.75', text_lower) and re.search(r'2\.33', text_lower):
            elements_found["mean_values_stated"] = True
            evidence.append("Mean values (0.750, 2.330) found")
        else:
            evidence.append("Mean values NOT found")

        # Checkpoint 3 — 1st quartile values (-0.175, 0.875)
        if re.search(r'-0\.175', text_lower) and re.search(r'0\.875', text_lower):
            elements_found["quartile_values_stated"] = True
            evidence.append("1st quartile values (-0.175, 0.875) found")
        else:
            evidence.append("1st quartile values NOT found")

        # Checkpoint 4 — SE mean values (0.566, 0.633)
        if re.search(r'0\.566', text_lower) and re.search(r'0\.633', text_lower):
            elements_found["se_mean_values_stated"] = True
            evidence.append("SE mean values (0.566, 0.633) found")
        else:
            evidence.append("SE mean values NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_cw5_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 5_5: Descriptive Statistics Report,
        Dataset Description, Standard Error.
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
                    "component_4_score": 10,
                },
                max_points=20,
                feedback="[TEST MODE] Dataset description, table, and descriptive statistics all correctly presented.",
                vibe="Student demonstrates solid understanding of descriptive statistics and standard error reporting",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "table_introduced": True,
                            "mean_values_stated": True,
                            "quartile_values_stated": True,
                            "se_mean_values_stated": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["please open"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task5. Calculate the standard error in descriptive statistics context. Please open Wagenmakers et al., p. 21 - 27. Read the file description. Use this text to prepare Class Report. Watch and reproduce a video: https://www.youtube.com/watch?v=jwZVujRcUeQ using the file JASP > Open > Data Library > Descriptives > Sleep. Prepare the Descriptive Statistics report, which includes the dataset description (5 points) and descriptive statistics: (a)Mean; (b) 1st quartile; (c) SE mean (10 points). Introduce this table, number and title it (5 points).

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

**Component 2: Dataset Description (4 points):**
- 4 points: correctly describing the dataset
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Table 1 Insertion (4 points):**
- 1 point: introductory phrase itself
- 1 point: reference to the table number in the introductory phrase
- 1 point: table number
- 1 point: table title
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Descriptive Statistics (10 points):**
- 3 points: correctly reporting the mean
- 4 points: correctly reporting the 1st quartile
- 3 points: correctly reporting the SE mean
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
The dataset Sleep provides the number of additional hours that each of ten patients slept after having been administered two soporific drugs. The descriptive statistics for this dataset was created using JASP, including mean, 1st quartile and SE mean separately for 2 groups. The results are shown in Table 1.

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
  "component_4_score": <0-10>,
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
            "component_2_score": "Dataset Description",
            "component_3_score": "Table 1 Insertion",
            "component_4_score": "Descriptive Statistics",
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
            "component_2_score": 4,
            "component_3_score": 4,
            "component_4_score": 10,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 5_5",
            question_description="Descriptive Statistics Report, Dataset Description, Standard Error",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )