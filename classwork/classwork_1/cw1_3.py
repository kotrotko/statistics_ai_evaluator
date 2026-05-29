"""
cw1_3.py
Classwork 1: File management: Basic Skills
Excel Editing and JASP Comparison
Evaluation method name: def grade_question_cw1_3_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW1_3Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 1_3.

    Task 3. Editing data in Excel.
        Save the same LikeLike file in Excel as LikeLike_modified.xlsx. In position Adults11 change value 11 to value 5 and in position Teens3 change value 15 to value 23. Open the file `LikeLike_modified` in JASP and calculate mean again. Introduce, refer, number and title the second Descriptive Statistics table (10 points).
        Now you can to compare Table 1 with Table 2: what changed? Describe changes in one sentence (10 points).
    """

    def __init__(self):
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

        # Regex-derived rubric checkpoints passed into AUTOMATIC DETECTION
        # inside the grading prompt. Used by the LLM to support consistent
        # hybrid rubric grading, especially for strict required elements.
        elements_found = {
            "value_changes_mentioned": False,
            "apa_table_introduction": False,
            "change_description": False,
        }

        evidence = []

        # Checkpoint 1 — Value changes (11→5 and 15→23)
        patterns = [
            r'11\s*(?:to|→|->)\s*5',
            r'15\s*(?:to|→|->)\s*23',
            r'adults11.*5',
            r'teens3.*23',
            r'changed.*11.*5',
            r'changed.*15.*23'
        ]
        found_changes = []
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                found_changes.append(match.group())
        if found_changes:
            elements_found["value_changes_mentioned"] = True
            evidence.append(f"Value changes found: {', '.join(found_changes)}")
        else:
            evidence.append("Value changes (11→5, 15→23) NOT found")

        # Checkpoint 2 — APA table introduction and reference
        if re.search(r'table\s*2', text_lower) and \
                re.search(r'presents|shows|displays|below|following', text_lower):
            elements_found["apa_table_introduction"] = True
            evidence.append("APA table introduction found")
        else:
            evidence.append("APA table introduction NOT found")

        # Checkpoint 3 — One-sentence change description
        if re.search(r'mean|average|statistic', text_lower) and \
                re.search(r'changed|increased|decreased|differ', text_lower):
            elements_found["change_description"] = True
            evidence.append("Change description found")
        else:
            evidence.append("Change description NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_question_cw1_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 1_3: Excel Editing and JASP Comparison.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_2_score": 9,
                    "component_3_score": 9,
                },
                max_points=20,
                feedback="[TEST MODE] Excel editing described. APA table introduction present. Change described.",
                vibe="Student demonstrates solid understanding of data editing and its effect on descriptive statistics.",
                additional_data={
                    # Mock mirrors what check_required_elements and
                    # check_formatting_elements_type2 return in actual grading
                    "element_check": {
                        # Simulates check_required_elements() output in test mode.
                        # Keys must match elements_found in check_required_elements exactly.
                        "elements_found": {
                            "value_changes_mentioned": True,
                            "apa_table_introduction": True,
                            "change_description": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    },
                    "formatting_check": {
                        "elements_found": {
                            "task_description": True,
                            "autoformatting": True,
                        },
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["now you can"]
        )

        prompt = f"""You are grading a statistics classwork assignment on Excel editing and JASP descriptive statistics.

**TASK DESCRIPTION:**
Editing data in Excel.
Save the same LikeLike file in Excel as LikeLike_modified.xlsx. In position Adults11 change value 11 to value 5 and in position Teens3 change value 15 to value 23. Open the file `LikeLike_modified` in JASP and calculate mean again. Introduce, refer, number and title the second Descriptive Statistics table (10 points). 
Now you can to compare Table 1 with Table 2: what changed? Describe changes in one sentence (10 points). 	

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
- 1 point: Task description correctly formatted
- 1 point: Proper autoformatting and structure

**Component 2: Table 2 (9 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Introductory phrase present before the table
- 1 point: Reference to the table number in the introductory phrase
- 1 point: Standalone table number present
- 1 point: Descriptive table title present
- 5 points: Table itself with numerical data present
- CRITICAL: A label above the table such as "Table 2. Descriptive Statistics" counts as a title
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Comparison (9 points):**
- 9 points: One clear sentence comparing Table 1 and Table 2, describing what changed after data modification
- Partial credit for incomplete or vague descriptions
- CRITICAL: Must reference both tables and describe the direction of change
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
The second Descriptive Statistics table (Table 2) presents the mean values after data modification in Excel.
Table 2. Descriptive Statistics for Outcome Variables (Modified Data)
[JASP table with updated values: Adults Mean 9.333, Teens Mean 18.267]

Comparing Table 1 and Table 2 shows that the mean for Adults decreased from 9.73 to 9.33, while the mean for Teens increased from 18.11 to 18.67 after data correction.

{FEEDBACK_RULES}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief explanation for formatting>",
  "component_2_score": <0-9>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-9>,
  "component_3_explanation": "<brief>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
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
        """Display grading results using OutputFormatter."""
        # Define component labels
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Table 2",
            "component_3_score": "Comparison",
        }

        # Define component types
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

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="CW1_3",
            question_description="Excel Editing and JASP Comparison",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )