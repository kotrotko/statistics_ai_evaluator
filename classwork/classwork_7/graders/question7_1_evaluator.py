"""
question7_1_evaluator.py
Hypothesis Testing - Problem Statement, Research Question, Hypotheses, α/df/CV
"""
import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter

class Question7_1Evaluator(BaseEvaluator):
    """
     Evaluator for Question 7_1: Hypothesis Testing Setup.

     Evaluates student's ability to write a problem statement,
     research question, hypotheses, and identify α, df, and CV.

     Inherits common functionality from BaseEvaluator.
     Contains only question-specific logic.
     """

    def __init__(self):
        """Initialize the evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=2500
        )
        self.formatter = OutputFormatter(default_width=60)

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
            "has_problem_statement": False,
            "has_research_question": False,
            "has_hypotheses": False,
            "has_alpha_df_cv": False
        }

        evidence = []

        if re.search(r'problem\s*statement', text_lower):
            elements_found["has_problem_statement"] = True
            evidence.append("Found problem statement indicator")

        if re.search(r'\?', student_answer) and re.search(r'(research\s*question|question\s*:)', text_lower):
            elements_found["has_research_question"] = True
            evidence.append("Found research question with question mark")

        if re.search(r'h0\s*:', text_lower) and re.search(r'h1\s*:|ha\s*:', text_lower):
            elements_found["has_hypotheses"] = True
            evidence.append("Found both H0 and H1/Ha")

        alpha_found = bool(re.search(r'\bα\b|\balpha\b|\ba\s*=', text_lower))
        df_found = bool(re.search(r'\bdf\b|\bdegrees\s*of\s*freedom\b', text_lower))
        cv_found = bool(re.search(r'\bcv\b|\bcritical\s*value\b', text_lower))
        if alpha_found and df_found and cv_found:
            elements_found["has_alpha_df_cv"] = True
            evidence.append("Found α, df, and CV indicators")
        elif df_found:
            evidence.append("Found df but missing α or CV")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_question7_1_answer(self, student_answer: str, test_mode: bool = False):
            """
            Grade Question7_1: Hypothesis Testing Setup.
            Returns detailed grading breakdown.

            Args:
                student_answer: The student's response text
                test_mode: If True, returns mock data without calling API
            """

            if test_mode:
                return self.create_mock_result(
                    component_scores={
                        "component_1_score": 0,
                        "component_2_score": 5,
                        "component_3_score": 5,
                        "component_4_score": 2,
                    },
                    max_points=20,
                    feedback="[TEST MODE] Problem statement is a conclusion. Hypotheses acceptable. Missing α and CV.",
                    vibe="Student shows partial understanding; key elements missing in problem statement and CV",
                    additional_data={
                        "element_check": {
                            "elements_found": {
                                "has_problem_statement": False,
                                "has_research_question": True,
                                "has_hypotheses": True,
                                "has_alpha_df_cv": False
                            },
                            "all_present": False,
                            "evidence": ["Test mode - partial elements present"]
                        }
                    }
                )

            prompt = f"""You are grading a statistics hypothesis testing assignment using a **STRICT rubric-based approach**.

    **TASK DESCRIPTION:**
    Students must complete 4 checkpoints for a one-sample t-test hypothesis testing setup.

    **IMPORTANT GRADING RULES:**
    1. Total score MUST be exactly 20 points
    2. Focus on conceptual understanding over formatting
    3. Ignore minor symbol errors (e.g., = instead of ≠ is a typing issue, not a conceptual error)
    4. Feedback should be SHORT, written as a teacher's comment
    5. Feedback CANNOT be an invitation for further discussion
    6. Award partial credit where reasoning is mostly correct but incomplete

    **RUBRIC:**

    Component 1: Problem Statement (5 points)
    - Describes what is being investigated (not a conclusion): required
    - Mentions context (test, comparing groups): 1 point
    - Cites source of reference values: 1 point
    - Writing a CONCLUSION instead of a problem = 0/5 (full deduction)

    Component 2: Research Question (5 points)
    - Phrased as a clear question with question mark: required
    - Specifies what is being compared/tested: 1 point
    - Minor grammar errors acceptable if meaning is clear
    - Be lenient: understandable question = 4-5 points

    Component 3: Hypotheses (5 points)
    - Both H₀ and H₁/Ha present: required
    - Must be in mathematical form (e.g., H₀: μ = 65): required
    - IGNORE = vs ≠ symbol errors — treat as typing issue, no deduction
    - Both present in math form = full 5 points

    Component 4: α, df, CV (5 points)
    - States significance level α: 1 point
    - Calculates degrees of freedom df correctly: 1 point
    - Provides actual CV value as a NUMBER: 2 points (just saying "found by table" = 0)
    - Justifies test choice (one-tailed vs two-tailed): 1 point

    **TYPICAL MISTAKES AND PENALTIES:**
    - Conclusion instead of problem statement: −5 points (0/5) from Component 1
    - Missing CV number: −2 points from Component 4
    - Missing α: −1 point from Component 4
    - Symbol errors (= vs ≠): ignore, no deduction

    STUDENT ANSWER:
    {{student_answer}}

    Return grading in this exact JSON format:
    {{
      "component_1_score": <0-5>,
      "component_1_explanation": "<brief explanation for problem statement>",
      "component_2_score": <0-5>,
      "component_2_explanation": "<brief explanation for research question>",
      "component_3_score": <0-5>,
      "component_3_explanation": "<brief explanation for hypotheses>",
      "component_4_score": <0-5>,
      "component_4_explanation": "<brief explanation for α/df/CV>",
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
        component_labels = {
            "component_1_score": "Problem Statement",
            "component_2_score": "Research Question",
            "component_3_score": "Hypotheses (H₀ and H₁)",
            "component_4_score": "α, df, and CV"
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT"
        }

        max_scores = {
            "component_1_score": 3,
            "component_2_score": 17,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 7.1",
            question_description="Hypothesis Testing - Problem Statement / RQ / Hypotheses / α df CV",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="STRICT"
        )


if __name__ == "__main__":
    evaluator = Question7_1Evaluator()

    aiden_submission = """
My problem statement: The sample of scores by GulzhigitBek differs from test value of 65

Main research question: Is the mean differs from score of 65 of GulzhigitBek?

Hypothesis:
Null hypothesis and alternative hypothesis:
H0: m= 65, H1: m=-65

Sample size n=17, therefore df = 16(it can be checked through Jasp also, but i just do it like n-1=16).
    """

    print("EVALUATING AIDEN'S SUBMISSION:")
    print("(Expected score: 12/20)")
    print("-" * 80)

    grading = evaluator.grade_question7_1_answer(aiden_submission)
    evaluator.print_grading_results(grading)

    print("\n" + "=" * 80)
    print("INSTRUCTOR'S ACTUAL SCORE: 12/20")
    print("Breakdown:")
    print("- Problem Statement: 0/5 (wrote conclusion, not problem)")
    print("- Research Question: 5/5 (acceptable)")
    print("- Hypotheses: 5/5 (has both in math form, = vs ≠ ignored)")
    print("- α, df, CV: 2/5 (df correct, but missing α and CV)")
    print("=" * 80)