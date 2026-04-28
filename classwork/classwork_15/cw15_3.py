"""
cw15_3.py
Classwork 15: Exploratory Factor Analysis
Communalities
Evaluation method name: def grade_question_cw15_3_answer
"""
import re
import textwrap

from config import BaseEvaluator


class CW15_3Evaluator(BaseEvaluator):
    """
    Evaluator for Class Work 15 Task 3.

    Task: Communalities.
    Compute Communality = 1 − Uniqueness for each variable (10 points).
    Identify variable with low communality (< .40): x2 (0.255) (5 points).
    Interpretation: explain poor fit and shared variance (5 points).
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
            "no_autoformatting": True,
            "intro_phrase": False,
            "table_ref_in_intro": False,
            "table_number": False,
            "table_title": False,
            "table_complete": False,
            "low_communality": False,
            "interpretation": False,
        }

        evidence = []

        # ------------------------------------------------------------------
        # Task description (pedagogical marker)
        # True when the student copy-pasted the task wording into their answer.
        # ------------------------------------------------------------------
        pedagogical_markers = [
            "find the uniqueness column",
            "use it to compute",
            "communality = 1",
            "communality=1",
        ]
        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # ------------------------------------------------------------------
        # Autoformatting
        # ------------------------------------------------------------------
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

        # ------------------------------------------------------------------
        # Introductory phrase — sentence like "As shown in Table 5, …"
        # that appears BEFORE the table label line.
        # ------------------------------------------------------------------
        intro_pattern = re.compile(
            r'(?:as\s+shown|presented|summarized|displayed|reported|illustrated)'
            r'.{0,60}table\s+\d+',
            re.IGNORECASE | re.DOTALL,
        )
        table_label_pattern = re.compile(
            r'^\s*table\s+\d+\s*\.',
            re.MULTILINE | re.IGNORECASE,
        )
        intro_match = intro_pattern.search(text_lower)
        table_label_match = table_label_pattern.search(student_answer)

        if intro_match and table_label_match:
            elements_found["intro_phrase"] = intro_match.start() < table_label_match.start()
        else:
            elements_found["intro_phrase"] = bool(intro_match)

        evidence.append(
            "Introductory phrase found" if elements_found["intro_phrase"]
            else "Introductory phrase NOT found"
        )

        # ------------------------------------------------------------------
        # Table number referenced inside the introductory phrase
        # ------------------------------------------------------------------
        if intro_match:
            intro_text = intro_match.group(0)
            elements_found["table_ref_in_intro"] = bool(
                re.search(r'table\s+\d+', intro_text, re.IGNORECASE)
            )
        evidence.append(
            "Table number referenced in intro" if elements_found["table_ref_in_intro"]
            else "Table number NOT referenced in intro"
        )

        # ------------------------------------------------------------------
        # Table number label — "Table N." on its own line
        # ------------------------------------------------------------------
        elements_found["table_number"] = bool(table_label_match)
        evidence.append(
            "Table number label found" if elements_found["table_number"]
            else "Table number label NOT found"
        )

        # ------------------------------------------------------------------
        # Table title — descriptive text follows "Table N."
        # ------------------------------------------------------------------
        table_title_pattern = re.compile(
            r'^\s*table\s+\d+\.\s+\S.+',
            re.MULTILINE | re.IGNORECASE,
        )
        elements_found["table_title"] = bool(table_title_pattern.search(student_answer))
        evidence.append(
            "Table title found" if elements_found["table_title"]
            else "Table title NOT found"
        )

        # ------------------------------------------------------------------
        # Table completeness — all 9 variables present with correct values
        # Communality = round(1 − Uniqueness, 3); tolerance ±0.005
        # ------------------------------------------------------------------
        expected_rows = {
            "x1": (0.523, 0.477),
            "x2": (0.745, 0.255),
            "x3": (0.547, 0.453),
            "x4": (0.272, 0.728),
            "x5": (0.246, 0.754),
            "x6": (0.309, 0.691),
            "x7": (0.481, 0.519),
            "x8": (0.480, 0.520),
            "x9": (0.540, 0.460),
        }
        data_row_re = re.compile(
            r'^\s*(x\d+)\s+([\d.]+)\s+([\d.]+)\s*$',
            re.MULTILINE,
        )
        found_rows = {}
        for m in data_row_re.finditer(student_answer):
            var = m.group(1)
            try:
                found_rows[var] = (float(m.group(2)), float(m.group(3)))
            except ValueError:
                pass

        if set(found_rows.keys()) == set(expected_rows.keys()):
            tol = 0.005
            elements_found["table_complete"] = all(
                abs(found_rows[v][0] - exp_u) <= tol and
                abs(found_rows[v][1] - exp_c) <= tol
                for v, (exp_u, exp_c) in expected_rows.items()
            )
        evidence.append(
            "Table complete and correct" if elements_found["table_complete"]
            else "Table incomplete or incorrect"
        )

        # ------------------------------------------------------------------
        # Low communality identification
        # x2 (0.255) is the only variable below the < .40 threshold.
        # Check: "low communalit…" line exists AND names x2 with value < 0.40.
        # ------------------------------------------------------------------
        low_comm_re = re.compile(r'low\s+communalit', re.IGNORECASE)
        if low_comm_re.search(student_answer):
            cited_re = re.compile(
                r'low\s+communalit[^\n]*?(x\d+)[^\n]*?([\d.]+)',
                re.IGNORECASE,
            )
            cited_match = cited_re.search(student_answer)
            if cited_match:
                cited_var = cited_match.group(1)
                try:
                    cited_val = float(cited_match.group(2))
                    elements_found["low_communality"] = (
                        cited_var == "x2" and cited_val < 0.40
                    )
                except ValueError:
                    pass
        evidence.append(
            "Low communality correctly identified" if elements_found["low_communality"]
            else "Low communality NOT correctly identified"
        )

        # ------------------------------------------------------------------
        # Interpretation paragraph
        # ------------------------------------------------------------------
        elements_found["interpretation"] = bool(
            re.search(r'interpretation\s*:', student_answer, re.IGNORECASE)
        )
        evidence.append(
            "Interpretation found" if elements_found["interpretation"]
            else "Interpretation NOT found"
        )

        return {
            "elements_found": elements_found,
            "evidence": evidence,
        }

    def grade_question_cw15_3_answer(self, student_answer: str, test_mode: bool = False):
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_1_task_score": 1,
                    "component_1_autoformat_score": 1,
                    "component_2_score": 8,
                    "component_2_intro_score": 1,
                    "component_2_table_ref_score": 1,
                    "component_2_table_number_score": 1,
                    "component_2_table_title_score": 1,
                    "component_2_table_itself_score": 4,
                    "component_3_score": 5,
                    "component_4_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Complete and accurate answer.",
                vibe="Student correctly computed communalities and identified the weak item."
            )

        formatting_check = self.check_formatting_elements(student_answer)
        fs = formatting_check["elements_found"]

        formatting_block = f"""
HEADER DETECTION RESULTS (USE AS FACTS):

task_description_present    = {fs["task_description"]}
no_autoformatting_present   = {fs["no_autoformatting"]}
intro_phrase_present        = {fs["intro_phrase"]}
table_ref_in_intro_present  = {fs["table_ref_in_intro"]}
table_number_present        = {fs["table_number"]}
table_title_present         = {fs["table_title"]}
table_complete              = {fs["table_complete"]}
low_communality_present     = {fs["low_communality"]}
interpretation_present      = {fs["interpretation"]}
"""

        prompt = f"""{formatting_block}

You are grading a statistics assignment.

TASK:
"In the Factor Loadings table, find the Uniqueness column. Use it to compute \
Communality = 1 − Uniqueness for each variable."

Use STRICT rubric-based grading. Total score MUST be exactly 22 points.

RUBRIC

Component 1: Formatting (2 points)
Start with 2 points.

Step 1 Task description (1 point)
Use task_description_present

Step 2 No autoformatting (1 point)
Use no_autoformatting_present

Step 1 Introductory phrase (1 point)
Use intro_phrase_present

Step 2 Table reference in intro (1 point)
Use table_ref_in_intro_present

Step 3 Table number label (1 point)
Use table_number_present

Step 4 Table title (1 point)
Use table_title_present

Step 5 Table itself (4 points)
Use table_complete.
- 4 points: table_complete is True
- 0-3 points: table_complete is False. Award based on the proportion of correct rows.

Component 2: Table 5 (8 points)
Step 1 Introductory phrase (1 point) -> component_2_intro_score
Step 2 Table reference in intro (1 point) -> component_2_table_ref_score
Step 3 Table number label (1 point) -> component_2_table_number_score
Step 4 Table title (1 point) -> component_2_table_title_score
Step 5 Table itself (4 points) -> component_2_table_itself_score
Use table_complete to grade Step 5.

Component 3: Low communalities (5 points)
Use low_communality_present.
- 5 points: low_communality_present is True
- 0-4 points: low_communality_present is False. Award based on partial identification.

Component 4: Interpretation (5 points)
Use interpretation_present.
- 5 points: interpretation_present is True and clear explanation is provided.
- 0-4 points: interpretation_present is False or vague.

SCORING INSTRUCTIONS:

component_1_task_score = 1 if not task_description_present else 0
component_1_autoformat_score = 1 if no_autoformatting_present else 0
component_1_score = component_1_task_score + component_1_autoformat_score

component_2_score = component_2_intro_score + component_2_table_ref_score + component_2_table_number_score + component_2_table_title_score + component_2_table_itself_score

total_points = component_1_score + component_2_score + component_3_score + component_4_score

ORIGINALITY CHECK:
If copied/AI-generated with suspiciously generic style, set all scores to 0 and set feedback to EXACTLY:
"Due to originality concern, your points are frozen. You can get them back if you provide oral explanation for this paper."

STUDENT ANSWER:
{student_answer}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-8>,
  "component_2_intro_score": <0-1>,
  "component_2_table_ref_score": <0-1>,
  "component_2_table_number_score": <0-1>,
  "component_2_table_title_score": <0-1>,
  "component_2_table_itself_score": <0-4>,
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
}}

SCORING INSTRUCTIONS:

component_1_task_score = 1 if not task_description_present else 0
component_1_autoformat_score = 1 if no_autoformatting_present else 0
component_1_score = component_1_task_score + component_1_autoformat_score

total_points = component_1_score + component_2_score + component_3_score + component_4_score


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
                "component_4_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        print("=" * 60)
        print("GRADING RESULTS - CW15_3")
        print("Communalities")
        print("=" * 60)

        if "component_1_score" in grading:
            if grading.get("originality_concern"):
                print("\n⚠️  ORIGINALITY CONCERN DETECTED")
                print("   All points frozen. See feedback below.")

            print("\nCOMPONENT BREAKDOWN:")
            print(f"\nFormatting: {grading.get('component_1_score')}/2")
            print(f"  • Task description:  {grading.get('component_1_task_score')}/1 (string match)")
            print(f"  • No autoformatting: {grading.get('component_1_autoformat_score')}/1 (regex)")
            if grading.get("component_1_explanation"):
                print(f"   → {grading.get('component_1_explanation')}")

            print(f"\nTable 5: {grading.get('component_2_score')}/8")
            print(f"  • Intro phrase:       {grading.get('component_2_intro_score')}/1")
            print(f"  • Table ref in intro: {grading.get('component_2_table_ref_score')}/1")
            print(f"  • Table number label: {grading.get('component_2_table_number_score')}/1")
            print(f"  • Table title:        {grading.get('component_2_table_title_score')}/1")
            print(f"  • Table itself:       {grading.get('component_2_table_itself_score')}/4")
            if grading.get("component_2_explanation"):
                print(f"   → {grading.get('component_2_explanation')}")

            print(f"\nLow communalities: {grading.get('component_3_score')}/5")
            if grading.get("component_3_explanation"):
                print(f"  → {grading.get('component_3_explanation')}")

            print(f"\nInterpretation: {grading.get('component_4_score')}/5")
            if grading.get("component_4_explanation"):
                print(f"  → {grading.get('component_4_explanation')}")

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

    evaluator = CW15_3Evaluator()

    print("=" * 60)
    print("CLASS WORK 15.3 EVALUATOR")
    print("Communalities")
    print("=" * 60)
    print("\nPlease enter the student's answer to CW15_3.")
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

    grading = evaluator.grade_cw15_3_answer(student_answer)

    evaluator.print_grading_results(grading)