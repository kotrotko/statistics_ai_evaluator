"""
cw9_3.py
Classwork 9: Independent groups t-test
Assumption checking: homogeneity of variance
Evaluation method name: def grade_question_cw9_3_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW9_3Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 9_3: Assumption Checking - Homogeneity of Variance.

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
        Check if required elements (variance method, table, homogeneity conclusion, method choice) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "variance_method": False,
            "table_present": False,
            "homogeneity_conclusion": False,
            "method_choice": False,
        }

        evidence = []

        # Checkpoint 1 — Variance homogeneity method (Levene's test)
        if re.search(r'levene[\s\']?s?\s*test', text_lower) and \
                re.search(r'variance|homogeneity|equality', text_lower):
            elements_found["variance_method"] = True
            evidence.append("Variance homogeneity method found")
        else:
            evidence.append("Variance homogeneity method NOT found")

        # Checkpoint 2 — Table 2 present with introductory phrase and table number reference
        table_ref_patterns = [
            r'table\s*2\b',
            r'\(\s*table\s*2\s*\)',
        ]
        intro_patterns = [
            r'presents|shows|displays|below|following|applied|conducted|used',
        ]
        table_ref_found = any(re.search(p, text_lower) for p in table_ref_patterns)
        intro_found = any(re.search(p, text_lower) for p in intro_patterns)
        if table_ref_found and intro_found:
            elements_found["table_present"] = True
            elements_found["table_intro_with_ref"] = True
            evidence.append("Table 2 with introductory phrase and table number reference found")
        else:
            elements_found["table_intro_with_ref"] = False
            evidence.append("Table 2 introductory phrase with number reference NOT found")

        # Checkpoint 3 — Homogeneity conclusion
        homogeneity_patterns = [r'variances?\s*(are\s*)?(homogeneous|homogenous|equal)',
                                 r'fail\s*to\s*reject', r'homogeneity\s*(is\s*)?(satisfied|met|confirmed)',
                                 r'p\s*[=>.]\s*[\.\d]+', r'α\s*=\s*0\.05']
        homogeneity_count = sum(1 for p in homogeneity_patterns if re.search(p, text_lower))
        if homogeneity_count >= 2:
            elements_found["homogeneity_conclusion"] = True
            evidence.append("Homogeneity conclusion found")
        else:
            evidence.append("Homogeneity conclusion NOT found")

        # Checkpoint 4 — Method choice based on assumptions
        method_patterns = [r'student[\s\']?s?\s*t[\s-]?test', r'equal\s*variances?\s*assumed',
                           r'standard\s*form', r'normality', r'homogeneity']
        method_count = sum(1 for p in method_patterns if re.search(p, text_lower))
        if method_count >= 2:
            elements_found["method_choice"] = True
            evidence.append("Method choice with justification found")
        else:
            evidence.append("Method choice with justification NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_question_cw9_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 9.3: Assumption Checking - Homogeneity of Variance.
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
                    "component_2_score": 3,
                    "component_3_score": 5,
                    "component_4_score": 5,
                    "component_5_score": 5,

                },
                max_points=20,
                feedback="[TEST MODE] Method stated. Table present with good APA formatting. Homogeneity conclusion clear with proper reasoning. Method choice justified.",
                vibe="Student demonstrates solid understanding of variance homogeneity testing and method selection",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "variance_method": True,
                            "table_present": True,
                            "homogeneity_conclusion": True,
                            "method_choice": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )
        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["will you apply", "how did you know"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 3. Assumption checking: homogeneity of variance. Which method will you apply to check variance homogeneity? (5 points).
Include the relevant table in APA style (5 points).
Are the variances homogenous, with significance level α = 0.05? How did you know? Describe your logic (5 points).
Based on normality and homogeneity of variance checking result, determine which form of the chosen statistical method should be applied and justify your decision (5 points).

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

**Component 2: Method Name (3 points):**
- 3/3: Levene's test explicitly named as the method for checking homogeneity of variance, stated in a sentence or in the table introduction phrase
- 1/3: Levene's test mentioned but only in a table header, not in a sentence or introduction phrase
- 0/3: No method named at all
- CRITICAL: Mention only in a table header does NOT earn full credit

**Component 3: Table 2 (5 points):**
- 1 point: Introductory phrase present before the table — use AUTOMATIC DETECTION: award if table_intro_with_ref is True
- 1 point: Reference to the table number in the introductory phrase — use AUTOMATIC DETECTION: award if table_intro_with_ref is True- 1 point: Standalone table number present (e.g., "Table 2")
- 1 point: Table title present
- 1 point: Table 2 itself present
- CRITICAL: Do NOT assume elements are present if not explicitly written in the
student's text

**Component 4: Inference (5 points):**
- 1 point: Decision rule stated (reject H₀ only if p < α)
- 1 point: Correct obtained p value reported (p = .132 specifically; other p values from different tests do not count)
- 1 point: Correct significance level stated (α = .05 specifically; α = .001 from normality check does not count)
- 1 point: Correct conclusion stated (fail to reject H₀, variances are homogeneous)
- 1 point: Explicit comparison of obtained p to α
- CRITICAL: Do NOT assume elements are present if not explicitly written in the
student's text

**Component 5: Final Determination (5 points):**
- 1 point: References the normality checking result
- 1 point: References the homogeneity of variance checking result
- 3 points: Names Student's t-test (equal variances assumed) as the chosen form
- CRITICAL: Do NOT assume elements are present if not explicitly written in the
student's text

**CORRECT ANSWER REFERENCE:**
Homogeneity of variance was checked using Levene's test. Table 2 presents the results of Levene's test for equality of variances conducted in JASP for the dependent variable drp.
Table 2
Test of Equality of Variances (Levene's)
        F    df1   df2    p
drp  2.362    1    42   .132
The decision rule is to reject the null hypothesis of equal variances only if p < α. Here, the significance level is α = 0.05, and the obtained value is p = .132. Since p > α, we fail to reject the null hypothesis of equal variances. Therefore, the variances are considered homogeneous at the α = 0.05 significance level.
Since the normality assumption was satisfied (Shapiro–Wilk, p = .396 > .001) and the homogeneity of variance assumption was also satisfied (Levene's, p = .132 > .05), the standard form of the independent samples t-test — Student's t-test assuming equal variances — is appropriate and will be applied.

{FEEDBACK_RULES}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-3>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-5>,
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
            "component_2_score": "Method Name",
            "component_3_score": "Table 2 (APA Style)",
            "component_4_score": "Inference",
            "component_5_score": "Final Determination",
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
            "component_2_score": 3,
            "component_3_score": 5,
            "component_4_score": 5,
            "component_5_score": 5,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="CLASSWORK 9_3",
            question_description="Assumption Checking: Homogeneity of Variance",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )
