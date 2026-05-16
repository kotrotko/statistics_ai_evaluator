"""
cw1_2.py
Classwork 1: File management: Basic skills
Mean Calculation with JASP
Evaluation method name: def grade_question_cw1_1_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter

class CW1_2Evaluator(BaseEvaluator):
    """
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
        """
        Check formatting elements in the student's answer.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with elements_found (dict of bools) and evidence (list of str)
        """
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "autoformatting": False,
        }

        evidence = []

        # Key phrases that would only appear if the student copied the task description
        pedagogical_markers = [
            "what is valid?",
            "what is missing?",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # autoformatting
        # catches bullet points: - item, • item, * item
        autoformat_violations = len(re.findall(r'^\s*[-•*]\s', student_answer, re.MULTILINE))
        print(f"DEBUG autoformat_violations: {autoformat_violations}")

        if autoformat_violations > 0:
            evidence.append("Autoformatting detected")
        else:
            elements_found["autoformatting"] = True
            evidence.append("No autoformatting detected")

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

    def grade_question_cw1_2_answer(self, student_answer: str, test_mode: bool = False):
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
                    "component_1_score": 2,
                    "component_2_score": 5,
                    "component_3_score": 4,
                    "component_4_score": 4,
                    "component_5_score": 5
                },
                max_points=20,
                feedback="Excellent work with proper APA formatting and clear explanations of Valid and Missing values.",
                vibe="Student demonstrates strong understanding of descriptive statistics and APA style",
                additional_data={
                    "sd_check": {"sd_found": False, "evidence": "Test mode - SD properly removed"}
                }
            )
        # Check formatting elements
        formatting_check = self.check_formatting_elements(student_answer)

        # Check if SD was removed
        sd_check = self.check_sd_removed(student_answer)

        # Build the grading prompt
        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - combining vibe-based holistic grading with strict requirements for specific components.

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

**AUTOMATIC FORMATTING DETECTION RESULT:**
Task description present (1 point if True): {formatting_check['elements_found']['task_description']}
No autoformatting (1 point if True): {formatting_check['elements_found']['autoformatting']}
Evidence: {formatting_check['evidence']}

**Component 1: Formatting (2 points)**

Step 1 Task description (1 point)
Use task_description_present.

Step 2 No autoformatting (1 point)
Use autoformatting_present.

**Component 2: Introduction phrase with reference - VIBE (0-5 points)**
- Focus: Does the student introduce their analysis with proper reference to the table?
- Examples of good intro: "Table 1 presents descriptive statistics for the LikeLike dataset" or "Descriptive statistics are shown in Table 1"
- Be generous: any reasonable introduction that references a table is acceptable
- Deduct only if: no introduction at all, or introduction doesn't reference the table

**Component 3: APA table numbering and naming - STRICT (0-4 points, MAX 4)**
- 4 points: Proper APA format: "Table 1" (or Table #) followed by descriptive title
- 3 points: Has both number and title, minor APA issues
- 2 points: Has table number OR title, but not both, or formatting issues
- 0 points: No table number or title mentioned
- **STRICT REQUIREMENT**: Must mention BOTH table number AND table title
- **HARD LIMIT**: component_3_score MUST NOT exceed 4

**Component 4: SD removed and table copied - STRICT (0-4 points, MAX 4)**
- **USE THE AUTOMATIC SD DETECTION RESULT ABOVE**
- If SD was found (sd_found = True):
  - 0 points: SD is present in the table - student failed to remove it
  - Award 0 points regardless of other factors
- If SD was NOT found (sd_found = False):
  - 4 points: Table properly referenced/described AND SD successfully removed
  - 2-3 points: Table referenced but minimal description
- **STRICT REQUIREMENT**: SD must be absent from the submitted table text
- **HARD LIMIT**: component_4_score MUST NOT exceed 4

**Component 5: Explain Valid and Missing - STRICT (0-5 points)**
- 5 points: Clear explanation of both Valid (cases with data) and Missing (cases without data)
- 4 points: Explains both but could be clearer
- 2-3 points: Explains only one (Valid OR Missing) OR very superficial
- 0 points: No explanation of Valid and Missing
- **STRICT REQUIREMENT**: Must explain BOTH Valid AND Missing

**CRITICAL RULES:**
1. Components 3, 4, and 5 are STRICT - must have required elements
2. Component 2 is VIBE - focus on understanding and intent
3. Component 4 is automatically checked - if SD appears in text, score must be 0 for that component
4. Be generous with table references - if they discuss the table, assume it exists
5. Focus on statistical understanding, not just formatting perfection

**SCORING PROCESS:**
1. Score Component 1 (Formatting) - STRICT: __/2
2. Score Component 2 (Introduction with reference) - VIBE: __/5
3. Score Component 3 (APA numbering and naming) - STRICT: __/4
4. Score Component 4 (SD removed + table copied) - STRICT: __/4 (MUST be 0 if sd_found = True)
5. Score Component 5 (Valid and Missing explanation) - STRICT: __/5
6. Total = sum of four scores

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- Acknowledges what they did well
- If SD was found, explicitly mention: "The table still contains Standard Deviation, which should have been removed"
- Points out any missing strict requirements specifically
- Comments on their statistical understanding
- Explains what would improve their score
- Remains encouraging and constructive

Return JSON only:
{{
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-4, MUST be 0 if sd_found=True>,
  "component_4_explanation": "<brief>",
  "component_5_score": <0-5>,
  "component_5_explanation": "<brief>",
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative explanation - what they did well, what's missing (especially if SD not removed), how to improve>",
  "vibe": "<one-sentence overall impression of their understanding of descriptive statistics and APA formatting>"
}}
"""

        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "formatting_check": formatting_check,
                "sd_check": sd_check}
        )

        # If grading succeeded, validate and enforce safety checks
        if "error" not in result:
            # Validate component scores sum correctly
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score",
                "component_5_score"
            ]
            result = self.validate_component_scores(result, component_keys, 20)

            # Enforce SD removal penalty if needed
            if sd_check['sd_found'] and result.get('component_4_score', 0) > 0:
                print("\n⚠️  WARNING: AI gave points for Component 4 despite SD being present. Correcting to 0.")
                result['component_4_score'] = 0
                result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results using OutputFormatter.

        Args:
            grading: Grading result dictionary
        """
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Introduction phrase with reference",
            "component_3_score": "APA table numbering and naming",
            "component_4_score": "SD removed and table copied",
            "component_5_score": "Explain Valid and Missing",
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "VIBE",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT",
            "component_5_score": "STRICT",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 5,
            "component_3_score": 4,
            "component_4_score": 4,
            "component_5_score": 5,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="CW1_2",
            question_description="Mean Calculation with JASP",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )