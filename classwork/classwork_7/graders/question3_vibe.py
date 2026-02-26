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
                "test_value_points": 0,
                "approach_points": 0,
                "table_points": 2,
                "mean_median_points": 3,
                "total_points": 5,
                "feedback": "[TEST MODE] Test Value: 0/5 - Not mentioned. Approach: 0/5 - Not answered. Table: 2/5 - (1) Table included ✓, (2) Not introduced ✗, (3) Not referred to ✗, (4) Numbered as 'Table 2' ✓, (5) 'Descriptives' is NOT an APA title ✗. Mean/Median: 3/5 - Mean provided (68.41), median missing.",
                "key_issue": "Missing test value, approach justification, table introduction/reference, proper APA title, and median value"
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

Grade this answer with careful attention to both substance and presentation:

**1. Test Value Identification and Source (5 points)**:
The student should identify the test value (73, representing the comparison value for women's indoor gardening scores) and explain where it comes from. Full points for clarity; partial credit if the identification or explanation is incomplete or unclear.

**2. Approach Selection and Justification (5 points)**:
The student should identify whether they used a parametric or non-parametric approach and explain why. Non-parametric (Wilcoxon) is expected here. Strong justifications might reference violated assumptions, data characteristics, or appropriateness for the research question. Weak or missing justifications lose points.

**3. Descriptive Statistics Table - APA Style (5 points)**:
A proper APA table has five key characteristics that work together:
- The table exists and contains the relevant statistics
- It's introduced in the text before it appears (e.g., "The descriptive statistics are presented below")
- It's referred to in the text (e.g., "As Table 2 shows...")
- It's numbered (Table 1, Table 2, etc.)
- It has a descriptive, informative title that tells readers what the table contains - NOT just "Descriptives" or "Table 2", but something like "Descriptive Statistics for Men's Indoor Gardening Test Scores"

Each missing element weakens the table presentation. Award points based on how many of these elements are present and how well-executed they are. A table with just a number and generic label ("Table 2: Descriptives") but no introduction or descriptive title would score low (around 2/5).

**4. Mean and Median Scores for Men (5 points)**:
Both values should be clearly provided. Full points for both, partial credit for only one, no points if neither is clear or if values are present but not identified as mean/median.

Grade holistically but precisely. Consider: Did the student demonstrate understanding? Is the presentation professional? Are key elements present?

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