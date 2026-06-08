"""
cw7_3.py
Classwork 7: One Sample T-Test
Wilcoxon Signed Rank + Approach Justification + Table 2 + Inference
Evaluation method name: def grade_question_cw7_3_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW7_3Evaluator(BaseEvaluator):
    """
    Evaluator for Question 7_3: Wilcoxon Signed Rank Test, Approach Justification, Table 2, and Inference.

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
        Check if required elements (test value, approach, table, inference) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "test_value_present": False,
            "wilcoxon_named": False,
            "shapiro_wilk_referenced": False,
            "table_introduced": False,
            "inference_present": False,
        }

        evidence = []

        # Checkpoint 1 — Test value 73
        if re.search(r'\b73\b', text_lower):
            elements_found["test_value_present"] = True
            evidence.append("Test value 73 found")
        else:
            evidence.append("Test value 73 NOT found")

        # Checkpoint 2 — Wilcoxon named
        if re.search(r'wilcoxon', text_lower):
            elements_found["wilcoxon_named"] = True
            evidence.append("Wilcoxon named")
        else:
            evidence.append("Wilcoxon NOT named")

        # Checkpoint 3 — Shapiro-Wilk referenced
        if re.search(r'shapiro', text_lower):
            elements_found["shapiro_wilk_referenced"] = True
            evidence.append("Shapiro-Wilk referenced")
        else:
            evidence.append("Shapiro-Wilk NOT referenced")

        # Checkpoint 4 — Table 2 introduced
        if re.search(r'table\s*2', text_lower) and \
                re.search(r'presents|shows|displays|below|following', text_lower):
            elements_found["table_introduced"] = True
            evidence.append("Table 2 introduction found")
        else:
            evidence.append("Table 2 introduction NOT found")

        # Checkpoint 5 — Inference present (reject/fail to reject null hypothesis)
        if re.search(r'reject', text_lower) and re.search(r'null hypothesis', text_lower):
            elements_found["inference_present"] = True
            evidence.append("Inference conclusion found")
        else:
            evidence.append("Inference conclusion NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_question_cw7_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 7_3: Wilcoxon Signed Rank test, approach justification, Table 2, and inference.
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
                feedback="[TEST MODE] Good application of Wilcoxon test with proper justification and inference.",
                vibe="Student demonstrates solid understanding of non-parametric testing and APA reporting",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "test_value_present": True,
                            "wilcoxon_named": True,
                            "shapiro_wilk_referenced": True,
                            "table_introduced": True,
                            "inference_present": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["did you apply"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 3. Tick out the default Student box and tick in Wilcoxon Signed Rank one, with the same figure in Test value box, at significance level α = 0.05. What is the Test Value in this case and where does it come from? (5 points) Which approach did you apply to determine whether men score differently than women on a test of indoor gardening (X̄ = 73), parametric or non-parametric, and why? (5 points). Include the Descriptive statistic table, introduce, refer to, and number it, title it in APA-style (5 points). What are the mean and median scores for men? Write these statistics down in APA style. (5 points).

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

**Component 2: Test Value (4 points):**
- 2 points: Test value is correctly stated as 73
- 2 points: Source is correctly identified as the female mean (X̄ = 73), used as an estimate of the population mean
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Approach Justification (4 points):**
- 1 point: Non-parametric approach is named
- 1 point: Wilcoxon Signed Rank test is named
- 2 points: The choice is explicitly linked to the Shapiro–Wilk result from Task 2 (normality assumption violated)
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Table 2 (5 points):**
- 1 point: Introductory phrase present before the table
- 1 point: Reference to table number in the introductory phrase
- 1 point: Standalone table number present
- 1 point: Table title present
- 1 point: Table itself present
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: Inference (5 points):**
- 1 point: Decision rule stated (reject null hypothesis if p < α)
- 1 point: Correct α = 0.05 stated
- 1 point: Test statistic V reported
- 1 point: p-value reported
- 1 point: Conclusion stated (men's scores differ significantly from the population mean of 73)
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
The Test Value is 73. It comes from the female mean (X̄ = 73), which was used as an estimate of the population mean under the assumption that men and women belong to the same population with respect to indoor gardening ability. A non-parametric approach was applied — specifically, the Wilcoxon Signed Rank test. This decision was justified by the result of the Shapiro–Wilk test conducted in Task 2, which showed that the distribution of men's scores significantly deviates from normality (W = 0.764, p < 0.001). Since the normality assumption was violated, the parametric one-sample t-test is inappropriate, and its non-parametric equivalent — the Wilcoxon Signed Rank test — was applied instead. The results of the Wilcoxon Signed Rank test are presented in Table 2. Table 2 shows that the test statistic is V = 136.000, p < .001. Table 2 One Sample T-Test (Wilcoxon Signed-Rank Test) V p V42 136.000 < .001 Note. For the Wilcoxon test, the alternative hypothesis specifies that the median is different from 0. Note. CI could not be computed for effect size, due to low sample size and/or extreme effect size. Note. Wilcoxon signed-rank test. The decision rule is to reject the null hypothesis if p < α. Here, α = 0.05, and the obtained value is p < .001. Since p < α, we reject the null hypothesis. Men's scores differ significantly from the assumed population mean of 73.

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
            "component_2_score": "Test Value",
            "component_3_score": "Approach Justification",
            "component_4_score": "Table 2",
            "component_5_score": "Inference",
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
            question_name="QUESTION 7_3",
            question_description="Wilcoxon Signed Rank + Approach Justification + Table 2 + Inference",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )