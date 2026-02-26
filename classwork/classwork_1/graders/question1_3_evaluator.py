import os
import re
import json
from groq import Groq

# GROQ API KEY
# os.environ["GROQ_API_KEY"] = "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"


class Question1_3Evaluator:
    def __init__(self):
        """Initialize the evaluator with Groq API key."""
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Please set GROQ_API_KEY environment variable")

        self.client = Groq(api_key=self.api_key)

    def check_value_changes_mentioned(self, student_answer: str) -> dict:
        """
        Check if student mentions the specific value changes (11→5 and 15→23).
        Returns dict with: changes_mentioned (bool) and evidence (str)
        """
        # Look for patterns indicating the value changes
        patterns = [
            r'11\s*(?:to|→|->)\s*5',
            r'15\s*(?:to|→|->)\s*23',
            r'Adults11.*5',
            r'Teens3.*23',
            r'changed.*11.*5',
            r'changed.*15.*23'
        ]

        text_lower = student_answer.lower()
        found_changes = []

        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                found_changes.append(match.group())

        if found_changes:
            return {
                "changes_mentioned": True,
                "evidence": f"Found value change references: {', '.join(found_changes)}"
            }

        return {
            "changes_mentioned": False,
            "evidence": "No explicit mention of value changes (11→5, 15→23) found"
        }

    def grade_question1_3_answer(self, student_answer: str):
        """
        Grade Question 1_3: Excel editing and JASP comparison.
        Returns detailed grading breakdown with component-specific feedback.

        Args:
            student_answer: The student's response text
        """

        # Check if value changes are mentioned
        changes_check = self.check_value_changes_mentioned(student_answer)

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - combining vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Students must:
1. Edit LikeLike file in Excel (Adults11: 11→5, Teens3: 15→23), save as LikeLike_excel.xlsx, open in JASP, compare with Table 1 (5 points)
2. Introduce, refer to, number and title the second Descriptive Statistics table in APA style (5 points)
3. Copy the second Descriptive Statistics table in JASP format into their classwork file (5 points)
4. Describe the changes in one sentence (5 points)

Total: 20 points

STUDENT ANSWER:
{student_answer}

**AUTOMATIC VALUE CHANGE DETECTION RESULT:**
Changes Mentioned: {changes_check['changes_mentioned']}
Evidence: {changes_check['evidence']}

**IMPORTANT NOTES:**
- Students submit text descriptions since visual elements (Excel files, JASP tables) cannot be captured in text
- If student REFERENCES a table (e.g., "Table 2", "see table below", "the descriptive statistics table shows"), ASSUME the table exists in their actual document
- DO NOT penalize for "missing" tables/files if they clearly reference and discuss the content
- Focus on whether they understand what they're doing (editing data, comparing results, observing changes)

**HYBRID GRADING APPROACH:**

**Component 1: Excel editing, JASP analysis, and comparison with Table 1 - VIBE (0-5 points)**
- Focus: Does the student demonstrate they completed the editing task and compared results?
- Evidence of understanding:
  * Mentions editing Excel file (changing values)
  * References opening file in JASP
  * Shows awareness of comparison with Table 1 (original data)
  * Any indication they understand the workflow: Excel → Edit → Save → JASP → Compare
- Be generous: even indirect evidence of completing the task is acceptable
- 5 points: Clear evidence of completing all steps
- 3-4 points: Most steps mentioned, minor gaps
- 1-2 points: Minimal evidence of completing the task
- 0 points: No indication the editing/comparison was done

**Component 2: APA introduction, reference, numbering and naming of Table 2 - STRICT (0-5 points)**
- 0 points: No table introduction, reference, number, or title
- 2-3 points: Missing one or more elements (intro/reference/number/title)
- 4 points: Has all elements but minor APA formatting issues
- 5 points: Proper APA format with:
  * Introduction phrase (e.g., "Table 2 presents...")
  * Clear reference to the table
  * Table number (should be "Table 2" since this is the second table)
  * Descriptive title
- **STRICT REQUIREMENT**: Must have introduction, reference, number, AND title

**Component 3: Second Descriptive Statistics table copied in JASP format - VIBE (0-5 points)**
- Focus: Did the student include/reference the second table with JASP descriptive statistics?
- Evidence of table inclusion:
  * References "Table 2" or "second table"
  * Mentions descriptive statistics (mean, N, etc.)
  * Discusses the table content
  * Shows JASP output was included
- Be generous: if they discuss the table and its content, assume it exists
- 5 points: Clear evidence table was included with proper JASP format
- 3-4 points: Table referenced but description minimal
- 1-2 points: Unclear if table was actually included
- 0 points: No mention of including the table

**Component 4: One-sentence description of changes - STRICT (0-5 points)**
- 0 points: No description of changes
- 2-3 points: Description present but vague, lacks specifics, or more/less than one sentence
- 4 points: One sentence describing changes, but could be more precise
- 5 points: Clear one-sentence description explaining what changed between Table 1 and Table 2
  * Should mention that values/statistics changed due to data edits
  * Could reference specific statistics (mean, N, etc.) that changed
  * Should be concise (one sentence)
- **STRICT REQUIREMENT**: Must provide a clear description of what changed
- **BONUS consideration**: If automatic check found value changes mentioned (changes_mentioned = True), this shows strong attention to detail

**CRITICAL FEEDBACK REQUIREMENTS:**

For each component, provide separate, specific feedback:

1. **component_1_feedback**: 
   - If 5/5: Empty "" or brief positive (e.g., "Good workflow demonstration")
   - If < 5: Explain SPECIFICALLY what's missing:
     * Which steps weren't mentioned (Excel editing? JASP opening? Comparison?)
     * What evidence would strengthen their response
     * Example: "You mentioned opening the file in JASP but didn't describe the editing process in Excel or comparing results with Table 1. Explain what values you changed and how the new statistics compare to the original."

2. **component_2_feedback**:
   - If 5/5: Empty "" or brief positive
   - If < 5: Identify EXACTLY which APA elements are missing:
     * Missing introduction/reference?
     * Missing table number?
     * Missing descriptive title?
     * Format issues?
     * Example: "Your table lacks a proper APA introduction and reference. You should introduce the table in text (e.g., 'Table 2 presents the updated descriptive statistics...') before presenting it."

3. **component_3_feedback**:
   - If 5/5: Empty "" or brief positive
   - If < 5: Explain what's unclear about the table inclusion:
     * Is there no reference to the table?
     * Is it unclear if JASP format was used?
     * Example: "It's unclear whether you actually included the JASP descriptive statistics table. Reference the table explicitly and discuss its content to show it's been included."

4. **component_4_feedback**:
   - If 5/5: Empty "" or brief positive
   - If < 5: Specify the issue:
     * No description provided?
     * Too vague?
     * Not one sentence?
     * Lacks specificity about what changed?
     * Example: "Your description is vague. Provide one clear sentence explaining what changed, such as: 'After editing the Excel data, the mean for Adults decreased and the mean for Teens increased in the updated descriptive statistics.'"

**CRITICAL RULES:**
1. Each feedback addresses ONLY its component - no mixing
2. If score is 5/5, feedback can be empty "" or very brief positive
3. If score < 5, feedback must be SPECIFIC and ACTIONABLE
4. No generic statements - tell them exactly what's missing and how to fix it
5. Focus on WHAT they need to do, not just what's wrong
6. Components 2 and 4 are STRICT - must have required elements
7. Components 1 and 3 are VIBE - focus on understanding and intent

**VIBE (Overall Impression):**
Provide ONE SENTENCE capturing your overall sense of their understanding of the data editing process and its impact on descriptive statistics.

Return your grading in this exact JSON format:
{{
  "component_1_score": <0-5>,
  "component_1_feedback": "<specific feedback for Component 1, or empty if 5/5>",
  "component_2_score": <0-5>,
  "component_2_feedback": "<specific feedback for Component 2, or empty if 5/5>",
  "component_3_score": <0-5>,
  "component_3_feedback": "<specific feedback for Component 3, or empty if 5/5>",
  "component_4_score": <0-5>,
  "component_4_feedback": "<specific feedback for Component 4, or empty if 5/5>",
  "total_points": <sum of component scores, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
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
                max_tokens=1500,
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

            # Add changes check info to result
            result['changes_check'] = changes_check

            # Verify total_points matches sum of components
            if all(key in result for key in
                   ['component_1_score', 'component_2_score', 'component_3_score', 'component_4_score']):
                calculated_total = (result['component_1_score'] +
                                    result['component_2_score'] +
                                    result['component_3_score'] +
                                    result['component_4_score'])
                result['total_points'] = calculated_total
                result['percentage'] = round((calculated_total / 20) * 100, 1)

            return result

        except json.JSONDecodeError as e:
            return {
                "error": "Could not parse grading result",
                "raw_response": response_text,
                "parse_error": str(e),
                "changes_check": changes_check
            }
        except Exception as e:
            return {
                "error": "API call failed",
                "error_message": str(e),
                "changes_check": changes_check
            }

    def print_grading_results(self, grading):
        """Helper function to display grading results with component-specific feedback"""
        print("=" * 60)
        print("GRADING RESULTS - QUESTION 1_3")
        print("Excel Editing and JASP Comparison")
        print("=" * 60)

        # Print value changes detection result
        if 'changes_check' in grading:
            changes_check = grading['changes_check']
            print("\nVALUE CHANGES MENTION CHECK:")
            if changes_check['changes_mentioned']:
                print(f"  ✅ CHANGES MENTIONED - Shows attention to detail")
                print(f"  Evidence: {changes_check['evidence']}")
            else:
                print(f"  ℹ️  Changes not explicitly mentioned in submission")
            print(f"  {'─' * 40}")

        # Print component breakdown with individual feedback
        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            # Component 1
            print(f"  Component 1 (Excel Edit + JASP + Compare) [VIBE]: {grading.get('component_1_score', 'N/A')}/5")
            if grading.get('component_1_feedback'):
                print(f"    → {grading['component_1_feedback']}")

            # Component 2
            print(f"  Component 2 (APA Intro/Ref/Number/Title) [STRICT]: {grading.get('component_2_score', 'N/A')}/5")
            if grading.get('component_2_feedback'):
                print(f"    → {grading['component_2_feedback']}")

            # Component 3
            print(f"  Component 3 (Table 2 Copied) [VIBE]: {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_feedback'):
                print(f"    → {grading['component_3_feedback']}")

            # Component 4
            print(
                f"  Component 4 (One-Sentence Change Description) [STRICT]: {grading.get('component_4_score', 'N/A')}/5")
            if grading.get('component_4_feedback'):
                print(f"    → {grading['component_4_feedback']}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points', 'N/A')}/{grading.get('max_points', 20)}")
        print(f"PERCENTAGE: {grading.get('percentage', 'N/A')}%")

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
    print("Welcome to the Classwork AI Evaluator System!")
    # Initialize evaluator
    evaluator = Question1_3Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("CLASSWORK 1 - QUESTION 1_3 EVALUATOR")
    print("Excel Editing and JASP Comparison")
    print("=" * 60)
    print("\nPlease enter the student's answer to Question 1_3.")
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
    grading = evaluator.grade_question1_3_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)