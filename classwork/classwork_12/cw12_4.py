"""
cw12_4.py
Classwork 12: Correlational Analysis
Effect size, correlation matrix, and plot informativeness
Evaluation method name: def grade_question_cw12_4_answer
"""

import re
from config import BaseEvaluator


class CW12_4Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 12_4.

    Task: Do you need to calculate the effect size? (5 points).
    If no, explain why. If yes, provide result (included into correlation matrix) and explain what does it mean,
    in one sentence (5 points).
    Following the Dr. E's video 04:47 minute, please explain why the plot is not so informative
    in case of Spearman correlation (5 points).
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
            "effect_size_decision": False,
            "effect_size_explanation": False,
            "plot_explanation": False
        }

        evidence = []

        # Task description (pedagogical anchors matching the task wording)
        pedagogical_markers = [
            "do you need to calculate the effect size",
            "if no, explain why",
            "if yes, provide the result",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Effect size decision
        if re.search(r'effect\s*size|r\s*=|r²|r\^2|cohen|small|medium|large|coefficient\s*of\s*determination', text_lower):
            elements_found["effect_size_decision"] = True
            evidence.append("Effect size decision found")
        else:
            evidence.append("Effect size decision NOT found")

        # Effect size explanation (result in matrix + interpretation)
        if re.search(r'matrix|table|because|since|due to|variance|proportion|magnitude|weak|moderate|strong|practical', text_lower):
            elements_found["effect_size_explanation"] = True
            evidence.append("Effect size explanation found")
        else:
            evidence.append("Effect size explanation NOT found")

        # Plot explanation (Spearman + plot informativeness reasoning)
        if re.search(r'spearman|rank|monotonic|linear|scatter|plot|informative|tied|ordinal|not\s*linear', text_lower):
            elements_found["plot_explanation"] = True
            evidence.append("Plot explanation found")
        else:
            evidence.append("Plot explanation NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def grade_question_cw12_4_answer(self, student_answer: str, test_mode: bool = False):

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
                feedback="[TEST MODE] Strong effect size and plot informativeness analysis.",
                vibe="Clear correlational follow-up analysis",
            )

        prompt = f"""You are grading a statistics assignment using a STRICT rubric.

TASK:
Students must complete 5 components.

RUBRIC:

Component 1: Task Description (1 point)
Component 2: Effect Size Decision (4 points)
Component 3: Effect Size Explanation (5 points)
Component 4: Plot Informativeness Explanation (5 points)
Component 5: Overall Clarity and Completeness (5 points)

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
        print("GRADING RESULTS - CLASSWORK 12.4")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Task Description): {grading.get('component_1_score')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Effect Size Decision): {grading.get('component_2_score')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Effect Size Explanation): {grading.get('component_3_score')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Plot Informativeness Explanation): {grading.get('component_4_score')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Overall Clarity and Completeness): {grading.get('component_5_score')}/5")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points')}/20")
        print(f"PERCENTAGE: {grading.get('percentage')}%")

        print("\nFEEDBACK:")
        print(textwrap.fill(grading.get('feedback', ''), width=60))


if __name__ == "__main__":
    evaluator = CW12_4Evaluator()

    from config import InputHandler
    input_handler = InputHandler()

    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 12.4",
        question_description="Effect Size, Correlation Matrix, and Plot Informativeness",
        min_length=10
    )

    if student_answer:
        grading = evaluator.grade_question_cw12_4_answer(student_answer)
        evaluator.print_grading_results(grading)
