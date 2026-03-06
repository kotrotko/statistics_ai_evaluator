"""
cw8_4.py
Classwork 8: Repeated Measures
Means Comparison - Method Justification / Statistics Table / Inference / Effect Size / Plot
Evaluation method name: def grade_cw8_4_answer
"""

import re
from config import BaseEvaluator


class CW8_4Evaluator (BaseEvaluator):
    """
    Evaluator for Means Comparison Analysis (CW8_4).

    Task: Justify the method of means comparison (explain why this method is suitable for our problem solving,
    based on two assumption checking) (5 points). Using JASP, calculate the statistics and include the table
    in APA style (5 points), make a statistical inference (reject or fail to reject the null hypothesis) (5 points).
    Add Cohen's d effect size and explain what does it mean (5 points). Add and interpret the Descriptive plot (5 points).
    Total (strictly) 20 points.

    Evaluates student's ability to justify statistical method choice based on assumptions, present results in APA format
    with statistical inference, interpret effect sizes, and analyze descriptive visualizations.

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
        Check if required structural and content elements are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "method_justification": False,
            "table": False,
            "inference": False,
            "effect_size": False
        }

        evidence = []

        # Checkpoint 1 — Task description
        task_full_text = "Justify the method of means comparison (i.e. explain why this method is suitable for our problem solving, based on two assumption checking). Using JASP, calculate the statistics and include the table in APA style (5 points), make a statistical inference (reject or fail to reject the null hypothesis) (5 points). Add Cohen's d effect size and explain what does it mean (5 points). Add and interpret the Descriptive plot (5 points)."

        if task_full_text.lower() in text_lower:
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Checkpoint 2 — Method justification based on assumptions
        if re.search(r'assumption|suitable|appropriate|justif|because|since|based on', text_lower):
            elements_found["method_justification"] = True
            evidence.append("Method justification found")
        else:
            evidence.append("Method justification NOT found")

        # Checkpoint 3 — Table (APA style)
        if re.search(r'table|statistic|p[\s-]?value|t\s*=|f\s*=|df\s*=', text_lower):
            elements_found["table"] = True
            evidence.append("Table found")
        else:
            evidence.append("Table NOT found")

        # Checkpoint 4 — Statistical inference
        if re.search(r'reject|fail\s*to\s*reject|do\s*not\s*reject|accept|null\s*hypothesis', text_lower):
            elements_found["inference"] = True
            evidence.append("Statistical inference found")
        else:
            evidence.append("Statistical inference NOT found")

        # Checkpoint 5 — Effect size (Cohen's d)
        if re.search(r"cohen'?s?\s*d|effect\s*size|d\s*=", text_lower):
            elements_found["effect_size"] = True
            evidence.append("Effect size found")
        else:
            evidence.append("Effect size NOT found")

        # Checkpoint 6 — Plot interpretation
        if re.search(r'plot|graph|figure|chart|visual|descriptive', text_lower):
            elements_found["plot"] = True
            evidence.append("Plot reference found")
        else:
            evidence.append("Plot reference NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_cw8_4_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 8.4: Means Comparison Analysis.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 4,
                    "component_2_score": 3,
                    "component_3_score": 5,
                    "component_4_score": 4,
                },
                max_points=20,
                feedback="[TEST MODE] Method justification present but could be clearer. Table included but APA formatting incomplete. Inference correct. Effect size explained well.",
                vibe="Student demonstrates understanding but needs to improve presentation and formatting",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "task_description": True,
                            "method_justification": True,
                            "table": True,
                            "inference": True,
                            "effect_size": True,
                            "plot": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics assignment about means comparison analysis using a **STRICT rubric-based approach.

**TASK DESCRIPTION:**
Students must complete 4 components: (1) justify method based on assumptions, (2) present JASP table in APA format and make statistical inference, (3) provide and interpret Cohen's d effect size, (4) add and interpret descriptive plot.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Focus on statistical reasoning and proper interpretation
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

**RUBRIC:**

**Component 1: Method Justification Based on Assumptions (5 points):**

PREREQUISITE: Task description must be pasted in answer. If missing → 0/5.

If task description present, evaluate justification:
- 5/5: Clear justification based on TWO assumptions
- 4/5: Justification with only one assumption
- 3/5: Weak justification  
- 2/5: Minimal justification
- 0/5: No task description

**Component 2: Statistics Table in APA Style AND Statistical Inference (5 points):**
- 5/5: Table with JASP output in proper APA format (statistics, df, p-value) AND clear decision (reject/fail to reject) with correct reasoning
- 4/5: Table in APA format OR inference correct, but one element has minor issues
- 3/5: Both table and inference present but with significant problems
- 2/5: Only table OR only inference present
- 0/5: Neither table nor inference provided
- CRITICAL: Must include BOTH APA-formatted table AND explicit reject/fail to reject decision
- CRITICAL: Decision must be consistent with p-value and significance level

**Component 3: Cohen's d Effect Size and Interpretation (5 points):**
- 5/5: Cohen's d value provided AND meaningful interpretation (small/medium/large effect with practical significance)
- 4/5: Cohen's d provided with basic interpretation but lacks depth
- 3/5: Cohen's d value stated but interpretation missing or unclear
- 2/5: Effect size mentioned but value not provided or interpretation wrong
- 0/5: No effect size discussion
- CRITICAL: Must provide the actual Cohen's d value
- CRITICAL: Must explain what the value means in context (not just "large effect" but what that implies)

**Component 4: Descriptive Plot and Interpretation (5 points):**
- 5/5: Plot included or referenced AND interpreted (describes pattern, differences, trends visible in the plot)
- 4/5: Plot referenced with basic interpretation but lacks detail
- 3/5: Plot mentioned but interpretation minimal
- 2/5: Plot present but no interpretation
- 0/5: No plot or reference to plot
- CRITICAL: Must describe what the plot shows about the data
- CRITICAL: Interpretation should connect to the research question

STUDENT ANSWER:
{student_answer}

Return grading in this exact JSON format:
{{
  "component_1_score": <0-5>,
  "component_1_explanation": "<brief explanation>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<brief explanation>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief explanation>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief explanation>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment>",
  "vibe": "<one-sentence overall impression>"
}}"""

        element_check = self.check_required_elements(student_answer)

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "element_check": element_check
            }
        )

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
        """Display grading results."""
        import textwrap
        print("=" * 60)
        print("GRADING RESULTS - CLASSWORK 8.4")
        print("Means Comparison - Justification / Table+Inference / Effect Size / Plot")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Task Description + Method Justification): {grading.get('component_1_score', 'N/A')}/5")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Table APA + Inference): {grading.get('component_2_score', 'N/A')}/5")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Cohen's d Effect Size): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Descriptive Plot): {grading.get('component_4_score', 'N/A')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

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
    evaluator = CW8_4Evaluator()
    from config import InputHandler

    input_handler = InputHandler()
    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 8.4",
        question_description="Means Comparison - Method Justification / JASP Table / Inference / Effect Size / Plot",
        min_length=30
    )
    if student_answer:
        grading = evaluator.grade_cw8_4_answer(student_answer)
        evaluator.print_grading_results(grading)