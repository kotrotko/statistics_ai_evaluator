"""
cw13_2.py
Classwork 13: Linear Regression
Assumption checking: residuals normality, outliers, homoscedasticity/linearity, method justification
Evaluation method name: def grade_question_cw13_2_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2

class CW13_2Evaluator(BaseEvaluator):
    """
    Evaluator for Linear Regression Assumptions Checking.

    Task 2. Check the residuals normality (Plots > Q-Q plot standardized residuals, 09:30). Include the plot, number and title it. (5 points). Check outliers (Statistics > Residuals > Statistics, 07:45). Include the table, number and title it. (5 points).  Visually check both the homoscedasticity and linearity (Plots > Residuals vs. predicted, 10:05). Include plot, number and title it. (5 points).  Name the method you choose based on the data level and justify it (i.e. explain why this method is suitable for our problem solving, based on the assumption checking) (5 points).

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
            "qq_plot_normality": False,
            "outliers_table": False,
            "homoscedasticity_plot": False,
            "step1_justification": False,
        }

        evidence = []

        # Checkpoint 1 — Q-Q plot / residuals normality check
        if re.search(r'q[\s-]?q\s*plot|quantile|standardized\s*residual|normality\s*(of\s*)?residual|residual\s*normality', text_lower):
            elements_found["qq_plot_normality"] = True
            evidence.append("Q-Q plot / residuals normality found")
        else:
            evidence.append("Q-Q plot / residuals normality NOT found")

        # Checkpoint 2 — Outliers table
        if re.search(r'outlier|cook|leverage|mahalanobis|residual\s*statistic|casewise|std\.\s*residual|standardized\s*residual', text_lower):
            elements_found["outliers_table"] = True
            evidence.append("Outliers / residuals statistics found")
        else:
            evidence.append("Outliers / residuals statistics NOT found")

        # Checkpoint 3 — Homoscedasticity / linearity plot
        if re.search(r'homoscedastic|heteroscedastic|residual[s]?\s*vs|linearity|residual\s*plot', text_lower):
            elements_found["homoscedasticity_plot"] = True
            evidence.append("Homoscedasticity / linearity plot found")
        else:
            evidence.append("Homoscedasticity / linearity plot NOT found")

        # Checkpoint 4 — Method justification
        if re.search(r'step\s*1|linear\s*regression|method|assumption|justify|justif|suitable|data\s*level|interval|ratio', text_lower):
            elements_found["step1_justification"] = True
            evidence.append("Method justification found")
        else:
            evidence.append("Mmethod justification NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_question_cw13_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 13.2: Regression assumption checking and method justification.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

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
                feedback="[TEST MODE] Formatting present. Q-Q plot figure numbered and titled. Outliers table numbered and titled. Homoscedasticity/linearity plot numbered and titled. Method named and justified.",
                vibe="Student demonstrates solid understanding of regression assumption checking and method justification",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "qq_plot_normality": True,
                            "outliers_table": True,
                            "homoscedasticity_plot": True,
                            "method_justification": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)
        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["name the method you choose"]
        )

        prompt = f"""You are grading a statistics assignment about checking linear regression assumptions in JASP using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
Task 2. Check the residuals normality (Plots > Q-Q plot standardized residuals, 09:30). Include the plot, number and title it. (5 points). Check outliers (Statistics > Residuals > Statistics, 07:45). Include the table, number and title it. (5 points).  Visually check both the homoscedasticity and linearity (Plots > Residuals vs. predicted, 10:05). Include plot, number and title it. (5 points).  Name the method you choose based on the data level and justify it (i.e. explain why this method is suitable for our problem solving, based on the assumption checking) (5 points).

Total: 20 points

STUDENT ANSWER:
{student_answer}

**IMPORTANT NOTES:**
- Students submit text descriptions of their work since visual elements (actual diagrams, screenshots, formatted documents) cannot be captured in text
- If student REFERENCES or DESCRIBES the required elements (e.g., "I used APA format to describe findings", "I inserted the frequency distribution diagram"), ASSUME they completed it in their actual document
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

**Component 2: Normality / Q-Q Plot (5 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Introductory phrase for the normality section is present
- 1 point: Introductory phrase references the figure number (e.g., "...using Q-Q Plot (Figure 1)")
- 1 point: Standalone figure number present in APA style (e.g., "Figure 1")
- 1 point: Descriptive figure title present in APA style (e.g., "Figure 1. Q-Q Plot Standardized Residuals.")
- 1 point: Figure (Q-Q plot image) itself is included
- CRITICAL: Do NOT award figure formatting points if no figure is present
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Outliers Table (4 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Introductory phrase for the outliers section is present
- 1 point: Introductory phrase references the table number (e.g., "...see Table 2")
- 1 point: Standalone table number present in APA style (e.g., "Table 2")
- 1 point: Descriptive table title present in APA style (e.g., "Table 2. Residuals Statistics")
- CRITICAL: Do NOT award table formatting points if no table is present
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Homoscedasticity and Linearity Plot (4 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Introductory phrase for the homoscedasticity/linearity section is present
- 1 point: Introductory phrase references the figure number (e.g., "...see Figure 2")
- 1 point: Standalone figure number present in APA style (e.g., "Figure 2")
- 1 point: Descriptive figure title present in APA style (e.g., "Figure 2. Residuals vs. Predicted Value Plot")
- CRITICAL: Do NOT award figure formatting points if no figure is present
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: Method Choice and Justification (5 points):**
- 1 point: Linear regression explicitly named as the chosen method
- 1 point: Justification references scale/interval/ratio level of measurement
- 1 point: Justification references normality of residuals AND absence of outliers
- 1 point: Justification references homoscedasticity
- 1 point: Justification references linearity
- CRITICAL: Justification must be explicitly written; it is not enough to name the method
- CRITICAL: Each sub-point must be explicitly stated; do not infer from generic phrasing

**FEEDBACK RULES**
- Identify which components were completed correctly
- Point out missing or incomplete elements explicitly
- Maintain supportive tone

---

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
}}
"""

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
            "component_2_score": "Normality / Q-Q Plot",
            "component_3_score": "Outliers Table",
            "component_4_score": "Homoscedasticity & Linearity Plot",
            "component_5_score": "Method Choice and Justification",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT",
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
            question_name="CLASSWORK 13_2",
            question_description="Regression Assumption Checks and Method Justification",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )