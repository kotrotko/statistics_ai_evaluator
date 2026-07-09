"""
cw8_5.py
Classwork 8: Repeated Measures
Summary: Result description, Research Question Answer
Evaluation method name: def grade_cw8_5_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW8_5Evaluator(BaseEvaluator):
    """
    Evaluator for Question 8_5: APA-style Result Interpretation and
    Main Research Question Answer.

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
        Check if required elements (APA stats, CI, d, means, directionality,
        takeaway, RQ restatement, yes/no answer) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "tdfp_reported": False,
            "ci_reported": False,
            "cohens_d_in_stats_line": False,
            "means_sds_reported": False,
            "directional_comparison_stated": False,
            "cohens_d_repeated": False,
            "effect_size_labeled_large": False,
            "takeaway_sentence_present": False,
            "research_question_restated": False,
            "yes_no_answer_stated": False,
        }

        evidence = []

        # Checkpoint 1 — t, df, p reported (t=6.452, df=14, p<.001)
        if re.search(r'6\.45', text_lower) and re.search(r'14', text_lower) and \
                re.search(r'p\s*<\s*\.?001|p\s*<\s*0?\.001', text_lower):
            elements_found["tdfp_reported"] = True
            evidence.append("t, df, p reported")
        else:
            evidence.append("t, df, p NOT reported")

        # Checkpoint 2 — 95% CI reported
        if re.search(r'1\.62', text_lower) and re.search(r'3\.24', text_lower):
            elements_found["ci_reported"] = True
            evidence.append("95% CI reported")
        else:
            evidence.append("95% CI NOT reported")

        # Checkpoint 3 — Cohen's d in stats line (first appearance, alongside t/df/p/CI)
        stats_line_match = re.search(r't\s*\(?\s*14\s*\)?.{0,150}?d\s*=\s*1\.66', text_lower, re.DOTALL)
        if stats_line_match:
            elements_found["cohens_d_in_stats_line"] = True
            evidence.append("Cohen's d present in statistical results line")
        else:
            evidence.append("Cohen's d NOT present in statistical results line")

        # Checkpoint 4 — Means and SDs reported (Moon and Other)
        if re.search(r'3\.02', text_lower) and re.search(r'0\.58', text_lower):
            elements_found["means_sds_reported"] = True
            evidence.append("Group means and SDs reported")
        else:
            evidence.append("Group means and SDs NOT reported")

        # Checkpoint 5 — Directional comparison
        if re.search(r'higher|greater', text_lower):
            elements_found["directional_comparison_stated"] = True
            evidence.append("Directional comparison stated")
        else:
            evidence.append("Directional comparison NOT stated")

        # Checkpoint 6 — Cohen's d repeated in means-comparison sentence
        d_occurrences = len(re.findall(r'd\s*=\s*1\.66', text_lower))
        if d_occurrences >= 2:
            elements_found["cohens_d_repeated"] = True
            evidence.append("Cohen's d repeated in means-comparison sentence")
        else:
            evidence.append("Cohen's d NOT repeated in means-comparison sentence")

        # Checkpoint 7 — Effect size labeled large
        if re.search(r'large', text_lower):
            elements_found["effect_size_labeled_large"] = True
            evidence.append("Effect size labeled as large")
        else:
            evidence.append("Effect size NOT labeled as large")

        # Checkpoint 8 — Takeaway sentence
        if re.search(r'support(s)?\s+the\s+idea|these\s+findings', text_lower):
            elements_found["takeaway_sentence_present"] = True
            evidence.append("Concluding takeaway sentence present")
        else:
            evidence.append("Concluding takeaway sentence NOT present")

        # Checkpoint 9 — Research question restated
        if re.search(r'research\s+question', text_lower):
            elements_found["research_question_restated"] = True
            evidence.append("Main research question restated")
        else:
            evidence.append("Main research question NOT restated")

        # Checkpoint 10 — Yes/No answer stated
        if re.search(r'\byes\b|\bno\b', text_lower):
            elements_found["yes_no_answer_stated"] = True
            evidence.append("Explicit yes/no answer stated")
        else:
            evidence.append("Explicit yes/no answer NOT stated")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_cw8_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 8_5: APA-style Result Interpretation and Main Research
        Question Answer.
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
                    "component_2_score": 9,
                    "component_3_score": 9,
                },
                max_points=20,
                feedback="[TEST MODE] APA-style result and research question answer both correctly and fully presented.",
                vibe="Student demonstrates solid understanding of APA-style reporting and result interpretation",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "tdfp_reported": True,
                            "ci_reported": True,
                            "cohens_d_in_stats_line": True,
                            "means_sds_reported": True,
                            "directional_comparison_stated": True,
                            "cohens_d_repeated": True,
                            "effect_size_labeled_large": True,
                            "takeaway_sentence_present": True,
                            "research_question_restated": True,
                            "yes_no_answer_stated": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["please describe", "you can answer"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 5. Interpretation. Please describe the result in APA style, following the example at 12:47 of our video (10 points). Now you can answer the main research question (10 points).

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

Component 1. Formatting (2 points total): 1 point for correct task description formatting, 1 point for proper autoformatting and structure in the solution.
Component 2. Result (9 points total): 1 point for t, df, p reported correctly, 1 point for 95% CI reported, 1 point for Cohen's d reported in the statistical results line, 1 point for both group means and SDs reported (Moon and Other), 1 point for directional comparison stated, 1 point for effect size (d) repeated in the means-comparison sentence, 1 point for effect size labeled as large, 2 points for concluding takeaway sentence present, linking the result to its substantive meaning.
Component 3. Answer to the Main Research Question (9 points total): 2 points for restating the main research question, 3 points for explicit yes/no answer clearly stated, 2 points for answer linked to the statistical direction found, 2 points for effect magnitude referenced in the answer.

CRITICAL: Score ONLY against the sub-points explicitly listed above. Any criterion not listed does not exist and must not affect the score. Do NOT assume elements are present if not explicitly written in the student's text.

**CORRECT ANSWER REFERENCE:**
Result: The groups differed significantly, t(14) = 6.452, p < .001, 95% C.I. [1.62, 3.24], d = 1.666. The mean number of disruptive behaviors during moon days (M = 3.022, SD = 1.499) was statistically significantly higher than during other days (M = 0.589, SD = 0.445), and the effect size was large (d = 1.666). These findings support the idea that the lunar cycle is associated with increased disruptive behavior in dementia patients. Answer to the main research question: The main research question asked whether the frequency of the lunar cycle has any impact on the behavior of dementia patients. Based on these results, the answer is yes: patients displayed significantly more disruptive behavior during moon days than during other days, and this effect was large in magnitude.

{FEEDBACK_RULES}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-9>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-9>,
  "component_3_explanation": "<brief>",
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
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results using OutputFormatter."""
        # Define component labels
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Result (APA-style)",
            "component_3_score": "Answer to the Main Research Question",
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
            question_name="QUESTION 8_5",
            question_description="APA-style Result Interpretation, Main Research Question Answer",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )