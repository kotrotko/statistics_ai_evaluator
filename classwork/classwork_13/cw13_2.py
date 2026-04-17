"""
cw13_2.py
Classwork 13: Linear Regression
Assumption checking: residuals normality, outliers, homoscedasticity/linearity, method justification
Evaluation method name: def grade_question_cw13_2_answer
"""

import re
from config import BaseEvaluator


class CW13_2Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 13_2.

    Task:
    Check the residuals normality (Plots > Q-Q plot standardized residuals) (5 points)
    and outliers (Statistics > Residuals > Statistics). Include the table, number and title it. (5 points).
    Visually check both the homoscedasticity and linearity (Plots > Residuals vs. predicted).
    Include plot, number and title it. (5 points).
    Following our Step system, on Step 1: Name the method you choose based on the data level
    and justify it (explain why this method is suitable for our problem solving,
    based on the assumption checking) (5 points).
    Total (strictly) 20 points.

    Evaluates student's ability to check regression assumptions in JASP and justify
    the chosen method based on those checks.

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    def __init__(self):
        """Initialize the evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1200
        )

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
            "task_description": False,
            "qq_plot_normality": False,
            "outliers_table": False,
            "homoscedasticity_plot": False,
            "step1_justification": False,
        }

        evidence = []

        # Checkpoint 1 — Task description (pedagogical markers, plain string matching)
        pedagogical_markers = [
            "visually check both the homoscedasticity and linearity",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found (via pedagogical markers)")
        else:
            elements_found["task_description"] = False
            evidence.append("Task description NOT found")

        # Checkpoint 2 — Q-Q plot / residuals normality check
        if re.search(r'q[\s-]?q\s*plot|quantile|standardized\s*residual|normality\s*(of\s*)?residual|residual\s*normality', text_lower):
            elements_found["qq_plot_normality"] = True
            evidence.append("Q-Q plot / residuals normality found")
        else:
            evidence.append("Q-Q plot / residuals normality NOT found")

        # Checkpoint 3 — Outliers table
        if re.search(r'outlier|cook|leverage|mahalanobis|residual\s*statistic|casewise|std\.\s*residual|standardized\s*residual', text_lower):
            elements_found["outliers_table"] = True
            evidence.append("Outliers / residuals statistics found")
        else:
            evidence.append("Outliers / residuals statistics NOT found")

        # Checkpoint 4 — Homoscedasticity / linearity plot
        if re.search(r'homoscedastic|heteroscedastic|residual[s]?\s*vs|linearity|residual\s*plot', text_lower):
            elements_found["homoscedasticity_plot"] = True
            evidence.append("Homoscedasticity / linearity plot found")
        else:
            evidence.append("Homoscedasticity / linearity plot NOT found")

        # Checkpoint 5 — Step 1 method justification
        if re.search(r'step\s*1|linear\s*regression|method|assumption|justify|justif|suitable|data\s*level|interval|ratio', text_lower):
            elements_found["step1_justification"] = True
            evidence.append("Step 1 method justification found")
        else:
            evidence.append("Step 1 method justification NOT found")

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
                    "component_1_score": 1,
                    "component_2_score": 5,
                    "component_3_score": 4,
                    "component_4_score": 5,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Task description present. Q-Q plot described. Outliers table in APA style. Homoscedasticity plot present. Step 1 method justified.",
                vibe="Student demonstrates solid understanding of regression assumption checking and method justification",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "task_description": True,
                            "qq_plot_normality": True,
                            "outliers_table": True,
                            "homoscedasticity_plot": True,
                            "step1_justification": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics assignment about checking linear regression assumptions in JASP using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
Students must complete 5 components: task description, residuals normality check, outliers table,
homoscedasticity/linearity plot, and method justification.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Focus on conceptual understanding over formatting
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

**RUBRIC:**

**Component 1: Task Description (1 point) — DO NOT SCORE, handled externally.**
Leave component_1_score as 0. It will be overridden.

**Component 2: Residuals Normality Check via Q-Q Plot (5 points):**
Student must check the normality of residuals using the Q-Q plot of standardized residuals
(via Plots > Q-Q plot standardized residuals in JASP).

- 5 points: Q-Q plot included and clearly described; student states whether residuals appear normal
  based on how closely points follow the diagonal reference line
- 4 points: Q-Q plot present and described but interpretation is vague or incomplete
- 3 points: Q-Q plot mentioned or shown but no interpretation provided
- 1 point: Normality of residuals mentioned but Q-Q plot not described or shown
- 0 points: Completely absent

Accept: references to the Q-Q plot, standardized residuals, points on the diagonal,
departure from normality, or normal distribution of residuals.

**Component 3: Outlier Check with Residuals Statistics Table (4 points):**
Student must check for outliers using residuals statistics (Statistics > Residuals > Statistics in JASP)
and include the output table in APA style, numbered and titled.

Breaking down the 4 points:
- 1 point: Outlier check performed and described (e.g., references to standardized residuals,
  Cook's distance, leverage, or casewise diagnostics)
- 1 point: Table is present and referenced in the text (e.g., "as shown in Table 1")
- 1 point: Table has a number in APA style (e.g., "Table 1")
- 1 point: Table has a descriptive title in APA style

Do NOT award table formatting points if no table is present.

**Component 4: Homoscedasticity and Linearity Check via Residuals vs. Predicted Plot (5 points):**
Student must visually check both homoscedasticity and linearity using the Residuals vs. Predicted
scatterplot (Plots > Residuals vs. predicted in JASP) and include the plot, numbered and titled.

Breaking down the 5 points:
- 1 point: Residuals vs. predicted plot included or clearly described
- 1 point: Student comments on homoscedasticity (equal spread of residuals across predicted values)
- 1 point: Student comments on linearity (no systematic curve in the residual pattern)
- 1 point: Plot is numbered in APA style (e.g., "Figure 1")
- 1 point: Plot has a descriptive title/caption in APA style

Do NOT award figure formatting points if no plot or figure is present.

**Component 5: Step 1 — Method Choice and Justification (5 points):**
Student must name the statistical method chosen (linear regression) and justify why it is
appropriate based on: (a) the level of measurement of the variables, and (b) the results of
the assumption checks performed above.

- 5 points: Method named correctly; justification explicitly references data level (interval/ratio)
  AND connects assumption check results (normality of residuals, no serious outliers,
  homoscedasticity, linearity) to the decision to use linear regression
- 4 points: Method named; justification references data level OR assumption checks but not both
- 3 points: Method named; justification present but vague or only partially connected to the checks
- 2 points: Method named but justification is minimal or generic
- 1 point: Method mentioned without any justification
- 0 points: Completely absent

CRITICAL: Justification must be explicitly written. It is not enough to name the method.
CRITICAL: Student must connect assumption checking results to the suitability of linear regression.

---

STUDENT ANSWER:
{student_answer}

Return grading in this exact JSON format:
{{
  "component_1_score": 0,
  "component_1_explanation": "Handled externally",
  "component_2_score": <0-5>,
  "component_2_explanation": "<brief explanation>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief explanation>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief explanation>",
  "component_5_score": <0-5>,
  "component_5_explanation": "<brief explanation>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment>",
  "vibe": "<one-sentence overall impression>"
}}

SCORING INSTRUCTIONS:
total_points = component_1_score + component_2_score + component_3_score + component_4_score + component_5_score
"""

        element_check = self.check_required_elements(student_answer)

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "element_check": element_check
            }
        )

        # Enforcement: Task description (plain string matching, overrides LLM)
        if "error" not in result:
            if not element_check["elements_found"]["task_description"]:
                result["component_1_score"] = 0
                result["component_1_explanation"] = "Task description NOT found (instructional phrasing missing)"
            else:
                result["component_1_score"] = 1
                result["component_1_explanation"] = "Task description found"

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
        """Display grading results."""
        import textwrap
        print("=" * 60)
        print("GRADING RESULTS - CLASSWORK 13.2")
        print("Regression Assumption Checks and Method Justification")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Task Description): {grading.get('component_1_score', 'N/A')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Residuals Normality / Q-Q Plot): {grading.get('component_2_score', 'N/A')}/5")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Outliers / Residuals Statistics Table): {grading.get('component_3_score', 'N/A')}/4")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Homoscedasticity & Linearity Plot): {grading.get('component_4_score', 'N/A')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Step 1: Method Choice & Justification): {grading.get('component_5_score', 'N/A')}/5")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points', 'N/A')}/{grading.get('max_points', 20)}")
        print(f"PERCENTAGE: {grading.get('percentage', 'N/A')}%")

        print("\n" + "=" * 60)
        print("FEEDBACK:")
        print("=" * 60)
        print(textwrap.fill(grading.get('feedback', 'No feedback available'), width=60))

        print("\n" + "=" * 60)
        print("THE VIBE:")
        print("=" * 60)
        print(textwrap.fill(grading.get('vibe', 'N/A'), width=60))

        if 'error' in grading:
            print("\n" + "=" * 60)
            print("ERROR:")
            print("=" * 60)
            print(grading.get('error'))
            if 'raw_response' in grading:
                print("\nRaw Response:")
                print(grading['raw_response'][:500])


if __name__ == "__main__":
    evaluator = CW13_2Evaluator()
    from config import InputHandler

    input_handler = InputHandler()
    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 13.2",
        question_description="Regression Assumption Checks and Method Justification",
        min_length=10
    )
    if student_answer:
        grading = evaluator.grade_question_cw13_2_answer(student_answer)
        evaluator.print_grading_results(grading)