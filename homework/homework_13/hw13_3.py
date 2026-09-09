"""
hw13_3.py
Homework 13: Linear Regression
Fill out ANOVA tables
Evaluation method name: def grade_hw13_3_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2


class HW13_3Evaluator(BaseEvaluator):
    """
    Evaluator for Homework 13 Task 3.

    Task: Fill out the rest of the ANOVA tables below for simple linear
    regressions.

    Formatting (2 points: task description, no autoformatting).
    Table 1 (9 points: table number, table title, calculation details,
    formulas provided, table itself).
    Table 2 (9 points: table number, table title, calculation details,
    formulas provided, table itself).

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
            "table1_number": False,
            "table1_title": False,
            "table1_calculations": False,
            "table1_formulas": False,
            "table1_table": False,
            "table2_number": False,
            "table2_title": False,
            "table2_calculations": False,
            "table2_formulas": False,
            "table2_table": False,
        }

        evidence = []

        # Checkpoint 1 — Table 1 number
        if re.search(r'table\s*1\b|table\s*a\b', text_lower):
            elements_found["table1_number"] = True
            evidence.append("Table 1 number found")
        else:
            evidence.append("Table 1 number NOT found")

        # Checkpoint 2 — Table 1 title
        if re.search(r'table\s*1[\.:]\s*\S|table\s*a[\.:]\s*\S', text_lower):
            elements_found["table1_title"] = True
            evidence.append("Table 1 title found")
        else:
            evidence.append("Table 1 title NOT found")

        # Checkpoint 3 — Table 1 calculation details
        if re.search(r'df\s*model|ms\s*model|ss\s*error|df\s*error|ms\s*error', text_lower):
            elements_found["table1_calculations"] = True
            evidence.append("Table 1 calculation details found")
        else:
            evidence.append("Table 1 calculation details NOT found")

        # Checkpoint 4 — Table 1 formulas
        if re.search(r'ms\s*=|ss\s*=|f\s*=|=\s*.+/.+', text_lower):
            elements_found["table1_formulas"] = True
            evidence.append("Table 1 formulas found")
        else:
            evidence.append("Table 1 formulas NOT found")

        # Checkpoint 5 — Table 1 table structure
        if re.search(r'source.*ss.*df.*ms.*f|model.*error.*total', text_lower):
            elements_found["table1_table"] = True
            evidence.append("Table 1 structure found")
        else:
            evidence.append("Table 1 structure NOT found")

        # Checkpoint 6 — Table 2 number
        if re.search(r'table\s*2\b|table\s*b\b', text_lower):
            elements_found["table2_number"] = True
            evidence.append("Table 2 number found")
        else:
            evidence.append("Table 2 number NOT found")

        # Checkpoint 7 — Table 2 title
        if re.search(r'table\s*2[\.:]\s*\S|table\s*b[\.:]\s*\S', text_lower):
            elements_found["table2_title"] = True
            evidence.append("Table 2 title found")
        else:
            evidence.append("Table 2 title NOT found")

        # Checkpoint 8 — Table 2 calculation details
        matches = list(re.finditer(r'df\s*model|ms\s*model|ss\s*error|df\s*error|ms\s*error', text_lower))
        if len(matches) >= 2:
            elements_found["table2_calculations"] = True
            evidence.append("Table 2 calculation details found")
        else:
            evidence.append("Table 2 calculation details NOT found")

        # Checkpoint 9 — Table 2 formulas
        matches = list(re.finditer(r'ms\s*=|ss\s*=|f\s*=|=\s*.+/.+', text_lower))
        if len(matches) >= 2:
            elements_found["table2_formulas"] = True
            evidence.append("Table 2 formulas found")
        else:
            evidence.append("Table 2 formulas NOT found")

        # Checkpoint 10 — Table 2 table structure
        matches = list(re.finditer(r'source.*ss.*df.*ms.*f|model.*error.*total', text_lower))
        if len(matches) >= 2:
            elements_found["table2_table"] = True
            evidence.append("Table 2 structure found")
        else:
            evidence.append("Table 2 structure NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_hw13_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Homework 13.3: ANOVA table completion for simple linear regressions.
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
                    "component_2_score": 9,
                    "component_3_score": 9,
                },
                max_points=20,
                feedback="[TEST MODE] Both ANOVA tables complete with correct calculations and formulas.",
                vibe="Student demonstrates solid understanding of ANOVA table completion for simple linear regression.",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "table1_number": True,
                            "table1_title": True,
                            "table1_calculations": True,
                            "table1_formulas": True,
                            "table1_table": True,
                            "table2_number": True,
                            "table2_title": True,
                            "table2_calculations": True,
                            "table2_formulas": True,
                            "table2_table": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)
        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["fill out the rest of the anova tables below for simple linear regressions"]
        )

        prompt = f"""You are grading a statistics assignment about completing ANOVA tables for simple linear regression using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
Fill out the rest of the ANOVA tables below for simple linear regressions.

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
Proper autoformatting and structure (1 point if True): {formatting_check['elements_found']['autoformatting']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC DETECTION:**
{element_check['elements_found']}

**RUBRIC:**

**Component 1: Formatting (2 points):**
Use AUTOMATIC FORMATTING DETECTION RESULT above.
- 1 point: Task description correctly formatted
- 1 point: Proper autoformatting and structure

**Component 2: Table 1 (9 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Table number present (use table1_number)
- 1 point: Table title present (use table1_title)
- 3 points: Calculation details shown, correctly and completely (use table1_calculations)
- 2 points: Formulas provided (use table1_formulas)
- 2 points: Table itself filled out correctly (use table1_table)
- CRITICAL: Verify the numeric values are mathematically correct (SS, df, MS, F relationships) before awarding calculation and table points
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Table 2 (9 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Table number present (use table2_number)
- 1 point: Table title present (use table2_title)
- 3 points: Calculation details shown, correctly and completely (use table2_calculations)
- 2 points: Formulas provided (use table2_formulas)
- 2 points: Table itself filled out correctly (use table2_table)
- CRITICAL: Verify the numeric values are mathematically correct (SS, df, MS, F relationships) before awarding calculation and table points
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
  "component_2_score": <0-9>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-9>,
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
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Table 1",
            "component_3_score": "Table 2",
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 9,
            "component_3_score": 9,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="HOMEWORK 13_3",
            question_description="ANOVA Table Completion for Simple Linear Regressions",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )