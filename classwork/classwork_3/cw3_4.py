"""
cw3_4.py
Classwork 3: Central Tendency and Variability
Boxplots by Gender
Evaluation method name: def grade_cw3_4_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW3_4Evaluator(BaseEvaluator):
    """
    Evaluator for Question 3_4: Boxplots of IQ Scores by Gender.

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
        Check if required elements (figure, box/median, whiskers, outliers) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "figure_introduced": False,
            "box_range_stated": False,
            "median_stated": False,
            "whiskers_stated": False,
            "outliers_stated": False,
        }

        evidence = []

        # Checkpoint 1 — Figure 3 introduced
        if re.search(r'figure\s*3', text_lower) and \
                re.search(r'presents|shows|displays|below|following', text_lower):
            elements_found["figure_introduced"] = True
            evidence.append("Figure 3 introduction found")
        else:
            evidence.append("Figure 3 introduction NOT found")

        # Checkpoint 2 — Box range for both genders (85/113 male, 92/105 female)
        if re.search(r'85', text_lower) and re.search(r'113', text_lower) and \
                re.search(r'92', text_lower) and re.search(r'105', text_lower):
            elements_found["box_range_stated"] = True
            evidence.append("Box range for both genders found")
        else:
            evidence.append("Box range for both genders NOT found")

        # Checkpoint 3 — Median values (95 male, 98 female)
        if re.search(r'95', text_lower) and re.search(r'98', text_lower):
            elements_found["median_stated"] = True
            evidence.append("Median values found")
        else:
            evidence.append("Median values NOT found")

        # Checkpoint 4 — Whisker values (43, 130 male; 65 female)
        if re.search(r'43', text_lower) and re.search(r'130', text_lower) and \
                re.search(r'65', text_lower):
            elements_found["whiskers_stated"] = True
            evidence.append("Whisker values found")
        else:
            evidence.append("Whisker values NOT found")

        # Checkpoint 5 — Outlier case numbers and values (case 2, 44, 53; values 65, 122, 130)
        if re.search(r'\b2\b', text_lower) and re.search(r'\b44\b', text_lower) and \
                re.search(r'\b53\b', text_lower) and re.search(r'122', text_lower):
            elements_found["outliers_stated"] = True
            evidence.append("Outlier case numbers and values found")
        else:
            evidence.append("Outlier case numbers and/or values NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_cw3_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 3_4: Boxplots of IQ Scores by Gender.
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
                    "component_2_score": 5,
                    "component_3_score": 5,
                    "component_4_score": 4,
                    "component_5_score": 4,
                },
                max_points=20,
                feedback="[TEST MODE] Figure, box/median, whiskers, and outliers all correctly presented.",
                vibe="Student demonstrates solid understanding of boxplot elements and gender comparison",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "figure_introduced": True,
                            "box_range_stated": True,
                            "median_stated": True,
                            "whiskers_stated": True,
                            "outliers_stated": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["please add"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 4. Please add boxplots for both genders. Write an introductory phrase referring to Figure 3, then title the Figure. Apply the 'Use color palette' and 'Label outliers' options (5 points). For the boxplots, describe what the box (its horizontal sides) shows and what the line inside the box represents (5 points). Describe what the whiskers show (5 points). Identify the outliers: what do they look like, and what are their values (5 points)?

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

**Component 2: Figure 3 (5 points):**
- 2 points: introductory phrase itself
- 1 point: reference to the figure number in the introductory phrase
- 1 point: figure number
- 1 point: figure title
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Box and Median (5 points):**
- 3 points: correctly describing what the box shows
- 2 points: correctly describing what the line inside the box represents
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Whiskers (4 points):**
- 4 points: correctly describing what the whiskers show
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: Outliers (4 points):**
- 2 points: correctly identifying what the outliers look like
- 2 points: correctly stating their values
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
Figure 3 presents boxplots of IQ scores for both genders.
Figure 3 Boxplots of IQ by Gender
The box shows the middle 50% of scores: its top and bottom sides mark the
3rd and 2nd quartiles. For males, the box runs from about 85 to 113; for
females, from about 92 to 105. The line inside the box marks the median
score, around 95 for males and 98 for females.
The whiskers extend from the box to the lowest and highest scores that are
not outliers, showing the spread of the remaining scores. For males, the
whiskers run from about 43 to 130. For females, the lower whisker reaches
about 65.
Outliers are shown as individual labeled dots, separate from the whiskers.
Males have no outliers. Females have one outlier below the lower whisker,
case 2, with an IQ score of about 65, and two outliers above the upper
whisker, cases 44 and 53, with IQ scores of about 122 and 130.

{FEEDBACK_RULES}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-4>,
  "component_4_explanation": "<brief>",
  "component_5_score": <0-4>,
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
                "component_5_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results using OutputFormatter."""
        # Define component labels
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Figure 3",
            "component_3_score": "Box and Median",
            "component_4_score": "Whiskers",
            "component_5_score": "Outliers",
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
            "component_2_score": 5,
            "component_3_score": 5,
            "component_4_score": 4,
            "component_5_score": 4,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 3_4",
            question_description="Boxplots of IQ Scores by Gender",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )