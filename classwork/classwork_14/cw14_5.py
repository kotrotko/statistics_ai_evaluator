"""
cw14_5.py
Classwork 14: Chi-Square Test of Independence
Output description (APA), research question answer, and causation conclusion
Evaluation method name: def grade_question_cw14_5_answer
"""

import re
from config import BaseEvaluator


class CW14_5Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 14_5.

    Task: Describe your output briefly. Follow the APA style you learned before. (5 points).
    Answer the main research question: Are physical activity and fruit consumption independent? (10 points).
    What do you think about causation? (5 points).
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
            "apa_output": False,
        }

        evidence = []

        # Task description — strongest pedagogical marker:
        # a student cannot say "you" about themselves
        pedagogical_markers = [
            "what do you think about causation",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # APA-style output description: must contain chi-square symbol (or χ2/x2),
        # degrees of freedom, N, and p-value together
        has_chi = bool(re.search(r'χ|chi.square|χ2|x2\(', text_lower))
        has_df = bool(re.search(r'\(\d+[,\s]', student_answer))
        has_n = bool(re.search(r'n\s*=\s*\d+', text_lower))
        has_p = bool(re.search(r'p\s*[=<>]\s*[.\d]+', text_lower))

        if has_chi and has_df and has_n and has_p:
            elements_found["apa_output"] = True
            evidence.append("APA output found")
        else:
            evidence.append("APA output NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def grade_question_cw14_5_answer(self, student_answer: str, test_mode: bool = False):

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 1,
                    "component_2_score": 1,
                    "component_3_score": 3,
                    "component_4_score": 10,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] APA output present. Research question answered. Causation addressed.",
                vibe="Clear APA reporting with well-reasoned research question and causation conclusion",
            )

        prompt = f"""You are grading a statistics assignment using a STRICT rubric.

TASK:
Students must complete 4 components summarizing chi-square test results in APA style,
answering the main research question, and reflecting on causation.

IMPORTANT GRADING RULES:
1. Total score MUST be exactly 20 points
2. Focus on conceptual understanding over formatting
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

RUBRIC:

Component 1: Task Description (1 point)
DO NOT SCORE — handled externally. Leave component_1_score as 0.

Component 2: Autoformatting (1 point)
Student must demonstrate correct academic document formatting.

- 1 point: Response is written in complete sentences and structured paragraphs
- 0 points: Unstructured, bullet-point only, or raw JASP output without written framing

Component 3: APA-Style Output Description (3 points)
Student must describe the chi-square result in APA format.

- 3 points: Full APA notation present: χ²(df, N = n) = value, p = .xxx; result described in a sentence naming both variables
- 2 points: APA notation present but one element missing (df, N, or p-value); or notation correct but no descriptive sentence
- 1 point: Some APA elements present (e.g. chi-square value and p) but notation incomplete or malformed
- 0 points: No APA notation at all

CRITICAL: Accept χ², X², or "chi-square" as the statistic label.
CRITICAL: Both variables must be named in the descriptive sentence (not just "the variables").

Component 4: Answer to the Main Research Question (10 points)
Student must answer: Are physical activity and fruit consumption independent?

- 10 points: Clear yes/no answer with ALL of the following:
  (a) explicit reference to the chi-square result (significance);
  (b) correct conclusion about independence/non-independence;
  (c) description of what the relationship means in practical terms for the specific variables;
  (d) acknowledgment that the association exists but is not strong
- 8 points: All elements present but one is underdeveloped
- 6 points: Correct conclusion with significance referenced, but practical meaning or strength missing
- 4 points: Correct conclusion stated but reasoning is vague or missing key elements
- 2 points: Answer present but confused (e.g., confuses independence with causation, or misreads significance)
- 0 points: Completely absent

CRITICAL: Student must explicitly use the word "independent" or "not independent" (or equivalent).
CRITICAL: Student must connect the answer to the specific variables (physical activity and fruit consumption).

Component 5: Conclusion on Causation (5 points)
Student must state whether causation can be concluded from a chi-square test and explain why.

- 5 points: Correctly states causation CANNOT be concluded; explains that chi-square identifies association only,
  not cause-and-effect; acknowledges that other factors may influence both variables
- 4 points: Correct conclusion with explanation but one element missing (e.g., no mention of confounding factors)
- 3 points: Correct conclusion stated with partial reasoning
- 2 points: Correct conclusion stated without any reasoning
- 1 point: Causation mentioned but answer is confused or contradictory
- 0 points: Completely absent

CRITICAL: Student must explicitly state that causation cannot be concluded from this test.
CRITICAL: Reasoning must be grounded in the nature of chi-square, not general knowledge only.

---

STUDENT ANSWER:
{student_answer}

Return JSON in this exact format:
{{
  "component_1_score": 0,
  "component_1_explanation": "Handled externally",
  "component_2_score": <0-1>,
  "component_2_explanation": "<brief explanation>",
  "component_3_score": <0-3>,
  "component_3_explanation": "<brief explanation>",
  "component_4_score": <0-10>,
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
        print("GRADING RESULTS - CLASSWORK 14.5")
        print("APA Output, Research Question, and Causation")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Task Description): {grading.get('component_1_score')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Autoformatting): {grading.get('component_2_score')}/1")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (APA-Style Output Description): {grading.get('component_3_score')}/3")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Answer to Research Question): {grading.get('component_4_score')}/10")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Conclusion on Causation): {grading.get('component_5_score')}/5")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points')}/20")
        print(f"PERCENTAGE: {grading.get('percentage')}%")

        print("\nFEEDBACK:")
        print(textwrap.fill(grading.get('feedback', ''), width=60))


if __name__ == "__main__":
    evaluator = CW14_5Evaluator()

    from config import InputHandler
    input_handler = InputHandler()

    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 14.5",
        question_description="APA Output, Research Question, and Causation",
        min_length=10
    )

    if student_answer:
        grading = evaluator.grade_question_cw14_5_answer(student_answer)
        evaluator.print_grading_results(grading)