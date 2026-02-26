import os
import re
import json
from groq import Groq

class Question4Evaluator:
    def __init__(self):
        """Initialize the evaluator with Groq API key."""
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Please set GROQ_API_KEY environment variable")

        self.client = Groq(api_key=self.api_key)

    def check_label_changes_mentioned(self, student_answer: str) -> dict:
        """
        Check if student mentions the label changes (Teens→Men, Adults→Women).
        Returns dict with: labels_mentioned (bool) and evidence (str)
        """
        patterns = [
            r'teens\s*(?:to|→|->)\s*men',
            r'adults\s*(?:to|→|->)\s*women',
            r'men.*women',
            r'changed.*labels',
            r'renamed.*columns'
        ]

        text_lower = student_answer.lower()
        found_mentions = []

        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                found_mentions.append(match.group())

        if found_mentions:
            return {
                "labels_mentioned": True,
                "evidence": f"Found label change references: {', '.join(found_mentions)}"
            }

        return {
            "labels_mentioned": False,
            "evidence": "No explicit mention of label changes (Teens→Men, Adults→Women)"
        }

    def check_data_type_change_mentioned(self, student_answer: str) -> dict:
        """
        Check if student mentions the data type change (ordinal→nominal).
        Returns dict with: type_mentioned (bool) and evidence (str)
        """
        patterns = [
            r'ordinal\s*(?:to|→|->)\s*nominal',
            r'nominal.*ordinal',
            r'changed.*type',
            r'data\s*type',
            r'measurement\s*(?:level|scale)'
        ]

        text_lower = student_answer.lower()
        found_mentions = []

        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                found_mentions.append(match.group())

        if found_mentions:
            return {
                "type_mentioned": True,
                "evidence": f"Found data type change references: {', '.join(found_mentions)}"
            }

        return {
            "type_mentioned": False,
            "evidence": "No explicit mention of data type change (ordinal→nominal)"
        }

    def check_value_changes_mentioned(self, student_answer: str) -> dict:
        """
        Check if student mentions changing Teens8 and Teens10 to 0.
        Returns dict with: values_mentioned (bool) and evidence (str)
        """
        patterns = [
            r'teens8.*0',
            r'teens10.*0',
            r'changed.*0',
            r'set.*0',
            r'value.*0'
        ]

        text_lower = student_answer.lower()
        found_mentions = []

        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                found_mentions.append(match.group())

        if found_mentions:
            return {
                "values_mentioned": True,
                "evidence": f"Found value change references: {', '.join(found_mentions)}"
            }

        return {
            "values_mentioned": False,
            "evidence": "No explicit mention of changing Teens8 and Teens10 to 0"
        }

    def grade_question4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 4: JASP Data Editing (two parts).
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        # Test mode for verification without API
        if test_mode:
            return {
                "component_1_score": 5,
                "component_2_score": 4,
                "component_3_score": 5,
                "component_4_score": 5,
                "total_points": 19,
                "max_points": 20,
                "percentage": 95.0,
                "feedback": "[TEST MODE] Excellent work! Table 3 properly introduced with clear APA formatting and good description of label/type changes. Table 4 also well-formatted with clear description of how setting values to 0 affected the statistics. Minor improvement possible in description clarity for Table 3.",
                "vibe": "Student demonstrates strong understanding of JASP data editing capabilities and how changes affect descriptive statistics",
                "labels_check": {"labels_mentioned": True, "evidence": "Test mode - labels properly mentioned"},
                "type_check": {"type_mentioned": True, "evidence": "Test mode - data type change mentioned"},
                "values_check": {"values_mentioned": True, "evidence": "Test mode - value changes mentioned"}
            }

        # Check for mentioned changes
        labels_check = self.check_label_changes_mentioned(student_answer)
        type_check = self.check_data_type_change_mentioned(student_answer)
        values_check = self.check_value_changes_mentioned(student_answer)

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - combining vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
This question has TWO parts:

**PART 1 (10 points):**
1. Open LikeLike.xlsx in JASP
2. Change column labels: Teens→Men, Adults→Women
3. Change data type: ordinal→nominal
4. Introduce, number (Table 3), title, and insert the third Descriptive Statistics table (5 points)
5. Describe changes in one sentence (5 points)

**PART 2 (10 points):**
1. Open original LikeLike.xlsx in JASP
2. Change Teens8 and Teens10 to value 0
3. Introduce, number (Table 4), title, and insert the fourth Descriptive Statistics table (5 points)
4. Describe changes in one sentence (5 points)

Total: 20 points

STUDENT ANSWER:
{student_answer}

**AUTOMATIC CHANGE DETECTION RESULTS:**
Label Changes Mentioned: {labels_check['labels_mentioned']}
Evidence: {labels_check['evidence']}

Data Type Change Mentioned: {type_check['type_mentioned']}
Evidence: {type_check['evidence']}

Value Changes Mentioned: {values_check['values_mentioned']}
Evidence: {values_check['evidence']}

**IMPORTANT NOTES:**
- Students submit text descriptions since visual elements (JASP tables) cannot be captured in text
- If student REFERENCES a table (e.g., "Table 3", "Table 4"), ASSUME the table exists in their actual document
- DO NOT penalize for "missing" tables if they clearly reference and discuss the content
- Focus on whether they understand what they're doing

**HYBRID GRADING APPROACH:**

**Component 1: PART 1 - Introduce/number/title/insert Table 3 - STRICT (0-5 points)**
- 0 points: No table introduction, number, title, or reference to insertion
- 2-3 points: Missing one or more elements (intro/number/title/insertion)
- 4 points: Has all elements but minor APA formatting issues
- 5 points: Proper format with:
  * Introduction phrase (e.g., "Table 3 shows descriptive statistics after relabeling...")
  * Table number (must be "Table 3")
  * Descriptive title about the changes (labels/data type)
  * Evidence table was inserted/included
- **STRICT REQUIREMENT**: Must have introduction, number "Table 3", title, AND insertion reference

**Component 2: PART 1 - Describe changes in one sentence - VIBE (0-5 points)**
- Focus: Quality of description about what changed (labels and/or data type)
- 5 points: Clear one-sentence description mentioning:
  * Label changes (Teens→Men, Adults→Women) AND/OR
  * Data type change (ordinal→nominal)
  * How these affected the analysis/table
- 3-4 points: One sentence describing changes, but vague or incomplete
- 1-2 points: Description present but very unclear or multiple sentences
- 0 points: No description of changes
- **VIBE FOCUS**: Reward understanding of what changed, be flexible on exact wording
- **BONUS consideration**: If automatic checks found mentions of label/type changes, student shows good attention to detail

**Component 3: PART 2 - Introduce/number/title/insert Table 4 - STRICT (0-5 points)**
- 0 points: No table introduction, number, title, or reference to insertion
- 2-3 points: Missing one or more elements (intro/number/title/insertion)
- 4 points: Has all elements but minor APA formatting issues
- 5 points: Proper format with:
  * Introduction phrase (e.g., "Table 4 presents descriptive statistics after setting values to 0...")
  * Table number (must be "Table 4")
  * Descriptive title about the value changes
  * Evidence table was inserted/included
- **STRICT REQUIREMENT**: Must have introduction, number "Table 4", title, AND insertion reference

**Component 4: PART 2 - Describe changes in one sentence - VIBE (0-5 points)**
- Focus: Quality of description about what changed when Teens8 & Teens10 set to 0
- 5 points: Clear one-sentence description explaining:
  * What values were changed (Teens8, Teens10 to 0)
  * How statistics changed (mean decreased, N changed, etc.)
  * Impact on the descriptive statistics
- 3-4 points: One sentence describing changes, but lacks specificity
- 1-2 points: Description present but very unclear or multiple sentences
- 0 points: No description of changes
- **VIBE FOCUS**: Reward understanding of how data changes affect statistics
- **BONUS consideration**: If automatic check found value changes mentioned, student shows attention to detail

**CRITICAL RULES:**
1. Components 1 and 3 are STRICT - must have all required elements (intro/number/title/insert)
2. Components 2 and 4 are VIBE - focus on understanding and quality of description
3. Be generous with table references - if they discuss it, assume it exists
4. Both tables must be present (Table 3 and Table 4)
5. Both descriptions must be present (one for each part)
6. One-sentence guideline is important but focus more on quality than strict counting

**SCORING PROCESS:**
1. Score Component 1 (PART 1: Table 3 intro/number/title/insert) - STRICT: __/5
2. Score Component 2 (PART 1: Change description) - VIBE: __/5
3. Score Component 3 (PART 2: Table 4 intro/number/title/insert) - STRICT: __/5
4. Score Component 4 (PART 2: Change description) - VIBE: __/5
5. Total = sum of four scores (max 20)

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- Acknowledges what they did well for BOTH parts
- If change mentions were detected, note this shows good attention to detail
- Points out any missing strict requirements for either table
- Comments on the quality of their change descriptions
- Notes whether they demonstrated understanding of how edits affect statistics
- Explains what would improve their score
- Remains encouraging and constructive

Return your grading in this exact JSON format:
{{
  "component_1_score": <0-5>,
  "component_2_score": <0-5>,
  "component_3_score": <0-5>,
  "component_4_score": <0-5>,
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative explanation - what they did well in both parts, what's missing, comment on description quality, how to improve>",
  "vibe": "<one-sentence overall impression of their understanding of JASP data editing and its impact on descriptive statistics>"
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
                max_tokens=1200,
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

            # Add check info to result
            result['labels_check'] = labels_check
            result['type_check'] = type_check
            result['values_check'] = values_check

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
                "labels_check": labels_check,
                "type_check": type_check,
                "values_check": values_check
            }
        except Exception as e:
            return {
                "error": "API call failed",
                "error_message": str(e),
                "labels_check": labels_check,
                "type_check": type_check,
                "values_check": values_check
            }

    def print_grading_results(self, grading):
        """Helper function to display grading results"""
        print("=" * 60)
        print("GRADING RESULTS - QUESTION 4 (HYBRID MODE)")
        print("JASP Data Editing - Two Parts")
        print("=" * 60)

        # Print change detection results
        if 'labels_check' in grading:
            print("\nCHANGE DETECTION RESULTS:")

            labels_check = grading['labels_check']
            if labels_check['labels_mentioned']:
                print(f"  ✅ Label Changes Mentioned (Teens→Men, Adults→Women)")
            else:
                print(f"  ℹ️  Label changes not explicitly mentioned")

            type_check = grading.get('type_check', {})
            if type_check.get('type_mentioned'):
                print(f"  ✅ Data Type Change Mentioned (ordinal→nominal)")
            else:
                print(f"  ℹ️  Data type change not explicitly mentioned")

            values_check = grading.get('values_check', {})
            if values_check.get('values_mentioned'):
                print(f"  ✅ Value Changes Mentioned (Teens8, Teens10→0)")
            else:
                print(f"  ℹ️  Value changes not explicitly mentioned")

            print(f"  {'─' * 40}")

        # Print component breakdown if available
        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(
                f"  PART 1 - Component 1 (Table 3 Intro/Number/Title/Insert) [STRICT]: {grading.get('component_1_score', 'N/A')}/5")
            print(f"  PART 1 - Component 2 (Change Description) [VIBE]: {grading.get('component_2_score', 'N/A')}/5")
            print(
                f"  PART 2 - Component 3 (Table 4 Intro/Number/Title/Insert) [STRICT]: {grading.get('component_3_score', 'N/A')}/5")
            print(f"  PART 2 - Component 4 (Change Description) [VIBE]: {grading.get('component_4_score', 'N/A')}/5")
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
    evaluator = Question4Evaluator()

    # Run mock test first to verify the system works
    print("=" * 60)
    print("RUNNING MOCK TEST FIRST...")
    print("=" * 60)
    print("\nMock Student Answer (Two Parts):")
    print("PART 1: Changed Teens to Men and Adults to Women, ordinal to nominal.")
    print("Table 3 shows the relabeled data.")
    print("PART 2: Set Teens8 and Teens10 to 0.")
    print("Table 4 displays statistics after value changes.")
    print("=" * 60)

    mock_grading = evaluator.grade_question4_answer(
        "Mock student answer with both parts completed",
        test_mode=True
    )
    evaluator.print_grading_results(mock_grading)

    print("\n" + "=" * 60)
    print("MOCK TEST COMPLETE - System is working!")
    print("Notice: Both tables graded, change descriptions evaluated")
    print("=" * 60)
    input("\nPress Enter to continue to real grading...\n")

    # Now prompt user for student's answer
    print("=" * 60)
    print("CLASSWORK 1 - QUESTION 4 EVALUATOR")
    print("JASP Data Editing - Two Parts")
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
    grading = evaluator.grade_question4_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)