"""
cw2_4.py
Classwork 2: Distributions and Graphs
Excel Histogram from Frequency Table
Evaluation method name: def grade_cw2_4_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW2_4Evaluator(BaseEvaluator):
    """
    Evaluator for Question 2_4: Excel Histogram Built Directly from a Frequency Table,
    Correctness Assessment, Axis/Bin Description, Explanation.

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
        Check if required elements (figure, correctness assessment, axis/bin
        description, explanation) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "figure_introduced": False,
            "correctness_stated": False,
            "bins_seen_vs_expected_stated": False,
            "text_labels_explanation_stated": False,
            "frequency_as_raw_data_explanation_stated": False,
        }

        evidence = []

        # Checkpoint 1 — Figure 3 introduced
        if re.search(r'figure\s*3', text_lower) and \
                re.search(r'presents|shows|displays|below|following', text_lower):
            elements_found["figure_introduced"] = True
            evidence.append("Figure 3 introduction found")
        else:
            evidence.append("Figure 3 introduction NOT found")

        # Checkpoint 2 — correctness assessment (histogram does/does not reflect table)
        if re.search(r'not\s+reflect|does\s+not\s+correctly|incorrect', text_lower):
            elements_found["correctness_stated"] = True
            evidence.append("Correctness assessment found")
        else:
            evidence.append("Correctness assessment NOT found")

        # Checkpoint 3 — bins seen vs expected (2 bins seen, 5 bins expected)
        if re.search(r'2\s*bins?', text_lower) and re.search(r'5\s*bins?', text_lower):
            elements_found["bins_seen_vs_expected_stated"] = True
            evidence.append("Bins seen (2) vs expected (5) comparison found")
        else:
            evidence.append("Bins seen vs expected comparison NOT found")

        # Checkpoint 4 — explanation: text category labels cannot be used as bins
        if re.search(r'text|label|category|categories', text_lower) and \
                re.search(r'bin', text_lower):
            elements_found["text_labels_explanation_stated"] = True
            evidence.append("Text-label-as-bins explanation found")
        else:
            evidence.append("Text-label-as-bins explanation NOT found")

        # Checkpoint 5 — explanation: frequency column values treated as raw data
        if re.search(r'frequency', text_lower) and \
                re.search(r'raw\s+data|raw\s+values|as\s+data', text_lower):
            elements_found["frequency_as_raw_data_explanation_stated"] = True
            evidence.append("Frequency-treated-as-raw-data explanation found")
        else:
            evidence.append("Frequency-treated-as-raw-data explanation NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_cw2_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 2_4: Excel Histogram Built Directly from a Frequency Table,
        Correctness Assessment, Axis/Bin Description, Explanation.
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
                    "component_4_score": 5,
                    "component_5_score": 4,
                },
                max_points=20,
                feedback="[TEST MODE] Figure, correctness assessment, axis/bin description, and explanation all correctly presented.",
                vibe="Student demonstrates solid understanding of why entering a frequency table directly produces an incorrect Excel histogram",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "figure_introduced": True,
                            "correctness_stated": True,
                            "bins_seen_vs_expected_stated": True,
                            "text_labels_explanation_stated": True,
                            "frequency_as_raw_data_explanation_stated": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["does your histogram"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 4. Try to build a histogram in Excel by entering the frequency table below directly. Insert the result as a Figure, introduce, name, and title it (5 points). Does your histogram reflects the table correctly (5 points)? What do you see on the histogram? Describe it: what do you see on axes? What did you expect to see? How many bins do you see? How many bins did you expect? (5 points). Why it happens (5 points)?

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

**Component 2: Figure 3 (4 points):**
- 1 point: introductory phrase itself
- 1 point: reference to the figure number in the introductory phrase
- 1 point: figure number
- 1 point: figure title
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Correctness Assessment (5 points):**
- 1 point: statement of whether the histogram reflects the table correctly
- 2 points: reference to the X-axis in that assessment
- 2 points: reference to the Y-axis in that assessment
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Histogram Description (5 points):**
- 1 point: description of what is seen on the X-axis
- 1 point: description of what is seen on the Y-axis
- 1 point: statement of what was expected to be seen
- 1 point: statement of the number of bins seen
- 1 point: statement of the number of bins expected
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: Explanation (4 points):**
- 2 points: explanation of why text category labels cannot be used as bins
- 2 points: explanation of why the frequency column values were treated as raw data
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
Figure 3 below presents the histogram produced by entering the frequency table directly into Excel. The histogram in Figure 3 does not reflect the frequency table correctly. On the axes, the X-axis shows only two intervals, [1, 7.5] and (7.5, 14], and the Y-axis shows counts ranging from 0 to 4.5, labelled in fractional increments (0.5, 1.5, 2.5, 3.5, 4.5). This is also incorrect, since a count of data points must always be a whole number — a bin cannot contain half a value. The X-axis was expected to show the five stress-level categories from the table (0-3, 4-7, 8-11, 12-15, 16-19), with bar heights matching their frequencies (3, 9, 7, 4, 1). Two bins are seen, but five bins were expected — one for each stress-level category in the table. This happens because Excel's histogram tool needs a column of raw numeric values to build bins from; it cannot use text category labels like "0 - 3" as bin boundaries. When the frequency table was entered directly, the only numeric column available was Frequency (3, 9, 7, 4, 1). Excel treated these five frequency counts as if they were five individual raw data values, and built its own two bins from their spread, instead of using them as bar heights for the five stress-level categories. As a result, the chart shows the distribution of the frequency numbers themselves, not the distribution of stress scores.

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
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-5>,
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
            "component_3_score": "Correctness Assessment",
            "component_4_score": "Histogram Description",
            "component_5_score": "Explanation",
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
            "component_3_score": 5,
            "component_4_score": 5,
            "component_5_score": 4,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 2_4",
            question_description="Excel Histogram Built Directly from a Frequency Table, Correctness Assessment, Axis/Bin Description, Explanation",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
                )