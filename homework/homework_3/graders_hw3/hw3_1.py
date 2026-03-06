"""
hw3_1.py
Mean, Median, Mode Sensitivity Comparison Evaluator
"""

import re
import textwrap

from config import BaseEvaluator


class HW3_1Evaluator(BaseEvaluator):
    """
    Evaluator for Mean, Median, Mode Sensitivity Comparison Question.

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    def __init__(self):
        """Initialize evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1200
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
            "student_name": False,
            "task_description": False,
            "mean_mentioned": False,
            "median_mentioned": False,
            "mode_mentioned": False
        }

        evidence = []

        # Check for student name
        name_patterns = [
            r'\bname\s*:',
            r'\bstudent\s*:',
            r'\bby\s+[A-Z][a-z]+\s+[A-Z][a-z]+',
            r'^[A-Z][a-z]+\s+[A-Z][a-z]+'
        ]
        for pattern in name_patterns:
            if re.search(pattern, student_answer, re.MULTILINE):
                elements_found["student_name"] = True
                evidence.append(f"Found name indication: {pattern}")
                break

        # Check for task description
        task_patterns = [
            r'compare.*mean.*median.*mode',
            r'sensitivity.*extreme\s+scores',
            r'task\s*:',
            r'question\s*:'
        ]
        for pattern in task_patterns:
            if re.search(pattern, text_lower):
                elements_found["task_description"] = True
                evidence.append(f"Found task description: {pattern}")
                break

        # Check if each measure is mentioned
        if re.search(r'\bmean\b', text_lower):
            elements_found["mean_mentioned"] = True
            evidence.append("Mean is discussed")

        if re.search(r'\bmedian\b', text_lower):
            elements_found["median_mentioned"] = True
            evidence.append("Median is discussed")

        if re.search(r'\bmode\b', text_lower):
            elements_found["mode_mentioned"] = True
            evidence.append("Mode is discussed")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear formatting elements found"]
        }

    def grade_sensitivity_comparison(self, student_answer: str, test_mode: bool = False):
        """
        Grade Mean, Median, Mode sensitivity comparison question.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API

        Returns:
            Detailed grading breakdown dictionary
        """
        # Test mode - use base class method
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 1,
                    "component_2_score": 1,
                    "component_3_score": 6,
                    "component_4_score": 6,
                    "component_5_score": 6
                },
                max_points=20,
                feedback="Test mode feedback for sensitivity comparison task.",
                vibe="Test mode vibe assessment",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "student_name": True,
                            "task_description": True,
                            "mean_mentioned": True,
                            "median_mentioned": True,
                            "mode_mentioned": True
                        },
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        # Check for formatting elements
        formatting_check = self.check_formatting_elements(student_answer)

        # Build the grading prompt
        prompt = f"""You are grading a statistics homework assignment where students must compare the mean, median, and mode in terms of their sensitivity to extreme scores.

**TASK DESCRIPTION:**
Compare the mean, median, and mode in terms of their sensitivity to extreme scores.

**RUBRIC (20 points total):**

**Component 1: Student Name (1 point)**
- 1 point: Student's name is included
- 0 points: Name is missing

**Component 2: Task Description (1 point)**
- 1 point: Task description is copied/included before the answer
- 0 points: Task description is missing

**Component 3: Mean's Sensitivity to Extreme Scores (6 points)**
- 6 points: Correctly explains that mean IS highly sensitive to extreme scores
  * Should explain WHY: mean uses all values in calculation (sum/n)
  * Extreme values directly affect the sum, thus changing the mean significantly
- 4-5 points: Correct conclusion but explanation lacks depth or clarity
- 2-3 points: Partially correct or very vague explanation
- 0-1 points: Incorrect or missing

**Component 4: Median's Sensitivity to Extreme Scores (6 points)**
- 6 points: Correctly explains that median is LESS sensitive/MORE resistant to extreme scores than the mean
  * Should explain WHY: median is the middle value, position-based
  * Can shift when extreme values change the dataset composition or which value occupies the middle position
  * Extreme values affect it minimally compared to mean
- 4-5 points: Correct conclusion but explanation lacks depth or clarity
- 2-3 points: Partially correct or very vague explanation
- 0-1 points: Incorrect or missing

**Component 5: Mode's Sensitivity to Extreme Scores (6 points)**
- 6 points: Correctly explains that mode is NOT sensitive to extreme scores
  * Should explain WHY: mode is the most frequent value
  * Extreme values don't change which value appears most often
- 4-5 points: Correct conclusion but explanation lacks depth or clarity
- 2-3 points: Partially correct or very vague explanation
- 0-1 points: Incorrect or missing

**Component 6: Overall Sensitivity Ranking (APPRECIATION ONLY - 0 points)**
- If student explicitly provides the correct sensitivity ranking/hierarchy, note this in feedback as excellent synthesis
  * States that Mean is MOST sensitive > Median is MODERATELY sensitive > Mode is LEAST sensitive
  * Can be stated anywhere in the answer
  * Examples: "In order of sensitivity: mean > median > mode" or "Mode is least affected, median somewhat affected, mean most affected"
- This component awards NO POINTS but should be acknowledged in the "vibe" or "feedback" sections as strong conceptual understanding

**STUDENT ANSWER:**
{student_answer}

**AUTOMATIC FORMATTING DETECTION RESULT:**
Elements Found: {formatting_check['elements_found']}
Evidence: {formatting_check['evidence']}

**GRADING GUIDELINES:**

For Component 1 (Name):
- Look for student's name anywhere in the submission
- 1 point if present, 0 if missing

For Component 2 (Task Description):
- Look for evidence that task description was copied
- Keywords: "compare", "mean, median, mode", "sensitivity", "extreme scores"
- 1 point if present, 0 if missing

For Component 3 (Mean's Sensitivity):
- CORRECT ANSWER: Mean IS highly sensitive to extreme scores
- WHY: Uses all values in calculation (sum divided by n), so extreme values directly affect the result
- Must discuss BOTH the conclusion AND the reasoning
- 5 points: Correct + clear explanation
- 3-4 points: Correct but weak explanation
- 1-2 points: Partially correct
- 0 points: Wrong or missing

For Component 4 (Median's Sensitivity):
- CORRECT ANSWER: Median is LESS sensitive to extreme scores than the mean but MORE sensitive than the mode
- WHY: Median is the middle value based on position - can be "pulled slightly out" into a skewed tail but remains closer to the bulk of the data
- Must explain why median is moderately resistant (less sensitive than mean)
- 6 points: Correct + clear explanation
- 4-5 points: Correct but weak explanation
- 2-3 points: Partially correct
- 1 point: Wrong but present in the answer
- 0 points: Missing

# SECTION: Component 5 Grading Guidelines (lines ~212-218)
# CHANGE: Simplified to prevent overly harsh grading

For Component 5 (Mode's Sensitivity):
- CORRECT ANSWER: Mode is NOT sensitive to extreme scores
- WHY: Mode is the most frequent value - extreme values don't change which value appears most often
- Must discuss BOTH the conclusion AND the reasoning
- DO NOT deduct points for not discussing edge cases or theoretical exceptions
- 4 points: Correct conclusion + reasonable explanation of why
- 2-3 points: Correct conclusion but vague/weak explanation
- 1 point: Partially correct
- 0 points: Wrong or missing

**CRITICAL RULES:**
1. Each measure must be evaluated separately based on the task description
2. Correct ranking: Mean (most sensitive) > Median (resistant) > Mode (not sensitive)
3. Students must explain WHY each measure has its sensitivity level, not just state it
4. Be strict on Component 1-2 (formatting requirements)
5. Award full points if student correctly identifies sensitivity AND explains the reasoning
6. For Components 3-5: If student correctly identifies the sensitivity level (sensitive/not sensitive) AND provides a reasonable explanation of WHY (uses all values, middle position, most frequent), award FULL points. Do not deduct points for not being overly detailed or not discussing theoretical edge cases.

**SCORING PROCESS:**
1. Score Component 1 (Name): __/1
2. Score Component 2 (Task Description): __/1
3. Score Component 3 (Mean's Sensitivity): __/6
4. Score Component 4 (Median's Sensitivity): __/6
5. Score Component 5 (Mode's Sensitivity): __/6
6. Evaluate Component 6 (Overall Ranking - appreciation only, no points)
7. Total = sum of five scores (max 20)

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- Identifies which formatting elements are missing
- Assesses accuracy of each measure's sensitivity explanation separately
- Notes whether student explained the WHY for each measure
- Remains constructive and educational

Return your grading in this exact JSON format:
{{
  "component_1_score": <0-1>,
  "component_1_explanation": "<if score < full points: one sentence explaining what's missing; if full points AND exceptional work: one sentence of praise; otherwise empty string>",
  "component_2_score": <0-1>,
  "component_2_explanation": "<if score < full points: one sentence explaining what's missing; if full points AND exceptional work: one sentence of praise; otherwise empty string>",
  "component_3_score": <0-6>,
  "component_3_explanation": "<if score < 5: one sentence explaining what's missing or incorrect about the mean explanation; if score = 5 AND exceptional work: one sentence of praise; otherwise empty string>",
  "component_4_score": <0-6>,
  "component_4_explanation": "<if score < 5: one sentence explaining what's missing or incorrect about the median explanation; if score = 5 AND exceptional work: one sentence of praise; otherwise empty string>",
  "component_5_score": <0-6>,
  "component_5_explanation": "<if score < 4: one sentence explaining what's missing or incorrect about the mode explanation; if score = 4 AND exceptional work: one sentence of praise; otherwise empty string>",
  "component_6_evaluation": <true/false>,
  "component_6_note": "<if true: brief positive note about providing comparative ranking; otherwise empty string>",
  "total_points": <sum of components 1-5, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative explanation - covering formatting compliance and accuracy of each measure's sensitivity explanation, if ranking was provided, mention it as evidence of strong synthesis>",
  "vibe": "<one-sentence overall impression of their understanding of measures of central tendency and their sensitivity to extreme scores, if ranking provided, acknowledge it as showing comprehensive understanding>"
}}"""

        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"formatting_check": formatting_check}
        )

        # If grading succeeded, validate component scores
        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score",
                "component_5_score"
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Helper function to display grading results"""
        print("=" * 60)
        print("GRADING RESULTS - HW3_1")
        print("Mean, Median, Mode Sensitivity Comparison")
        print("=" * 60)

        # Print component breakdown if available
        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Student Name): {grading.get('component_1_score', 'N/A')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Task Description): {grading.get('component_2_score', 'N/A')}/1")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Mean's Sensitivity): {grading.get('component_3_score', 'N/A')}/6")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Median's Sensitivity): {grading.get('component_4_score', 'N/A')}/6")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Mode's Sensitivity): {grading.get('component_5_score', 'N/A')}/6")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points', 'N/A')}/{grading.get('max_points', 16)}")
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
    evaluator = HW3_1Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("HOMEWORK 3 - QUESTION 3_1 EVALUATOR")
    print("Mean, Median, Mode Sensitivity Comparison")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION 3_1.")
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
    grading = evaluator.grade_sensitivity_comparison(student_answer)

    # Display results
    evaluator.print_grading_results(grading)