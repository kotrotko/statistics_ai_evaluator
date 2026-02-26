"""
question3_1_central_tendency_evaluator.py
Mean, Median, Mode by Gender (GPA & IQ)
"""

import re
import textwrap
from config import BaseEvaluator


class Question3_1Evaluator(BaseEvaluator):
    """
    Evaluator for Central Tendency (Mean, Median, Mode) split by gender.
    """

    def __init__(self):
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1400
        )

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Detect references to mean, median, mode, GPA, IQ, and gender split.
        """
        text = student_answer.lower()

        checks = {
            "mean": bool(re.search(r"\bmean\b", text)),
            "median": bool(re.search(r"\bmedian\b", text)),
            "mode": bool(re.search(r"\bmode\b", text)),
            "gpa": bool(re.search(r"\bgpa\b", text)),
            "iq": bool(re.search(r"\biq\b", text)),
            "gender": bool(re.search(r"\bgender\b|\bmale\b|\bfemale\b", text))
        }

        return {
            "checks": checks,
            "all_present": all(checks.values())
        }

    def check_intro_phrase_position(self, student_answer: str) -> dict:
        """
        Check if an introductory phrase appears BEFORE any table/data.
        Returns whether intro phrase is present and correctly positioned.
        """
        text = student_answer.strip()

        # Look for table reference patterns
        table_ref_patterns = [
            r'table\s+\d+\s+presents',
            r'table\s+\d+\s+shows',
            r'as\s+shown\s+in\s+table\s+\d+',
            r'see\s+table\s+\d+'
        ]

        # Look for table start markers (common patterns)
        table_markers = [
            r'\t',  # Tab character (tables often have tabs)
            r'male\s+female',  # Gender columns
            r'iq\s+gpa',  # Column headers
            r'\|\s+',  # Pipe separators
        ]

        intro_phrase_pos = -1
        table_start_pos = -1

        # Find first intro phrase position
        for pattern in table_ref_patterns:
            match = re.search(pattern, text.lower())
            if match:
                intro_phrase_pos = match.start()
                break

        # Find first table marker position
        for pattern in table_markers:
            match = re.search(pattern, text)
            if match:
                table_start_pos = match.start()
                break

        has_intro_phrase = intro_phrase_pos != -1
        intro_before_table = False

        if has_intro_phrase and table_start_pos != -1:
            intro_before_table = intro_phrase_pos < table_start_pos
        elif has_intro_phrase and table_start_pos == -1:
            # Has intro phrase but no clear table marker - assume acceptable
            intro_before_table = True

        return {
            "has_intro_phrase": has_intro_phrase,
            "intro_before_table": intro_before_table,
            "intro_phrase_position": intro_phrase_pos,
            "table_start_position": table_start_pos
        }

    def grade_question3_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 3: Mean, Median, Mode by Gender.
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 5,
                    "component_2_score": 5,
                    "component_3_score": 5,
                    "component_4_score": 5,
                    "component_5_score": 5,
                    "component_6_score": 5
                },
                max_points=30,
                feedback="Excellent work calculating and interpreting mean, median, and mode for GPA and IQ split by gender.",
                vibe="Strong and confident use of descriptive statistics in JASP",
                additional_data={"detection": "test mode"}
            )

        stat_check = self.check_required_elements(student_answer)
        intro_check = self.check_intro_phrase_position(student_answer)

        prompt = f"""
        
        You are grading a statistics assignment using a **HYBRID grading approach**.

**TASK DESCRIPTION (30 points):**
Students must:
1. Provide introductory phrase with table reference before the table (1 point) + Calculate Mean for GPA by gender (4 points) = 5 points total
2. Calculate Median for GPA by gender (5 points)
3. Calculate Mode for GPA by gender (5 points)
4. Calculate Mean for IQ by gender (5 points)
5. Calculate Median for IQ by gender (5 points)
6. Calculate Mode for IQ by gender (5 points)

Students submit written descriptions of JASP output.

STUDENT ANSWER:
{student_answer}

**IMPORTANT NOTES:**
- Students submit text descriptions of their work since visual elements (actual tables, screenshots, formatted output) cannot be captured in text
- If student REFERENCES or DESCRIBES the required statistics (e.g., "I calculated mean GPA by gender", "the median IQ for males is X"), ASSUME they completed it in JASP
- DO NOT penalize for "missing" visual elements if they clearly describe what they calculated
- Focus on whether they mention the correct statistics and provide gender-split results

**AUTOMATIC INTRO PHRASE CHECK:**
Intro phrase detected: {intro_check['has_intro_phrase']}
Intro phrase appears BEFORE table: {intro_check['intro_before_table']}

For Component 1 bonus point:
- If intro_before_table is True: award bonus point
- If intro_before_table is False: do NOT award bonus point

**PRECONDITION CHECK FOR COMPONENT 1:**
Before scoring Component 1, check if the student provided ANY mention of mean for GPA.
- If NO mention of mean GPA → Component 1 score = 0. Do not proceed to rubric tiers.
- If mean GPA mentioned → Proceed to score using the rubric below.

**Component 1: Mean for GPA by Gender - STRICT (0-5 points)**

Award points as follows:
- 4 points: Student correctly calculated and reported mean GPA for both genders
- 3 points: Calculated mean GPA with minor issues (one gender missing or unclear)
- 2 points: Mentioned mean GPA but unclear gender split
- 1 point: Mentioned mean GPA but no gender differentiation
- 0 points: Did not mention mean for GPA

THEN add 1 bonus point if and only if:
- An introductory sentence referencing the table appears BEFORE the table in the student's text
- Examples: "Table 1 presents...", "As shown in Table 1..."
- If the table reference appears AFTER the table, do NOT add the bonus point

Maximum score: 5 points

**Component 2: Median for GPA by Gender - STRICT (0-5 points)**
- 5 points: Student correctly calculated and reported median GPA for both genders with clear values
- 4 points: Calculated median GPA by gender with minor issues (e.g., one gender missing or unclear value)
- 2-3 points: Mentioned median GPA but unclear gender split or incomplete data
- 1 point: Mentioned median GPA but no gender differentiation
- 0 points: Did not mention or calculate median for GPA

**Component 3: Mode for GPA by Gender - STRICT (0-5 points)**
- 5 points: Student correctly calculated and reported mode GPA for both genders with clear values
- 4 points: Calculated mode GPA by gender with minor issues (e.g., one gender missing or unclear value)
- 2-3 points: Mentioned mode GPA but unclear gender split or incomplete data
- 1 point: Mentioned mode GPA but no gender differentiation
- 0 points: Did not mention or calculate mode for GPA

**Component 4: Mean for IQ by Gender - STRICT (0-5 points)**
- 5 points: Student correctly calculated and reported mean IQ for both genders with clear values
- 4 points: Calculated mean IQ by gender with minor issues (e.g., one gender missing or unclear value)
- 2-3 points: Mentioned mean IQ but unclear gender split or incomplete data
- 1 point: Mentioned mean IQ but no gender differentiation
- 0 points: Did not mention or calculate mean for IQ

**Component 5: Median for IQ by Gender - STRICT (0-5 points)**
- 5 points: Student correctly calculated and reported median IQ for both genders with clear values
- 4 points: Calculated median IQ by gender with minor issues (e.g., one gender missing or unclear value)
- 2-3 points: Mentioned median IQ but unclear gender split or incomplete data
- 1 point: Mentioned median IQ but no gender differentiation
- 0 points: Did not mention or calculate median for IQ

**Component 6: Mode for IQ by Gender - STRICT (0-5 points)**
- 5 points: Student correctly calculated and reported mode IQ for both genders with clear values
- 4 points: Calculated mode IQ by gender with minor issues (e.g., one gender missing or unclear value)
- 2-3 points: Mentioned mode IQ but unclear gender split or incomplete data
- 1 point: Mentioned mode IQ but no gender differentiation
- 0 points: Did not mention or calculate mode for IQ

**CRITICAL RULES:**
1. Each component is STRICT - must be present to earn points
2. If student meets requirements exactly: full points (5/5 for all components)
3. If student does extra correct work beyond requirements: full points + praise in explanation
4. Minor issues are acceptable if the core requirement is met

**SCORING PROCESS:**
1. Score Component 1 (Table Reference + Mean): __/5
2. Score Component 2 (Median GPA): __/5
3. Score Component 3 (Mode GPA): __/5
4. Score Component 4 (Mean IQ): __/5
5. Score Component 5 (Median IQ): __/5
6. Score Component 6 (Mode IQ): __/5
7. Total = sum of six scores

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- Acknowledges what elements they successfully completed
- Points out any missing components specifically
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
  "component_5_score": <0-5>,
  "component_5_explanation": "<if score < 5: one sentence explaining what's missing or problematic; if score = 5 AND student did good extra work beyond requirements (provided helpful examples, added clear explanations, showed original insight, caught errors): one sentence of praise; otherwise empty string>",
  "component_6_score": <0-5>,
  "component_6_explanation": "<if score < 5: one sentence explaining what's missing or problematic; if score = 5 AND student did good extra work beyond requirements (provided helpful examples, added clear explanations, showed original insight, caught errors): one sentence of praise; otherwise empty string>",
  "total_points": <sum of above, 0-30>,
  "max_points": 30,
  "percentage": <percentage>,
  "feedback": "<narrative explanation - which statistics they calculated well, what's missing, how to improve>",
  "vibe": "<one-sentence overall impression of their statistical analysis and gender comparison skills>"
}}
"""
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"stat_check": stat_check}
        )

        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score",
                "component_5_score",
                "component_6_score",
            ]
            result = self.validate_component_scores(result, component_keys, 30)

        return result

    def print_grading_results(self, grading):
        print("=" * 60)
        print("GRADING RESULTS – QUESTION 3")
        print("Central Tendency (Mean, Median, Mode) by Gender")
        print("=" * 60)

        for i in range(1, 7):
            key = f"component_{i}_score"
            if key in grading:
                print(f"Component {i}: {grading[key]}/5")

        print(f"\nTOTAL: {grading.get('total_points')}/{grading.get('max_points')}")
        print(f"PERCENTAGE: {grading.get('percentage')}%")

        print("\nFEEDBACK:")
        print(textwrap.fill(grading.get("feedback", ""), 60))

        print("\nTHE VIBE:")
        print(textwrap.fill(grading.get("vibe", ""), 60))
