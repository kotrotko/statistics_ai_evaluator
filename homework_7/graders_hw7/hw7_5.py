""""
hw7_5.py
One-Sample t-Test (One-Tailed) Hypothesis Testing Evaluation
Evaluation method name: def grade_question_hw7_5_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW7_5Evaluator(BaseEvaluator):
    """
    Evaluator for One-Sample t-Test (One-Tailed) Hypothesis Testing (HW7_5).

    Task: Test if college students have MORE stress than the general population
    (μ = 12) using a sample of 25 students (X̄ = 13.11, s = 3.89).

    This is a ONE-TAILED test because the hypothesis is directional ("more than").

    Requires strict adherence to 5-step hypothesis testing process.

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    TASK_DESCRIPTION = "You want to know if college students have more stress in their daily lives than the general population (μ = 12), so you gather data from 25 people to test your hypothesis. Your sample has an average stress score of X̅ = 13.11 and a standard deviation of s = 3.89. Use a 1-sample t-test to see if there is a difference."

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
            r'college\s+students.*more\s+stress',
            r'stress.*general\s+population.*μ\s*=\s*12',
            r'25\s+people',
            r'x̅\s*=\s*13\.11.*s\s*=\s*3\.89|average.*13\.11.*standard\s+deviation.*3\.89'
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
        if re.search(r'95%\s*ci|90%\s*ci|confidence\s+interval|ci\s*=|\(.*,.*\)', student_answer):
            elements_found["confidence_interval_present"] = True
            evidence.append("Confidence interval present")

        # Check for conclusion
        if re.search(r'fail\s+to\s+reject|reject.*h[_\s]*0|not\s+significantly|significantly.*more|significantly.*greater', text_lower):
            elements_found["conclusion_present"] = True
            evidence.append("Statistical conclusion found")

        # Check for APA style reporting
        apa_patterns = [
            r'[x̄x]\s*=\s*13\.11',
            r'μ\s*=\s*12',
            r'9[05]%\s*ci\s*=\s*\(',
            r'm\s*=\s*13\.11'
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
            "one_tailed_identified": False,
            "hypotheses_correct": False,
            "alpha_stated": False,
            "df_correct": False,
            "critical_value_correct": False,
            "se_calculated": False,
            "se_value_correct": False,
            "ci_calculated": False,
            "ci_bounds_reasonable": False,
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

        # Check for one-tailed test mention (CRITICAL - this is directional)
        if re.search(r'one[-\s]tailed|1[-\s]tailed|>|greater|more\s+than|directional', text_lower):
            calculations_found["one_tailed_identified"] = True
            evidence.append("One-tailed test identified (directional hypothesis)")

        # Check for correct hypotheses (H₀: μ = 12 or μ ≤ 12, Hₐ: μ > 12)
        if re.search(r'h[_\s]*0.*[=≤].*12|null.*12', text_lower):
            if re.search(r'h[_\s]*a.*>.*12|alternative.*>.*12|h[_\s]*a.*greater.*12', text_lower):
                calculations_found["hypotheses_correct"] = True
                evidence.append("Hypotheses correctly stated: H₀: μ ≤ 12, Hₐ: μ > 12")

        # Check for alpha stated (default 0.05 if not specified)
        if re.search(r'α\s*=\s*0\.05|alpha\s*=\s*0\.05|α\s*=\s*0\.10|alpha\s*=\s*0\.10', text_lower):
            calculations_found["alpha_stated"] = True
            evidence.append("Alpha level stated")

        # Check for correct df (24 = n-1 = 25-1)
        if re.search(r'df\s*=\s*24|degrees\s+of\s+freedom.*24|n\s*-\s*1\s*=\s*24', text_lower):
            calculations_found["df_correct"] = True
            evidence.append("df = 24 correctly calculated")

        # Check for critical value (one-tailed: t* ≈ 1.711 for α=0.05, df=24)
        if re.search(r't\*?\s*=\s*1\.71[0-9]|critical.*1\.71[0-9]|t\s*=\s*1\.71[0-9]', student_answer):
            calculations_found["critical_value_correct"] = True
            evidence.append("Critical value t* ≈ 1.711 found (one-tailed)")

        # Check for SE calculation
        if re.search(r'se\s*=|standard\s+error\s*=', text_lower):
            calculations_found["se_calculated"] = True
            evidence.append("Standard error calculation present")

        # Check for correct SE value (s/√n = 3.89/√25 = 3.89/5 = 0.778)
        if re.search(r'se\s*=\s*0\.77[0-9]?|se\s*=\s*0\.78|3\.89\s*/\s*√?\s*25|3\.89\s*/\s*5', student_answer):
            calculations_found["se_value_correct"] = True
            evidence.append("SE ≈ 0.778 correctly calculated")

        # Check for CI calculation (for one-tailed, typically 90% CI is used)
        if re.search(r'9[05]%\s*ci|confidence\s+interval|x̄\s*±|13\.11\s*±', text_lower):
            calculations_found["ci_calculated"] = True
            evidence.append("Confidence interval calculation present")

        # Check for reasonable CI bounds (90% CI: 13.11 ± 1.711*0.778 ≈ [11.78, 14.44])
        # OR 95% two-sided: 13.11 ± 2.064*0.778 ≈ [11.50, 14.72]
        if re.search(r'1[01]\.[5-9].*14\.[0-9]|11\.[0-9].*14\.[0-9]', student_answer):
            calculations_found["ci_bounds_reasonable"] = True
            evidence.append("CI bounds appear reasonable")

        # Check if student assessed whether null value is in CI
        if re.search(r'12.*<.*1[34]\.|12.*>.*1[01]\.|12.*in.*ci|12.*not.*in.*ci|ci.*contains.*12|ci.*does\s+not\s+contain', text_lower):
            calculations_found["null_in_ci_assessed"] = True
            evidence.append("Assessment of null value within CI present")

        # Check for correct decision
        # For one-tailed test with X̄=13.11, μ=12, the result is ambiguous:
        # t = (13.11-12)/0.778 = 1.43, which is LESS than 1.711, so FAIL TO REJECT
        # However, if using CI method and 12 is outside CI, then REJECT
        # Accept either decision with proper justification
        if re.search(r'fail\s+to\s+reject|not\s+reject.*h[_\s]*0|not\s+significantly|reject\s+h[_\s]*0', text_lower):
            calculations_found["decision_correct"] = True
            evidence.append("Decision stated (accept both reject/fail to reject with proper work)")

        # Check for APA-style conclusion
        apa_conclusion_patterns = [
            r'x̄\s*=\s*13\.11|m\s*=\s*13\.11',
            r'μ\s*=\s*12',
            r'9[05]%\s*ci\s*=\s*\([^)]+\)',
            r'(not\s+)?significantly.*more|college\s+students'
        ]
        apa_matches = sum(1 for pattern in apa_conclusion_patterns if re.search(pattern, text_lower))
        if apa_matches >= 3:
            calculations_found["apa_conclusion_present"] = True
            evidence.append(f"APA-style conclusion detected (matched {apa_matches}/4 elements)")

        # Check for copy-paste detection
        copy_paste_phrases = [
            r'i\s+want\s+to\s+test\s+whether',
            r'becauser\s+this\s+question',
            r'based\s+on\s+our\s+sample\s+of\s+25'
        ]
        copy_paste_count = sum(1 for pattern in copy_paste_phrases if re.search(pattern, text_lower))
        if copy_paste_count >= 2:
            calculations_found["copy_paste_detected"] = True
            evidence.append(f"WARNING: Possible copy-paste detected ({copy_paste_count} exact phrases)")

        return {
            "calculations_found": calculations_found,
            "evidence": evidence if evidence else ["No calculations or formulas found"]
        }

    def grade_question_hw7_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade the One-Sample t-Test (One-Tailed) Hypothesis Testing assignment (HW7_5).
        Task: Test if college students have MORE stress than general population.

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
                vibe="Student demonstrates solid understanding of one-tailed hypothesis testing.",
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
                            "one_tailed_identified": True,
                            "hypotheses_correct": True,
                            "alpha_stated": True,
                            "df_correct": True,
                            "critical_value_correct": True,
                            "se_calculated": True,
                            "se_value_correct": True,
                            "ci_calculated": True,
                            "ci_bounds_reasonable": True,
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

        prompt = f"""You are grading a statistics homework assignment on one-sample t-test hypothesis testing with a DIRECTIONAL (one-tailed) hypothesis.

**TASK DESCRIPTION:**
You want to know if college students have more stress in their daily lives than the general population (μ = 12), so you gather data from 25 people to test your hypothesis. Your sample has an average stress score of X̅ = 13.11 and a standard deviation of s = 3.89. Use a 1-sample t-test to see if there is a difference.

**CRITICAL NOTE: This is a ONE-TAILED test because the hypothesis asks if students have "MORE" stress (directional hypothesis).**

**EXPECTED SOLUTION WITH 5-STEP PROCESS:**

**Step 1: Select the appropriate statistics**
- One-Sample t-Test
- Purpose: Test whether college students have MORE stress than the general population
- This is a ONE-TAILED test (testing for "more than," which is directional)
- Deduct points if student incorrectly uses two-tailed test

**Step 2: State Hypotheses**
- H₀: μ ≤ 12 (college students have equal or less stress than general population)
- Hₐ: μ > 12 (college students have more stress than general population)
- Alternative acceptable format: H₀: μ = 12, Hₐ: μ > 12
- CRITICAL: The alternative must be ">" not "≠"

**Step 3: State α, calculate df, find the critical value**
- α = 0.05 (default if not specified; accept 0.10 as well)
- df = n - 1 = 25 - 1 = 24
- Critical value (ONE-TAILED): t* = 1.711 (α = 0.05, df = 24)
- For comparison: two-tailed would be 2.064 - deduct points if student uses two-tailed value

**Step 4: Compute the test statistic (including assumptions checking)**
- SE = s / √n = 3.89 / √25 = 3.89 / 5 = 0.778
- Calculate t-statistic: t = (X̅ - μ) / SE = (13.11 - 12) / 0.778 = 1.11 / 0.778 ≈ 1.43
- For CI approach (90% CI for one-tailed at α=0.05):
  - Margin of error = t* × SE = 1.711 × 0.778 ≈ 1.33
  - 90% CI = X̅ ± ME = 13.11 ± 1.33 = [11.78, 14.44]
- Alternative: 95% two-sided CI = 13.11 ± 2.064×0.778 = [11.50, 14.72]

**Step 5: Make the statistical inference**
METHOD 1 - Critical value comparison:
- t-calculated (1.43) < t-critical (1.711)
- Decision: Fail to reject H₀
- Conclusion: Based on our sample of 25 college students, college students do not have significantly more stress (X̅ = 13.11) than the general population mean (μ = 12), 90% CI = [11.78, 14.44].

METHOD 2 - CI method (if using 90% CI):
- Since 12 is inside [11.78, 14.44], fail to reject H₀
- Same conclusion as above

METHOD 3 - CI method (if using 95% two-sided CI):
- Since 12 is inside [11.50, 14.72], fail to reject H₀
- Same conclusion

**Accept either method with proper work shown.**

**RUBRIC (20 points total):**

**Component 1: Task Description Included (1 point)**
- 1 point: Complete task description included at the beginning
- 0 points: Task description missing or incomplete

**Component 2: Step 1 - Test Selection (4 points)**
- 4 points: Correctly identifies one-sample t-test, explains purpose in words, correctly states ONE-TAILED test
- 3 points: Correct test type and purpose, but incorrectly states two-tailed
- 2 points: Correct test type but minimal explanation and wrong tail specification
- 1 point: Test type mentioned but no explanation
- 0 points: Missing or wrong test type

**Component 3: Step 2 - Hypotheses (4 points)**
- 4 points: Both H₀ and Hₐ correctly stated with Hₐ: μ > 12 (one-tailed)
- 3 points: Correct hypotheses but minor notation issues
- 2 points: Uses two-tailed (Hₐ: μ ≠ 12) instead of one-tailed - major error
- 1 point: Hypotheses attempted but incorrect values
- 0 points: Missing or entirely wrong

**Component 4: Step 3 - Alpha, df, Critical Value (4 points)**
- 4 points: α stated, df = 24 calculated correctly, t* ≈ 1.711 found (one-tailed)
- 3 points: All present but uses two-tailed critical value (2.064) instead of one-tailed
- 2 points: Two of three correct
- 1 point: Only one correct or formula shown without values
- 0 points: Missing or all incorrect

**Component 5: Step 4 - Test Statistic & CI (4 points)**
- 4 points: SE correctly calculated (≈0.778), t-statistic or CI calculated, bounds correct
- 3 points: Correct process but minor arithmetic error in bounds (±0.2 tolerance)
- 2 points: SE correct but CI bounds or t-statistic significantly off
- 1 point: Formula present but calculations incomplete
- 0 points: Missing or entirely wrong

**Component 6: Step 5 - Inference & Conclusion (3 points)**
- 3 points: Correctly makes decision based on their work, provides full APA-style conclusion
  with X̅, μ, and CI values in words (accept either reject or fail to reject if work supports it)
- 2 points: Correct decision but incomplete conclusion (missing APA elements or not in words)
- 1 point: Decision stated but no proper conclusion
- 0 points: Wrong decision given their work, or missing

**CRITICAL GRADING RULES:**
1. All 5 steps MUST be explicitly labeled (Step 1, Step 2, etc.). If not labeled: -1 point from Component 1
2. ONE-TAILED vs TWO-TAILED is critical: using two-tailed when should be one-tailed = lose points in Components 2, 3, 4
3. Copy-paste detection: Any exact phrases from examples = -1 point per instance
4. Numbers-only answers without words = deduct 1 point from relevant component
5. Accept minor rounding differences (±0.1) in SE, CI bounds, t-statistic
6. Accept either decision (reject or fail to reject) IF properly justified with their calculations
7. Total MUST equal exactly 20 points maximum

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
  "component_2_explanation": "<brief explanation for step 1 - note if one-tailed vs two-tailed>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief explanation for step 2 - note if hypotheses are one-tailed or two-tailed>",
  "component_4_score": <0-4>,
  "component_4_explanation": "<brief explanation for step 3 - note if critical value is one-tailed or two-tailed>",
  "component_5_score": <0-4>,
  "component_5_explanation": "<brief explanation for step 4>",
  "component_6_score": <0-3>,
  "component_6_explanation": "<brief explanation for step 5>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression of the student's understanding of one-tailed hypothesis testing>",
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
        print("GRADING RESULTS - HW7_5")
        print("One-Sample t-Test (One-Tailed) Hypothesis Testing")
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

    evaluator = HW7_5Evaluator()

    print("=" * 60)
    print("HOMEWORK 7 - QUESTION 7_5 EVALUATOR")
    print("One-Sample t-Test (One-Tailed) Hypothesis Testing")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION 7_5.")
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

    grading = evaluator.grade_question_hw7_5_answer(student_answer)

    evaluator.print_grading_results(grading)