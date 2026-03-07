"""
cw8_2.py
Classwork 8: Repeated Measures
Normality Check - Method / Normal Distribution / Reasoning
Evaluation method name: def grade_cw8_2_answer
"""

import re
from config import BaseEvaluator


class CW8_2Evaluator (BaseEvaluator):
    """
    Evaluator for Normality Check (CW8_2).

    Task: Check normality assumption (5 points). Which method did you apply to check normality? (5 points).
    Is this distribution normal, with significance level α = 0.001? (5 points) How did you know? (5 points).
    Total (strictly) 20 points.

    Evaluates student's ability to check normality assumption, name the method used,
    state whether distribution is normal at α = 0.001, and explain the reasoning.

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
            "task_description": False,
            "normality_method": False,
            "normality_conclusion": False,
            "reasoning": False
        }

        evidence = []

        # Checkpoint 1 — Task description
        task_full_text = "Check normality assumption (5 points). Which method did you apply to check normality? (5 points). Is this distribution normal, with significance level α = 0.001? (5 points) How did you know? (5 points)."

        if task_full_text.lower() in text_lower:
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Checkpoint 2 — Normality method (strict)
        if re.search(r'shapiro[\s-]?wilk|normality\s*test|s-w\s*test|kolmogorov|anderson', text_lower):
            elements_found["normality_method"] = True
            evidence.append("Normality method found")
        else:
            evidence.append("Normality method NOT found")

        # Checkpoint 3 — Normality conclusion (yes/no)
        if re.search(r'distribution\s*is\s*(not\s*)?normal|is\s*(not\s*)?normally\s*distributed|normal\s*distribution', text_lower):
            elements_found["normality_conclusion"] = True
            evidence.append("Normality conclusion found")
        else:
            evidence.append("Normality conclusion NOT found")

        # Checkpoint 4 — Reasoning with α
        if re.search(r'α\s*=\s*0\.001|alpha\s*=\s*0\.001|significance\s*level', text_lower) and \
                re.search(r'p[\s-]?value|p\s*[<>]=?\s*0\.', text_lower):
            elements_found["reasoning"] = True
            evidence.append("Reasoning with α found")
        else:
            evidence.append("Reasoning with α NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_cw8_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 8.2: Normality Check.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 0,
                    "component_2_score": 5,
                    "component_3_score": 0,
                    "component_4_score": 3,
                },
                max_points=20,
                feedback="[TEST MODE] Method not stated explicitly. Normality assumption checked. No clear yes/no conclusion. Reasoning partially correct.",
                vibe="Student shows partial understanding; normality method and conclusion need improvement",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "task_description": False,
                            "normality_method": False,
                            "normality_conclusion": False,
                            "reasoning": True
                        },
                        "all_present": False,
                        "evidence": ["Test mode - partial elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics assignment about normality checking using a **STRICT rubric-based approach.

**TASK DESCRIPTION:**
Students must complete 4 components for a normality assumption check.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Focus on conceptual understanding over formatting
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

**RUBRIC:**

**Component 1: Check Normality Assumption (5 points):**

PREREQUISITE: Task description must be pasted in answer. If missing → 0/5.

If task description present, evaluate whether normality was checked:
- 5/5: Clear evidence that normality assumption was checked (test performed, results shown)
- 3/5: Normality check mentioned but incomplete
- 0/5: No task description OR no evidence of normality check

**Component 2: Name the Normality Method (5 points):**
- 5/5: Method name explicitly stated in a sentence (e.g., "I used the Shapiro-Wilk test")
- 3/5: Method mentioned but statement incomplete or unclear
- 0/5: Method name only in table header, or not mentioned at all
- CRITICAL: Must explicitly state the method name in text, not just in a table

**Component 3: Is This Distribution Normal? (5 points):**
- 5/5: Clear yes/no statement about normality at α = 0.001, correct conclusion
- 0/5: No clear yes/no statement, or conclusion contradicts test results
- CRITICAL: Must explicitly state "distribution is normal" or "distribution is not normal" at α = 0.001

**Component 4: Explain Your Reasoning (5 points):**
- 1 point: Student attempts to explain
- 1 point [VIBE]: Use your judgment to assess whether the final conclusion is correct given the test results provided
- 3 points: Reasoning is correct (proper comparison of p-value with α = 0.001)
- CRITICAL: Evaluate reasoning and conclusion INDEPENDENTLY
- CRITICAL: If student correctly applies decision rule but final conclusion contradicts it, deduct 1 point for wrong conclusion only — reasoning (3 points) remains correct
- CRITICAL: If student incorrectly applies decision rule (e.g. p > α → not normal), deduct 3 points for wrong reasoning regardless of conclusion

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
        print("GRADING RESULTS - CLASSWORK 8.2")
        print("Normality Check - Method / Normal Distribution / Reasoning")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Check Normality): {grading.get('component_1_score', 'N/A')}/5")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Normality Method): {grading.get('component_2_score', 'N/A')}/5")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Normal Distribution): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Reasoning): {grading.get('component_4_score', 'N/A')}/5")
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
    evaluator = CW8_2Evaluator()
    from config import InputHandler

    input_handler = InputHandler()
    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 8.2",
        question_description="Normality Check - Method / Normal Distribution / Reasoning",
        min_length=10
    )
    if student_answer:
        grading = evaluator.grade_cw8_2_answer(student_answer)
        evaluator.print_grading_results(grading)