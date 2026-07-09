"""
cw3_3.py
Classwork 3: Central Tendency And Variability
Distribution Plots with Density Curve + Description of Distributions + Area Under Density Curve
def grade_question_cw3_3_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2
from config.constants import IMPORTANT_NOTES, IMPORTANT_GRADING_RULES, FEEDBACK_RULES


class CW3_3Evaluator(BaseEvaluator):
    """
    Evaluator for Question 3_3: Distribution Plots with Density Curves,
    Description of Distributions, and Area Under Density Curve.

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
        Check if required elements (figures, gender split,
        distribution descriptions, area under curve) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "figure_introduced": False,
            "gender_split": False,
            "distribution_description": False,
            "area_under_curve": False,
        }

        evidence = []

        # Checkpoint 1 — Figure introduction and numbering
        if re.search(r'figure\s*[12]', text_lower) and \
                re.search(r'presents|shows|displays|below|following', text_lower):
            elements_found["figure_introduced"] = True
            evidence.append("Figure introduction found")
        else:
            evidence.append("Figure introduction NOT found")

        # Checkpoint 2 — Gender split
        if re.search(r'\bgender\b|\bmale\b|\bfemale\b|\bsplit\b', text_lower):
            elements_found["gender_split"] = True
            evidence.append("Gender split found")
        else:
            evidence.append("Gender split NOT found")

        # Checkpoint 3 — Distribution description (shape, skew, modality)
        desc_patterns = [r'\bsymmetric\b', r'\bskew', r'\bunimodal\b', r'\bbimodal\b',
                         r'\bmodal\b', r'\brange\b', r'\bpeak\b']
        desc_count = sum(1 for p in desc_patterns if re.search(p, text_lower))
        if desc_count >= 2:
            elements_found["distribution_description"] = True
            evidence.append("Distribution description found")
        else:
            evidence.append("Distribution description NOT found")

        # Checkpoint 4 — Area under density curve
        if re.search(r'\barea\b', text_lower) and re.search(r'\b1\b|100\s*%|one\b', text_lower):
            elements_found["area_under_curve"] = True
            evidence.append("Area under curve found")
        else:
            evidence.append("Area under curve NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_question_cw3_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 3_3: Distribution plots with density curves, description of
        distributions, and area under density curve.
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
                    "component_3_score": 8,
                    "component_4_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Good distribution plots with density curves split by gender. Distribution descriptions and area under curve well addressed.",
                vibe="Student demonstrates solid understanding of distribution shapes and density functions",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "figure_introduced": True,
                            "gender_split": True,
                            "distribution_description": True,
                            "area_under_curve": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["do not forget"]
        )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 3. Then add the graphics: distribution plots with density curve, split by gender, for both variables. Do not forget to introduce, refer to the figure, number, and title a figure. (5 points).
Describe your distributions: Is every distribution (roughly) symmetric, skewed (left/right), unimodal or multimodal (10 points).
What is the area under the density curve (5 points)?

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

**Component 2: Graphics (5 points):**
- 1 point: Introductory phrase presenting both figures
- 1 point: Reference to figure numbers in the introductory phrase
- 1 point: Figure numbers present (Figure 1 and Figure 2)
- 1 point: Figure titles present
- 1 point: Distribution split by gender in both figures
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Description of distributions (8 points):**
- 1 point: Male IQ — symmetry/skew assessment
- 1 point: Male IQ — modality assessment
- 1 point: Female IQ — symmetry/skew assessment
- 1 point: Female IQ — modality assessment
- 1 point: Male GPA — symmetry/skew assessment
- 1 point: Male GPA — modality assessment
- 1 point: Female GPA — symmetry/skew assessment
- 1 point: Female GPA — modality assessment
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text
- CRITICAL: "Modality assessment" is satisfied by any explicit statement of unimodal, bimodal, multimodal, or number of peaks (e.g. "slightly bimodal", "one clear peak")

**Component 4: Area under the density curve (5 points):**
- 2 points: Correct value stated (equals 1)
- 2 points: Identified as a property of probability density functions
- 1 point: Interpretation in terms of probability or percentage (e.g. 100% of probability)
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**
Figures 1 and 2 present the distribution of IQ and GPA scores, respectively, for male and female students. Each plot shows patterns such as shape, spread (a general impression of how dispersed the distribution is), central tendency, and skewness. By comparing the male and female distributions for both IQ and GPA, the plots allow for an initial visual comparison of similarities and differences between genders before conducting further statistical analyses.
Figure 1 Distribution of IQ Scores by Gender
Figure 2 Distribution of GPA Scores by Gender
Description of distributions
Figure 1 – Distribution of IQ Scores by Gender
Male IQ: Roughly symmetric, bimodal (two visible peaks around 80 and 110), range approximately 40–140
Female IQ: Slightly right-skewed, unimodal (single peak around 90–95), range approximately 60–140
Figure 2 – Distribution of GPA Scores by Gender
Male GPA: Slightly left-skewed, unimodal (single peak around 2.5), range approximately 0.5–4
Female GPA: Roughly symmetric, unimodal (single peak around 2.5–2.8), range approximately 1–4
Area under the density curve
The area under each density curve always equals 1. This is a fundamental property of probability density functions: regardless of the shape, spread, or variable being plotted, the total area equals 1, representing 100% of the probability.

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
  "component_3_score": <0-8>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief>",
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
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results using OutputFormatter."""
        # Define component labels
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Graphics",
            "component_3_score": "Description of Distributions",
            "component_4_score": "Area Under Density Curve",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
            "component_4_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 5,
            "component_3_score": 8,
            "component_4_score": 5,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 3_3",
            question_description="Distribution Plots + Description of Distributions + Area Under Density Curve",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )