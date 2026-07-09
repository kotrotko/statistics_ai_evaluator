"""
cw12_4.py
Classwork 12: Correlational Analysis
Spearman correlation matrix, Effect Size, and Plot Informativeness
Evaluation method name: def grade_cw12_4_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW12_4Evaluator(BaseEvaluator):
    """
    Evaluator for Question 12_4: Correlation Matrix, Significant Correlations, Effect Size, and Plot Informativeness.

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    def __init__(self):
        """Initialize evaluator with API handler."""
        super().__init__(
            temperature=0.3,
            max_tokens=2000
        )
        # Initialize output formatter
        self.formatter = OutputFormatter(default_width=60)

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check if required elements (table, significant correlations, effect size, plot explanation) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "table_introduced": False,
            "significant_count_present": False,
            "non_significant_pairs_named": False,
            "effect_size_no_decision": False,
            "plot_explanation_present": False,
        }

        evidence = []

        # Checkpoint 1 — Table 2 introduced
        if re.search(r'table\s*2', text_lower) and \
                re.search(r'presents|shows|displays|below|following', text_lower):
            elements_found["table_introduced"] = True
            evidence.append("Table 2 introduction found")
        else:
            evidence.append("Table 2 introduction NOT found")

        # Checkpoint 2 — Significant correlations count (13)
        if re.search(r'\b13\b', text_lower):
            elements_found["significant_count_present"] = True
            evidence.append("Significant correlations count 13 found")
        else:
            evidence.append("Significant correlations count 13 NOT found")

        # Checkpoint 3 — Non-significant pairs named (scale11-scale13, scale11-scale15)
        if re.search(r'scale\s*11.{0,15}scale\s*13', text_lower) and \
                re.search(r'scale\s*11.{0,15}scale\s*15', text_lower):
            elements_found["non_significant_pairs_named"] = True
            evidence.append("Non-significant pairs (scale11-scale13, scale11-scale15) named")
        else:
            evidence.append("Non-significant pairs (scale11-scale13, scale11-scale15) NOT named")

        # Checkpoint 4 — Effect size "No" decision
        if re.search(r'\bno\b.{0,60}effect\s*size|effect\s*size.{0,60}\bno\b|no\s*separate\s*effect\s*size', text_lower):
            elements_found["effect_size_no_decision"] = True
            evidence.append("Effect size 'No' decision found")
        else:
            evidence.append("Effect size 'No' decision NOT found")

        # Checkpoint 5 — Plot explanation (ranked data)
        if re.search(r'rank(ed)?', text_lower):
            elements_found["plot_explanation_present"] = True
            evidence.append("Plot explanation (ranked data) found")
        else:
            evidence.append("Plot explanation (ranked data) NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_cw12_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 12_4: Correlation Matrix, Significant Correlations, Effect Size, and Plot Informativeness.
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
                    "component_4_score": 4,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Good identification of significant correlations, effect size reasoning, and plot explanation.",
                vibe="Student demonstrates solid understanding of correlation matrices and effect size interpretation",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "table_introduced": True,
                            "significant_count_present": True,
                            "non_significant_pairs_named": True,
                            "effect_size_no_decision": True,
                            "plot_explanation_present": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["do you see", "do you need"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
4. Correlation matrix. Add the correlation matrix. (5 points). How many significant correlations do you see? Flag them (5 points). Do you need to calculate the effect size? If no, explain why. If yes, provide result (included into correlation matrix) and explain what does it mean, in one sentence (5 points). Following the Dr. E's video on 04:47 minute, please explain why the plot is not so informative in case of Spearman correlation (5 points).

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
- 1 point: Correct task description formatting
- 1 point: Lack of autoformatting

**Component 2: Table 2 (4 points):**
- 1 point: Introductory phrase present before the table
- 1 point: Reference to the table number in the introductory phrase
- 1 point: Standalone table number and title present
- 1 point: The table itself present
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Significant correlations (5 points):**
- 1 point: Count of significant correlations stated
- 2 points: Correct value (13 out of 15)
- 2 points: Both non-significant pairs flagged in the table (scale11–scale13, scale11–scale15)
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Effect size (4 points):**
- 1 point: "No" decision stated
- 3 points: Justification that the correlation coefficient itself serves as the effect size, since it conveys both strength and direction of the relationship
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: Plot explanation (5 points):**
- 1 point: States that Spearman's rho is calculated on ranked data rather than raw continuous values
- 1 point: Links this to the small number of repeated scale points causing overlap in the scatterplot
- 1 point: States that this overlap obscures the visual pattern
- 2 points: Conclusion that the numerical coefficient is a clearer summary than the plot
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
Table 2 presents the correlation matrix for the six variables. Of the 15 pairwise correlations shown in Table 2, 13 are statistically significant at α = .05. The only two non-significant correlations are scale11–scale13 (ρ = -0.146, p = .117) and scale11–scale15 (ρ = -0.125, p = .180); all remaining pairs reach significance and are flagged accordingly in the table above. No separate effect size calculation is needed. In correlation analysis, the correlation coefficient itself serves as the effect size, since it conveys both the strength and the direction of the relationship in a single value. The scatterplot is less informative for Spearman correlation because Spearman's rho is calculated on the ranked data rather than on the raw continuous values. Because these variables have a small number of repeated scale points, many observations overlap in the scatterplot, so the visual pattern becomes less clear than the numerical coefficient.

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
            "component_3_score": "Significant Correlations",
            "component_4_score": "Effect Size",
            "component_5_score": "Plot Explanation",
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
            "component_4_score": 4,
            "component_5_score": 5,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 12_4",
            question_description="Correlation Matrix, Significant Correlations, Effect Size, and Plot Informativeness",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )