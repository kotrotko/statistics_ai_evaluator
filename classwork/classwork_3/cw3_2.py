"""
cw3_2.py
Classwork 3
Range, Variance, Standard Deviation (GPA & IQ)
Evaluation method name: def grade_question_cw3_2_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2

class CW3_2Evaluator(BaseEvaluator):
    """
    Evaluator for Variability Measures (Range, Variance, Standard Deviation).
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

    def grade_question_cw3_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 3.2: Range, Variance, Standard Deviation.
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
                feedback="Excellent work calculating and interpreting range, variance, and standard deviation using JASP.",
                vibe="Strong understanding of variability measures",
                additional_data={"detection": "test mode"}
            )

        stat_check = self.detect_statistics(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["do not forget"]
        )

        prompt = f"""
You are grading a statistics assignment using a **HYBRID grading approach**.

**TASK DESCRIPTION (20 points):**
Task 2. Calculate and add the variability measures: range (5 points), variance (5 points), and standard deviation (5 points), also for (a) GPA and (b) IQ variables, split by gender. Include them to the Table 2. Do not forget to introduce it, refer to the table in introductory phrase, number and title this table in APA style (5 points).

Total: 20 points

STUDENT ANSWER:
{student_answer}

**IMPORTANT NOTES:**
- Students submit text descriptions of their work since visual elements (actual diagrams, screenshots, formatted documents) cannot be captured in text
- If student REFERENCES or DESCRIBES the required elements (e.g., "I used APA format to describe findings", "I inserted the frequency distribution diagram"), ASSUME they completed it in their actual document
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
Task description present (1 point if True): {formatting_check['elements_found']['task_description']}
No autoformatting (1 point if True): 
{formatting_check['elements_found']['autoformatting']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC DETECTION:**
{stat_check['checks']}

**RUBRIC:**

**Component 1: Formatting (2 points)**

Step 1 Task description (1 point)
Use task_description_present.

Step 2 No autoformatting (1 point)
Use autoformatting_present.

**Component 2: Table 1 formatting - STRICT (0-4 points, MAX 4)**
- 1 point: Introductory phrase present
- 1 point: Reference to table number in introductory phrase
- 1 point: Table number present
- 1 point: Table title present
- **HARD LIMIT**: component_2_score MUST NOT exceed 4

**Component 3: Standard Deviation - STRICT (0-4 points)**
- 4 points: Clearly calculated and correctly interpreted
- 3 points: Clear but minimal explanation
- 2 points: Mentioned but unclear or incomplete
- 0 points: Not mentioned

**Component 4: Variance - STRICT (0-5 points)**
- 5 points: Clearly calculated and correctly interpreted
- 4 points: Clear but minimal explanation
- 2-3 points: Mentioned but unclear or incomplete
- 0 points: Not mentioned

**Component 5: Range - STRICT (0-5 points)**
- 5 points: Clearly calculated and correctly interpreted
- 4 points: Clear but minimal explanation
- 2-3 points: Mentioned but unclear or incomplete
- 0 points: Not mentioned

**FEEDBACK RULES**
- Identify which variability measures were calculated correctly
- Point out missing measures explicitly
- Encourage interpretation of what these measures tell us about data spread
- Maintain supportive tone

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
            additional_checks={"stat_check": stat_check, "formatting_check": formatting_check}
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
            "component_2_score": "Table 1 formatting",
            "component_3_score": "Standard Deviation",
            "component_4_score": "Variance",
            "component_5_score": "Range",
        }

        # Define component types
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

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 3_2",
            question_description="Variability Measures (Range, Variance, Standard Deviation)",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,  # No automatic checks for this question
            width=60,
            mode="HYBRID"
        )
