"""
cw9_5.py
Classwork 9: Independent groups t-test
Statistical Analysis: Table + Inference + Cohen's d + Plot + APA Report + Research Question
Evaluation method name: def grade_cw9_5_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW9_5Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 9_5: Statistical Analysis and Interpretation.

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
        Check if required elements (table, inference, Cohen's d, plot, APA report) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "table_present": False,
            "inference_correct": False,
            "cohens_d_present": False,
            "plot_present": False,
        }

        evidence = []

        # Checkpoint 1 — Table 3 present
        if re.search(r'table\s*3', text_lower) and \
                re.search(r'presents|shown|results|following', text_lower):
            elements_found["table_present"] = True
            evidence.append("Table 3 found")
        else:
            evidence.append("Table 3 NOT found")

        # Checkpoint 2 — Statistical inference (t = 2.267, reject H0)
        t_patterns = [r't\s*=\s*2\.267', r't\s*\(\s*42\s*\)', r'2\.267']
        reject_patterns = [r'reject\s*h[₀0]', r'reject\s*the\s*null', r'p\s*=\s*\.014', r'p\s*<\s*α']
        t_found = any(re.search(p, text_lower) for p in t_patterns)
        reject_found = any(re.search(p, text_lower) for p in reject_patterns)
        if t_found and reject_found:
            elements_found["inference_correct"] = True
            evidence.append("t = 2.267 and reject H0 found")
        else:
            evidence.append("t statistic and/or rejection decision NOT found")

        # Checkpoint 3 — Cohen's d = 0.684
        cohens_patterns = [r'cohen', r'd\s*=\s*0\.684', r'd\s*=\s*\.684', r'effect\s*size']
        if any(re.search(p, text_lower) for p in cohens_patterns):
            elements_found["cohens_d_present"] = True
            evidence.append("Cohen's d found")
        else:
            evidence.append("Cohen's d NOT found")

        # Checkpoint 4 — Descriptive plot / Figure 1
        plot_patterns = [r'figure\s*1', r'descriptive\s*plot', r'descriptives\s*plot']
        if any(re.search(p, text_lower) for p in plot_patterns):
            elements_found["plot_present"] = True
            evidence.append("Descriptive plot / Figure 1 found")
        else:
            evidence.append("Descriptive plot / Figure 1 NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_cw9_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 9.5: Statistical Analysis and Interpretation.
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
                    "component_2_score": 6,
                    "component_3_score": 4,
                    "component_4_score": 4,
                    "component_5_score": 4,
                },
                max_points=20,
                feedback="[TEST MODE] Table present in APA style. Inference correct. Cohen's d and plot included. APA report complete.",
                vibe="Student demonstrates solid understanding of statistical analysis and interpretation for independent groups t-test",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "table_present": True,
                            "inference_correct": True,
                            "cohens_d_present": True,
                            "plot_present": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["please describe"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 5. Statistical analysis and interpretation. Using JASP, calculate the statistics and include the table in APA style. Make a statistical inference (reject or fail to reject the null hypothesis) (5 points). Include Cohen's d effect size and explain what it means. Add and describe the Descriptive plot (5 points). Please describe the result in APA style, following the example at 15:47 of our video (5 points). Answer the main research question (5 points).

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
- 1 point: Absence of autoformatting

**Component 2: Table 3 and Statistical inference (6 points):**
- 1 point: Introductory phrase with table number reference present before the table
- 1 point: Standalone table number present (e.g., "Table 3")
- 1 point: Table title present
- 1 point: Test statistic t(42) = 2.267 (or close) reported
- 1 point: Correct decision to reject H₀
- 1 point: Explicit comparison t > t* and/or p < α with correct critical value t* = +1.686
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Cohen's d and Descriptive plot (4 points):**
- 1 point: Cohen's d = 0.684 reported
- 1 point: Interpretation of effect size magnitude
- 1 point: Figure 1 present with introductory phrase, figure number, and title
- 1 point: At least one interpretive sentence about the plot
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Report (4 points):**
- 1 point: Normality result referenced
- 1 point: Homogeneity of variance result referenced
- 1 point: t(42) = 2.267, p = .014 (one-tailed) reported
- 1 point: d = 0.684 and its interpretation reported
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: Research question answer (4 points):**
- 2 points: Direct answer to the research question
- 2 points: Answer is correct
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text
**CORRECT ANSWER REFERENCE:**
An independent samples t-test was conducted in JASP to compare reading performance between the treatment and control groups. The results are presented in Table 3. Table 3 Independent Samples T-Test. drp: t = 2.267, df = 42, p = .014, Cohen's d = 0.684, SE Cohen's d = 0.318. Note. For all tests, the alternative hypothesis specifies that group Control is less than group Treat. Student's t-test. Statistical inference: The test statistic is t(42) = 2.267. The critical value is t* = +1.682. Since t = 2.267 > t* = 1.682, and p = .014 < α = .05, we reject H₀. The treatment group performed significantly better than the control group. Effect size: Cohen's d = 0.684. According to Cohen's guidelines, this represents a medium-to-large effect size, indicating that the treatment group scored approximately 0.68 standard deviations higher than the control group. Descriptive plot: The descriptive plot is presented in Figure 1. It shows the sample means and 95% confidence intervals for both groups. The mean for the Treatment group (M = 51.48) is visibly higher than the mean for the Control group (M = 41.52). The confidence intervals partially overlap. This does not contradict the significant t-test result — partial overlap of 95% CIs is compatible with statistical significance and is not a substitute for formal hypothesis testing. APA style report: Preliminary data screening confirmed normality (Shapiro–Wilk, p = .396 > .001) and homogeneity of variance (Levene's F = 2.362, p = .132 > .05). An independent samples t-test indicated that the treatment group scored significantly higher than the control group, t(42) = 2.267, p = .014 (one-tailed), d = 0.684. The mean for the Treatment group (M = 51.48, SD = 11.01) was significantly higher than the Control group (M = 41.52, SD = 17.15). Answer to research question: Directed reading activities significantly improved reading performance compared to the standard curriculum. H₀ is rejected.

{FEEDBACK_RULES}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-6>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-4>,
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
            "component_2_score": "Table 3 and Statistical inference",
            "component_3_score": "Cohen's d and Descriptive plot",
            "component_4_score": "Report",
            "component_5_score": "Research question answer",
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
            "component_2_score": 6,
            "component_3_score": 4,
            "component_4_score": 4,
            "component_5_score": 4,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="CLASSWORK 9_5",
            question_description="Statistical Analysis: Table + Inference + Cohen's d + Plot + APA Report + Research Question",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )