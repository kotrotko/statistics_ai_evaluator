"""
cw8_4.py
Classwork 8: Repeated Measures
Paired t-test inference, Effect size, Descriptive plot
Evaluation method name: def grade_cw8_4_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW8_4Evaluator(BaseEvaluator):
    """
    Evaluator for Question 8_4: JASP Statistics Table, Statistical Inference,
    Cohen's d Effect Size, Descriptive Plot.

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
        Check if required elements (table, inference, Cohen's d, plot) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "table_introduced": False,
            "t_vs_cv_stated": False,
            "p_vs_alpha_stated": False,
            "reject_decision_stated": False,
            "cohens_d_value_stated": False,
            "figure_introduced": False,
        }

        evidence = []

        # Checkpoint 1 — Table 2 introduced
        if re.search(r'table\s*2', text_lower) and \
                re.search(r'presents|shows|displays|below|following', text_lower):
            elements_found["table_introduced"] = True
            evidence.append("Table 2 introduction found")
        else:
            evidence.append("Table 2 introduction NOT found")

        # Checkpoint 2 — t vs CV comparison (t = 6.452, CV = 2.145)
        if re.search(r'6\.45', text_lower) and re.search(r'2\.145', text_lower):
            elements_found["t_vs_cv_stated"] = True
            evidence.append("t (6.452) vs CV (2.145) comparison found")
        else:
            evidence.append("t vs CV comparison NOT found")

        # Checkpoint 3 — p vs alpha
        if re.search(r'p\s*<\s*\.?001|p\s*<\s*0?\.001', text_lower) and \
                re.search(r'α\s*=\s*0\.05|alpha\s*=\s*0\.05', text_lower):
            elements_found["p_vs_alpha_stated"] = True
            evidence.append("p vs α comparison found")
        else:
            evidence.append("p vs α comparison NOT found")

        # Checkpoint 4 — reject/fail-to-reject decision
        if re.search(r'reject\s+h', text_lower):
            elements_found["reject_decision_stated"] = True
            evidence.append("Reject/fail-to-reject decision found")
        else:
            evidence.append("Reject/fail-to-reject decision NOT found")

        # Checkpoint 5 — Cohen's d value (1.666) and threshold (0.8)
        if re.search(r'cohen', text_lower) and re.search(r'1\.66', text_lower) and re.search(r'0\.8', text_lower):
            elements_found["cohens_d_value_stated"] = True
            evidence.append("Cohen's d value and threshold found")
        else:
            evidence.append("Cohen's d value and/or threshold NOT found")

        # Checkpoint 6 — Figure 1 introduced
        if re.search(r'figure\s*1', text_lower) and \
                re.search(r'presents|shows|displays|below|following', text_lower):
            elements_found["figure_introduced"] = True
            evidence.append("Figure 1 introduction found")
        else:
            evidence.append("Figure 1 introduction NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_cw8_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 8_4: JASP Statistics Table, Statistical Inference,
        Cohen's d Effect Size, Descriptive Plot.
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
                    "component_3_score": 4,
                    "component_4_score": 4,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Table, inference, Cohen's d, and plot all correctly presented.",
                vibe="Student demonstrates solid understanding of paired t-test inference and effect size interpretation",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "table_introduced": True,
                            "t_vs_cv_stated": True,
                            "p_vs_alpha_stated": True,
                            "reject_decision_stated": True,
                            "cohens_d_value_stated": True,
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
            pedagogical_markers=["please calculate"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 4. Statistical analysis. Using JASP, please calculate the statistics and include the table in APA style (5 points). Make a statistical inference (reject or fail to reject the null hypothesis) (5 points). Include Cohen's d effect size and explain what it means (5 points). Add and interpret the Descriptive plot (5 points).

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

**Component 2: Table 2 (5 points):**
- 1 point: introductory phrase
- 1 point: reference to table number in introductory phrase
- 1 point: table number
- 1 point: table title
- 1 point: Table 2 itself
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Statistical inference (4 points):**
- 1 point: comparison of t to CV
- 1 point: |t*| absolute value notation or its equivalent
- 1 point: p compared to α
- 1 point: reject/fail-to-reject decision
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Cohen's d (4 points):**
- 1 point: Cohen's d value
- 1 point: threshold comparison
- 1 point: effect size label (large)
- 1 point: explanation of what it means that Cohen's d > 1
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: Descriptive plot (5 points):**
- 1 point: introductory phrase
- 1 point: reference to figure number in introductory phrase
- 1 point: figure number
- 1 point: figure title
- 1 point: interpretation of the plot
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
Table 2 presents the results of the paired samples t-test. Since the calculated t = 6.452 exceeds the critical value |t*| = 2.145 (two-tailed critical region: t < −2.145 or t > +2.145), and p < .001 < α = 0.05, we reject H₀ and conclude that there is a statistically significant difference in the number of aggressive behaviors between the two lunar phases. Cohen's d = 1.666, which exceeds the threshold of 0.8, indicating a large effect size. This means the difference between the two conditions is not only statistically significant but also practically meaningful. Figure 1 presents the descriptive plot of the two measurements, showing that the mean number of aggressive behaviors during the Moon phase is substantially higher than during the Other phase.

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
            "component_2_score": "Table 2",
            "component_3_score": "Statistical Inference",
            "component_4_score": "Cohen's d",
            "component_5_score": "Descriptive Plot",
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
            question_name="QUESTION 8_4",
            question_description="JASP Statistics Table, Statistical Inference, Cohen's d Effect Size, Descriptive Plot",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )