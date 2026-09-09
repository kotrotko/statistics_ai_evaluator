"""
cw1_5.py
Classwork 1: File management: How to create, edit, and save files
Data analysis with JASP descriptive statistics: Table 5 Anxiety level
Evaluation method name: def grade_cw1_5_answer
"""
import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW1_5Evaluator(BaseEvaluator):
    """
    Evaluator for Question 1_5: Data analysis with JASP descriptive statistics.
    Rename the Columns, Clean and Prepare the Data, Table 5 Insertion, Correct Statistics.

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
        Check if required elements (Table 5 insertion, renamed columns, clean data,
        recoded/valid statistics, correct stat set) are present.

        Each key below is named after, and maps directly to, a specific Rubricator
        sub-point (see comments). These checks only supply evidence for the
        AUTOMATIC DETECTION block in the prompt; they do not score Components 2/3
        (Rename, Clean and Prepare) themselves, since those require semantic
        judgment. Components 4 and 5 sub-points are fully covered by these checks.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            # Component 4: Table 5 Insertion sub-points
            "table5_introduced": False,          # "1 point for introductory phrase itself" +
                                                   # "1 point for reference to the table number in the introductory phrase"
            "table5_number_present": False,       # "1 point for table number"
            "table5_title_present": False,        # "1 point for table title"
            # Component 5: Correct Statistics sub-points (one per named element)
            "stat_valid_included": False,         # "1 point for including Valid"
            "stat_missing_included": False,       # "1 point for including Missing"
            "stat_mean_included": False,          # "1 point for including Mean"
            "stat_maximum_included": False,       # "1 point for including Maximum"
            "stat_minimum_included": False,       # "1 point for including Minimum"
            # Supporting evidence only (feeds Components 2/3 HYBRID judgment, does not score them directly)
            "rename_evidence_present": False,     # evidence for Component 2 (Rename)
            "no_extraneous_row": False,           # evidence for Component 3 (Clean: "no unneeded row")
            "numeric_mean_evidence": False,       # evidence for Component 3 (Clean: "valid computed statistics")
        }

        evidence = []

        # Checkpoint 1 — Table 5 introductory phrase + number reference
        if re.search(r'table\s*5', text_lower) and \
                re.search(r'presents|shows|displays|below|following', text_lower):
            elements_found["table5_introduced"] = True
            evidence.append("Table 5 introductory phrase with number reference found")
        else:
            evidence.append("Table 5 introductory phrase NOT found")

        # Checkpoint 2 — Table number present (standalone "Table 5" label)
        if re.search(r'table\s*5\b', text_lower):
            elements_found["table5_number_present"] = True
            evidence.append("Table 5 number found")
        else:
            evidence.append("Table 5 number NOT found")

        # Checkpoint 3 — Table title present (heuristic: "descriptive statistics" near table 5)
        if re.search(r'descriptive statistics', text_lower):
            elements_found["table5_title_present"] = True
            evidence.append("Table title ('Descriptive Statistics...') found")
        else:
            evidence.append("Table title NOT found")

        # Checkpoint 4 — Valid included
        if re.search(r'\bvalid\b', text_lower):
            elements_found["stat_valid_included"] = True
            evidence.append("Valid statistic found")
        else:
            evidence.append("Valid statistic NOT found")

        # Checkpoint 5 — Missing included
        if re.search(r'\bmissing\b', text_lower):
            elements_found["stat_missing_included"] = True
            evidence.append("Missing statistic found")
        else:
            evidence.append("Missing statistic NOT found")

        # Checkpoint 6 — Mean included
        if re.search(r'\bmean\b', text_lower):
            elements_found["stat_mean_included"] = True
            evidence.append("Mean statistic found")
        else:
            evidence.append("Mean statistic NOT found")

        # Checkpoint 7 — Maximum included
        if re.search(r'\bmaximum\b', text_lower):
            elements_found["stat_maximum_included"] = True
            evidence.append("Maximum statistic found")
        else:
            evidence.append("Maximum statistic NOT found")

        # Checkpoint 8 — Minimum included
        if re.search(r'\bminimum\b', text_lower):
            elements_found["stat_minimum_included"] = True
            evidence.append("Minimum statistic found")
        else:
            evidence.append("Minimum statistic NOT found")

        # Checkpoint 9 — Rename evidence (both group labels present as renamed headers)
        if re.search(r'\bmale\b', text_lower) and re.search(r'\bfemale\b', text_lower):
            elements_found["rename_evidence_present"] = True
            evidence.append("Renamed column headers (Male/Female) found")
        else:
            evidence.append("Renamed column headers NOT found")

        # Checkpoint 10 — No extraneous row (e.g., leftover "Valid N (listwise)" row)
        if not re.search(r'valid n \(listwise\)|valid n listwise', text_lower):
            elements_found["no_extraneous_row"] = True
            evidence.append("No extraneous 'Valid N (listwise)' row found")
        else:
            evidence.append("Extraneous 'Valid N (listwise)' row found")

        # Checkpoint 11 — Numeric mean evidence (decimal number near "mean"), suggesting recoding occurred
        if re.search(r'mean[^\n]{0,40}?\d+\.\d+|\d+\.\d+[^\n]{0,40}?mean', text_lower):
            elements_found["numeric_mean_evidence"] = True
            evidence.append("Numeric (decimal) Mean value found")
        else:
            evidence.append("Numeric (decimal) Mean value NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_cw1_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 1_5: Data analysis with JASP descriptive statistics.
        Rename the Columns, Clean and Prepare the Data, Table 5 Insertion, Correct Statistics.
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
                    "component_2_score": 4,
                    "component_3_score": 4,
                    "component_4_score": 5,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Columns renamed, data cleaned and prepared, Table 5 correctly inserted with correct statistics.",
                vibe="Student demonstrates solid understanding of data cleaning, recoding, and descriptive statistics reporting in JASP",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "table5_introduced": True,
                            "table5_number_present": True,
                            "table5_title_present": True,
                            "stat_valid_included": True,
                            "stat_missing_included": True,
                            "stat_mean_included": True,
                            "stat_maximum_included": True,
                            "stat_minimum_included": True,
                            "rename_evidence_present": True,
                            "no_extraneous_row": True,
                            "numeric_mean_evidence": True,
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
Task 5. Data analysis with JASP descriptive statistics. Open the "1.3.6. Anxiety level" dataset in JASP. Rename the columns based on the information contained in the dataset (5 points). Using JASP tools, clean the data: delete the row that is no longer needed and the column that contains no data. Perform any additional data preparation you find necessary before running the analysis (5 points). Using JASP / Descriptive Statistics, please analyze the cleaned dataset. Introduce, number, title and insert the fifth Descriptive Statistics table in JASP format into your class work file (5 points). Make sure that you included only: Valid, Missing, Mean, Maximum, Minimum (5 points).

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

**Component 2: Rename the Columns (4 points):**
- 4 points: the table shows column headers that correctly reflect the dataset's actual variables
- Use "rename_evidence_present" from AUTOMATIC DETECTION as supporting evidence only; the correctness of the renaming itself requires your judgment
- IMPORTANT: This task, unlike earlier ones, does NOT require the student to write a sentence describing that they renamed the columns. Score this component based solely on what the submitted table itself shows (its column headers). Do NOT deduct points, and do NOT treat as "no evidence," just because the student did not narrate the renaming action in prose — the renamed headers appearing in the table ARE the evidence.
- CRITICAL: Do NOT assume elements are present if not visible in the table or explicitly written in the student's text

**Component 3: Clean and Prepare the Data (4 points):**
- 4 points: the table contains no unneeded row and shows valid computed statistics for both included variables
- Use "no_extraneous_row" and "numeric_mean_evidence" from AUTOMATIC DETECTION as supporting evidence only; whether the statistics are genuinely valid for both variables requires your judgment
- IMPORTANT: This task, unlike earlier ones, does NOT require the student to write a sentence describing that they deleted a row/column or prepared the data. Score this component based solely on what the submitted table itself shows (absence of an unneeded row such as "Valid N (listwise)", and the presence of valid, non-degenerate Mean/Minimum/Maximum values for both variables). Do NOT deduct points, and do NOT treat as missing, just because the student did not narrate the cleaning/preparation steps in prose — the table's own contents ARE the evidence.
- CRITICAL: Do NOT assume elements are present if not visible in the table or explicitly written in the student's text

**Component 4: Table 5 Insertion (5 points):**
- 1 point: introductory phrase itself
- 1 point: reference to the table number in the introductory phrase
- 1 point: table number
- 1 point: table title
- 1 point: the table itself
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: Correct Statistics (5 points):**
- 1 point: including Valid
- 1 point: including Missing
- 1 point: including Mean
- 1 point: including Maximum
- 1 point: including Minimum
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
Table 5 presents the descriptive statistics for the "1.3.6. Anxiety level" dataset, with columns renamed to Female and Male based on the dataset's original labels. The table includes only Valid, Missing, Mean, Minimum, and Maximum, with no extraneous rows or columns. Female (N = 30, Missing = 0): Mean = 1.900, Minimum = 0.000, Maximum = 3.000. Male (N = 30, Missing = 0): Mean = 0.733, Minimum = 0.000, Maximum = 2.000. The presence of valid, non-degenerate computed Mean values for both groups confirms that the textual anxiety-level responses were recoded to a numeric scale prior to analysis.

{FEEDBACK_RULES}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief>",
  "component_5_score": <0-5>,
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
            "component_2_score": "Rename the Columns",
            "component_3_score": "Clean and Prepare the Data",
            "component_4_score": "Table 5 Insertion",
            "component_5_score": "Correct Statistics",
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
            "component_2_score": 4,
            "component_3_score": 4,
            "component_4_score": 5,
            "component_5_score": 5,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 1_5",
            question_description="Data analysis with JASP descriptive statistics: Rename, Clean/Prepare, Table 5 Insertion, Correct Statistics",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )