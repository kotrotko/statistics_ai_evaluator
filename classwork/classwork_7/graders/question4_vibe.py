from groq import Groq
import os
import json
import re

class Question4Evaluator:
    def __init__(self):
        """Initialize the evaluator with Groq API key."""
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Please set GROQ_API_KEY environment variable")

        self.client = Groq(api_key=self.api_key)

    def grade_wilcoxon_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade a student's Wilcoxon answer using Vibe-approach.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        # Test mode for verification without API
        if test_mode:
            return {
                "total_points": 16,
                "max_points": 20,
                "percentage": 80.0,
                "feedback": "[TEST MODE] Strong statistical understanding demonstrated. Table and plot are well-presented with proper interpretations.",
                "vibe": "Student clearly gets it - solid work overall"
            }

        prompt = f"""You are grading a statistics assignment using the **Vibe-approach** - holistic grading that focuses on overall understanding and quality rather than strict checklist marking.

The assignment asks students to:
- Include Wilcoxon table (V, p) (5 points)
- Number it and title it in APA style (5 points)  
- Interpret it (5 points)
- Include Descriptive plot with confidence interval 95% (5 points)

Total: 20 points

STUDENT ANSWER:
{student_answer}

IMPORTANT NOTE ABOUT VISUAL ELEMENTS:
Students submit their work with images, plots, and figures, but this text-only interface cannot capture visual elements. If the student REFERENCES a figure, plot, or table (e.g., "Figure 1", "as shown in the plot", "see Table 3 below", "the graph shows"), you should ASSUME the visual element exists in their original submission.

Grade based on:
1. Whether they reference the visual element (shows they included it)
2. How well they DESCRIBE what the visual shows
3. How well they INTERPRET the visual element

Do NOT penalize students for "missing" plots/figures if they clearly reference and discuss them in their text.

Using the Vibe-approach, evaluate this work holistically:

**What is Vibe-approach grading?**
- Focus on whether the student *understands* the material, not just whether they hit every checkbox
- Consider the overall quality and coherence of their work
- Reward demonstration of statistical thinking
- Be generous with minor formatting issues if the substance is solid
- Think: "Does this student get it?" rather than "Did they do exactly X, Y, Z?"

**Key Questions:**
1. Did they include/reference the Wilcoxon results (V and p-value)?
2. Is there reasonable table presentation or reference (even if not perfectly APA)?
3. Do they understand what the results mean statistically?
4. Is there evidence of a plot with confidence intervals (referenced, described, or discussed)?

Grade based on the **overall impression** of competence and understanding. A student who clearly understands the material but has minor formatting issues should score well. A student with perfect formatting but no understanding should not.

**IMPORTANT - Provide Narrative Explanation:**
In your feedback, explain your score in narrative form. Tell the story of this student's work:
- What did they do well? (Be specific about strengths)
- What could be stronger? (Be specific about areas for improvement)
- Why this score and not higher/lower?

Use natural language, not bullet points or score breakdowns. Think: "If a student asked me 'Why did I get this score?', what would I say in a conversation?"

Return your grading in this exact JSON format:
{{
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative explanation of the score - tell the story of their work, what's strong, what could be better, and why this score>",
  "vibe": "<one-sentence overall impression: does this student get it?>"
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
        print("GRADING RESULTS - QUESTION 4 (VIBE-APPROACH)")
        print("=" * 60)
        print(f"\nSCORE: {grading.get('total_points', 'N/A')}/{grading.get('max_points', 20)}")
        print(f"PERCENTAGE: {grading.get('percentage', 'N/A')}%")

        print("\n" + "=" * 60)
        print("FEEDBACK:")
        print("=" * 60)
        print(grading.get('feedback', 'No feedback available'))

        print("\n" + "=" * 60)
        print("THE VIBE:")
        print("=" * 60)
        print(grading.get('vibe', 'N/A'))

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
    evaluator = Question4Evaluator()

    # Mock student answer for testing (commented out)
    # student_answer = """
    # I used the One-Sample T-Test under the T-Test module in JASP. The Wilcoxon signed-rank test gave a test statistic of V = 51.50 with p = .649. Since the p-value is much larger than the significance level (α = .05), we fail to reject the null hypothesis. This means that men's gardening scores are not significantly different from the test value of 73 (Table 3).
    #
    # Table 3
    # Wilcoxon Signed-Rank Test Results for GulzhigitBek Dataset (N = 16)
    # V    p
    # V65        51.500        .649
    #
    # Note. The Wilcoxon signed-rank test compared men's gardening scores against the test value of 73.
    #
    # I ticked Descriptive Plots under the Plots section in JASP. The descriptive plot shows that the sample mean (68.63) is below the test value of 73. The vertical bar shows the 95% confidence interval around the mean, and it crosses the dashed line at 73. This means the sample mean is not clearly different from 73, which matches the Wilcoxon result: V = 51.50, p = .649 (Figure 2).
    #
    # Figure 1
    # Descriptive plot with 95% confidence interval for men's gardening scores compared to the test value of 73
    #
    # Note. The black dot represents the sample mean (68.63). The vertical bar shows the 95% confidence interval. The dashed line marks the test value of 73.
    # """

    # Prompt user for student's answer
    print("=" * 60)
    print("QUESTION 4 EVALUATOR - VIBE-APPROACH")
    print("=" * 60)
    print("\nPlease enter the student's answer to Question 4.")
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
    grading = evaluator.grade_wilcoxon_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)