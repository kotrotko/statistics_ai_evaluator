"""
cw12_3.py
Classwork 12: Correlational Analysis
Step system: Test selection and execution
Evaluation method name: def grade_question_cw12_3_answer
"""

import re
from config import BaseEvaluator


class CW12_3Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 12_3.

    Task: Using our Step system:
    Step 1. Based on your assumptions checking results, select the appropriate statistics (5 points).
    Justify your selection, i.e. explain why did you choose this form of correlational analysis (5 points).
    Step 2. State hypotheses in needed form. (5 points).
    Step 3. State the significance level α, calculate df, find the critical value. (5 points)
    Step 4. Compute the test statistic. Make the inference in terms of hypotheses statement (5 points).
    Total (strictly) 20 points.
    """

    def __init__(self):
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1200
        )

    def check_required_elements(self, student_answer: str) -> dict:
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "method_selection": False,
            "justification": False,
            "hypotheses": False,
            "statistical_execution": False
        }

        evidence = []

        # Task description (pedagogical anchors matching the step system)
        pedagogical_markers = [
            "based on your assumptions checking results,"
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Method selection (correlational analysis methods)
        if re.search(
            r'pearson|spearman|kendall|point[\s-]?biserial|phi[\s-]?coefficient|'
            r'correlation|correlational|parametric|non[\s-]?parametric',
            text_lower
        ):
            elements_found["method_selection"] = True
            evidence.append("Method selection found")
        else:
            evidence.append("Method selection NOT found")

        # Justification
        if re.search(r'because|since|due to|assumption|normal|linearity|monotonic|ordinal|interval|ratio|outlier', text_lower):
            elements_found["justification"] = True
            evidence.append("Justification found")
        else:
            evidence.append("Justification NOT found")

        # Hypotheses
        if re.search(r'h[0o]|h[1a]|null\s*hypothesis|alternative\s*hypothesis|ρ|rho|r\s*=\s*0|no\s*correlation', text_lower):
            elements_found["hypotheses"] = True
            evidence.append("Hypotheses found")
        else:
            evidence.append("Hypotheses NOT found")

        # Statistical execution + inference (merged)
        if re.search(r'α|alpha|df|t\s*=|r\s*=|statistic|p[\s-]?value|reject|fail to reject|conclude|critical', text_lower):
            elements_found["statistical_execution"] = True
            evidence.append("Statistical execution found")
        else:
            evidence.append("Statistical execution NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def grade_question_cw12_3_answer(self, student_answer: str, test_mode: bool = False):

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
                feedback="[TEST MODE] Strong structured answer.",
                vibe="Clear correlational analysis reasoning",
            )

        prompt = f"""You are grading a statistics assignment using a STRICT rubric.

TASK:
Students must complete 5 components.

RUBRIC:

Component 1: Task Description (1 point)
Component 2: Select the Appropriate Statistics (4 points)
Component 3: Justify Your Selection (5 points)
Component 4: State Hypotheses (5 points)
Component 5: Statistical Execution and Inference (5 points)

STUDENT ANSWER:
{student_answer}

Return JSON:
{{
  "component_1_score": <0-1>,
  "component_1_explanation": "...",
  "component_2_score": <0-4>,
  "component_2_explanation": "...",
  "component_3_score": <0-5>,
  "component_3_explanation": "...",
  "component_4_score": <0-5>,
  "component_4_explanation": "...",
  "component_5_score": <0-5>,
  "component_5_explanation": "...",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "...",
  "vibe": "..."
}}"""

        element_check = self.check_required_elements(student_answer)

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"element_check": element_check}
        )

        # Enforcement: task description check
        if "error" not in result:
            if not element_check["elements_found"]["task_description"]:
                result["component_1_score"] = 0
                result["component_1_explanation"] = "Task description NOT found (instructional phrasing missing)"
            else:
                result["component_1_score"] = 1
                result["component_1_explanation"] = "Task description found"

        if "error" not in result:
            result = self.validate_component_scores(
                result,
                [
                    "component_1_score",
                    "component_2_score",
                    "component_3_score",
                    "component_4_score",
                    "component_5_score",
                ],
                20
            )

        return result

    def print_grading_results(self, grading):
        import textwrap

        print("=" * 60)
        print("GRADING RESULTS - CLASSWORK 12.3")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Task Description): {grading.get('component_1_score')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Select the Appropriate Statistics): {grading.get('component_2_score')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Justify Your Selection): {grading.get('component_3_score')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (State Hypotheses): {grading.get('component_4_score')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Statistical Execution and Inference): {grading.get('component_5_score')}/5")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points')}/20")
        print(f"PERCENTAGE: {grading.get('percentage')}%")

        print("\nFEEDBACK:")
        print(textwrap.fill(grading.get('feedback', ''), width=60))


if __name__ == "__main__":
    evaluator = CW12_3Evaluator()

    from config import InputHandler
    input_handler = InputHandler()

    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 12.3",
        question_description="Correlational Analysis Step System",
        min_length=10
    )

    if student_answer:
        grading = evaluator.grade_question_cw12_3_answer(student_answer)
        evaluator.print_grading_results(grading)