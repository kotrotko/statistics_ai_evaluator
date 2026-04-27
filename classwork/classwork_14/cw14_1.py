"""
cw14_1.py
Classwork 14: Chi Square
Evaluation method name: def grade_question_cw14_1_answer
"""

import re
import textwrap
from config import BaseEvaluator


class CW14_1Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 14_1.

    Task: State the problem with your own words (10 points)
    and formulate Research question (10 points).
    Total (strictly) 20 points.

    Rubric:
    Formatting (4 points: name, title, task description, no autoformatting)
    Problem Statement (8 points)
    Research Question (8 points)
    Total (strictly) 20 points.
    """

    def __init__(self):
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1200
        )

    def check_formatting_elements(self, student_answer: str) -> dict:
        text_lower = student_answer.lower()
        first_lines = student_answer[:200]

        elements_found = {
            "paper_title": False,
            "task_description": False,
            "no_autoformatting": True,
        }

        evidence = []

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

        pedagogical_markers = [
            "state the problem with your own words (10 points) and formulate research question",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        autoformat_patterns = [
            r'(?m)(?:^\s*\d+[\.\)]\s+\S.*\n){2,}',
            r'^\s*[-•*]\s+\S',
        ]

        for pattern in autoformat_patterns:
            if re.search(pattern, student_answer, re.MULTILINE):
                elements_found["no_autoformatting"] = False
                evidence.append("Autoformatting detected")
                break

        if elements_found["no_autoformatting"]:
            evidence.append("No autoformatting found")

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def grade_question_cw14_1_answer(self, student_answer: str, test_mode: bool = False):

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 4,
                    "component_1_name_score": 1,
                    "component_1_title_score": 1,
                    "component_1_task_score": 1,
                    "component_1_autoformat_score": 1,
                    "component_2_score": 8,
                    "component_3_score": 8,
                },
                max_points=20,
                feedback="[TEST MODE] Complete and accurate answer.",
                vibe="Student demonstrates clear understanding of Chi Square problem formulation."
            )

        formatting_check = self.check_formatting_elements(student_answer)
        fs = formatting_check["elements_found"]

        formatting_block = f"""
HEADER DETECTION RESULTS (USE AS FACTS):

paper_title_present = {fs["paper_title"]}
task_description_present = {fs["task_description"]}
no_autoformatting_present = {fs["no_autoformatting"]}
"""

        prompt = f"""{formatting_block}

You are grading a statistics classwork assignment.

TASK:
"State the problem with your own words (10 points) and formulate Research question (10 points)."

Use STRICT rubric-based grading. Total score MUST be exactly 20 points.

RUBRIC

Component 1: Formatting (4 points)
Start with 4 points.

Step 1 Name (1 point)
- Valid name = two capitalized words like John Doe
- Must appear in first two lines before content

Step 2 Title (1 point)
Use paper_title_present

Step 3 Task description (1 point)
Use task_description_present

Step 4 No autoformatting (1 point)
Use no_autoformatting_present

Component 2: Problem Statement (8 points)
Student must describe the research problem in their own words, connected to the context
of Chi Square analysis. The problem should reference the variables under investigation
(e.g. physical activity and fruit consumption) and the nature of the question
(association between categorical variables).

- 8 points: Clear, specific, well-articulated problem in own words, connected to Chi Square context
- 6 points: Good statement with minor clarity issues or missing variable context
- 4 points: Problem present but vague or lacks connection to the variables or method
- 2 points: Problem poorly articulated but shows some understanding
- 1 point: Attempted but unclear or off-topic
- 0 points: Completely blank

CRITICAL: Do NOT accept a problem statement that is a restatement of the research question.
CRITICAL: Do NOT accept AI-generated boilerplate without any connection to the specific variables.

Component 3: Research Question (8 points)
Student must formulate a clear, testable Research Question appropriate for Chi Square
analysis — asking whether there is a significant association between two categorical variables.

- 8 points: Clear, testable question directly addressing the association between
  the two categorical variables (e.g. physical activity and fruit consumption)
- 6 points: Good question with minor precision issues or missing variable specificity
- 4 points: Question present but vague or only partially addresses the association
- 2 points: Question unclear or poorly formulated
- 1 point: Attempted but not testable or irrelevant to Chi Square
- 0 points: Completely blank

CRITICAL: The question must be phrased in terms of association or independence between
categorical variables, not in terms of prediction or causation.
CRITICAL: Do NOT accept a research question that is simply copied from an AI tool
without adaptation to the student's own understanding.

---

EXAMPLE OF A COMPLETE ANSWER

Problem Statement:
This study examines whether there is an association between levels of physical activity
and fruit consumption among individuals in the Health Habits dataset. Both variables are
categorical, making Chi Square the appropriate test to determine whether the distribution
of fruit consumption differs across physical activity groups.

Research Question:
Is there a statistically significant association between physical activity level
(Low, Moderate, Vigorous) and fruit consumption (Low, Medium, High)?

---

ORIGINALITY CHECK:

IMPORTANT:
Students are required to copy the following task description into their answer.
This exact text is NEVER an originality concern and must be fully excluded before evaluation:

--- TASK DESCRIPTION START ---
State the problem with your own words (10 points) and formulate Research question (10 points).
--- TASK DESCRIPTION END ---

STEP 1: Remove any text matching or paraphrasing the block above.
STEP 2: Evaluate ONLY what remains — the student's own problem statement and research question.
STEP 3: Set originality_concern = true ONLY if the remaining text is AI-generated, generic,
and contains no personal reasoning connected to Chi Square and the specific variables.

Otherwise set originality_concern = false.

DO NOT modify or override component scores based on originality_concern.

STUDENT ANSWER:
{student_answer}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-4>,
  "component_1_name_score": <0-1>,
  "component_1_title_score": <0-1>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief explanation for formatting>",
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief explanation for problem statement>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief explanation for research question>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression>"
}}

SCORING INSTRUCTIONS:

component_1_name_score = 1 if valid name found, else 0
component_1_title_score = 1 if paper_title_present else 0
component_1_task_score = 1 if task_description_present else 0
component_1_autoformat_score = 1 if no_autoformatting_present else 0
component_1_score = component_1_name_score + component_1_title_score + component_1_task_score + component_1_autoformat_score

total_points = component_1_score + component_2_score + component_3_score
"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"formatting_check": formatting_check}
        )

        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results."""
        print("=" * 60)
        print("GRADING RESULTS - CW14_1")
        print("Chi Square - Problem Statement & Research Question")
        print("=" * 60)

        if "component_1_score" in grading:
            if grading.get("originality_concern"):
                print("\n⚠️  ORIGINALITY CONCERN DETECTED")
                print("   All points frozen. See feedback below.")

            print(f"\nFormatting: {grading.get('component_1_score')}/4")
            print(f"  • Student name:      {grading.get('component_1_name_score')}/1 (LLM)")
            print(f"  • Paper title:       {grading.get('component_1_title_score')}/1 (regex)")
            print(f"  • Task description:  {grading.get('component_1_task_score')}/1 (string match)")
            print(f"  • No autoformatting: {grading.get('component_1_autoformat_score')}/1 (regex)")
            if grading.get('component_1_explanation'):
                print(f"   → {grading.get('component_1_explanation')}")

            print(f"\nProblem Statement: {grading.get('component_2_score')}/8")
            if grading.get('component_2_explanation'):
                print(f"  → {grading.get('component_2_explanation')}")

            print(f"Research Question: {grading.get('component_3_score')}/8")
            if grading.get('component_3_explanation'):
                print(f"  → {grading.get('component_3_explanation')}")

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


if __name__ == "__main__":

    evaluator = CW14_1Evaluator()

    print("CLASSWORK 14.1 EVALUATOR")
    print("=" * 60)

    print("Enter student's answer (type END to finish):")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    student_answer = "\n".join(lines)

    grading = evaluator.grade_question_cw14_1_answer(student_answer)

    evaluator.print_grading_results(grading)