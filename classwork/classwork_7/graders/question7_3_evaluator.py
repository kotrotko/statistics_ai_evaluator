"""
question7_3_evaluator.py
Hypothesis Testing with Wilcoxon
"""
import re

from config import BaseEvaluator

class Question7_3Evaluator(BaseEvaluator):
    def __init__(self):
        """Initialize the evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1200
        )

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
            "test_value": False,
            "approach_justification": False,
            "descriptive_table": False,
            "mean_median": False
        }

        evidence = []

        # Checkpoint 1 — Test value identification
        if re.search(r'test\s*value|73|x\s*=\s*73|mean\s*women', text_lower):
            elements_found["test_value"] = True
            evidence.append("Test value found")
        else:
            evidence.append("Test value NOT found")

        # Checkpoint 2 — Approach and justification
        if re.search(r'non[\s-]?parametric|wilcoxon', text_lower) and \
                re.search(r'normal|parametric|justif|because|since|reason', text_lower):
            elements_found["approach_justification"] = True
            evidence.append("Approach and justification found")
        else:
            evidence.append("Approach and justification NOT found")

        # Checkpoint 3 — Descriptive statistics table (APA)
        if re.search(r'table\s*\d+|table\s*[1-9]', text_lower) and \
                re.search(r'mean|median|descriptive', text_lower):
            elements_found["descriptive_table"] = True
            evidence.append("Descriptive table found")
        else:
            evidence.append("Descriptive table NOT found")

        # Checkpoint 4 — Mean and median for men
        if re.search(r'mean|median', text_lower) and \
                re.search(r'men|male', text_lower):
            elements_found["mean_median"] = True
            evidence.append("Mean and median for men found")
        else:
            evidence.append("Mean and median for men NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_question7_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 7.3: Wilcoxon Signed Rank Test.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
                return self.create_mock_result(
                    component_scores={
                        "component_1_score": 3,
                        "component_2_score": 4,
                        "component_3_score": 2,
                        "component_4_score": 5,
                    },
                    max_points=20,
                    feedback="[TEST MODE] Test value mentioned but source unclear. Non-parametric identified. Table formatting issues. Mean and median correct.",
                    vibe="Student shows partial understanding; test value source and table APA formatting need improvement",
                    additional_data={
                        "element_check": {
                            "elements_found": {
                                "test_value": True,
                                "approach_justification": True,
                                "descriptive_table": False,
                                "mean_median": True
                        },
                            "all_present": False,
                            "evidence": ["Test mode - partial elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics assignment about the Wilcoxon Signed Rank test using a **STRICT rubric-based approach**.

    **TASK DESCRIPTION:**
    Students must complete 4 components for a Wilcoxon Signed Rank test analysis.

    **IMPORTANT GRADING RULES:**
    1. Total score MUST be exactly 20 points
    2. Focus on conceptual understanding over formatting
    3. Feedback should be SHORT, written as a teacher's comment
    4. Feedback CANNOT be an invitation for further discussion
    
    **RUBRIC:**

    Component 1: Test Value Identification and Source (5 points)
    - 5/5: Correctly identifies test value (73, mean for women) AND explains source
    - 3/5: Identifies test value but source explanation unclear or incomplete
    - 1/5: Test value mentioned but no source explanation
    - 0/5: Test value not identified or wrong

    Component 2: Approach Selection and Justification (5 points)
    - 5/5: Correctly identifies non-parametric AND provides valid justification
    - 4/5: Correctly identifies non-parametric but reasoning incomplete
    - 2/5: Identifies approach but reasoning mostly wrong
    - 0/5: Wrong approach or no justification

    Component 3: Descriptive Statistics Table (5 points)
    - 5/5: Table included, numbered, titled, introduced in text, proper APA formatting
    - 4/5: 4 elements present
    - 3/5: 3 elements present
    - 2/5: 2 elements present
    - 1/5: Table attempted but severely incomplete
    - 0/5: No table provided

    Component 4: Mean and Median for Men (5 points)
    - 5/5: Both mean AND median correctly provided in APA style
    - 3/5: Only one value provided correctly
    - 1/5: Values mentioned but unclear or incorrect
    - 0/5: Neither value provided

    STUDENT ANSWER:
    {student_answer}

    Return grading in this exact JSON format:
    {{
      "component_1_score": <0-5>,
      "component_1_explanation": "<brief explanation>",
      "component_2_score": <0-5>,
      "component_2_explanation": "<brief explanation>",
      "component_3_score": <0-5>,
      "component_3_explanation": "<brief explanation>",
      "component_4_score": <0-5>,
      "component_4_explanation": "<brief explanation>",
      "total_points": <0-20>,
      "max_points": 20,
      "percentage": <percentage>,
      "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
      "vibe": "<one-sentence overall impression>"
    }}"""

        element_check = self.check_required_elements(student_answer)

        result = self.grade_with_prompt(
                student_answer=student_answer,
                prompt=prompt,
                additional_checks={
                    "element_check": element_check
                }
            )

        if "error" not in result:
                component_keys = [
                    "component_1_score",
                    "component_2_score",
                    "component_3_score",
                    "component_4_score"
                ]
                result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results."""
        import textwrap
        print("=" * 60)
        print("GRADING RESULTS - QUESTION 7.3")
        print("Wilcoxon Signed Rank Test - Test Value / Approach / Table / Mean & Median")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Test Value & Source): {grading.get('component_1_score', 'N/A')}/5")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Approach & Justification): {grading.get('component_2_score', 'N/A')}/5")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Descriptive Table APA): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Mean & Median for Men): {grading.get('component_4_score', 'N/A')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points', 'N/A')}/{grading.get('max_points', 20)}")
        print(f"PERCENTAGE: {grading.get('percentage', 'N/A')}%")

        print("\n" + "=" * 60)
        print("FEEDBACK:")
        print("=" * 60)
        print(textwrap.fill(grading.get('feedback', 'No feedback available'), width=60))

        print("\n" + "=" * 60)
        print("THE VIBE:")
        print("=" * 60)
        print(textwrap.fill(grading.get('vibe', 'N/A'), width=60))

        if 'error' in grading:
            print("\n" + "=" * 60)
            print("ERROR:")
            print("=" * 60)
            print(grading.get('error'))
            if 'raw_response' in grading:
                print("\nRaw Response:")
                print(grading['raw_response'][:500])


if __name__ == "__main__":
    evaluator = Question7_3Evaluator()
    from config import InputHandler
    input_handler = InputHandler()
    student_answer = input_handler.collect_and_validate_input(
        question_name="QUESTION 7.3",
        question_description="Wilcoxon Signed Rank Test - Test Value / Approach / Table / Mean & Median",
        min_length=10
    )
    if student_answer:
        grading = evaluator.grade_question7_3_answer(student_answer)
        evaluator.print_grading_results(grading)