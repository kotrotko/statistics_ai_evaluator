"""
cw14_2.py
Classwork 14: Chi Square
Step system: method justification, hypotheses, significance level, and statistical inference
Evaluation method name: def grade_question_cw14_2_answer
"""

import re
from config import BaseEvaluator


class CW14_2Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 14_2.

    Task: Following our Step system, on:
    Step 1. Name the method you choose and justify it based on the data level (5 points).
    Step 2. State the hypotheses in needed form (5 points).
    Step 3. State the significance level α, calculate df, find the critical value. (5 points).
    Step 4. Open the JASP > Frequencies > Contingency Tables tool. Make sure that you have Physical Activity on Rows and Fruit Consumption on Columns. Include the "Contingency Tables" table, number it, make sure that it is introduced, numbered, and named (5 points).
    Total (strictly) 20 points.

    Evaluates student's ability to follow the step system for Chi Square analysis.

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
        first_lines = student_answer[:200]

        elements_found = {
            "paper_title": False,
            "task_description": False,
            "no_autoformatting": True,
            "method_justification": False,
            "hypotheses": False,
            "significance_setup": False,
            "inference": False,
        }

        evidence = []

        # Paper title
        title_patterns = [
            r'^\s*classwork\s*14',
            r'^\s*cw\s*14\b',
            r'^\s*class\s*work\s*(week\s*)?14',
            r'^\s*in.?class\s*14'
        ]

        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["paper_title"] = True
                evidence.append("Title found")
                break

        # Task description (pedagogical markers, plain string matching)
        pedagogical_markers = [
            "name the method you choose and justify it based on the data level",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # No autoformatting
        autoformat_patterns = [
            r'(?m)(?:^\s*\d+[\.\)]\s+\S.*\n){2,}',
            r'^\s*[-•*]\s+\S',
        ]

        for pattern in autoformat_patterns:
            if re.search(pattern, student_answer, re.MULTILINE):
                elements_found["no_autoformatting"] = False
                evidence.append("Autoformatting detected")
                break

        # Method justification (Step 1)
        if re.search(
            r'chi[\s-]?square|chi[\s-]?squared|χ²|categorical|nominal|'
            r'independence|contingency|non[\s-]?parametric',
            text_lower
        ):
            elements_found["method_justification"] = True
            evidence.append("Method justification found")
        else:
            evidence.append("Method justification NOT found")

        # Hypotheses (Step 2)
        if re.search(
            r'h[0o]\s*:|h[1a]\s*:|null\s*hypothesis|alternative\s*hypothesis|'
            r'independent|not\s*independent|associated|no\s*association',
            text_lower
        ):
            elements_found["hypotheses"] = True
            evidence.append("Hypotheses found")
        else:
            evidence.append("Hypotheses NOT found")

        # Significance level, df, critical value (Step 3)
        if re.search(
            r'α|alpha|significance\s*level|df\s*=|\bdf\b|degrees\s*of\s*freedom|'
            r'critical\s*value|χ²\s*crit|chi[\s-]?square\s*critical',
            text_lower
        ):
            elements_found["significance_setup"] = True
            evidence.append("Significance setup found")
        else:
            evidence.append("Significance setup NOT found")

        # Chi Square result and inference (Step 4)
        if re.search(
            r'χ²|chi[\s-]?square\s*=|p\s*[<>=]\s*[0\.]|reject|fail\s*to\s*reject|'
            r'significant|conclude|inference',
            text_lower
        ):
            elements_found["inference"] = True
            evidence.append("Inference found")
        else:
            evidence.append("Inference NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_question_cw14_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 14.2: Chi Square step system.
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
                feedback="[TEST MODE] Strong structured answer with all steps present.",
                vibe="Clear Chi Square step-system reasoning",
            )

        prompt = f"""You are grading a statistics assignment using a STRICT rubric.

TASK:
Students must complete 5 components following the Step system for Chi Square analysis.

IMPORTANT GRADING RULES:
1. Total score MUST be exactly 20 points
2. Focus on conceptual understanding over formatting
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

RUBRIC:

Component 1: Task Description (1 point)
DO NOT SCORE — handled externally. Leave component_1_score as 0.

Component 2: Step 1 — Method Choice and Justification (4 points)
Student must name Chi Square test of independence and justify why it is appropriate
based on the level of measurement of the variables (both categorical/nominal).

- 4 points: Method named correctly (Chi Square test of independence) and justification
  explicitly references the categorical/nominal nature of both variables
- 3 points: Method named correctly but justification vague or only partially connected
  to data level
- 2 points: Method named but justification is minimal or generic
- 1 point: Method mentioned without any justification
- 0 points: Completely absent

CRITICAL: Justification must reference data level (categorical/nominal), not just say
"Chi Square is appropriate."

Component 3: Step 2 — State the Hypotheses (5 points)
Student must state both H0 and H1 in correct form for Chi Square test of independence.

- 5 points: Both hypotheses stated correctly in proper form
  H0: The two variables are independent (no association)
  H1: The two variables are not independent (there is an association)
- 4 points: Both present but one is imprecise or uses informal language
- 3 points: Both present but incorrectly formulated or missing variable names
- 2 points: Only one hypothesis stated
- 1 point: Hypotheses attempted but substantially wrong or incomplete
- 0 points: Completely absent

Accept symbolic or verbal forms. Variables must be identifiable (physical activity,
fruit consumption, or equivalent).

Component 4: Step 3 — Significance Level, df, Critical Value (5 points)
Student must state α, calculate df correctly, and identify the critical value.

- 5 points: All three elements present and correct
  α = 0.05, df = (R-1)(C-1), critical value from Chi Square table
- 4 points: All three present but one contains a minor error
- 3 points: Two of the three elements present and correct
- 2 points: Only one element present, or all three with significant errors
- 1 point: Minimal attempt
- 0 points: Completely absent

CRITICAL: df for Chi Square = (rows - 1)(columns - 1). For a 3×3 table: df = 4.
Accept any correct critical value corresponding to the stated df and α.

Component 5: Step 4 — Contingency Table (5 points)
Student must include the Contingency Tables output from JASP, properly introduced, numbered, and named,
with Physical Activity on Rows and Fruit Consumption on Columns.

- 5 points: Table present, introduced in text, numbered, and titled with both variable names;
  Physical Activity on rows and Fruit Consumption on columns
- 4 points: Table present and introduced but title missing one variable name, or row/column
  assignment not explicitly stated
- 3 points: Table present and numbered but not introduced or not named
- 2 points: Table present but missing number, title, and introduction
- 1 point: Minimal attempt — reference to contingency table without actual table
- 0 points: Completely absent

CRITICAL: Table must be introduced with a sentence before it appears.
CRITICAL: Table must have a number label and a descriptive title naming both variables.
CRITICAL: Do NOT accept a chi-square test table as a substitute for the contingency table.
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
  "component_5_explanation": "<brief explanation for contingency table>",
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

        # Enforcement: task description (plain string matching, overrides LLM)
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
        """Display grading results."""
        import textwrap

        print("=" * 60)
        print("GRADING RESULTS - CLASSWORK 14.2")
        print("Chi Square — Step System")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Task Description): {grading.get('component_1_score')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Step 1: Method Choice & Justification): {grading.get('component_2_score')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Step 2: Hypotheses): {grading.get('component_3_score')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Step 3: α, df, Critical Value): {grading.get('component_4_score')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Step 4: Contingency Table): {grading.get('component_5_score')}/5")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points')}/20")
        print(f"PERCENTAGE: {grading.get('percentage')}%")

        print("\nFEEDBACK:")
        print(textwrap.fill(grading.get('feedback', ''), width=60))


if __name__ == "__main__":
    evaluator = CW14_2Evaluator()

    from config import InputHandler
    input_handler = InputHandler()

    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 14.2",
        question_description="Chi Square — Step System",
        min_length=10
    )

    if student_answer:
        grading = evaluator.grade_question_cw14_2_answer(student_answer)
        evaluator.print_grading_results(grading)
