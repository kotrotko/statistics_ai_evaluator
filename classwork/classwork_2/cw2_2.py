"""
cw2_2.py
APA Format Findings + Diagram Insertion + Diagram Formatting + JASP Progressive Disclosure
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter


class CW2_2Evaluator(BaseEvaluator):
    """
    Evaluator for Question 2_2: APA Format, Diagram Insertion, and JASP Features.

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
        # Initialize output formatter
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
            "do not forget",
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

    def check_required_elements(self, student_answer: str) -> dict:

        """
        Check if required elements (APA format, diagram, numbering, JASP) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "apa_format": False,
            "diagram_inserted": False,
            "diagram_numbered": False,
            "progressive_disclosure": False
        }

        evidence = []

        # Check for APA format-related terms
        apa_patterns = [r'\bapa\b', r'\bformat\b', r'\bcitation\b', r'\breference\b', r'\bitalic\b']
        for pattern in apa_patterns:
            if re.search(pattern, text_lower):
                elements_found["apa_format"] = True
                evidence.append(f"Found APA format indicator: {pattern}")
                break

        # Check for diagram insertion
        diagram_patterns = [r'\bdiagram\b', r'\bfigure\b', r'\bchart\b', r'\bgraph\b', r'\binsert\b', r'\bfrequency distribution\b']
        for pattern in diagram_patterns:
            if re.search(pattern, text_lower):
                elements_found["diagram_inserted"] = True
                evidence.append(f"Found diagram indicator: {pattern}")
                break

        # Check for diagram numbering/titling
        numbering_patterns = [r'\bfigure 1\b', r'\bdiagram 1\b', r'\bnumber\b', r'\btitle\b', r'\bcaption\b']
        for pattern in numbering_patterns:
            if re.search(pattern, text_lower):
                elements_found["diagram_numbered"] = True
                evidence.append(f"Found numbering/title indicator: {pattern}")
                break

        # Check for progressive disclosure
        jasp_patterns = [r'\bprogressive disclosure\b', r'\bjasp\b', r'\bdisclosure\b', r'\bprogressive\b']
        for pattern in jasp_patterns:
            if re.search(pattern, text_lower):
                elements_found["progressive_disclosure"] = True
                evidence.append(f"Found JASP/progressive disclosure indicator: {pattern}")
                break

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_question_cw2_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 2_2: APA format findings, diagram insertion, numbering, and JASP question.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        # Test mode for verification without API
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 4,
                    "component_2_score": 5,
                    "component_3_score": 5,
                    "component_4_score": 5,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Good work on diagram insertion and numbering. APA format needs minor improvements.",
                vibe="Student demonstrates solid understanding of academic formatting and JASP features",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "apa_format": True,
                            "diagram_inserted": True,
                            "diagram_numbered": True,
                            "progressive_disclosure": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        # Check formatting elements
        formatting_check = self.check_formatting_elements(student_answer)

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Task 2. Introduce, number, and title your diagram 1 as a Figure 1 (5 points). Create and insert the JASP diagram of frequency distribution (5 points). Display density (5 points). What is the progressive disclosure option in JASP? (5 points).
Total: 20 points

STUDENT ANSWER:
{student_answer}

**IMPORTANT NOTES:**
- Students submit text descriptions of their work since visual elements (actual diagrams, screenshots, formatted documents) cannot be captured in text
- If student REFERENCES or DESCRIBES the required elements (e.g., "I used APA format to describe findings", "I inserted the frequency distribution diagram"), ASSUME they completed it in their actual document
- DO NOT penalize for "missing" visual elements if they clearly describe what they did

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

**Component 2: Introduce, number, and title diagram - STRICT (0-3 points, MAX 3)**
- 3 points: Correctly introduced, numbered (Figure 1/Diagram 1), and titled the diagram
- 2 points: Correctly numbered and titled but missing introductory sentence
- 1 point: Has only number OR title (not both)
- 0 points: No diagram number or title mentioned
- **STRICT REQUIREMENT**: Must have BOTH number AND title
- **HARD LIMIT**: component_2_score MUST NOT exceed 3

**Component 3: Create and insert JASP frequency distribution diagram - STRICT (0-5 points)**
- 5 points: Correctly created and inserted the frequency distribution diagram from JASP
- 4 points: Diagram inserted with minor issues
- 2-3 points: Diagram inserted but with significant issues
- 0 points: No diagram inserted

**Component 4: Display density - STRICT (0-5 points)**
- 5 points: Density is correctly displayed on the diagram
- 4 points: Density displayed with minor issues
- 2-3 points: Partial or unclear density display
- 0 points: Density not displayed

**Component 5: Progressive disclosure explanation - STRICT (0-5 points)**
- 5 points: Correctly explained progressive disclosure in JASP (shows basic results first, advanced options appear when selected)
- 4 points: Correct explanation with minor inaccuracies
- 2-3 points: Partial understanding or vague explanation
- 0-1 points: Incorrect explanation or did not answer

**CRITICAL RULES:**
1. Each component is STRICT - must be present to earn points
2. If student meets requirements exactly: 5/5 points
3. If student does extra correct work beyond requirements: 5/5 points + praise in explanation
4. Minor issues are acceptable if the core requirement is met
5. PRECONDITION for Component 1: Check for statistical tokens FIRST. No tokens = 0 points automatically, skip rubric evaluation.

**SCORING PROCESS:**
1. Score Component 1 (APA Format): __/5
2. Score Component 2 (Diagram Insertion): __/5
3. Score Component 3 (Numbering/Title): __/5
4. Score Component 4 (Progressive Disclosure): __/5
5. Total = sum of four scores

**FEEDBACK STRUCTURE:**

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- Acknowledges what elements they successfully completed
- Points out any missing components specifically
- Explains what would improve their score
- Remains encouraging and constructive

Return JSON only:
{{
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-3>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief>",
  "component_5_score": <0-5>,
  "component_5_explanation": "<brief>",
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative explanation - what they did well, what's missing, how to improve>",
  "vibe": "<one-sentence overall impression of their understanding of diagram formatting and JASP features>"
}}"""

        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"formatting_check": formatting_check}
        )

        # If grading succeeded, validate component scores
        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score",
                "component_5_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """
        Display grading results using OutputFormatter.

        Args:
            grading: Grading result dictionary
        """
        # Define component labels
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Introduce, number, and title diagram",
            "component_3_score": "Insert JASP frequency distribution diagram",
            "component_4_score": "Display density",
            "component_5_score": "Progressive disclosure explanation",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT",
            "component_5_score": "STRICT",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 3,
            "component_3_score": 5,
            "component_4_score": 5,
            "component_5_score": 5,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 2_2",
            question_description="APA Format + Diagram + Numbering + JASP",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,  # No automatic checks for this question
            width=60,
            mode="HYBRID"
        )