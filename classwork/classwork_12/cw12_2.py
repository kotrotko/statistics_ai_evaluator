"""
cw12_2.py
Classwork 12: Spearman's Rho correlation
Bivariate normality check and justification for Spearman's correlation
Evaluation method name: def grade_question_cw12_2_answer
"""

import re
from config import BaseEvaluator


class CW12_2Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 12_2.

    Task: Check normality assumption using the bivariate normality test (5 points).
    If you see more than 5 normality violations, use it as a reason to apply Spearman's correlation. Write it down (5 points).
    Include the table, number and name it (10 points).
    Total (strictly) 20 points.

    Evaluates student's ability to check bivariate normality, justify Spearman's correlation,
    and present table in APA style.

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
            "violations_count": False,
            "spearman_justification": False,
            "table_present": False
        }

        evidence = []

        # Checkpoint 1 — Task description (Pedagogical markers)
        pedagogical_markers = [
            "check normality",
            "include the table",
            "number and name it",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found (via pedagogical markers)")
        else:
            elements_found["task_description"] = False
            evidence.append("Task description NOT found")

        # Checkpoint 2 — Normality method
        if re.search(r'bivariate\s*normality|normality\s*test|mardia|henze|royston', text_lower):
            elements_found["normality_method"] = True
            evidence.append("Normality method found")
        else:
            evidence.append("Normality method NOT found")

        # Checkpoint 3 — Violations count
        if re.search(r'violation|more\s*than\s*5|\d+\s*violation|\bviolat', text_lower):
            elements_found["violations_count"] = True
            evidence.append("Violations count found")
        else:
            evidence.append("Violations count NOT found")

        # Checkpoint 4 — Spearman justification
        if re.search(r'spearman|rank\s*correlation|non[\s-]?parametric', text_lower):
            elements_found["spearman_justification"] = True
            evidence.append("Spearman justification found")
        else:
            evidence.append("Spearman justification NOT found")

        # Checkpoint 5 — Table present
        if re.search(r'table\s*\d|p[\s-]?value|statistic|bivariate', text_lower):
            elements_found["table_present"] = True
            evidence.append("Table found")
        else:
            evidence.append("Table NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_question_cw12_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 12.2: Bivariate Normality Check and Spearman Justification.
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
                    "component_4_score": 10,
                },
                max_points=20,
                feedback="[TEST MODE] Normality check present. Violations counted. Spearman justified. Table present with APA formatting.",
                vibe="Student demonstrates clear understanding of bivariate normality and Spearman justification",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "task_description": True,
                            "normality_method": True,
                            "violations_count": True,
                            "spearman_justification": True,
                            "table_present": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics assignment about bivariate normality checking and justification for Spearman's correlation using a **STRICT rubric-based approach.

**TASK DESCRIPTION:**
Students must complete 4 components for bivariate normality checking and Spearman justification.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Focus on conceptual understanding over formatting
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

**RUBRIC:**

**Component 1: Task Description (1 point):**
- 1 point: Student includes pedagogical markers indicating they understand the task
- 0 points: No task description present

**Component 2: Check Bivariate Normality (4 points):**
- 4 points: Bivariate normality test performed and clearly described using JASP
- 3 points: Normality check mentioned but method unclear or incomplete
- 1 point: Normality mentioned but not checked or described
- 0 points: No normality check present

Acceptable normality methods: bivariate normality test in JASP

**Component 3: Violations Count and Spearman Justification (5 points):**
This component combines:
- Count of normality violations identified
- Written justification for applying Spearman's correlation

Breaking down the 5 points:
- 2 points: Student explicitly states the number of normality violations observed
- 3 points: Student clearly writes that more than 5 violations justify using Spearman's correlation

CRITICAL: Student must explicitly connect the violation count to the decision to use Spearman's correlation
CRITICAL: Justification must be written out, not implied

**Component 4: Include Table in APA Style (10 points):**
This component combines:
- Table included and referenced
- Table numbered and named in APA style

Breaking down the 10 points:
- 2 points: Table is present in the answer
- 2 points: Table is referenced in the text (e.g., "as shown in Table 1")
- 2 points: Table number in APA style (e.g., "Table 1")
- 2 points: Descriptive table title in APA style
- 2 points: Introduction phrase before table appears

APA table requirements:
1. Introduction before table appears
2. Reference to table in text (e.g., "as shown in Table 1")
3. Table number (e.g., "Table 1")
4. Descriptive title
5. Proper formatting (horizontal lines, clear labels)

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
  "component_4_score": <0-10>,
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

        # Enforcement: Task description
        if "error" not in result:
            if not element_check["elements_found"]["task_description"]:
                result["component_1_score"] = 0
                result["component_1_explanation"] = "Task description NOT found (instructional phrasing missing)"
            else:
                result["component_1_score"] = 1
                result["component_1_explanation"] = "Task description found"

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
        """Display grading results."""
        import textwrap
        print("=" * 60)
        print("GRADING RESULTS - CLASSWORK 12.2")
        print("Bivariate Normality Check and Spearman Justification")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Task Description): {grading.get('component_1_score', 'N/A')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Bivariate Normality Check): {grading.get('component_2_score', 'N/A')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Violations Count & Spearman Justification): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Table in APA Style): {grading.get('component_4_score', 'N/A')}/10")
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
    evaluator = CW12_2Evaluator()
    from config import InputHandler

    input_handler = InputHandler()
    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 12.2",
        question_description="Bivariate Normality Check and Spearman Justification",
        min_length=10
    )
    if student_answer:
        grading = evaluator.grade_question_cw12_2_answer(student_answer)
        evaluator.print_grading_results(grading)