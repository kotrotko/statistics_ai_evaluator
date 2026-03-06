"""
hw2_1.py
Pie Chart vs Bar Chart Discussion Evaluator
"""

import re
import textwrap

from config import BaseEvaluator


class HW2_1Evaluator(BaseEvaluator):
    """
    Evaluator for Pie Chart vs Bar Chart Discussion Question.

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

    def check_formatting_elements(self, student_answer: str) -> dict:
        """
        Check if student includes required formatting elements.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "student_name": False,
            "task_description": False,
            "introductory_phrase": False,
            "figure_numbering": False,
            "explicit_conclusion": False,
            "formal_justification": False,
            "figure_reference": False
        }

        evidence = []

        # Check for student name (look for common name patterns or "name:" pattern)
        name_patterns = [
            r'\bname\s*:',
            r'\bstudent\s*:',
            r'\bby\s+[A-Z][a-z]+\s+[A-Z][a-z]+',
            r'^[A-Z][a-z]+\s+[A-Z][a-z]+'
        ]
        for pattern in name_patterns:
            if re.search(pattern, student_answer, re.MULTILINE):
                elements_found["student_name"] = True
                evidence.append(f"Found name indication: {pattern}")
                break

        # Check for task description
        task_patterns = [
            r'given the following data',
            r'construct a pie chart and a bar chart',
            r'which.*more appropriate.*display',
            r'task\s*:',
            r'question\s*:'
        ]
        for pattern in task_patterns:
            if re.search(pattern, text_lower):
                elements_found["task_description"] = True
                evidence.append(f"Found task description: {pattern}")
                break

        # Check for introductory phrase with figure reference
        intro_patterns = [
            r'(as|in|from)\s+(shown|displayed|presented|illustrated)\s+in\s+figure',
            r'figure\s+\d+\s+(shows|displays|presents|illustrates)',
            r'the\s+(following|above|below)\s+figure',
            r'based on\s+figure'
        ]
        for pattern in intro_patterns:
            if re.search(pattern, text_lower):
                elements_found["introductory_phrase"] = True
                evidence.append(f"Found introductory phrase: {pattern}")
                break

        # Check for figure numbering and titling (APA style)
        figure_patterns = [
            r'figure\s+\d+',
            r'fig\.\s+\d+'
        ]
        for pattern in figure_patterns:
            if re.search(pattern, text_lower):
                elements_found["figure_numbering"] = True
                evidence.append(f"Found figure numbering: {pattern}")
                break

        # Check for explicit conclusion about which is more appropriate
        conclusion_patterns = [
            r'(pie\s+chart|bar\s+chart)\s+is\s+(more|better|most)\s+(appropriate|useful|suitable)',
            r'i\s+(think|believe|conclude)\s+(the\s+)?(pie\s+chart|bar\s+chart)\s+is\s+(more|better)',
            r'(therefore|thus|hence|in conclusion),?\s+(the\s+)?(pie\s+chart|bar\s+chart)',
            r'(pie\s+chart|bar\s+chart)\s+should\s+be\s+used',
            r'(prefer|recommend|choose)\s+(the\s+)?(pie\s+chart|bar\s+chart)'
        ]
        for pattern in conclusion_patterns:
            if re.search(pattern, text_lower):
                elements_found["explicit_conclusion"] = True
                evidence.append(f"Found explicit conclusion: {pattern}")
                break

        # Check for formal justification (textbook criteria)
        justification_patterns = [
            r'(textbook|according to|based on)',
            r'(many|few)\s+categories',
            r'comparing.*distribution',
            r'formal\s+(criteria|reason)',
            r'statistical\s+(principle|guideline|rule)',
            r'p\.\s*\d+'  # page reference
        ]
        for pattern in justification_patterns:
            if re.search(pattern, text_lower):
                elements_found["formal_justification"] = True
                evidence.append(f"Found formal justification: {pattern}")
                break

        # Check for proper figure reference terminology
        figure_ref_patterns = [
            r'\bfigure\s+\d+',
            r'\bfig\.\s+\d+'
        ]
        # Should NOT contain improper references like "histogram", "pie chart" instead of "Figure"
        improper_patterns = [
            r'(the\s+)?(histogram|pie\s*chart|bar\s*chart)\s+(shows|displays|below|above)',
        ]

        has_proper_ref = any(re.search(pattern, text_lower) for pattern in figure_ref_patterns)
        has_improper_ref = any(re.search(pattern, text_lower) for pattern in improper_patterns)

        if has_proper_ref and not has_improper_ref:
            elements_found["figure_reference"] = True
            evidence.append("Found proper figure reference terminology")
        elif has_improper_ref:
            evidence.append("Found improper figure reference (using specific chart names instead of 'Figure')")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear formatting elements found"],
            "all_present": all(elements_found.values())
        }

    def grade_chart_comparison(self, student_answer: str, test_mode: bool = False):
        """
        Grade Pie Chart vs Bar Chart comparison question.

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
                    "component_1_score": 1,
                    "component_2_score": 1,
                    "component_3_score": 2,
                    "component_4_score": 2,
                    "component_5_score": 5,
                    "component_6_score": 5,
                    "component_7_score": 0
                },
                max_points=16,
                feedback="Test mode feedback for chart comparison task.",
                vibe="Test mode vibe assessment",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "student_name": True,
                            "task_description": True,
                            "introductory_phrase": True,
                            "figure_numbering": True,
                            "explicit_conclusion": True,
                            "formal_justification": True,
                            "figure_reference": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        # Check for formatting elements
        formatting_check = self.check_formatting_elements(student_answer)

        # Build the grading prompt
        prompt = f"""You are grading a statistics homework assignment where students must construct a pie chart and bar chart from given data, then discuss which is more appropriate.

**TASK DESCRIPTION:**
Students are given data and must:
1. Construct a pie chart
2. Construct a bar chart  
3. Discuss which is more appropriate or useful for displaying the data

**RUBRIC (16 points total):**

**Component 1: Student Name (1 point)**
- 1 point: Student's name is included
- 0 points: Name is missing

**Component 2: Task Description (1 point)**
- 1 point: Task description is copied/included before the answer
- 0 points: Task description is missing

**Component 3: Introductory Phrase with Figure Reference (2 points)**
- 2 points: Includes introductory phrase referring to the figure(s)
- 0 points: Missing introductory phrase

**Component 4: Figure Numbering and Titling (2 points)**
- 2 points: Figures are numbered and titled in APA style (e.g., "Figure 1", "Figure 2")
- 0 points: Figures not properly numbered/titled in APA style

**Component 5: Explicit Conclusion (5 points)**
- 5 points: Clear, direct statement of which chart type is more appropriate
- 2-3 points: Vague or indirect conclusion
- 0 points: No explicit conclusion given, only general discussion

**Component 6: Formal Justification (5 points)**
- 5 points: Choice justified by formal statistical criteria (textbook p. 43: bar charts for many categories or comparing distributions; pie charts for fewer categories)
- 2-3 points: Some reasoning given but not based on formal statistical criteria
- 0 points: Choice based only on personal preference or UX, no formal justification

**Component 7: Proper Figure Reference Terminology (0 points - bonus check)**
- Note: All graphic materials should be referred to as "Figures" not "Histogram", "Pie Chart", etc.
- This is a formatting note, already covered in Component 4

**STUDENT ANSWER:**
{student_answer}

**AUTOMATIC FORMATTING DETECTION RESULT:**
Elements Found: {formatting_check['elements_found']}
All Elements Present: {formatting_check['all_present']}
Evidence: {formatting_check['evidence']}

**GRADING GUIDELINES:**

For Component 1 (Name):
- Look for student's name anywhere in the submission
- 1 point if present, 0 if missing

For Component 2 (Task Description):
- Look for evidence that task description was copied
- Keywords: "given the following data", "construct", "pie chart and bar chart", "more appropriate"
- 1 point if present, 0 if missing

For Component 3 (Introductory Phrase):
- Look for phrases like "As shown in Figure 1", "The following figure displays", etc.
- Must reference the figure(s)
- 2 points if present, 0 if missing

For Component 4 (Figure Numbering):
- Look for "Figure 1", "Figure 2", or similar APA-style numbering
- Should include titles for figures
- 2 points if properly formatted, 0 if missing

For Component 5 (Explicit Conclusion):
- CRITICAL: Must explicitly state which chart type is more appropriate
- Not enough to say "both are acceptable" - must choose one
- Examples of explicit: "The pie chart is more appropriate", "I recommend the bar chart"
- 5 points: Clear, direct choice stated
- 2-3 points: Indirect or unclear choice
- 0 points: No explicit choice made

For Component 6 (Formal Justification):
- CRITICAL: Must use formal statistical criteria, not just personal preference
- According to textbook (p. 43): bar charts for many categories or comparing distributions; pie charts for fewer categories
- Should reference textbook, statistical principles, or formal guidelines
- 5 points: Clear formal justification based on statistical criteria
- 2-3 points: Some reasoning but mostly personal preference
- 0 points: Only UX or personal preference mentioned

**CRITICAL RULES:**
1. Component 5 requires explicit statement - "both work" or vague discussion = 0 points
2. Component 6 requires formal criteria - personal preference or UX alone = low/no points
3. Be strict on formatting requirements (Components 1-4)
4. For this specific task, according to textbook criteria, pie chart is typically better for fewer categories

**SCORING PROCESS:**
1. Score Component 1 (Name): __/1
2. Score Component 2 (Task Description): __/1
3. Score Component 3 (Introductory Phrase): __/2
4. Score Component 4 (Figure Numbering): __/2
5. Score Component 5 (Explicit Conclusion): __/5
6. Score Component 6 (Formal Justification): __/5
7. Total = sum of six scores (max 16)

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- Identifies which formatting elements are missing
- Notes whether explicit conclusion was given
- Assesses quality of justification (formal vs. personal preference)
- Explains the textbook criteria for chart selection
- Remains constructive and educational

Return your grading in this exact JSON format:
{{
  "component_1_score": <0-1>,
  "component_1_explanation": "<if score < full points: one sentence explaining what's missing; if full points AND exceptional work: one sentence of praise; otherwise empty string>",
  "component_2_score": <0-1>,
  "component_2_explanation": "<if score < full points: one sentence explaining what's missing; if full points AND exceptional work: one sentence of praise; otherwise empty string>",
  "component_3_score": <0-2>,
  "component_3_explanation": "<if score < full points: one sentence explaining what's missing; if full points AND exceptional work: one sentence of praise; otherwise empty string>",
  "component_4_score": <0-2>,
  "component_4_explanation": "<if score < full points: one sentence explaining what's missing; if full points AND exceptional work: one sentence of praise; otherwise empty string>",
  "component_5_score": <0-5>,
  "component_5_explanation": "<if score < 5: one sentence explaining what's missing or problematic; if score = 5 AND exceptional work: one sentence of praise; otherwise empty string>",
  "component_6_score": <0-5>,
  "component_6_explanation": "<if score < 5: one sentence explaining what's missing or problematic; if score = 5 AND exceptional work: one sentence of praise; otherwise empty string>",
  "total_points": <sum of above, 0-16>,
  "max_points": 16,
  "percentage": <percentage>,
  "feedback": "<narrative explanation covering formatting compliance, whether explicit conclusion was given, quality of justification, and reference to textbook criteria>",
  "vibe": "<one-sentence overall impression of their understanding of chart selection principles and academic formatting>"
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
                "component_6_score"
            ]
            result = self.validate_component_scores(result, component_keys, 16)

        return result

    def print_grading_results(self, grading):
        """Helper function to display grading results"""
        print("=" * 60)
        print("GRADING RESULTS - HW2_1")
        print("Pie Chart vs Bar Chart Discussion")
        print("=" * 60)

        # Print component breakdown if available
        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Student Name): {grading.get('component_1_score', 'N/A')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Task Description): {grading.get('component_2_score', 'N/A')}/1")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Introductory Phrase): {grading.get('component_3_score', 'N/A')}/2")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Figure Numbering/Titling): {grading.get('component_4_score', 'N/A')}/2")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Explicit Conclusion): {grading.get('component_5_score', 'N/A')}/5")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

            print(f"  Component 6 (Formal Justification): {grading.get('component_6_score', 'N/A')}/5")
            if grading.get('component_6_explanation'):
                print(f"    → {grading.get('component_6_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points', 'N/A')}/{grading.get('max_points', 16)}")
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
    print("Welcome to the Homework AI Evaluator System!")
    print("=" * 60)

    # Initialize evaluator
    evaluator = HW2_1Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("HOMEWORK 2 - QUESTION 2_1 EVALUATOR")
    print("Pie Chart vs Bar Chart Discussion")
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
    grading = evaluator.grade_chart_comparison(student_answer)

    # Display results
    evaluator.print_grading_results(grading)
