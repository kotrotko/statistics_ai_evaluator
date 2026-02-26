"""
question3_3_evaluator.py
Distribution Plots with Density Curve, Split by Gender
"""

import re
import textwrap
from config import BaseEvaluator


class Question3_3Evaluator(BaseEvaluator):
    """
    Evaluator for Distribution Plots with Density Curves by Gender.
    """

    def __init__(self):
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1400
        )

    def detect_graphics(self, student_answer: str) -> dict:
        """
        Detect references to distribution plots, density curves, and gender split.
        """
        text = student_answer.lower()

        checks = {
            "distribution": bool(re.search(r"\bdistribution\b|\bhistogram\b|\bplot\b", text)),
            "density": bool(re.search(r"\bdensity\b|\bcurve\b", text)),
            "gender": bool(re.search(r"\bgender\b|\bmale\b|\bfemale\b|\bsplit\b", text)),
            "gpa": bool(re.search(r"\bgpa\b", text)),
            "iq": bool(re.search(r"\biq\b", text)),
            "graphic": bool(re.search(r"\bgraph\b|\bchart\b|\bfigure\b|\bplot\b|\bvisualization\b", text))
        }

        return {
            "checks": checks,
            "all_present": all(checks.values())
        }

    def grade_distribution_plots(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 3.3: Distribution Plots with Density Curves by Gender.
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 5,
                    "component_2_score": 5
                },
                max_points=10,
                feedback="Excellent work creating distribution plots with density curves split by gender for both GPA and IQ.",
                vibe="Strong visualization skills with proper gender-based comparisons",
                additional_data={"detection": "test mode"}
            )

        graphic_check = self.detect_graphics(student_answer)

        prompt = f"""
You are grading a statistics assignment using a **HYBRID grading approach**.

**TASK DESCRIPTION (10 points):**
Students must create distribution plots with density curves using JASP, split by gender:
  - GPA distribution plot with density curve, split by gender (5 points)
  - IQ distribution plot with density curve, split by gender (5 points)

Students submit written descriptions or include the graphics in their submission.

STUDENT ANSWER:
{student_answer}

**AUTOMATIC DETECTION:**
{graphic_check['checks']}

**IMPORTANT ASSUMPTIONS:**
- If students clearly describe or reference distribution plots, assume they were created in JASP
- Do NOT penalize for missing screenshots if descriptions are clear
- Focus on whether they created BOTH plots with proper gender splits
- Density curves should be mentioned or implied
- Students may describe shape, spread, or comparisons between male/female distributions

---

### COMPONENT SCORING (ALL VIBE, 0–5 EACH)

**Component 1:** GPA distribution plot with density curve, split by gender
**Component 2:** IQ distribution plot with density curve, split by gender

Scoring guidance:
- 0: Not mentioned or created
- 2–3: Plot mentioned but unclear if density curve included or gender split unclear
- 4: Clear plot with density curve and gender split, minimal interpretation
- 5: Complete plot with density curve, clear gender split, with interpretation or comparison

Be generous if students clearly reference creating the plots or describe distributions by gender.

---

### FEEDBACK RULES
- Confirm which plots were successfully created
- Point out if density curves or gender splits are missing
- Encourage interpretation of distribution shapes and gender differences
- Maintain supportive tone
- Suggest improvements for clarity if needed

---

Return your grading in **this exact JSON format**:

{{
  "component_1_score": <0-5>,
  "component_2_score": <0-5>,
  "total_points": <0-10>,
  "max_points": 10,
  "percentage": <percentage>,
  "feedback": "<narrative feedback>",
  "vibe": "<one-sentence overall impression>"
}}
"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"graphic_check": graphic_check}
        )

        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score"
            ]
            result = self.validate_component_scores(result, component_keys, 10)

        return result

    def print_grading_results(self, grading):
        print("=" * 60)
        print("GRADING RESULTS – QUESTION 3.3")
        print("Distribution Plots with Density Curves by Gender")
        print("=" * 60)

        plots = ["GPA Distribution Plot (by gender)", "IQ Distribution Plot (by gender)"]
        for i in range(1, 3):
            key = f"component_{i}_score"
            if key in grading:
                print(f"{plots[i-1]}: {grading[key]}/5")

        print(f"\nTOTAL: {grading.get('total_points')}/{grading.get('max_points')}")
        print(f"PERCENTAGE: {grading.get('percentage')}%")

        print("\nFEEDBACK:")
        print(textwrap.fill(grading.get("feedback", ""), 60))

        print("\nTHE VIBE:")
        print(textwrap.fill(grading.get("vibe", ""), 60))