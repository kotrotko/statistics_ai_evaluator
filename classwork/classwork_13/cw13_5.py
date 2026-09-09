"""
cw13_5.py
Classwork 13: Linear Regression
Results description, research question answer
Evaluation method name: def grade_cw13_5_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2

class CW13_5Evaluator(BaseEvaluator):
    """
    Evaluator for Linear Regression APA Results and Research Question Answer.

    Task 5. Describe your results in APA style, using as template the text on video, but include only results you got yourself (21:40). Please keep in mind that your assignment is different from the description presented in the video: it is shortened. (10 points). Answer the main research question (10 points).

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
            "f_statistic_present": False,
            "p_value_present": False,
            "r2_present": False,
            "plain_language_summary": False,
            "predictor_named": False,
            "significant_prediction_stated": False,
        }

        evidence = []

        # Checkpoint 1 — F(1, 18) = 18.46
        if re.search(r'f\s*\(\s*1\s*,\s*18\s*\)\s*=\s*18\.4[5-7]', text_lower):
            elements_found["f_statistic_present"] = True
            evidence.append("F(1, 18) = 18.46 found")
        else:
            evidence.append("F(1, 18) = 18.46 NOT found")

        # Checkpoint 2 — p < .001
        if re.search(r'p\s*<\s*\.?0?01', text_lower) or re.search(r'p\s*<\s*\.001', text_lower):
            elements_found["p_value_present"] = True
            evidence.append("p < .001 found")
        else:
            evidence.append("p < .001 NOT found")

        # Checkpoint 3 — R² = .506
        if re.search(r'\.506|0\.506', text_lower):
            elements_found["r2_present"] = True
            evidence.append("R² = .506 found")
        else:
            evidence.append("R² = .506 NOT found")

        # Checkpoint 4 — plain-language summary linking study hours to final scores
        if re.search(r'studied\s*longer|study(ing)?\s*(more|longer)|higher\s*(final\s*)?scores', text_lower):
            elements_found["plain_language_summary"] = True
            evidence.append("Plain-language summary found")
        else:
            evidence.append("Plain-language summary NOT found")

        # Checkpoint 5 — predictor named (hours spent on statistics homework)
        if re.search(r'hours\s*spent\s*on\s*statistics\s*homework|study\s*hours|hours\s*(spent\s*)?studying', text_lower):
            elements_found["predictor_named"] = True
            evidence.append("Predictor named")
        else:
            evidence.append("Predictor NOT named")

        # Checkpoint 6 — significantly predicted final course scores
        if re.search(r'significantly\s*predict(ed)?', text_lower):
            elements_found["significant_prediction_stated"] = True
            evidence.append("Significant prediction statement found")
        else:
            evidence.append("Significant prediction statement NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_cw13_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 13.5: APA-style results description and research question answer.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_2_score": 8,
                    "component_3_score": 10,
                },
                max_points=20,
                feedback="[TEST MODE] Formatting present. APA results correctly reported. Research question answered clearly.",
                vibe="Well-structured regression summary with proper APA reporting",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "f_statistic_present": True,
                            "p_value_present": True,
                            "r2_present": True,
                            "plain_language_summary": True,
                            "predictor_named": True,
                            "significant_prediction_stated": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)
        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["please keep in mind"]
        )

        prompt = f"""You are grading a statistics assignment about APA-style results reporting and research question interpretation using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
Task 5. Describe your results in APA style, using as template the text on video, but include only results you got yourself (21:40). Please keep in mind that your assignment is different from the description presented in the video: it is shortened. (10 points). Answer the main research question (10 points).

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

**Component 2: APA Results Description (8 points):**
Use AUTOMATIC DETECTION above.
- 2 points: F(1, 18) = 18.46 reported
- 2 points: p < .001 reported
- 2 points: R² = .506 reported
- 2 points: plain-language summary linking study hours to final scores
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Research Question Answer (10 points):**
Use AUTOMATIC DETECTION above.
- 5 points: naming the predictor (hours spent on statistics homework)
- 5 points: stating it significantly predicted final course scores
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
  "component_2_score": <0-8>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-10>,
  "component_3_explanation": "<brief>",
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
            "component_2_score": "APA Results Description",
            "component_3_score": "Research Question Answer",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 8,
            "component_3_score": 10,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="CLASSWORK 13_5",
            question_description="APA Results Description and Research Question Answer",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )