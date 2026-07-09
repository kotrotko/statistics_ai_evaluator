"""
cw13_5.py
Classwork 13: Linear Regression
APA-style results description and research question answer
Evaluation method name: def grade_question_cw13_5_answer
"""

import re
from config import BaseEvaluator


class CW13_5Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 13_5.

    Task: Describe your results in APA style, using as template the text on video,
    but include only results you got yourself (10 points).
    Please keep in mind that your assignment is different from the description presented
    in the video: it is shortened.
    Answer the main research question (10 points).
    Total (strictly) 20 points.
    """

    def __init__(self):
        super().__init__()

    def check_required_elements(self, student_answer: str) -> dict:
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "apa_format": False,
            "results_content": False,
            "research_question_answer": False,
            "alignment": False,
        }

        evidence = []

        # Task description (pedagogical anchors that students would NOT naturally write)
        pedagogical_markers = [
            "include only results you got yourself",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # APA format indicators
        apa_indicators = [
            r'b\s*=',
            r'β\s*=',
            r'r\s*²|r2|r\^2',
            r'f\s*\(',
            r't\s*\(',
            r'p\s*[<>=]\s*\.\d+',
            r'p\s*[<>=]\s*0\.\d+',
            r'\d+\s*%.*variance',
            r'95\s*%',
            r'ci',
        ]
        if any(re.search(pattern, text_lower) for pattern in apa_indicators):
            elements_found["apa_format"] = True
            evidence.append("APA format indicators found")
        else:
            evidence.append("APA format indicators NOT found")

        # Results content (actual regression values reported)
        results_indicators = [
            "regression",
            "coefficient",
            "intercept",
            "slope",
            "significant",
            "not significant",
            "predict",
            "explained",
            "variance",
            "linear",
            r"r\s*²",
            r"b\s*=",
        ]
        if any(re.search(pattern, text_lower) if pattern.startswith('r') or '\\' in pattern
               else pattern in text_lower
               for pattern in results_indicators):
            elements_found["results_content"] = True
            evidence.append("Results content found")
        else:
            evidence.append("Results content NOT found")

        # Research question answer
        rq_indicators = [
            "research question",
            "main question",
            "therefore",
            "thus",
            "in conclusion",
            "to answer",
            "the results show",
            "found that",
            "significant linear",
            "no significant",
            "reject",
            "fail to reject",
            "supports",
            "does not support",
        ]
        if any(indicator in text_lower for indicator in rq_indicators):
            elements_found["research_question_answer"] = True
            evidence.append("Research question answer found")
        else:
            evidence.append("Research question answer NOT found")

        # Alignment — results and RQ answer are consistent with each other
        alignment_indicators = [
            "based on",
            "consistent with",
            "aligned with",
            "as shown",
            "as indicated",
            "these results",
            "this suggests",
            "therefore",
            "thus",
            "accordingly",
        ]
        if any(indicator in text_lower for indicator in alignment_indicators):
            elements_found["alignment"] = True
            evidence.append("Alignment indicators found")
        else:
            evidence.append("Alignment indicators NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def grade_question_cw13_5_answer(self, student_answer: str, test_mode: bool = False):

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
                feedback="[TEST MODE] APA-style results present with correct values. Research question answered clearly.",
                vibe="Well-structured regression summary with proper APA reporting",
            )

        prompt = f"""You are grading a statistics assignment using a STRICT rubric.

TASK:
Students must complete 5 components: task description, APA-style formatting,
results content, research question answer, and alignment between results and conclusion.

IMPORTANT GRADING RULES:
1. Total score MUST be exactly 20 points
2. Focus on conceptual understanding and correct APA reporting
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

RUBRIC:

Component 1: Task Description (1 point)
DO NOT SCORE — handled externally. Leave component_1_score as 0.

Component 2: APA Style and Format (4 points)
Student must report results using APA style as modelled in the video, adapted for their
own (shortened) assignment. APA regression reporting includes: F-statistic with df,
p-value, R², unstandardized coefficient B, and where applicable, t-value.

- 4 points: Results reported in correct APA format with at least three of the following:
  F(df1, df2) = value, p = value, R² = value, B = value, t(df) = value
- 3 points: APA format attempted with two elements correct; minor deviations acceptable
- 2 points: Some APA elements present but format substantially incomplete or incorrect
- 1 point: Minimal APA attempt — only one element or values without proper notation
- 0 points: No APA formatting present

CRITICAL: Student must use their own results, not values from the video example.
CRITICAL: Notation must follow APA style (e.g., F(1, 48) = 12.34, p = .003, R² = .20).

Component 3: Results Content Accuracy (5 points)
Student must describe the actual regression results they obtained, including the direction
and significance of the effect, and what the model shows about the relationship between
the predictor and criterion variables.

- 5 points: Results clearly described with correct values; direction (positive/negative),
  significance decision (p < or > .05), and R² or variance explained all addressed
- 4 points: Results correct but one element (direction, significance, or R²) missing
- 3 points: Results partially described — correct values present but interpretation is vague
- 2 points: Some results reported but key elements missing or unclear
- 1 point: Minimal results content — only one value mentioned without context
- 0 points: No results content

CRITICAL: Student must report their own values, not copy from the video template.
CRITICAL: Values must be consistent with a linear regression output (not correlation output).

Component 4: Answer to Main Research Question (5 points)
Student must provide a clear, direct answer to the main research question formulated
in Task 1, phrased in terms of linear regression and significance.

- 5 points: Research question directly answered with explicit reference to the regression
  result — states whether the predictor significantly predicts the criterion,
  and whether H0 is rejected, in plain language
- 4 points: Answer present and correct but missing explicit connection to H0 or significance
- 3 points: Answer present but vague or only partially addresses the research question
- 2 points: Attempt to answer but confused or inconsistent with reported results
- 1 point: Minimal answer — restates the question without providing a conclusion
- 0 points: No answer to the research question

CRITICAL: Answer must be phrased in terms of linear regression, not correlation.
CRITICAL: Answer must be consistent with the p-value and results reported in Component 3.

Component 5: Alignment Between Results and Conclusion (5 points)
Student must demonstrate that their research question answer is logically consistent
with the results they reported — the conclusion must follow from the data.

- 5 points: Conclusion clearly follows from the reported results; direction, significance,
  and practical meaning are all coherent and mutually consistent
- 4 points: Conclusion mostly consistent but one minor inconsistency present
- 3 points: Conclusion generally consistent but reasoning is not explicitly connected
- 2 points: Partial alignment — conclusion present but not clearly derived from results
- 1 point: Conclusion contradicts or ignores reported results
- 0 points: No conclusion or completely absent

CRITICAL: If p < .05 was reported, the conclusion MUST state rejection of H0.
CRITICAL: If p > .05 was reported, the conclusion MUST state failure to reject H0.

---

STUDENT ANSWER:
{student_answer}

Return JSON in this exact format:
{{
  "component_1_score": 0,
  "component_1_explanation": "Handled externally",
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
}}

SCORING INSTRUCTIONS:
total_points = component_1_score + component_2_score + component_3_score + component_4_score + component_5_score
"""

        element_check = self.check_required_elements(student_answer)

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"element_check": element_check}
        )

        # Enforcement: task description check (plain string matching, overrides LLM)
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
        print("GRADING RESULTS - CLASSWORK 13.5")
        print("APA Results Description and Research Question Answer")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Task Description): {grading.get('component_1_score')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (APA Style and Format): {grading.get('component_2_score')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Results Content Accuracy): {grading.get('component_3_score')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Research Question Answer): {grading.get('component_4_score')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Alignment Between Results and Conclusion): {grading.get('component_5_score')}/5")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points')}/20")
        print(f"PERCENTAGE: {grading.get('percentage')}%")

        print("\nFEEDBACK:")
        print(textwrap.fill(grading.get('feedback', ''), width=60))


if __name__ == "__main__":
    evaluator = CW13_5Evaluator()

    from config import InputHandler
    input_handler = InputHandler()

    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 13.5",
        question_description="APA Results Description and Research Question Answer",
        min_length=10
    )

    if student_answer:
        grading = evaluator.grade_question_cw13_5_answer(student_answer)
        evaluator.print_grading_results(grading)
