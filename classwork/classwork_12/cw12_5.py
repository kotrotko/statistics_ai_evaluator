"""
cw12_5.py
Classwork 12: Correlational Analysis
Correlation Summary
Evaluation method name: def grade_cw12_5_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2

class CW12_5Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 12_5.

    Task 5. Summary: Add a Heatmap, introduce, number, and title it as a Figure (5 points).
    Describe your results following the example on 15.03 and 15.18 minutes of Dr.Todd's video
    (5 points). Answer the main Research question (5 points). Your answer should be aligned with
    the results and phrased in terms of correlation (or lack thereof). (5 points).

    Inherits common functionality from BaseEvaluator.
    """

    def __init__(self):
        """Initialize the evaluator with API handler."""
        super().__init__()
        # Initialize output formatter
        self.formatter = OutputFormatter(default_width=60)

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check if required elements are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "figure_introduced": False,
            "negative_relationship_present": False,
            "positive_relationship_present": False,
            "rq_yes_decision": False,
            "correlation_phrasing": False,
            "exception_noted": False,
        }

        evidence = []

        # Checkpoint 1 — Figure 2 introduced
        if re.search(r'figure\s*2', text_lower) and \
                re.search(r'presents|shows|displays|below|following', text_lower):
            elements_found["figure_introduced"] = True
            evidence.append("Figure 2 introduction found")
        else:
            evidence.append("Figure 2 introduction NOT found")

        # Checkpoint 2 — Negative relationship with rs, df, p
        if re.search(r'-\.?\d+.{0,30}rs\s*\(\s*115\s*\)|rs\s*\(\s*115\s*\)\s*=\s*-\.?\d+', text_lower):
            elements_found["negative_relationship_present"] = True
            evidence.append("Negative relationship with rs/df/p found")
        else:
            evidence.append("Negative relationship with rs/df/p NOT found")

        # Checkpoint 3 — Positive relationship with rs, df, p
        if re.search(r'rs\s*\(\s*115\s*\)\s*=\s*\.?\d+', text_lower):
            elements_found["positive_relationship_present"] = True
            evidence.append("Positive relationship with rs/df/p found")
        else:
            evidence.append("Positive relationship with rs/df/p NOT found")

        # Checkpoint 4 — RQ "Yes" decision
        if re.search(r'\byes\b.{0,30}(rq|research\s*question)|(rq|research\s*question).{0,30}\byes\b', text_lower):
            elements_found["rq_yes_decision"] = True
            evidence.append("RQ 'Yes' decision found")
        else:
            evidence.append("RQ 'Yes' decision NOT found")

        # Checkpoint 5 — Correlation/linear relationship phrasing
        if re.search(r'correlat|linear\s*relationship|monotonic', text_lower):
            elements_found["correlation_phrasing"] = True
            evidence.append("Correlation/linear relationship phrasing found")
        else:
            evidence.append("Correlation/linear relationship phrasing NOT found")

        # Checkpoint 6 — Exception (scale11) noted
        if re.search(r'scale\s*11', text_lower):
            elements_found["exception_noted"] = True
            evidence.append("Exception (scale11) noted")
        else:
            evidence.append("Exception (scale11) NOT noted")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_cw12_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 12.5: Heatmap, Results Summary, and Research Question Answer.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

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
                feedback="[TEST MODE] Heatmap correctly introduced, results follow Dr. Todd's format, RQ answer aligned with results.",
                vibe="Student demonstrates solid grasp of correlation summary and research question interpretation",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "figure_introduced": True,
                            "negative_relationship_present": True,
                            "positive_relationship_present": True,
                            "rq_yes_decision": True,
                            "correlation_phrasing": True,
                            "exception_noted": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["describe your", "your answer"]
        )

        prompt = f"""You are grading a statistics assignment about correlation heatmap summary and research question interpretation using a **STRICT rubric-based approach.

**TASK DESCRIPTION:**
5. Summary: Add a Heatmap, introduce, number, and title it as a Figure (5 points). Describe your results following the example on 15.03 and 15.18 minutes of Dr.Todd's video (5 points). Answer the main Research question (5 points). Your answer should be aligned with the results and phrased in terms of correlation (or lack thereof). (5 points).

Total: 20 points

STUDENT ANSWER:
{student_answer}

**IMPORTANT NOTES:**
- Students submit text descriptions of their work since visual elements (actual diagrams, screenshots, formatted documents) cannot be captured in text
- If student REFERENCES or DESCRIBES the required elements, ASSUME they completed it in their actual document
- DO NOT penalize for "missing" visual elements if they clearly describe what they did

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Reasoning is required; calculations are mandatory
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. Award partial credit where reasoning is mostly correct but incomplete
6. It is expected to see both student's logic and calculations, not only the final answer
7. Explanations must be SPECIFIC and ACTIONABLE - avoid vague phrases like "lacks depth", "could be better", "needs improvement". Instead, point to what is actually missing or what was done well.

**HYBRID GRADING APPROACH:**

**AUTOMATIC FORMATTING DETECTION RESULT:**
Task description correctly formatted (1 point if True): {formatting_check['elements_found']['task_description']}
Lack of auto-formatting (1 point if True): {formatting_check['elements_found']['autoformatting']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC DETECTION:**
{element_check['elements_found']}

**RUBRIC:**

**Component 1: Formatting (2 points):**
Use AUTOMATIC FORMATTING DETECTION RESULT above.
- 1 point: Task description
- 1 point: Lack of auto-formatting

**Component 2: Heatmap (4 points):**
- 1 point: Introductory phrase
- 1 point: Reference to the figure number in the introductory phrase
- 1 point: Standalone figure number and title
- 1 point: The figure itself
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Results (5 points):**
- 1 point: Any stating the negative relationship with rs, df, and p
- 1 point: Any stating the positive relationship with rs, df, and p
- 3 points: Following the comparative sentence structure ("more strongly related to X than to Y")
- CRITICAL: Score ONLY against these sub-points; any criterion not listed here does not exist and must not affect the score

**Component 4: Answer to RQ (4 points):**
- 2 points: "Yes" decision stated
- 2 points: Full answer referencing 13 out of 15 significant pairs
- CRITICAL: Score ONLY against these sub-points; any criterion not listed here does not exist and must not affect the score

**Component 5: Phrasing aligned with results, in terms of correlation (5 points):**
- 1 point: Framing the answer in terms of correlation/linear relationship rather than causal language
- 1 point: Stating that most variables are correlated with one another
- 1 point: Identifying the exception (scale11 pairings not significant)
- 2 points: The conclusion being consistent with the numeric results reported in Component 3
- CRITICAL: Score ONLY against these sub-points; any criterion not listed here does not exist and must not affect the score

**CORRECT ANSWER REFERENCE:**
Figure 2 presents the heatmap for the given variables. Figure 2. Heatmap for Given Variables. Scale10 was more negatively related to scale13, rs(115) = -.522, p < .001, than to scale12, rs(115) = -.453, p < .001. A complete list of correlations is presented in Table 2 and a heatmap of the variables is in Figure 2.
Answer to RQ: Yes, the results show statistically significant monotonic relationships among most of the selected variables, specifically 13 out of 15 pairs, with only the scale11 pairings failing to reach significance.

**FEEDBACK RULES**
- Identify which components were completed correctly
- Point out missing or incomplete elements explicitly
- Maintain supportive tone


Return JSON only:
{{
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
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative feedback>",
  "vibe": "<one-sentence overall impression>"
}}"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "element_check": element_check,
                "formatting_check": formatting_check
            }
        )

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
        """
        Display grading results using OutputFormatter.

        Args:
            grading: Grading result dictionary
        """
        # Define component labels
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Heatmap",
            "component_3_score": "Results",
            "component_4_score": "Answer to RQ",
            "component_5_score": "Phrasing Aligned with Results",
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
            question_name="QUESTION 12_5",
            question_description="Heatmap, Results Summary, and Research Question Answer",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )