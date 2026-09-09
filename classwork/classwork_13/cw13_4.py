"""
cw13_4.py
Classwork 13: Linear Regression
Explanatory relation, coefficient of determination, and R² interpretation
Evaluation method name: def grade_cw13_4_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2

class CW13_4Evaluator(BaseEvaluator):
    """
    Evaluator for Linear Regression Explanatory Relation and R².

    Task 4. Do you see the explanatory relation between variables? (5 points). Find the Coefficient of determination R² (5 points). It shows how well the model explains the variability of the dependent variable. Interpret it: Which proportion of variance was predictable from level of study hours? (10 points).

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
            "explanatory_relation_exists": False,
            "significance_stated": False,
            "r2_value_present": False,
            "r2_interpretation": False,
        }

        evidence = []

        # Checkpoint 1 — Explanatory relation exists
        if re.search(
            r'explanatory\s*relation\s*exists|relation\s*exists|'
            r'there\s*is\s*(an?\s*)?explanatory\s*relation',
            text_lower
        ):
            elements_found["explanatory_relation_exists"] = True
            evidence.append("Explanatory relation existence statement found")
        else:
            evidence.append("Explanatory relation existence statement NOT found")

        # Checkpoint 2 — Significance stated
        if re.search(r'significant|p\s*<\s*\.?0?5|p\s*<\s*0\.05', text_lower):
            elements_found["significance_stated"] = True
            evidence.append("Significance statement found")
        else:
            evidence.append("Significance statement NOT found")

        # Checkpoint 3 — R² value .506
        if re.search(r'\.506|0\.506|50\.6\s*%', text_lower):
            elements_found["r2_value_present"] = True
            evidence.append("R² value .506 found")
        else:
            evidence.append("R² value .506 NOT found")

        # Checkpoint 4 — R² interpretation (proportion of variance, tied to variables)
        if re.search(
            r'proportion\s*of\s*variance|variance\s*(in|explained)|'
            r'50\.6\s*%|predictable\s*from',
            text_lower
        ):
            elements_found["r2_interpretation"] = True
            evidence.append("R² interpretation found")
        else:
            evidence.append("R² interpretation NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_cw13_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 13.4: Explanatory relation, coefficient of determination, and R² interpretation.
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
                    "component_3_score": 5,
                    "component_4_score": 8,
                },
                max_points=20,
                feedback="[TEST MODE] Formatting present. Explanatory relation confirmed and significant. R² correctly reported and interpreted.",
                vibe="Student demonstrates solid understanding of explanatory relation and R² interpretation",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "explanatory_relation_exists": True,
                            "significance_stated": True,
                            "r2_value_present": True,
                            "r2_interpretation": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)
        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["do you see the explanatory relation"]
        )

        prompt = f"""You are grading a statistics assignment about linear regression explanatory relation and R² using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
Task 4. Do you see the explanatory relation between variables? (5 points). Find the Coefficient of determination R² (5 points). It shows how well the model explains the variability of the dependent variable. Interpret it: Which proportion of variance was predictable from level of study hours? (10 points).

Total: 20 points

STUDENT ANSWER:
{student_answer}

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

**Component 2: Explanatory Relation (5 points):**
Use AUTOMATIC DETECTION above.
- 2 points: confirming an explanatory relation exists
- 3 points: confirming it is significant
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Coefficient of Determination (5 points):**
Use AUTOMATIC DETECTION above.
- 5 points: R² correctly reported as .506
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: R² Interpretation (8 points):**
Use AUTOMATIC DETECTION above.
- 8 points: states that 50.6% is the proportion of variance in final course scores predictable from hours spent on statistics homework, explicitly connecting the percentage to both variables
- 0 points: if the percentage is stated without being connected to the specific variables, or if the variables/percentage are missing
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

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
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-8>,
  "component_4_explanation": "<brief>",
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
            "component_2_score": "Explanatory Relation",
            "component_3_score": "Coefficient of Determination",
            "component_4_score": "R² Interpretation",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT",
            "component_4_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 5,
            "component_3_score": 5,
            "component_4_score": 8,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="CLASSWORK 13_4",
            question_description="Explanatory Relation, Coefficient of Determination, and R² Interpretation",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )