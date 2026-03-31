"""
cw10_5.py
Classwork 10: One Way ANOVA
Summary with JASP table and research question
Evaluation method name: def grade_question_cw10_5_answer
"""

import re
from config import BaseEvaluator


class CW10_5Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 10_5.

    Task: Add the JASP table ANOVA-Score (5 points), name and title in APA style (5 points)
    and describe it briefly, following example on 12:48 and 13:07 of our video (5 points).
    Answer the main Research question (5 points). Your answer should be aligned with the results
    and phrased in terms of group differences (or lack thereof).
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
            "jasp_table": False,
            "apa_formatting": False,
            "table_description": False,
            "research_question": False
        }

        evidence = []

        # Task description (pedagogical markers)
        pedagogical_markers = [
            "add the jasp table anova",
            "name and title",
            "describe it",
            "answer the main research question",
            "your answer"
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # JASP table presence
        jasp_indicators = [
            "jasp",
            "table",
            "anova",
            r"f\s*=",
            r"p\s*[=<>]",
            "sum of squares",
            "mean square",
            "df"
        ]
        if any(re.search(pattern, text_lower) for pattern in jasp_indicators):
            elements_found["jasp_table"] = True
            evidence.append("JASP table indicators found")
        else:
            evidence.append("JASP table indicators NOT found")

        # APA formatting indicators
        apa_indicators = [
            "table",
            "figure",
            r"f\(\d+,\s*\d+\)",
            "anova",
            "note\.",
            "italicized",
            "italic"
        ]
        if any(re.search(pattern, text_lower) for pattern in apa_indicators):
            elements_found["apa_formatting"] = True
            evidence.append("APA formatting indicators found")
        else:
            evidence.append("APA formatting indicators NOT found")

        # Table description
        description_indicators = [
            "shows",
            "indicates",
            "reveals",
            "demonstrates",
            "displays",
            "presents",
            "significant",
            "not significant",
            "difference",
            "effect"
        ]
        if any(indicator in text_lower for indicator in description_indicators):
            elements_found["table_description"] = True
            evidence.append("Table description found")
        else:
            evidence.append("Table description NOT found")

        # Research question answer
        research_indicators = [
            "research question",
            "main question",
            "therefore",
            "thus",
            "in conclusion",
            "results show",
            "found that",
            "difference between",
            "no difference",
            "significant difference",
            "groups differ",
            "groups do not differ"
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

    def grade_question_cw10_5_answer(self, student_answer: str, test_mode: bool = False):

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
                feedback="[TEST MODE] Complete ANOVA summary with proper APA formatting.",
                vibe="Well-structured summary",
            )

        prompt = f"""You are grading a statistics assignment using a STRICT rubric.

TASK:
Students must complete 5 components for an ANOVA summary.

RUBRIC:

Component 1: Task Description (1 point)
- Student includes pedagogical markers indicating they understand the task

Component 2: JASP Table ANOVA-Score (4 points)
- 4 points: Complete JASP table with all necessary statistics (F, df, p, MS, SS)
- 3 points: Table present but missing some elements
- 1-2 points: Partial table or incorrect values
- 0 points: No table present

Component 3: Name and Title in APA Style (5 points)
- 5 points: Proper APA formatting (Table number, descriptive title, italics where needed, note if applicable)
- 3-4 points: Most APA elements present but minor errors
- 1-2 points: Minimal APA formatting attempted
- 0 points: No APA formatting

Component 4: Brief Description of Table (5 points)
- 5 points: Clear description following video examples (12:48 and 13:07), mentions key statistics
- 3-4 points: Adequate description but missing some details
- 1-2 points: Minimal description
- 0 points: No description

Component 5: Answer to Main Research Question (5 points)
- 5 points: Clear answer aligned with results, phrased in terms of group differences/similarities
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

        # Enforcement: Task description
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
        print("GRADING RESULTS - CLASSWORK 10.5")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Task Description): {grading.get('component_1_score')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (JASP Table ANOVA-Score): {grading.get('component_2_score')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (APA Style Name and Title): {grading.get('component_3_score')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Table Description): {grading.get('component_4_score')}/5")
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
    evaluator = CW10_5Evaluator()

    from config import InputHandler
    input_handler = InputHandler()

    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 10.5",
        question_description="ANOVA Summary with JASP Table and Research Question",
        min_length=10
    )

    if student_answer:
        grading = evaluator.grade_question_cw10_5_answer(student_answer)
        evaluator.print_grading_results(grading)