"""
cw12_2.py
Classwork 12: Spearman's Rho correlation
Bivariate normality check and justification for Spearman's correlation
Evaluation method name: def grade_question_cw12_2_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2

class CW12_2Evaluator(BaseEvaluator):
    """
    Task 2. Let's check normality assumption. Which method you are going to use?
    Which form of this method will you choose and why? (5 points).
    Include the table, number and name it (5 points).
    Choose significancy level 0.001. What is your decision rule to reject the null hypothesis
    about normality? How many normality violations do you see, if any? (5 points).
    If you see more than 5 normality violations, use it as a criterium for the form of
    correlation analysis choosing. Is this the case? Based on your assumptions checking results,
    choose the most appropriate correlational statistical method (5 points).

    Inherits common functionality from BaseEvaluator.
    """

    def __init__(self):
        """Initialize the evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
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
            "shapiro_wilk_method": False,
            "bivariate_form": False,
            "table_present": False,
            "normality_violations": False,
            "spearman_selected": False,
        }

        evidence = []

        # Checkpoint 1 — Shapiro-Wilk method named
        if re.search(r'shapiro[\s-]?wilk|shapiro\s*wilk', text_lower):
            elements_found["shapiro_wilk_method"] = True
            evidence.append("Shapiro-Wilk method found")
        else:
            evidence.append("Shapiro-Wilk method NOT found")

        # Checkpoint 2 — Bivariate form explicitly mentioned
        if re.search(r'bivariate\s*(normality|form|test)|bivariate', text_lower):
            elements_found["bivariate_form"] = True
            evidence.append("Bivariate form found")
        else:
            evidence.append("Bivariate form NOT found")

        # Checkpoint 3 — Table present
        if re.search(r'table\s*\d|p[\s-]?value|shapiro|bivariate\s*normality', text_lower):
            elements_found["table_present"] = True
            evidence.append("Table found")
        else:
            evidence.append("Table NOT found")

        # Checkpoint 4 — Normality violations mentioned
        if re.search(
                r'violation|normality\s*(not\s*met|violated|assumption)|not\s*normal|p\s*<\s*[.0]*0{0,1}1\b',
                text_lower
        ):
            elements_found["normality_violations"] = True
            evidence.append("Normality violations mentioned")
        else:
            evidence.append("Normality violations NOT mentioned")

        # Checkpoint 5 — Spearman selected
        if re.search(r'spearman', text_lower):
            elements_found["spearman_selected"] = True
            evidence.append("Spearman's correlation found")
        else:
            evidence.append("Spearman's correlation NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_question_cw12_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 12.2: Bivariate Normality Check and Spearman Justification.

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
                feedback="[TEST MODE] Shapiro-Wilk test in bivariate form is applied correctly",
                vibe="Student demonstrates clear understanding of bivariate normality and Spearman justification",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "task_description": True,
                            "shapiro_wilk_method": True,
                            "bivariate_form": True,
                            "table_present": True,
                            "normality_violations": True,
                            "spearman_selected": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["if you see", "is this the case"]
        )

        prompt = f"""You are grading a statistics assignment about bivariate normality checking and justification for Spearman's correlation using a **STRICT rubric-based approach.

**TASK DESCRIPTION:**
Task 2. Let's check normality assumption. Which method you are going to use? Which form of this method will you choose and why? (5 points). Include the table, number and name it (5 points). Choose significancy level 0.001. What is your decision rule to reject the null hypothesis about normality? How many normality violations do you see, if any? (5 points). If you see more than 5 normality violations, use it as a criterium for the form of correlation analysis choosing. Is this the case? Based on your assumptions checking results, choose the most appropriate correlational statistical method (5 points).

Total: 20 points
 
STUDENT ANSWER:
{student_answer}

**IMPORTANT NOTES:**
- Students submit text descriptions of their work since visual elements (actual tables, screenshots, formatted documents) cannot be captured in text
- If student REFERENCES or DESCRIBES the required elements (e.g., "I used APA format", "I inserted the table"), ASSUME they completed it in their actual document
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
Proper autoformatting and structure (1 point if True): {formatting_check['elements_found']['autoformatting']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC DETECTION:**
{element_check['elements_found']}

**RUBRIC:**

**Component 1: Formatting (2 points):**
Use AUTOMATIC FORMATTING DETECTION RESULT above.
- 1 point: Task description correctly formatted
- 1 point: Proper autoformatting and structure
 
**Component 2: Bivariate Normality Naming (4 points):**
- 2 points: Shapiro-Wilk method explicitly named in the text (e.g., "We use Shapiro-Wilk test")
- 2 points: Bivariate form explicitly chosen AND a reason given (e.g., "we use bivariate form because correlation is not univariate but bivariate")
- CRITICAL: Both the test name AND the bivariate form must be stated in the text, not only in a table header
- CRITICAL: The justification for bivariate form must be present to receive the 2 points for form; naming the form alone without reasoning is 1 point
 
**Component 3: Table 1 (5 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Introductory phrase present before the table
- 1 point: Reference to table number in the introductory phrase (e.g., "Table 1 presents...")
- 1 point: Standalone table number present (e.g., "Table 1")
- 1 point: Descriptive table title present (e.g., "Shapiro-Wilk Test for Bivariate Normality")
- 1 point: Table itself present and referenced
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text
 
**Component 4: Normality Violations (4 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Decision rule explicitly stated (e.g., "reject H0 if p < α")
- 1 point: Mention of variable pairs (not individual variables) in the context of violations
- 1 point: Statistical inference stated with reference to the significance level α = 0.001 (e.g., "since p < .001, normality is violated")
- 1 point: The "more than 5 violations" criterion explicitly mentioned as the decision criterion for method selection
- CRITICAL: Student must refer to variable pairs, not individual variables, to earn the pair-mention point
- CRITICAL: α must be set to 0.001 as instructed; using a different α (e.g., 0.05) loses the inference point
 
**Component 5: Method Selection (5 points):**
Use AUTOMATIC DETECTION above.
- 2 points: Spearman's rank-order (or Spearman's) correlation explicitly named as the selected method
- 3 points: Correct justification — must explain that Spearman's is chosen as the nonparametric alternative because normality assumption was violated (all three ideas needed for full 3 points: nonparametric, alternative to parametric, due to normality violation)
- CRITICAL: Simply naming Spearman without justification gives 2 points only
- CRITICAL: Justification that only partially covers the three ideas receives 1 or 2 of the 3 justification points proportionally

**CORRECT ANSWER REFERENCE:**
We checked the normality assumption in JASP using Shapiro-Wilk test for bivariate normality. We use Bivariate Normality form of test, because correlational analysis (as analysis of relationship) is not univariate, it is bivariate.
Table 1 presents Shapiro-Wilk test for Bivariate Normality for all variable pairs.
Table 1
Shapiro-Wilk Test for Bivariate Normality
[table with variable pairs, Shapiro-Wilk statistic, and p-values all < .001]
 
The decision rule is to reject the null hypothesis of normality only if p < α.
Since all tested variable pairs showed significant violations of normality (p < .001) the assumption of bivariate normality was not met. More than five normality violations were identified; therefore, Spearman's rank-order correlation is the appropriate statistical method.
 
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
            "component_2_score": "Bivariate Normality Naming",
            "component_3_score": "Table 1",
            "component_4_score": "Normality Violations",
            "component_5_score": "Method Selection",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "STRICT",
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
            question_name="QUESTION 12_2",
            question_description="Normality Assumption Checking and Correlation Method Selection",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )
