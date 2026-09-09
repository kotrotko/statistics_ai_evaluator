"""
hw13_5.py
Homework 13: Linear Regression
Problem statement, research question, line of best fit, hypothesis test
Evaluation method name: def grade_hw13_5_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2


class HW13_5Evaluator(BaseEvaluator):
    """
    Evaluator for Homework 13 Task 5.

    Task: You have summary data for two variables: how extroverted someone
    is (X) and how often someone volunteers (Y). Using these values,
    calculate the line of best fit predicting volunteering from
    extroversion then test for a statistically significant relation using
    the hypothesis testing procedure.

    Formatting (2 points: task description, no autoformatting).
    Problem statement (3 points).
    Research question (5 points: question, H0 stated, H0 symbolic, H1
    stated, H1 symbolic).
    Line of best fit (5 points: formula for b, b calculated, a calculated,
    regression equation).
    Hypothesis test (5 points: critical value, ANOVA table, decision, APA
    inference).

    Inherits common functionality from BaseEvaluator.
    """

    def __init__(self):
        """Initialize the evaluator with API handler."""
        super().__init__()
        self.formatter = OutputFormatter(default_width=60)

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check if required content elements are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "problem_statement": False,
            "research_question": False,
            "h0_stated": False,
            "h0_symbolic": False,
            "h1_stated": False,
            "h1_symbolic": False,
            "b_formula": False,
            "b_calculated": False,
            "a_calculated": False,
            "regression_equation": False,
            "critical_value": False,
            "anova_table": False,
            "decision_stated": False,
            "apa_inference": False,
        }

        evidence = []

        # Checkpoint 1 — Problem statement
        if re.search(r'extrovert.*volunteer|volunteer.*extrovert|linear\s*relationship', text_lower):
            elements_found["problem_statement"] = True
            evidence.append("Problem statement found")
        else:
            evidence.append("Problem statement NOT found")

        # Checkpoint 2 — Research question
        if re.search(r'does\s*extroversion|research\s*question', text_lower):
            elements_found["research_question"] = True
            evidence.append("Research question found")
        else:
            evidence.append("Research question NOT found")

        # Checkpoint 3 — H0 stated
        if re.search(r'h0|h\s*0|null\s*hypothesis', text_lower):
            elements_found["h0_stated"] = True
            evidence.append("H0 stated")
        else:
            evidence.append("H0 NOT stated")

        # Checkpoint 4 — H0 symbolic form
        if re.search(r'β\s*=\s*0|beta\s*=\s*0', text_lower):
            elements_found["h0_symbolic"] = True
            evidence.append("H0 symbolic form found")
        else:
            evidence.append("H0 symbolic form NOT found")

        # Checkpoint 5 — H1 stated
        if re.search(r'h1|h\s*1|alternative\s*hypothesis', text_lower):
            elements_found["h1_stated"] = True
            evidence.append("H1 stated")
        else:
            evidence.append("H1 NOT stated")

        # Checkpoint 6 — H1 symbolic form
        if re.search(r'β\s*≠\s*0|beta\s*≠\s*0|β\s*!=\s*0|beta\s*!=\s*0', text_lower):
            elements_found["h1_symbolic"] = True
            evidence.append("H1 symbolic form found")
        else:
            evidence.append("H1 symbolic form NOT found")

        # Checkpoint 7 — Formula for b
        if re.search(r'b\s*=\s*r|r\s*×\s*\(|r\s*\*\s*\(', text_lower):
            elements_found["b_formula"] = True
            evidence.append("Formula for b found")
        else:
            evidence.append("Formula for b NOT found")

        # Checkpoint 8 — b calculated
        if re.search(r'0\.155|0\.1550', text_lower):
            elements_found["b_calculated"] = True
            evidence.append("b calculation found")
        else:
            evidence.append("b calculation NOT found")

        # Checkpoint 9 — a calculated
        if re.search(r'5\.49', text_lower):
            elements_found["a_calculated"] = True
            evidence.append("a calculation found")
        else:
            evidence.append("a calculation NOT found")

        # Checkpoint 10 — Regression equation
        if re.search(r'ŷ|y-hat|y\s*hat|=\s*5\.49', text_lower):
            elements_found["regression_equation"] = True
            evidence.append("Regression equation found")
        else:
            evidence.append("Regression equation NOT found")

        # Checkpoint 11 — Critical value
        if re.search(r'3\.99', text_lower):
            elements_found["critical_value"] = True
            evidence.append("Critical value found")
        else:
            evidence.append("Critical value NOT found")

        # Checkpoint 12 — ANOVA table
        if re.search(r'source.*ss.*df.*ms.*f|model.*error.*total', text_lower):
            elements_found["anova_table"] = True
            evidence.append("ANOVA table found")
        else:
            evidence.append("ANOVA table NOT found")

        # Checkpoint 13 — Decision stated
        if re.search(r'reject\s*h0|fail\s*to\s*reject', text_lower):
            elements_found["decision_stated"] = True
            evidence.append("Decision stated")
        else:
            evidence.append("Decision NOT stated")

        # Checkpoint 14 — APA statistical inference
        if re.search(r'f\s*\(\s*1\s*,\s*65\s*\)|p\s*<\s*\.?0?5', text_lower):
            elements_found["apa_inference"] = True
            evidence.append("APA statistical inference found")
        else:
            evidence.append("APA statistical inference NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_hw13_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Homework 13.5: Extroversion predicting volunteering, line of
        best fit and hypothesis test.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_1_task_score": 1,
                    "component_1_autoformat_score": 1,
                    "component_2_score": 3,
                    "component_3_score": 5,
                    "component_4_score": 5,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Complete and accurate answer.",
                vibe="Student demonstrates full understanding of the regression and hypothesis testing procedure.",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "problem_statement": True,
                            "research_question": True,
                            "h0_stated": True,
                            "h0_symbolic": True,
                            "h1_stated": True,
                            "h1_symbolic": True,
                            "b_formula": True,
                            "b_calculated": True,
                            "a_calculated": True,
                            "regression_equation": True,
                            "critical_value": True,
                            "anova_table": True,
                            "decision_stated": True,
                            "apa_inference": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)
        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=[]
        )

        prompt = f"""You are grading a statistics assignment about predicting volunteering from extroversion using linear regression and hypothesis testing, using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
You have summary data for two variables: how extroverted someone is (X) and how often someone volunteers (Y). Using these values, calculate the line of best fit predicting volunteering from extroversion then test for a statistically significant relation using the hypothesis testing procedure: X̄ = 12.58, sX = 4.65, Ȳ = 7.44, sY = 2.12, r = 0.34, N = 67, SSM = 19.79, SSE = 215.77.

Total: 20 points

STUDENT ANSWER:
{student_answer}

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Reasoning is required; calculations are mandatory
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. Award partial credit where reasoning is mostly correct but incomplete, within the sub-point structure below
6. It is expected to see both student's logic and calculations, not only the final answer
7. Explanations must be SPECIFIC and ACTIONABLE - avoid vague phrases like "lacks depth", "could be better", "needs improvement". Instead, point to what is actually missing or what was done well.
8. Allow reasonable rounding freedom when checking numeric answers; do not penalize minor rounding differences.

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

**Component 2: Problem Statement (3 points):**
Use AUTOMATIC DETECTION above (problem_statement).
- 3 points: Statement of the linear relationship question between extroversion and volunteering, linked to predictive purpose
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Research Question (5 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Research question stated (use research_question)
- 1 point: H0 stated (use h0_stated)
- 1 point: H0 in symbolic form β = 0 (use h0_symbolic)
- 1 point: H1 stated (use h1_stated)
- 1 point: H1 in symbolic form β ≠ 0 (use h1_symbolic)
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Line of Best Fit (5 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Formula for b provided (use b_formula)
- 1 point: b correctly calculated ≈ 0.155 (use b_calculated)
- 1 point: a correctly calculated ≈ 5.490 (use a_calculated)
- 2 points: Regression equation Ŷ = 5.490 + 0.155X written (use regression_equation)
- CRITICAL: Verify the numeric values are mathematically correct before awarding calculation points
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: Hypothesis Test (5 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Critical value stated at α = 0.05, df(1, 65) ≈ 3.99 (use critical_value)
- 2 points: ANOVA table completed (use anova_table)
- 1 point: Decision to reject/fail to reject H0 stated with comparison to critical value (use decision_stated)
- 1 point: APA-style statistical inference reported, F(1, 65) = 5.96, p < .05 (use apa_inference)
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
  "component_2_score": <0-3>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-5>,
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
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Problem Statement",
            "component_3_score": "Research Question",
            "component_4_score": "Line of Best Fit",
            "component_5_score": "Hypothesis Test",
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT",
            "component_5_score": "STRICT",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 3,
            "component_3_score": 5,
            "component_4_score": 5,
            "component_5_score": 5,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="HOMEWORK 13_5",
            question_description="Extroversion Predicting Volunteering: Regression and Hypothesis Test",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )