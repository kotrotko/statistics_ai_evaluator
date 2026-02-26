"""
question2_2_evaluator.py
APA Format Findings + Diagram Insertion + Diagram Formatting + JASP Progressive Disclosure
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter


class Question2_2Evaluator(BaseEvaluator):
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

    def grade_question2_2_answer(self, student_answer: str, test_mode: bool = False):
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
                    "component_4_score": 4,
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

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Students must:
1. Describe findings using APA format as demonstrated in video (5 points)
2. Insert the diagram of frequency distribution (5 points)
3. Introduce, number, and title the diagram as "Figure 1" or "Diagram 1" (5 points)
4. Answer: What is the progressive disclosure option in JASP? (5 points)

Total: 20 points

STUDENT ANSWER:
{student_answer}

**IMPORTANT NOTES:**
- Students submit text descriptions of their work since visual elements (actual diagrams, screenshots, formatted documents) cannot be captured in text
- If student REFERENCES or DESCRIBES the required elements (e.g., "I used APA format to describe findings", "I inserted the frequency distribution diagram"), ASSUME they completed it in their actual document
- DO NOT penalize for "missing" visual elements if they clearly describe what they did

**HYBRID GRADING APPROACH:**

**PRECONDITION CHECK:**
Before scoring Component 1, check if the student provided ANY statistical description with APA format elements (e.g., M =, SD =, mean, median, percentage, n =, p <, t =, F =, r =).
- If NO statistical tokens found → Component 1 score = 0. Do not proceed to rubric tiers.
- If statistical tokens present → Proceed to score using the rubric below.

**Component 1: APA Format Description - STRICT (0-5 points)**
- 5 points: Student provided findings described in proper APA format (e.g., "M = 85.5, SD = 12.3")
- 4 points: Provided APA format description with minor issues (1-2 small formatting errors)
- 2-3 points: Provided statistical description but APA format has multiple major errors
- 0 points: Did not provide any description of findings

**Component 2: Diagram Insertion - STRICT (0-5 points)**
- 0 points: No diagram inserted
- 1 point: Attempted to insert diagram but with major issues or completely incorrect diagram type
- 3 points: Inserted diagram but with significant placement/sizing/formatting issues
- 4 points: Correctly inserted frequency distribution diagram with minor placement/sizing issues
- 5 points: Student correctly inserted the frequency distribution diagram with proper placement and sizing

**Component 3: Diagram Introduction/Numbering/Title - STRICT (0-5 points)**
- 0 points: No diagram number or title
- 1 point: Has only number OR title (not both)
- 3 points: Has both number and title but incorrect number (not Figure 1/Diagram 1)
- 4 points: Correctly numbered (Figure 1/Diagram 1) and titled but missing introductory sentence
- 5 points: Student correctly introduced, numbered (Figure 1/Diagram 1), and titled the diagram

**Component 4: Progressive Disclosure Explanation - STRICT (0-5 points)**
- 5 points: Student correctly explained what progressive disclosure is in JASP (feature that reveals analysis options step-by-step/gradually)
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
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative explanation - which elements they completed well, what's missing, how to improve>",
  "vibe": "<one-sentence overall impression of their academic formatting and technical knowledge>"
}}"""
        # Check for required elements
        element_check = self.check_required_elements(student_answer)

        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"element_check": element_check}
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
        """
        Display grading results using OutputFormatter.

        Args:
            grading: Grading result dictionary
        """
        # Define component labels
        component_labels = {
            "component_1_score": "Component 1 (APA Format Findings)",
            "component_2_score": "Component 2 (Diagram Insertion)",
            "component_3_score": "Component 3 (Diagram Number/Title)",
            "component_4_score": "Component 4 (Progressive Disclosure)"
        }

        # Define component types (all STRICT for this question)
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT"
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 2_2",
            question_description="APA Format + Diagram + Numbering + JASP",
            component_labels=component_labels,
            max_score=5,
            component_types=component_types,
            check_configs=None,  # No automatic checks for this question
            width=60,
            mode="HYBRID"
        )