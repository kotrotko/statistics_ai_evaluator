"""
cw9_3.py
Classwork 9: Independent groups comparison
Assumption checking: homogeneity of variance
Evaluation method name: def grade_question_cw9_3_answer
"""

import re
from config import BaseEvaluator


class CW9_3Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 9_3.

    Task: Which method will you apply to check variance homogeneity? (5 points).
    Include the relevant table in APA style (5 points).
    Are the variances homogenous, with significance level α = 0.05? How did you know? Describe your logic (5 points).
    Based on normality and homogeneity of variance checking result, determine which form of the chosen statistical method should be applied and justify your decision (5 points).
    Total (strictly) 20 points.

    Evaluates student's ability to name the variance homogeneity method, present table in APA style,
    state whether variances are homogenous at α = 0.05, explain reasoning, and determine appropriate statistical method form.

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    def __init__(self):
        """Initialize the evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1200
        )

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check if required elements are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "variance_method": False,
            "table_present": False,
            "homogeneity_conclusion": False,
            "method_choice": False
        }

        evidence = []

        # Checkpoint 1 — Task description (Pedagogical Anchor)
        # Use phrases unique to your instructional style
        pedagogical_markers = [
            "which method",
            "name it",
            "describe your logic",
            "justify your decision",
            "refer, number and title"
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found (via pedagogical anchors)")
        else:
            elements_found["task_description"] = False
            evidence.append("Task description NOT found")

        # Checkpoint 2 — Variance homogeneity method
        if re.search(r'levene[\s\']?s?\s*test|levene|bartlett', text_lower):
            elements_found["variance_method"] = True
            evidence.append("Variance homogeneity method found")
        else:
            evidence.append("Variance homogeneity method NOT found")

        # Checkpoint 3 — Table present
        if re.search(r'table\s*\d|p[\s-]?value|statistic', text_lower):
            elements_found["table_present"] = True
            evidence.append("Table found")
        else:
            evidence.append("Table NOT found")

        # Checkpoint 4 — Homogeneity conclusion (yes/no)
        if re.search(r'variance\s*is\s*(not\s*)?homogenous|homogeneity|variances\s*are\s*(not\s*)?homogenous|equal\s*variance', text_lower):
            elements_found["homogeneity_conclusion"] = True
            evidence.append("Homogeneity conclusion found")
        else:
            evidence.append("Homogeneity conclusion NOT found")

        # Checkpoint 5 — Method choice based on assumptions
        if re.search(r'(student|welch|t[\s-]?test|anova|mann[\s-]?whitney|kruskal[\s-]?wallis)', text_lower) and \
                re.search(r'(normality|variance|homogeneity|assumption)', text_lower):
            elements_found["method_choice"] = True
            evidence.append("Method choice with justification found")
        else:
            evidence.append("Method choice with justification NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_question_cw9_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 9.3: Assumption Checking - Homogeneity of Variance.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 1,
                    "component_2_score": 4,
                    "component_3_score": 5,
                    "component_4_score": 5,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Method stated. Table present with good APA formatting. Homogeneity conclusion clear with proper reasoning. Method choice justified.",
                vibe="Student demonstrates solid understanding of variance homogeneity testing and method selection",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "variance_method": True,
                            "table_present": True,
                            "homogeneity_conclusion": True,
                            "method_choice": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics assignment about variance homogeneity checking using a **STRICT rubric-based approach.

**TASK DESCRIPTION:**
Students must complete 4 components for homogeneity of variance assumption checking.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Focus on conceptual understanding over formatting
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. Check for originality first; copied AI text should receive 0 points with comment: "Due to originality concern, your points are frozen. You can get them back if you provide oral explanation for this paper."

**RUBRIC:**

**Component 1: Task Description (1 point)**
- Use task_description from elements_found.
- 1/1: If task_description_present is True.
- 0/1: If task_description_present is False.

**Component 2: Name the Variance Homogeneity Method (4 points):**
- 4/4: Method name explicitly stated in a sentence (e.g., "I used the Levene test") OR mentioned in the table introduction phrase
- 2/4: Method mentioned but statement incomplete or unclear
- 0/4: Method name only in table header, or not mentioned at all
- CRITICAL: Method can be stated in dedicated sentence OR in table introduction phrase, but NOT only in table header

Acceptable method: Levene's test

**Component 3: Table in APA Style (5 points):**
- 5/5: Levene's table present with all APA elements: introduction phrase (may include method name), reference to table by number, table number in APA style, table title in APA style, table itself
- 3/5: Table present with some APA elements but missing some requirements
- 0/5: No table present
- CRITICAL: Must include introduction phrase, reference by number, table number, table title, and the table

APA table requirements:
1. Introduction before table appears
2. Reference to table in text (e.g., "as shown in Table 1")
3. Table number (e.g., "Table 1")
4. Descriptive title
5. Proper formatting (horizontal lines, clear labels)

**Component 4: Is Variance Homogenous? (5 points):**
- 5/5: Clear yes/no statement about variance homogeneity at α = 0.05 and a correct explanation of reasoning based on Levene's test, explicitly linking p-value to α
- 3/5: Yes/no statement is present but reasoning is partial, vague, or missing details connecting the test result to α
- 2/5: Reasoning is unclear, incomplete, or misapplied; yes/no may be correct by chance
- 1/5: No clear yes/no statement; or conclusion contradicts test results
- 0/5: No any answer, the component is totally omitted
- CRITICAL: Must explicitly mention test results and significance level α = 0.05

**Component 5: Determine Statistical Method Form (5 points):**
- 5/5: Clearly states which form of the statistical method should be applied and provides a correct justification based on normality and variance homogeneity results, explicitly linking test outcomes to the choice
- 3/5: States the method form but reasoning is partial, vague, or missing some connection to normality or variance results
- 1/5: Choice or justification is unclear, incomplete, or incorrectly linked to normality/variance results
- 0/5: No method form stated or justification is absent/contradicts the checking results
- CRITICAL: Must explicitly refer to both normality and variance homogeneity results when explaining the choice

STUDENT ANSWER:
{student_answer}

Return grading in this exact JSON format:
{{
  "component_1_score": <0-1>,
  "component_1_explanation": "<brief explanation>",
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief explanation>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief explanation>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief explanation>",
  "component_5_score": <0-5>,
  "component_5_explanation": "<brief explanation>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment>",
  "vibe": "<one-sentence overall impression>"
}}"""

        element_check = self.check_required_elements(student_answer)
        element_summary = element_check["elements_found"]

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "element_check": element_check
            }
        )

        # Force the score to 0 if the pedagogical anchors are missing
        if "error" not in result:
            if not element_check["elements_found"]["task_description"]:
                result["component_1_score"] = 0
                result["component_1_explanation"] = "Task description NOT found (instructional phrasing missing)"

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
        """Display grading results."""
        import textwrap
        print("=" * 60)
        print("GRADING RESULTS - CLASSWORK 9.3")
        print("Assumption Checking: Homogeneity of Variance")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Task Description): {grading.get('component_1_score', 'N/A')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Variance Homogeneity Method): {grading.get('component_2_score', 'N/A')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Table APA Style): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Homogeneity Conclusion): {grading.get('component_4_score', 'N/A')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Method Form Selection): {grading.get('component_5_score', 'N/A')}/5")
            if grading.get('component_5_explanation'):
                print(f"    → {grading.get('component_5_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points', 'N/A')}/{grading.get('max_points', 20)}")
        print(f"PERCENTAGE: {grading.get('percentage', 'N/A')}%")

        print("\n" + "=" * 60)
        print("FEEDBACK:")
        print("=" * 60)
        print(textwrap.fill(grading.get('feedback', 'No feedback available'), width=60))

        print("\n" + "=" * 60)
        print("THE VIBE:")
        print("=" * 60)
        print(textwrap.fill(grading.get('vibe', 'N/A'), width=60))

        if 'error' in grading:
            print("\n" + "=" * 60)
            print("ERROR:")
            print("=" * 60)
            print(grading.get('error'))
            if 'raw_response' in grading:
                print("\nRaw Response:")
                print(grading['raw_response'][:500])


if __name__ == "__main__":
    evaluator = CW9_3Evaluator()
    from config import InputHandler

    input_handler = InputHandler()
    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 9.3",
        question_description="Assumption Checking: Homogeneity of Variance",
        min_length=10
    )
    if student_answer:
        grading = evaluator.grade_question_cw9_3_answer(student_answer)
        evaluator.print_grading_results(grading)