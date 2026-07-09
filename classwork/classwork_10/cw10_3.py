"""
cw10_3.py
Classwork 10: One Way ANOVA
ANOVA Selection, Hypotheses, and Welch's ANOVA Computation
Evaluation method name: def grade_cw10_3_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2

class CW10_3Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 10_3.

    Task 3. Use the Step system: Step 1. Based on your assumptions checking results, select the
    appropriate statistics. Justify your selection, i.e. explain why did you choose ANOVA and this
    specific form of ANOVA-related group of tests (5 points). Step 2. State hypotheses. If it needs
    the math form, apply it. If it doesn't, explain why. (5 points). Step 3. State the significance
    level α, calculate df, find the critical value. (5 points). Step 4. Compute the test statistic.
    Make the inference in terms of hypotheses statement (5 points).

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
            "welchs_anova_selected": False,
            "ttest_ruled_out": False,
            "kruskal_wallis_ruled_out": False,
            "one_way_anova_ruled_out": False,
            "h0_math_form": False,
            "h1_verbal_statement": False,
            "alpha_stated": False,
            "df_values": False,
            "table_present": False,
            "f_cv_comparison": False,
            "reject_h0": False,
        }

        evidence = []

        # Checkpoint 1 — Welch's ANOVA selected
        if re.search(r"welch'?s?\s*anova", text_lower):
            elements_found["welchs_anova_selected"] = True
            evidence.append("Welch's ANOVA selection found")
        else:
            evidence.append("Welch's ANOVA selection NOT found")

        # Checkpoint 2 — t-test ruled out
        if re.search(r"t-?test", text_lower) and re.search(r"more than two|two groups|rul(e|ing)\s*out", text_lower):
            elements_found["ttest_ruled_out"] = True
            evidence.append("t-test ruled out found")
        else:
            evidence.append("t-test ruled out NOT found")

        # Checkpoint 3 — Kruskal-Wallis ruled out (normality met)
        if re.search(r"kruskal[\s-]?wallis", text_lower):
            elements_found["kruskal_wallis_ruled_out"] = True
            evidence.append("Kruskal-Wallis ruled out found")
        else:
            evidence.append("Kruskal-Wallis ruled out NOT found")

        # Checkpoint 4 — Standard one-way ANOVA ruled out (unequal variances, Levene's)
        if re.search(r"levene", text_lower) and re.search(r"unequal\s*varian|not\s*equal\s*varian|heterogene", text_lower):
            elements_found["one_way_anova_ruled_out"] = True
            evidence.append("One-way ANOVA ruled out (Levene's) found")
        else:
            evidence.append("One-way ANOVA ruled out (Levene's) NOT found")

        # Checkpoint 5 — H0 in math form
        if re.search(r"μ1\s*=\s*μ2\s*=\s*μ3\s*=\s*μ4\s*=\s*μ5|mu1\s*=\s*mu2\s*=\s*mu3\s*=\s*mu4\s*=\s*mu5", text_lower):
            elements_found["h0_math_form"] = True
            evidence.append("H0 math form found")
        else:
            evidence.append("H0 math form NOT found")

        # Checkpoint 6 — H1 verbal statement
        if re.search(r"at\s*least\s*one\s*mean.{0,20}differ", text_lower):
            elements_found["h1_verbal_statement"] = True
            evidence.append("H1 verbal statement found")
        else:
            evidence.append("H1 verbal statement NOT found")

        # Checkpoint 7 — Significance level alpha = .05
        if re.search(r"α\s*=\s*0?\.?05|alpha\s*=\s*0?\.?05", text_lower):
            elements_found["alpha_stated"] = True
            evidence.append("α = .05 found")
        else:
            evidence.append("α = .05 NOT found")

        # Checkpoint 8 — df values (Welch-Satterthwaite: df1 = 4, df2 = 61)
        if re.search(r"df\s*1?\s*=\s*4\b", text_lower) and re.search(r"df\s*2?\s*=\s*61\b", text_lower):
            elements_found["df_values"] = True
            evidence.append("df1 = 4, df2 = 61 found")
        else:
            evidence.append("df1 = 4, df2 = 61 NOT found")

        # Checkpoint 9 — Table reference
        if re.search(r'table\s*\d', text_lower):
            elements_found["table_present"] = True
            evidence.append("Table reference found")
        else:
            evidence.append("Table reference NOT found")

        # Checkpoint 10 — F vs CV comparison
        if re.search(r"5\.445", text_lower) and re.search(r"2\.52", text_lower):
            elements_found["f_cv_comparison"] = True
            evidence.append("F (5.445) vs CV (2.52) comparison found")
        else:
            evidence.append("F (5.445) vs CV (2.52) comparison NOT found")

        # Checkpoint 11 — Reject H0
        if re.search(r"reject.{0,20}(null|h0)", text_lower):
            elements_found["reject_h0"] = True
            evidence.append("Reject H0 conclusion found")
        else:
            evidence.append("Reject H0 conclusion NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_cw10_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 10.3: Test Selection, Hypotheses, and Welch's ANOVA Computation.
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
                    "component_3_score": 3,
                    "component_4_score": 3,
                    "component_5_score": 4,
                },
                max_points=20,
                feedback="[TEST MODE] Test selection justified with most exclusions covered. Hypotheses and df/CV reported with minor gaps.",
                vibe="Student shows solid understanding of test selection and Welch's ANOVA computation",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "welchs_anova_selected": True,
                            "ttest_ruled_out": True,
                            "kruskal_wallis_ruled_out": True,
                            "one_way_anova_ruled_out": True,
                            "h0_math_form": True,
                            "h1_verbal_statement": True,
                            "alpha_stated": True,
                            "df_values": True,
                            "table_present": True,
                            "f_cv_comparison": True,
                            "reject_h0": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - partial elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["justify your selection"]
        )

        prompt = f"""You are grading a statistics assignment about test selection, hypotheses, and Welch's ANOVA computation using a **STRICT rubric-based approach.

**TASK DESCRIPTION:**
Task 3. Use the Step system: Step 1. Based on your assumptions checking results, select the appropriate statistics. Justify your selection, i.e. explain why did you choose ANOVA and this specific form of ANOVA-related group of tests (5 points). Step 2. State hypotheses. If it needs the math form, apply it. If it doesn't, explain why. (5 points). Step 3. State the significance level α, calculate df, find the critical value. (5 points). Step 4. Compute the test statistic. Make the inference in terms of hypotheses statement (5 points).

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

**Component 2: Test selection justification (5 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Selecting ANOVA family (more than two groups, comparing means)
- 1 point: Selecting Welch's ANOVA specifically
- 1 point: Ruling out t-test
- 1 point: Ruling out Kruskal-Wallis (normality met)
- 1 point: Ruling out standard one-way ANOVA (unequal variances per Levene's)
- CRITICAL: Score ONLY against these sub-points; any criterion not listed here does not exist and must not affect the score

**Component 3: Hypotheses (4 points):**
Use AUTOMATIC DETECTION above.
- 1 point: H0 in math form (μ1 = μ2 = μ3 = μ4 = μ5)
- 1 point: H1 verbal statement (at least one mean is different)
- 2 points: Explanation of why H1 has no math form
- CRITICAL: Score ONLY against these sub-points; any criterion not listed here does not exist and must not affect the score

**Component 4: Significance level, df, critical value (4 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Significance level stated
- 1 point: α = .05
- 1 point: df1 = 4 (Welch-Satterthwaite numerator df)
- 1 point: df2 = 61 (Welch-Satterthwaite denominator df)
- CRITICAL: Score ONLY against these sub-points; any criterion not listed here does not exist and must not affect the score

**Component 5: Test statistic and inference (5 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Introductory phrase with reference to the table number
- 1 point: Table number
- 1 point: Table title
- 1 point: Comparing F (5.445) to CV (2.52)
- 1 point: Rejecting H0 with correct conclusion
- CRITICAL: Score ONLY against these sub-points; any criterion not listed here does not exist and must not affect the score

**CORRECT ANSWER REFERENCE:**
Step 1. We select Welch's ANOVA test because: (1) the independent variable has more than two groups, ruling out a t-test; (2) normality assumption is met, ruling out Kruskal-Wallis; (3) Levene's test indicated unequal variances across groups, ruling out one-way ANOVA.
Step 2. H0: μ1 = μ2 = μ3 = μ4 = μ5. H1: at least one mean is different. H1 is not stated in math form because, unlike a two-group comparison, there is no single equation that expresses "at least one mean differs" for more than two groups — it can only be expressed verbally or as a logical negation of H0.
Step 3. The significance level α = 0.05 (default, not specified in the task). df1 = 4; df2 = 61. According to the F-Table of Critical Values for Significance Level = 0.05, the CV is 2.522.
Step 4. Table 2 presents Welch's ANOVA results for Facebook friends. Table 2, Statistics for given variable, shows F = 5.445, p < .001, η² = 0.114. Since F > CV, we reject the null hypothesis.

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
  "component_2_score": <0-5>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-4>,
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
            "component_2_score": "Test Selection Justification",
            "component_3_score": "Hypotheses",
            "component_4_score": "Significance Level, df, Critical Value",
            "component_5_score": "Test Statistic and Inference",
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
            question_name="QUESTION 10_3",
            question_description="Test Selection, Hypotheses, and Welch's ANOVA Computation",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )