"""
cw8_3.py
Classwork 8: Repeated Measures
Hypothesis Testing - State Hypotheses / Significance Level / df / Critical Value
Evaluation method name: def grade_cw8_3_answer
"""

import re
from config import BaseEvaluator


class CW8_3Evaluator(BaseEvaluator):
    """
    Evaluator for Hypothesis Testing Setup (CW8_3).

    Task: State Hypotheses explicitly in needed form (in math form or not, one- or two-tailed test) (5 points),
    select a level of significance α (5 points), calculate df (5 points), find the CV (5 points).
    Total (strictly) 20 points.

    Evaluates student's ability to state null and alternative hypotheses, select significance level,
    calculate degrees of freedom with complete logic, and find critical value with proper source reference.

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
            "step_system": False,
            "hypotheses": False,
            "alpha": False,
            "df": False
        }

        evidence = []

        # Checkpoint 0 — Step System (critical for evaluation)
        if re.search(r'step\s*1|step\s*2|step\s*3|step\s*4', text_lower):
            elements_found["step_system"] = True
            evidence.append("Step system found")
        else:
            evidence.append("Step system NOT found (required format)")

        # Checkpoint 1 — Hypotheses (H0 and H1/Ha)
        if re.search(r'h[_0₀]|h[_1₁]|h[_a]|null\s*hypothesis|alternative\s*hypothesis', text_lower):
            elements_found["hypotheses"] = True
            evidence.append("Hypotheses found")
        else:
            evidence.append("Hypotheses NOT found")

        # Checkpoint 2 — Significance level (α)
        if re.search(r'α\s*=|alpha\s*=|significance\s*level', text_lower):
            elements_found["alpha"] = True
            evidence.append("Significance level found")
        else:
            evidence.append("Significance level NOT found")

        # Checkpoint 3 — Degrees of freedom with calculation
        if re.search(r'df\s*=|degrees?\s*of\s*freedom|d\.f\.', text_lower):
            # Check if calculation is shown (pattern like "n - 1" or "17 - 1 = 16")
            if re.search(r'\d+\s*[-−]\s*\d+\s*=\s*\d+|\d+\s*[-−]\s*\d+', text_lower):
                elements_found["df"] = True
                evidence.append("Degrees of freedom with calculation found")
            else:
                elements_found["df"] = True
                evidence.append("Degrees of freedom found but calculation may be missing")
        else:
            evidence.append("Degrees of freedom NOT found")

        # Checkpoint 4 — Critical value with source reference
        if re.search(
                r'critical\s*value|cv\s*=|c\.v\.|t[\s_]*critical|z[\s_]*critical|chi[\s_]*critical|f[\s_]*critical',
                text_lower):
            elements_found["critical_value"] = True
            evidence.append("Critical value found")
        else:
            evidence.append("Critical value NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_question_cw8_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 8.3: Hypothesis Testing Setup.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 4,
                    "component_2_score": 5,
                    "component_3_score": 3,
                    "component_4_score": 4,
                },
                max_points=20,
                feedback="[TEST MODE] Hypotheses mostly correct. Alpha stated. df calculation incomplete. CV found but source unclear.",
                vibe="Student understands basics but needs to show complete calculations and source references",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "step_system": True,
                            "hypotheses": True,
                            "alpha": True,
                            "df": True,
                            "critical_value": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics assignment about hypothesis testing setup using a **STRICT rubric-based approach.

**TASK DESCRIPTION:**
Students must complete 4 steps for hypothesis testing setup according to the Step System format (as described in document 6.2.3).

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Students MUST use explicit Step System format (Step 1, Step 2, Step 3, Step 4) — if not used, deduct 1 point from total and mention in feedback
3. Students MUST demonstrate complete understanding by providing logic and calculations, not only answers (see doc 0.6.1)
4. Feedback should be SHORT, written as a teacher's comment
5. Feedback CANNOT be an invitation for further discussion

**RUBRIC:**

**Component 1: State Hypotheses Explicitly (5 points):**
- 5/5: Both H₀ and H₁ (or Hₐ) explicitly stated in proper form (mathematical notation or clear verbal form), correctly identifies one-tailed or two-tailed test
- 4/5: Hypotheses stated but minor issue (e.g., unclear whether one- or two-tailed, or notation slightly imprecise)
- 3/5: Hypotheses present but incomplete (e.g., only H₀ stated, or direction unclear)
- 2/5: Hypotheses attempted but significantly incorrect
- 0/5: Hypotheses not stated or completely wrong
- CRITICAL: Must explicitly state BOTH null and alternative hypotheses
- CRITICAL: Must indicate test type (one-tailed or two-tailed)

**Component 2: Select Level of Significance (5 points):**
- 5/5: α explicitly stated with value (e.g., "α = 0.05" or "significance level = 0.01"), clearly presented as Step 2
- 3/5: α value mentioned but not explicitly labeled or unclear presentation
- 0/5: α not stated or no significance level mentioned
- CRITICAL: Must use explicit notation (α = [value])

**Component 3: Calculate Degrees of Freedom (5 points):**
- 5/5: df calculated correctly with complete formula and arithmetic shown (e.g., "df = n - 1 = 17 - 1 = 16")
- 4/5: df calculated with formula but arithmetic step missing (e.g., "df = n - 1 = 16" without showing 17 - 1)
- 3/5: df value correct but calculation/formula not shown, or minor error in logic
- 1/5: df attempted but calculation incorrect or incomplete
- 0/5: df not calculated or completely wrong
- CRITICAL: Must show COMPLETE arithmetic calculation (e.g., 17 - 1 = 16), not just the answer
- CRITICAL: Formula must be appropriate for the specific test type

**Component 4: Find the Critical Value (5 points):**
- 5/5: Critical value found correctly with source reference (e.g., "I found it in the t-table" or "I calculated it using Excel")
- 4/5: CV correct but source reference missing or vague
- 2/5: CV attempted but incorrect value or no source mentioned
- 0/5: CV not provided or completely wrong
- CRITICAL: Must include brief reference to source (table, Excel, calculator, software, etc.)
- CRITICAL: CV must match the test type (one-tailed vs two-tailed)

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
        print("GRADING RESULTS - CLASSWORK 8.3")
        print("Hypothesis Testing Setup - Hypotheses / α / df / CV")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Hypotheses): {grading.get('component_1_score', 'N/A')}/5")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Significance Level): {grading.get('component_2_score', 'N/A')}/5")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Degrees of Freedom): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Critical Value): {grading.get('component_4_score', 'N/A')}/5")
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
    evaluator = CW8_3Evaluator()
    from config import InputHandler

    input_handler = InputHandler()
    student_answer = input_handler.collect_and_validate_input(
        question_name="CLASSWORK 8.3",
        question_description="Hypothesis Testing Setup - State Hypotheses / Select α / Calculate df / Find CV",
        min_length=20
    )
    if student_answer:
        grading = evaluator.grade_cw8_3_answer(student_answer)
        evaluator.print_grading_results(grading)