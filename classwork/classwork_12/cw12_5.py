"""
cw12_5.py
Classwork 12: Correlational Analysis
Summary with correlation matrix, heatmap, and research question
Evaluation method name: def grade_question_cw12_5_answer
"""

import re
from config import BaseEvaluator


class CW12_5Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 12_5.

    Task: Add the correlation matrix. How many significant correlations do you see? Flag them (5 points).
    Add a Heatmap (5 points).
    Describe your results following the example on 15.03 and 15.18 minutes of Dr. Todd's video (5 points).
    Answer the main Research question (5 points). Your answer should be aligned with the results
    and phrased in terms of correlation (or lack thereof).
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
            "correlation_matrix": False,
            "heatmap": False,
            "results_description": False,
            "research_question": False
        }

        evidence = []

        # Task description (pedagogical anchors that students would NOT naturally write)
        # Deliberately narrow: only phrases copied verbatim from the task instructions
        pedagogical_markers = [
            "how many significant correlations do you see",
            "describe your results",
            "your answer should be aligned with the results",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Correlation matrix presence
        matrix_indicators = [
            "correlation matrix",
            "matrix",
            r"r\s*=",
            r"p\s*[=<>]",
            "pearson",
            "spearman",
            "kendall",
            r"\*\*",
            r"\*"
        ]
        if any(re.search(pattern, text_lower) for pattern in matrix_indicators):
            elements_found["correlation_matrix"] = True
            evidence.append("Correlation matrix indicators found")
        else:
            evidence.append("Correlation matrix indicators NOT found")

        # Heatmap presence
        heatmap_indicators = [
            "heatmap",
            "heat map",
            "color",
            "colour",
            "gradient",
            "shading"
        ]
        if any(indicator in text_lower for indicator in heatmap_indicators):
            elements_found["heatmap"] = True
            evidence.append("Heatmap indicators found")
        else:
            evidence.append("Heatmap indicators NOT found")

        # Results description
        description_indicators = [
            "shows",
            "indicates",
            "reveals",
            "demonstrates",
            "significant",
            "not significant",
            "positive",
            "negative",
            "strong",
            "weak",
            "moderate",
            "correlation"
        ]
        if any(indicator in text_lower for indicator in description_indicators):
            elements_found["results_description"] = True
            evidence.append("Results description found")
        else:
            evidence.append("Results description NOT found")

        # Research question answer
        research_indicators = [
            "research question",
            "main question",
            "therefore",
            "thus",
            "in conclusion",
            "results show",
            "found that",
            "significant correlation",
            "no correlation",
            "no significant correlation",
            "correlated",
            "not correlated"
        ]
        if any(indicator in text_lower for indicator in research_indicators):
            elements_found["research_question"] = True
            evidence.append("Research question answer found")
        else:
            evidence.append("Research question answer NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def grade_question_cw12_5_answer(self, student_answer: str, test_mode: bool = False):

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
                feedback="[TEST MODE] Complete correlational summary with proper matrix and heatmap.",
                vibe="Well-structured correlational summary",
            )

        prompt = f"""You are grading a statistics assignment using a STRICT rubric.

TASK:
Students must complete 5 components for a correlational analysis summary.

RUBRIC:

Component 1: Task Description (1 point)

Component 2: Correlation Matrix with Flagged Significant Correlations (4 points)
- 4 points: Complete correlation matrix with significant correlations clearly flagged (e.g., asterisks) and count stated
- 3 points: Matrix present but flagging incomplete or count missing
- 1-2 points: Partial matrix or no flagging attempted
- 0 points: No matrix present

Component 3: Heatmap (5 points)
- 5 points: Heatmap present and described or referenced clearly
- 3-4 points: Heatmap mentioned but not described or only partially addressed
- 1-2 points: Minimal reference to heatmap
- 0 points: No heatmap

Component 4: Description of Results (5 points)
- 5 points: Clear description following video example style, mentions direction, strength, and significance of correlations
- 3-4 points: Adequate description but missing some details (e.g., no mention of direction or strength)
- 1-2 points: Minimal description
- 0 points: No description

Component 5: Answer to Main Research Question (5 points)
- 5 points: Clear answer aligned with results, phrased in terms of correlation or lack thereof
- 3-4 points: Answer present but not clearly aligned or poorly phrased
- 1-2 points: Vague or incomplete answer
- 0 points: No answer to research question

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
        print("GRADING RESULTS - CLASSWORK 12.5")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Task Description): {grading.get('component_1_score')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Correlation Matrix with Flagged Significant Correlations): {grading.get('component_2_score')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Heatmap): {grading.get('component_3_score')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Description of Results): {grading.get('component_4_score')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Research Question Answer): {grading.get('component_5_score')}/5")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points')}/20")
        print(f"PERCENTAGE: {grading.get('percentage')}%")

        print("\nFEEDBACK:")
        print(textwrap.fill(grading.get('feedback', ''), width=60))


if __name__ == "__main__":
    evaluator = CW12_5Evaluator()

    from config import InputHandler
    input_handler = InputHandler()

    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 12.5",
        question_description="Correlational Analysis Summary with Matrix, Heatmap, and Research Question",
        min_length=10
    )

    if student_answer:
        grading = evaluator.grade_question_cw12_5_answer(student_answer)
        evaluator.print_grading_results(grading)