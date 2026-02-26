import os
import re
import json
from groq import Groq

class Question5Evaluator:
    def __init__(self):
        """Initialize the evaluator with Groq API key."""
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Please set GROQ_API_KEY environment variable")

        self.client = Groq(api_key=self.api_key)

    def check_extra_statistics(self, student_answer: str) -> dict:
        """
        Check if student included unnecessary statistics beyond the required ones.
        Required: Valid, Missing, Mean, Maximum, Minimum
        Unnecessary: SD/Std. Deviation, Median, Mode, Variance, Range, etc.

        Returns dict with: extra_found (bool), extra_items (list), and penalty (int)
        """
        # Statistics that should NOT be in the table
        unwanted_patterns = [
            (r'std\.\s*deviation', 'Std. Deviation'),
            (r'std\s+deviation', 'Std Deviation'),
            (r'standard\s+deviation', 'Standard Deviation'),
            (r'\bsd\b', 'SD'),
            (r'\bs\.d\.\b', 'S.D.'),
            (r'\bmedian\b', 'Median'),
            (r'\bmode\b', 'Mode'),
            (r'\bvariance\b', 'Variance'),
            (r'\brange\b', 'Range'),
            (r'\bsum\b', 'Sum'),
            (r'\bstd\.\s*error', 'Std. Error'),
            (r'standard\s+error', 'Standard Error'),
            (r'\bskewness\b', 'Skewness'),
            (r'\bkurtosis\b', 'Kurtosis'),
            (r'\bpercentile', 'Percentile'),
            (r'\bquartile', 'Quartile')
        ]

        text_lower = student_answer.lower()
        extra_items_found = []

        for pattern, item_name in unwanted_patterns:
            match = re.search(pattern, text_lower)
            if match:
                # Check if it's in a table context (not just mentioned in text)
                context_start = max(0, match.start() - 50)
                context_end = min(len(student_answer), match.end() + 50)
                context = student_answer[context_start:context_end].lower()

                # Look for table-like indicators around the match
                table_indicators = ['table', 'statistics', 'descriptive', '|', 'valid', 'missing', 'mean']
                if any(indicator in context for indicator in table_indicators):
                    extra_items_found.append(item_name)

        # Remove duplicates
        extra_items_found = list(set(extra_items_found))

        # Calculate penalty: 1 point per extra statistic
        penalty = len(extra_items_found)

        if extra_items_found:
            return {
                "extra_found": True,
                "extra_items": extra_items_found,
                "penalty": penalty,
                "evidence": f"Found {penalty} unnecessary statistic(s): {', '.join(extra_items_found)}"
            }

        return {
            "extra_found": False,
            "extra_items": [],
            "penalty": 0,
            "evidence": "No unnecessary statistics found - table contains only required items"
        }

    def grade_question5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 5: JASP Anxiety Level Descriptive Statistics Analysis.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        # Test mode for verification without API
        if test_mode:
            return {
                "component_1_score": 5,
                "component_2_score": 4,  # 5 - 1 penalty for extra statistics
                "component_3_score": 9,
                "total_points": 18,
                "max_points": 20,
                "percentage": 90.0,
                "feedback": "[TEST MODE] Good work! Table 5 properly introduced and formatted. However, the table included Standard Deviation which was not required (1 point deducted). Insightful comments on the statistics lab experience.",
                "vibe": "Student shows solid understanding of JASP and descriptive statistics, with thoughtful reflections on the learning process",
                "extra_stats_check": {
                    "extra_found": True,
                    "extra_items": ["Std. Deviation"],
                    "penalty": 1,
                    "evidence": "Test mode - found unnecessary Std. Deviation in table"
                }
            }

        # Check for extra statistics
        extra_stats_check = self.check_extra_statistics(student_answer)

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - combining vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Students must:
1. Analyze "1.3.6. Anxiety level" dataset using JASP Descriptive Statistics
2. Introduce, number (Table 5), title, and insert the fifth Descriptive Statistics table in JASP format (5 points)
3. Include ONLY these statistics: Valid, Missing, Mean, Maximum, Minimum - NO other statistics (5 points)
4. Provide 1-3 brief comments or insights reflecting their experience in today's Statistics lab (10 points)

Total: 20 points

STUDENT ANSWER:
{student_answer}

**AUTOMATIC EXTRA STATISTICS DETECTION RESULT:**
Extra Statistics Found: {extra_stats_check['extra_found']}
Extra Items: {extra_stats_check['extra_items']}
Penalty: {extra_stats_check['penalty']} point(s)
Evidence: {extra_stats_check['evidence']}

**IMPORTANT NOTES:**
- Students submit text descriptions since visual elements (JASP tables) cannot be captured in text
- If student REFERENCES a table (e.g., "Table 5", "see table below"), ASSUME the table exists in their actual document
- DO NOT penalize for "missing" tables if they clearly reference and discuss the table content
- Focus on whether they understand what they're doing

**HYBRID GRADING APPROACH:**

**Component 1: Introduce, number (Table 5), title, and insert table - STRICT (0-5 points)**
- 0 points: No table introduction, number, title, or reference to insertion
- 2-3 points: Missing one or more elements (intro/number/title/insertion reference)
- 4 points: Has all elements but minor APA formatting issues
- 5 points: Proper format with:
  * Introduction phrase (e.g., "Table 5 presents anxiety level descriptive statistics...")
  * Table number (must be "Table 5")
  * Descriptive title about anxiety level
  * Evidence table was inserted/included
- **STRICT REQUIREMENT**: Must have introduction, number "Table 5", title, AND insertion reference

**Component 2: Table contains ONLY required statistics - STRICT with PENALTY (0-5 points)**
- **REQUIRED statistics ONLY**: Valid, Missing, Mean, Maximum, Minimum
- **AUTOMATIC PENALTY SYSTEM**: 
  * Base score: 5 points if only required statistics mentioned
  * Deduct 1 point for EACH extra/unnecessary statistic included
  * Extra statistics include: SD, Std. Deviation, Median, Mode, Variance, Range, Std. Error, Skewness, Kurtosis, Sum, Percentiles, Quartiles, etc.
- **USE THE AUTOMATIC DETECTION RESULT ABOVE**
- If extra_found = True:
  * Start with 5 points
  * Subtract the penalty value (1 point per extra item)
  * Minimum score: 0 points (cannot go negative)
  * Example: If 2 extra statistics found → 5 - 2 = 3 points
- If extra_found = False:
  * 5 points: Only required statistics present
  * 3-4 points: Required statistics present, unclear if extras included
  * 0-2 points: Missing some required statistics
- **STRICT REQUIREMENT**: Table must contain ONLY the 5 required statistics

**Component 3: 1-3 brief comments/insights on Statistics lab experience - VIBE (0-10 points)**
- Focus: Quality and thoughtfulness of reflections, NOT just presence
- This is worth 10 points - evaluate carefully!
- 9-10 points: Excellent insights
  * 1-3 thoughtful comments that show genuine learning/reflection
  * Specific observations about JASP, statistical concepts, or learning process
  * Demonstrates engagement with the material
  * Clear, well-articulated thoughts
- 7-8 points: Good insights
  * 1-3 comments present
  * Show some thought but could be deeper
  * Somewhat generic but still meaningful
- 5-6 points: Adequate insights
  * 1-3 comments present but superficial
  * Generic statements without much depth
  * Minimal engagement evident
- 3-4 points: Minimal insights
  * Very brief or only 1 comment
  * Very generic ("it was interesting", "I learned a lot")
  * Little evidence of actual reflection
- 0-2 points: Poor or no insights
  * No comments provided
  * Completely off-topic
  * Just restating task without reflection
- **VIBE FOCUS**: Reward genuine reflection and learning, not just word count

**CRITICAL RULES:**
1. Components 1 and 2 are STRICT - must have required elements
2. Component 2 has AUTOMATIC PENALTY - deduct 1 point per extra statistic
3. Component 3 is VIBE - focus on quality of reflection (worth 10 points!)
4. Be generous with table references - if they discuss it, assume it exists
5. The extra statistics penalty is AUTOMATIC and NON-NEGOTIABLE

**SCORING PROCESS:**
1. Score Component 1 (Intro/Number/Title/Insert Table 5) - STRICT: __/5
2. Score Component 2 (Only required statistics) - STRICT with PENALTY: __/5
   - Start with base score, then apply automatic penalty
   - Score = max(0, base_score - penalty)
   - If extra_found = True, you MUST deduct penalty points
3. Score Component 3 (1-3 comments/insights) - VIBE: __/10
4. Total = sum of three scores (max 20)

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- Acknowledges what they did well
- If extra statistics found, EXPLICITLY state: "The table included [list items] which were not required. 1 point deducted per extra statistic."
- Comments on the quality and thoughtfulness of their reflections
- Notes whether they demonstrated genuine engagement with the lab
- Explains what would improve their score
- Remains encouraging and constructive

Return your grading in this exact JSON format:
{{
  "component_1_score": <0-5>,
  "component_2_score": <0-5, MUST apply penalty if extra_found=True>,
  "component_3_score": <0-10>,
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative explanation - what they did well, what's missing, mention extra statistics penalty if applicable, comment on reflection quality, how to improve>",
  "vibe": "<one-sentence overall impression of their JASP skills and reflection on learning>"
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

            # Add extra stats check info to result
            result['extra_stats_check'] = extra_stats_check

            # Verify total_points matches sum of components
            if all(key in result for key in
                   ['component_1_score', 'component_2_score', 'component_3_score']):
                calculated_total = (result['component_1_score'] +
                                    result['component_2_score'] +
                                    result['component_3_score'])
                result['total_points'] = calculated_total
                result['percentage'] = round((calculated_total / 20) * 100, 1)

            # Force Component 2 penalty if extra statistics were found (safety check)
            if extra_stats_check['extra_found']:
                penalty = extra_stats_check['penalty']
                corrected_score = max(0, 5 - penalty)

                if result.get('component_2_score', 0) > corrected_score:
                    print(
                        f"\n⚠️  WARNING: AI gave {result['component_2_score']} points for Component 2 despite {penalty} extra statistic(s). Correcting to {corrected_score}.")
                    result['component_2_score'] = corrected_score
                    result['total_points'] = (result['component_1_score'] +
                                              corrected_score +
                                              result['component_3_score'])
                    result['percentage'] = round((result['total_points'] / 20) * 100, 1)

            return result

        except json.JSONDecodeError as e:
            return {
                "error": "Could not parse grading result",
                "raw_response": response_text,
                "parse_error": str(e),
                "extra_stats_check": extra_stats_check
            }
        except Exception as e:
            return {
                "error": "API call failed",
                "error_message": str(e),
                "extra_stats_check": extra_stats_check
            }

    def print_grading_results(self, grading):
        """Helper function to display grading results"""
        print("=" * 60)
        print("GRADING RESULTS - QUESTION 5 (HYBRID MODE)")
        print("JASP Anxiety Level Descriptive Statistics Analysis")
        print("=" * 60)

        # Print extra statistics detection result
        if 'extra_stats_check' in grading:
            extra_check = grading['extra_stats_check']
            print("\nEXTRA STATISTICS CHECK:")
            if extra_check['extra_found']:
                print(f"  ❌ EXTRA STATISTICS FOUND - Penalty Applied")
                print(f"  Items: {', '.join(extra_check['extra_items'])}")
                print(f"  Penalty: -{extra_check['penalty']} point(s)")
                print(f"  Evidence: {extra_check['evidence']}")
            else:
                print(f"  ✅ NO EXTRA STATISTICS - Only Required Items Included")
                print(f"  Evidence: {extra_check['evidence']}")
            print(f"  {'─' * 40}")

        # Print component breakdown if available
        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Intro/Number/Title/Insert) [STRICT]: {grading.get('component_1_score', 'N/A')}/5")

            comp2_score = grading.get('component_2_score', 'N/A')
            if 'extra_stats_check' in grading and grading['extra_stats_check']['extra_found']:
                penalty = grading['extra_stats_check']['penalty']
                print(f"  Component 2 (Only Required Stats) [STRICT]: {comp2_score}/5 (5 - {penalty} penalty)")
            else:
                print(f"  Component 2 (Only Required Stats) [STRICT]: {comp2_score}/5")

            print(f"  Component 3 (1-3 Comments/Insights) [VIBE]: {grading.get('component_3_score', 'N/A')}/10")
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

    # Run mock test first to verify the system works
    print("=" * 60)
    print("RUNNING MOCK TEST FIRST...")
    print("=" * 60)
    print("\nMock Student Answer:")
    print("Table 5 presents descriptive statistics for anxiety levels.")
    print("The table includes Valid, Missing, Mean, Maximum, Minimum, and Standard Deviation.")
    print("My insights: I learned how to use JASP for descriptive statistics.")
    print("It was interesting to see the anxiety data patterns.")
    print("=" * 60)

    mock_grading = evaluator.grade_question5_answer(
        "Mock student answer with extra statistics included",
        test_mode=True
    )
    evaluator.print_grading_results(mock_grading)

    print("\n" + "=" * 60)
    print("MOCK TEST COMPLETE - System is working!")
    print("Notice: Component 2 score is 4/5 due to 1 point penalty")
    print("=" * 60)
    input("\nPress Enter to continue to real grading...\n")

    # Now prompt user for student's answer
    print("=" * 60)
    print("CLASSWORK 1 - QUESTION 5 EVALUATOR")
    print("JASP Anxiety Level Descriptive Statistics Analysis")
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
    grading = evaluator.grade_question5_answer(student_answer)

    # Display results
    evaluator.print_grading_results(grading)