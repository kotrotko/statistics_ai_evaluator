"""
Question 1.2 Evaluator - Refactored Version
Mean Calculation with JASP - Using class-based config architecture
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter


class CW2_1Evaluator(BaseEvaluator):
    """
    Evaluator for Question 1.2: Mean Calculation with JASP.

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
        self.formatter = OutputFormatter(default_width=60)

    def check_formatting_elements(self, student_answer: str) -> dict:
        text_lower = student_answer.lower()
        first_lines = student_answer[:200]

        elements_found = {
            "paper_title": False,
            "task_description": False,
            "no_autoformatting": True,
        }

        evidence = []

        title_patterns = [
            r'^\s*classwork\s*2',
            r'^\s*cw\s*2\b',
            r'^\s*class\s*work\s*(week\s*)?2',
            r'^\s*in.?class\s*2'
        ]

        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["paper_title"] = True
                evidence.append("Title found")
                break

        pedagogical_markers = [
            "distributions and graphs",
            "quiz 5 variable",
            "cumulative frequencies",
            "introductory phrase",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        autoformat_patterns = [
            r'(?m)(?:^\s*\d+[\.\)]\s+\S.*\n){2,}',
            r'^\s*[-•*]\s+\S',
        ]

        for pattern in autoformat_patterns:
            if re.search(pattern, student_answer, re.MULTILINE):
                elements_found["no_autoformatting"] = False
                evidence.append("Autoformatting detected")
                break

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def check_sd_removed(self, student_answer: str) -> dict:
        """
        Check if SD/Standard Deviation appears in the student's answer.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with sd_found (bool) and evidence (str)
        """
        sd_patterns = [
            r'std\.\s*deviation',
            r'std\s+deviation',
            r'standard\s+deviation',
            r'std\.\s*dev',
            r'std\s+dev',
            r'\bsd\b',
            r'\bs\.d\.\b',
            r'\bs\.d\b'
        ]

        text_lower = student_answer.lower()

        for pattern in sd_patterns:
            match = re.search(pattern, text_lower)
            if match:
                # Found SD in the text
                context_start = max(0, match.start() - 30)
                context_end = min(len(student_answer), match.end() + 30)
                evidence = student_answer[context_start:context_end]
                return {
                    "sd_found": True,
                    "evidence": f"Found: '{match.group()}' in context: ...{evidence}..."
                }

        return {
            "sd_found": False,
            "evidence": "No SD/Standard Deviation found in submitted text"
        }

    def grade_question_cw2_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 1.2: Mean calculation with JASP.

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
                    "component_2_score": 4,
                    "component_3_score": 5,
                    "component_4_score": 5
                },
                max_points=20,
                feedback="Excellent work with proper APA formatting and clear explanations of Valid and Missing values.",
                vibe="Student demonstrates strong understanding of descriptive statistics and APA style",
                additional_data={
                    "sd_check": {"sd_found": False, "evidence": "Test mode - SD properly removed"}
                }
            )

        formatting_check = self.check_formatting_elements(student_answer)
        formatting_summary = formatting_check["elements_found"]

        formatting_block = f"""
        HEADER DETECTION RESULTS (DO NOT RE-EVALUATE):

        paper_title_present = {formatting_summary["paper_title"]}
        task_description_present = {formatting_summary["task_description"]}
        no_autoformatting_present = {formatting_summary["no_autoformatting"]}
        """

        # Check if SD was removed
        sd_check = self.check_sd_removed(student_answer)

        # Build the grading prompt
        prompt = f"""{formatting_block}

You are grading a statistics classwork using a **HYBRID approach** - combining vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Students must:
1. Write an introduction phrase with reference (5 points)
2. Number and name the Table in APA style (5 points)
3. Remove the SD column from JASP output and copy the Descriptive Statistics table (5 points)
4. Explain what is "Valid" and what is "Missing" (5 points)

Total: 20 points

STUDENT ANSWER:
{student_answer}

**AUTOMATIC SD DETECTION RESULT:**
SD Found in Table: {sd_check['sd_found']}
Evidence: {sd_check['evidence']}

**IMPORTANT NOTES:**
- Students submit text descriptions since visual elements (actual JASP tables) cannot be captured in text
- If student REFERENCES a table (e.g., "Table 1", "see table below", "the descriptive statistics table shows"), ASSUME the table exists in their actual document
- DO NOT penalize for "missing" tables if they clearly reference and discuss the table content
- Focus on whether they understand what they're doing, not just whether the visual is literally present in the text

**HYBRID GRADING APPROACH:**

**Component 1: Introduction phrase with reference - VIBE (0-5 points)**
- Focus: Does the student introduce their analysis with proper reference to the table?
- Examples of good intro: "Table 1 presents descriptive statistics for the LikeLike dataset" or "Descriptive statistics are shown in Table 1"
- Be generous: any reasonable introduction that references a table is acceptable
- Deduct only if: no introduction at all, or introduction doesn't reference the table

**Component 2: APA table numbering and naming - STRICT (0-5 points)**
- 0 points: No table number or title mentioned
- 2-3 points: Has table number OR title, but not both, or formatting issues
- 4 points: Has both number and title, minor APA issues
- 5 points: Proper APA format: "Table 1" (or Table #) followed by descriptive title
- **STRICT REQUIREMENT**: Must mention BOTH table number AND table title

**Component 3: SD removed and table copied - STRICT (0-5 points)**
- **USE THE AUTOMATIC SD DETECTION RESULT ABOVE**
- If SD was found (sd_found = True):
  - 0 points: SD is present in the table - student failed to remove it
  - Award 0 points regardless of other factors
- If SD was NOT found (sd_found = False):
  - 3-4 points: Table referenced but minimal description
  - 5 points: Table properly referenced/described AND SD successfully removed
- **STRICT REQUIREMENT**: SD must be absent from the submitted table text

**Component 4: Frequencies, cumulative frequencies, and percentiles - STRICT (0-5 points)**
- 0 points: No frequency table or values present
- 2-3 points: Only one or two of the three measures present (e.g. frequencies only, missing cumulative or percentiles)
- 4 points: All three measures present but with minor errors or omissions
- 5 points: All three measures correctly calculated and presented: frequencies, cumulative frequencies, and percentiles
- **STRICT REQUIREMENT**: Must include ALL THREE: frequencies, cumulative frequencies, AND percentiles

**CRITICAL RULES:**
1. Components 2, 3, and 4 are STRICT - must have required elements
2. Component 1 is VIBE - focus on understanding and intent
3. Component 3 is automatically checked - if SD appears in text, score must be 0 for that component
4. Be generous with table references - if they discuss the table, assume it exists
5. Focus on statistical understanding, not just formatting perfection

**SCORING PROCESS:**
1. Score Component 1 (Introduction with reference) - VIBE: __/5
2. Score Component 2 (APA numbering and naming) - STRICT: __/5
3. Score Component 3 (SD removed + table copied) - STRICT: __/5 (MUST be 0 if sd_found = True)
4. Score Component 4 (Frequencies, cumulative frequencies, and percentiles) - STRICT: __/5
5. Total = sum of four scores

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- Acknowledges what they did well
- If SD was found, explicitly mention: "The table still contains Standard Deviation, which should have been removed"
- Points out any missing strict requirements specifically
- Comments on their statistical understanding
- Explains what would improve their score
- Remains encouraging and constructive

Return your grading in this exact JSON format:
{{
  "component_1_score": <0-5>,
  "component_2_score": <0-5>,
  "component_3_score": <0-5, MUST be 0 if sd_found=True>,
  "component_4_score": <0-5>,
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative explanation - what they did well, what's missing (especially if SD not removed), how to improve>",
  "vibe": "<one-sentence overall impression of their understanding of descriptive statistics and APA formatting>"
}}"""

        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"sd_check": sd_check, "formatting_check": formatting_check}
        )

        # If grading succeeded, validate and enforce safety checks
        if "error" not in result:
            # Validate component scores sum correctly
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score"
            ]
            result = self.validate_component_scores(result, component_keys, 20)

            # Enforce SD removal penalty if needed
            if sd_check['sd_found'] and result.get('component_3_score', 0) > 0:
                print("\n⚠️  WARNING: AI gave points for Component 3 despite SD being present. Correcting to 0.")
                result['component_3_score'] = 0
                result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """
        Display grading results using OutputFormatter.

        Args:
            grading: Grading result dictionary
        """
        component_labels = {
            "component_1_score": "Component 1 (Introduction with reference)",
            "component_2_score": "Component 2 (APA table numbering and naming)",
            "component_3_score": "Component 3 (SD removed + table copied)",
            "component_4_score": "Component 4 (Frequencies, cumulative frequencies, percentiles)"
        }

        component_types = {
            "component_1_score": "VIBE",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT"
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 2_1",
            question_description="Distributions and Graphs - Frequencies Table",
            component_labels=component_labels,
            max_score=5,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )