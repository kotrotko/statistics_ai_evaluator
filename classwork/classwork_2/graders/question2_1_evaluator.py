"""
question2_1_evaluator.py
Frequencies, Cumulative Frequencies, and Percentiles Calculation
"""

import re
import textwrap

from config import BaseEvaluator

class Question2_1Evaluator(BaseEvaluator):
    """
    Evaluator for Frequencies/Percentiles Question.

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

    def check_required_columns(self, student_answer: str) -> dict:
        """
        Check if required columns (frequencies, cumulative, percentiles) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found columns and evidence
        """
        text_lower = student_answer.lower()

        columns_found = {
            "frequency": False,
            "cumulative": False,
            "percentile": False
        }

        evidence = []

        # Check for frequency-related terms
        freq_patterns = [r'\bfrequenc(y|ies)\b', r'\bfreq\b', r'\bcount\b']
        for pattern in freq_patterns:
            if re.search(pattern, text_lower):
                columns_found["frequency"] = True
                evidence.append(f"Found frequency indicator: {pattern}")
                break

        # Check for cumulative-related terms
        cumul_patterns = [r'\bcumulative\b', r'\bcumul\b', r'\bcum\.\s*freq']
        for pattern in cumul_patterns:
            if re.search(pattern, text_lower):
                columns_found["cumulative"] = True
                evidence.append(f"Found cumulative indicator: {pattern}")
                break

        # Check for percentile-related terms
        perc_patterns = [r'\bpercentile\b', r'\bpercent\b', r'\b%\b', r'\bperc\b']
        for pattern in perc_patterns:
            if re.search(pattern, text_lower):
                columns_found["percentile"] = True
                evidence.append(f"Found percentile indicator: {pattern}")
                break

        return {
            "columns_found": columns_found,
            "evidence": evidence if evidence else ["No clear column indicators found"],
            "all_present": all(columns_found.values())
        }

    def grade_frequencies_percentiles(self, student_answer: str, test_mode: bool = False):
        """
        Grade Frequencies/Percentiles question.

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
                    "component_1_score": 5,
                    "component_2_score": 5,
                    "component_3_score": 5,
                    "component_4_score": 5
                },
                max_points=20,
                feedback="Excellent work calculating frequencies, cumulative frequencies, and percentiles with proper APA table formatting.",
                vibe="Student demonstrates strong understanding of frequency distributions and percentile calculations",
                additional_data={
                    "column_check": {
                        "columns_found": {"frequency": True, "cumulative": True, "percentile": True},
                        "all_present": True,
                        "evidence": ["Test mode - all columns present"]
                    }
                }
            )

        # Check for required columns
        column_check = self.check_required_columns(student_answer)

        # Build the grading prompt
        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - combining vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Students must:
1. Calculate frequencies for Q5 variable (5 points)
2. Calculate cumulative frequencies for Q5 variable (5 points)
3. Calculate percentiles for Q5 variable (5 points)
4. Introduce, number, and title the table in APA style (5 points)

Total: 20 points

STUDENT ANSWER:
{student_answer}

**AUTOMATIC COLUMN DETECTION RESULT:**
Columns Found: {column_check['columns_found']}
All Required Columns Present: {column_check['all_present']}
Evidence: {column_check['evidence']}

**IMPORTANT NOTES:**
- Students submit text descriptions since visual elements (actual tables) cannot be captured in text
- If student REFERENCES a table (e.g., "Table 1", "see table below", "the frequency table shows"), ASSUME the table exists in their actual document
- DO NOT penalize for "missing" tables if they clearly reference and discuss the table content
- Focus on whether they understand the required calculations and present the results appropriately

**HYBRID GRADING APPROACH:**

**Component 1: Student Name + Frequencies - HYBRID (0-5 points)**

STEP 1 - Check for student name (STRICT):
- Look for a student name at the TOP of the submission
- Common patterns: "Name: John Doe", "Student: Jane Smith", "By: Alex Brown"
- If NO name found: Maximum score for Component 1 = 4 points (deduct 1 point)
- Add this feedback: "Your name is expected here. Minus 1 point."

STEP 2 - Evaluate frequencies (VIBE):
- Focus: Does the student show evidence of calculating frequencies for Q5?
- Evidence: mentions frequencies, counts, or distribution of values
- Be generous: any reasonable indication that they calculated frequencies
- 0 points: No mention of frequencies at all
- 2-3 points: Mentions frequencies but minimal detail
- 4-5 points: Clear evidence of frequency calculation

FINAL SCORE:
- If name is missing: Cap maximum at 4/5 even if frequencies are perfect
- If name is present: Score normally based on frequency work (0-5)

**Component 2: Cumulative frequencies calculated - VIBE (0-5 points)**
- Focus: Does the student show evidence of calculating cumulative frequencies?
- Evidence: mentions cumulative frequencies, running totals, or cumulative counts
- Be generous: any reasonable indication of cumulative calculation
- 0 points: No mention of cumulative frequencies
- 2-3 points: Mentions cumulative but unclear or minimal
- 5 points: Clear evidence of cumulative frequency calculation

**Component 3: Percentiles calculated - VIBE (0-5 points)**
- Focus: Does the student show evidence of calculating percentiles?
- Evidence: mentions percentiles, percentages, % distribution, or cumulative percent
- Be generous: any reasonable indication of percentile calculation
- 0 points: No mention of percentiles or percentages
- 2-3 points: Mentions percentiles but minimal detail
- 4-5 points: Clear evidence of percentile calculation

**Component 4: Table introduction, numbering, and titling - STRICT (0-5 points)**
- 0 points: No table number or title
- 1 point: Has only number OR title (not both)
- 3 points: Has both number and title but incorrect table number (not Table 1)
- 4 points: Correctly numbered (Table 1) and titled but missing introductory sentence
- 5 points: Student correctly introduced, numbered (Table 1), and titled the table
- **STRICT REQUIREMENT**: Must have introductory sentence, number (Table 1), AND title
- **IMPORTANT**: The table caption alone (e.g., "Table 1 Title") does NOT count as an introductory sentence. There must be a separate sentence in the main text that references the table (e.g., "As shown in Table 1..." or "Table 1 presents..."). Maximum score is 4 points if introductory sentence is missing.

**CRITICAL RULES:**
1. Components 1, 2, and 3 are VIBE - focus on evidence of understanding
2. Component 4 is STRICT - must have all three elements (intro, number, title)
3. Be generous with table references - if they discuss calculations, assume they did them
4. Focus on statistical understanding of frequency distributions
5. Don't over-penalize for imperfect formatting as long as content is there

**SCORING PROCESS:**
1. Score Component 1 (Frequencies) - VIBE: __/5
2. Score Component 2 (Cumulative Frequencies) - VIBE: __/5
3. Score Component 3 (Percentiles) - VIBE: __/5
4. Score Component 4 (Table intro/number/title) - STRICT: __/5
5. Total = sum of four scores

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- Acknowledges what calculations they completed
- Points out any missing calculations specifically
- Comments on their table presentation and APA formatting
- Explains what would improve their score
- Remains encouraging and constructive

Return your grading in this exact JSON format:
{{
  "component_1_score": <0-5>,
  "component_1_explanation": "<if score < 5: one sentence explaining what's missing or problematic; if score = 5 AND student did good extra work beyond requirements (provided helpful examples, added clear explanations, showed original insight, caught errors): one sentence of praise; otherwise empty string>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<if score < 5: one sentence explaining what's missing or problematic; if score = 5 AND student did good extra work beyond requirements (provided helpful examples, added clear explanations, showed original insight, caught errors): one sentence of praise; otherwise empty string>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<if score < 5: one sentence explaining what's missing or problematic; if score = 5 AND student did good extra work beyond requirements (provided helpful examples, added clear explanations, showed original insight, caught errors): one sentence of praise; otherwise empty string>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<if score < 5: one sentence explaining what's missing or problematic; if score = 5 AND student did good extra work beyond requirements (provided helpful examples, added clear explanations, showed original insight, caught errors): one sentence of praise; otherwise empty string>",
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative explanation - which tools they used well, what's missing, how to improve>",
  "vibe": "<one-sentence overall impression of their equation tool mastery>"
}}"""

        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"column_check": column_check}
        )

        # If grading succeeded, validate component scores
        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score"
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Helper function to display grading results"""
        print("=" * 60)
        print("GRADING RESULTS - QUESTION 2_1 (HYBRID MODE)")
        print("Frequencies, Cumulative Frequencies, and Percentiles Calculation")
        print("=" * 60)

        # Print component breakdown if available
        # Print component breakdown if available
        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Frequencies): {grading.get('component_1_score', 'N/A')}/5")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Cumulative Frequencies): {grading.get('component_2_score', 'N/A')}/5")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Percentiles): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Table intro/number/title): {grading.get('component_4_score', 'N/A')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

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
    print("Welcome to the Classwork AI Evaluator System!")
    print("=" * 60)

    # Initialize evaluator
    evaluator = Question2_1Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("CLASSWORK 2 - QUESTION 2_1 EVALUATOR")
    print("Frequencies, Cumulative Frequencies, and Percentiles Calculation")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION 2_1.")
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
    grading = evaluator.grade_frequencies_percentiles(student_answer)

    # Display results
    evaluator.print_grading_results(grading)