"""
cw8_5.py
Classwork 8: Repeated Measures
Summary - APA Style Result Description / Research Question Answer
Evaluation method name: def grade_cw8_5_answer
"""

import re
from config import BaseEvaluator


class CW8_5Evaluator(BaseEvaluator):
    """
    Evaluator for Summary and Conclusion (CW8_5).

    Task: Describe the result in APA style, following the example at 12:47 of our video (10 points).
    Answer the main research question (10 points).
    Total (strictly) 20 points.

    Evaluates student's ability to summarize statistical results in proper APA format and
    answer the research question based on the analysis.

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
        Check if required structural and content elements are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "apa_result": False,
            "research_answer": False
        }

        evidence = []

        # Checkpoint 1 — Task description
        task_full_text = "Describe the result in APA style, following the example at 12:47 of our video (10 points). Answer the main research question (10 points)."

        if task_full_text.lower() in text_lower:
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Checkpoint 2 — APA style result description
        if re.search(r't\s*\(\d+\)\s*=|f\s*\(\d+,\s*\d+\)\s*=|p\s*[<>=]|m\s*=|sd\s*=|cohen|effect', text_lower):
            elements_found["apa_result"] = True
            evidence.append("APA style result found")
        else:
            evidence.append("APA style result NOT found")

        # Checkpoint 3 — Research question answer
        if re.search(r'research\s*question|conclude|conclusion|result|finding|evidence\s*suggest|data\s*show',
                     text_lower):
            elements_found["research_answer"] = True
            evidence.append("Research question answer found")
        else:
            evidence.append("Research question answer NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_cw8_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 8.5: Summary and Conclusion.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 8,
                    "component_2_score": 9,
                },
                max_points=20,
                feedback="[TEST MODE] APA result description mostly correct. Research question answered clearly.",
                vibe="Student demonstrates good understanding of APA formatting and draws appropriate conclusions",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "task_description": True,
                            "apa_result": True,
                            "research_answer": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics assignment about summary and conclusion using a **STRICT rubric-based approach.

**TASK DESCRIPTION:**
Students must complete 2 components: (1) describe results in APA style following the video example at 12:47, (2) answer the main research question.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Focus on APA formatting accuracy and clear research question answer
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

**RUBRIC:**

**Component 1: APA Style Result Description (10 points):**

PREREQUISITE: Task description must be pasted in answer. If missing → 0/10.

If task description present, evaluate APA result description:
- 10/10: Complete APA format result with all elements: test statistic with df, p-value, means/SD, effect size, and proper sentence structure
- 8-9/10: APA format mostly correct but minor element missing or formatting issue
- 6-7/10: APA format attempted but missing key elements (e.g., no effect size, no means)
- 4-5/10: Partial APA format with significant issues
- 2-3/10: Minimal attempt at APA format
- 0/10: No task description OR no APA result description

CRITICAL APA ELEMENTS REQUIRED:
- Test statistic with degrees of freedom (e.g., t(16) = 4.23 or F(1,16) = 17.89)
- P-value (e.g., p < .001 or p = .023)
- Descriptive statistics (M and SD for groups/conditions)
- Effect size (Cohen's d or eta-squared)
- Proper sentence format (e.g., "A paired-samples t-test revealed...")

**Component 2: Answer the Main Research Question (10 points):**
- 10/10: Clear, direct answer to research question based on statistical results with proper interpretation
- 8-9/10: Research question answered but lacks some clarity or detail
- 6-7/10: Answer attempted but unclear or incomplete connection to results
- 4-5/10: Vague answer that doesn't clearly address research question
- 2-3/10: Minimal attempt to answer
- 0/10: No answer to research question

CRITICAL: Must explicitly state what the research question asked and provide a clear answer based on the statistical findings

STUDENT ANSWER:
{student_answer}

Return grading in this exact JSON format:
{{
  "component_1_score": <0-10>,
  "component_1_explanation": "<brief explanation>",
  "component_2_score": <0-10>,
  "component_2_explanation": "<brief explanation>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment>",
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
                "component_2_score"
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results."""
        import textwrap
        print("=" * 60)
        print("GRADING RESULTS - CLASSWORK 8.5")
        print("Summary - APA Result / Research Question Answer")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (APA Style Result): {grading.get('component_1_score', 'N/A')}/10")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Research Question Answer): {grading.get('component_2_score', 'N/A')}/10")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

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
    evaluator = CW8_5Evaluator()
    from config import InputHandler

    input_handler = InputHandler()
    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 8.5",
        question_description="Summary - APA Style Result Description / Research Question Answer",
        min_length=30
    )
    if student_answer:
        grading = evaluator.grade_cw8_5_answer(student_answer)
        evaluator.print_grading_results(grading)