"""
question7_5_evaluator.py
Hypothesis Testing - Output Description / Effect Size / Gender Context / Cultural Context
"""
import re

from config import BaseEvaluator

class Question7_5Evaluator(BaseEvaluator):
    """
        Evaluator for Question 7_5: Gender and Cultural Context Analysis.

        Evaluates student's ability to describe statistical output, calculate
        and interpret effect size, and interpret findings in gender and cultural contexts.

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
            "output_description": False,
            "effect_size": False,
            "gender_context": False,
            "cultural_context": False
        }

        evidence = []

        # Checkpoint 1 — Output description
        if re.search(r'mean|median|p[\s-]?value|statistic|result|output', text_lower) and \
                re.search(r'significant|differ|test|wilcoxon|t[\s-]?test', text_lower):
            elements_found["output_description"] = True
            evidence.append("Output description found")
        else:
            evidence.append("Output description NOT found")

        # Checkpoint 2 — Effect size (strict)
        if re.search(r'effect\s*size|cohen|rank[\s-]?biserial|d\s*=|r\s*=', text_lower) and \
                re.search(r'small|medium|large|negligible|practical', text_lower):
            elements_found["effect_size"] = True
            evidence.append("Effect size calculation and interpretation found")
        else:
            evidence.append("Effect size NOT found")

        # Checkpoint 3 — Gender context
        if re.search(r'gender|men|women|male|female', text_lower) and \
                re.search(r'differ|context|finding|interpret|score', text_lower):
            elements_found["gender_context"] = True
            evidence.append("Gender context found")
        else:
            evidence.append("Gender context NOT found")

        # Checkpoint 4 — Cultural context
        if re.search(r'cultur|country|nation|background|societ', text_lower) and \
                re.search(r'differ|context|finding|interpret|score', text_lower):
            elements_found["cultural_context"] = True
            evidence.append("Cultural context found")
        else:
            evidence.append("Cultural context NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_question7_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 7.5: Output Description / Effect Size / Gender and Cultural Context.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 4,
                    "component_2_score": 0,
                    "component_3a_score": 3,
                    "component_3b_score": 3,
                },
                max_points=20,
                feedback="[TEST MODE] Output described well. Effect size missing. Gender and cultural contexts partially addressed.",
                vibe="Student shows partial understanding; effect size calculation and interpretation are missing",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "output_description": True,
                            "effect_size": False,
                            "gender_context": True,
                            "cultural_context": True
                        },
                        "all_present": False,
                        "evidence": ["Test mode - partial elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics assignment using a **HYBRID approach** - vibe-based holistic grading with ONE strict component.

**TASK DESCRIPTION:**
Students must complete 4 components for gender and cultural context analysis.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Components 1, 3a, 3b use VIBE approach - holistic, generous, focus on understanding
3. Component 2 ONLY uses STRICT approach - effect size must be present to earn points
4. Feedback should be SHORT, written as a teacher's comment
5. Feedback CANNOT be an invitation for further discussion

**RUBRIC:**

Component 1: Output Description [VIBE] (5 points)
- Focus on whether student presents statistical findings clearly
- Include key statistics (means, test results, p-values)
- Be generous - focus on substance over format

Component 2: Effect Size [STRICT] (5 points)
- 0/5: No effect size calculation AND no interpretation
- 1-2/5: Only calculation OR only interpretation (not both)
- 3-4/5: Both present but could be stronger
- 5/5: Clear calculation AND meaningful interpretation of magnitude
- CRITICAL: Both calculation AND interpretation required for full credit

Component 3a: Gender Context [VIBE] (5 points)
- Does student discuss what findings mean for gender differences?
- Is interpretation thoughtful and goes beyond surface level?
- Be generous - reward genuine understanding

Component 3b: Cultural Context [VIBE] (5 points)
- Does student discuss what findings mean for cultural differences?
- Is interpretation thoughtful and goes beyond surface level?
- Be generous - reward genuine understanding

STUDENT ANSWER:
{student_answer}

Return grading in this exact JSON format:
{{
  "component_1_score": <0-5>,
  "component_1_explanation": "<brief explanation>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<brief explanation>",
  "component_3a_score": <0-5>,
  "component_3a_explanation": "<brief explanation>",
  "component_3b_score": <0-5>,
  "component_3b_explanation": "<brief explanation>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
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
                "component_3a_score",
                "component_3b_score"
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results."""
        import textwrap
        print("=" * 60)
        print("GRADING RESULTS - QUESTION 7.5")
        print("Output Description / Effect Size / Gender Context / Cultural Context")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Output Description): {grading.get('component_1_score', 'N/A')}/5")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Effect Size): {grading.get('component_2_score', 'N/A')}/5")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3a (Gender Context): {grading.get('component_3a_score', 'N/A')}/5")
            if grading.get('component_3a_explanation'):
                print(f"    → {grading.get('component_3a_explanation')}")

            print(f"  Component 3b (Cultural Context): {grading.get('component_3b_score', 'N/A')}/5")
            if grading.get('component_3b_explanation'):
                print(f"    → {grading.get('component_3b_explanation')}")

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
    evaluator = Question7_5Evaluator()
    from config import InputHandler
    input_handler = InputHandler()
    student_answer = input_handler.collect_and_validate_input(
        question_name="QUESTION 7.5",
        question_description="Output Description / Effect Size / Gender Context / Cultural Context",
        min_length=10
    )
    if student_answer:
        grading = evaluator.grade_question7_5_answer(student_answer)
        evaluator.print_grading_results(grading)