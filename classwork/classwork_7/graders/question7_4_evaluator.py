"""
question7_4_evaluator.py
Hypothesis Testing - Wilcoxon Table / APA Formatting / Interpretation / Descriptive Plot
"""
import re

from config import BaseEvaluator

class Question7_4Evaluator(BaseEvaluator):
    """
        Evaluator for Question 7_4: Wilcoxon Test Results and Interpretation.

        Evaluates student's ability to include and format the Wilcoxon table,
        interpret the results, and provide a descriptive plot with CI interpretation.

        Inherits common functionality from BaseEvaluator.
        Contains only question-specific logic.
        """

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
            "wilcoxon_table": False,
            "apa_formatting": False,
            "wilcoxon_interpretation": False,
            "descriptive_plot": False
        }

        evidence = []

        # Checkpoint 1 — Wilcoxon table (V, p)
        if re.search(r'wilcoxon|v\s*=|statistic', text_lower) and \
                re.search(r'p[\s-]?value|p\s*[<>=]', text_lower):
            elements_found["wilcoxon_table"] = True
            evidence.append("Wilcoxon table found")
        else:
            evidence.append("Wilcoxon table NOT found")

        # Checkpoint 2 — APA numbering and title of Wilcoxon table
        if re.search(r'table\s*\d+|table\s*[1-9]', text_lower) and \
                re.search(r'wilcoxon|signed|rank', text_lower):
            elements_found["apa_formatting"] = True
            evidence.append("APA table numbering and title found")
        else:
            evidence.append("APA table numbering and title NOT found")

        # Checkpoint 3 — Interpretation of Wilcoxon results
        if re.search(r'reject|fail\s*to\s*reject|significant|null\s*hypothesis', text_lower) and \
                re.search(r'p[\s-]?value|α|alpha', text_lower):
            elements_found["wilcoxon_interpretation"] = True
            evidence.append("Wilcoxon interpretation found")
        else:
            evidence.append("Wilcoxon interpretation NOT found")

        # Checkpoint 4 — Descriptive plot with CI 95% and interpretation
        if re.search(r'plot|figure|graph|chart', text_lower) and \
                re.search(r'confidence\s*interval|ci\s*95|95\s*%', text_lower):
            elements_found["descriptive_plot"] = True
            evidence.append("Descriptive plot with CI found")
        else:
            evidence.append("Descriptive plot with CI NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_question7_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 7.4: Wilcoxon Table / APA Formatting / Interpretation / Descriptive Plot.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 5,
                    "component_2_score": 3,
                    "component_3_score": 3,
                    "component_4_score": 2,
                },
                max_points=20,
                feedback="[TEST MODE] Wilcoxon table present. APA formatting incomplete. Interpretation partial. Plot missing CI interpretation.",
                vibe="Student shows partial understanding; APA formatting and plot interpretation need improvement",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "wilcoxon_table": True,
                            "apa_formatting": False,
                            "wilcoxon_interpretation": True,
                            "descriptive_plot": False
                        },
                        "all_present": False,
                        "evidence": ["Test mode - partial elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics assignment about Wilcoxon Signed Rank test results using a **STRICT rubric-based approach**.

    **TASK DESCRIPTION:**
    Students must complete 4 components for Wilcoxon test results presentation and interpretation.

    **IMPORTANT GRADING RULES:**
    1. Total score MUST be exactly 20 points
    2. Focus on conceptual understanding over formatting
    3. Feedback should be SHORT, written as a teacher's comment
    4. Feedback CANNOT be an invitation for further discussion
    5. Award partial credit where reasoning is mostly correct but incomplete

    **RUBRIC:**

    Component 1: Wilcoxon Table with V and p (5 points)
    - 5/5: Table included with both V and p values clearly presented
    - 3/5: Table present but missing V or p value
    - 1/5: Values mentioned in text but no table
    - 0/5: No table provided

    Component 2: APA Numbering and Title (5 points)
    - 5/5: Table numbered (e.g. Table 1), properly titled, introduced in text, APA style
    - 4/5: 3 elements present
    - 3/5: 2 elements present
    - 1/5: Table attempted but severely incomplete
    - 0/5: No APA formatting at all

    Component 3: Interpretation of Wilcoxon Results (5 points)
    - 5/5: Correctly interprets V and p, states reject/fail to reject H0, links to α
    - 3/5: Partial interpretation, missing reject/fail to reject or α comparison
    - 1/5: Mentions significance but reasoning unclear
    - 0/5: No interpretation provided

    Component 4: Descriptive Plot with CI 95% and Interpretation (5 points)
    - 5/5: Plot included with CI 95% and correctly interpreted
    - 3/5: Plot included but interpretation missing or incomplete
    - 1/5: Plot mentioned but not shown or no CI
    - 0/5: No plot provided

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
            print("GRADING RESULTS - QUESTION 7.4")
            print("Wilcoxon Table / APA Formatting / Interpretation / Descriptive Plot")
            print("=" * 60)

            if 'component_1_score' in grading:
                print("\nCOMPONENT BREAKDOWN:")
                print(f"  Component 1 (Wilcoxon Table V & p): {grading.get('component_1_score', 'N/A')}/5")
                if grading.get('component_1_explanation'):
                    print(f"    → {grading.get('component_1_explanation')}")

                print(f"  Component 2 (APA Numbering & Title): {grading.get('component_2_score', 'N/A')}/5")
                if grading.get('component_2_explanation'):
                    print(f"    → {grading.get('component_2_explanation')}")

                print(f"  Component 3 (Interpretation): {grading.get('component_3_score', 'N/A')}/5")
                if grading.get('component_3_explanation'):
                    print(f"    → {grading.get('component_3_explanation')}")

                print(f"  Component 4 (Descriptive Plot CI 95%): {grading.get('component_4_score', 'N/A')}/5")
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
    evaluator = Question7_4Evaluator()
    from config import InputHandler
    input_handler = InputHandler()
    student_answer = input_handler.collect_and_validate_input(
        question_name="QUESTION 7.4",
        question_description="Wilcoxon Table / APA Formatting / Interpretation / Descriptive Plot",
        min_length=10
    )
    if student_answer:
        grading = evaluator.grade_question7_4_answer(student_answer)
        evaluator.print_grading_results(grading)