"""
cw9_5.py
Classwork 9: Independent groups comparison
Statistical analysis and interpretation
Evaluation method name: def grade_cw9_5_answer
"""

import re
from config import BaseEvaluator


class CW9_5Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 9_5.

    Task: Using JASP, calculate the statistics and include the table in APA style.
    Make a statistical inference (reject or fail to reject the null hypothesis) (5 points).
    Include Cohen's d effect size and explain what it means. Add and describe the Descriptive plot (5 points).
    Describe the result in APA style (5 points).
    Answer the main research question (5 points).
    Total (strictly) 20 points.

    Evaluates student's ability to present JASP output in APA format, make statistical inference,
    report effect size with interpretation, include descriptive plot, write APA-style results,
    and answer the research question.

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
        print(f"DEBUG: FULL student_answer:\n{student_answer}\n{'='*60}")
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "step_system": False,
            "statistical_inference": False,
            "effect_size": False,
            "descriptive_plot": False,
            "apa_description": False,
            "research_question": False
        }

        evidence = []

        # Checkpoint 1 — Task description (Pedagogical markers)
        pedagogical_markers = [
            "explain what it means",
            "add and describe",
            "answer the main research question",
            "reject or fail to reject",
            "make a statistical inference"
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found (via pedagogical markers)")
        else:
            elements_found["task_description"] = False
            evidence.append("Task description NOT found")

        # Checkpoint 2 — Step System (Step 5)
        if re.search(r'step\s*5', text_lower):
            elements_found["step_system"] = True
            evidence.append("Step 5 found")
        else:
            evidence.append("Step 5 NOT found (required format)")

        # Checkpoint 3 — Statistical inference
        if re.search(r'reject|fail\s*to\s*reject|do\s*not\s*reject|cannot\s*reject', text_lower) and \
                re.search(r'null\s*hypothesis|h[_0₀]', text_lower):
            elements_found["statistical_inference"] = True
            evidence.append("Statistical inference found")
        else:
            evidence.append("Statistical inference NOT found")

        # Checkpoint 4 — Effect size (Cohen's d)
        if re.search(r'cohen[\s\']?s?\s*d|effect\s*size', text_lower):
            elements_found["effect_size"] = True
            evidence.append("Effect size (Cohen's d) found")
        else:
            evidence.append("Effect size (Cohen's d) NOT found")

        # Checkpoint 5 — Descriptive plot
        if re.search(r'descriptive\s*plot|plot|figure|graph|chart', text_lower):
            elements_found["descriptive_plot"] = True
            evidence.append("Descriptive plot found")
        else:
            evidence.append("Descriptive plot NOT found")

        # Checkpoint 6 — APA-style description with statistical markers
        apa_markers = re.search(r't\s*\(|p\s*=|ci|confidence\s*interval|m\s*=|sd\s*=|mean|standard\s*deviation', text_lower)
        if apa_markers:
            elements_found["apa_description"] = True
            evidence.append("APA-style description found")
        else:
            evidence.append("APA-style description NOT found")

        # Checkpoint 7 — Research question answer
        if re.search(r'research\s*question|main\s*question|question|answer|conclusion', text_lower):
            elements_found["research_question"] = True
            evidence.append("Research question answer found")
        else:
            evidence.append("Research question answer NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_cw9_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 9.5: Statistical Analysis and Interpretation.
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
                feedback="[TEST MODE] JASP table included with proper APA formatting. Statistical inference clear. Cohen's d reported with interpretation. Descriptive plot included. APA-style description complete. Research question answered.",
                vibe="Student demonstrates comprehensive understanding of statistical analysis and APA reporting",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "task_description": True,
                            "step_system": True,
                            "statistical_inference": True,
                            "effect_size": True,
                            "descriptive_plot": True,
                            "apa_description": True,
                            "research_question": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics assignment about statistical analysis and interpretation using a **STRICT rubric-based approach.

**TASK DESCRIPTION:**
Students must complete 4 components for statistical analysis and interpretation using JASP output.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Students MUST use explicit Step System format (Step 5) — if not used, deduct 1 point from total and mention in feedback
3. Focus on conceptual understanding and proper APA formatting
4. Feedback should be SHORT, written as a teacher's comment
5. Feedback CANNOT be an invitation for further discussion
6. Check for originality first; copied AI text should receive 0 points with comment: "Due to originality concern, your points are frozen. You can get them back if you provide oral explanation for this paper."

**RUBRIC:**

**Component 1: Task Description (1 point)**
- Use task_description from elements_found.
- 1/1: If task_description_present is True.
- 0/1: If task_description_present is False.

**Component 2: Statistical Test Result and Inference (4 points):**
- 4/4: JASP output table included with all APA elements (introductory phrase with reference by table number, table number, table title) AND correct statistical inference explicitly stated (reject / fail to reject H₀)
- 3/4: Table and inference present but one element missing (e.g., no reference by table number in introductory phrase, or no table number, or no table title)
- 2/4: Table and inference present but two elements missing (e.g., no introductory phrase, or no table number and no table title)
- 1/4: Table and inference present but three elements missing (e.g., no introductory phrase and no table number, or no introductory phrase and no table title)
- 0/4: No statistical result provided
- CRITICAL: Student must explicitly state "reject" or "fail to reject" the null hypothesis
- CRITICAL: Table must include introductory phrase, reference by number, table number, and table title

**Component 3: Effect Size Cohen's d and Descriptive Plot (5 points):**
- - Use effect_size and descriptive_plot from elements_found.
- CRITICAL: If descriptive_plot is False, maximum score is 2/5 regardless of other content
- 5/5: Cohen's d value correctly reported AND interpreted (small / medium / large effect) AND Descriptive plot included with clear interpretation
- 4/5: Cohen's d reported AND Descriptive plot included, but one of expected interpretations is missing or unclear
- 3/5: Cohen's d reported AND Descriptive plot included, but both expected interpretations are missing or unclear
- 2/5: EITHER Cohen's d is missing OR Descriptive plot is missing (not both present)
- 1/5: Attempt present but incorrect or poorly explained
- 0/5: Both Cohen's d and Descriptive plot are not reported
- CRITICAL: This component requires BOTH elements - if either is missing, maximum score is 2/5
- CRITICAL: Descriptive plot must be explicitly mentioned (e.g., "Figure 1", "the plot shows", "as illustrated in the graph")
- CRITICAL: Simply having Cohen's d without a plot = 2/5 maximum, not 5/5
- CRITICAL: Cohen's d interpretation should classify effect as small (d ≈ 0.2), medium (d ≈ 0.5), or large (d ≈ 0.8)

**Component 4: APA-Style Result Description (5 points):**
- 5/5: Result description follows expected APA structure with all three blocks in correct order:
  (a) research design statement (test type and groups described),
  (b) assumption checks (normality and homogeneity tests with p-values),
  (c) t-test results block including: t(df), p =, CI, d =, M =, SD = for each group
- 4/5: Structure mostly followed; minor omissions or formatting issues
- 3/5: One block out of three is missing or out of order
- 2/5: Two blocks out of three are missing or out of order
- 1/5: Attempt present but structure or statistics mostly incorrect
- 0/5: No component provided
- CRITICAL: Description must include APA markers: t(df), p =, CI, d =, M =, SD =
- CRITICAL: Sequence matters: Research design → Assumptions → t-test results → Descriptives
- CRITICAL: Numeric style: p-values may omit leading zero; other statistics ≥1 require leading zero
- NOTE: Statistical symbols (t, p, d, M, SD) should be italicized (instructor confirms during manual review)

**Component 5: Answer the Main Research Question (5 points):**
- 5/5: Clear, direct answer to the research question, supported by statistical results, written in plain language accessible to non-statisticians
- 4/5: Answer present but slightly unclear or missing minor supporting detail
- 3/5: Answer present but vague or poorly connected to statistical results
- 2/5: Attempt present but answer is incomplete or weakly supported
- 1/5: Answer attempted but mostly incorrect or unsupported
- 0/5: No answer to research question provided
- CRITICAL: Answer must directly address the original research question, not just restate statistical findings
- CRITICAL: Should be written in accessible language, translating statistical results into practical meaning

STUDENT ANSWER:
{student_answer}

Return grading in this exact JSON format:
{{
  "component_1_score": <0-1>,
  "component_1_explanation": "<brief explanation>",
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
}}"""

        element_check = self.check_required_elements(student_answer)
        element_summary = element_check["elements_found"]

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "element_check": element_check
            }
        )

        # Force the score to 0 if the pedagogical markers are missing
        if "error" not in result:
            if not element_check["elements_found"]["task_description"]:
                result["component_1_score"] = 0
                result["component_1_explanation"] = "Task description NOT found (instructional phrasing missing)"

        # Force Component 3 score cap if descriptive_plot is missing
        if "error" not in result:
            if not element_check["elements_found"]["descriptive_plot"]:
                if result.get("component_3_score", 0) > 2:
                    result["component_3_score"] = 2
                    result[
                        "component_3_explanation"] = "Descriptive plot NOT found - score capped at 2/5. " + result.get(
                        "component_3_explanation", "")

        # Force Component 3 score cap if effect_size is missing
        if "error" not in result:
            print(f"DEBUG: effect_size = {element_check['elements_found']['effect_size']}")
            print(f"DEBUG: component_3_score BEFORE = {result.get('component_3_score', 0)}")
            if not element_check["elements_found"]["effect_size"]:
                if result.get("component_3_score", 0) > 2:
                    result["component_3_score"] = 2
                    result[
                        "component_3_explanation"] = "Cohen's d NOT found - score capped at 2/5. " + result.get(
                        "component_3_explanation", "")
                    print(f"DEBUG: component_3_score AFTER CAP = {result['component_3_score']}")
        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score",
                "component_5_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results."""
        import textwrap
        print("=" * 60)
        print("GRADING RESULTS - CLASSWORK 9.5")
        print("Statistical Analysis and Interpretation")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Task Description): {grading.get('component_1_score', 'N/A')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Statistical Result & Inference): {grading.get('component_2_score', 'N/A')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Cohen's d & Descriptive Plot): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (APA-Style Description): {grading.get('component_4_score', 'N/A')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Research Question Answer): {grading.get('component_5_score', 'N/A')}/5")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

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
            if 'raw_response' in grading:
                print("\nRaw Response:")
                print(grading['raw_response'][:500])


if __name__ == "__main__":
    evaluator = CW9_5Evaluator()
    from config import InputHandler

    input_handler = InputHandler()
    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 9.5",
        question_description="Statistical Analysis and Interpretation",
        min_length=20
    )
    if student_answer:
        grading = evaluator.grade_cw9_5_answer(student_answer)
        evaluator.print_grading_results(grading)