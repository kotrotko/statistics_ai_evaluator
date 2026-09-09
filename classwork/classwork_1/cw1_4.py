"""
cw1_4.py
Classwork 1: File management: How to create, edit, and save files
Editing data in JASP: Table 3 Insertion/Description, Table 4 Insertion/Description
Evaluation method name: def grade_cw1_4_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW1_4Evaluator(BaseEvaluator):
    """
    Evaluator for Question 1_4: Editing data in JASP.
    Table 3 Insertion/Description (renamed columns, nominal type),
    Table 4 Insertion/Description (values changed to zero).

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    def __init__(self):
        """Initialize evaluator with API handler."""
        super().__init__()
        # Initialize output formatter
        self.formatter = OutputFormatter(default_width=60)

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check if required elements (Table 3, Table 4, and their described changes) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "table3_introduced": False,
            "table3_values_stated": False,
            "table3_no_change_stated": False,
            "table4_introduced": False,
            "table4_teens_value_stated": False,
            "table4_teens_decrease_stated": False,
        }

        evidence = []

        # Checkpoint 1 — Table 3 introduced
        if re.search(r'table\s*3', text_lower) and \
                re.search(r'presents|shows|displays|below|following', text_lower):
            elements_found["table3_introduced"] = True
            evidence.append("Table 3 introduction found")
        else:
            evidence.append("Table 3 introduction NOT found")

        # Checkpoint 2 — Table 3 mean values (Women 9.73, Men 18.13)
        if re.search(r'9\.73', text_lower) and re.search(r'18\.13', text_lower):
            elements_found["table3_values_stated"] = True
            evidence.append("Table 3 mean values (9.73, 18.13) found")
        else:
            evidence.append("Table 3 mean values NOT found")

        # Checkpoint 3 — renaming/nominal change did not affect the statistics
        if re.search(r'renam', text_lower) and re.search(r'nominal', text_lower) and \
                re.search(r'not affect|no change|unchanged|same|identical', text_lower):
            elements_found["table3_no_change_stated"] = True
            evidence.append("No-change statement for renaming/nominal type found")
        else:
            evidence.append("No-change statement for renaming/nominal type NOT found")

        # Checkpoint 4 — Table 4 introduced
        if re.search(r'table\s*4', text_lower) and \
                re.search(r'presents|shows|displays|below|following', text_lower):
            elements_found["table4_introduced"] = True
            evidence.append("Table 4 introduction found")
        else:
            evidence.append("Table 4 introduction NOT found")

        # Checkpoint 5 — Table 4 Teens mean value (15.93)
        if re.search(r'15\.93', text_lower):
            elements_found["table4_teens_value_stated"] = True
            evidence.append("Table 4 Teens mean value (15.93) found")
        else:
            evidence.append("Table 4 Teens mean value NOT found")

        # Checkpoint 6 — Teens mean decrease stated
        if re.search(r'teens', text_lower) and re.search(r'decreas', text_lower):
            elements_found["table4_teens_decrease_stated"] = True
            evidence.append("Teens mean decrease statement found")
        else:
            evidence.append("Teens mean decrease statement NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_cw1_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 1_4: Editing data in JASP.
        Table 3 Insertion/Description, Table 4 Insertion/Description.
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
                    "component_2_score": 5,
                    "component_3_score": 4,
                    "component_4_score": 5,
                    "component_5_score": 4,
                },
                max_points=20,
                feedback="[TEST MODE] Table 3 and Table 4 correctly inserted and described.",
                vibe="Student demonstrates solid understanding of how renaming, type changes, and value edits affect descriptive statistics",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "table3_introduced": True,
                            "table3_values_stated": True,
                            "table3_no_change_stated": True,
                            "table4_introduced": True,
                            "table4_teens_value_stated": True,
                            "table4_teens_decrease_stated": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["please open"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 4. Editing data in JASP. Open the original LikeLike.xlsx file in JASP. Change the column labels from Teens to Men and from Adults to Women. Change type of data from ordinal to nominal. Introduce, number, title and insert the third Descriptive Statistics table in JASP format into your class work file (5 points). Describe changes in one sentence (5 points). Open the original LikeLike.xlsx file in JASP. Following the intuitive interface design, change positions Teens8 and Teens10 to value 0. Introduce, number, title and insert the fourth Descriptive Statistics table in JASP format into your class work file (5 points) and describe changes in one sentence (5 points).

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
- 1 point: correct task description formatting
- 1 point: proper autoformatting and structure in the solution

**Component 2: Table 3 Insertion (5 points):**
- 1 point: introductory phrase itself
- 1 point: reference to the table number in the introductory phrase
- 1 point: table number
- 1 point: table title
- 1 point: the table itself
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Table 3 Description (4 points):**
- 2 points: correctly stating that renaming the columns did not affect the descriptive statistics
- 2 points: correctly stating that changing the data type to nominal did not affect the descriptive statistics
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Table 4 Insertion (5 points):**
- 1 point: introductory phrase itself
- 1 point: reference to the table number in the introductory phrase
- 1 point: table number
- 1 point: table title
- 1 point: the table itself
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: Table 4 Description (4 points):**
- 2 points: correctly stating that the results for Adults are unchanged
- 2 points: correctly stating that the mean for Teens decreased
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
Table 3 presents the mean values after renaming the columns (Adults to Women, Teens to Men) and changing the data type from ordinal to nominal. Renaming the columns and changing the data type from ordinal to nominal did not affect the descriptive statistics; all values for Women and Men are identical to those originally reported for Adults and Teens, respectively. Table 4 presents the mean values after changing positions Teens8 and Teens10 to zero. For Adults, the results are unchanged. For Teens, the mean decreased.

{FEEDBACK_RULES}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief>",
  "component_5_score": <0-4>,
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
            "component_2_score": "Table 3 Insertion",
            "component_3_score": "Table 3 Description",
            "component_4_score": "Table 4 Insertion",
            "component_5_score": "Table 4 Description",
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
            "component_2_score": 5,
            "component_3_score": 4,
            "component_4_score": 5,
            "component_5_score": 4,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 1_4",
            question_description="Editing data in JASP: Table 3 Insertion/Description, Table 4 Insertion/Description",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )