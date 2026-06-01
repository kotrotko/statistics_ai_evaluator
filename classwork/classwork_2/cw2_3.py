"""
cw2_3.py
Classwork 2: Distributions and graphs
Excel Histogram + X-axis Labels + Bar Chart vs Histogram
Evaluation method name: def grade_question_cw2_3_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW2_3Evaluator(BaseEvaluator):
    """
    Evaluator for Question 2_3: Excel Histogram, Figure Formatting, and Chart Comparison.

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
        Check if required elements (histogram, figure numbering, x-axis, comparison) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "figure_introduced": False,
            "bins_10": False,
            "bin_notation": False,
            "bar_histogram_difference": False,
        }

        evidence = []

        # Checkpoint 1 — Figure introduction and numbering
        if re.search(r'figure\s*1', text_lower) and \
                re.search(r'presents|shows|displays|below|following', text_lower):
            elements_found["figure_introduced"] = True
            evidence.append("Figure introduction found")
        else:
            evidence.append("Figure introduction NOT found")

        # Checkpoint 2 — 10 bins and data range explanation
        bins_patterns = [r'\b10\s*bins?\b', r'\bten\s*bins?\b', r'\b10\s*intervals?\b']
        range_patterns = [r'\brange\b', r'\b1\s*to\s*10\b', r'\bdata range\b', r'\bscore\b']
        bins_found = any(re.search(p, text_lower) for p in bins_patterns)
        range_found = any(re.search(p, text_lower) for p in range_patterns)
        if bins_found and range_found:
            elements_found["bins_10"] = True
            evidence.append("10-bin structure and range explanation found")
        else:
            evidence.append("10-bin structure or range explanation NOT found")

        # Checkpoint 3 — Bin notation (two numbers, brackets, interval boundaries)
        notation_patterns = [r'\bbracket\b', r'\binterval\b',
                            r'\bleft.open\b', r'\bright.closed\b', r'\[\d']
        notation_count = sum(1 for p in notation_patterns if re.search(p, text_lower))
        if notation_count >= 2:
            elements_found["bin_notation"] = True
            evidence.append("Bin notation explanation found")
        else:
            evidence.append("Bin notation explanation NOT found")

        # Checkpoint 4 — Bar chart vs histogram comparison
        comparison_patterns = [r'\bbar chart\b', r'\bcategorical\b', r'\bcontinuous\b', r'\binterval\b',
                               r'\bhistogram\b.*\bbar\b']
        comparison_count = sum(1 for p in comparison_patterns if re.search(p, text_lower))
        if comparison_count >= 2:
            elements_found["bar_histogram_difference"] = True
            evidence.append("Bar chart vs histogram comparison found")
        else:
            evidence.append("Bar chart vs histogram comparison NOT found")
        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_question_cw2_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 2_3: Excel histogram, figure formatting, x-axis labels, and chart comparison.
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
                    "component_2_score": 4,
                    "component_3_score": 5,
                    "component_4_score": 4,
                },
                max_points=20,
                feedback="[TEST MODE] Good histogram creation and x-axis labeling. Minor improvements needed in figure numbering and comparison explanation.",
                vibe="Student demonstrates solid understanding of Excel charts and statistical visualization concepts",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "histogram_built": True,
                            "figure_numbered": True,
                            "x_axis_labels": True,
                            "bar_histogram_difference": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )
        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["find your way", "does your histogram"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 3. Find your way using AI: In Excel, build a histogram 2 for the Quiz 5 variable. 
Introduce, number, and title the histogram as a Figure. (5 points). 
How many bins does your histogram has and why? (5 points) 
Ensure correct X-axis labels. Why every bin is labelled by 2 numbers? Why they are in square 
brackets? (5 points). 
What is the difference between bar chart and histogram? Why scores in this case could be treated 
as interval data? Is histogram acceptable in this case? (5 points).

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

**Component 2: Figure (5 points):**
- 1 point: Introductory phrase present before the figure
- 1 point: Reference to the figure number in the introductory phrase
- 1 point: Standalone figure number present
- 1 point: Figure title present
- 1 point: Histogram figure itself present
- CRITICAL: A label such as "Figure 1. Frequency Distribution Diagram..." counts as both 
number and title
- CRITICAL: Do NOT assume elements are present if not explicitly written in the 
student's text

**Component 3: Bins (4 points):**
- 2 points: Histogram has 10 bins
- 2 points: Explanation references the data range (scores 1 to 10)
- CRITICAL: Do NOT assume elements are present if not explicitly written in the 
student's text

**Component 4: Bin Notation (4 points):**
- 1 point: Explains that each bin label contains two numbers (interval boundaries)
- 1 point: Explains that brackets indicate interval boundaries
- 1 point: Identifies left-open bracket notation
- 1 point: Identifies right-closed bracket notation
- CRITICAL: Do NOT assume elements are present if not explicitly written in the 
student's text

**Component 5: Comparison (5 points):**
- 1 point: Correctly identifies data type difference (continuous vs categorical)
- 1 point: Mentions bars touch in histogram (no gaps between bins)
- 1 point: Mentions bars have spaces in bar chart
- 1 point: Explains scores can be treated as interval data (equal distances)
- 1 point: Concludes histogram is acceptable for this data
- CRITICAL: Do NOT assume elements are present if not explicitly written in the 
student's text

**CORRECT ANSWER REFERENCE:**
A histogram was constructed in Excel for the variable Quiz 5 to examine the frequency distribution of scores. The resulting histogram is presented in Figure 1.
Figure 1.
Frequency Distribution Diagram Produced in Excel. Quiz 5.
The histogram contains 10 bins. The number of bins is chosen based on the data range (from 1 to 10).
Each bin on the X-axis is labelled by two numbers because in Excel histogram a bin represents an interval rather than a single value. The numbers are shown in square brackets because the brackets indicate the boundaries of the interval included in that bin. Typically Excel uses left-open, right-closed intervals.
A histogram in Excel is used for continuous numerical data and displays the frequency distribution of values grouped into intervals (bins). The bars in a histogram touch each other. In contrast, a bar chart is used for categorical data and compares frequencies or values across distinct categories. The bars in a bar chart are separated by spaces because the categories are independent of one another. The scores in this case could be treated as interval data because of equal distance between values, and the histogram is acceptable for them.

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
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-4>,
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
            "component_2_score": "Figure",
            "component_3_score": "Bins",
            "component_4_score": "Bin Notation",
            "component_5_score": "Comparison",
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
            "component_3_score": 4,
            "component_4_score": 4,
            "component_5_score": 5,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 2_3",
            question_description="Excel Histogram + Bin Analysis + Bar Chart vs Histogram",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )
