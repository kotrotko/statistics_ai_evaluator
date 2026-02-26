"""
question3_2_evaluator.py
Range, Variance, Standard Deviation (GPA & IQ)
"""

import re
import textwrap
from config import BaseEvaluator


class Question3_2Evaluator(BaseEvaluator):
    """
    Evaluator for Variability Measures (Range, Variance, Standard Deviation).
    """

    def __init__(self):
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1400
        )

    def detect_statistics(self, student_answer: str) -> dict:
        """
        Detect references to range, variance, standard deviation, GPA, and IQ.
        """
        text = student_answer.lower()

        checks = {
            "range": bool(re.search(r"\brange\b", text)),
            "variance": bool(re.search(r"\bvariance\b", text)),
            "std_dev": bool(re.search(r"\bstandard deviation\b|\bstd\b|\bs\.d\.\b", text)),
            "gpa": bool(re.search(r"\bgpa\b", text)),
            "iq": bool(re.search(r"\biq\b", text))
        }

        return {
            "checks": checks,
            "all_present": all(checks.values())
        }

    def grade_variability(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 3.2: Range, Variance, Standard Deviation.
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 5,
                    "component_2_score": 5,
                    "component_3_score": 5
                },
                max_points=15,
                feedback="Excellent work calculating and interpreting range, variance, and standard deviation using JASP.",
                vibe="Strong understanding of variability measures",
                additional_data={"detection": "test mode"}
            )

        stat_check = self.detect_statistics(student_answer)

        prompt = f"""
You are grading a statistics assignment using a **HYBRID grading approach**.

**TASK DESCRIPTION (15 points):**
Students must calculate variability measures using JASP for GPA and/or IQ:
  - Range (5 points)
  - Variance (5 points)
  - Standard Deviation (5 points)

Students submit written descriptions of JASP output.

STUDENT ANSWER:
{student_answer}

**AUTOMATIC DETECTION:**
{stat_check['checks']}

**IMPORTANT ASSUMPTIONS:**
- If students clearly describe results, assume calculations were performed in JASP
- Do NOT penalize for missing screenshots or tables
- Focus on statistical correctness and task coverage
- Students may report for GPA, IQ, or both variables

---

### COMPONENT SCORING (ALL VIBE, 0–5 EACH)

**Component 1:** Range calculation and interpretation
**Component 2:** Variance calculation and interpretation
**Component 3:** Standard Deviation calculation and interpretation

Scoring guidance:
- 0: Not mentioned
- 2–3: Mentioned but unclear or incomplete
- 4: Clear but minimal explanation
- 5: Clearly calculated and correctly interpreted

Be generous if students show understanding of what each measure represents.

---

### FEEDBACK RULES
- Identify which variability measures were calculated correctly
- Point out missing measures explicitly
- Encourage interpretation of what these measures tell us about data spread
- Maintain supportive tone

---

Return your grading in **this exact JSON format**:

{{
  "component_1_score": <0-5>,
  "component_2_score": <0-5>,
  "component_3_score": <0-5>,
  "total_points": <0-15>,
  "max_points": 15,
  "percentage": <percentage>,
  "feedback": "<narrative feedback>",
  "vibe": "<one-sentence overall impression>"
}}
"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"stat_check": stat_check}
        )

        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score"
            ]
            result = self.validate_component_scores(result, component_keys, 15)

        return result

    def print_grading_results(self, grading):
        print("=" * 60)
        print("GRADING RESULTS – QUESTION 3.2")
        print("Variability Measures (Range, Variance, Standard Deviation)")
        print("=" * 60)

        measures = ["Range", "Variance", "Standard Deviation"]
        for i in range(1, 4):
            key = f"component_{i}_score"
            if key in grading:
                print(f"{measures[i-1]}: {grading[key]}/5")

        print(f"\nTOTAL: {grading.get('total_points')}/{grading.get('max_points')}")
        print(f"PERCENTAGE: {grading.get('percentage')}%")

        print("\nFEEDBACK:")
        print(textwrap.fill(grading.get("feedback", ""), 60))

        print("\nTHE VIBE:")
        print(textwrap.fill(grading.get("vibe", ""), 60))