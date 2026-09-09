"""
cw14_1.py
Classwork 14: Chi-Square
Problem statement, Research Question
Evaluation method name: def grade_cw14_1_answer
"""

"""
cw14_1.py
Classwork 14: Chi-Square Test of Independence
Problem statement, Research Question
Evaluation method name: def grade_cw14_1_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.constants import (
    IMPORTANT_NOTES,
    IMPORTANT_GRADING_RULES,
    FEEDBACK_RULES,
)
from config.formatting_checks import check_formatting_elements_type2

class CW14_1Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 14_1.

    Task: State the problem with your own words (10 points) and
    formulate Research question (10 points).
    """

    def __init__(self):
        super().__init__()
        self.formatter = OutputFormatter(default_width=60)

    def check_required_elements(self, student_answer: str) -> dict:
        first_lines = student_answer[:200]

        elements_found = {
            "name": False,
            "title": False,
            "task_description": False,
            "no_autoformatting": True,
        }

        evidence = []

        # STEP 1 - Name (strict; not covered by the shared type2 utility)
        name_patterns = [
            r'name\s*:\s*\w+',
            r'student\s*:\s*\w+',
            r'by\s*:\s*\w+',
            r'^\s*[A-Z][a-z]+\s+[A-Z][a-z]+',
        ]
        for pattern in name_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["name"] = True
                evidence.append("Name found")
                break
        if not elements_found["name"]:
            evidence.append("Name NOT found")

        # STEP 2 - Title (strict; not covered by the shared type2 utility)
        title_patterns = [
            r'^\s*classwork\s*14',
            r'^\s*cw\s*14\b',
            r'^\s*class\s*work\s*(week\s*)?14',
            r'^\s*in.?class\s*14'
        ]
        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["title"] = True
                evidence.append("Title found")
                break
        if not elements_found["title"]:
            evidence.append("Title NOT found")

        # STEP 3 & 4 - Task Description and Autoformatting via shared utility
        pedagogical_markers = [
            "state the problem with your own words",
            "formulate research question",
        ]

        shared_check = check_formatting_elements_type2(
            student_answer, pedagogical_markers
        )
        elements_found["task_description"] = shared_check[
            "elements_found"
        ]["task_description"]
        elements_found["no_autoformatting"] = shared_check[
            "elements_found"
        ]["autoformatting"]
        evidence.extend(shared_check["evidence"])

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def grade_cw14_1_answer(
        self, student_answer: str, test_mode: bool = False
    ):
        """
        Grade Question14_1: Problem Statement and Research Question.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text

        """
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 4,
                    "component_1_name_score": 1,
                    "component_1_title_score": 1,
                    "component_1_task_score": 1,
                    "component_1_autoformat_score": 1,
                    "component_2_score": 8,
                    "component_3_score": 8,
                },
                max_points=20,
                feedback="[TEST MODE] Excellent understanding",
                vibe=(
                    "Student shows solid understanding of the problem "
                    "and research question"
                ),
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "name": False,
                            "title": False,
                            "task_description": False,
                            "no_autoformatting": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        prompt = f"""You are grading a statistics classwork assignment.

**TASK DESCRIPTION:**

State the problem with your own words (10 points). Formulate Research question (10 points).

{IMPORTANT_NOTES}

{IMPORTANT_GRADING_RULES}

**AUTOMATIC DETECTION:**
{element_check['elements_found']}

---

**RUBRIC**

**Component 1: Formatting (4 points total)**
Use AUTOMATIC DETECTION above. Do not independently judge these
four elements from your own reading of the text.
- Student name present: 1 point
- Paper title present (e.g., "Classwork 14"): 1 point
- Task description present: 1 point
- No autoformatting: 1 point

**Component 2: Problem Statement (8 points)**
Scored only if formulated in terms of a research gap.
- 8 points: Describes what is unknown or a research gap (not a conclusion)
- 4 points: Present but weakly formulated
- 0 points: Missing or is a conclusion/finding

**Component 3: Research Question (8 points)**
Unbroken block, no sub-points. Loose synonyms or rewording of
variable names are acceptable (e.g., referring to physical activity
as "performance") and must not be penalized.

- 8 points: Research question is present, phrased as a testable
  question, and addresses the variables from the problem statement
- 0 points: Research question is missing, not phrased as a
  question, or does not relate to the variables in the problem
  statement at all

{FEEDBACK_RULES}

---

EXAMPLE OF A COMPLETE ANSWER

Problem Statement:
Although student health behaviors have been widely studied, prior
findings are inconsistent, leaving unclear whether physical
activity level and fruit consumption are significantly associated
among college students.

Research Question:
Is there a statistically significant association between physical
activity level and fruit consumption level among college students,
or are these two variables independent?

---
ORIGINALITY CHECK:

IMPORTANT:
Students are required to copy the following task description into
their answer.
This exact text is NEVER an originality concern and must be fully
excluded before evaluation:

--- TASK DESCRIPTION START ---
State the problem with your own words (10 points) and formulate
Research question (10 points).
--- TASK DESCRIPTION END ---

STEP 1: Remove any text matching or paraphrasing the block above.
STEP 2: Evaluate ONLY what remains — the student's own problem
statement and research question.
STEP 3: Set originality_concern = true ONLY if the remaining text
is AI-generated, generic, and contains no personal reasoning
connected to the task.

Otherwise set originality_concern = false.

DO NOT modify or override component scores based on originality_concern.

STUDENT ANSWER:
{student_answer}

Return grading in this exact JSON format:
{{
  "originality_concern": <true/false>,
  "formatting_deductions": <0-4>,
  "formatting_name_deduction": <0-1>,
  "formatting_title_deduction": <0-1>,
  "formatting_task_deduction": <0-1>,
  "formatting_autoformat_deduction": <0-1>,
  "formatting_explanation": "<brief explanation for deductions>",
  "component_1_score": <0-4>,
  "component_1_explanation": "<brief explanation for Task Setup>",
  "component_2_score": <0-8>,
  "component_2_explanation": "<brief explanation for problem statement>",
  "component_3_score": <0-8>,
  "component_3_explanation": "<brief explanation for research question>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression>"
}}

"""
        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "formatting_check": element_check
            }
        )

        # Code-level enforcement: Component 1 is fully determined by the
        # deterministic/isolated checks above. Prompt-only grounding has
        # not reliably stopped the LLM from re-judging these elements
        # itself, so override component_1_score directly rather than
        # trust the model's own value.
        if "error" not in result:
            found = element_check["elements_found"]
            result["component_1_score"] = (
                    (1 if found["name"] else 0)
                    + (1 if found["title"] else 0)
                    + (1 if found["task_description"] else 0)
                    + (1 if found["no_autoformatting"] else 0)
            )

        # If grading succeeded, validate component scores
        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results using OutputFormatter.

        Args:
            grading: Grading result dictionary
        """

        component_labels = {
            "component_1_score": "Task Setup (Name/Title/Task/Formatting)",
            "component_2_score": "Problem Statement",
            "component_3_score": "Research Question",
        }

        component_types = {
            "component_1_score": "HYBRID",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 4,
            "component_2_score": 8,
            "component_3_score": 8,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="CW14_1",
            question_description=(
                "Chi-Square - Problem Statement and Research Question"
            ),
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )