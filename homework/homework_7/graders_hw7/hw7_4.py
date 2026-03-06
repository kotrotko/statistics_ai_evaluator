"""
hw7_4.py
Hypothesis Testing Decision-Making Evaluation
Evaluation method name: def grade_question_hw7_4_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW7_4Evaluator(BaseEvaluator):
    """
    Evaluator for Hypothesis Testing Decision-Making (HW7_4).

    Task: Determine whether to reject or fail to reject H₀ in four scenarios:
    a. t-value comparison (two-tailed)
    b. t-value comparison (one-tailed)
    c. CI comparison (μ outside CI)
    d. CI comparison (μ inside CI)

    No step system required for this question.

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    TASK_DESCRIPTION = "Determine whether you would reject or fail to reject the null hypothesis in the following situations: a. t = 2.58, N = 21, two-tailed test at α = 0.05, b. t = 1.99, N = 49, one-tailed test at α = 0.01, c. μ = 47.82, 99% CI = (48.71, 49.28), d. μ = 0, 95% CI = (-0.15, 0.20)"

    def __init__(self):
        """Initialize evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1500
        )

    def check_formatting_elements(self, student_answer: str) -> dict:
        """
        Check if student includes required formatting elements for hypothesis testing decisions.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "part_a_present": False,
            "part_b_present": False,
            "part_c_present": False,
            "part_d_present": False,
            "all_parts_present": False,
            "df_calculations_present": False,
            "critical_values_present": False,
            "decisions_stated": False,
            "ci_comparisons_present": False
        }

        evidence = []

        # Check for task description
        task_patterns = [
            r'reject.*fail\s+to\s+reject.*null\s+hypothesis',
            r'determine.*reject.*null',
            r't\s*=\s*2\.58.*n\s*=\s*21',
            r'μ\s*=\s*47\.82.*ci'
        ]
        task_matches = sum(1 for pattern in task_patterns if re.search(pattern, text_lower))
        if task_matches >= 2:
            elements_found["task_description"] = True
            evidence.append(f"Found task description (matched {task_matches}/4 key phrases)")

        # Check for part a
        if re.search(r'\ba[\.\):\s]', student_answer) or re.search(r'part\s*a', text_lower):
            elements_found["part_a_present"] = True
            evidence.append("Part a found")
        else:
            evidence.append("Part a NOT found")

        # Check for part b
        if re.search(r'\bb[\.\):\s]', student_answer) or re.search(r'part\s*b', text_lower):
            elements_found["part_b_present"] = True
            evidence.append("Part b found")
        else:
            evidence.append("Part b NOT found")

        # Check for part c
        if re.search(r'\bc[\.\):\s]', student_answer) or re.search(r'part\s*c', text_lower):
            elements_found["part_c_present"] = True
            evidence.append("Part c found")
        else:
            evidence.append("Part c NOT found")

        # Check for part d
        if re.search(r'\bd[\.\):\s]', student_answer) or re.search(r'part\s*d', text_lower):
            elements_found["part_d_present"] = True
            evidence.append("Part d found")
        else:
            evidence.append("Part d NOT found")

        # Check if all parts are present
        if all([
            elements_found["part_a_present"],
            elements_found["part_b_present"],
            elements_found["part_c_present"],
            elements_found["part_d_present"]
        ]):
            elements_found["all_parts_present"] = True
            evidence.append("All 4 parts explicitly labeled")

        # Check for df calculations
        if re.search(r'df\s*=\s*n\s*-\s*1|degrees\s+of\s+freedom', text_lower):
            elements_found["df_calculations_present"] = True
            evidence.append("df calculations present")

        # Check for critical values
        if re.search(r't\*|t\s*=\s*[0-9]\.[0-9]+|critical\s+value', text_lower):
            elements_found["critical_values_present"] = True
            evidence.append("Critical values mentioned")

        # Check for decisions stated
        if re.search(r'reject\s+h[_\s]*0|fail\s+to\s+reject', text_lower):
            elements_found["decisions_stated"] = True
            evidence.append("Decisions (reject/fail to reject) stated")

        # Check for CI comparisons
        if re.search(r'inside.*ci|outside.*ci|within.*ci|not.*in.*ci|μ.*<|μ.*>', text_lower):
            elements_found["ci_comparisons_present"] = True
            evidence.append("CI comparisons present")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear formatting elements found"]
        }

    def check_formatting_graphs_and_calculations(self, student_answer: str) -> dict:
        """
        Check if student includes required calculations for hypothesis testing decisions.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found calculations and evidence
        """
        text_lower = student_answer.lower()

        calculations_found = {
            "part_a_df_correct": False,
            "part_a_critical_value_correct": False,
            "part_a_comparison_present": False,
            "part_a_decision_correct": False,
            "part_b_df_correct": False,
            "part_b_critical_value_correct": False,
            "part_b_comparison_present": False,
            "part_b_decision_correct": False,
            "part_c_comparison_present": False,
            "part_c_decision_correct": False,
            "part_d_comparison_present": False,
            "part_d_decision_correct": False
        }

        evidence = []

        # Part a: t = 2.58, N = 21, two-tailed test at α = 0.05
        # df = 20, critical value ≈ 2.09 (two-tailed)
        # 2.58 > 2.09 → Reject H₀

        if re.search(r'df\s*=\s*20|20\s*->|n\s*-\s*1\s*=\s*20', student_answer):
            calculations_found["part_a_df_correct"] = True
            evidence.append("Part a: df = 20 found")

        if re.search(r't\*?\s*=\s*2\.0[89]|critical.*2\.0[89]|2\.0[89]', student_answer):
            calculations_found["part_a_critical_value_correct"] = True
            evidence.append("Part a: critical value ≈ 2.09 found")

        if re.search(r'2\.58\s*>|>\s*2\.0[89]|2\.58.*greater', text_lower):
            calculations_found["part_a_comparison_present"] = True
            evidence.append("Part a: comparison 2.58 > 2.09 present")

        if re.search(r'reject\s+h[_\s]*0(?!\s*fail)|reject.*null(?!\s*fail)', text_lower):
            # Check if this appears in context of part a (before part b or near 2.58)
            part_a_section = student_answer[
                             :student_answer.lower().find('b.') if 'b.' in student_answer.lower() else len(
                                 student_answer)]
            if re.search(r'reject\s+h[_\s]*0|reject.*null', part_a_section.lower()):
                calculations_found["part_a_decision_correct"] = True
                evidence.append("Part a: decision 'Reject H₀' found")

        # Part b: t = 1.99, N = 49, one-tailed test at α = 0.01
        # df = 48, critical value ≈ 2.41 (one-tailed)
        # 1.99 < 2.41 → Fail to reject H₀

        if re.search(r'df\s*=\s*48|48\s*->|n\s*-\s*1\s*=\s*48', student_answer):
            calculations_found["part_b_df_correct"] = True
            evidence.append("Part b: df = 48 found")

        if re.search(r't\*?\s*=\s*2\.4[01]|critical.*2\.4[01]|2\.4[01]', student_answer):
            calculations_found["part_b_critical_value_correct"] = True
            evidence.append("Part b: critical value ≈ 2.41 found")

        if re.search(r'1\.99\s*<|<\s*2\.4[01]|2\.4[01]\s*>\s*1\.99|1\.99.*less', text_lower):
            calculations_found["part_b_comparison_present"] = True
            evidence.append("Part b: comparison 1.99 < 2.41 present")

        # For part b, look for "fail to reject" after part b starts
        if 'b.' in student_answer.lower() or 'part b' in student_answer.lower():
            part_b_start = max(
                student_answer.lower().find('b.') if 'b.' in student_answer.lower() else 0,
                student_answer.lower().find('part b') if 'part b' in student_answer.lower() else 0
            )
            part_b_section = student_answer[
                             part_b_start:student_answer.lower().find('c.') if 'c.' in student_answer.lower() else len(
                                 student_answer)]
            if re.search(r'fail\s+to\s+reject', part_b_section.lower()):
                calculations_found["part_b_decision_correct"] = True
                evidence.append("Part b: decision 'Fail to reject H₀' found")

        # Part c: μ = 47.82, 99% CI = (48.71, 49.28)
        # 47.82 is NOT inside (48.71, 49.28) → Reject H₀

        if re.search(r'47\.82.*not.*inside|47\.82.*outside|47\.82.*<.*48\.71|not.*in.*ci', text_lower):
            calculations_found["part_c_comparison_present"] = True
            evidence.append("Part c: comparison showing μ outside CI present")

        # For part c, look for reject (not fail to reject)
        if 'c.' in student_answer.lower() or 'part c' in student_answer.lower():
            part_c_start = max(
                student_answer.lower().find('c.') if 'c.' in student_answer.lower() else 0,
                student_answer.lower().find('part c') if 'part c' in student_answer.lower() else 0
            )
            part_c_section = student_answer[
                             part_c_start:student_answer.lower().find('d.') if 'd.' in student_answer.lower() else len(
                                 student_answer)]
            if re.search(r'reject\s+h[_\s]*0(?!.*fail)|reject(?!.*fail)', part_c_section.lower()):
                calculations_found["part_c_decision_correct"] = True
                evidence.append("Part c: decision 'Reject H₀' found")

        # Part d: μ = 0, 95% CI = (-0.15, 0.20)
        # 0 is inside (-0.15, 0.20) → Fail to reject H₀

        if re.search(r'0.*inside|0.*within|inside.*ci|-0\.15.*<.*0.*<.*0\.20|0.*in.*ci', text_lower):
            calculations_found["part_d_comparison_present"] = True
            evidence.append("Part d: comparison showing μ inside CI present")

        # For part d, look for fail to reject
        if 'd.' in student_answer.lower() or 'part d' in student_answer.lower():
            part_d_start = max(
                student_answer.lower().find('d.') if 'd.' in student_answer.lower() else 0,
                student_answer.lower().find('part d') if 'part d' in student_answer.lower() else 0
            )
            part_d_section = student_answer[part_d_start:]
            if re.search(r'fail\s+to\s+reject', part_d_section.lower()):
                calculations_found["part_d_decision_correct"] = True
                evidence.append("Part d: decision 'Fail to reject H₀' found")

        return {
            "calculations_found": calculations_found,
            "evidence": evidence if evidence else ["No calculations or formulas found"]
        }

    def grade_question_hw7_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade the Hypothesis Testing Decision-Making assignment (HW7_4).
        Task: Determine reject/fail to reject H₀ in four scenarios.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API

        Returns:
            Detailed grading breakdown dictionary
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 5,
                    "component_2_score": 5,
                    "component_3_score": 5,
                    "component_4_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] All decisions correctly made with proper justifications.",
                vibe="Student demonstrates solid understanding of hypothesis testing decision rules.",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "task_description": True,
                            "all_parts_present": True,
                            "df_calculations_present": True,
                            "critical_values_present": True,
                            "decisions_stated": True,
                            "ci_comparisons_present": True
                        },
                        "evidence": ["Test mode - all elements present"]
                    },
                    "calculation_check": {
                        "calculations_found": {
                            "part_a_df_correct": True,
                            "part_a_critical_value_correct": True,
                            "part_a_comparison_present": True,
                            "part_a_decision_correct": True,
                            "part_b_df_correct": True,
                            "part_b_critical_value_correct": True,
                            "part_b_comparison_present": True,
                            "part_b_decision_correct": True,
                            "part_c_comparison_present": True,
                            "part_c_decision_correct": True,
                            "part_d_comparison_present": True,
                            "part_d_decision_correct": True
                        },
                        "evidence": ["Test mode - all calculations present"]
                    }
                }
            )

        formatting_check = self.check_formatting_elements(student_answer)
        calculation_check = self.check_formatting_graphs_and_calculations(student_answer)

        prompt = f"""You are grading a statistics homework assignment on hypothesis testing decision-making.

**TASK DESCRIPTION:**
Determine whether you would reject or fail to reject the null hypothesis in the following situations:
a. t = 2.58, N = 21, two-tailed test at α = 0.05
b. t = 1.99, N = 49, one-tailed test at α = 0.01
c. μ = 47.82, 99% CI = (48.71, 49.28)
d. μ = 0, 95% CI = (-0.15, 0.20)

**EXPECTED SOLUTIONS:**

**Part a: t = 2.58, N = 21, two-tailed test at α = 0.05**
- Step 1: df = n - 1 = 21 - 1 = 20
- Step 2: Find critical value: t* = 2.09 (two-tailed, α = 0.05, df = 20)
- Step 3: Compare: 2.58 > 2.09
- Decision: Reject H₀

**Part b: t = 1.99, N = 49, one-tailed test at α = 0.01**
- Step 1: df = n - 1 = 49 - 1 = 48
- Step 2: Find critical value: t* = 2.41 (one-tailed, α = 0.01, df = 48)
- Step 3: Compare: 1.99 < 2.41
- Decision: Fail to reject H₀

**Part c: μ = 47.82, 99% CI = (48.71, 49.28)**
- Check if μ is inside the CI
- 47.82 is NOT inside (48.71, 49.28) because 47.82 < 48.71
- Decision: Reject H₀

**Part d: μ = 0, 95% CI = (-0.15, 0.20)**
- Check if μ is inside the CI
- 0 is inside (-0.15, 0.20) because -0.15 < 0 < 0.20
- Decision: Fail to reject H₀

**RUBRIC (20 points total, 5 points per part):**

**Component 1: Part a (5 points)**
- 5 points: Correct df (20), correct critical value (≈2.09), correct comparison (2.58 > 2.09),
  correct decision (Reject H₀)
- 4 points: All correct but minor notation issues
- 3 points: Correct decision with some work shown but missing df or critical value
- 2 points: Correct decision but no work shown OR wrong decision with correct work
- 1 point: Attempted but mostly incorrect
- 0 points: Missing or entirely wrong

**Component 2: Part b (5 points)**
- 5 points: Correct df (48), correct critical value (≈2.41), correct comparison (1.99 < 2.41),
  correct decision (Fail to reject H₀)
- 4 points: All correct but minor notation issues
- 3 points: Correct decision with some work shown but missing df or critical value
- 2 points: Correct decision but no work shown OR wrong decision with correct work
- 1 point: Attempted but mostly incorrect
- 0 points: Missing or entirely wrong

**Component 3: Part c (5 points)**
- 5 points: Correctly identifies that 47.82 is NOT inside (48.71, 49.28),
  correct decision (Reject H₀)
- 4 points: Correct decision with clear reasoning
- 3 points: Correct decision but minimal or unclear reasoning
- 2 points: Correct decision but no reasoning OR wrong decision with some reasoning
- 1 point: Attempted but mostly incorrect
- 0 points: Missing or entirely wrong

**Component 4: Part d (5 points)**
- 5 points: Correctly identifies that 0 is inside (-0.15, 0.20),
  correct decision (Fail to reject H₀)
- 4 points: Correct decision with clear reasoning
- 3 points: Correct decision but minimal or unclear reasoning
- 2 points: Correct decision but no reasoning OR wrong decision with some reasoning
- 1 point: Attempted but mostly incorrect
- 0 points: Missing or entirely wrong

**TYPICAL MISTAKES AND PENALTIES:**
- Confusing one-tailed vs two-tailed critical values: deduct 2 points from that part
- Wrong df calculation: deduct 1 point from that part
- Correct decision but no work shown: maximum 3 points for that part
- Wrong direction of comparison but correct final decision: deduct 1 point

**CRITICAL GRADING RULES:**
1. Accept minor variations in critical values from t-tables (±0.02)
2. For parts c and d: reasoning about whether μ is in/out of CI must be clear
3. Decision must be stated clearly (reject/fail to reject)
4. No step system required - student can show work in any reasonable format
5. Total MUST equal exactly 20 points maximum

**STUDENT ANSWER:**
{student_answer}

**AUTOMATIC FORMATTING DETECTION RESULT:**
Elements Found: {formatting_check['elements_found']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC CALCULATION DETECTION RESULT:**
Calculations Found: {calculation_check['calculations_found']}
Evidence: {calculation_check['evidence']}

Return your grading in this exact JSON format:
{{
  "component_1_score": <0-5>,
  "component_1_explanation": "<brief explanation for part a>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<brief explanation for part b>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief explanation for part c>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief explanation for part d>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of hypothesis testing decisions>"
}}"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "formatting_check": formatting_check,
                "calculation_check": calculation_check
            }
        )

        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score"
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, result: dict):
        """
        Print grading results in a formatted way.

        Args:
            result: Dictionary containing grading results
        """
        print("\n" + "=" * 60)
        print("GRADING RESULTS - HW7_4")
        print("Hypothesis Testing Decision-Making")
        print("=" * 60)

        if result.get("component_1_score") is not None:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Part a - two-tailed, α=0.05): {result.get('component_1_score', 'N/A')}/5")
            if result.get('component_1_explanation'):
                print(f"    → {result.get('component_1_explanation')}")

            print(f"  Component 2 (Part b - one-tailed, α=0.01): {result.get('component_2_score', 'N/A')}/5")
            if result.get('component_2_explanation'):
                print(f"    → {result.get('component_2_explanation')}")

            print(f"  Component 3 (Part c - CI comparison, μ outside): {result.get('component_3_score', 'N/A')}/5")
            if result.get('component_3_explanation'):
                print(f"    → {result.get('component_3_explanation')}")

            print(f"  Component 4 (Part d - CI comparison, μ inside): {result.get('component_4_score', 'N/A')}/5")
            if result.get('component_4_explanation'):
                print(f"    → {result.get('component_4_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {result.get('total_points', 'N/A')}/{result.get('max_points', 20)}")
        print(f"PERCENTAGE: {result.get('percentage', 'N/A')}%")

        print("\n" + "=" * 60)
        print("FEEDBACK:")
        print("=" * 60)
        print(textwrap.fill(result.get('feedback', 'No feedback available'), width=60))

        print("\n" + "=" * 60)
        print("THE VIBE:")
        print("=" * 60)
        print(textwrap.fill(result.get('vibe', 'N/A'), width=60))

        if 'error' in result:
            print("\n" + "=" * 60)
            print("ERROR:")
            print("=" * 60)
            print(result.get('error'))
            if 'raw_response' in result:
                print("\nRaw Response:")
                print(result['raw_response'][:500])


if __name__ == "__main__":
    print("Welcome to the Homework AI Evaluator System!")
    print("=" * 60)

    evaluator = HW7_4Evaluator()

    print("=" * 60)
    print("HOMEWORK 7 - QUESTION 7_4 EVALUATOR")
    print("Hypothesis Testing Decision-Making")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION 7_4.")
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

    grading = evaluator.grade_question_hw7_4_answer(student_answer)

    evaluator.print_grading_results(grading)