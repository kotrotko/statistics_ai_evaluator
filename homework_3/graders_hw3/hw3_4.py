"""
hw3_4.py
Mean, Variance and Standard Deviation with Outlier Analysis Evaluator
"""

import re
import textwrap

from config import BaseEvaluator


class HW3_4Evaluator(BaseEvaluator):
    """
    Evaluator for Variance and Standard Deviation with Outlier Analysis Question.

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
            "introductory_phrase": False,
            "table_reference": False,
            "apa_numbering": False,
            "title_present": False,
            "exercise_7_referenced": False,
            "dataset_with_65_shown": False,
            "incorrect_notation": False,
            "approximate_symbol_used": False
        }

        evidence = []

        # Check for introductory phrase before table
        intro_patterns = [
            r'table\s+\d+.*shows',
            r'as\s+(seen|shown|illustrated)\s+in\s+table\s+\d+',
            r'refer\s+to\s+table\s+\d+'
        ]
        for pattern in intro_patterns:
            if re.search(pattern, text_lower):
                elements_found["introductory_phrase"] = True
                evidence.append(f"Found introductory phrase: {pattern}")
                break

        # Check for table reference by number
        if re.search(r'table\s*\d+', text_lower):
            elements_found["table_reference"] = True
            evidence.append("Found table reference with number")

        # Check for APA-style numbering
        apa_patterns = [
            r'table\s+\d+',
            r'figure\s+\d+'
        ]
        for pattern in apa_patterns:
            if re.search(pattern, text_lower):
                elements_found["apa_numbering"] = True
                evidence.append(f"Found APA-style numbering: {pattern}")
                break

        # Check for title (often contains descriptive text after the number)
        title_patterns = [
            r'table\s+\d+[\.:]\s*\w+',
            r'descriptive\s+statistics',
            r'measures\s+of\s+(central\s+tendency|variability)'
        ]
        for pattern in title_patterns:
            if re.search(pattern, text_lower):
                elements_found["title_present"] = True
                evidence.append(f"Found title: {pattern}")
                break

        # Check if Exercise 7 is referenced
        ex7_patterns = [
            r'exercise\s+7',
            r'problem\s+7',
            r'task\s+7',
            r'from\s+the\s+previous\s+(exercise|problem)',
            r'without\s+(the\s+)?65'
        ]
        for pattern in ex7_patterns:
            if re.search(pattern, text_lower):
                elements_found["exercise_7_referenced"] = True
                evidence.append("Exercise 7 is referenced")
                break

        # Check if dataset with 65 is shown
        if '65' in student_answer:
            # Look for the full dataset or explicit inclusion of 65
            if re.search(r'25.*36.*41.*28.*29.*32.*39.*37.*34.*34.*37.*35.*30.*36.*31.*31.*65',
                         student_answer.replace('\n', ' ').replace(',', ' ')):
                elements_found["dataset_with_65_shown"] = True
                evidence.append("Dataset with 65 is explicitly shown")
            elif re.search(r'includ(e|ing).*65|add(ing)?.*65|with.*65', text_lower):
                elements_found["dataset_with_65_shown"] = True
                evidence.append("Explicit mention of including 65")

        # Check for incorrect notation (X instead of X̄)
        if re.search(r'\bX\s*=(?!\s*individual)', student_answer) and not re.search(r'X̄|\\bar\{X\}|x̄|\\bar\{x\}|mean',
                                                                                    text_lower):
            elements_found["incorrect_notation"] = False
            evidence.append("WARNING: Potentially incorrect notation detected (X without bar for mean)")

        # Check for approximate symbol (≈)
        if '≈' in student_answer:
            elements_found["approximate_symbol_used"] = True
            evidence.append("WARNING: Approximate symbol (≈) used instead of rounded values")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear formatting elements found"]
        }

    def check_calculations_and_comparisons(self, student_answer: str) -> dict:
        """
        Check if student includes required calculations and comparisons.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found calculations and evidence
        """
        text_lower = student_answer.lower()

        calculations_found = {
            "mean_calculation": False,
            "mean_comparison": False,
            "range_calculation": False,
            "range_comparison": False,
            "variance_calculation": False,
            "variance_comparison": False,
            "sd_calculation": False,
            "sd_comparison": False,
            "change_discussed": False,
            "outlier_sensitivity_mentioned": False
        }

        evidence = []

        # Check for mean calculation with 65
        mean_patterns = [
            r'mean\s*=',
            r'x̄\s*=|\\bar\{x\}',
            r'sum.*\/.*17|sum.*\/.*n',
            r'(37\.35|37\.4|633)'  # Expected values
        ]
        for pattern in mean_patterns:
            if re.search(pattern, text_lower) or re.search(pattern, student_answer):
                calculations_found["mean_calculation"] = True
                evidence.append("Found mean calculation")
                break

        # Check for mean comparison with Exercise 7
        mean_comp_patterns = [
            r'mean.*(increase|decrease|change|different|was.*now)',
            r'(33\.5|33\.50).*(37\.35|37\.4)',
            r'from.*(33\.5|33\.50).*to.*(37\.35|37\.4)',
            r'compar(e|ed|ing).*mean'
        ]
        for pattern in mean_comp_patterns:
            if re.search(pattern, text_lower) or re.search(pattern, student_answer):
                calculations_found["mean_comparison"] = True
                evidence.append("Found mean comparison with Exercise 7")
                break

        # Check for range calculation
        range_patterns = [
            r'range\s*=',
            r'max.*min|maximum.*minimum',
            r'65.*25|40',  # 65 - 25 = 40
            r'highest.*lowest'
        ]
        for pattern in range_patterns:
            if re.search(pattern, text_lower):
                calculations_found["range_calculation"] = True
                evidence.append("Found range calculation")
                break

        # Check for range comparison
        range_comp_patterns = [
            r'range.*(increase|decrease|change|different|was.*now)',
            r'(16|15).*(40|39)',
            r'from.*1[56].*to.*40',
            r'compar(e|ed|ing).*range'
        ]
        for pattern in range_comp_patterns:
            if re.search(pattern, text_lower):
                calculations_found["range_comparison"] = True
                evidence.append("Found range comparison")
                break

        # Check for variance calculation
        variance_patterns = [
            r'variance\s*=|s[²2]\s*=',
            r'Σ.*\(.*x.*-.*mean.*\)[²2]|sum.*squared.*deviation',
            r'(115\.8|120\.8|116)',  # Expected variance values
            r'\(n.*-.*1\)'
        ]
        for pattern in variance_patterns:
            if re.search(pattern, text_lower) or re.search(pattern, student_answer):
                calculations_found["variance_calculation"] = True
                evidence.append("Found variance calculation")
                break

        # Check for variance comparison
        var_comp_patterns = [
            r'variance.*(increase|decrease|change|different|was.*now)',
            r'(21\.5|21\.50).*(115\.8|120\.8|116)',
            r'from.*(21\.5|21\.50).*to.*(115\.8|120\.8|116)',
            r'compar(e|ed|ing).*variance'
        ]
        for pattern in var_comp_patterns:
            if re.search(pattern, text_lower) or re.search(pattern, student_answer):
                calculations_found["variance_comparison"] = True
                evidence.append("Found variance comparison")
                break

        # Check for standard deviation calculation
        sd_patterns = [
            r'standard\s+deviation\s*=|s\s*=|sd\s*=',
            r'√|sqrt|square\s+root.*variance',
            r'(10\.7|10\.76|10\.8)',  # Expected SD values
        ]
        for pattern in sd_patterns:
            if re.search(pattern, text_lower) or re.search(pattern, student_answer):
                calculations_found["sd_calculation"] = True
                evidence.append("Found standard deviation calculation")
                break

        # Check for SD comparison
        sd_comp_patterns = [
            r'standard\s+deviation.*(increase|decrease|change|different|was.*now)',
            r'(4\.6|4\.64).*(10\.7|10\.76|10\.8)',
            r'from.*(4\.6|4\.64).*to.*(10\.7|10\.76|10\.8)',
            r'compar(e|ed|ing).*standard\s+deviation'
        ]
        for pattern in sd_comp_patterns:
            if re.search(pattern, text_lower) or re.search(pattern, student_answer):
                calculations_found["sd_comparison"] = True
                evidence.append("Found SD comparison")
                break

        # Check for discussion of change
        change_patterns = [
            r'how.*did.*change',
            r'all.*(increase|decrease)',
            r'each.*(value|measure).*(increase|decrease|change)',
            r'(mean|range|variance|standard\s+deviation).*(and|,).*(increase|decrease)'
        ]
        for pattern in change_patterns:
            if re.search(pattern, text_lower):
                calculations_found["change_discussed"] = True
                evidence.append("Found discussion of how values changed")
                break

        # Check for outlier sensitivity mentioned
        outlier_patterns = [
            r'outlier',
            r'extreme.*value',
            r'sensitive.*to',
            r'affect.*by.*high.*value',
            r'impact.*of.*65',
            r'variability.*increase'
        ]
        for pattern in outlier_patterns:
            if re.search(pattern, text_lower):
                calculations_found["outlier_sensitivity_mentioned"] = True
                evidence.append("Found mention of outlier sensitivity")
                break

        return {
            "calculations_found": calculations_found,
            "evidence": evidence if evidence else ["No calculations or comparisons found"]
        }

    def grade_question_hw3_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade the variance and standard deviation with outlier analysis assignment.

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
                    "component_3_score": 10,
                },
                max_points=20,
                feedback="Test mode feedback for variance outlier analysis task.",
                vibe="Test mode vibe assessment",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "introductory_phrase": True,
                            "table_reference": True,
                            "apa_numbering": True,
                            "title_present": True,
                            "exercise_7_referenced": True,
                            "dataset_with_65_shown": True
                        },
                        "evidence": ["Test mode - all elements present"]
                    },
                    "calculation_check": {
                        "calculations_found": {
                            "mean_calculation": True,
                            "mean_comparison": True,
                            "range_calculation": True,
                            "range_comparison": True,
                            "variance_calculation": True,
                            "variance_comparison": True,
                            "sd_calculation": True,
                            "sd_comparison": True,
                            "change_discussed": True,
                            "outlier_sensitivity_mentioned": True
                        },
                        "evidence": ["Test mode - all calculations present"]
                    }
                }
            )

        formatting_check = self.check_formatting_elements(student_answer)
        calculation_check = self.check_calculations_and_comparisons(student_answer)

        prompt = f"""You are grading a statistics homework assignment on variance, standard deviation, and outlier sensitivity.

**TASK DESCRIPTION:**
Using the same values from Exercise 7, calculate the range, sample variance, and sample standard deviation, but this time include 65 in the list of values. How did each of the three values change?

Values: 25, 36, 41, 28, 29, 32, 39, 37, 34, 34, 37, 35, 30, 36, 31, 31, 65

**EXPECTED ANSWERS:**
Exercise 7 (WITHOUT 65, n=16):
- Mean = 33.50
- Range = 16 (41 - 25)
- Variance = 21.50
- Standard Deviation = 4.64

Exercise 8 (WITH 65, n=17):
- Mean = 37.35 (sum = 635)
- Range = 40 (65 - 25)
- Variance = 115.81
- Standard Deviation = 10.76

Changes:
- Mean increased from 33.50 to 37.35 (by 3.85)
- Range increased from 16 to 40 (by 24)
- Variance increased from 21.50 to 115.81 (by 94.31)
- Standard Deviation increased from 4.64 to 10.76 (by 6.12)

**RUBRIC (20 points total):**

**Component 1: Task Setup (1 point total)**
- 1 point: Task description present AND Exercise 7 statistics explicitly referenced (textbook values or recalculated) AND dataset with 65 explicitly shown
- 0 points: Missing task description OR missing Exercise 7 reference OR dataset with 65 not shown

**Component 2: Calculations (9 points total)**
This component evaluates calculations with comparisons for mean, range, variance, and standard deviation.

Mean (not graded separately, but must be present for variance/SD calculations):
- Check if calculated (required for other calculations)

Range (1.5 points):
- 0.5 points: Correct manual calculation with 65 included (Range = 40)
- 1 point: Explicit comparison with Exercise 7 range

Variance (3.75 points):
- 1.25 points: Correct manual calculation with 65 included (Variance ≈ 115.81)
- 2.5 points: Explicit comparison with Exercise 7 variance

Standard Deviation (3.75 points):
- 1.25 points: Correct manual calculation with 65 included (SD ≈ 10.76)
- 2.5 points: Explicit comparison with Exercise 7 SD

Scoring guidelines:
- Full credit requires BOTH correct calculation AND explicit comparison for each measure
- "Explicit comparison" means stating both the old value (from Exercise 7) and new value (with 65)
- Manual calculations must be shown; final answers alone insufficient
- Minor rounding differences acceptable (±0.1)
- Range: 1.5 points max (0.5 calculation + 1 comparison)
- Variance: 3.75 points max (1.25 calculation + 2.5 comparison)
- SD: 3.75 points max (1.25 calculation + 2.5 comparison)

**Component 3: Interpretation and Conclusion (10 points total)**
- 6 points: Direct and explicit answer to "How did each of the three values change?" (must address range, variance, and SD individually)
- 4 points: General conclusion emphasizing sensitivity to outliers (effect of extreme value on variability measures)

Scoring breakdown for interpretation:
- 6 points: Clearly states how EACH measure changed (e.g., "Range increased from 16 to 40", "Variance increased from 21.50 to 115.81", "SD increased from 4.64 to 10.76")
- 3 points: States changes but not all measures addressed or lacks specificity
- 1 point: Vague statement like "all increased" without specific values
- 0 points: No discussion of changes

Scoring breakdown for conclusion:
- 4 points: Clear statement about outlier sensitivity/effect of extreme values on variability
- 2 points: Mentions outliers but lacks clear connection to variability measures
- 0 points: No mention of outliers or sensitivity

**STUDENT ANSWER:**
{student_answer}

**AUTOMATIC FORMATTING DETECTION RESULT:**
Elements Found: {formatting_check['elements_found']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC CALCULATION DETECTION RESULT:**
Calculations Found: {calculation_check['calculations_found']}
Evidence: {calculation_check['evidence']}

**CRITICAL GRADING RULES:**
1. Component 1: Requires ALL three elements (task description + Exercise 7 reference + dataset with 65). Missing ANY element = 0 points
2. Component 2: Each measure must have BOTH calculation AND comparison. Calculation alone = partial credit. Comparison alone = 0 points for that measure.
3. Component 3: Requires BOTH specific discussion of changes (6 pts) AND general conclusion about outliers (4 pts)
4. Be strict on mathematical correctness - verify all calculations manually
5. "Explicit comparison" means student states BOTH old and new values, not just "it increased"
6. Manual calculations MUST be shown - final answers alone insufficient
7. Software-only calculations receive minimal credit

**COMMON STUDENT MISTAKES TO PENALIZE:**
- Missing introductory phrase before tables (note in feedback, no point deduction unless severe)
- Table not numbered/titled in APA style (note in feedback)
- More than two decimals (note in feedback, no point deduction)
- Incorrect notation (X instead of X̄) (note in feedback)
- Approximate symbol (≈) instead of rounded values (note in feedback, minor APA violation)
- No visible calculations/logic (major deduction in Component 2)
- Software calculations without manual work (major deduction in Component 2)
- Failure to explain changes (major deduction in Component 3)
- No explicit answer to "How did each change?" (major deduction in Component 3)
- Missing outlier sensitivity statement (major deduction in Component 3)

**EXAMPLE OF UNSATISFACTORY ANSWER (0-5 points total):**
"The standard deviation, variance and mean are presented in Table 2. These values have changed, all of them."
This receives major deductions for:
- No calculations shown (Component 2: ~0-1 points)
- No specific comparisons (Component 2: 0 points)
- No specific discussion of HOW they changed (Component 3: 0-1 points)
- No outlier conclusion (Component 3: 0 points)

**SCORING PROCESS:**
1. Component 1 (Task Setup): Check if ALL three elements present (0 or 1)
2. Component 2 (Calculations): 
   - Range: calculation (0.5) + comparison (1) = 1.5 max
   - Variance: calculation (1.25) + comparison (2.5) = 3.75 max
   - SD: calculation (1.25) + comparison (2.5) = 3.75 max
   Total: 0-9
3. Component 3 (Interpretation): 
   - Specific changes discussed (0-6)
   - Outlier sensitivity conclusion (0-4)
   Total: 0-10
4. Total = sum of three components (max 20)

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- Addresses presence/absence of task description, Exercise 7 reference, and dataset with 65
- For EACH measure (range, variance, SD): notes whether calculation shown, whether comparison made, whether values correct
- Evaluates whether student explicitly answered "How did each value change?"
- Evaluates whether student provided conclusion about outlier sensitivity
- Notes any formatting issues (table formatting, notation, rounding)
- Remains constructive and encourages complete work with reasoning
- Provides specific examples of what's missing or done well
- If student exceeds expectations, provides verbal appraisal only

**IMPORTANT:** Formulate feedback strictly as teacher's comments. Do NOT use wording that invites discussion (e.g., avoid "Feel free to...", "Let me know if...", "Would you like..."). Use declarative statements only.

Return your grading in this exact JSON format:
{{
  "component_1_score": <0 or 1>,
  "component_1_explanation": "<explanation of task setup completeness>",
  "component_2_score": <0-9>,
  "component_2_explanation": "<detailed explanation covering range (calc+comp), variance (calc+comp), SD (calc+comp)>",
  "component_3_score": <0-10>,
  "component_3_explanation": "<explanation of interpretation quality and outlier sensitivity discussion>",
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
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
        print("VARIANCE AND STANDARD DEVIATION WITH OUTLIER - GRADING RESULTS")
        print("=" * 60)

        print(f"\nComponent 1 - Task Setup: {result['component_1_score']}/1")
        if result.get('component_1_explanation'):
            print(f"  {result['component_1_explanation']}")

        print(f"\nComponent 2 - Calculations: {result['component_2_score']}/9")
        if result.get('component_2_explanation'):
            print(f"  {result['component_2_explanation']}")

        print(f"\nComponent 3 - Interpretation and Conclusion: {result['component_3_score']}/10")
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
    evaluator = HW3_4Evaluator()

    # Sample student answer for testing
    sample_answer = """
    Task: Using the values from Exercise 7, calculate the range, variance, and standard deviation with 65 included.

    From Exercise 7 (without 65): Mean = 33.50, Range = 16, Variance = 21.50, SD = 4.64

    Dataset with 65: 25, 36, 41, 28, 29, 32, 39, 37, 34, 34, 37, 35, 30, 36, 31, 31, 65 (n=17)

    Calculations:

    Mean = Σx / n = (25+36+41+28+29+32+39+37+34+34+37+35+30+36+31+31+65) / 17 = 635 / 17 = 37.35

    Range = Maximum - Minimum = 65 - 25 = 40
    The range increased from 16 to 40.

    Variance = Σ(x - x̄)² / (n-1)
    Deviations squared:
    (25-37.35)² = 152.52
    (36-37.35)² = 1.82
    (41-37.35)² = 13.32
    (28-37.35)² = 87.42
    (29-37.35)² = 69.72
    (32-37.35)² = 28.62
    (39-37.35)² = 2.72
    (37-37.35)² = 0.12
    (34-37.35)² = 11.22
    (34-37.35)² = 11.22
    (37-37.35)² = 0.12
    (35-37.35)² = 5.52
    (30-37.35)² = 54.02
    (36-37.35)² = 1.82
    (31-37.35)² = 40.32
    (31-37.35)² = 40.32
    (65-37.35)² = 764.02

    Sum of squared deviations = 1852.92
    Variance = 1852.92 / 16 = 115.81
    The variance increased from 21.50 to 115.81.

    Standard Deviation = √Variance = √115.81 = 10.76
    The standard deviation increased from 4.64 to 10.76.

    How did each value change?
    - Range increased from 16 to 40 (by 24)
    - Variance increased from 21.50 to 115.81 (by 94.31)
    - Standard Deviation increased from 4.64 to 10.76 (by 6.12)

    All three measures of variability increased substantially when the outlier (65) was added to the dataset. This demonstrates that measures of variability are highly sensitive to extreme values. The presence of a single outlier can dramatically affect the range, variance, and standard deviation, illustrating why it's important to identify and consider outliers when analyzing data.
    """

    print("Testing HW3_4 Evaluator with sample answer...")
    print("\nSample Answer:")
    print(sample_answer)

    result = evaluator.grade_question_hw3_4_answer(sample_answer)
    evaluator.print_grading_results(result)


if __name__ == "__main__":
    main()