"""
cw4_2.py
Classwork 4
Theoretical Normal Distribution (GPA)
Evaluation method name: def grade_question_cw4_2_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2


class CW4_2Evaluator(BaseEvaluator):
    """
    Evaluator for Question 4_2: Theoretical Normal Distribution.
    Inherits common functionality from BaseEvaluator.
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

    def detect_distribution_elements(self, student_answer: str) -> dict:
        """
        Detect references to theoretical normal distribution elements:
        mean, standard deviation, range, GPA bounds, and unboundedness.
        """
        text = student_answer.lower()

        checks = {
            "mean": bool(re.search(r"\bmean\b|\bμ\b|\bmu\b", text)),
            "std_dev": bool(re.search(
                r"\bstandard deviation\b|\bstd\b|\bs\.d\.\b|\bσ\b|\bsigma\b", text
            )),
            "range_selected": bool(re.search(
                r"\b0\s*[-–]\s*5\b|\brange\b.*\b5\b|\b5\b.*\brange\b", text
            )),
            "gpa_bounded": bool(re.search(
                r"gpa.*\b(0|four|4)\b|\b(0|four|4)\b.*gpa|bounded|valid range|0.*4|4.*0", text
            )),
            "normal_unbounded": bool(re.search(
                r"unbounded|no fixed limit|extends beyond|not bounded|infinite", text
            )),
        }

        return {
            "checks": checks,
            "all_present": all(checks.values())
        }

    def grade_question_cw4_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 4.2: Theoretical Normal Distribution.
        """

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
                feedback=(
                    "Excellent work constructing the theoretical normal distribution "
                    "and justifying the range selection with proper APA formatting."
                ),
                vibe="Strong understanding of theoretical distribution visualization",
                additional_data={"detection": "test mode"}
            )

        dist_check = self.detect_distribution_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["ensure that",
                                 "justify your choice",]
        )

        prompt = f"""
You are grading a statistics assignment using a **HYBRID grading approach**.

**TASK DESCRIPTION (20 points):**
Task 2. Create the theoretical distribution. Using JASP > Distributions tab, create a
theoretical normal distribution for the GPA variable using the same mean (μ) and standard
deviation (σ) calculated previously. Insert the theoretical distribution into your class paper
as Figure 3. Introduce, number, and title the figure according to APA style (5 points). Ensure
that both tails of the distribution curve are fully visible (5 points). Indicate which range you
selected to display both tails (5 points). Justify your choice of range based on the nature of
the GPA variable and the requirements of correctly visualizing a theoretical normal distribution
(5 points).

Total: 20 points

STUDENT ANSWER:
{student_answer}

**IMPORTANT NOTES:**
- Students submit text descriptions of their work since visual elements (actual diagrams,
  screenshots, formatted documents) cannot be captured in text.
- If a student REFERENCES or DESCRIBES the required elements (e.g., "I set the range to 0–5",
  "Figure 3 is titled ...", "both tails are visible"), ASSUME they completed it in their actual
  document.
- DO NOT penalize for "missing" visual elements if the student clearly describes what they did.

**HYBRID GRADING APPROACH:**

**AUTOMATIC FORMATTING DETECTION RESULT:**
Task description present (1 point if True): {formatting_check['elements_found']['task_description']}
No autoformatting (1 point if True): {formatting_check['elements_found']['autoformatting']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC DETECTION:**
{dist_check['checks']}

**Component 1: Formatting (2 points)**

Step 1 – Task description (1 point)
Use task_description_present from automatic detection.

Step 2 – No autoformatting (1 point)
Use autoformatting_present from automatic detection.

**Component 2: Figure 3 APA formatting — STRICT (0–4 points, MAX 4)**
Award 1 point each for:
- Introductory phrase present (text introduces Figure 3 before displaying it)
- Reference to "Figure 3" by number in the introductory phrase
- Correct figure number placement (e.g., "Figure 3." or "Figure 3")
- Correct APA-style figure title (italicized or indicated as such, descriptive title)
**HARD LIMIT**: component_2_score MUST NOT exceed 4.

**Component 3: Theoretical distribution specification — STRICT (0–4 points)**
Award 2 points for correct use of mean (μ) and 2 points for correct use of
standard deviation (σ) in constructing the theoretical normal distribution:
- 4 points: Both μ and σ correctly specified and used
- 3 points: Both mentioned but one is unclear or only partially described
- 2 points: Only one of μ or σ clearly used; other missing or unclear
- 0 points: Neither mentioned or distribution not described

**Component 4: Range selection — STRICT (0–5 points)**
- 5 points: Correct range stated as 0–5 (or equivalent, e.g., "from 0 to 5")
- 3–4 points: A reasonable range is stated but not exactly 0–5, or range is described
  without being explicitly stated as a number pair
- 1–2 points: Range vaguely mentioned without specific values
- 0 points: No range mentioned

**Component 5: Interpretation and justification — STRICT (0–5 points)**
Award points as follows:
- 2 points: States that GPA is bounded between 0 and 4
- 2 points: Explains that the normal distribution is unbounded (has no fixed limits /
  extends beyond valid GPA range)
- 1 point: Explains that the theoretical distribution represents a model, not empirical data
  (i.e., the theoretical and empirical curves differ, or the normal model does not perfectly
  describe the empirical distribution)
- 0 points: No justification provided

**FEEDBACK RULES**
- Identify which APA figure formatting elements were present or missing.
- Note whether μ and σ were correctly referenced.
- Note whether the 0–5 range was stated and whether both tails were addressed.
- Evaluate the quality of the justification: GPA bounds, unboundedness of normal distribution,
  and model vs. empirical distinction.
- Maintain a supportive, constructive tone.

Return JSON only:
{{
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
                "dist_check": dist_check,
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
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Figure 3 APA formatting",
            "component_3_score": "Theoretical distribution specification (μ and σ)",
            "component_4_score": "Range selection",
            "component_5_score": "Interpretation and justification",
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT",
            "component_5_score": "STRICT",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 4,
            "component_3_score": 4,
            "component_4_score": 5,
            "component_5_score": 5,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 4_2",
            question_description="Theoretical Normal Distribution (GPA)",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )