"""
cw9_4.py
Classwork 9: Independent groups t-test
Hypotheses + Significance Level + Degrees of Freedom + Critical Value
Evaluation method name: def grade_cw9_4_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW9_4Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 9_4: Hypothesis Testing Setup.

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    def __init__(self):
        """Initialize evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1200
        )
        # Initialize output formatter
        self.formatter = OutputFormatter(default_width=60)

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check if required elements (hypotheses, alpha, df, critical value) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "hypotheses_stated": False,
            "alpha_stated": False,
            "df_correct": False,
            "cv_correct": False,
        }

        evidence = []

        # Checkpoint 1 — Hypotheses in math form (one-tailed, right)
        h0_patterns = [r'h0', r'h₀', r'μ.*=.*μ', r'mu.*=.*mu']
        h1_patterns = [r'h1', r'h₁', r'μ.*>.*μ', r'mu.*>.*mu']
        h0_found = any(re.search(p, text_lower) for p in h0_patterns)
        h1_found = any(re.search(p, text_lower) for p in h1_patterns)
        if h0_found and h1_found:
            elements_found["hypotheses_stated"] = True
            evidence.append("H0 and H1 found")
        else:
            evidence.append("H0 and/or H1 NOT found")

        # Checkpoint 2 — Significance level α = .05
        alpha_patterns = [r'α\s*=\s*\.05', r'alpha\s*=\s*\.05', r'α\s*=\s*0\.05']
        if any(re.search(p, text_lower) for p in alpha_patterns):
            elements_found["alpha_stated"] = True
            evidence.append("Significance level α = .05 found")
        else:
            evidence.append("Significance level α = .05 NOT found")

        # Checkpoint 3 — df = 42
        df_patterns = [r'\bdf\s*=\s*42\b', r'n_1\s*\+\s*n_2\s*-\s*2', r'23\s*\+\s*21\s*-\s*2']
        if any(re.search(p, text_lower) for p in df_patterns):
            elements_found["df_correct"] = True
            evidence.append("df = 42 found")
        else:
            evidence.append("df = 42 NOT found")

        # Checkpoint 4 — CV = +1.682
        cv_patterns = [r'\+\s*1\.686', r'1\.686', r'cv\s*=\s*1\.686']
        if any(re.search(p, text_lower) for p in cv_patterns):
            elements_found["cv_correct"] = True
            evidence.append("CV = +1.686 found")
        else:
            evidence.append("CV = +1.686 NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_cw9_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 9.4: Hypothesis Testing Setup.
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
                    "component_3_score": 3,
                    "component_4_score": 5,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Hypotheses stated correctly in math form. Significance level, df, and CV properly calculated.",
                vibe="Student demonstrates solid understanding of hypothesis testing setup for independent groups t-test",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "hypotheses_stated": True,
                            "alpha_stated": True,
                            "df_correct": True,
                            "cv_correct": True,
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
Task 4. Hypothesis testing setup. Please state hypotheses explicitly in needed form (in math form or not, one- or two-tailed test) (5 points). Select level of significance α (5 points), calculate df (5 points), find the CV (5 points).

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
- 1 point: Absence of autoformatting

**Component 2: Hypotheses (5 points):**
- 1 point: H₀ stated
- 1 point: H₀ in math form
- 1 point: H₁ stated
- 1 point: H₁ in math form
- 1 point: one-tailed (right) specification
- CRITICAL: if multiple hypothesis forms (one-tailed and two-tailed) are presented without a single committed choice, score 0 for this component
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Significance level (3 points):**
- 1 point: α stated
- 2 points: correct value α = .05
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Degrees of freedom (5 points):**
- 2 points: df = n₁ + n₂ − 2 formula stated
- 3 points: correct value df = 42
- CRITICAL: if multiple df values are presented without a single committed choice, score 0 for this component
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: Critical value (5 points):**
- 2 points: correct value CV = +1.682
- 1 point: positive sign reflecting one-tailed (right) critical region
- 1 point: critical value clearly distinguished from the obtained test statistic by any notation
- 1 point: linked to correct df = 42 and α = .05
- CRITICAL: if multiple CV values are presented without a single committed choice, score 0 for this component
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
Hypotheses are stated in math form for a one-tailed (right) test: H₀: μtreatment = μcontrol (the mean reading score of the treatment group equals that of the control group). H₁: μtreatment > μcontrol (the mean reading score of the treatment group is greater than that of the control group). Significance level: α = .05. Degrees of freedom: df = n₁ + n₂ − 2 = 23 + 21 − 2 = 42. Critical value: For Student's t-test at df = 42, α = .05, one-tailed: CV = +1.682.

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
  "component_3_score": <0-3>,
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
            "component_2_score": "Hypotheses",
            "component_3_score": "Significance level",
            "component_4_score": "Degrees of freedom",
            "component_5_score": "Critical value",
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
            "component_3_score": 3,
            "component_4_score": 5,
            "component_5_score": 5,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="CLASSWORK 9_4",
            question_description="Hypotheses + Significance Level + Degrees of Freedom + Critical Value",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )