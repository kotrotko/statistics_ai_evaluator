"""
midv1_2.py
Histogram Creation Evaluator - Body/Tails Labeling and Distribution Shape
Evaluation method name: def grade_midv1_question2_answer
"""

import re
import textwrap

from config import BaseEvaluator


class MidV1_2Evaluator(BaseEvaluator):
    """
    Evaluator for Histogram Creation Question (Mid v1, Question 2).

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.

    NOTE: This evaluator CANNOT recognize graphical elements (histogram bars,
    axis labels drawn in Word/image). Human reviewer must verify graphic
    components manually. A checklist reminder is printed after scoring.
    """

    def __init__(self):
        """Initialize evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1500
        )

    # ------------------------------------------------------------------
    # Section 1: Formatting / Setup Checks
    # ------------------------------------------------------------------

    def check_formatting_elements(self, student_answer: str) -> dict:
        """
        Check if student includes required formatting / setup elements.

        Checks for:
          - Task description included
          - Introductory phrase present
          - Introductory phrase contains histogram number reference
          - Histogram numbered in APA style (e.g. "Figure 1")
          - Histogram titled in APA style

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "intro_phrase": False,
            "intro_has_number": False,
            "apa_numbered": False,
            "apa_titled": False,
        }

        evidence = []

        # Task description
        task_patterns = [
            r'create a histogram',
            r'make.*histogram',
            r'histogram.*following data',
            r'task\s*:',
            r'question\s*:',
            r'hours in gym',
        ]
        for pattern in task_patterns:
            if re.search(pattern, text_lower):
                elements_found["task_description"] = True
                evidence.append(f"Found task description via pattern: '{pattern}'")
                break

        # Introductory phrase (sentence before or introducing the histogram)
        intro_patterns = [
            r'below\s+is',
            r'the following',
            r'shown below',
            r'presented below',
            r'figure\s+\d+\s+(?:shows|displays|presents|illustrates|depicts)',
            r'histogram\s+(?:shows|displays|presents|illustrates|depicts)',
            r'(?:i\s+)?(?:created|made|constructed|drew|built)\s+(?:a\s+)?histogram',
        ]
        for pattern in intro_patterns:
            if re.search(pattern, text_lower):
                elements_found["intro_phrase"] = True
                evidence.append(f"Found introductory phrase via pattern: '{pattern}'")
                break

        # Introductory phrase contains a histogram/figure number reference
        intro_number_patterns = [
            r'figure\s+\d+',
            r'histogram\s+\d+',
            r'figure\s+[ivxlc]+',
        ]
        for pattern in intro_number_patterns:
            if re.search(pattern, text_lower):
                elements_found["intro_has_number"] = True
                evidence.append(f"Intro phrase contains histogram number reference: '{pattern}'")
                break

        # APA-style figure number (e.g. "Figure 1" or "Figure 1." as standalone label)
        apa_number_patterns = [
            r'\bfigure\s+\d+\b',
            r'\bfig\.\s*\d+\b',
        ]
        for pattern in apa_number_patterns:
            if re.search(pattern, text_lower):
                elements_found["apa_numbered"] = True
                evidence.append(f"APA figure number found: '{pattern}'")
                break

        # APA-style title (a descriptive title line, often italicized in APA)
        # Heuristic: look for a title-like phrase near "histogram" or "hours"
        title_patterns = [
            r'hours\s+(?:in\s+)?(?:gym|per\s+week)',
            r'gym\s+hours',
            r'frequency\s+of\s+',
            r'distribution\s+of\s+',
            r'histogram\s+of\s+',
        ]
        for pattern in title_patterns:
            if re.search(pattern, text_lower):
                elements_found["apa_titled"] = True
                evidence.append(f"APA-style title found via pattern: '{pattern}'")
                break

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear formatting elements found"],
        }

    # ------------------------------------------------------------------
    # Section 2: Distribution Shape Check
    # ------------------------------------------------------------------

    def check_distribution_shape(self, student_answer: str) -> dict:
        """
        Check if student correctly identifies distribution shape.

        Checks for:
          - Explicit mention of distribution shape
          - Skewness mentioned
          - Right-skewed / positively skewed direction identified

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        shape_found = {
            "shape_mentioned": False,
            "skewed_mentioned": False,
            "right_skewed_identified": False,
        }

        evidence = []

        # SYSTEMATIC FIX: Define the end of the prompt instructions.
        # We only evaluate text appearing AFTER this marker.
        prompt_marker = "or symmetrical"
        if prompt_marker in text_lower:
            eval_area = text_lower.split(prompt_marker)[-1]
        else:
            eval_area = text_lower

        # 1. Distribution shape mentioned (3 pts) - YOUR original patterns
        shape_patterns = [
            r'the shape is', r'distribution is', r'skew',
            r'right skewed', r'positively skewed'
        ]
        for pattern in shape_patterns:
            if re.search(pattern, eval_area):
                shape_found["shape_mentioned"] = True
                evidence.append(f"Distribution shape mentioned via pattern: '{pattern}'")
                break

        # 2. Skewness mentioned (1 pt) - YOUR original patterns
        if re.search(r'skew', eval_area):
            shape_found["skewed_mentioned"] = True
            evidence.append("Skewness mentioned")

        # 3. Right-skewed / positive skew identified (1 pt) - YOUR original patterns
        right_skew_patterns = [
            r'right[\s\-]*skew',
            r'positively\s+skew',
            r'skew(?:ed)?\s+(?:to\s+the\s+)?right',
            r'positive\s+skew',
        ]

        for pattern in right_skew_patterns:
            if re.search(pattern, eval_area):
                shape_found["right_skewed_identified"] = True
                evidence.append(f"Right-skewed / positive skew identified via pattern: '{pattern}'")
                break

        return {
            "shape_found": shape_found,
            "evidence": evidence if evidence else ["No distribution shape discussion found"],
        }

    # ------------------------------------------------------------------
    # Section 3: Body and Tails Labeling Check
    # ------------------------------------------------------------------

    def check_body_tails_labeling(self, student_answer: str) -> dict:
        """
        Check textual evidence of body and tails labeling.

        NOTE: Actual graphical labels in images/Word cannot be verified
        programmatically. This checks only for textual mentions/descriptions.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        labeling_found = {
            "body_mentioned": False,
            "tails_mentioned": False,
        }

        evidence = []

        body_patterns = [
            r'\bbody\b',
            r'center\s+(?:of\s+)?(?:the\s+)?(?:histogram|distribution)',
            r'middle\s+(?:of\s+)?(?:the\s+)?(?:histogram|distribution)',
            r'main\s+(?:part|portion|section)',
        ]
        for pattern in body_patterns:
            if re.search(pattern, text_lower):
                labeling_found["body_mentioned"] = True
                evidence.append(f"Body mentioned via pattern: '{pattern}'")
                break

        tail_patterns = [
            r'\btail',
            r'left\s+(?:side|end)',
            r'right\s+(?:side|end)',
            r'extreme\s+value',
        ]
        for pattern in tail_patterns:
            if re.search(pattern, text_lower):
                labeling_found["tails_mentioned"] = True
                evidence.append(f"Tails mentioned via pattern: '{pattern}'")
                break

        return {
            "labeling_found": labeling_found,
            "evidence": evidence if evidence else ["No textual body/tails labeling found"],
        }

    # ------------------------------------------------------------------
    # Section 4: Main Grading Method
    # ------------------------------------------------------------------

    def grade_midv1_question2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade the histogram creation and analysis question.

        Rubric (20 points total):
          Component 1 – Histogram Setup (6 pts)
          Component 2 – Histogram Basic Labeling (4 pts) [HUMAN REVIEW]
          Component 3 – Body and Tails Labeling (5 pts) [HUMAN REVIEW]
          Component 4 – Distribution Shape (5 pts)

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock result without API call

        Returns:
            Dictionary with grading results
        """
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 5,
                    "component_2_score": 4,
                    "component_3_score": 4,
                    "component_4_score": 4,
                },
                max_points=20,
                feedback="Test mode feedback for histogram creation task.",
                vibe="Test mode vibe assessment",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "task_description": True,
                            "intro_phrase": True,
                            "intro_has_number": True,
                            "apa_numbered": True,
                            "apa_titled": True,
                        },
                        "evidence": ["Test mode - all elements present"],
                    },
                    "distribution_check": {
                        "shape_found": {
                            "shape_mentioned": True,
                            "skewed_mentioned": True,
                            "right_skewed_identified": True,
                        },
                        "evidence": ["Test mode - shape correctly identified"],
                    },
                    "body_tails_check": {
                        "labeling_found": {
                            "body_mentioned": True,
                            "tails_mentioned": True,
                        },
                        "evidence": ["Test mode - body and tails mentioned"],
                    },
                },
            )

        # Run automatic checks
        formatting_check = self.check_formatting_elements(student_answer)
        distribution_check = self.check_distribution_shape(student_answer)
        body_tails_check = self.check_body_tails_labeling(student_answer)

        prompt = f"""You are grading a statistics midterm assignment where students must create a histogram, label it properly (including body and tails), and analyze its distribution shape.

**TASK DESCRIPTION (m1_2):**
Create a histogram for the following data (10 points).
Label the tails and body (5 points) and determine if it is skewed (and direction, if so) or symmetrical (5 points).
For labeling, students may use Word/Draw or Word/Insert/Shapes.

Data table:
  Hours in Gym per Week | Frequency
  0–3                   | 3
  4–7                   | 9
  8–11                  | 7
  12–15                 | 4
  16–19                 | 1

**CORRECT DISTRIBUTION SHAPE:**
This data is RIGHT-SKEWED (positively skewed). The histogram peaks in the 4–7 interval and tapers off to the right, making the right tail longer.

**ORIGINALITY CHECK:**
If the student's answer appears to be copied AI-generated text (generic, impersonal, highly polished, lacks any student-specific reasoning or personalization), assign 0 points to ALL components and include the following teacher's comment verbatim in the feedback field:
"Due to originality concern, your points are frozen. You can get them back if you provide oral explanation for this paper."
Stop further evaluation if copied AI text is detected.

---

**RUBRIC (20 points total):**

**Component 1: Histogram Setup (6 points)**
NOTE: Components 2 and 3 (graphical elements) CANNOT be verified by this evaluator.
Score only what is visible in the text portion of the answer.
  - Task description included correctly: 1 point
  - Introductory phrase present: 1 point
  - Introductory phrase contains reference to histogram number: 1 point
  - Histogram is numbered in APA style (e.g., "Figure 1"): 1 point
  - Histogram is titled in APA style (descriptive title near figure label): 1 point
  Maximum: 5 text-verifiable points. The 6th point is awarded only if all 5 text elements are present AND the student also mentions or describes the histogram itself (any reference to bars, classes, or the graph structure).

**Component 2: Histogram Basic Labeling (4 points) — HUMAN REVIEW REQUIRED**
This evaluator CANNOT verify graphical axis labels. Award full 4 points for scoring purposes.
Human reviewer must manually verify:
  - Correct number of class intervals on x-axis (equal to 5): 1 point
  - Correct frequencies on y-axis: 1 point
  - X-axis labeled properly (Hours per Week): 1 point
  - Y-axis labeled properly (Frequency): 1 point

**Component 3: Body and Tails Labeling (5 points) — HUMAN REVIEW REQUIRED**
This evaluator CANNOT verify graphical body/tails labels. Award full 5 points for scoring purposes.
Human reviewer must manually verify:
  - Clear labeling of body: 3 points
  - Clear labeling of tails: 2 points
HOWEVER: If the student makes NO textual mention of body or tails anywhere in their written answer, deduct 2 points from Component 3 (score = 3 instead of 5), as they may not have attempted this at all.

**Component 4: Distribution Shape (5 points)**
STRICT EVIDENCE RULES:
1. Ignore the task description text ("determine if it is skewed...").
2. Ignore figure titles (e.g., "Figure 1 presents...").
3. Points are only awarded if the student adds a NEW sentence of analysis after the histogram/data table.

Scoring:
- Distribution shape is mentioned in the student's own analysis: 3 points
- Distribution is identified as skewed (any direction): 1 point
- Distribution is correctly identified as right-skewed (or positively skewed): 1 point

If the student answer contains only the data and the figure titles, Component 4 score MUST be 0.

---

**STUDENT ANSWER:**
{{student_answer}}

**AUTOMATIC FORMATTING DETECTION RESULT:**
Elements Found: {{formatting_check['elements_found']}}
Evidence: {{formatting_check['evidence']}}

**AUTOMATIC DISTRIBUTION SHAPE DETECTION RESULT:**
Shape Found: {{distribution_check['shape_found']}}
Evidence: {{distribution_check['evidence']}}

**AUTOMATIC BODY/TAILS DETECTION RESULT:**
Labeling Found: {{body_tails_check['labeling_found']}}
Evidence: {{body_tails_check['evidence']}}

**FINAL GRADING RULE FOR COMPONENT 4:**
You must prioritize the **Evidence** provided in the "AUTOMATIC DISTRIBUTION SHAPE DETECTION RESULT" block. 
If that evidence states "No distribution shape discussion found", you are FORBIDDEN from awarding points for Component 4, even if you see the word "skewed" in the task instructions.

**CRITICAL GRADING RULES:**
1. If AI-copied text is detected → 0 points all components, add teacher's comment.
2. Component 2 and Component 3 graphic elements CANNOT be verified — award full graphic points and remind human reviewer.
3. Exception to Rule 2: If student makes no written mention of body/tails, deduct 2 from Component 3.
4. The correct distribution shape is RIGHT-SKEWED. Any other answer loses the directional point.
5. Students must explicitly mention "skewed" to earn the skewness point.
6. Total must equal exactly 20 points maximum.

**SCORING PROCESS:**
1. Check for AI text originality — if copied, score 0 everywhere.
2. Score Component 1 (Histogram Setup): __/6
3. Score Component 2 (Basic Labeling): 4/4 [graphic, assumed correct for scoring; human reviews]
4. Score Component 3 (Body/Tails Labeling): 5/5 [graphic, assumed correct] OR 3/5 if no written mention
5. Score Component 4 (Distribution Shape): __/5
6. Total = sum (max 20)

Return your grading in this exact JSON format:
{{
  "component_1_score": <0-6>,
  "component_1_explanation": "<if score < 6: one sentence explaining what setup elements are missing; if 6: confirm all present>",
  "component_2_score": <0-4>,
  "component_2_explanation": "Graphic elements cannot be verified by this evaluator. Awarded full 4 points pending human review. See checklist below.",
  "component_3_score": <0-5>,
  "component_3_explanation": "<if no written body/tails mention: note deduction of 2 points; otherwise: awarded full 5 points pending human review>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<always explain: what shape elements are present, whether right-skewed was correctly identified, and what is missing>",
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative covering: (1) originality status, (2) setup/formatting compliance, (3) body and tails labeling attempt, (4) distribution shape analysis with correctness assessment>",
  "vibe": "<one-sentence assessment of student's overall understanding of histograms and distribution shape>"
}}"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "formatting_check": formatting_check,
                "distribution_check": distribution_check,
                "body_tails_check": body_tails_check,
            },
        )

        # Attach auxiliary checks to result for transparency
        if "error" not in result:
            result["formatting_check"] = formatting_check
            result["distribution_check"] = distribution_check
            result["body_tails_check"] = body_tails_check

        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    # ------------------------------------------------------------------
    # Section 5: Print Results
    # ------------------------------------------------------------------

    def print_grading_results(self, grading: dict):
        """Print formatted grading results to console."""
        print("=" * 60)
        print("GRADING RESULTS - MID V1 Q2")
        print("Histogram Creation - Body/Tails Labeling & Distribution Shape")
        print("=" * 60)

        if "component_1_score" in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Histogram Setup): {grading.get('component_1_score', 'N/A')}/6")
            if grading.get("component_1_explanation"):
                wrapped = textwrap.fill(
                    grading["component_1_explanation"], width=54,
                    initial_indent="    → ", subsequent_indent="      "
                )
                print(wrapped)

            print(f"  Component 2 (Basic Labeling): {grading.get('component_2_score', 'N/A')}/4")
            if grading.get("component_2_explanation"):
                wrapped = textwrap.fill(
                    grading["component_2_explanation"], width=54,
                    initial_indent="    → ", subsequent_indent="      "
                )
                print(wrapped)

            print(f"  Component 3 (Body & Tails Labeling): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get("component_3_explanation"):
                wrapped = textwrap.fill(
                    grading["component_3_explanation"], width=54,
                    initial_indent="    → ", subsequent_indent="      "
                )
                print(wrapped)

            print(f"  Component 4 (Distribution Shape): {grading.get('component_4_score', 'N/A')}/5")
            if grading.get("component_4_explanation"):
                wrapped = textwrap.fill(
                    grading["component_4_explanation"], width=54,
                    initial_indent="    → ", subsequent_indent="      "
                )
                print(wrapped)

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points', 'N/A')}/{grading.get('max_points', 20)}")
        print(f"PERCENTAGE: {grading.get('percentage', 'N/A')}%")

        print("\n" + "=" * 60)
        print("FEEDBACK:")
        print("=" * 60)
        feedback_text = grading.get("feedback", "No feedback available")
        print(textwrap.fill(feedback_text, width=60))

        print("\n" + "=" * 60)
        print("THE VIBE:")
        print("=" * 60)
        vibe_text = grading.get("vibe", "N/A")
        print(textwrap.fill(vibe_text, width=60))

        # ========------------------------------------------------------------------
        # Section 6: Human Reviewer Checklist
        # ========------------------------------------------------------------------        print("\n" + "=" * 60)
        print("\n" + "=" * 60)
        print("⚠️  HUMAN REVIEWER CHECKLIST (Graphic Elements):")
        print("=" * 60)
        print("Please verify the chart and enter 'y' if correct or 'n' if missing:")
        print("=" * 60)

        # Initialize manual scores
        c2_manual = 0
        c3_manual = 0

        # These lines now act as interactive prompts
        if input("  • Correct number of class intervals (5) [y/n]: ").lower().strip() == 'y': c2_manual += 1
        if input("  • Correct frequencies on Y-axis [y/n]: ").lower().strip() == 'y': c2_manual += 1
        if input("  • X-axis labelled (Hours per Week) [y/n]: ").lower().strip() == 'y': c2_manual += 1
        if input("  • Y-axis labelled (Frequency) [y/n]: ").lower().strip() == 'y': c2_manual += 1

        if input("  • Body and tails labelled properly [y/n]: ").lower().strip() == 'y': c3_manual += 5


        print("  • Correct number of class intervals (5): 1 pt")
        print("  • Correct frequencies on Y-axis:         1 pt")
        print("  • X-axis labelled (Hours per Week):      1 pt")
        print("  • Y-axis labelled (Frequency):           1 pt")
        print("  • Body and tails labelled properly:      5 pts")
        print("Please check the student's chart and enter points to DEDUCT")
        print("if any elements are missing (Enter 0 if all are perfect):")
        print("=" * 60)

        # Update components with your manual review values
        grading['component_2_score'] = c2_manual
        grading['component_3_score'] = c3_manual

        # Recalculate total based on manual review + AI auto-graded sections
        grading['total_points'] = (
                grading.get('component_1_score', 0) +
                grading['component_2_score'] +
                grading['component_3_score'] +
                grading.get('component_4_score', 0)
        )

        # Recalculate percentage
        grading['percentage'] = round((grading['total_points'] / grading['max_points']) * 100, 1)

        print("\n" + "=" * 60)
        print(f"✅ FINAL ADJUSTED SCORE: {grading['total_points']}/{grading['max_points']} ({grading['percentage']}%)")
        print("=" * 60)

        # try:
        #     # Now the prompt appears AFTER the instructions
        #     deduction = input("Total points to DEDUCT: ").strip()
        #     deduction_val = float(deduction) if deduction else 0.0
        #
        #     if deduction_val > 0:
        #         grading['total_points'] -= deduction_val
        #         # Recalculate percentage
        #         grading['percentage'] = round((grading['total_points'] / grading['max_points']) * 100, 1)
        #
        #         print(f"\n✅ Score adjusted!")
        #         print(f"NEW TOTAL: {grading['total_points']}/{grading['max_points']} ({grading['percentage']}%)")
        #     else:
        #         print("\n✅ No deductions applied. Original score kept.")
        # except ValueError:
        #     print("\n❌ Invalid input. No adjustments made.")

        print("=" * 60)
        print("  • Please make sure that you see correct frequencies on")
        print("    y-axis: 1 point")
        print("  • Please make sure that you see X-axis labelled properly")
        print("    (Hours per Week): 1 point")
        print("  • Please make sure that you see Y-axis labelled properly")
        print("    (Frequency): 1 point")
        print("  • Please make sure that you see body and tails labelled")
        print("    properly: 5 points")
        print()
        print("If any graphic element is missing, adjust the total score")
        print("accordingly and update the student's record.")
        print("=" * 60)

        if "error" in grading:
            print("\n" + "=" * 60)
            print("ERROR:")
            print("=" * 60)
            print(grading.get("error"))
            if "raw_response" in grading:
                print("\nRaw Response:")
                print(grading["raw_response"][:500])


# ------------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------------

if __name__ == "__main__":
    print("Welcome to the Homework AI Evaluator System!")
    print("=" * 60)

    evaluator = MidV1_2Evaluator()

    print("=" * 60)
    print("MIDTERM V1 - QUESTION 2 EVALUATOR")
    print("Histogram Creation - Body/Tails Labeling & Distribution Shape")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION M1_2.")
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

    grading = evaluator.grade_midv1_question2_answer(student_answer)

    evaluator.print_grading_results(grading)