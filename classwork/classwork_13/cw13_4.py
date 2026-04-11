"""
cw13_4.py
Classwork 13: Linear Regression
Regression equation, explanatory relation, and coefficient of determination R²
Evaluation method name: def grade_question_cw13_4_answer
"""

import re
from config import BaseEvaluator


class CW13_4Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 13_4.

    Task: Find and interpret coefficients. With a and b for regression, create a regression equation. (5 points).
    Do you see the explanatory relation between variables? (5 points).
    Find the Coefficient of determination R² (5 points).
    It shows how well the model explains the variability of the dependent variable.
    Interpret it: Which proportion of variance was predictable from level of study hours? (5 points).
    Total (strictly) 20 points.
    """

    def __init__(self):
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1200
        )

    def check_required_elements(self, student_answer: str) -> dict:
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "regression_equation": False,
            "explanatory_relation": False,
            "r2_value": False,
            "r2_interpretation": False,
        }

        evidence = []

        # Task description (pedagogical anchors matching the task wording)
        pedagogical_markers = [
            "create a regression equation",
            "explanatory relation",
            "coefficient of determination",
            "proportion of variance",
            "level of study hours",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Regression equation with a and b
        if re.search(
            r'y\s*=|ŷ\s*=|regression\s*equation|intercept|slope|'
            r'\ba\s*=|\bb\s*=|equation|formula',
            text_lower
        ):
            elements_found["regression_equation"] = True
            evidence.append("Regression equation found")
        else:
            evidence.append("Regression equation NOT found")

        # Explanatory relation between variables
        if re.search(
            r'explanator|predictor|predict|explain|cause|effect|'
            r'relation|dependent|independent|criterion|increase|decrease',
            text_lower
        ):
            elements_found["explanatory_relation"] = True
            evidence.append("Explanatory relation found")
        else:
            evidence.append("Explanatory relation NOT found")

        # R² value reported
        if re.search(
            r'r\s*²|r\s*2|r\^2|r-squared|coefficient\s*of\s*determination|'
            r'r²\s*=|r2\s*=|\.\d{2,}',
            text_lower
        ):
            elements_found["r2_value"] = True
            evidence.append("R² value found")
        else:
            evidence.append("R² value NOT found")

        # R² interpretation (proportion of variance)
        if re.search(
            r'proportion|variance|variability|explained|percent|%|'
            r'study\s*hours|predictable|accounts\s*for|model\s*explain',
            text_lower
        ):
            elements_found["r2_interpretation"] = True
            evidence.append("R² interpretation found")
        else:
            evidence.append("R² interpretation NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def grade_question_cw13_4_answer(self, student_answer: str, test_mode: bool = False):

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 1,
                    "component_2_score": 4,
                    "component_3_score": 5,
                    "component_4_score": 5,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Regression equation present. Explanatory relation addressed. R² found and interpreted.",
                vibe="Clear regression interpretation and R² analysis",
            )

        prompt = f"""You are grading a statistics assignment using a STRICT rubric.

TASK:
Students must complete 5 components interpreting linear regression results and R².

IMPORTANT GRADING RULES:
1. Total score MUST be exactly 20 points
2. Focus on conceptual understanding over formatting
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

RUBRIC:

Component 1: Task Description (1 point)
DO NOT SCORE — handled externally. Leave component_1_score as 0.

Component 2: Regression Equation with Coefficients a and b (4 points)
Student must report the values of a (intercept) and b (slope) from JASP and write
the regression equation in the form: Ŷ = a + b·X (or equivalent notation).
Student must also briefly interpret what a and b mean in context.

- 4 points: Equation written correctly with both a and b values; both coefficients interpreted in context
- 3 points: Equation written correctly but interpretation is vague or missing for one coefficient
- 2 points: Equation present but values missing, or both values reported without equation form
- 1 point: Only one coefficient mentioned or equation attempted without values
- 0 points: Completely absent

Accept any standard notation: Y = a + bX, Ŷ = a + b·X, Y' = b0 + b1·X.
Interpretation must connect a and b to the specific variables in the dataset.

Component 3: Explanatory Relation Between Variables (5 points)
Student must answer whether an explanatory (predictive) relation exists between the predictor
and criterion variables, based on the regression results.

- 5 points: Clear yes/no answer with explicit reasoning — references the direction of b (positive/negative),
  the significance of the result (from Step 4), and what the relation means in practical terms
- 4 points: Correct answer with reasoning but one element (direction, significance, or practical meaning) missing
- 3 points: Correct answer stated but reasoning is vague or incomplete
- 2 points: Answer present but reasoning is incorrect or confused with correlation
- 1 point: Minimal attempt — states yes or no without any reasoning
- 0 points: Completely absent

CRITICAL: Student must distinguish explanatory/predictive relation from mere correlation.
CRITICAL: Reasoning must be grounded in the regression output, not general knowledge.

Component 4: Find the Coefficient of Determination R² (5 points)
Student must locate and report the R² value from the JASP regression output.

- 5 points: R² value correctly reported with its exact numerical value from JASP
- 4 points: R² value reported but with minor imprecision (e.g., rounded differently)
- 3 points: R² mentioned and approximately correct but value unclear or not explicitly stated
- 2 points: R² mentioned but value not reported or clearly wrong
- 1 point: R² referenced without any value
- 0 points: Completely absent

Accept: R², R-squared, coefficient of determination. Value must be between 0 and 1
(or expressed as a percentage between 0% and 100%).

Component 5: Interpret R² — Proportion of Variance Explained (5 points)
Student must interpret R² by stating what proportion of variance in the dependent variable
is explained by the predictor (study hours), in their own words.

- 5 points: Interpretation explicitly states the percentage (or proportion) of variance in the
  dependent variable that is explained by study hours, connected to the specific R² value reported
- 4 points: Correct interpretation but missing the specific variable name or percentage link
- 3 points: General interpretation of R² present but not connected to study hours or the specific value
- 2 points: Interpretation attempted but conceptually confused (e.g., confuses R² with r)
- 1 point: Minimal attempt — only restates R² without interpretation
- 0 points: Completely absent

CRITICAL: Interpretation must connect the numeric R² to the specific variables in the dataset.
CRITICAL: Student must use language such as "X% of the variance in [criterion] is explained by [predictor]".

---

STUDENT ANSWER:
{student_answer}

Return JSON in this exact format:
{{
  "component_1_score": 0,
  "component_1_explanation": "Handled externally",
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief explanation>",
  "component_3_score": <0-5>,
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
            additional_checks={"element_check": element_check}
        )

        # Enforcement: task description check (plain string matching, overrides LLM)
        if "error" not in result:
            if not element_check["elements_found"]["task_description"]:
                result["component_1_score"] = 0
                result["component_1_explanation"] = "Task description NOT found (instructional phrasing missing)"
            else:
                result["component_1_score"] = 1
                result["component_1_explanation"] = "Task description found"

        if "error" not in result:
            result = self.validate_component_scores(
                result,
                [
                    "component_1_score",
                    "component_2_score",
                    "component_3_score",
                    "component_4_score",
                    "component_5_score",
                ],
                20
            )

        return result

    def print_grading_results(self, grading):
        import textwrap

        print("=" * 60)
        print("GRADING RESULTS - CLASSWORK 13.4")
        print("Regression Equation, Explanatory Relation, and R²")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Task Description): {grading.get('component_1_score')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Regression Equation with a and b): {grading.get('component_2_score')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Explanatory Relation Between Variables): {grading.get('component_3_score')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Coefficient of Determination R²): {grading.get('component_4_score')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Interpretation of R²): {grading.get('component_5_score')}/5")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points')}/20")
        print(f"PERCENTAGE: {grading.get('percentage')}%")

        print("\nFEEDBACK:")
        print(textwrap.fill(grading.get('feedback', ''), width=60))


if __name__ == "__main__":
    evaluator = CW13_4Evaluator()

    from config import InputHandler
    input_handler = InputHandler()

    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 13.4",
        question_description="Regression Equation, Explanatory Relation, and R²",
        min_length=10
    )

    if student_answer:
        grading = evaluator.grade_question_cw13_4_answer(student_answer)
        evaluator.print_grading_results(grading)