"""
hw3_5.py
Sample Mean and Sample Standard Deviation Evaluator
"""

import re
import textwrap

from config import BaseEvaluator


class HW3_5Evaluator(BaseEvaluator):
    """
    Evaluator for Sample Mean and Sample Standard Deviation Question.

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    def __init__(self):
        """Initialize evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1500
        )

        # Dataset for this exercise
        self.dataset = [-8, -4, -7, -6, -8, -5, -7, -9, -2, 0]

        # Compute expected values internally
        self.expected_mean = self._compute_sample_mean(self.dataset)
        self.expected_sd = self._compute_sample_sd(self.dataset)

    def _compute_sample_mean(self, data: list) -> float:
        """
        Compute sample mean.

        Args:
            data: List of numerical values

        Returns:
            Sample mean
        """
        return sum(data) / len(data)

    def _compute_sample_sd(self, data: list) -> float:
        """
        Compute sample standard deviation using the standard formula.
        Formula: s = sqrt(Σ(x - x̄)² / (n-1))

        Args:
            data: List of numerical values

        Returns:
            Sample standard deviation
        """
        n = len(data)
        mean = self._compute_sample_mean(data)

        # Calculate sum of squared deviations
        sum_squared_deviations = sum((x - mean) ** 2 for x in data)

        # Sample variance (divide by n-1)
        variance = sum_squared_deviations / (n - 1)

        # Sample standard deviation
        return variance ** 0.5

    def _round_half_up(self, value: float, decimals: int = 2) -> float:
        """
        Round value to specified decimal places using round-half-up method.

        Args:
            value: Value to round
            decimals: Number of decimal places

        Returns:
            Rounded value
        """
        from decimal import Decimal, ROUND_HALF_UP

        decimal_value = Decimal(str(value))
        rounded = decimal_value.quantize(
            Decimal(10) ** -decimals,
            rounding=ROUND_HALF_UP
        )
        return float(rounded)

    def _values_match_after_rounding(self, value1: float, value2: float, decimals: int = 2) -> bool:
        """
        Check if two values match after rounding to specified decimal places.

        Args:
            value1: First value
            value2: Second value
            decimals: Number of decimal places

        Returns:
            True if values match after rounding
        """
        rounded1 = self._round_half_up(value1, decimals)
        rounded2 = self._round_half_up(value2, decimals)
        return rounded1 == rounded2

    def check_formatting_elements(self, student_answer: str) -> dict:
        """
        Check if student includes required formatting elements.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "dataset_shown": False,
            "incorrect_notation": False,
            "approximate_symbol_used": False
        }

        evidence = []

        # Check for task description
        task_patterns = [
            r'task\s+10',
            r'exercise\s+10',
            r'problem\s+10',
            r'compute.*mean.*standard\s+deviation',
            r'calculate.*mean.*standard\s+deviation'
        ]
        for pattern in task_patterns:
            if re.search(pattern, text_lower):
                elements_found["task_description"] = True
                evidence.append("Found task description")
                break

        # Check if dataset is shown
        if re.search(r'-8.*-4.*-7.*-6.*-8.*-5.*-7.*-9.*-2.*0', student_answer.replace('\n', ' ').replace(',', ' ')):
            elements_found["dataset_shown"] = True
            evidence.append("Dataset is explicitly shown")

        # Check for incorrect notation (X instead of X̄)
        if re.search(r'\bX\s*=(?!\s*individual)', student_answer) and not re.search(r'X̄|\\bar\{X\}|x̄|\\bar\{x\}|mean',
                                                                                    text_lower):
            elements_found["incorrect_notation"] = True
            evidence.append("WARNING: Potentially incorrect notation detected (X without bar for mean)")

        # Check for approximate symbol (≈)
        if '≈' in student_answer:
            elements_found["approximate_symbol_used"] = True
            evidence.append("WARNING: Approximate symbol (≈) used instead of rounded values")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear formatting elements found"]
        }

    def check_mean_calculation(self, student_answer: str) -> dict:
        """
        Check if student includes required mean calculation elements.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        calculations_found = {
            "mean_formula_stated": False,
            "mean_formula_used": False,
            "mean_calculation_shown": False,
            "mean_correct": False
        }

        evidence = []

        # Check for mean formula stated
        mean_formula_patterns = [
            r'mean\s*=\s*Σ.*\/.*n',
            r'x̄\s*=\s*Σ.*\/.*n|\\bar\{x\}\s*=',
            r'μ\s*=\s*Σ.*\/.*n',
            r'mean\s*=\s*sum.*\/.*n',
            r'average\s*=.*sum.*divided.*by',
            r'formula.*mean'
        ]
        for pattern in mean_formula_patterns:
            if re.search(pattern, text_lower) or re.search(pattern, student_answer):
                calculations_found["mean_formula_stated"] = True
                evidence.append("Mean formula is explicitly stated")
                break

        # Check if formula is used in calculations (showing the sum)
        if re.search(r'(-8.*-4.*-7.*-6.*-8.*-5.*-7.*-9.*-2.*0)|sum.*=.*-56|Σ.*=.*-56',
                     student_answer.replace('\n', ' ')):
            calculations_found["mean_formula_used"] = True
            evidence.append("Mean formula is demonstrated in calculations")

        # Check for calculation steps
        calc_patterns = [
            r'-56.*\/.*10',
            r'sum.*=.*-56',
            r'Σ.*=.*-56',
            r'total.*=.*-56'
        ]
        for pattern in calc_patterns:
            if re.search(pattern, student_answer):
                calculations_found["mean_calculation_shown"] = True
                evidence.append("Mean calculation steps are shown")
                break

            # Check for correct answer
            # Extract student's SD value and compare with expected after rounding
                sd_value_pattern = r'(?:standard\s+deviation|s|sd)\s*=\s*([0-9]+\.?[0-9]*)'
                sd_match = re.search(sd_value_pattern, text_lower)
                if sd_match:
                    try:
                        student_sd = float(sd_match.group(1))
                        # Note: Actual validation will be done by the LLM with proper rounding
                        calculations_found["sd_correct"] = True
                        evidence.append(f"SD value found: {student_sd}")
                    except ValueError:
                        pass
        return {
            "calculations_found": calculations_found,
            "evidence": evidence if evidence else ["No mean calculation elements found"]
        }

    def check_sd_calculation(self, student_answer: str) -> dict:
        """
        Check if student includes required standard deviation calculation elements.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        calculations_found = {
            "sd_formula_stated": False,
            "sd_formula_used": False,
            "sd_calculation_shown": False,
            "sd_correct": False
        }

        evidence = []

        # Check for SD formula stated
        sd_formula_patterns = [
            r's\s*=\s*√|s\s*=\s*sqrt',
            r'standard\s+deviation\s*=\s*√',
            r'√\s*\[?\s*Σ.*\(.*x.*-.*mean.*\)[²2].*\/.*\(.*n.*-.*1.*\)',
            r's\s*=\s*√\s*\[?\s*variance',
            r'formula.*standard\s+deviation',
            r'sd\s*=.*√.*Σ'
        ]
        for pattern in sd_formula_patterns:
            if re.search(pattern, text_lower) or re.search(pattern, student_answer):
                calculations_found["sd_formula_stated"] = True
                evidence.append("Standard deviation formula is explicitly stated")
                break

        # Check if formula is used (showing deviations or variance calculation)
        deviation_patterns = [
            r'\(.*-8.*-.*-5\.6.*\)[²2]|\(.*-8.*\+.*5\.6.*\)[²2]',
            r'squared.*deviation',
            r'Σ.*\(.*x.*-.*x̄.*\)[²2]',
            r'variance.*=.*[0-9]+\.[0-9]+'
        ]
        for pattern in deviation_patterns:
            if re.search(pattern, student_answer.replace(' ', '')):
                calculations_found["sd_formula_used"] = True
                evidence.append("SD formula is demonstrated in calculations")
                break

        # Check for calculation steps
        calc_patterns = [
            r'variance',
            r'√.*[0-9]+\.[0-9]+',
            r'square\s+root',
            r's[²2]\s*='
        ]
        for pattern in calc_patterns:
            if re.search(pattern, text_lower):
                calculations_found["sd_calculation_shown"] = True
                evidence.append("SD calculation steps are shown")
                break

        # Check for correct answer (approximately 2.59 or 2.6)
        if re.search(r'2\.59|2\.60|2\.6[^0-9]|s\s*=\s*2\.6', student_answer):
            calculations_found["sd_correct"] = True
            evidence.append("Correct SD value found (≈2.59 or 2.6)")

        return {
            "calculations_found": calculations_found,
            "evidence": evidence if evidence else ["No SD calculation elements found"]
        }

    def grade_question_hw3_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade the sample mean and sample standard deviation assignment.

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
                    "component_2_score": 9,
                    "component_3_score": 9,
                },
                max_points=19,
                feedback="Test mode feedback for mean and SD calculation task.",
                vibe="Test mode vibe assessment",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "task_description": True,
                            "dataset_shown": True
                        },
                        "evidence": ["Test mode - all elements present"]
                    },
                    "mean_check": {
                        "calculations_found": {
                            "mean_formula_stated": True,
                            "mean_formula_used": True,
                            "mean_calculation_shown": True,
                            "mean_correct": True
                        },
                        "evidence": ["Test mode - all mean elements present"]
                    },
                    "sd_check": {
                        "calculations_found": {
                            "sd_formula_stated": True,
                            "sd_formula_used": True,
                            "sd_calculation_shown": True,
                            "sd_correct": True
                        },
                        "evidence": ["Test mode - all SD elements present"]
                    }
                }
            )

        formatting_check = self.check_formatting_elements(student_answer)
        mean_check = self.check_mean_calculation(student_answer)
        sd_check = self.check_sd_calculation(student_answer)

        prompt = f"""You are grading a statistics homework assignment on calculating sample mean and sample standard deviation.

**EVALUATOR-COMPUTED REFERENCE VALUES:**
These values are computed internally using standard formulas and serve as the ONLY reference:
- Sample Mean (x̄) = {self.expected_mean} (rounded to 2 decimals: {self._round_half_up(self.expected_mean)})
- Sample Standard Deviation (s) = {self.expected_sd} (rounded to 2 decimals: {self._round_half_up(self.expected_sd)})

**NUMERICAL VALIDATION RULES:**
1. Both the evaluator-computed value and student's reported value are rounded to 2 decimal places (round-half-up) before comparison
2. Values are considered equal if they match exactly after rounding
3. A student's numerical result produced by software is NOT incorrect by itself
4. Penalties apply ONLY if manual calculations, formulas, or logical steps are missing (per rubric)
5. Numerical mismatch alone must NOT be used as evidence of incorrect work unless it contradicts the evaluator-computed reference after rounding
6. Example: If student reports 2.59 and reference is 2.59 (after rounding), they match. If student reports 2.88, they do NOT match.

**TASK DESCRIPTION:**
Task 10. Compute the sample mean and sample standard deviation for the following scores:

Values: −8, −4, −7, −6, −8, −5, −7, −9, −2, 0

**EXPECTED ANSWERS:**
- Sample Mean (x̄) = -5.6
  Calculation: Sum = -56, n = 10, Mean = -56/10 = -5.6

- Sample Standard Deviation (s) = 2.59 (or 2.6 with rounding)
  Calculation steps:
  1. Calculate deviations: (x - x̄)
  2. Square deviations: (x - x̄)²
  3. Sum squared deviations: Σ(x - x̄)² = 60.4
  4. Calculate variance: s² = 60.4/(10-1) = 60.4/9 = 6.71
  5. Take square root: s = √6.71 ≈ 2.59

**RUBRIC (19 points total):**

**Component 1: Task Setup (1 point total)**
- 1 point: Task description is present and correct
- 0 points: Task description missing or incorrect

Component 2: Sample Mean (9 points total)**
This component starts at 9 points with deductions applied for missing elements.

Deduction rules:
- Formula not explicitly stated: -1 point
- Formula stated but not demonstrated in calculations: -1 point
- Calculation steps not shown clearly: -3 points
- Final answer incorrect (after rounding to 2 decimals): -2 points
- Final answer only, no work shown: -6 points (formula -1, demonstration -1, steps -3, answer evaluated)

Maximum deduction: Cannot go below 0 points

Scoring logic:
- Start with 9 points
- If no formula stated: subtract 1
- If formula stated but not used/demonstrated: subtract 1
- If calculation steps missing or unclear: subtract 3
- If answer doesn't match reference (after rounding): subtract 2
- Result: 9 - (deductions) = final score (minimum 0)

**Component 3: Sample Standard Deviation (9 points total)**
This component starts at 9 points with deductions applied for missing elements.

Deduction rules:
- Formula not explicitly stated: -1 point
- Formula stated but not demonstrated in calculations: -1 point
- Calculation steps not shown clearly: -3 points
- Final answer incorrect (after rounding to 2 decimals): -2 points
- Final answer only, no work shown: -6 points (formula -1, demonstration -1, steps -3, answer evaluated)

Maximum deduction: Cannot go below 0 points

Scoring logic:
- Start with 9 points
- If no formula stated: subtract 1
- If formula stated but not used/demonstrated: subtract 1
- If calculation steps missing or unclear: subtract 3
- If answer doesn't match reference (after rounding): subtract 2
- Result: 9 - (deductions) = final score (minimum 0)
Example scenarios:
- No formula, no demonstration, no steps, wrong answer: 9 - 1 - 1 - 3 - 2 = 2 points
- No formula, no demonstration, no steps, only final answer: 9 - 1 - 1 - 3 = 4 points (if answer correct after rounding)
- Formula stated, not demonstrated, steps shown, answer correct: 9 - 1 = 8 points
- Everything present and correct: 9 points

**STUDENT ANSWER:**
{student_answer}

**AUTOMATIC FORMATTING DETECTION RESULT:**
Elements Found: {formatting_check['elements_found']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC MEAN CALCULATION DETECTION RESULT:**
Calculations Found: {mean_check['calculations_found']}
Evidence: {mean_check['evidence']}

**AUTOMATIC SD CALCULATION DETECTION RESULT:**
Calculations Found: {sd_check['calculations_found']}
Evidence: {sd_check['evidence']}

**CRITICAL GRADING RULES:**
1. Component 1: Task description must be present for credit
2. Component 2 & 3: Each has three subscores (formula stated, formula demonstrated, calculation steps)
3. "Formula stated" means the formula is explicitly written out (not just implied)
4. "Formula demonstrated" means showing the actual numbers being plugged into the formula
5. Final answers alone are INSUFFICIENT - must show work
6. Be strict on mathematical correctness: Mean = -5.6, SD ≈ 2.59 or 2.6
7. Manual calculations MUST be shown - software-only results receive minimal credit
8. Apply penalty rules: -1 for formula not specified, -1 for formula not demonstrated (max -2 per component)

**COMMON STUDENT MISTAKES TO NOTE IN FEEDBACK:**
- Incorrect notation (X instead of X̄) - note in feedback
- Approximate symbol (≈) instead of rounded values - note in feedback
- More than two decimals - note in feedback (no penalty)
- No visible logic or calculations - major deduction
- Final answers only without work - major deduction
- Formula stated but not applied - penalty applies

**SCORING PROCESS:**
1. Component 1 (Task Setup): Present and correct? (0 or 1)
2. Component 2 (Mean): 
   - Start with 9 points
   - Subtract 1 if formula not stated
   - Subtract 1 if formula not demonstrated
   - Subtract 3 if calculation steps missing/unclear
   - Subtract 2 if answer incorrect (after rounding)
   - Final: 9 - deductions (minimum 0, maximum 9)
3. Component 3 (SD):
   - Start with 9 points
   - Subtract 1 if formula not stated
   - Subtract 1 if formula not demonstrated
   - Subtract 3 if calculation steps missing/unclear
   - Subtract 2 if answer incorrect (after rounding)
   - Final: 9 - deductions (minimum 0, maximum 9)
4. Total = sum of three components (max 19)

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- Addresses presence/absence of task description
- For mean: evaluates formula statement, formula demonstration, calculation steps, and correctness
- For SD: evaluates formula statement, formula demonstration, calculation steps, and correctness
- Notes any formatting issues (notation, rounding, approximate symbols)
- Identifies specific missing elements or errors
- Remains constructive and encourages complete work with formulas and steps
- Provides specific examples of what's missing or done well
- Formulated strictly as teacher's comments without invitations to discussion

**IMPORTANT:** 
- It is expected to see the student's logic and calculations, not only final answers
- Formulate feedback strictly as teacher's comments
- Do NOT use wording that invites discussion (e.g., "Feel free to...", "Let me know if...")
- Use declarative statements only

Return your grading in this exact JSON format:
{{
  "component_1_score": <0 or 1>,
  "component_1_explanation": "<explanation of task setup>",
  "component_2_score": <0-9>,
  "component_2_explanation": "<detailed explanation: formula stated (0-3), formula demonstrated (0-3), calculation steps (0-3), penalties applied>",
  "component_3_score": <0-9>,
  "component_3_explanation": "<detailed explanation: formula stated (0-3), formula demonstrated (0-3), calculation steps (0-3), penalties applied>",
  "total_points": <sum of above, 0-19>,
  "max_points": 19,
  "percentage": <percentage>,
  "feedback": "<comprehensive narrative covering all components, formatted as teacher's comments>",
  "vibe": "<one-sentence assessment of student's statistical understanding and work quality>"
}}"""

        return self.grade_with_prompt(student_answer, prompt)

    def print_grading_results(self, result: dict):
        """
        Print grading results in a formatted way.

        Args:
            result: Dictionary containing grading results
        """
        print("\n" + "=" * 60)
        print("SAMPLE MEAN AND STANDARD DEVIATION - GRADING RESULTS")
        print("=" * 60)

        print(f"\nComponent 1 - Task Setup: {result['component_1_score']}/1")
        if result.get('component_1_explanation'):
            print(f"  {result['component_1_explanation']}")

        print(f"\nComponent 2 - Sample Mean: {result['component_2_score']}/9")
        if result.get('component_2_explanation'):
            print(f"  {result['component_2_explanation']}")

        print(f"\nComponent 3 - Sample Standard Deviation: {result['component_3_score']}/9")
        if result.get('component_3_explanation'):
            print(f"  {result['component_3_explanation']}")

        print("\n" + "-" * 60)
        print(f"TOTAL SCORE: {result['total_points']}/{result['max_points']} ({result['percentage']:.1f}%)")
        print("-" * 60)

        print("\nFEEDBACK:")
        print(textwrap.fill(result['feedback'], width=60))

        print("\nVIBE CHECK:")
        print(textwrap.fill(result['vibe'], width=60))

        print("\n" + "=" * 60 + "\n")


def main():
    """Test the evaluator with a sample student answer."""
    evaluator = HW3_5Evaluator()

    # Sample student answer for testing
    sample_answer = """
    Task 10: Compute the sample mean and sample standard deviation for the scores.

    Dataset: −8, −4, −7, −6, −8, −5, −7, −9, −2, 0

    Sample Mean Calculation:

    Formula: x̄ = Σx / n

    Sum of all values:
    Σx = (-8) + (-4) + (-7) + (-6) + (-8) + (-5) + (-7) + (-9) + (-2) + 0
    Σx = -56

    Number of values: n = 10

    Mean = -56 / 10 = -5.6

    Sample Standard Deviation Calculation:

    Formula: s = √[Σ(x - x̄)² / (n-1)]

    First, calculate deviations from mean (x - x̄):
    -8 - (-5.6) = -2.4
    -4 - (-5.6) = 1.6
    -7 - (-5.6) = -1.4
    -6 - (-5.6) = -0.4
    -8 - (-5.6) = -2.4
    -5 - (-5.6) = 0.6
    -7 - (-5.6) = -1.4
    -9 - (-5.6) = -3.4
    -2 - (-5.6) = 3.6
    0 - (-5.6) = 5.6

    Square each deviation:
    (-2.4)² = 5.76
    (1.6)² = 2.56
    (-1.4)² = 1.96
    (-0.4)² = 0.16
    (-2.4)² = 5.76
    (0.6)² = 0.36
    (-1.4)² = 1.96
    (-3.4)² = 11.56
    (3.6)² = 12.96
    (5.6)² = 31.36

    Sum of squared deviations:
    Σ(x - x̄)² = 5.76 + 2.56 + 1.96 + 0.16 + 5.76 + 0.36 + 1.96 + 11.56 + 12.96 + 31.36 = 74.4

    Variance: s² = 74.4 / (10-1) = 74.4 / 9 = 8.27

    Standard Deviation: s = √8.27 = 2.88

    Final Answers:
    Sample Mean = -5.6
    Sample Standard Deviation = 2.88
    """

    print("Testing HW3_5 Evaluator with sample answer...")
    print("\nExpected values (computed internally):")
    print(f"  Mean: {evaluator.expected_mean} (rounded: {evaluator._round_half_up(evaluator.expected_mean)})")
    print(f"  SD: {evaluator.expected_sd} (rounded: {evaluator._round_half_up(evaluator.expected_sd)})")
    print("\nSample Answer:")
    print(sample_answer)

    result = evaluator.grade_question_hw3_5_answer(sample_answer)
    evaluator.print_grading_results(result)

if __name__ == "__main__":
    main()
