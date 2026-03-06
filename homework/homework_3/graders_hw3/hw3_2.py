"""
hw3_2.py
Data Sets Creation Evaluator - Mean, Median, Standard Deviation
"""

import re
import textwrap

from config import BaseEvaluator


class HW3_2Evaluator(BaseEvaluator):
    """
    Evaluator for Data Sets Creation Question.

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
            "task_description": False,
            "part_a_mentioned": False,
            "part_b_mentioned": False,
            "part_c_mentioned": False
        }

        evidence = []

        # Check for task description
        task_patterns = [
            r'make up.*data sets',
            r'three data sets.*5 numbers',
            r'task\s*:',
            r'question\s*:'
        ]
        for pattern in task_patterns:
            if re.search(pattern, text_lower):
                elements_found["task_description"] = True
                evidence.append(f"Found task description: {pattern}")
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

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear formatting elements found"]
        }

    def check_calculations_and_formulas(self, student_answer: str) -> dict:
        text_lower = student_answer.lower()

        calculations_found = {
            "mean_formula": False,
            "mean_calculation": False,
            "median_explanation": False,
            "sd_formula": False,
            "sd_calculation": False,
            "shows_work": False
        }

        evidence = []

        mean_patterns = [
            r'mean\s*=\s*\(?sum|sum.*\/.*n|average.*=',
            r'μ\s*=',
            r'\(.*\+.*\+.*\+.*\+.*\)\s*\/\s*5',
            r'add.*divide\s+by\s+5'
        ]
        for pattern in mean_patterns:
            if re.search(pattern, text_lower):
                calculations_found["mean_formula"] = True
                evidence.append(f"Found mean formula or calculation")
                break

        if re.search(r'\d+\s*[\+]\s*\d+\s*[\+]\s*\d+\s*[\+]\s*\d+\s*[\+]\s*\d+\s*[=/]\s*\d+', student_answer):
            calculations_found["mean_calculation"] = True
            evidence.append("Found explicit mean calculation with numbers")

        median_patterns = [
            r'median.*middle',
            r'middle.*value',
            r'sort|order.*find.*middle',
            r'3rd.*value|third.*value'
        ]
        for pattern in median_patterns:
            if re.search(pattern, text_lower):
                calculations_found["median_explanation"] = True
                evidence.append("Found median explanation")
                break

        sd_patterns = [
            r'standard\s+deviation\s*=|sd\s*=',
            r'√|sqrt|square\s+root',
            r'variance',
            r'σ\s*=',
            r'\(x\s*-\s*mean\)|\(x\s*-\s*μ\)'
        ]
        for pattern in sd_patterns:
            if re.search(pattern, text_lower):
                calculations_found["sd_formula"] = True
                evidence.append("Found standard deviation formula or reference")
                break

        if re.search(r'\d+\.\d+|≈|approximately', student_answer):
            calculations_found["sd_calculation"] = True
            evidence.append("Found numerical SD calculation results")

        work_patterns = [
            r'calculation:|verify:|check:',
            r'mean\s*=\s*\d+',
            r'median\s*=\s*\d+',
            r'sd\s*=\s*\d+',
            r'=\s*\d+\.\d+'
        ]
        work_count = sum(1 for pattern in work_patterns if re.search(pattern, text_lower))
        if work_count >= 3:
            calculations_found["shows_work"] = True
            evidence.append(f"Found {work_count} instances of showing work")

        return {
            "calculations_found": calculations_found,
            "evidence": evidence if evidence else ["No calculations or formulas found"]
        }

    def extract_and_verify_data_sets(self, student_answer: str) -> dict:
        """
        Extract data sets from student answer and verify their statistical properties.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with verification results for parts a, b, c
        """
        import re
        from statistics import mean, median, stdev

        results = {
            "part_a": {"valid": False, "details": "Not found or not analyzed"},
            "part_b": {"valid": False, "details": "Not found or not analyzed"},
            "part_c": {"valid": False, "details": "Not found or not analyzed"}
        }

        # Helper function to extract numbers from a line
        def extract_numbers(text):
            # Look for sequences of numbers separated by commas or spaces
            numbers = re.findall(r'-?\d+(?:\.\d+)?', text)
            return [float(n) for n in numbers]

        # Helper function to find data sets in a section
        def find_data_sets_in_section(section_text):
            data_sets = []
            lines = section_text.split('\n')
            for line in lines:
                if '(' not in line:
                    continue
                before_paren = line.split('(')[0]
                before_paren = re.sub(r'^\s*\d+\.\s*', '', before_paren)
                pattern = r'(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)'
                matches = re.findall(pattern, before_paren)
                for match in matches:
                    numbers = [float(n) for n in match]
                    data_sets.append(numbers)
                    break
            return data_sets

        # Split answer into parts
        text_lower = student_answer.lower()

        # Find part a
        # Find part a
        part_a_match = re.search(r'(?:a[\.\):]|part\s+a)', text_lower)
        part_b_match = re.search(r'(?:b[\.\):]|part\s+b)', text_lower)
        part_c_match = re.search(r'(?:c[\.\):]|part\s+c)', text_lower)

        # Extract part a
        if part_a_match:
            start = part_a_match.start()
            end = part_b_match.start() if part_b_match else len(student_answer)
            part_a_text = student_answer[start:end]
            data_sets_a = find_data_sets_in_section(part_a_text)

            if len(data_sets_a) >= 3:
                try:
                    means = [mean(ds) for ds in data_sets_a[:3]]
                    stdevs = [stdev(ds) for ds in data_sets_a[:3]]

                    means_equal = all(abs(m - means[0]) < 0.1 for m in means)
                    stdevs_different = len(set(round(s, 1) for s in stdevs)) >= 2

                    if means_equal and stdevs_different:
                        results["part_a"]["valid"] = True
                        results["part_a"][
                            "details"] = f"Valid: means={[round(m, 2) for m in means]}, SDs={[round(s, 2) for s in stdevs]}"
                    else:
                        results["part_a"][
                            "details"] = f"Invalid: means_equal={means_equal}, SDs_different={stdevs_different}, means={[round(m, 2) for m in means]}"
                except:
                    results["part_a"]["details"] = "Error calculating statistics"
            else:
                results["part_a"]["details"] = f"Found only {len(data_sets_a)} data sets, need 3"

        # Extract part b
        if part_b_match:
            start = part_b_match.start()
            end = part_c_match.start() if part_c_match else len(student_answer)
            part_b_text = student_answer[start:end]
            data_sets_b = find_data_sets_in_section(part_b_text)

            if len(data_sets_b) >= 3:
                try:
                    means = [mean(ds) for ds in data_sets_b[:3]]
                    medians = [median(ds) for ds in data_sets_b[:3]]

                    means_equal = all(abs(m - means[0]) < 0.1 for m in means)
                    medians_different = len(set(round(m, 1) for m in medians)) >= 2

                    if means_equal and medians_different:
                        results["part_b"]["valid"] = True
                        results["part_b"][
                            "details"] = f"Valid: means={[round(m, 2) for m in means]}, medians={[round(m, 2) for m in medians]}"
                    else:
                        results["part_b"][
                            "details"] = f"Invalid: means_equal={means_equal}, medians_different={medians_different}, means={[round(m, 2) for m in means]}, medians={[round(m, 2) for m in medians]}"
                except:
                    results["part_b"]["details"] = "Error calculating statistics"
            else:
                results["part_b"]["details"] = f"Found only {len(data_sets_b)} data sets, need 3"

        # Extract part c
        if part_c_match:
            start = part_c_match.start()
            part_c_text = student_answer[start:]
            data_sets_c = find_data_sets_in_section(part_c_text)

            if len(data_sets_c) >= 3:
                try:
                    means = [mean(ds) for ds in data_sets_c[:3]]
                    medians = [median(ds) for ds in data_sets_c[:3]]

                    medians_equal = all(abs(m - medians[0]) < 0.1 for m in medians)
                    means_different = len(set(round(m, 1) for m in means)) >= 2

                    if medians_equal and means_different:
                        results["part_c"]["valid"] = True
                        results["part_c"][
                            "details"] = f"Valid: medians={[round(m, 2) for m in medians]}, means={[round(m, 2) for m in means]}"
                    else:
                        results["part_c"][
                            "details"] = f"Invalid: medians_equal={medians_equal}, means_different={means_different}, medians={[round(m, 2) for m in medians]}, means={[round(m, 2) for m in means]}"
                except:
                    results["part_c"]["details"] = "Error calculating statistics"
            else:
                results["part_c"]["details"] = f"Found only {len(data_sets_c)} data sets, need 3"

        return results

    def grade_data_sets(self, student_answer: str, test_mode: bool = False):
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 1,
                    "component_2_score": 6,
                    "component_3_score": 7,
                    "component_4_score": 6
                },
                max_points=20,
                feedback="Test mode feedback for data sets creation task.",
                vibe="Test mode vibe assessment",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "task_description": True,
                            "part_a_mentioned": True,
                            "part_b_mentioned": True,
                            "part_c_mentioned": True
                        },
                        "evidence": ["Test mode - all elements present"]
                    },
                    "calculation_check": {
                        "calculations_found": {
                            "mean_formula": True,
                            "mean_calculation": True,
                            "median_explanation": True,
                            "sd_formula": True,
                            "sd_calculation": True,
                            "shows_work": True
                        },
                        "evidence": ["Test mode - all calculations present"]
                    }
                }
            )

        formatting_check = self.check_formatting_elements(student_answer)
        calculation_check = self.check_calculations_and_formulas(student_answer)
        verification_check = self.extract_and_verify_data_sets(student_answer)

        part_a_penalty = 0
        if not verification_check['part_a']['valid']:
            part_a_penalty = 1

        part_b_penalty = 0
        if not verification_check['part_b']['valid']:
            part_b_penalty = 1

        part_c_penalty = 0
        if not verification_check['part_c']['valid']:
            part_c_penalty = 1

        prompt = f"""You are grading a statistics homework assignment where students must create three different sets of data sets with specific statistical properties.

        **TASK DESCRIPTION:**
        Make up three data sets with 5 numbers each that have:
        a. the same mean but different standard deviations.
        b. the same mean but different medians.
        c. the same median but different means.

        **RUBRIC (20 points total):**

        **Component 1: Task Description (1 point)**
        - 1 point: Task description is copied/included before the answer
        - 0 points: Task description is missing

        **Component 2: Part a - Same Mean, Different Standard Deviations (6 points)**
        Base requirement: Creates THREE valid data sets, each with 5 numbers, where all three data sets have the SAME mean and DIFFERENT standard deviations.

        Scoring:
        - 6 points: All requirements met PLUS shows complete calculations (mean formula/calculation AND SD formula/calculation for all three sets)
        - 5 points: All requirements met but missing ONE calculation element (e.g., shows means but not SDs, or shows formulas but not actual calculations)
        - 4 points: All requirements met but missing TWO calculation elements
        - 3 points: All requirements met but missing THREE or more calculation elements (only states final values)
        - 2 points: Creates valid data sets but requirements not fully met (means not equal OR SDs not different) OR only two data sets instead of three
        - 1 point: Attempts the problem but data sets are incorrect
        - 0 points: Missing or no valid attempt
        
        After determining the score, subtract the part_a_penalty: {part_a_penalty} point(s) for incorrect calculations.

        **Component 3: Part b - Same Mean, Different Medians (7 points)**
        Base requirement: Creates THREE valid data sets, each with 5 numbers, where all three data sets have the SAME mean and DIFFERENT medians.
        
        IMPORTANT: If automatic verification shows part_b is invalid, apply a 1-point penalty to the final Component 3 score (minimum 0).
                
        Scoring:
        - 7 points: All requirements met PLUS shows complete calculations (mean formula/calculation AND median identification/explanation for all three sets)
        - 6 points: All requirements met but missing ONE calculation element
        - 5 points: All requirements met but missing TWO calculation elements
        - 4 points: All requirements met but missing THREE or more calculation elements (only states final values)
        - 3 points: Creates valid data sets but requirements not fully met (means not equal OR medians not different) OR only two data sets instead of three
        - 2 points: Attempts the problem but data sets are incorrect
        - 1 point: Minimal attempt
        - 0 points: Missing or no valid attempt

        **Component 4: Part c - Same Median, Different Means (6 points)**
        Base requirement: Creates THREE valid data sets, each with 5 numbers, where all three data sets have the SAME median and DIFFERENT means.

        Scoring:
        - 6 points: All requirements met PLUS shows complete calculations (median identification/explanation AND mean formula/calculation for all three sets)
        - 5 points: All requirements met but missing ONE calculation element
        - 4 points: All requirements met but missing TWO calculation elements
        - 3 points: All requirements met but missing THREE or more calculation elements (only states final values)
        - 2 points: Creates valid data sets but requirements not fully met (medians not equal OR means not different) OR only two data sets instead of three
        - 1 point: Attempts the problem but data sets are incorrect
        - 0 points: Missing or no valid attempt
        
        After determining the score, subtract the part_b_penalty: {part_b_penalty} point(s) for incorrect calculations.

        **STUDENT ANSWER:**
        {student_answer}

        **AUTOMATIC FORMATTING DETECTION RESULT:**
        Elements Found: {formatting_check['elements_found']}
        Evidence: {formatting_check['evidence']}

        **AUTOMATIC CALCULATION DETECTION RESULT:**
        Calculations Found: {calculation_check['calculations_found']}
        Evidence: {calculation_check['evidence']}

       **AUTOMATIC VERIFICATION RESULT:**
        Part a verification: {verification_check['part_a']}
        Part b verification: {verification_check['part_b']}
        Part c verification: {verification_check['part_c']}
        
        **CRITICAL GRADING RULES:**
        1. Each part (a, b, c) requires THREE data sets, not two
        2. Each data set must have exactly 5 numbers
        3. VERIFY the mathematical requirements are actually met by calculating yourself if needed
        4. DEDUCT 1 POINT for each missing calculation element:
           - Missing mean formula or calculation
           - Missing median explanation or identification
           - Missing SD formula or calculation
           - Only stating final values without showing work
        5. Maximum deduction for missing calculations per component: 3 points
        6. A student can get at most 3/6 points if data sets are correct but NO calculations are shown
        7. Be strict on Components 1-2 (formatting requirements)
        8. Statistical correctness is mandatory - if numbers don't meet requirements, score cannot exceed 2 points for that component

        **CALCULATION REQUIREMENTS BY PART:**
        Part a: Must show mean calculation/formula AND standard deviation calculation/formula for each set
        Part b: Must show mean calculation/formula AND median identification/explanation for each set
        Part c: Must show median identification/explanation AND mean calculation/formula for each set

        **SCORING PROCESS:**
        1. Score Component 1 (Task Description): __/1
        2. Score Component 2 (Part a): __/6
           - Start with 6 if data sets are correct
           - Deduct 1 point for EACH missing: mean calculation, SD calculation, formulas/reasoning
           - THEN subtract part_a_penalty ({part_a_penalty} points) if calculations are mathematically incorrect
           - Minimum 0, maximum 6
        3. Score Component 3 (Part b): __/7
           - Start with 7 if data sets are correct
           - Deduct 1 point for EACH missing: mean calculation, median explanation, formulas/reasoning
           - THEN subtract part_b_penalty ({part_b_penalty} points) if calculations are mathematically incorrect
           - Minimum 0, maximum 7
        4. Score Component 4 (Part c): __/6
           - Start with 6 if data sets are correct
           - Deduct 1 point for EACH missing: median explanation, mean calculation, formulas/reasoning
           - THEN subtract part_c_penalty ({part_c_penalty} points) if calculations are mathematically incorrect
           - Minimum 0, maximum 6
        5. Total = sum of four scores (max 20)

        **FEEDBACK STRUCTURE:**
        Provide narrative feedback that:
        - Identifies which formatting elements are missing
        - For each part (a, b, c), states whether data sets meet statistical requirements
        - EXPLICITLY identifies which calculations/formulas are missing
        - Counts how many calculation elements are absent and explains the point deduction
        - Notes if student only provided final values without showing work
        - Identifies any mathematical errors in calculations
        - Remains constructive and encourages showing complete work

        Return your grading in this exact JSON format:
        {{
          "component_1_score": <0-1>,
          "component_1_explanation": "<if score < full points: one sentence explaining what's missing; if full points AND exceptional work: one sentence of praise; otherwise empty string>",
          "component_2_score": <0-6>,
          "component_2_explanation": "<REQUIRED: Always provide explanation. If score < 6: state what calculations are missing AND if penalty applied for incorrect math (e.g., 'Missing mean calculations, -2 points; Incorrect calculation results verified, -1 point'); if score = 6: confirm all calculations shown and verified correct>",
          "component_3_score": <0-7>,
          "component_3_explanation": "<REQUIRED: Always provide explanation. If score < 7: state what calculations are missing AND if penalty applied for incorrect math; if score = 7: confirm all calculations shown and verified correct>",
          "component_4_score": <0-6>,
          "component_4_explanation": "<REQUIRED: Always provide explanation. If score < 6: state what calculations are missing AND if penalty applied for incorrect math; if score = 6: confirm all calculations shown and verified correct>",
          "total_points": <sum of above, 0-20>,
          "max_points": 20,
          "percentage": <percentage>,
          "feedback": "<narrative explanation covering: (1) formatting compliance, (2) statistical correctness of data sets, (3) completeness of calculations and formulas for each part, (4) specific count of missing calculation elements>",
          "vibe": "<one-sentence assessment of student's understanding and work quality, noting whether they demonstrate understanding through calculations or just provide answers>"
        }}"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "formatting_check": formatting_check,
                "calculation_check": calculation_check,
                "verification_check": verification_check
            }
        )

        # Add verification_check to result so it appears in output
        if "error" not in result:
            result["verification_check"] = verification_check

        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        print("=" * 60)
        print("GRADING RESULTS - HW3_2")
        print("Data Sets Creation - Mean, Median, Standard Deviation")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Task Description): {grading.get('component_1_score', 'N/A')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")
            print(f"  Component 2 (Part a - Same Mean, Different SD): {grading.get('component_2_score', 'N/A')}/6")
            if grading.get('component_2_explanation'):
                wrapped_exp2 = textwrap.fill(grading.get('component_2_explanation'), width=54, initial_indent="    → ",
                                             subsequent_indent="      ")
                print(wrapped_exp2)
            print(f"  Component 3 (Part b - Same Mean, Different Medians): {grading.get('component_3_score', 'N/A')}/7")
            if grading.get('component_3_explanation'):
                wrapped_exp3 = textwrap.fill(grading.get('component_3_explanation'), width=54, initial_indent="    → ",
                                             subsequent_indent="      ")
                print(wrapped_exp3)
            print(f"  Component 4 (Part c - Same Median, Different Means): {grading.get('component_4_score', 'N/A')}/6")
            if grading.get('component_4_explanation'):
                wrapped_exp4 = textwrap.fill(grading.get('component_4_explanation'), width=54, initial_indent="    → ",
                                             subsequent_indent="      ")
                print(wrapped_exp4)
            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points', 'N/A')}/{grading.get('max_points', 20)}")
        print(f"PERCENTAGE: {grading.get('percentage', 'N/A')}%")

        print("\n" + "=" * 60)
        print("FEEDBACK:")
        print("=" * 60)
        feedback_text = grading.get('feedback', 'No feedback available')
        wrapped_feedback = textwrap.fill(feedback_text, width=60)
        print(wrapped_feedback)

        print("\n" + "=" * 60)
        print("THE VIBE:")
        print("=" * 60)
        vibe_text = grading.get('vibe', 'N/A')
        wrapped_vibe = textwrap.fill(vibe_text, width=60)
        print(wrapped_vibe)

        if 'error' in grading:
            print("\n" + "=" * 60)
            print("ERROR:")
            print("=" * 60)
            print(grading.get('error'))
            if 'raw_response' in grading:
                print("\nRaw Response:")
                print(grading['raw_response'][:500])

if __name__ == "__main__":
    print("Welcome to the Homework AI Evaluator System!")
    print("=" * 60)

    # Initialize evaluator
    evaluator = HW3_2Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("HOMEWORK 3 - QUESTION 3_2 EVALUATOR")
    print("Data Sets Creation - Mean, Median, Standard Deviation")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION 3_2.")
    print("(Press Enter twice when finished, or type 'END' on a new line)\n")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        lines.append(line)
        # Check if last two lines are empty (double Enter)
        if len(lines) >= 2 and lines[-1] == '' and lines[-2] == '':
            lines = lines[:-2]  # Remove the two empty lines
            break

    student_answer = '\n'.join(lines)

    # Validate input
    if not student_answer.strip():
        print("\n❌ Error: No answer provided. Exiting.")
        exit(1)

    print("\n" + "=" * 60)
    print("EVALUATING...")
    print("=" * 60)

    # Grade with Groq API
    grading = evaluator.grade_data_sets(student_answer)

    # Display results
    evaluator.print_grading_results(grading)