"""
cw12_3.py
Classwork 12: Correlational Analysis
Spearman correlation and Effect Size
Evaluation method name: def grade_cw12_3_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW12_3Evaluator(BaseEvaluator):
    """
    Evaluator for Question 12_3: Spearman Hypotheses, Sample Size via Power, df, and Critical Value.

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    def __init__(self):
        """Initialize evaluator with API handler."""
        super().__init__(
            temperature=0.3,
            max_tokens=1200
        )
        # Initialize output formatter
        self.formatter = OutputFormatter(default_width=60)

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check if required elements (hypotheses, alpha, sample size, df, critical value) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "hypotheses_present": False,
            "alpha_correct": False,
            "sample_size_graph_present": False,
            "df_present": False,
            "critical_value_present": False,
        }

        evidence = []

        # Checkpoint 1 — Hypotheses (rho = 0 / rho != 0)
        if re.search(r'ρ\s*=\s*0', text_lower) and re.search(r'ρ\s*≠\s*0', text_lower):
            elements_found["hypotheses_present"] = True
            evidence.append("Hypotheses in math form (ρ = 0 / ρ ≠ 0) found")
        else:
            evidence.append("Hypotheses in math form (ρ = 0 / ρ ≠ 0) NOT found")

        # Checkpoint 2 — Alpha correct value
        if re.search(r'α\s*=\s*\.?0?\.05', text_lower) or re.search(r'alpha\s*=\s*\.?0?\.05', text_lower):
            elements_found["alpha_correct"] = True
            evidence.append("Correct α = .05 found")
        else:
            evidence.append("Correct α = .05 NOT found")

        # Checkpoint 3 — Required sample size from graph (n ~ 85)
        if re.search(r'\b85\b', text_lower):
            elements_found["sample_size_graph_present"] = True
            evidence.append("Required sample size 85 found")
        else:
            evidence.append("Required sample size 85 NOT found")

        # Checkpoint 4 — df = 115
        if re.search(r'\b115\b', text_lower):
            elements_found["df_present"] = True
            evidence.append("df = 115 found")
        else:
            evidence.append("df = 115 NOT found")

        # Checkpoint 5 — Critical value ±.174
        if re.search(r'\.174', text_lower):
            elements_found["critical_value_present"] = True
            evidence.append("Critical value .174 found")
        else:
            evidence.append("Critical value .174 NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_cw12_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 12_3: Hypotheses, significance level, sample size via power, df, and critical value.
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
                    "component_4_score": 4,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Good application of hypotheses, power analysis, and critical value.",
                vibe="Student demonstrates solid understanding of correlation testing and power analysis",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "hypotheses_present": True,
                            "alpha_correct": True,
                            "sample_size_graph_present": True,
                            "df_present": True,
                            "critical_value_present": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["please state"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 3. Please state hypotheses in needed form (5 points). State the significance level α (5 points). To reach the desired statistical power (1−β ≥ .80), find the required sample size using the graph below. Is your actual sample size enough? (5 points). Calculate df, find the critical value (5 points).

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

**Component 2: Hypotheses (5 points):**
- 2 points: H0 stated (1 point for statement, 1 point for math form ρ = 0)
- 2 points: H1 stated (1 point for statement, 1 point for math form ρ ≠ 0)
- 1 point: Two-tailed specification stated
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Significance level (4 points):**
- 2 points: α is stated
- 2 points: Correct value α = 0.05
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Sample size via graph (4 points):**
- 2 points: Required sample size n ≈ 85 obtained from graph
- 2 points: Actual sample size n = 117 compared to required n, with conclusion that power is adequate
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: df and critical value (5 points):**
- 1 point: df = n − 2 formula stated
- 1 point: Correct value df = 115
- 1 point: Correct critical value CV = ±.174
- 2 points: Explanation that the ± sign reflects the two-tailed critical region
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
Hypotheses are stated for each variable pair in the same bilateral form. H0: there is no linear relationship between the two variables in the population (ρ = 0). H1: a linear relationship exists (ρ ≠ 0). The significance level α = .05. To achieve the desired statistical power (1−β ≥ .80), the required sample size was found using the graph (correlation: two-tailed; effect size ρ = 0.3 (medium); α = .05; power ≥ .80), yielding a minimum required sample size of about n = 85. The actual sample size (n = 117) exceeds this requirement; statistical power is adequate. Degrees of freedom are calculated as df = n − 2 = 117 − 2 = 115. The critical value for Spearman's r at df = 115, α = .05, two-tailed is CV = ±.174.

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
  "component_4_score": <0-4>,
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
            "component_2_score": "Hypotheses",
            "component_3_score": "Significance Level",
            "component_4_score": "Sample Size via Graph",
            "component_5_score": "df and Critical Value",
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
            question_name="QUESTION 12_3",
            question_description="Spearman Hypotheses, Sample Size via Power, df, and Critical Value",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )