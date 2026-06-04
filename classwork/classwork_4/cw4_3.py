"""
cw4_3.py
Classwork 4: Theoretical Normal Distribution and IQ
Normal Curve IQ Percentages + Figure Formatting
Evaluation method name: def grade_question_cw4_3_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW4_3Evaluator(BaseEvaluator):
    """
    Evaluator for Question 4_3: Theoretical Normal Distribution, IQ Percentages, and Figure Formatting.

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
        Check if required elements (IQ answers, figure numbering, figure itself) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "iq_above_100": False,
            "iq_above_130": False,
            "iq_120_130": False,
            "figure_introduced": False,
        }

        evidence = []

        # Checkpoint 1 — IQ > 100 answer (~50% or ~43%)
        iq_100_patterns = [r'\b50\s*%', r'\b43\s*%', r'\biq\s*>\s*100\b', r'\bgreater than 100\b',
                           r'\babove 100\b']
        if any(re.search(p, text_lower) for p in iq_100_patterns):
            elements_found["iq_above_100"] = True
            evidence.append("IQ > 100 answer found")
        else:
            evidence.append("IQ > 100 answer NOT found")

        # Checkpoint 2 — IQ > 130 answer (~2%)
        iq_130_patterns = [r'\b2\s*%', r'\biq\s*>\s*130\b', r'\bgreater than 130\b',
                           r'\babove 130\b']
        if any(re.search(p, text_lower) for p in iq_130_patterns):
            elements_found["iq_above_130"] = True
            evidence.append("IQ > 130 answer found")
        else:
            evidence.append("IQ > 130 answer NOT found")

        # Checkpoint 3 — IQ between 120 and 130 (~6%)
        iq_120_130_patterns = [r'\b6\s*%', r'\b120\s*and\s*130\b', r'\bbetween 120\b',
                                r'\b120.*130\b']
        if any(re.search(p, text_lower) for p in iq_120_130_patterns):
            elements_found["iq_120_130"] = True
            evidence.append("IQ 120–130 answer found")
        else:
            evidence.append("IQ 120–130 answer NOT found")

        # Checkpoint 4 — Figure introduction and numbering
        if re.search(r'figure\s*4', text_lower) and \
                re.search(r'presents|shows|displays|below|following', text_lower):
            elements_found["figure_introduced"] = True
            evidence.append("Figure introduction found")
        else:
            evidence.append("Figure introduction NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_question_cw4_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 4_3: Theoretical normal distribution, IQ percentages, and figure formatting.
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
                    "component_4_score": 4,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Good application of normal distribution. Minor improvements needed in figure formatting.",
                vibe="Student demonstrates solid understanding of theoretical normal distribution and IQ percentages",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "iq_above_100": True,
                            "iq_above_130": True,
                            "iq_120_130": True,
                            "figure_introduced": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["please add", "using this curve"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 3. Apply the theoretical distribution to IQ. Using this curve, answer questions and report your results, step by step.
What percentage of students theoretically should have:
(a) IQ > 100? (5 points)
(b) IQ > 130? (5 points)
(c) between 120 and 130? (5 points)
Only for (c) task, please add the normal curve with area of interest, marked by color. Introduce this figure, refer to its number, number, and title it in APA style (5 points).

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

**Component 2: IQ > 100 (4 points):**
- 2 points: Correct answer (approximately 50% or 43%)
- 2 points: Answer written as a complete sentence
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: IQ > 130 (4 points):**
- 2 points: Correct answer (approximately 2%)
- 2 points: Answer written as a complete sentence
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: IQ between 120 and 130 (5 points):**
- 2 points: Correct answer (approximately 6%)
- 2 points: Answer written as a complete sentence
- 1 point: Calculation or reasoning step shown
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: Figure (5 points):**
- 1 point: Introductory phrase present before the figure
- 1 point: Reference to Figure 4 number in the introductory phrase
- 1 point: Standalone figure number present (e.g., "Figure 4" on its own line)
- 1 point: Figure title present in APA style
- 1 point: Figure (normal curve with highlighted area) itself present
- CRITICAL: A label such as "Figure 4. Theoretical Normal Distribution..." counts as both number and title
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
The percentage of students who theoretically should have:
(a) IQ > 100: Approximately 43% of students theoretically should have an IQ greater than 100.
(b) IQ > 130: Approximately 2% of students theoretically should have an IQ greater than 130.
(c) IQ between 120 and 130: Approximately 6% of students theoretically should have an IQ between 120 and 130.
Figure 4 presents the theoretical normal distribution of IQ with the area of interest between 120 and 130 highlighted in color.
Figure 4
Theoretical Normal Distribution of IQ With Highlighted Area Between 120 and 130

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
            "component_2_score": "IQ > 100",
            "component_3_score": "IQ > 130",
            "component_4_score": "IQ 120–130",
            "component_5_score": "Figure",
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
            question_name="QUESTION 4_3",
            question_description="Normal Distribution IQ Percentages + Figure Formatting",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )