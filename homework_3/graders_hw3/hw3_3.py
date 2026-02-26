"""
hw3_3.py
Histogram and Central Tendency Analysis Evaluator
"""

import re
import textwrap

from config import BaseEvaluator


class HW3_3Evaluator(BaseEvaluator):
    """
    Evaluator for Histogram and Central Tendency Analysis Question.

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
        Check if student includes required formatting elements for histogram.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "introductory_phrase": False,
            "illustration_reference": False,
            "apa_numbering": False,
            "title_present": False,
            "part_a_mentioned": False,
            "part_b_mentioned": False,
            "part_c_mentioned": False,
            "part_d_mentioned": False
        }

        evidence = []

        # Check for task description
        task_patterns = [
            r'construct.*histogram',
            r'describe.*shape',
            r'predict.*mean.*median.*mode',
            r'compute.*sample.*mean',
            r'locate.*mean.*median.*mode',
            r'task\s*:',
            r'question\s*:',
            r'data\s*:\s*5,?\s*8,?\s*8'  # Check if they included the data set
        ]
        for pattern in task_patterns:
            if re.search(pattern, text_lower):
                elements_found["task_description"] = True
                evidence.append(f"Found task description: {pattern}")
                break

        # Check for introductory phrase before histogram
        intro_patterns = [
            r'figure\s+\d+.*shows',
            r'fig\.\s*\d+.*shows',
            r'as\s+(seen|shown|illustrated)\s+in\s+(figure|fig\.)\s+\d+',
            r'refer\s+to\s+(figure|fig\.)\s+\d+'
        ]
        for pattern in intro_patterns:
            if re.search(pattern, text_lower):
                elements_found["introductory_phrase"] = True
                evidence.append(f"Found introductory phrase: {pattern}")
                break

        # Check for illustration reference by number
        if re.search(r'(figure|fig\.?|histogram)\s*\d+', text_lower):
            elements_found["illustration_reference"] = True
            evidence.append("Found illustration reference with number")

        # Check for APA-style numbering
        apa_patterns = [
            r'figure\s+\d+',
            r'fig\.\s*\d+',
            r'table\s+\d+'
        ]
        for pattern in apa_patterns:
            if re.search(pattern, text_lower):
                elements_found["apa_numbering"] = True
                evidence.append(f"Found APA-style numbering: {pattern}")
                break

        # Check for title (often contains descriptive text after the number)
        title_patterns = [
            r'(figure|fig\.?)\s+\d+[\.:]\s*\w+',
            r'histogram\s+of',
            r'distribution\s+of.*scores'
        ]
        for pattern in title_patterns:
            if re.search(pattern, text_lower):
                elements_found["title_present"] = True
                evidence.append(f"Found title: {pattern}")
                break

        # Check if parts are mentioned
        if re.search(r'\ba[\.\):]', text_lower) or re.search(r'part\s+a', text_lower):
            elements_found["part_a_mentioned"] = True
            evidence.append("Part a is mentioned")

        if re.search(r'\bb[\.\):]', text_lower) or re.search(r'part\s+b', text_lower):
            elements_found["part_b_mentioned"] = True
            evidence.append("Part b is mentioned")

        if re.search(r'\bc[\.\):]', text_lower) or re.search(r'part\s+c', text_lower):
            elements_found["part_c_mentioned"] = True
            evidence.append("Part c is mentioned")

        if re.search(r'\bd[\.\):]', text_lower) or re.search(r'part\s+d', text_lower):
            elements_found["part_d_mentioned"] = True
            evidence.append("Part d is mentioned")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear formatting elements found"]
        }

    def check_formatting_graphs_and_calculations(self, student_answer: str) -> dict:
        """
        Check if student includes required calculations and formulas.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found calculations and evidence
        """
        text_lower = student_answer.lower()

        calculations_found = {
            "shape_identified": False,
            "shape_reasoning": False,
            "prediction_stated": False,
            "prediction_reasoning": False,
            "mean_formula": False,
            "mean_calculation": False,
            "median_method": False,
            "mode_identification": False,
            "verification_stated": False
        }

        evidence = []

        # Check for shape identification
        shape_patterns = [
            r'positively\s+skewed',
            r'right[\s-]skewed',
            r'right[\s-]tailed',
            r'skewed\s+(to\s+the\s+)?right'
        ]
        for pattern in shape_patterns:
            if re.search(pattern, text_lower):
                calculations_found["shape_identified"] = True
                evidence.append(f"Found shape identification: {pattern}")
                break

        # Check for shape reasoning
        reasoning_patterns = [
            r'tail.*right|right.*tail',
            r'outlier.*high|high.*outlier',
            r'mean.*pull|pull.*mean',
            r'few.*high.*value|high.*value.*few'
        ]
        for pattern in reasoning_patterns:
            if re.search(pattern, text_lower):
                calculations_found["shape_reasoning"] = True
                evidence.append(f"Found shape reasoning: {pattern}")
                break

        # Check for prediction
        prediction_patterns = [
            r'mean\s*>\s*median',
            r'mean.*greater.*median',
            r'mean.*higher.*median',
            r'median\s*<\s*mean'
        ]
        for pattern in prediction_patterns:
            if re.search(pattern, text_lower):
                calculations_found["prediction_stated"] = True
                evidence.append(f"Found prediction: {pattern}")
                break

        # Check for prediction reasoning
        pred_reasoning_patterns = [
            r'skew.*pull.*mean',
            r'mean.*affect.*skew',
            r'median.*resistant',
            r'mean.*sensitive.*outlier'
        ]
        for pattern in pred_reasoning_patterns:
            if re.search(pattern, text_lower):
                calculations_found["prediction_reasoning"] = True
                evidence.append(f"Found prediction reasoning: {pattern}")
                break

        # Check for mean formula
        mean_patterns = [
            r'mean\s*=\s*\(?sum|sum.*\/.*n|average.*=',
            r'μ\s*=|x̄\s*=',
            r'Σ.*\/.*n',
            r'add.*divide\s+by\s+(20|n)'
        ]
        for pattern in mean_patterns:
            if re.search(pattern, text_lower):
                calculations_found["mean_formula"] = True
                evidence.append(f"Found mean formula")
                break

        # Check for mean calculation with numbers
        if re.search(r'(165|8\.25|sum\s*=\s*165)', student_answer):
            calculations_found["mean_calculation"] = True
            evidence.append("Found mean calculation with numbers")

        # Check for median method
        median_patterns = [
            r'median.*middle',
            r'middle.*value',
            r'sort|order.*find.*middle',
            r'10th.*11th|n/2',
            r'average.*middle.*two'
        ]
        for pattern in median_patterns:
            if re.search(pattern, text_lower):
                calculations_found["median_method"] = True
                evidence.append("Found median method/explanation")
                break

        # Check for mode identification
        mode_patterns = [
            r'mode.*most\s+frequent',
            r'most\s+frequent|appears.*most',
            r'mode.*=.*8',
            r'8.*appears.*\d+.*times'
        ]
        for pattern in mode_patterns:
            if re.search(pattern, text_lower):
                calculations_found["mode_identification"] = True
                evidence.append("Found mode identification")
                break

        # Check for verification
        verification_patterns = [
            r'verif|confirm|check.*prediction',
            r'prediction.*correct|matches',
            r'as\s+predicted|expected',
            r'consistent\s+with.*prediction'
        ]
        for pattern in verification_patterns:
            if re.search(pattern, text_lower):
                calculations_found["verification_stated"] = True
                evidence.append("Found verification statement")
                break

        return {
            "calculations_found": calculations_found,
            "evidence": evidence if evidence else ["No calculations or formulas found"]
        }

    def grade_histogram_analysis(self, student_answer: str, test_mode: bool = False):
        """
        Grade the histogram and central tendency analysis assignment.

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
                    "component_2_score": 4,
                    "component_3_score": 5,
                    "component_4_score": 5,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="Test mode feedback for histogram analysis task.",
                vibe="Test mode vibe assessment",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "introductory_phrase": True,
                            "illustration_reference": True,
                            "apa_numbering": True,
                            "title_present": True
                        },
                        "evidence": ["Test mode - all elements present"]
                    },
                    "calculation_check": {
                        "calculations_found": {
                            "shape_identified": True,
                            "shape_reasoning": True,
                            "prediction_stated": True,
                            "prediction_reasoning": True,
                            "mean_formula": True,
                            "mean_calculation": True,
                            "median_method": True,
                            "mode_identification": True,
                            "verification_stated": True
                        },
                        "evidence": ["Test mode - all calculations present"]
                    }
                }
            )
        formatting_check = self.check_formatting_elements(student_answer)
        calculation_check = self.check_formatting_graphs_and_calculations(student_answer)

        prompt = f"""You are grading a statistics homework assignment on histogram analysis and central tendency measures.

**TASK DESCRIPTION:**
Data: 5, 8, 8, 8, 7, 8, 9, 12, 8, 9, 8, 10, 7, 9, 7, 6, 9, 10, 11, 8

a. Construct a histogram for the data and describe its shape.
b. Based on the shape, predict how the mean, median, and mode will compare.
c. Compute the sample mean, median, and mode.
d. Locate the mean, median, and mode on your histogram and verify your prediction.

**EXPECTED ANSWERS:**
- Shape: Positively skewed (right-tailed/right-skewed)
- Prediction: Mean > Median (values should be close together)
- Mean = 8.25 (sum = 165, n = 20)
- Median = 8 (average of 10th and 11th values when sorted)
- Mode = 8 (appears 7 times)
- Verification: Prediction matches calculations

**RUBRIC (20 points total):**

**Component 1: Part a - Shape Identification (5 points)**
- 5 points: Task description included + Histogram presented + Correct shape + Reasoning
- 4 points: Task description included + Histogram presented + Correct shape (no reasoning)
- 3 points: Histogram presented + Correct shape + Reasoning (no task description)
- 2 points: Histogram presented + Correct shape (no task description, no reasoning)
- 1 point: Correct shape only (no task description, no histogram) OR partial attempt
- 0 points: Missing or completely incorrect

**Component 2: Part b - Prediction with Reasoning (5 points)**
- 5 points: Correct prediction (Mean > Median) + reasoning (any reasoning qualifies)
- 2 points: Correct prediction but no reasoning
- 1 point: Partially correct or incorrect prediction but shows understanding attempt
- 0 points: Missing

**Component 3: Part c - Central Tendency Calculations (5 points)**
This component combines all three measures. Award 1 point for each correctly calculated measure with proper work shown:
- Mean (1 point): Formula/method shown + calculation + correct answer (8.25)
  * 1 point if all three elements present
  * 0 points if missing formula/method OR calculation OR answer is incorrect
- Median (1 point): Method/explanation shown + correct answer (8)
  * 1 point if both elements present
  * 0 points if missing method OR answer is incorrect
- Mode (1 point): Identification/explanation shown + correct answer (8)
  * 1 point if both elements present
  * 0 points if missing explanation OR answer is incorrect
- Additional point (1 point): Award if student shows exceptional work across all three measures (detailed formulas, clear organization, verification of sorted data for median, frequency count for mode)

Scoring guidelines:
- 5 points: All three measures correct with methods shown + exceptional work
- 3 points: All three measures correct with methods shown
- 2 points: Two measures correct with methods OR all three correct but minimal work shown
- 1 point: One measure correct OR attempts shown but with errors
- 0 points: Missing or all incorrect

**Component 4: Part d - Verification (4 points)**
- 5 points: Explicitly verifies prediction matches calculations + clear reasoning + references specific values on histogram
- 3 points: Verifies prediction matches calculations + reasoning but lacks histogram reference
- 2 points: States verification but minimal reasoning
- 1 point: Mentions verification but unclear or incomplete
- 0 points: No verification or incorrect verification

**STUDENT ANSWER:**
{student_answer}

**AUTOMATIC FORMATTING DETECTION RESULT:**
Elements Found: {formatting_check['elements_found']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC CALCULATION DETECTION RESULT:**
Calculations Found: {calculation_check['calculations_found']}
Evidence: {calculation_check['evidence']}

**CRITICAL GRADING RULES:**
1. Component 1: Check task_description (True/False), check histogram formatting elements (at least one True = histogram presented), check shape correctness, check reasoning presence. Use the 5-4-3-2-1-0 scale exactly as stated in rubric.
2. Component 2: If prediction is correct + ANY reasoning present = 5 points. Correct prediction without reasoning = 2 points
3. Component 3: Each measure (mean, median, mode) must have method/formula shown + correct answer to earn its point. The 5th point requires exceptional work across all three.
4. Component 4: Explicit verification with reasoning required for full credit
5. Be strict on mathematical correctness - verify: Mean = 8.25, Median = 8, Mode = 8
6. Missing work/formulas significantly reduces scores even if final answers are correct

**SCORING PROCESS:**
1. Component 1 (Part a): Score 0-5 based on:
- Task description present? (check formatting_check['task_description'])
- Histogram presented? (check if ANY of: introductory_phrase, illustration_reference, apa_numbering, title_present = True)
- Shape correct? (positively/right skewed)
- Reasoning present? (any reasoning)
Apply rubric: 5=all four / 4=task+hist+shape / 3=hist+shape+reasoning / 2=hist+shape / 1=shape only or partial / 0=missing
2. Component 2 (Prediction): Correct prediction + any reasoning = 5 pts; correct prediction without reasoning = 2 pts (0-5)
3. Component 3 (Calculations): 
   - Mean correct with method? (+1 or 0)
   - Median correct with method? (+1 or 0)
   - Mode correct with method? (+1 or 0)
   - Exceptional work across all? (+1 or 0)
   Total: 0-5
4. Component 4 (Verification): Evaluate explicitness + reasoning (0-5)
5. Total = sum of five components (max 20)

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- For Component 1: Check task_description (present/missing), histogram formatting (presented/not presented), shape (correct/incorrect), reasoning (present/absent). State which elements present and final score 0-5.
- Identifies which formatting elements are present/missing (Component 1)
- Notes correctness of shape identification and presence/absence of reasoning (Component 2) - do not evaluate quality of reasoning
- Evaluates prediction correctness and presence/absence of reasoning (Component 3) - do not evaluate quality of reasoning
- For Component 4, addresses EACH measure separately: whether method shown, calculation detailed, answer correct
- Confirms whether verification is explicit and complete (Component 5)
- Notes any mathematical errors
- Remains constructive and encourages complete work with reasoning

Return your grading in this exact JSON format:
{{
  "component_1_score": <0-5>,
  "component_1_explanation": "<State which elements present: task description (yes/no), histogram (yes/no), correct shape (yes/no), reasoning (yes/no), then justify the score>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<explanation of prediction correctness and reasoning>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<explanation covering mean (method+answer), median (method+answer), mode (method+answer), and overall work quality>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<explanation of verification quality and completeness>",
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<comprehensive narrative covering all components>",
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
        print("HISTOGRAM AND CENTRAL TENDENCY ANALYSIS - GRADING RESULTS")
        print("=" * 60)

        print(f"\nComponent 1 - Part a (Shape Identification): {result['component_1_score']}/5")
        if result.get('component_1_explanation'):
            print(f"  {result['component_1_explanation']}")

        print(f"\nComponent 2 - Part b (Prediction with Reasoning): {result['component_2_score']}/5")
        if result.get('component_2_explanation'):
            print(f"  {result['component_2_explanation']}")

        print(f"\nComponent 3 - Part c (Central Tendency Calculations): {result['component_3_score']}/5")
        if result.get('component_3_explanation'):
            print(f"  {result['component_3_explanation']}")

        print(f"\nComponent 4 - Part d (Verification): {result['component_4_score']}/5")
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


def main():
    """Test the evaluator with a sample student answer."""
    evaluator = HW3_3Evaluator()

    # Sample student answer for testing
    sample_answer = """
    a. Figure 1 shows the histogram for the given data.
    
    Figure 1: Distribution of Test Scores
    [Histogram would be drawn here]
    
    The histogram is positively skewed (right-tailed) because there are a few higher values that pull the distribution to the right.
    
    b. Based on the positively skewed shape, I predict that the mean will be greater than the median. The mean is sensitive to extreme values and will be pulled toward the higher scores, while the median is more resistant to outliers.
    
    c. Calculations:
    
    Mean = Σx / n = (5+8+8+8+7+8+9+12+8+9+8+10+7+9+7+6+9+10+11+8) / 20
    Mean = 165 / 20 = 8.25
    
    Median: First, sort the data: 5, 6, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 11, 12
    Since n=20 (even), median = average of 10th and 11th values = (8+8)/2 = 8
    
    Mode: The value 8 appears 7 times, which is more frequent than any other value. Mode = 8
    
    d. On the histogram, the mode (8) is at the peak, the median (8) is at the same location, and the mean (8.25) is slightly to the right of the median. This confirms my prediction that mean > median in a positively skewed distribution.
    """

    print("Testing HW3_3 Evaluator with sample answer...")
    print("\nSample Answer:")
    print(sample_answer)

    result = evaluator.grade_histogram_analysis(sample_answer)
    evaluator.print_grading_results(result)


if __name__ == "__main__":
    main()