from groq import Groq
import os
import json
import re

class Question2Evaluator:
    def __init__(self):
        """Initialize the evaluator with Groq API key."""
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Please set GROQ_API_KEY in the code above")

        self.client = Groq(api_key=self.api_key)

    def grade_statistics_answer(self, student_answer: str, test_mode: bool = False) -> dict:
        """
        Grade a student's normality test answer using vibe coding approach.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        # Test mode for verification without API
        if test_mode:
            return {
                "method_points": 5,
                "table_points": 4,
                "conclusion_points": 0,
                "reasoning_points": 1,
                "total_points": 10,
                "feedback": "[TEST MODE] Method: 5/5 - Shapiro-Wilk test correctly identified. Table: 4/5 - Results provided (W=0.786, p=0.002) but no formal table format. Conclusion: 0/5 - No explicit statement about whether distribution is normal at α=0.001. Reasoning: 1/5 - Interpretation present but fundamentally wrong; at α=0.001, p=0.002 > α means FAIL to reject H₀, so distribution IS normal, not non-normal as student concluded.",
                "key_issue": "Student did not explicitly state conclusion about normality and misinterpreted the hypothesis test result at α=0.001"
            }

        rubric = """
        GRADING RUBRIC (Total: 20 points):
        1. Method selection (5 points): Did they choose an appropriate normality test?
        2. Table/Results (5 points): Did they provide the test statistic and p-value?
        3. Conclusion at α = 0.001 (5 points): Did they correctly interpret with the given significance level?
        4. Reasoning (5 points): Did they explain their logic clearly and correctly?
        """

        student_submission = f"""
        STUDENT ANSWER:
        {student_answer}
        """

        prompt = f"""You are grading a statistics assignment about normality testing.

{rubric}

{student_submission}

Grade this answer EXACTLY according to these strict criteria:

**1. Method (5 points)**: 
- 5/5: Appropriate normality test mentioned (Shapiro-Wilk, Kolmogorov-Smirnov, Anderson-Darling)
- 0/5: Wrong method or no method

**2. Table/Results (5 points)**:
- 5/5: Both test statistic AND p-value provided in a formatted table
- 4/5: Both test statistic AND p-value provided, but NO formal table (just text)
- 3/5: Only one of (test statistic OR p-value) provided
- 0/5: No results provided

**3. Conclusion about normality at α = 0.001 (5 points)**:
CRITICAL: At α = 0.001, if p = 0.002:
- p (0.002) > α (0.001) → FAIL TO REJECT H₀ → Distribution IS NORMAL
- 5/5: Correct conclusion (distribution is normal at α = 0.001)
- 0/5: Wrong conclusion OR no explicit statement about normality

**4. Reasoning/Interpretation (5 points)**:
- 5/5: Clear, correct explanation of why conclusion follows from p-value and α
- 3/5: Attempt at interpretation but with minor errors
- 1/5: Interpretation present but fundamentally wrong (e.g., misinterprets hypothesis test)
- 0/5: No interpretation or reasoning provided

GRADING EXAMPLE FOR REFERENCE:
Student answer: "Method: Shapiro-Wilk. W = 0.786, p = 0.002. p is small so not normal. Use Wilcoxon instead."
Correct grading:
- Method: 5/5 (Shapiro-Wilk mentioned)
- Table: 4/5 (results given but no table format)
- Conclusion: 0/5 (no explicit statement about normality at α = 0.001)
- Reasoning: 1/5 (interpretation exists but wrong - at α = 0.001, distribution IS normal)
Total: 10/20

Return your grading in this exact JSON format:
{{
  "method_points": <0-5>,
  "table_points": <0-5>,
  "conclusion_points": <0-5>,
  "reasoning_points": <0-5>,
  "total_points": <sum>,
  "feedback": "<detailed feedback explaining each score, referencing the criteria>",
  "key_issue": "<main problem if any>"
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
                model="llama-3.3-70b-versatile",  # You can also use "mixtral-8x7b-32768"
                temperature=0.3,  # Lower temperature for more consistent grading
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
        print("GRADING RESULTS")
        print("=" * 60)
        print(f"Method: {grading.get('method_points', 'N/A')}/5")
        print(f"Table: {grading.get('table_points', 'N/A')}/5")
        print(f"Conclusion: {grading.get('conclusion_points', 'N/A')}/5")
        print(f"Reasoning: {grading.get('reasoning_points', 'N/A')}/5")
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
    evaluator = Question2Evaluator()

    # Mock student answer for testing (commented out)
    # student_answer = """
    # Method used: Shapiro-Wilk test. (5/5).
    # Result: W = 0.786, p = 0.002.
    # Interpretation with α = 0.001: However, p = 0.002 is a small value that would be
    # considered significant at α = 0.05.
    # Since the value is close to the threshold and the data exhibit some outliers,
    # I use the nonparametric Wilcoxon signed-rank test, which does not require normality.
    # """

    # Prompt user for student's answer
    print("=" * 60)
    print("STATISTICS ANSWER EVALUATOR")
    print("=" * 60)
    print("\nPlease enter the student's answer to Question 2.")
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
    grading = evaluator.grade_statistics_answer(student_answer)
    evaluator.print_grading_results(grading)