"""
cw10_4.py
Classwork 10: One Way ANOVA
Post hoc testing and effect size
Evaluation method name: def grade_question_cw10_4_answer
"""

import re
from config import BaseEvaluator


class CW10_4Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 10_4.

    Task: Do you need a post hoc test? (5 points).
    If no, explain why. If yes, provide result (including a table) and explain what does it mean (5 points).
    Do you need to calculate effect size η^2 ? (5 points).
    If no, explain why. If yes, provide the result and explain what does it mean. (5 points).
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
            "post_hoc_decision": False,
            "post_hoc_explanation": False,
            "effect_size_decision": False,
            "effect_size_explanation": False
        }

        evidence = []

        # Task description (cw9-style pedagogical anchors)
        pedagogical_markers = [
            "do you need a post hoc",
            "if no, explain why",
            "if yes, provide the result",
            "do you need to calculate effect size",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Post hoc decision
        if re.search(r'post[\s-]?hoc|tukey|bonferroni|scheffe|dunnett|holm|sidak', text_lower):
            elements_found["post_hoc_decision"] = True
            evidence.append("Post hoc decision found")
        else:
            evidence.append("Post hoc decision NOT found")

        # Post hoc explanation
        if re.search(r'because|since|due to|significant|reject|comparison|pairwise|difference', text_lower):
            elements_found["post_hoc_explanation"] = True
            evidence.append("Post hoc explanation found")
        else:
            evidence.append("Post hoc explanation NOT found")

        # Effect size decision
        if re.search(r'η|eta|effect\s*size|omega|cohen', text_lower):
            elements_found["effect_size_decision"] = True
            evidence.append("Effect size decision found")
        else:
            evidence.append("Effect size decision NOT found")

        # Effect size explanation
        if re.search(r'small|medium|large|variance|proportion|practical|magnitude', text_lower):
            elements_found["effect_size_explanation"] = True
            evidence.append("Effect size explanation found")
        else:
            evidence.append("Effect size explanation NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def grade_question_cw10_4_answer(self, student_answer: str, test_mode: bool = False):

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
                feedback="[TEST MODE] Strong post hoc and effect size analysis.",
                vibe="Clear follow-up analysis",
            )

        prompt = f"""You are grading a statistics assignment using a STRICT rubric.

TASK:
Students must complete 5 components.

RUBRIC:

Component 1: Task Description (1 point)
Component 2: Post Hoc Test Decision (4 points)
Component 3: Post Hoc Test Explanation (5 points)
Component 4: Effect Size Decision (5 points)
Component 5: Effect Size Explanation (5 points)

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

        # cw9 enforcement
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
        print("GRADING RESULTS - CLASSWORK 10.4")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Task Description): {grading.get('component_1_score')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Post Hoc Test Decision): {grading.get('component_2_score')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Post Hoc Test Explanation): {grading.get('component_3_score')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Effect Size Decision): {grading.get('component_4_score')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Effect Size Explanation): {grading.get('component_5_score')}/5")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points')}/20")
        print(f"PERCENTAGE: {grading.get('percentage')}%")

        print("\nFEEDBACK:")
        print(textwrap.fill(grading.get('feedback', ''), width=60))


if __name__ == "__main__":
    evaluator = CW10_4Evaluator()

    from config import InputHandler
    input_handler = InputHandler()

    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 10.4",
        question_description="Post Hoc Testing and Effect Size",
        min_length=10
    )

    if student_answer:
        grading = evaluator.grade_question_cw10_4_answer(student_answer)
        evaluator.print_grading_results(grading)
