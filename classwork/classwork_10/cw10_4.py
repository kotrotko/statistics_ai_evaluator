"""
cw10_4.py
Classwork 10: One Way ANOVA
Post hoc testing and effect size
Evaluation method name: def grade_cw10_4_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2

class CW10_4Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 10_4.

    Task 4. Do you need a post hoc test? (5 points). If no, explain why. If yes, provide result
    (refer to a table) and explain what does it mean (5 points). Do you need to calculate effect
    size η² ? (5 points). If no, explain why. If yes, provide the result and explain what does it
    mean. (5 points).

    Inherits common functionality from BaseEvaluator.
    """

    def __init__(self):
        """Initialize the evaluator with API handler."""
        super().__init__(
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

        elements_found = {
            "post_hoc_decision": False,
            "post_hoc_justification": False,
            "table_present": False,
            "significant_comparison": False,
            "eta_decision": False,
            "eta_value": False,
        }

        evidence = []

        # Checkpoint 1 — Post hoc decision (yes/need)
        if re.search(r'\byes\b.{0,40}post[\s-]?hoc|need\s*a\s*post[\s-]?hoc', text_lower):
            elements_found["post_hoc_decision"] = True
            evidence.append("Post hoc decision found")
        else:
            evidence.append("Post hoc decision NOT found")

        # Checkpoint 2 — Post hoc justification
        if re.search(r"welch'?s?\s*anova.{0,60}significant|significant.{0,60}welch'?s?\s*anova|at\s*least\s*one\s*pair", text_lower):
            elements_found["post_hoc_justification"] = True
            evidence.append("Post hoc justification found")
        else:
            evidence.append("Post hoc justification NOT found")

        # Checkpoint 3 — Table present
        if re.search(r'table\s*\d', text_lower):
            elements_found["table_present"] = True
            evidence.append("Table reference found")
        else:
            evidence.append("Table reference NOT found")

        # Checkpoint 4 — Significant comparison (302-902)
        if re.search(r'302.{0,10}902|902.{0,10}302', text_lower):
            elements_found["significant_comparison"] = True
            evidence.append("Significant comparison (302 vs 902) found")
        else:
            evidence.append("Significant comparison (302 vs 902) NOT found")

        # Checkpoint 5 — Eta squared decision
        if re.search(r'\byes\b.{0,40}η²|need.{0,20}calculate.{0,20}η²|need.{0,20}effect\s*size', text_lower):
            elements_found["eta_decision"] = True
            evidence.append("η² decision found")
        else:
            evidence.append("η² decision NOT found")

        # Checkpoint 6 — Eta squared value
        if re.search(r'η²\s*=\s*0?\.?114|η²\s*=\s*\.114|11\.4\s*%', text_lower):
            elements_found["eta_value"] = True
            evidence.append("η² value found")
        else:
            evidence.append("η² value NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_cw10_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 10.4: Post Hoc Test Decision and η² Decision with Interpretation.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_2_score": 4,
                    "component_3_score": 3,
                    "component_4_score": 3,
                    "component_5_score": 4,
                },
                max_points=20,
                feedback="[TEST MODE] Post hoc decision justified with table reference. η² decision and value reported with minor interpretation gaps.",
                vibe="Student shows solid understanding of post hoc testing and effect size interpretation",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "post_hoc_decision": True,
                            "post_hoc_justification": True,
                            "table_present": True,
                            "significant_comparison": True,
                            "eta_decision": True,
                            "eta_value": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - partial elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["do you need"]
        )

        prompt = f"""You are grading a statistics assignment about post hoc test decision and effect size (η²) decision using a **STRICT rubric-based approach.

**TASK DESCRIPTION:**
Task 4. Do you need a post hoc test? (5 points). If no, explain why. If yes, provide result (refer to a table) and explain what does it mean (5 points). Do you need to calculate effect size η² ? (5 points). If no, explain why. If yes, provide the result and explain what does it mean. (5 points).

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
Lack of auto-formatting (1 point if True): {formatting_check['elements_found']['autoformatting']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC DETECTION:**
{element_check['elements_found']}

**RUBRIC:**

**Component 1: Formatting (2 points):**
Use AUTOMATIC FORMATTING DETECTION RESULT above.
- 1 point: Task description correctly formatted
- 1 point: Lack of auto-formatting

**Component 2: Post hoc (5 points):**
Use AUTOMATIC DETECTION above.
- 1 point: "Yes" decision stated
- 1 point: Justification (Welch's ANOVA significant, at least one pair differs, but not which pair)
- 1 point: Introductory phrase with reference to the table number
- 1 point: Standalone table number present (e.g., "Table 3")
- 1 point: Descriptive table title present
- CRITICAL: Score ONLY against these sub-points; any criterion not listed here does not exist and must not affect the score

**Component 3: Post hoc result interpretation (4 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Identifies 302–902 as the only significant comparison (p = .017)
- 2 points: Correct directional interpretation (302 rated significantly more attractive than 902)
- 1 point: Notes other comparisons are not significant
- CRITICAL: Score ONLY against these sub-points; any criterion not listed here does not exist and must not affect the score

**Component 4: η² decision and justification (4 points):**
Use AUTOMATIC DETECTION above.
- 2 points: "Yes" decision stated
- 2 points: Justification (significant effect exists)
- CRITICAL: Score ONLY against these sub-points; any criterion not listed here does not exist and must not affect the score

**Component 5: η² result and interpretation (5 points):**
Use AUTOMATIC DETECTION above.
- 1 point: η² = 0.114 reported
- 1 point: Identifies it as a moderate effect size
- 2 points: Percentage interpretation (11.4% of variance explained)
- 1 point: Names the variable relationship (friends → attractiveness ratings)
- CRITICAL: Score ONLY against these sub-points; any criterion not listed here does not exist and must not affect the score

**CORRECT ANSWER REFERENCE:**
Yes, we need a post hoc test, because the Welch's ANOVA result was significant (F > CV), telling us that at least one pair of group means differs, but not which one. Table 3 presents Games-Howell post hoc comparisons for the variable Friends.
Table 3
Games-Howell Post Hoc Comparisons – Friends
Looking at the pairwise comparisons, only the 302–902 comparison is statistically significant (p = .017). This means that profiles with 302 friends were rated as significantly more socially attractive than profiles with 902 friends. None of the other pairwise comparisons reached significance.
Yes, we need to calculate η², because the ANOVA result is statistically significant. η² = 0.114, indicating a moderate effect size: approximately 11.4% of the variance in attractiveness ratings is explained by the number of friends shown.

**FEEDBACK RULES**
- Identify which components were completed correctly
- Point out missing or incomplete elements explicitly
- Maintain supportive tone


Return JSON only:
{{
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-4>,
  "component_4_explanation": "<brief>",
  "component_5_score": <0-5>,
  "component_5_explanation": "<brief>",
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative feedback>",
  "vibe": "<one-sentence overall impression>"
}}"""

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
        # Define component labels
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Post Hoc",
            "component_3_score": "Post Hoc Result Interpretation",
            "component_4_score": "η² Decision and Justification",
            "component_5_score": "η² Result and Interpretation",
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
            "component_4_score": 4,
            "component_5_score": 5,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 10_4",
            question_description="Post Hoc Test Decision and η² Decision with Interpretation",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )