"""
hw7_2.py
Confidence Interval Calculations Around Sample Mean
Evaluation method name: def grade_question_hw7_2_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW7_2Evaluator(BaseEvaluator):
    """
    Evaluator for Confidence Interval Calculations (HW7_2).

    Task: Construct a confidence interval around the sample mean X=25
    for four conditions (a, b, c, d) with varying N, s, confidence levels.

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    TASK_DESCRIPTION = "Construct a confidence interval around the sample mean X=25 for the following conditions: a. N=25, s=15, 95% confidence level, b. N=25, s=15, 90% confidence level, c. s_X=4.5, α=0.05, df=20, d. s=12, df=16"

    def __init__(self):
        """Initialize evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1500
        )

    def check_formatting_elements(self, student_answer: str) -> dict:
        """
        Check if student includes required formatting elements for CI calculation problem.

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
            "ci_bounds_present": False,
            "t_value_mentioned": False,
            "standard_error_mentioned": False
        }

        evidence = []

        # Check for task description
        task_patterns = [
            r'confidence\s+interval.*sample\s+mean',
            r'construct.*confidence\s+interval',
            r'x\s*=?\s*25.*confidence',
            r'sample\s+mean.*25'
        ]
        for pattern in task_patterns:
            if re.search(pattern, text_lower):
                elements_found["task_description"] = True
                evidence.append(f"Found task description: {pattern}")
                break

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

        # Check for CI bounds (two numbers representing lower and upper bound)
        if re.search(r'\d+\.?\d*\s*[,;–\-to]+\s*\d+\.?\d*', text_lower):
            elements_found["ci_bounds_present"] = True
            evidence.append("CI bounds found")
        else:
            evidence.append("CI bounds NOT found")

        # Check for t-value mention
        if re.search(r'\bt[\*\s]?=|\bt[-\s]value|\bt[-\s]critical|t\s*\(', text_lower):
            elements_found["t_value_mentioned"] = True
            evidence.append("t-value mentioned")

        # Check for standard error mention
        if re.search(r'standard\s+error|se\s*=|s\s*/\s*√|s\s*/\s*sqrt', text_lower):
            elements_found["standard_error_mentioned"] = True
            evidence.append("Standard error mentioned")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear formatting elements found"]
        }

    def check_formatting_graphs_and_calculations(self, student_answer: str) -> dict:
        """
        Check if student includes required formulas and calculations for the CI problem.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found calculations and evidence
        """
        text_lower = student_answer.lower()

        calculations_found = {
            "se_formula_present": False,
            "se_part_a_correct": False,
            "se_part_b_correct": False,
            "t_value_part_a_correct": False,
            "t_value_part_b_correct": False,
            "t_value_part_c_correct": False,
            "t_value_part_d_correct": False,
            "ci_part_a_correct": False,
            "ci_part_b_correct": False,
            "ci_part_c_correct": False,
            "ci_part_d_correct": False,
            "part_d_assumption_stated": False
        }

        evidence = []

        # Check for SE formula
        if re.search(r's\s*/\s*√\s*n|s\s*/\s*sqrt\s*\(\s*n|standard\s+error\s*=\s*s\s*/\s*√', text_lower):
            calculations_found["se_formula_present"] = True
            evidence.append("Found SE formula: s / √n")

        # Check for correct SE in parts a and b (SE = 15/√25 = 3.0)
        if re.search(r'15\s*/\s*√?\s*25|15\s*/\s*5|se\s*=\s*3\.?0*\b', student_answer):
            calculations_found["se_part_a_correct"] = True
            calculations_found["se_part_b_correct"] = True
            evidence.append("Found correct SE = 3.0 for parts a and b")

        # Check for correct t* for part a (df=24, 95%: t* ≈ 2.064)
        if re.search(r'2\.06[0-9]|2\.064', student_answer):
            calculations_found["t_value_part_a_correct"] = True
            evidence.append("Found correct t* ≈ 2.064 for part a")

        # Check for correct t* for part b (df=24, 90%: t* ≈ 1.711)
        if re.search(r'1\.71[0-9]|1\.711', student_answer):
            calculations_found["t_value_part_b_correct"] = True
            evidence.append("Found correct t* ≈ 1.711 for part b")

        # Check for correct t* for part c (df=20, α=0.05: t* ≈ 2.086)
        if re.search(r'2\.08[0-9]|2\.086', student_answer):
            calculations_found["t_value_part_c_correct"] = True
            evidence.append("Found correct t* ≈ 2.086 for part c")

        # Check for correct t* for part d (df=16, 95% default: t* ≈ 2.120)
        if re.search(r'2\.12[0-9]|2\.120', student_answer):
            calculations_found["t_value_part_d_correct"] = True
            evidence.append("Found correct t* ≈ 2.120 for part d")

        # Check for correct CI bounds part a ([18.81, 31.19] ±0.5)
        if re.search(r'1[89]\.\d+.*3[01]\.\d+|18\.[5-9]\d*|19\.[0-3]\d*', student_answer):
            calculations_found["ci_part_a_correct"] = True
            evidence.append("Found correct CI bounds for part a ≈ [18.81, 31.19]")

        # Check for correct CI bounds part b ([19.87, 30.13] ±0.5)
        if re.search(r'19\.[5-9]\d*.*30\.[0-5]\d*|19\.8[0-9]|20\.[0-3]\d*', student_answer):
            calculations_found["ci_part_b_correct"] = True
            evidence.append("Found correct CI bounds for part b ≈ [19.87, 30.13]")

        # Check for correct CI bounds part c ([15.61, 34.39] ±0.5)
        if re.search(r'1[56]\.\d+.*3[34]\.\d+|15\.[1-9]\d*|16\.[0-1]\d*', student_answer):
            calculations_found["ci_part_c_correct"] = True
            evidence.append("Found correct CI bounds for part c ≈ [15.61, 34.39]")

        # Check for correct CI bounds part d ([18.83, 31.17] ±0.5)
        if re.search(r'18\.[5-9]\d*.*31\.[0-5]\d*|18\.8[0-9]|19\.[0-3]\d*', student_answer):
            calculations_found["ci_part_d_correct"] = True
            evidence.append("Found correct CI bounds for part d ≈ [18.83, 31.17]")

        # Check for stated assumption in part d
        if re.search(r'assum|default|95\s*%.*confidence|confidence.*95\s*%', text_lower):
            calculations_found["part_d_assumption_stated"] = True
            evidence.append("Found stated assumption for part d")

        return {
            "calculations_found": calculations_found,
            "evidence": evidence if evidence else ["No calculations or formulas found"]
        }

    def grade_question_hw7_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade the Confidence Interval Calculations assignment (HW7_2).
        Task: Construct a confidence interval around X=25 for four conditions.

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
                feedback="[TEST MODE] All four parts calculated correctly.",
                vibe="Student demonstrates solid understanding of confidence interval construction.",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "task_description": True,
                            "part_a_present": True,
                            "part_b_present": True,
                            "part_c_present": True,
                            "part_d_present": True,
                            "ci_bounds_present": True,
                            "t_value_mentioned": True,
                            "standard_error_mentioned": True
                        },
                        "evidence": ["Test mode - all elements present"]
                    },
                    "calculation_check": {
                        "calculations_found": {
                            "se_formula_present": True,
                            "se_part_a_correct": True,
                            "se_part_b_correct": True,
                            "t_value_part_a_correct": True,
                            "t_value_part_b_correct": True,
                            "t_value_part_c_correct": True,
                            "t_value_part_d_correct": True,
                            "ci_part_a_correct": True,
                            "ci_part_b_correct": True,
                            "ci_part_c_correct": True,
                            "ci_part_d_correct": True,
                            "part_d_assumption_stated": True
                        },
                        "evidence": ["Test mode - all calculations present"]
                    }
                }
            )

        formatting_check = self.check_formatting_elements(student_answer)
        calculation_check = self.check_formatting_graphs_and_calculations(student_answer)

        prompt = f"""You are grading a statistics homework assignment on confidence interval construction.

**TASK DESCRIPTION:**
Construct a confidence interval around the sample mean X=25 for the following conditions:
a. N=25, s=15, 95% confidence level
b. N=25, s=15, 90% confidence level
c. s_X=4.5, α=0.05, df=20
d. s=12, df=16

**EXPECTED SOLUTIONS:**

Part a: N=25, s=15, 95% confidence level
- SE = s / √N = 15 / √25 = 15 / 5 = 3.0
- df = 24, t* = 2.064 (two-tailed, 95%)
- Margin of error = 2.064 × 3.0 = 6.19
- CI: [25 − 6.19, 25 + 6.19] = [18.81, 31.19]

Part b: N=25, s=15, 90% confidence level
- SE = 15 / √25 = 3.0
- df = 24, t* = 1.711 (two-tailed, 90%)
- Margin of error = 1.711 × 3.0 = 5.13
- CI: [25 − 5.13, 25 + 5.13] = [19.87, 30.13]
- NOTE: 90% CI is narrower than 95% CI — this is expected

Part c: s_X=4.5, α=0.05, df=20
- SE is already given as s_X = 4.5 — student should use it directly
- t* = 2.086 (two-tailed, α=0.05, df=20)
- Margin of error = 2.086 × 4.5 = 9.39
- CI: [25 − 9.39, 25 + 9.39] = [15.61, 34.39]

Part d: s=12, df=16
- df=16 means N=17, so SE = s / √N = 12 / √17 ≈ 2.91
- Confidence level not given — student must state an assumption (95% is standard default)
- t* = 2.120 (two-tailed, 95%, df=16)
- Margin of error = 2.120 × 2.91 = 6.17
- CI: [25 − 6.17, 25 + 6.17] = [18.83, 31.17]

**RUBRIC (20 points total, 5 points per part):**

**Component 1: Part a (5 points)**
- 5 points: Correct SE (3.0), correct t* (≈2.064), correct CI bounds ≈ [18.81, 31.19] (±0.5 accepted)
- 3 points: Correct process but minor arithmetic error in final bounds
- 2 points: Correct SE but wrong t* value, OR correct t* but wrong SE
- 1 point: Formula set up correctly but calculation not completed
- 0 points: Missing or entirely wrong

**Component 2: Part b (5 points)**
- 5 points: Correct SE (3.0), correct t* (≈1.711), correct CI bounds ≈ [19.87, 30.13] (±0.5 accepted)
- 3 points: Correct process but minor arithmetic error in final bounds
- 2 points: Correct SE but wrong t* value, OR correct t* but wrong SE
- 1 point: Formula set up correctly but calculation not completed
- 0 points: Missing or entirely wrong

**Component 3: Part c (5 points)**
- 5 points: Uses s_X=4.5 directly as SE, correct t* (≈2.086 for df=20, α=0.05),
  correct CI bounds ≈ [15.61, 34.39] (±0.5 accepted)
- 3 points: Correct process but minor arithmetic error in final bounds
- 2 points: Recalculates SE instead of using given s_X directly, OR uses wrong t*
- 1 point: Formula set up correctly but calculation not completed
- 0 points: Missing or entirely wrong

**Component 4: Part d (5 points)**
- 5 points: Correctly derives N=17 from df=16, correct SE (≈2.91), states confidence
  level assumption, correct t* (≈2.120 for 95%), correct CI bounds ≈ [18.83, 31.17] (±0.5 accepted)
- 3 points: Correct process but minor arithmetic error, OR correct bounds but no
  stated assumption about confidence level
- 2 points: Wrong SE derivation but correct t* and process, OR correct SE but wrong t*
- 1 point: Formula set up correctly but calculation not completed
- 0 points: Missing or entirely wrong

**TYPICAL MISTAKES AND PENALTIES:**
- Using z* instead of t*: deduct 2 points from that part
- Wrong df (e.g., using N instead of N−1): deduct 1 point from that part
- Not stating confidence level assumption in part d: deduct 1 point from component 4
- Correct bounds but no work shown: deduct 2 points from that part

**STUDENT ANSWER:**
{student_answer}

**AUTOMATIC FORMATTING DETECTION RESULT:**
Elements Found: {formatting_check['elements_found']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC CALCULATION DETECTION RESULT:**
Calculations Found: {calculation_check['calculations_found']}
Evidence: {calculation_check['evidence']}

**CRITICAL GRADING RULES:**
1. Accept minor rounding differences (±0.5) in final CI bounds
2. Accept any reasonable t* value from a standard t-table (minor table reading differences allowed)
3. For part d: accept any stated confidence level assumption, not only 95%
4. Formula alone without calculation = no full credit for that component
5. Total MUST equal exactly 20 points maximum

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
  "vibe": "<one-sentence overall impression of the student's understanding of confidence interval construction>"
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
        print("GRADING RESULTS - HW7_2")
        print("Confidence Interval Calculations Around Sample Mean")
        print("=" * 60)

        if result.get("component_1_score") is not None:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Part a - 95% CI, N=25): {result.get('component_1_score', 'N/A')}/5")
            if result.get('component_1_explanation'):
                print(f"    → {result.get('component_1_explanation')}")

            print(f"  Component 2 (Part b - 90% CI, N=25): {result.get('component_2_score', 'N/A')}/5")
            if result.get('component_2_explanation'):
                print(f"    → {result.get('component_2_explanation')}")

            print(f"  Component 3 (Part c - given SE, df=20): {result.get('component_3_score', 'N/A')}/5")
            if result.get('component_3_explanation'):
                print(f"    → {result.get('component_3_explanation')}")

            print(f"  Component 4 (Part d - s=12, df=16): {result.get('component_4_score', 'N/A')}/5")
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

    evaluator = HW7_2Evaluator()

    print("=" * 60)
    print("HOMEWORK 7 - QUESTION 7_2 EVALUATOR")
    print("Confidence Interval Calculations Around Sample Mean")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION 7_2.")
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

    grading = evaluator.grade_question_hw7_2_answer(student_answer)

    evaluator.print_grading_results(grading)