"""
hw7_3.py
One-Sample t-Test Hypothesis Testing Evaluation
Evaluation method name: def grade_question_hw7_3_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW7_3Evaluator(BaseEvaluator):
    """
    Evaluator for One-Sample t-Test Hypothesis Testing (HW7_3).

    Task: Test if college students differ from the general population in political
    affiliation (μ = 4.00) using a sample of 150 students (X̄ = 3.76, s = 1.52)
    at α = 0.05 level using a 1-sample t-test.

    Requires strict adherence to 5-step hypothesis testing process.

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    TASK_DESCRIPTION = "You hear that college campuses may differ from the general population in terms of political affiliation, and you want to use hypothesis testing to see if this is true and, if so, how big the difference is. You know that the average political affiliation in the nation is μ = 4.00 on a scale of 1.00 to 7.00, so you gather data from 150 college students across the nation to see if there is a difference. You find that the average score is 3.76 with a standard deviation of 1.52. Use a 1-sample t-test to see if there is a difference at the α = 0.05 level."

    def __init__(self):
        """Initialize evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1500
        )

    def check_formatting_elements(self, student_answer: str) -> dict:
        """
        Check if student includes required formatting elements for hypothesis testing.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "step_1_present": False,
            "step_2_present": False,
            "step_3_present": False,
            "step_4_present": False,
            "step_5_present": False,
            "all_steps_labeled": False,
            "hypotheses_stated": False,
            "test_statistic_present": False,
            "confidence_interval_present": False,
            "conclusion_present": False,
            "apa_style_present": False
        }

        evidence = []

        # Check for task description
        task_patterns = [
            r'college\s+campuses.*differ.*political\s+affiliation',
            r'political\s+affiliation.*μ\s*=\s*4\.00',
            r'150\s+college\s+students',
            r'average\s+score.*3\.76.*standard\s+deviation.*1\.52'
        ]
        task_matches = sum(1 for pattern in task_patterns if re.search(pattern, text_lower))
        if task_matches >= 2:
            elements_found["task_description"] = True
            evidence.append(f"Found task description (matched {task_matches}/4 key phrases)")

        # Check for Step 1
        if re.search(r'step\s*1|step\s*one', text_lower):
            elements_found["step_1_present"] = True
            evidence.append("Step 1 label found")

        # Check for Step 2
        if re.search(r'step\s*2|step\s*two', text_lower):
            elements_found["step_2_present"] = True
            evidence.append("Step 2 label found")

        # Check for Step 3
        if re.search(r'step\s*3|step\s*three', text_lower):
            elements_found["step_3_present"] = True
            evidence.append("Step 3 label found")

        # Check for Step 4
        if re.search(r'step\s*4|step\s*four', text_lower):
            elements_found["step_4_present"] = True
            evidence.append("Step 4 label found")

        # Check for Step 5
        if re.search(r'step\s*5|step\s*five', text_lower):
            elements_found["step_5_present"] = True
            evidence.append("Step 5 label found")

        # Check if all 5 steps are labeled
        if all([
            elements_found["step_1_present"],
            elements_found["step_2_present"],
            elements_found["step_3_present"],
            elements_found["step_4_present"],
            elements_found["step_5_present"]
        ]):
            elements_found["all_steps_labeled"] = True
            evidence.append("All 5 steps explicitly labeled")

        # Check for hypotheses
        if re.search(r'h[_\s]*0|null\s+hypothesis', text_lower) and re.search(r'h[_\s]*a|alternative\s+hypothesis', text_lower):
            elements_found["hypotheses_stated"] = True
            evidence.append("Both null and alternative hypotheses found")

        # Check for test statistic (SE or t-value)
        if re.search(r'se\s*=|standard\s+error|t\s*=|t[-\s]value|t[-\s]statistic', text_lower):
            elements_found["test_statistic_present"] = True
            evidence.append("Test statistic mentioned")

        # Check for confidence interval
        if re.search(r'95%\s*ci|confidence\s+interval|ci\s*=|\(.*,.*\)', student_answer):
            elements_found["confidence_interval_present"] = True
            evidence.append("Confidence interval present")

        # Check for conclusion
        if re.search(r'fail\s+to\s+reject|reject.*h[_\s]*0|not\s+significantly\s+different|significantly\s+different', text_lower):
            elements_found["conclusion_present"] = True
            evidence.append("Statistical conclusion found")

        # Check for APA style reporting (X̄ = value, CI = range, or similar)
        apa_patterns = [
            r'[x̄x]\s*=\s*3\.76',
            r'μ\s*=\s*4\.00',
            r'95%\s*ci\s*=\s*\(',
            r'm\s*=\s*3\.76'
        ]
        apa_matches = sum(1 for pattern in apa_patterns if re.search(pattern, text_lower))
        if apa_matches >= 2:
            elements_found["apa_style_present"] = True
            evidence.append(f"APA-style reporting detected (matched {apa_matches}/4 patterns)")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear formatting elements found"]
        }

    def check_formatting_graphs_and_calculations(self, student_answer: str) -> dict:
        """
        Check if student includes required calculations for the hypothesis test.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found calculations and evidence
        """
        text_lower = student_answer.lower()

        calculations_found = {
            "test_type_identified": False,
            "two_tailed_mentioned": False,
            "hypotheses_correct": False,
            "alpha_stated": False,
            "df_correct": False,
            "critical_value_correct": False,
            "se_calculated": False,
            "se_value_correct": False,
            "ci_calculated": False,
            "ci_bounds_correct": False,
            "null_in_ci_assessed": False,
            "decision_correct": False,
            "apa_conclusion_present": False,
            "copy_paste_detected": False
        }

        evidence = []

        # Check for test type identification
        if re.search(r'one[-\s]sample\s+t[-\s]test|1[-\s]sample\s+t[-\s]test|single[-\s]sample\s+t', text_lower):
            calculations_found["test_type_identified"] = True
            evidence.append("Test type correctly identified as one-sample t-test")

        # Check for two-tailed test mention
        if re.search(r'two[-\s]tailed|2[-\s]tailed|≠|!=|differ', text_lower):
            calculations_found["two_tailed_mentioned"] = True
            evidence.append("Two-tailed test mentioned")

        # Check for correct hypotheses (H₀: μ = 4.00, Hₐ: μ ≠ 4.00)
        if re.search(r'h[_\s]*0.*[=:].*4\.00|null.*4\.00', text_lower):
            if re.search(r'h[_\s]*a.*≠.*4\.00|alternative.*≠.*4\.00|h[_\s]*a.*!=.*4\.00', text_lower):
                calculations_found["hypotheses_correct"] = True
                evidence.append("Hypotheses correctly stated: H₀: μ = 4.00, Hₐ: μ ≠ 4.00")

        # Check for alpha stated
        if re.search(r'α\s*=\s*0\.05|alpha\s*=\s*0\.05', text_lower):
            calculations_found["alpha_stated"] = True
            evidence.append("Alpha = 0.05 stated")

        # Check for correct df (149 = n-1 = 150-1)
        if re.search(r'df\s*=\s*149|degrees\s+of\s+freedom.*149|n\s*-\s*1\s*=\s*149', text_lower):
            calculations_found["df_correct"] = True
            evidence.append("df = 149 correctly calculated")

        # Check for critical value (t* ≈ 1.98 for df=149, α=0.05, two-tailed)
        if re.search(r't\*?\s*=\s*1\.9[78]|critical.*1\.9[78]|t\s*=\s*[±+\-]?\s*1\.9[78]', student_answer):
            calculations_found["critical_value_correct"] = True
            evidence.append("Critical value t* ≈ 1.98 found")

        # Check for SE calculation
        if re.search(r'se\s*=|standard\s+error\s*=', text_lower):
            calculations_found["se_calculated"] = True
            evidence.append("Standard error calculation present")

        # Check for correct SE value (s/√n = 1.52/√150 ≈ 0.124 or 0.12)
        if re.search(r'se\s*=\s*0\.12[0-9]?|1\.52\s*/\s*√?\s*150|1\.52\s*/\s*12\.2', student_answer):
            calculations_found["se_value_correct"] = True
            evidence.append("SE ≈ 0.12 correctly calculated")

        # Check for CI calculation
        if re.search(r'95%\s*ci|confidence\s+interval|x̄\s*±|3\.76\s*±', text_lower):
            calculations_found["ci_calculated"] = True
            evidence.append("Confidence interval calculation present")

        # Check for correct CI bounds (3.52, 4.00 or 3.52, 4.01 approximately)
        # Lower bound: 3.76 - 1.98*0.124 ≈ 3.51-3.52
        # Upper bound: 3.76 + 1.98*0.124 ≈ 4.00-4.01
        if re.search(r'3\.5[0-3].*4\.0[0-1]|lower.*3\.5[0-3].*upper.*4\.0[0-1]', student_answer):
            calculations_found["ci_bounds_correct"] = True
            evidence.append("CI bounds approximately [3.52, 4.01] found")

        # Check if student assessed whether null value is in CI
        if re.search(r'4\.00.*<.*4\.0[0-1]|4\.00.*>.*3\.5[0-3]|brackets.*null|null.*in.*ci|ci.*contains.*4\.00', text_lower):
            calculations_found["null_in_ci_assessed"] = True
            evidence.append("Assessment of null value within CI present")

        # Check for correct decision (fail to reject H₀)
        if re.search(r'fail\s+to\s+reject|not\s+reject.*h[_\s]*0|not\s+significantly\s+different', text_lower):
            calculations_found["decision_correct"] = True
            evidence.append("Correct decision: fail to reject H₀")

        # Check for APA-style conclusion
        apa_conclusion_patterns = [
            r'x̄\s*=\s*3\.76|m\s*=\s*3\.76',
            r'μ\s*=\s*4\.00',
            r'95%\s*ci\s*=\s*\([^)]+\)',
            r'not\s+significantly\s+different'
        ]
        apa_matches = sum(1 for pattern in apa_conclusion_patterns if re.search(pattern, text_lower))
        if apa_matches >= 3:
            calculations_found["apa_conclusion_present"] = True
            evidence.append(f"APA-style conclusion detected (matched {apa_matches}/4 elements)")

        # Check for copy-paste detection (looking for exact phrases from example)
        copy_paste_phrases = [
            r'becauser\s+this\s+question',  # Typo from example
            r'i\s+want\s+to\s+test\s+whether\s+college\s+students\s+differ',
            r'since\s+4\.00\s*<\s*4\.01\s+and\s+4\.00\s*>\s*3\.52',
            r'based\s+on\s+our\s+sample\s+of\s+150\s+college\s+students'
        ]
        copy_paste_count = sum(1 for pattern in copy_paste_phrases if re.search(pattern, text_lower))
        if copy_paste_count >= 2:
            calculations_found["copy_paste_detected"] = True
            evidence.append(f"WARNING: Possible copy-paste detected ({copy_paste_count} exact phrases)")

        return {
            "calculations_found": calculations_found,
            "evidence": evidence if evidence else ["No calculations or formulas found"]
        }

    def grade_question_hw7_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade the One-Sample t-Test Hypothesis Testing assignment (HW7_3).
        Task: Test if college students differ from general population in political affiliation.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API

        Returns:
            Detailed grading breakdown dictionary
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 1,
                    "component_2_score": 4,
                    "component_3_score": 4,
                    "component_4_score": 4,
                    "component_5_score": 4,
                    "component_6_score": 3,
                },
                max_points=20,
                feedback="[TEST MODE] All steps completed with proper structure and calculations.",
                vibe="Student demonstrates solid understanding of hypothesis testing procedure.",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "task_description": True,
                            "all_steps_labeled": True,
                            "hypotheses_stated": True,
                            "test_statistic_present": True,
                            "confidence_interval_present": True,
                            "conclusion_present": True,
                            "apa_style_present": True
                        },
                        "evidence": ["Test mode - all elements present"]
                    },
                    "calculation_check": {
                        "calculations_found": {
                            "test_type_identified": True,
                            "two_tailed_mentioned": True,
                            "hypotheses_correct": True,
                            "alpha_stated": True,
                            "df_correct": True,
                            "critical_value_correct": True,
                            "se_calculated": True,
                            "se_value_correct": True,
                            "ci_calculated": True,
                            "ci_bounds_correct": True,
                            "null_in_ci_assessed": True,
                            "decision_correct": True,
                            "apa_conclusion_present": True,
                            "copy_paste_detected": False
                        },
                        "evidence": ["Test mode - all calculations present"]
                    }
                }
            )

        formatting_check = self.check_formatting_elements(student_answer)
        calculation_check = self.check_formatting_graphs_and_calculations(student_answer)

        prompt = f"""You are grading a statistics homework assignment on one-sample t-test hypothesis testing.

**TASK DESCRIPTION:**
You hear that college campuses may differ from the general population in terms of political affiliation, and you want to use hypothesis testing to see if this is true and, if so, how big the difference is. You know that the average political affiliation in the nation is μ = 4.00 on a scale of 1.00 to 7.00, so you gather data from 150 college students across the nation to see if there is a difference. You find that the average score is 3.76 with a standard deviation of 1.52. Use a 1-sample t-test to see if there is a difference at the α = 0.05 level.

**EXPECTED SOLUTION WITH 5-STEP PROCESS:**

**Step 1: Select the appropriate statistics**
- One-Sample t-Test
- Purpose: Test whether college students differ from the general population for political affiliation
- This is a two-tailed test (testing for "difference," not direction)

**Step 2: State Hypotheses**
- H₀: μ = 4.00 (college students = general population)
- Hₐ: μ ≠ 4.00 (college students ≠ general population)

**Step 3: State α, calculate df, find the critical value**
- α = 0.05 (given)
- df = n - 1 = 150 - 1 = 149
- Critical value: t* = ±1.98 (two-tailed, df = 149, α = 0.05)

**Step 4: Compute the test statistic (including assumptions checking)**
- SE = s / √n = 1.52 / √150 = 1.52 / 12.247 ≈ 0.124 (or 0.12)
- Margin of error = t* × SE = 1.98 × 0.124 ≈ 0.245 (or 0.24)
- 95% CI = X̄ ± (t* × SE) = 3.76 ± 0.245
- Lower bound = 3.76 - 0.245 ≈ 3.52
- Upper bound = 3.76 + 0.245 ≈ 4.00 (or 4.01)
- Answer: 95% CI = (3.52, 4.01)

**Step 5: Make the statistical inference**
- Since 4.00 < 4.01 AND 4.00 > 3.52, the confidence interval brackets the null value
- Decision: Fail to reject H₀
- Conclusion (APA style): Based on our sample of 150 college students, college students are not significantly different in average political affiliation (X̄ = 3.76) from the national population mean (μ = 4.00), 95% CI = (3.52, 4.01).

**RUBRIC (20 points total):**

**Component 1: Task Description Included (1 point)**
- 1 point: Complete task description included at the beginning
- 0 points: Task description missing or incomplete

**Component 2: Step 1 - Test Selection (4 points)**
- 4 points: Correctly identifies one-sample t-test, explains purpose in words, states two-tailed test
- 3 points: Correct test type and purpose, but missing two-tailed specification
- 2 points: Correct test type but minimal explanation
- 1 point: Test type mentioned but no explanation
- 0 points: Missing or wrong test type

**Component 3: Step 2 - Hypotheses (4 points)**
- 4 points: Both H₀ and Hₐ correctly stated (H₀: μ = 4.00, Hₐ: μ ≠ 4.00) with proper symbols
- 3 points: Both hypotheses present but minor notation issues
- 2 points: Only one hypothesis correctly stated
- 1 point: Hypotheses attempted but incorrect values
- 0 points: Missing or entirely wrong

**Component 4: Step 3 - Alpha, df, Critical Value (4 points)**
- 4 points: α = 0.05 stated, df = 149 calculated correctly, t* ≈ 1.98 found
- 3 points: All three present but one minor error (e.g., df = 150 instead of 149)
- 2 points: Two of three correct
- 1 point: Only one correct or formula shown without values
- 0 points: Missing or all incorrect

**Component 5: Step 4 - Test Statistic & CI (4 points)**
- 4 points: SE correctly calculated (≈0.12), margin of error calculated, CI bounds correct (≈3.52, 4.01)
- 3 points: Correct process but minor arithmetic error in bounds (±0.1 tolerance)
- 2 points: SE correct but CI bounds significantly off
- 1 point: Formula present but calculations incomplete
- 0 points: Missing or entirely wrong

**Component 6: Step 5 - Inference & Conclusion (3 points)**
- 3 points: Correctly assesses null value in CI, states "fail to reject H₀", provides full APA-style
  conclusion with X̄, μ, and CI values in words
- 2 points: Correct decision but incomplete conclusion (missing APA elements or not in words)
- 1 point: Correct decision but no proper conclusion
- 0 points: Wrong decision or missing

**CRITICAL GRADING RULES:**
1. All 5 steps MUST be explicitly labeled (Step 1, Step 2, etc.). If not labeled: -1 point from Component 1
2. Copy-paste detection: Any exact phrases from provided example (except task description) = -1 point per instance
3. Numbers-only answers without words = deduct 1 point from relevant component
4. Accept minor rounding differences (±0.1) in SE, CI bounds
5. Accept t* values from 1.96 to 2.00 (table reading variation)
6. Total MUST equal exactly 20 points maximum

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
  "component_1_score": <0-1>,
  "component_1_explanation": "<brief explanation for task description>",
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief explanation for step 1>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief explanation for step 2>",
  "component_4_score": <0-4>,
  "component_4_explanation": "<brief explanation for step 3>",
  "component_5_score": <0-4>,
  "component_5_explanation": "<brief explanation for step 4>",
  "component_6_score": <0-3>,
  "component_6_explanation": "<brief explanation for step 5>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of hypothesis testing>",
  "copy_paste_penalty": <number of points deducted for copy-paste if any>
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
                "component_4_score",
                "component_5_score",
                "component_6_score"
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
        print("GRADING RESULTS - HW7_3")
        print("One-Sample t-Test Hypothesis Testing")
        print("=" * 60)

        if result.get("component_1_score") is not None:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Task Description): {result.get('component_1_score', 'N/A')}/1")
            if result.get('component_1_explanation'):
                print(f"    → {result.get('component_1_explanation')}")

            print(f"  Component 2 (Step 1 - Test Selection): {result.get('component_2_score', 'N/A')}/4")
            if result.get('component_2_explanation'):
                print(f"    → {result.get('component_2_explanation')}")

            print(f"  Component 3 (Step 2 - Hypotheses): {result.get('component_3_score', 'N/A')}/4")
            if result.get('component_3_explanation'):
                print(f"    → {result.get('component_3_explanation')}")

            print(f"  Component 4 (Step 3 - α, df, CV): {result.get('component_4_score', 'N/A')}/4")
            if result.get('component_4_explanation'):
                print(f"    → {result.get('component_4_explanation')}")

            print(f"  Component 5 (Step 4 - Test Statistic & CI): {result.get('component_5_score', 'N/A')}/4")
            if result.get('component_5_explanation'):
                print(f"    → {result.get('component_5_explanation')}")

            print(f"  Component 6 (Step 5 - Inference & Conclusion): {result.get('component_6_score', 'N/A')}/3")
            if result.get('component_6_explanation'):
                print(f"    → {result.get('component_6_explanation')}")

            if result.get('copy_paste_penalty', 0) > 0:
                print(f"\n  ⚠️  COPY-PASTE PENALTY: -{result.get('copy_paste_penalty')} points")

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

    evaluator = HW7_3Evaluator()

    print("=" * 60)
    print("HOMEWORK 7 - QUESTION 7_3 EVALUATOR")
    print("One-Sample t-Test Hypothesis Testing")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION 7_3.")
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

    grading = evaluator.grade_question_hw7_3_answer(student_answer)

    evaluator.print_grading_results(grading)