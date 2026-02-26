from groq import Groq
import os
import json
import re

# GROQ API KEY
os.environ["GROQ_API_KEY"] = "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"


class Question3Evaluator:
    def __init__(self):
        """Initialize the evaluator with Groq API key."""
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Please set GROQ_API_KEY in the code above")

        self.client = Groq(api_key=self.api_key)

    def grade_wilcoxon_answer(self, student_answer: str, test_mode: bool = False) -> dict:
        """
        Grade a student's Wilcoxon Signed Rank test answer.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        # Test mode for verification without API
        if test_mode:
            return {
                "test_value_points": 3,
                "approach_points": 4,
                "table_points": 2,
                "mean_median_points": 5,
                "total_points": 14,
                "feedback": "[TEST MODE] Test Value: 3/5 - Value mentioned but source unclear. Approach: 4/5 - Non-parametric identified, reasoning partially correct. Table: 2/5 - Table present but formatting/APA issues. Mean/Median: 5/5 - Both values correctly identified.",
                "key_issue": "APA formatting and incomplete explanation of test value source"
            }

        rubric = """
        GRADING RUBRIC (Total: 20 points):
        1. Test Value identification and source (5 points): What is it and where does it come from?
        2. Approach selection and justification (5 points): Parametric or non-parametric, and why?
        3. Descriptive statistics table (5 points): APA formatting, numbering, title, proper introduction
        4. Mean and median for men (5 points): Correct values provided
        """

        student_submission = f"""
        STUDENT ANSWER:
        {student_answer}
        """

        prompt = f"""You are grading a statistics assignment about the Wilcoxon Signed Rank test.

{rubric}

{student_submission}

Grade this answer EXACTLY according to these strict criteria:

**1. Test Value Identification and Source (5 points)**:
- 5/5: Correctly identifies the test value (73, which is X̅ for women's indoor gardening score) AND clearly explains it comes from the problem/comparison value
- 3/5: Identifies the test value but explanation of source is unclear or incomplete
- 1/5: Test value mentioned but no source explanation
- 0/5: Test value not identified or wrong

**2. Approach Selection and Justification (5 points)**:
- 5/5: Correctly identifies non-parametric approach AND provides valid justification (e.g., normality violated, small sample, ordinal data, etc.)
- 4/5: Correctly identifies non-parametric but reasoning is incomplete or partially incorrect
- 2/5: Identifies approach but reasoning is mostly wrong
- 0/5: Wrong approach or no justification provided

**3. Descriptive Statistics Table (5 points)**:
This requires ALL of the following in APA style:
- Table is included
- Table is numbered (e.g., "Table 1")
- Table has a proper title
- Table is introduced/referenced in text before it appears
- Proper APA formatting (clear headers, aligned data)

Scoring:
- 5/5: All 5 elements present and correct
- 4/5: 4 elements present
- 3/5: 3 elements present
- 2/5: 2 elements present (table exists but poor formatting/missing elements)
- 1/5: Table mentioned or attempted but severely incomplete
- 0/5: No table provided

**4. Mean and Median Scores for Men (5 points)**:
- 5/5: Both mean AND median correctly provided for men
- 3/5: Only one value (mean OR median) provided correctly
- 1/5: Values mentioned but unclear which is which, or values appear incorrect
- 0/5: Neither value provided

Return your grading in this exact JSON format:
{{
  "test_value_points": <0-5>,
  "approach_points": <0-5>,
  "table_points": <0-5>,
  "mean_median_points": <0-5>,
  "total_points": <sum>,
  "feedback": "<detailed feedback explaining each score>",
  "key_issue": "<main problems if any>"
}}"""

        try:
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                max_tokens=1000,
            )

            # Extract the response text
            response_text = chat_completion.choices[0].message.content

            # Parse JSON from response (handle markdown code blocks)
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find JSON object in the response
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    json_str = response_text

            result = json.loads(json_str)
            return result

        except json.JSONDecodeError as e:
            return {
                "error": "Could not parse grading result",
                "raw_response": response_text,
                "parse_error": str(e)
            }
        except Exception as e:
            return {
                "error": "API call failed",
                "error_message": str(e)
            }

    def print_grading_results(self, grading):
        """Helper function to display grading results"""
        print("=" * 60)
        print("GRADING RESULTS - QUESTION 3")
        print("=" * 60)
        print(f"Test Value & Source: {grading.get('test_value_points', 'N/A')}/5")
        print(f"Approach & Justification: {grading.get('approach_points', 'N/A')}/5")
        print(f"Descriptive Table (APA): {grading.get('table_points', 'N/A')}/5")
        print(f"Mean & Median for Men: {grading.get('mean_median_points', 'N/A')}/5")
        print(f"\nTOTAL: {grading.get('total_points', 'N/A')}/20")
        print("\n" + "=" * 60)
        print("FEEDBACK:")
        print("=" * 60)
        print(grading.get('feedback', 'No feedback available'))

        if 'key_issue' in grading:
            print("\n" + "=" * 60)
            print("KEY ISSUE:")
            print("=" * 60)
            print(grading['key_issue'])

        if 'error' in grading:
            print("\n" + "=" * 60)
            print("ERROR:")
            print("=" * 60)
            print(grading.get('error'))
            if 'raw_response' in grading:
                print("\nRaw Response:")
                print(grading['raw_response'][:500])


# Example usage
if __name__ == "__main__":
    # Initialize evaluator
    evaluator = Question3Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("QUESTION 3 EVALUATOR - WILCOXON SIGNED RANK TEST")
    print("=" * 60)
    print("\nPlease enter the student's answer to Question 3.")
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

    # Grade immediately with Groq API
    grading = evaluator.grade_wilcoxon_answer(student_answer)
    evaluator.print_grading_results(grading)