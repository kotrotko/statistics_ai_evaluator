"""
cw9_2.py
Classwork 9: Independent groups comparison
Assumption checking: normality
Evaluation method name: def grade_question_cw9_2_answer
"""

import re
from config import BaseEvaluator


class CW9_2Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 9_2.

    Task: Which method do you apply to check normality? Name it. (5 points).
    Include the table, introduce, refer, number and title it in APA style (5 points).
    Are distributions normal, with significance level α = 0.001? (5 points).
    How did you know? Describe your logic in one sentence. (5 points).
    Total (strictly) 20 points.

    Evaluates student's ability to name the normality method, present table in APA style,
    state whether distributions are normal at α = 0.001, and explain the reasoning.

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
            "table_present": False,
            "normality_conclusion": False,
            "reasoning": False
        }

        evidence = []

        # Checkpoint 1 — Task description (Pedagogical markers)
        # Standardized naming with discriminative markers from the image
        pedagogical_markers = [
            "which method",
            "name it",
            "include relevant",
            "describe your logic",
            "justify your decision",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found (via pedagogical markers)")
        else:
            elements_found["task_description"] = False
            evidence.append("Task description NOT found")

        # Checkpoint 2 — Normality method (strict)
        if re.search(r'shapiro[\s-]?wilk|s-w\s*test|q[\s-]?q\s*plot|qq\s*plot', text_lower):
            elements_found["normality_method"] = True
            evidence.append("Normality method found")
        else:
            evidence.append("Normality method NOT found")

        # Checkpoint 3 — Table present
        if re.search(r'table\s*\d|p[\s-]?value|statistic', text_lower):
            elements_found["table_present"] = True
            evidence.append("Table found")
        else:
            evidence.append("Table NOT found")

        # Checkpoint 4 — Normality conclusion (yes/no)
        if re.search(r'distribution\s*is\s*(not\s*)?normal|is\s*(not\s*)?normally\s*distributed|normal\s*distribution|are\s*(not\s*)?normal', text_lower):
            elements_found["normality_conclusion"] = True
            evidence.append("Normality conclusion found")
        else:
            evidence.append("Normality conclusion NOT found")

        # Checkpoint 5 — Reasoning with α
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

    def grade_question_cw9_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 9.2: Assumption Checking - Normality.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 1,
                    "component_2_score": 4,
                    "component_3_score": 5,
                    "component_4_score": 5,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Method stated. Table present with minor APA issues. Normality conclusion clear. Reasoning correct.",
                vibe="Student shows solid understanding of normality testing and APA formatting",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "normality_method": True,
                            "table_present": True,
                            "normality_conclusion": True,
                            "reasoning": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics assignment about normality checking using a **STRICT rubric-based approach.

**TASK DESCRIPTION:**
Students must complete 4 components for normality assumption checking.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Focus on conceptual understanding over formatting
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

**RUBRIC:**

**Component 1: Task Description (1 point)**
- Use task_description from elements_found.
- 1/1: If task_description_present is True.
- 0/1: If task_description_present is False.

**Component 2: Name the Normality Method (4 points):**
- 4/4: Method name explicitly stated in a sentence (e.g., "I used the Shapiro-Wilk test")
- 2/4: Method mentioned but statement incomplete or unclear
- 0/4: Method name only in table header, or not mentioned at all
- CRITICAL: Method can be stated in dedicated sentence OR in table introduction phrase, but NOT only in table header

Acceptable methods: Shapiro-Wilk test, Q-Q plot

**Component 3: Table in APA Style (5 points):**
Evaluate each element (1 point each):
- 1 point: Introduction phrase before table appears
- 1 point: Reference to table by number in text (e.g., "Table 1")
- 1 point: Table number in APA style (e.g., "Table 1")
- 1 point: Table title in APA style (descriptive)
- 1 point: No table present.

APA table requirements:
1. Introduction before table appears
2. Reference to table in text (e.g., "as shown in Table 1")
3. Table number (e.g., "Table 1")
4. Descriptive title
5. Proper formatting (horizontal lines, clear labels)

**Component 4: Are Distributions Normal? (5 points):**
- 5/5: Clear yes/no statement about distributions being normal at α = 0.001, correct conclusion
- 0/5: No clear yes/no statement, or conclusion contradicts test results
- CRITICAL: Must explicitly state "distributions are normal" or "distributions are not normal" at α = 0.001
- Note: "distributions" is plural - student should address both groups

**Component 5: Explain Your Logic (5 points):**
- 1 point: Student attempts to explain
- 1 point [VIBE]: Use your judgment to assess whether the final conclusion is correct given the test results provided
- 3 points: Logic is correct (proper comparison of p-value with α = 0.001)
- CRITICAL: Evaluate logic and conclusion INDEPENDENTLY
- CRITICAL: If student correctly applies decision rule but final conclusion contradicts it, deduct 1 point for wrong conclusion only — logic (3 points) remains correct
- CRITICAL: If student incorrectly applies decision rule (e.g. p > α → not normal), deduct 3 points for wrong logic regardless of conclusion

STUDENT ANSWER:
{student_answer}

Return grading in this exact JSON format:
{{
  "component_1_score": <0-1>,
  "component_1_explanation": "<brief explanation>",
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief explanation>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief explanation>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief explanation>",
  "component_5_score": <0-5>,
  "component_5_explanation": "<brief explanation>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment>",
  "vibe": "<one-sentence overall impression>"
}}"""

        element_check = self.check_required_elements(student_answer)
        element_summary = element_check["elements_found"]

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "element_check": element_check
            }
        )

        # Force the score to 0 if the pedagogical markers are missing
        if "error" not in result:
            if not element_check["elements_found"]["task_description"]:
                result["component_1_score"] = 0
                result["component_1_explanation"] = "Task description NOT found (instructional phrasing missing)"

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
        """Display grading results."""
        import textwrap
        print("=" * 60)
        print("GRADING RESULTS - CLASSWORK 9.2")
        print("Assumption Checking: Normality")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Task Description): {grading.get('component_1_score', 'N/A')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Normality Method): {grading.get('component_2_score', 'N/A')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Table APA Style): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Normality Conclusion): {grading.get('component_4_score', 'N/A')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Logic/Reasoning): {grading.get('component_5_score', 'N/A')}/5")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

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
    evaluator = CW9_2Evaluator()
    from config import InputHandler

    input_handler = InputHandler()
    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 9.2",
        question_description="Assumption Checking: Normality",
        min_length=10
    )
    if student_answer:
        grading = evaluator.grade_question_cw9_2_answer(student_answer)
        evaluator.print_grading_results(grading)