from groq import Groq
import os
import json
import re

# GROQ API KEY
# os.environ["GROQ_API_KEY"] = "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"

class Question5Evaluator:
    def __init__(self):
        """Initialize the evaluator with Groq API key."""
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Please set GROQ_API_KEY environment variable")

        self.client = Groq(api_key=self.api_key)

    def grade_gender_culture_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade a student's gender and culture analysis using Vibe-approach.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        # Test mode for verification without API
        if test_mode:
            return {
                "total_points": 17,
                "max_points": 20,
                "percentage": 85.0,
                "feedback": "[TEST MODE] Excellent analysis of gender and cultural differences with proper effect size calculation and interpretation.",
                "vibe": "Student demonstrates strong understanding of intersectionality between gender and culture with solid statistical grounding"
            }

        prompt = f"""You are grading a statistics assignment using a **HYBRID approach** - vibe-based holistic grading with ONE strict component.

The assignment asks students to:
- Describe output briefly using the template from video (at 16:15) (5 points)
- Calculate and interpret the effect size (5 points)  
- Interpret findings - gender context (5 points)
- Interpret findings - cultural context (5 points)

Total: 20 points

STUDENT ANSWER:
{student_answer}

Using the HYBRID approach, evaluate this work:

**HYBRID Grading Philosophy:**
- **Components 1, 3a, 3b**: Use VIBE approach - holistic, generous, focus on understanding
- **Component 2 ONLY**: Use STRICT approach - effect size must be present to earn points

**VIBE APPROACH (Components 1, 3a, 3b):**
- Focus on whether the student *understands* the material
- Consider overall quality and coherence
- Reward demonstration of statistical and conceptual thinking
- Be generous with minor issues if the substance is solid
- Think: "Does this student get it?"

**STRICT APPROACH (Component 2 ONLY - Effect Size):**
- Effect size component requires BOTH calculation AND interpretation
- If BOTH are completely absent → 0 points
- If only calculation present (no interpretation) → 1-2 points maximum
- If only interpretation present (no calculation) → 1-2 points maximum
- If both present but weak → 3-4 points
- If both present and strong → 5 points

**Key Questions:**
1. **[VIBE]** Did they describe their output with statistical results? (means, p-values, conclusions)
2. **[STRICT]** Did they calculate an effect size (Cohen's d, rank-biserial, or other measure)?
3. **[STRICT]** Did they interpret what the effect size means (small/medium/large, practical significance)?
4. **[VIBE]** Do they show understanding of gender differences in the data?
5. **[VIBE]** Do they show understanding of cultural differences in the data?
6. **[VIBE]** Do they connect findings to meaningful interpretations about gender and culture?

**SCORING GUIDELINES:**

**Component 1: Output Description [VIBE] (0-5 points)**
- Does the student present their statistical findings clearly?
- Do they include key statistics (means, test results, p-values)?
- Is it coherent and understandable?
- Be generous - focus on substance over format

**Component 2: Effect Size [STRICT] (0-5 points)**
- **0 points**: No effect size calculation AND no interpretation
- **1-2 points**: Only calculation OR only interpretation (not both)
- **3-4 points**: Both calculation AND interpretation present but could be stronger
- **5 points**: Clear calculation AND meaningful interpretation of magnitude/significance
- **CRITICAL**: This component requires BOTH parts - one without the other cannot score above 2

**Component 3a: Gender Context [VIBE] (0-5 points)**
- Do they discuss what the findings mean for gender differences?
- Is the interpretation thoughtful and goes beyond surface level?
- Do they connect statistics to meaningful gender insights?
- Be generous - reward genuine understanding

**Component 3b: Cultural Context [VIBE] (0-5 points)**
- Do they discuss what the findings mean for cultural differences?
- Is the interpretation thoughtful and goes beyond surface level?
- Do they connect statistics to meaningful cultural insights?
- Be generous - reward genuine understanding

**CRITICAL RULES:**
1. **Component 2 (Effect Size) is STRICT**: If completely absent → 0 points. No exceptions.
2. **Components 1, 3a, 3b are VIBE**: Be holistic and generous if student shows understanding
3. **For Component 2**: Both calculation AND interpretation required for full credit
4. **For Components 1, 3a, 3b**: Focus on understanding over perfect execution

**Scoring Process:**
1. Score Component 1 (output description) with VIBE approach: __/5
2. Score Component 2 (effect size) with STRICT approach: __/5
3. Score Component 3a (gender context) with VIBE approach: __/5
4. Score Component 3b (cultural context) with VIBE approach: __/5
5. Total = sum of the four scores above

**What makes a strong answer:**
- Clear presentation of statistical results (means, p-values, test statistics, etc.)
- Effect size calculation with proper interpretation of magnitude and meaning
- Understanding of what effect size tells us beyond just statistical significance
- Thoughtful interpretation that goes beyond just stating "there is a difference"
- Understanding of what gender differences mean in context
- Understanding of what cultural differences mean in context
- Synthesis of both dimensions (how gender and culture interact)

**What to watch for:**
- Missing effect size calculation entirely
- Calculating effect size but not interpreting it
- Superficial interpretations (e.g., just saying "men and women are different")
- Missing connection between statistics and real-world meaning
- Confusion about what the data actually shows
- Lack of engagement with BOTH gender AND cultural contexts

**Effect Size Considerations:**
- Did they provide a numerical value (e.g., Cohen's d = 0.23, rank-biserial = 0.15)?
- Did they interpret the magnitude (small, medium, large, negligible)?
- Did they discuss practical vs. statistical significance?
- Even if they don't use formal effect size names, do they discuss the magnitude of difference?

**IMPORTANT - Provide Narrative Explanation:**
In your feedback, explain your score in narrative form:
- Start with overall strengths in the student's work
- Explain Component 2 (effect size) clearly - was it present? If not, state clearly this component was missing and received 0 points
- Discuss how well they addressed gender and cultural contexts (Components 3a, 3b)
- Mention the quality of their output description (Component 1)
- End with what would improve their score

Use natural language. Be constructive and encouraging while being clear about the strict Component 2 requirement.

Return your grading in this exact JSON format:
{{
  "component_1_score": <0-5>,
  "component_2_score": <0-5>,
  "component_3a_score": <0-5>,
  "component_3b_score": <0-5>,
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative explanation - tell the story of their work, emphasizing strengths in vibe components and being clear about effect size requirement>",
  "vibe": "<one-sentence overall impression>"
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

            # Verify total_points matches sum of components
            if all(key in result for key in
                   ['component_1_score', 'component_2_score', 'component_3a_score', 'component_3b_score']):
                calculated_total = (result['component_1_score'] +
                                    result['component_2_score'] +
                                    result['component_3a_score'] +
                                    result['component_3b_score'])
                result['total_points'] = calculated_total
                result['percentage'] = round((calculated_total / 20) * 100, 1)

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
        print("GRADING RESULTS - QUESTION 5 (HYBRID MODE)")
        print("=" * 60)

        # Print component breakdown if available
        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Output description): {grading.get('component_1_score', 'N/A')}/5")
            print(f"  Component 2 (Effect size): {grading.get('component_2_score', 'N/A')}/5")
            print(f"  Component 3a (Gender context): {grading.get('component_3a_score', 'N/A')}/5")
            print(f"  Component 3b (Cultural context): {grading.get('component_3b_score', 'N/A')}/5")
            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points', 'N/A')}/{grading.get('max_points', 20)}")
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
    evaluator = Question5Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("QUESTION 5 EVALUATOR - HYBRID MODE")
    print("Vibe Approach + Strict Effect Size Requirement")
    print("=" * 60)
    print("\nPlease enter the student's answer to Question 5.")
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
    grading = evaluator.grade_gender_culture_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)