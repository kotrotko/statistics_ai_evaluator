"""
question7_1_evaluator.py
Hypothesis Testing - Problem Statement, Research Question, Hypotheses, α/df/CV
"""
import re

from config import BaseEvaluator

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
        first_lines = student_answer[:200]

        elements_found = {
            "name": False,
            "title": False,
            "variant": False,
            "task_description": False,
            "problem_statement": False,
            "research_question": False,
            "hypotheses": False,
            "alpha_df_cv": False
        }

        evidence = []

        # STEP 1 — Name (strict)
        name_patterns = [
            r'name\s*:\s*\w+',
            r'student\s*:\s*\w+',
            r'by\s*:\s*\w+',
            r'^\s*[A-Z][a-z]+\s+[A-Z][a-z]+',
        ]
        for pattern in name_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["name"] = True
                evidence.append("Name found")
                break
        if not elements_found["name"]:
            evidence.append("Name NOT found")

        # STEP 2 — Title (strict)
        if re.search(r'question\s*7[\._]?1', text_lower) or re.search(r'hypothesis\s*testing', text_lower):
            elements_found["title"] = True
            evidence.append("Title found")
        else:
            evidence.append("Title NOT found")

        # STEP 3 — Variant (strict)
        if re.search(r'variant\s*\d+|v\s*\d+\b', text_lower):
            elements_found["variant"] = True
            evidence.append("Variant found")
        else:
            evidence.append("Variant NOT found")

        # STEP 4 — Task description (strict)
        if re.search(r'task|assignment|instructions?|dataset|problem\s*description', text_lower):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Research question
        if re.search(r'\?', student_answer) and re.search(r'(research\s*question|question\s*:)', text_lower):
            elements_found["research_question"] = True
            evidence.append("Found research question with question mark")

        # Hypotheses
        if re.search(r'h0\s*:', text_lower) and re.search(r'h1\s*:|ha\s*:', text_lower):
            elements_found["hypotheses"] = True
            evidence.append("Found both H0 and H1/Ha")

            # Alpha, df, CV
        alpha_found = bool(re.search(r'\bα\b|\balpha\b|\ba\s*=', text_lower))
        df_found = bool(re.search(r'\bdf\b|\bdegrees\s*of\s*freedom\b', text_lower))
        cv_found = bool(re.search(r'\bcv\b|\bcritical\s*value\b', text_lower))
        if alpha_found and df_found and cv_found:
            elements_found["alpha_df_cv"] = True
            evidence.append("Found α, df, and CV indicators")
        elif df_found:
            evidence.append("Found df but missing α or CV")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
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

    Component 1: Header + Problem Statement (5 points)
    Start at 5 points. Deduct 1 for each missing element below.
    
    STEP 1 - Name [STRICT]: Use elements_found["name"].
    - If False: deduct 1 point. Add to explanation: "Name is missing. -1 point."
    
    STEP 2 - Title [STRICT]: Use elements_found["title"].
    - If False: deduct 1 point. Add to explanation: "Title is missing. -1 point."
    
    STEP 3 - Variant [STRICT]: Use elements_found["variant"].
    - If False: deduct 1 point. Add to explanation: "Variant indicator is missing. -1 point."
    
    STEP 4 - Task Description [STRICT]: Use elements_found["task_description"].
    - If False: deduct 1 point. Add to explanation: "Task description is missing. -1 point."
    
    STEP 5 - Problem Statement [VIBE]: Read the student's problem statement carefully.
    Award 1 point ONLY if BOTH conditions are true:
    - It is present
    - It is properly formulated as a research problem (answers: what is a problem? or: what do we not know? or: what is the gap?)
    If it is missing, or present but does not describe a problem or research gap: 0 points.
    Add to explanation: "Problem statement is missing or not properly formulated. -1 point."

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
        """Display grading results"""
        import textwrap
        print("=" * 60)
        print("GRADING RESULTS - QUESTION 7.1")
        print("Hypothesis Testing - Problem Statement / RQ / Hypotheses / α df CV")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Name + Title + Variant + Task + Problem Statement): {grading.get('component_1_score', 'N/A')}/5")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Research Question): {grading.get('component_2_score', 'N/A')}/5")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Hypotheses H₀ and H₁): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (α, df, and CV): {grading.get('component_4_score', 'N/A')}/5")
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