"""
cw8_3.py
Classwork 8: Repeated Measures
Hypothesis Testing Setup: Hypotheses, α, df, CV
Evaluation method name: def grade_question_cw8_3_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES

class CW8_3Evaluator(BaseEvaluator):
    """
    Evaluator for Question 8_3: Hypothesis Testing Setup (Hypotheses, α, df, CV).

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
        Check if required elements (hypotheses, alpha, df, CV) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "hypotheses_stated": False,
            "alpha_stated": False,
            "df_calculated": False,
            "cv_stated": False,
        }

        evidence = []

        # Checkpoint 1 — Hypotheses stated (H0 and H1)
        h0_found = bool(re.search(r'h\s*0|h\s*₀|null hypothesis', text_lower))
        h1_found = bool(re.search(r'h\s*1|h\s*₁|alternative hypothesis', text_lower))
        if h0_found and h1_found:
            elements_found["hypotheses_stated"] = True
            evidence.append("Both H0 and H1 found")
        else:
            evidence.append("H0 and/or H1 NOT found")

        # Checkpoint 2 — Alpha stated
        if re.search(r'α\s*=\s*0\.05|alpha\s*=\s*0\.05|significance level.*0\.05', text_lower):
            elements_found["alpha_stated"] = True
            evidence.append("α = 0.05 found")
        else:
            evidence.append("α = 0.05 NOT found")

        # Checkpoint 3 — df calculated
        if re.search(r'df\s*=\s*14|degrees of freedom.*14', text_lower):
            elements_found["df_calculated"] = True
            evidence.append("df = 14 found")
        else:
            evidence.append("df = 14 NOT found")

        # Checkpoint 4 — Critical value stated
        if re.search(r'cv\s*=.*2\.145|critical value.*2\.145|±\s*2\.145|2\.145', text_lower):
            elements_found["cv_stated"] = True
            evidence.append("CV = ±2.145 found")
        else:
            evidence.append("CV = ±2.145 NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_question_cw8_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 8_3: Hypothesis testing setup (hypotheses, α, df, CV).
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
                feedback="[TEST MODE] Hypotheses, α, df, and CV all correctly stated.",
                vibe="Student demonstrates solid understanding of hypothesis testing setup for paired samples",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "hypotheses_stated": True,
                            "alpha_stated": True,
                            "df_calculated": True,
                            "cv_stated": True,
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
Task 3. Hypothesis testing setup. Please state Hypotheses explicitly in needed form (in math form or not, 
one- or two-tailed test) (5 points), select a level of significance α (5 points), calculate df 
(5 points), find the CV (5 points).

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
- 1 point: H₀ stated correctly in required form
- 1 point: H₀ stated in math form (μd = 0)
- 1 point: H₁ stated correctly in required form
- 1 point: H₁ stated in math form (μd ≠ 0)
- 1 point: Two-tailed test specified
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Level of significance (4 points):**
- 2 points: α stated explicitly
- 2 points: correct value α = 0.05
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Degrees of freedom (4 points):**
- 1 point: correct formula (df = n − 1)
- 1 point: calculation shown (15 − 1)
- 2 points: correct result df = 14
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: Critical Value (5 points):**
- 2 points: correct value CV = ±2.145
- 1 point: sign (± both directions) correct
- 2 points: linked to correct df and α
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
Hypotheses:
H₀: There is no difference in the frequency of disruptive behavior between full moon days and normal days in dementia patients (μd = 0).
H₁: There is a difference in the frequency of disruptive behavior between full moon days and normal days in dementia patients (μd ≠ 0).
This is a two-tailed test.
Level of significance: α = 0.05
Degrees of freedom: df = n − 1 = 15 − 1 = 14
CV: ±2.145

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
            "component_3_score": "Level of significance",
            "component_4_score": "Degrees of freedom",
            "component_5_score": "Critical Value",
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
            question_name="QUESTION 8_3",
            question_description="Hypothesis Testing Setup: Hypotheses, α, df, CV",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )