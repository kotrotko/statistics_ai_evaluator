"""
hw5_3.py
Sampling Distribution and Z-Score Analysis Evaluator
Evaluation method name: def grade_question_hw5_3_answer
"""
import re
import textwrap

from config import BaseEvaluator


class HW5_3Evaluator(BaseEvaluator):
    """
    Evaluator for Sampling Distribution and Z-Score Analysis Question.
    Evaluation method name: def grade_question_hw5_3_answer

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    TASK_DESCRIPTION = "For a population with a mean of 75 and a standard deviation of 12, what proportion of sample means of size n = 16 fall above 82"

    def __init__(self):
        """Initialize evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1500
        )

    def check_formatting_elements(self, student_answer: str) -> dict:
        """
        Check if student includes required formatting elements for sampling distribution problem.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()
        task_lower = self.TASK_DESCRIPTION.lower()

        elements_found = {
            "task_description": False,
            "task_number_mentioned": False,
            "part_calculation_mentioned": False,
            "part_interpretation_mentioned": False,
            "formula_section_present": False,
            "calculation_section_present": False,
            "answer_section_present": False
        }

        evidence = []

        # Check for task description (must be included exactly as written)
        task_patterns = [
            r'population.*mean.*75.*standard\s+deviation.*12',
            r'mean\s*=?\s*75.*standard\s+deviation\s*=?\s*12',
            r'μ\s*=\s*75.*σ\s*=\s*12',
            r'proportion.*sample\s+means.*size.*n\s*=\s*16.*fall\s+above\s+82',
            r'sample\s+means.*n\s*=?\s*16.*above\s+82',
            r'what\s+proportion.*sample\s+means'
        ]
        for pattern in task_patterns:
            if re.search(pattern, text_lower):
                elements_found["task_description"] = True
                evidence.append(f"Found task description: {pattern}")
                break

        # Check for setup/formula section
        setup_patterns = [
            r'(given|known|setup|set\s+up|information)',
            r'(identify|identifying)\s+(the\s+)?(sampling|distribution)',
            r'(formula|formulas|equation)',
            r'standard\s+error'
        ]
        for pattern in setup_patterns:
            if re.search(pattern, text_lower):
                elements_found["part_setup_mentioned"] = True
                evidence.append(f"Found setup section indicator: {pattern}")
                break

        # Check for calculation section
        calc_patterns = [
            r'calculat|comput|solving|solve',
            r'step\s+\d',
            r'σ_?[mx̄]?\s*=|se\s*=|standard\s+error\s*='
        ]
        for pattern in calc_patterns:
            if re.search(pattern, text_lower):
                elements_found["part_calculation_mentioned"] = True
                evidence.append(f"Found calculation section: {pattern}")
                break

        # Check for interpretation/answer section
        interp_patterns = [
            r'(proportion|probability|p\s*\()',
            r'(interpret|therefore|conclusion|thus)',
            r'(above|greater\s+than)\s+(82|the\s+value)',
            r'(percent|%)\s+(of\s+)?(sample\s+means)'
        ]
        for pattern in interp_patterns:
            if re.search(pattern, text_lower):
                elements_found["part_interpretation_mentioned"] = True
                evidence.append(f"Found interpretation section: {pattern}")
                break

        # Check for formula section presence
        formula_patterns = [
            r'σ\s*/\s*√',
            r'sigma\s*/\s*sqrt',
            r'σ\s*/\s*\(?n\^?0?\.?5\)?',
            r'z\s*=\s*\(?[mx̄μ]'
        ]
        for pattern in formula_patterns:
            if re.search(pattern, text_lower):
                elements_found["formula_section_present"] = True
                evidence.append(f"Found formula section: {pattern}")
                break

        # Check for calculation section presence (numeric work)
        if re.search(r'12\s*/\s*√?\s*16|12\s*/\s*4|σ_?[mx̄]\s*=\s*3', student_answer):
            elements_found["calculation_section_present"] = True
            evidence.append("Found standard error calculation with numbers")

        # Check for final answer section
        answer_patterns = [
            r'(answer|result|final|proportion)\s*[:=]',
            r'p\s*[=≈]\s*0\.\d+',
            r'\d+\.\d+\s*%?\s*(of|sample)',
            r'0\.\d{4}'
        ]
        for pattern in answer_patterns:
            if re.search(pattern, text_lower):
                elements_found["answer_section_present"] = True
                evidence.append(f"Found answer section: {pattern}")
                break

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear formatting elements found"]
        }

    def check_formatting_graphs_and_calculations(self, student_answer: str) -> dict:
        """
        Check if student includes required formulas and calculations for the sampling distribution problem.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found calculations and evidence
        """
        text_lower = student_answer.lower()

        calculations_found = {
            "sampling_distribution_identified": False,
            "standard_error_formula": False,
            "standard_error_correct": False,
            "z_score_formula": False,
            "z_score_correct": False,
            "standard_error_value": False,
            "z_value_correct": False,
            "right_tail_identified": False,
            "probability_value_correct": False,
            "interpretation_stated": False
        }

        evidence = []

        # Check for sampling distribution identification
        sampling_patterns = [
            r'sampling\s+distribution\s+of\s+(the\s+)?mean',
            r'distribution\s+of\s+sample\s+means',
            r'central\s+limit\s+theorem',
            r'standard\s+error\s+of\s+(the\s+)?mean',
            r'σ_?[mx̄]|se\s*=|σ/√n'
        ]
        for pattern in sampling_patterns:
            if re.search(pattern, text_lower):
                calculations_found["sampling_distribution_identified"] = True
                evidence.append(f"Found sampling distribution identification: {pattern}")
                break

        # Check for standard error formula
        se_formula_patterns = [
            r'σ\s*/\s*√\s*n',
            r'σ\s*/\s*sqrt\s*\(\s*n\s*\)',
            r'standard\s+error\s*=\s*σ\s*/\s*√',
            r'se\s*=\s*σ\s*/\s*√',
            r'σ_?[mx̄]\s*=\s*σ\s*/\s*√',
            r'12\s*/\s*√\s*16'
        ]
        for pattern in se_formula_patterns:
            if re.search(pattern, text_lower):
                calculations_found["standard_error_formula"] = True
                evidence.append(f"Found standard error formula: {pattern}")
                break

        # Check for correct standard error formula (σ / √n specifically)
        if re.search(r'σ\s*/\s*√\s*n|standard\s+error\s*=\s*σ\s*/\s*√\s*n', text_lower):
            calculations_found["standard_error_correct"] = True
            evidence.append("Found correct standard error formula: σ / √n")

        # Check for z-score formula
        z_formula_patterns = [
            r'z\s*=\s*\(?[mx̄μ]?\s*[-−]\s*μ\s*\)?\s*/\s*\(?σ',
            r'z\s*=\s*\(?\s*\d+\s*[-−]\s*\d+\s*\)?\s*/\s*\(?σ',
            r'z\s*=\s*\(?\s*x̄?\s*[-−]\s*μ\s*\)?\s*/\s*\(?σ\s*/\s*√',
            r'z\s*=\s*\(?m\s*[-−]\s*μ\s*\)?\s*/\s*se',
            r'z[-\s]score\s*formula'
        ]
        for pattern in z_formula_patterns:
            if re.search(pattern, text_lower):
                calculations_found["z_score_formula"] = True
                evidence.append(f"Found z-score formula: {pattern}")
                break

        # Check for correct z-score formula setup
        if re.search(r'z\s*=\s*\(?\s*[mx̄]?\s*[-−]\s*μ\s*\)?\s*/\s*\(?\s*σ\s*/\s*√\s*n', text_lower):
            calculations_found["z_score_correct"] = True
            evidence.append("Found correct z-score formula: z = (M − μ) / (σ / √n)")

        # Check for standard error value = 3
        if re.search(r'(standard\s+error|se|σ_?[mx̄])\s*=\s*3\.?0*\b|12\s*/\s*4\s*=\s*3', student_answer):
            calculations_found["standard_error_value"] = True
            evidence.append("Found correct standard error value = 3")

        # Check for z-value = 2.33 (or close: 7/3 ≈ 2.33)
        if re.search(r'z\s*=\s*2\.3[23]|z\s*=\s*7\s*/\s*3', student_answer):
            calculations_found["z_value_correct"] = True
            evidence.append("Found correct z-value ≈ 2.33")

        # Check for right-tail identification
        right_tail_patterns = [
            r'above|right[\s-]tail|upper\s+tail',
            r'p\s*\(\s*[zx̄m]\s*>\s*(2\.3[23]|82)',
            r'proportion.*above',
            r'greater\s+than.*82'
        ]
        for pattern in right_tail_patterns:
            if re.search(pattern, text_lower):
                calculations_found["right_tail_identified"] = True
                evidence.append(f"Found right-tail identification: {pattern}")
                break

        # Check for probability value (correct: ~0.0099 or 0.01)
        if re.search(r'0\.009[5-9]|0\.010[0-5]|0\.01\b|1\s*%|0\.0099', student_answer):
            calculations_found["probability_value_correct"] = True
            evidence.append("Found correct probability value (~0.0099 or 0.01)")

        # Check for interpretation
        interp_patterns = [
            r'(proportion|probability|percent)\s+of\s+sample\s+means',
            r'(about|approximately|roughly)\s+\d+(\.\d+)?\s*%\s+of\s+sample',
            r'sample\s+means.*above\s+82',
            r'(this\s+means|therefore|thus|conclusion)',
            r'(represent|indicates?|shows?)\s+(the\s+)?proportion'
        ]
        for pattern in interp_patterns:
            if re.search(pattern, text_lower):
                calculations_found["interpretation_stated"] = True
                evidence.append(f"Found interpretation: {pattern}")
                break

        return {
            "calculations_found": calculations_found,
            "evidence": evidence if evidence else ["No calculations or formulas found"]
        }

    def grade_question_hw5_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade the sampling distribution and z-score analysis assignment.
        Evaluation method name: def grade_question_hw5_3_answer

        Args:
            student_answer: The student's response text
            test_mode: If True, return mock results for testing

        Returns:
            Dictionary containing grading results
        """
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 1,
                    "component_2_score": 6,
                    "component_3_score": 6,
                    "component_4_score": 7,
                },
                max_points=20,
                feedback="Test mode feedback for sampling distribution z-score task.",
                vibe="Test mode vibe assessment",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "task_description": True,
                            "part_setup_mentioned": True,
                            "part_calculation_mentioned": True,
                            "part_interpretation_mentioned": True,
                            "formula_section_present": True,
                            "calculation_section_present": True,
                            "answer_section_present": True
                        },
                        "evidence": ["Test mode - all elements present"]
                    },
                    "calculation_check": {
                        "calculations_found": {
                            "sampling_distribution_identified": True,
                            "standard_error_formula": True,
                            "standard_error_correct": True,
                            "z_score_formula": True,
                            "z_score_correct": True,
                            "standard_error_value": True,
                            "z_value_correct": True,
                            "right_tail_identified": True,
                            "probability_value_correct": True,
                            "interpretation_stated": True
                        },
                        "evidence": ["Test mode - all calculations present"]
                    }
                }
            )

        formatting_check = self.check_formatting_elements(student_answer)
        calculation_check = self.check_formatting_graphs_and_calculations(student_answer)

        prompt = f"""You are grading a statistics homework assignment on sampling distributions and z-scores.

**TASK DESCRIPTION (must appear exactly as written):**
For a population with a mean of 75 and a standard deviation of 12, what proportion of sample means of size n = 16 fall above 82

**EXPECTED SOLUTION:**
- Given: μ = 75, σ = 12, n = 16, M = 82
- Standard Error: σ_M = σ / √n = 12 / √16 = 12 / 4 = 3
- Z-score: z = (M − μ) / (σ / √n) = (82 − 75) / 3 = 7 / 3 ≈ 2.33
- Right-tail probability: P(z > 2.33) ≈ 0.0099 (approximately 0.01 or ~1%)
- Interpretation: Approximately 0.99% (or ~1%) of sample means of size n=16 fall above 82.

**RUBRIC (20 points total):**

**Component 1: Task Description (1 point)**
- 1 point: Task description is included exactly and correctly
- 0 points: Task description is missing or incorrect

**Component 2: Setup and Formulas (6 points)**
This component checks three sub-elements:
- Correct identification of sampling distribution of the mean (uses standard error): 1 point
- Standard error formula (σ / √n): max 3 points
  * Correct formula (σ / √n): 3 points
  * Formula provided but incorrect version: 1 point
  * Not provided: 0 points
- Z-score formula z = (M − μ) / (σ / √n): max 3 points
  * Correct setup: 3 points
  * Formula provided but incorrect version: 1 point
  * Not provided: 0 points

**Component 3: Calculation Procedure (6 points)**
- Correct calculation of standard error (result = 3): 3 points
- Correct calculation of z-value using M=82 (result ≈ 2.33): 3 points
Adjustments:
  * Minor arithmetic error with correct procedure: −1 point total
  * Major computational error showing misunderstanding: −1 point per error (not below 0)
  * No calculation provided, only final answer: 1 point total for this component
  * Neither calculation nor answer provided: 0 points

**Component 4: Final Probability and Interpretation (7 points)**
- Correct identification of right-tail probability (proportion above 82): 3 points
- Correct or very close probability value from z-table (~0.0099 or 0.01): 3 points
- Clear interpretation stating this represents proportion of sample means above 82: 1 point
Adjustments:
  * Probability value correct but method unclear: −1 point
  * Tail direction incorrect: −1 point
  * Final answer given without interpretation: −1 point
  * Maximum for this component: 7 points

**TOTAL: 20 points strictly.**

**STUDENT ANSWER:**
{student_answer}

**AUTOMATIC FORMATTING DETECTION RESULT:**
Elements Found: {formatting_check['elements_found']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC CALCULATION DETECTION RESULT:**
Calculations Found: {calculation_check['calculations_found']}
Evidence: {calculation_check['evidence']}

**ORIGINALITY CHECK — CRITICAL RULE:**
Before grading, scan the student answer for signs of copied or AI-generated text. Indicators include:
- Unnaturally polished, textbook-like phrasing without any personal working style
- Multiple consecutive lines that could have been pasted from an AI tool or textbook
- Lack of any personal notation, scratched work, or natural student errors
- Suspicious uniformity in formatting/language that suggests copy-paste

If you detect copied or AI-generated text (anything beyond the task description), set ALL component scores to 0 and set the feedback to exactly:
"Due to originality concern, your points are frozen. You can get them back if you provide oral explanation for this paper."
Do not evaluate further if this is triggered.

Additionally, deduct 1 point for each line of copy-pasted content detected (excluding task description). Apply this penalty to the relevant component before capping at 0.

**CRITICAL GRADING RULES:**
1. Component 1: Only 1 point if the exact task description is present. 0 otherwise.
2. Component 2: Check each sub-element independently. Sampling distribution identified (1pt) + SE formula (0/1/3 pts) + Z formula (0/1/3 pts). Max 6.
3. Component 3: Standard error calculation (3 pts) + z-value calculation (3 pts). Apply adjustments as stated.
4. Component 4: Right-tail ID (3 pts) + probability value (3 pts) + interpretation (1 pt). Apply penalties. Max 7.
5. Be strict: formula alone without calculation = no credit for Component 3. Final answer alone without formula = no credit for Component 2.
6. Minor rounding is acceptable (e.g., z = 2.33 is acceptable).
7. Total = Component 1 + Component 2 + Component 3 + Component 4. Must equal exactly 20 max.

**SCORING PROCESS:**
1. Originality check first — if plagiarism detected, score everything 0 with the frozen points message.
2. Component 1 (Task Description): 1 if task description present, 0 otherwise.
3. Component 2 (Setup & Formulas):
   - Sampling distribution identified? (+1 or 0)
   - Standard error formula correct (σ/√n)? (+3), incorrect formula (+1), missing (+0)
   - Z-score formula correct (z=(M−μ)/(σ/√n))? (+3), incorrect formula (+1), missing (+0)
   Total: 0–6
4. Component 3 (Calculations):
   - Standard error calculated correctly (= 3)? (+3 or adjusted)
   - Z-value calculated correctly (≈ 2.33)? (+3 or adjusted)
   - Apply adjustment rules. Total: 0–6
5. Component 4 (Probability & Interpretation):
   - Right-tail identified? (+3 or adjusted)
   - Probability value correct (~0.0099)? (+3 or adjusted)
   - Interpretation stated? (+1 or 0)
   - Apply penalties. Total: 0–7
6. Grand total = sum of all components. Max = 20.

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- States whether originality check passed or triggered the frozen points message
- For Component 1: Whether task description is present exactly as written
- For Component 2: Covers sampling distribution identification, standard error formula (correct/incorrect/missing), z-score formula (correct/incorrect/missing)
- For Component 3: Covers standard error calculation (correct value = 3?), z-value calculation (correct ≈ 2.33?), any arithmetic errors
- For Component 4: Covers right-tail identification, probability value accuracy, interpretation quality
- Notes any deductions applied and why
- Is constructive and encourages showing complete work with formulas and reasoning

Return your grading in this exact JSON format:
{{
  "component_1_score": <0-1>,
  "component_1_explanation": "<State whether task description is present exactly as written>",
  "component_2_score": <0-6>,
  "component_2_explanation": "<Cover: sampling distribution identified (yes/no), SE formula (correct/incorrect/missing), z-formula (correct/incorrect/missing), justify score>",
  "component_3_score": <0-6>,
  "component_3_explanation": "<Cover: SE calculation (value and correctness), z-value calculation (value and correctness), any errors or adjustments applied>",
  "component_4_score": <0-7>,
  "component_4_explanation": "<Cover: right-tail identification, probability value accuracy, interpretation quality, penalties applied>",
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<comprehensive narrative covering all components>",
  "vibe": "<one-sentence assessment of student's statistical understanding and work quality>"
}}"""

        # return self.grade_with_prompt(student_answer, prompt)

        result = self.grade_with_prompt(
            student_answer=student_answer, # TODO: Check and remove
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
        print("SAMPLING DISTRIBUTION Z-SCORE ANALYSIS - GRADING RESULTS")
        print("=" * 60)

        print(f"\nComponent 1 - Task Description: {result['component_1_score']}/1")
        if result.get('component_1_explanation'):
            print(f"  {result['component_1_explanation']}")

        print(f"\nComponent 2 - Setup and Formulas: {result['component_2_score']}/6")
        if result.get('component_2_explanation'):
            print(f"  {result['component_2_explanation']}")

        print(f"\nComponent 3 - Calculation Procedure: {result['component_3_score']}/6")
        if result.get('component_3_explanation'):
            print(f"  {result['component_3_explanation']}")

        print(f"\nComponent 4 - Final Probability and Interpretation: {result['component_4_score']}/7")
        if result.get('component_4_explanation'):
            print(f"  {result['component_4_explanation']}")

        print("\n" + "-" * 60)
        print(f"TOTAL SCORE: {result['total_points']}/{result['max_points']} ({result['percentage']:.1f}%)")
        print("-" * 60)

        print("\nFEEDBACK:")
        print(textwrap.fill(result['feedback'], width=60))

        print("\nVIBE CHECK:")
        print(textwrap.fill(result['vibe'], width=60))

        print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    print("Welcome to the Homework AI Evaluator System!")
    print("=" * 60)

    evaluator = HW5_3Evaluator()

    print("=" * 60)
    print("HOMEWORK 5 - QUESTION 5_3 EVALUATOR")
    print("Z-Score Proportion Calculation for Given Population")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION 5_3.")
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

    grading = evaluator.grade_question_hw5_3_answer(student_answer)

    evaluator.print_grading_results(grading)

# TODO: Check and remove
# def main():
#     """Test the evaluator with a sample student answer."""
#     evaluator = HW5_3Evaluator()
#
#     print("=" * 60)
#     print("HOMEWORK 5.3 EVALUATOR")
#     print("Sampling Distribution and Z-Score Analysis")
#     print("=" * 60)
#     print("\nPlease enter the student's answer to HOMEWORK 5.3.")
#     print("(Press Enter twice when finished, or type 'END' on a new line)\n")
#
#     lines = []
#     while True:
#         line = input()
#         if line.strip().upper() == "END":
#             break
#         lines.append(line)
#         if len(lines) >= 2 and lines[-1] == "" and lines[-2] == "":
#             lines = lines[:-2]
#             break
#
#     student_answer = "\n".join(lines)
#
#     if not student_answer.strip():
#         print("\n❌ Error: No answer provided. Exiting.")
#         exit(1)
#
#     print("\n" + "=" * 60)
#     print("EVALUATING...")
#     print("=" * 60)
#
#     result = evaluator.grade_question_hw5_3_answer(sample_answer)
#     evaluator.print_grading_results(result)
#
#
# if __name__ == "__main__":
#     main()
#
