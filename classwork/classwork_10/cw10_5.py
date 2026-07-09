"""
cw10_5.py
Classwork 10: One-Way ANOVA
Welch's ANOVA Summary and Research Question Answer
Evaluation method name: def grade_cw10_5_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2

class CW10_5Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 10_5.

    Task 5. Summary: Describe your results briefly, following example on 12:48 and 13:07 of our video (10 points).
    Answer the main Research question (10 points). Your answer should be aligned with the results and phrased
    in terms of group differences (or lack thereof).

    Inherits common functionality from BaseEvaluator.
    """

    def __init__(self):
        """Initialize the evaluator with API handler."""
        super().__init__(
            temperature=0.3,
            max_tokens=1200
        )
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
            "welch_f_stat": False,
            "p_value": False,
            "effect_size": False,
            "post_hoc_result": False,
            "null_hypothesis_decision": False,
            "group_difference_phrasing": False,
        }

        evidence = []

        # Checkpoint 1 — Welch's F statistic
        if re.search(r"welch'?s?\s*f\s*\(\s*\d+(\.\d+)?\s*,\s*\d+(\.\d+)?\s*\)\s*=\s*\d+(\.\d+)?", text_lower):
            elements_found["welch_f_stat"] = True
            evidence.append("Welch's F statistic found")
        else:
            evidence.append("Welch's F statistic NOT found")

        # Checkpoint 2 — p-value
        if re.search(r"p\s*[<=]\s*\.?\d+", text_lower):
            elements_found["p_value"] = True
            evidence.append("p-value found")
        else:
            evidence.append("p-value NOT found")

        # Checkpoint 3 — Effect size (eta squared)
        if re.search(r"η²|eta\s*squared|eta2|\bη\^?2\b", text_lower):
            elements_found["effect_size"] = True
            evidence.append("Effect size (η²) found")
        else:
            evidence.append("Effect size (η²) NOT found")

        # Checkpoint 4 — Post hoc result
        if re.search(r"post[\s-]?hoc", text_lower):
            elements_found["post_hoc_result"] = True
            evidence.append("Post hoc result found")
        else:
            evidence.append("Post hoc result NOT found")

        # Checkpoint 5 — Null hypothesis decision
        if re.search(r"null\s*hypothesis\s*(is\s*)?(rejected|not\s*rejected|fail(ed)?\s*to\s*reject)", text_lower):
            elements_found["null_hypothesis_decision"] = True
            evidence.append("Null hypothesis decision found")
        else:
            evidence.append("Null hypothesis decision NOT found")

        # Checkpoint 6 — Group difference phrasing
        if re.search(r"group[s]?\s*(difference|differ|significantly\s*more|significantly\s*less)", text_lower):
            elements_found["group_difference_phrasing"] = True
            evidence.append("Group difference phrasing found")
        else:
            evidence.append("Group difference phrasing NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_cw10_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 10.5: Summary and Research Question Answer.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_2_score": 7,
                    "component_3_score": 8,
                },
                max_points=20,
                feedback="[TEST MODE] Summary mostly complete with minor gaps. Research question answer aligned with results.",
                vibe="Student demonstrates solid grasp of Welch's ANOVA summary and research question interpretation",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "welch_f_stat": True,
                            "p_value": True,
                            "effect_size": True,
                            "post_hoc_result": True,
                            "null_hypothesis_decision": True,
                            "group_difference_phrasing": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - partial elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["describe your results"]
        )

        prompt = f"""You are grading a statistics assignment about Welch's ANOVA summary and research question interpretation using a **STRICT rubric-based approach.

**TASK DESCRIPTION:**
Task 5. Summary: Describe your results briefly, following example on 12:48 and 13:07 of our video (10 points). Answer the main Research question (10 points). Your answer should be aligned with the results and phrased in terms of group differences (or lack thereof).

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
- 1 point: Task description correctly formatted
- 1 point: Lack of auto-formatting

**Component 2: Summary (9 points):**
Use AUTOMATIC DETECTION above.
- 2 points: Welch's F(4, 61.144) = 5.445 correctly reported
- 2 points: p < .001 correctly reported
- 2 points: η² = 0.114 reported with effect size interpretation (does not exceed threshold for a large effect; % of variance explained)
- 3 points: Post hoc result correctly reported (Group 302 vs Group 902 significant, p = .017, correct direction, no other comparisons significant)
- CRITICAL: Score ONLY against these sub-points; any criterion not listed here does not exist and must not affect the score

**Component 3: Research question answer (9 points):**
- 4 points: States the null hypothesis is rejected
- 5 points: Phrases the answer in terms of group differences, tied to the research question (i.e., number of Facebook friends affects perceived social attractiveness; Group 302 rated significantly more socially attractive than Group 902)
- CRITICAL: Answer must be aligned with the results and phrased in terms of group differences (or lack thereof), not just a restatement of the statistical decision

**CORRECT ANSWER REFERENCE:**
There was a significant difference among the five experimental groups on social attractiveness ratings, Welch's F(4, 61.144) = 5.445, p < .001, η² = 0.114. This effect size does not exceed the threshold for a large effect, meaning the independent variable explains 11.4% of the total variance in attractiveness rating. Post hoc comparisons revealed that profiles with a moderate number of friends (Group 302) were rated as significantly more socially attractive than profiles with a high number of friends (Group 902), p = .017. No other pairwise comparisons reached significance.
The null hypothesis is rejected. Profiles with a moderate number of friends (Group 302) were rated as significantly more socially attractive than profiles with a high number of friends (Group 902), indicating that the number of Facebook friends affects perceived social attractiveness.

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
  "component_2_score": <0-9>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-9>,
  "component_3_explanation": "<brief>",
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
            "component_2_score": "Summary",
            "component_3_score": "Research Question Answer",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 9,
            "component_3_score": 9,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 10_5",
            question_description="Summary and Research Question Answer",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )