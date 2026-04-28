"""
cw15_4.py
Classwork 15: Exploratory Factor Analysis
Plots — Path Diagram and Scree Plot
Evaluation method name: def grade_question_cw15_4_answer
"""
import re
import textwrap

from config import BaseEvaluator


class CW15_4Evaluator(BaseEvaluator):
    """
    Evaluator for Class Work 15 Task 4.

    Task: Plots. In this section, please ensure you include the Path diagram
          as Figure 1: it should show how observed variables load on factors
          (5 points for diagram and 5 points for explanation). Additionally,
          you should include the Scree plot as Figure 2: this is used to choose
          the appropriate number of factors by identifying the elbow point
          (5 points for diagram and 5 points for explanation).

    Rubric:
    Component 1: Path diagram       (5 points)
    Component 2: Path explanation   (5 points)
    Component 3: Scree plot         (5 points)
    Component 4: Scree explanation  (5 points)
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

        elements_found = {
            "task_description": False,
            "figure_1_label": False,
            "figure_1_explanation": False,
            "figure_2_label": False,
            "figure_2_explanation": False,
        }

        evidence = []

        # ------------------------------------------------------------------
        # Task description (pedagogical marker)
        # True when the student copy-pasted the task wording into their answer.
        # The marker is the teacher's instruction phrase unique to this task.
        # ------------------------------------------------------------------
        pedagogical_markers = [
            "please ensure you",
        ]
        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # ------------------------------------------------------------------
        # Figure 1 label — "Figure 1. Path Diagram" (or similar) present
        # ------------------------------------------------------------------
        figure_1_label_pattern = re.compile(
            r'figure\s+1[\.\s]',
            re.IGNORECASE,
        )
        elements_found["figure_1_label"] = bool(
            figure_1_label_pattern.search(student_answer)
        )
        evidence.append(
            "Figure 1 label found" if elements_found["figure_1_label"]
            else "Figure 1 label NOT found"
        )

        # ------------------------------------------------------------------
        # Figure 1 explanation — text discussing path diagram content
        # (factor loadings, observed variables loading on factors)
        # Must be a sentence of substance, not just the label line itself.
        # ------------------------------------------------------------------
        figure_1_explanation_pattern = re.compile(
            r'(?:path\s+diagram|factor\s+load|observed\s+variable|load\s+on\s+factor)',
            re.IGNORECASE,
        )
        # Require a match that is NOT on the same short label line as "Figure 1."
        # We check that there is explanatory prose beyond the bare label.
        fig1_matches = list(figure_1_explanation_pattern.finditer(student_answer))
        if fig1_matches:
            # At least one match must appear in a line longer than a bare label
            for m in fig1_matches:
                line_start = student_answer.rfind('\n', 0, m.start()) + 1
                line_end = student_answer.find('\n', m.end())
                if line_end == -1:
                    line_end = len(student_answer)
                line_text = student_answer[line_start:line_end].strip()
                # A label line is short; explanation prose is longer
                if len(line_text) > 40:
                    elements_found["figure_1_explanation"] = True
                    break
        evidence.append(
            "Figure 1 explanation found" if elements_found["figure_1_explanation"]
            else "Figure 1 explanation NOT found"
        )

        # ------------------------------------------------------------------
        # Figure 2 label — "Figure 2. Scree plot" (or similar) present
        # ------------------------------------------------------------------
        figure_2_label_pattern = re.compile(
            r'figure\s+2[\.\s]',
            re.IGNORECASE,
        )
        elements_found["figure_2_label"] = bool(
            figure_2_label_pattern.search(student_answer)
        )
        evidence.append(
            "Figure 2 label found" if elements_found["figure_2_label"]
            else "Figure 2 label NOT found"
        )

        # ------------------------------------------------------------------
        # Figure 2 explanation — text discussing scree plot content
        # (eigenvalues, elbow point, number of factors)
        # ------------------------------------------------------------------
        figure_2_explanation_pattern = re.compile(
            r'(?:scree\s+plot|eigenvalue|elbow\s+point|number\s+of\s+factor|elbow)',
            re.IGNORECASE,
        )
        fig2_matches = list(figure_2_explanation_pattern.finditer(student_answer))
        if fig2_matches:
            for m in fig2_matches:
                line_start = student_answer.rfind('\n', 0, m.start()) + 1
                line_end = student_answer.find('\n', m.end())
                if line_end == -1:
                    line_end = len(student_answer)
                line_text = student_answer[line_start:line_end].strip()
                if len(line_text) > 40:
                    elements_found["figure_2_explanation"] = True
                    break
        evidence.append(
            "Figure 2 explanation found" if elements_found["figure_2_explanation"]
            else "Figure 2 explanation NOT found"
        )

        return {
            "elements_found": elements_found,
            "evidence": evidence,
        }

    def grade_question_cw15_4_answer(self, student_answer: str, test_mode: bool = False):
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 5,
                    "component_2_score": 5,
                    "component_3_score": 5,
                    "component_4_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Complete answer with both figures and explanations.",
                vibe="Student correctly included and explained both the path diagram and scree plot."
            )

        formatting_check = self.check_formatting_elements(student_answer)
        fs = formatting_check["elements_found"]

        formatting_block = f"""
HEADER DETECTION RESULTS (USE AS FACTS):

task_description_present    = {fs["task_description"]}
figure_1_label_present      = {fs["figure_1_label"]}
figure_1_explanation_present = {fs["figure_1_explanation"]}
figure_2_label_present      = {fs["figure_2_label"]}
figure_2_explanation_present = {fs["figure_2_explanation"]}
"""

        prompt = f"""{formatting_block}

You are grading a statistics assignment.

TASK:
"In this section, please ensure you include the Path diagram as Figure 1: \
it should show how observed variables load on factors (5 points for diagram \
and 5 points for explanation). Additionally, you should include the Scree plot \
as Figure 2: this is used to choose the appropriate number of factors by \
identifying the elbow point (5 points for diagram and 5 points for explanation)."

Use STRICT rubric-based grading. Total score MUST be exactly 20 points.

RUBRIC

Component 1: Path diagram (5 points)
Use figure_1_label_present.
Award 5 points if True (Figure 1 label present, path diagram included).
Award 0 points if False.

Component 2: Path diagram explanation (5 points)
Use figure_1_explanation_present as a signal, but read the student answer directly.
Award 5 points for a complete explanation of what the path diagram shows:
  how observed variables load on factors, which variables belong to which factor,
  the direction and strength of loadings.
Award 0–4 for partial or vague explanation.

Component 3: Scree plot (5 points)
Use figure_2_label_present.
Award 5 points if True (Figure 2 label present, scree plot included).
Award 0 points if False.

Component 4: Scree plot explanation (5 points)
Use figure_2_explanation_present as a signal, but read the student answer directly.
Award 5 points for a complete explanation of what the scree plot shows:
  eigenvalues plotted against factor number, identification of the elbow point,
  justification for the chosen number of factors.
Award 0–4 for partial or vague explanation.

SCORING INSTRUCTIONS:
total_points = component_1_score + component_2_score + component_3_score + component_4_score

ORIGINALITY CHECK:
If copied/AI-generated with suspiciously generic style, set all scores to 0 and set feedback to EXACTLY:
"Due to originality concern, your points are frozen. You can get them back if you provide oral explanation for this paper."

STUDENT ANSWER:
{student_answer}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-5>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <number>,
  "feedback": "<short teacher comment>",
  "vibe": "<one sentence overall impression>"
}}"""

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
                "component_4_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        print("=" * 60)
        print("GRADING RESULTS - CW15_4")
        print("Plots: Path Diagram and Scree Plot")
        print("=" * 60)

        if grading.get("originality_concern"):
            print("\n⚠️  ORIGINALITY CONCERN DETECTED")
            print("   All points frozen. See feedback below.")

        print("\nCOMPONENT BREAKDOWN:")
        print(f"\nPath diagram: {grading.get('component_1_score')}/5")
        if grading.get("component_1_explanation"):
            print(f"   → {grading.get('component_1_explanation')}")

        print(f"\nPath explanation: {grading.get('component_2_score')}/5")
        if grading.get("component_2_explanation"):
            print(f"   → {grading.get('component_2_explanation')}")

        print(f"\nScree plot: {grading.get('component_3_score')}/5")
        if grading.get("component_3_explanation"):
            print(f"   → {grading.get('component_3_explanation')}")

        print(f"\nScree explanation: {grading.get('component_4_score')}/5")
        if grading.get("component_4_explanation"):
            print(f"   → {grading.get('component_4_explanation')}")

        print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points')}/{grading.get('max_points', 20)}")
        print(f"PERCENTAGE: {grading.get('percentage')}%")

        print("\n" + "=" * 60)
        print("FEEDBACK:")
        print("=" * 60)
        print(textwrap.fill(grading.get("feedback", ""), width=60))

        print("\n" + "=" * 60)
        print("THE VIBE:")
        print("=" * 60)
        print(textwrap.fill(grading.get("vibe", ""), width=60))

        if "error" in grading:
            print("\n" + "=" * 60)
            print("ERROR:")
            print("=" * 60)
            print(grading.get("error"))


if __name__ == "__main__":
    print("Welcome to the Homework AI Evaluator System!")
    print("=" * 60)

    evaluator = CW15_4Evaluator()

    print("=" * 60)
    print("CLASS WORK 15.4 EVALUATOR")
    print("Plots: Path Diagram and Scree Plot")
    print("=" * 60)
    print("\nPlease enter the student's answer to CW15_4.")
    print("(Press Enter twice when finished, or type 'END' on a new line)\n")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
        if len(lines) >= 2 and lines[-1] == "" and lines[-2] == "":
            lines = lines[:-2]
            break

    student_answer = "\n".join(lines)

    if not student_answer.strip():
        print("\n❌ Error: No answer provided. Exiting.")
        exit(1)

    print("\n" + "=" * 60)
    print("EVALUATING...")
    print("=" * 60)

    grading = evaluator.grade_question_cw15_4_answer(student_answer)

    evaluator.print_grading_results(grading)