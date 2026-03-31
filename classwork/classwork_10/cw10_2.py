"""
cw10_2.py
Classwork 10: One-Way ANOVA
Assumption checking: normality and variance homogeneity
Evaluation method name: def grade_question_cw10_2_answer
"""

import re
from config import BaseEvaluator


class CW10_2Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 10_2.

    Task: Check normality assumption (5 points).
    Which method did you apply to check normality? Include the graph, number and title it in APA style (5 points).
    Check variance homogeneity and provide your conclusion about homogeneity (5 points).
    Name the method you used. Include the table, number and name it (5 points).
    Total (strictly) 20 points.

    Evaluates student's ability to check normality, present graph in APA style,
    check variance homogeneity, and present table in APA style.

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
            "normality_method": False,
            "graph_present": False,
            "homogeneity_method": False,
            "homogeneity_conclusion": False,
            "table_present": False
        }

        evidence = []

        # Checkpoint 1 — Task description (Pedagogical markers)
        pedagogical_markers = [
            "check normality",
            "which method",
            "include the graph",
            "check variance homogeneity",
            "name the method",
            "include the table",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found (via pedagogical markers)")
        else:
            elements_found["task_description"] = False
            evidence.append("Task description NOT found")

        # Checkpoint 2 — Normality method
        if re.search(r'shapiro[\s-]?wilk|s-w\s*test|q[\s-]?q\s*plot|qq\s*plot|normality\s*test', text_lower):
            elements_found["normality_method"] = True
            evidence.append("Normality method found")
        else:
            evidence.append("Normality method NOT found")

        # Checkpoint 3 — Graph present
        if re.search(r'figure\s*\d|graph|plot|q[\s-]?q|histogram', text_lower):
            elements_found["graph_present"] = True
            evidence.append("Graph found")
        else:
            evidence.append("Graph NOT found")

        # Checkpoint 4 — Homogeneity method
        if re.search(r'levene|bartlett|variance\s*homogeneity|homogeneity\s*test|homoscedasticity', text_lower):
            elements_found["homogeneity_method"] = True
            evidence.append("Homogeneity method found")
        else:
            evidence.append("Homogeneity method NOT found")

        # Checkpoint 5 — Homogeneity conclusion
        if re.search(r'variance\s*(is|are)\s*(not\s*)?homogeneous|homogeneity\s*(is|are)\s*(not\s*)?satisfied|equal\s*variance', text_lower):
            elements_found["homogeneity_conclusion"] = True
            evidence.append("Homogeneity conclusion found")
        else:
            evidence.append("Homogeneity conclusion NOT found")

        # Checkpoint 6 — Table present
        if re.search(r'table\s*\d|p[\s-]?value|statistic|levene|bartlett', text_lower):
            elements_found["table_present"] = True
            evidence.append("Table found")
        else:
            evidence.append("Table NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_question_cw10_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 10.2: Assumption Checking - Normality and Variance Homogeneity.
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
                feedback="[TEST MODE] Normality check complete. Graph present with minor APA issues. Homogeneity conclusion clear. Table present.",
                vibe="Student shows solid understanding of assumption checking and APA formatting",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "task_description": True,
                            "normality_method": True,
                            "graph_present": True,
                            "homogeneity_method": True,
                            "homogeneity_conclusion": True,
                            "table_present": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics assignment about normality and variance homogeneity checking using a **STRICT rubric-based approach.

**TASK DESCRIPTION:**
Students must complete 5 components for assumption checking (normality and variance homogeneity).

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Focus on conceptual understanding over formatting
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

**RUBRIC:**

**Component 1: Task Description (1 point):**
- 1 point: Student includes pedagogical markers indicating they understand the task
- 0 points: No task description present

**Component 2: Check Normality & Name Method with Graph in APA (4 points):**
This component combines:
- Normality check performed
- Method named
- Graph included, numbered and titled in APA style

Breaking down the 4 points:
- 1 point: Normality assumption check attempted/mentioned
- 1 point: Method explicitly named (e.g., "I used Q-Q plots" or "Shapiro-Wilk test")
- 1 point: Graph/figure is present and referenced
- 1 point: Figure number in APA style (e.g., "Figure 1")

Acceptable normality methods: Shapiro-Wilk test, Q-Q plot, histogram with normal curve

APA figure requirements:
1. Reference to figure in text (e.g., "as shown in Figure 1")
2. Figure number (e.g., "Figure 1")
3. Descriptive title/caption
4. Figure appears after being referenced

**Component 3: Which Method for Normality (5 points):**
- 5/5: Method name explicitly stated in a clear sentence (e.g., "I used Q-Q plots to check normality")
- 3/5: Method mentioned but statement incomplete or unclear
- 1/5: Method implied or only mentioned in figure caption
- 0/5: Method not mentioned at all

CRITICAL: Method can be stated in dedicated sentence OR in figure introduction phrase, but NOT only in figure caption

**Component 4: Check Variance Homogeneity & Provide Conclusion (5 points):**
This component combines:
- Homogeneity check performed
- Clear conclusion about whether variances are homogeneous

Breaking down the 5 points:
- 2 points: Homogeneity test performed/attempted
- 3 points: Clear yes/no conclusion about variance homogeneity (e.g., "variances are homogeneous" or "variances are not equal")

CRITICAL: Must explicitly state whether variances are homogeneous or not
CRITICAL: Conclusion should be based on test results and appropriate significance level

**Component 5: Name Homogeneity Method & Include Table in APA (5 points):**
This component combines:
- Method named
- Table included, numbered and named in APA style

Breaking down the 5 points:
- 1 point: Homogeneity method explicitly named (e.g., "Levene's test")
- 1 point: Table present and referenced in text
- 1 point: Table number in APA style (e.g., "Table 1" or "Table 2")
- 1 point: Descriptive table title in APA style
- 1 point: Introduction phrase before table appears

Acceptable homogeneity methods: Levene's test

APA table requirements:
1. Introduction before table appears
2. Reference to table in text (e.g., "as shown in Table 1")
3. Table number (e.g., "Table 1")
4. Descriptive title
5. Proper formatting (horizontal lines, clear labels)

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

        # Enforcement: Task description
        if "error" not in result:
            if not element_check["elements_found"]["task_description"]:
                result["component_1_score"] = 0
                result["component_1_explanation"] = "Task description NOT found (instructional phrasing missing)"
            else:
                result["component_1_score"] = 1
                result["component_1_explanation"] = "Task description found"

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
        print("GRADING RESULTS - CLASSWORK 10.2")
        print("Assumption Checking: Normality and Variance Homogeneity")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Task Description): {grading.get('component_1_score', 'N/A')}/1")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Normality Check & Graph APA): {grading.get('component_2_score', 'N/A')}/4")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Which Method for Normality): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Homogeneity Check & Conclusion): {grading.get('component_4_score', 'N/A')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  Component 5 (Homogeneity Method & Table APA): {grading.get('component_5_score', 'N/A')}/5")
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
    evaluator = CW10_2Evaluator()
    from config import InputHandler

    input_handler = InputHandler()
    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 10.2",
        question_description="Assumption Checking: Normality and Variance Homogeneity",
        min_length=10
    )
    if student_answer:
        grading = evaluator.grade_question_cw10_2_answer(student_answer)
        evaluator.print_grading_results(grading)
