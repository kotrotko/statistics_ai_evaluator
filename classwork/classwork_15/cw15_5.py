"""
cw15_5.py
Classwork 15: Exploratory Factor Analysis
Report — Data & Method, Factor Extraction, Rotation, Interpretation
Evaluation method name: def grade_question_cw15_5_answer
"""
import re
import textwrap

from config import BaseEvaluator


class CW15_5Evaluator(BaseEvaluator):
    """
    Evaluator for Class Work 15 Task 5.

    Task: Include the following elements in your report:
          Description of the data and method (5 points).
          Please make sure that you included the Factor extraction results (5 points).
          Which Rotation method did you use? (5 points).
          Write the Interpretation of the factor loading (5 points).

    Rubric:
    Component 1: Data & method description  (5 points)
    Component 2: Factor extraction results  (5 points)
    Component 3: Rotation method            (5 points)
    Component 4: Interpretation             (5 points)
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
            "data_method": False,
            "factor_extraction": False,
            "rotation_method": False,
            "interpretation": False,
        }

        evidence = []

        # ------------------------------------------------------------------
        # Task description (pedagogical marker)
        # True when the student copy-pasted the task wording into their answer.
        # ------------------------------------------------------------------
        pedagogical_markers = [
            "please make sure that you",
        ]
        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # ------------------------------------------------------------------
        # Data & method description
        # Requires substantive prose — not just a keyword on a short line.
        # Keywords: data, participants/sample, method, exploratory factor analysis, EFA.
        # ------------------------------------------------------------------
        data_method_pattern = re.compile(
            r'(?:exploratory\s+factor\s+analysis|principal\s+axis|maximum\s+likelihood'
            r'|the\s+data\s+consist|sample\s+of|participants|variables\s+were'
            r'|\befa\b)',
            re.IGNORECASE,
        )
        for m in data_method_pattern.finditer(student_answer):
            line = _get_line(student_answer, m)
            if len(line) > 40:
                elements_found["data_method"] = True
                break
        evidence.append(
            "Data & method description found" if elements_found["data_method"]
            else "Data & method description NOT found"
        )

        # ------------------------------------------------------------------
        # Factor extraction results
        # Keywords: factor extraction, eigenvalue, retained, variance explained.
        # Bare label "Factor extraction results." (≤40 chars) does NOT qualify.
        # ------------------------------------------------------------------
        factor_extraction_pattern = re.compile(
            r'(?:factor\s+extraction|eigenvalue|retained|variance\s+explained'
            r'|number\s+of\s+factor|scree\s+plot|kaiser)',
            re.IGNORECASE,
        )
        for m in factor_extraction_pattern.finditer(student_answer):
            line = _get_line(student_answer, m)
            if len(line) > 40:
                elements_found["factor_extraction"] = True
                break
        evidence.append(
            "Factor extraction results found" if elements_found["factor_extraction"]
            else "Factor extraction results NOT found"
        )

        # ------------------------------------------------------------------
        # Rotation method
        # Keywords: rotation, promax, varimax, oblique, orthogonal.
        # ------------------------------------------------------------------
        rotation_pattern = re.compile(
            r'(?:promax|varimax|oblimin|oblique|orthogonal'
            r'|rotation\s+method|rotated)',
            re.IGNORECASE,
        )
        for m in rotation_pattern.finditer(student_answer):
            line = _get_line(student_answer, m)
            if len(line) > 40:
                elements_found["rotation_method"] = True
                break
        evidence.append(
            "Rotation method found" if elements_found["rotation_method"]
            else "Rotation method NOT found"
        )

        # ------------------------------------------------------------------
        # Interpretation of factor loadings
        # Keywords: factor loading, factor 1/2/3, defined by, loads on.
        # ------------------------------------------------------------------
        interpretation_pattern = re.compile(
            r'(?:factor\s+loading|factor\s+[123]|defined\s+by|loads?\s+on'
            r'|interpretation|strong\s+load)',
            re.IGNORECASE,
        )
        for m in interpretation_pattern.finditer(student_answer):
            line = _get_line(student_answer, m)
            if len(line) > 40:
                elements_found["interpretation"] = True
                break
        evidence.append(
            "Interpretation found" if elements_found["interpretation"]
            else "Interpretation NOT found"
        )

        return {
            "elements_found": elements_found,
            "evidence": evidence,
        }

    def grade_question_cw15_5_answer(self, student_answer: str, test_mode: bool = False):
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 5,
                    "component_2_score": 5,
                    "component_3_score": 5,
                    "component_4_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Complete report with all four sections present.",
                vibe="Student produced a well-structured EFA report covering all required elements."
            )

        formatting_check = self.check_formatting_elements(student_answer)
        fs = formatting_check["elements_found"]

        formatting_block = f"""
HEADER DETECTION RESULTS (USE AS FACTS):

task_description_present   = {fs["task_description"]}
data_method_present        = {fs["data_method"]}
factor_extraction_present  = {fs["factor_extraction"]}
rotation_method_present    = {fs["rotation_method"]}
interpretation_present     = {fs["interpretation"]}
"""

        prompt = f"""{formatting_block}

You are grading a statistics assignment.

TASK:
"Include the following elements in your report: Description of the data and \
method (5 points). Please make sure that you included the Factor extraction \
results (5 points). Which Rotation method did you use? (5 points). Write the \
Interpretation of the factor loading (5 points)."

Use STRICT rubric-based grading. Total score MUST be exactly 20 points.

RUBRIC

Component 1: Description of data and method (5 points)
Use data_method_present as a signal, but read the student answer directly.
Award 5 points for a complete description covering:
  - the dataset (variables, sample size or participants)
  - the analysis method (e.g. exploratory factor analysis, principal axis factoring)
Award 0–4 for partial description (e.g. method named but no data context, or vice versa).
Award 0 if data_method_present is False.

Component 2: Factor extraction results (5 points)
Use factor_extraction_present as a signal, but read the student answer directly.
Award 5 points for a complete account covering:
  - number of factors retained
  - criterion used (eigenvalue > 1, scree plot, variance explained)
  - variance explained by each factor or total
Award 0–4 for partial results.
Award 0 if factor_extraction_present is False.

Component 3: Rotation method (5 points)
Use rotation_method_present as a signal, but read the student answer directly.
Award 5 points for naming the rotation method AND explaining why it was chosen
  (e.g. promax/oblique because factors are expected to correlate;
   varimax/orthogonal because factors are assumed independent).
Award 2–4 for naming the method without justification.
Award 0 if rotation_method_present is False.

Component 4: Interpretation of factor loadings (5 points)
Use interpretation_present as a signal, but read the student answer directly.
Award 5 points for a complete interpretation covering:
  - which variables load on which factor
  - loading values or strength (above .40 threshold)
  - what each factor represents substantively
Award 0–4 for partial or vague interpretation.
Award 0 if interpretation_present is False.

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
        print("GRADING RESULTS - CW15_5")
        print("Report: Data & Method, Extraction, Rotation, Interpretation")
        print("=" * 60)

        if grading.get("originality_concern"):
            print("\n⚠️  ORIGINALITY CONCERN DETECTED")
            print("   All points frozen. See feedback below.")

        print("\nCOMPONENT BREAKDOWN:")

        print(f"\nData & method: {grading.get('component_1_score')}/5")
        if grading.get("component_1_explanation"):
            print(f"   → {grading.get('component_1_explanation')}")

        print(f"\nFactor extraction: {grading.get('component_2_score')}/5")
        if grading.get("component_2_explanation"):
            print(f"   → {grading.get('component_2_explanation')}")

        print(f"\nRotation method: {grading.get('component_3_score')}/5")
        if grading.get("component_3_explanation"):
            print(f"   → {grading.get('component_3_explanation')}")

        print(f"\nInterpretation: {grading.get('component_4_score')}/5")
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


# ---------------------------------------------------------------------------
# Module-level helper — extract the full line containing a regex match
# ---------------------------------------------------------------------------

def _get_line(text: str, match: re.Match) -> str:
    line_start = text.rfind('\n', 0, match.start()) + 1
    line_end = text.find('\n', match.end())
    if line_end == -1:
        line_end = len(text)
    return text[line_start:line_end].strip()


if __name__ == "__main__":
    print("Welcome to the Homework AI Evaluator System!")
    print("=" * 60)

    evaluator = CW15_5Evaluator()

    print("=" * 60)
    print("CLASS WORK 15.5 EVALUATOR")
    print("Report: Data & Method, Extraction, Rotation, Interpretation")
    print("=" * 60)
    print("\nPlease enter the student's answer to CW15_5.")
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

    grading = evaluator.grade_question_cw15_5_answer(student_answer)

    evaluator.print_grading_results(grading)