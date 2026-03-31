# hw10_5.py
# One-Way ANOVA - Training Methods Effectiveness
# Evaluation method name: def grade_hw10_5_answer(...)

import re
import textwrap
from config import BaseEvaluator


class HW10_5Evaluator(BaseEvaluator):
    """
    Evaluator for One-Way ANOVA Training Methods HW10.5.

    Task: You are in charge of assessing different training methods for effectiveness.
    You have data on 4 methods: Method 1 (X̅ = 87, n = 12), Method 2 (X̅ = 92, n = 14),
    Method 3 (X̅ = 88, n = 15), and Method 4 (X̅ = 75, n = 11). Test for differences
    among these means, assuming SSB = 64.81 and SST = 399.45.

    Evaluates student's ability to conduct ANOVA hypothesis testing.
    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    def __init__(self):
        super().__init__(model="llama-3.3-70b-versatile", temperature=0.3, max_tokens=1500)

    def check_formatting_elements(self, student_answer: str) -> dict:
        """
        Check if required structural and content elements are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()
        elements_found = {"task_description": False, "no_autoformatting": True}
        evidence = []

        # Task patterns for HW10.5
        task_patterns = [
            r"method 1.*87",
            r"method 2.*92",
            r"method 3.*88",
            r"method 4.*75",
            r"ssb.*64.81",
            r"sst.*399.45",
            r"training method",
        ]
        if any(re.search(pattern, text_lower) for pattern in task_patterns):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Autoformatting patterns (same as hw10_4)
        autoformat_patterns = [
            r"^\d+\..*\d+\.$",  # only 2 consecutive numbered lines
            r"^- .*,?$",  # bullet list -,
        ]
        for pattern in autoformat_patterns:
            if re.search(pattern, student_answer, re.MULTILINE):
                elements_found["no_autoformatting"] = False
                evidence.append("Autoformatting detected")
                break
        if elements_found["no_autoformatting"]:
            evidence.append("No autoformatting found")

        return elements_found, evidence if evidence else ["No clear formatting indicators found"]

    def grade_hw10_5_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 10.5: ANOVA hypothesis testing for training methods effectiveness.

        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API

        Returns:
            Detailed grading breakdown dictionary
        """
        if test_mode:
            return self.create_mock_result({
                "component1_score": 2,
                "component1_taskscore": 1,
                "component1_autoformatscore": 1,
                "component2_score": 5,
                "component3_score": 6,
                "component4_score": 7,
            }, max_points=20,
                feedback="TEST MODE: All formatting elements present. ANOVA calculations correct with strong hypothesis testing.",
                vibe="Student demonstrates solid understanding of ANOVA with minor issues.")

        formatting_check = self.check_formatting_elements(student_answer)
        formatting_summary = formatting_check["elements_found"]


        formatting_block = f"""HEADER DETECTION RESULTS (DO NOT RE-EVALUATE, USE AS FACTS):
task_description_present: {formatting_summary['task_description']}
no_autoformatting_present: {formatting_summary['no_autoformatting']}
You MUST deduct points in Component 1 strictly according to these values.
If task_description_present False, you MUST deduct 1 point.
If no_autoformatting_present False, you MUST deduct 1 point."""

        prompt = f"""{formatting_block}

You are grading a statistics assignment where a student must:
"You are in charge of assessing different training methods for effectiveness. You have data on 4 methods: Method 1 (X̅ = 87, n = 12), Method 2 (X̅ = 92, n = 14), Method 3 (X̅ = 88, n = 15), and Method 4 (X̅ = 75, n = 11). Test for differences among these means, assuming SSB = 64.81 and SST = 399.45."

Use a STRICT rubric-based approach. Total score MUST be exactly 20 points.

IMPORTANT GRADING RULES:
1. Total score MUST be exactly 20 points
2. 0 only if completely blank
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. For low-scoring answers, use encouraging language "Credit for trying, but..."

---
RUBRIC

Component 1: Header Structural Integrity (2 points)
Start at 2 points. Deduct 1 point for each missing element
STEP 1 - Task Description (STRICT): Use task_description_present. If False deduct 1 point. Add "Task description is missing. -1 point."
STEP 2 - No autoformatting (STRICT): Use no_autoformatting_present. If False deduct 1 point. Add "Autoformatting detected. -1 point."

---
Component 2: ANOVA Calculations (6 points)
The student must calculate df, MS, and F-statistic.

GIVEN DATA:
- k = 4 methods (Method 1,2,3,4)
- Sample sizes: n1=12, n2=14, n3=15, n4=11
- N total = 12+14+15+11 = 52
- Means: 87, 92, 88, 75
- SSB = 64.81
- SST = 399.45
- SSW = SST - SSB = 399.45 - 64.81 = 334.64 (students may compute)

CORRECT CALCULATIONS:
1. df_between = k - 1 = 3
2. df_within = N - k = 48
3. df_total = N - 1 = 51
4. MSB = SSB / df_between = 64.81 / 3 = 21.6033 (21.60)
5. MSW = SSW / df_within = 334.64 / 48 ≈ 6.972 (6.97)
6. F = MSB / MSW ≈ 21.6033 / 6.972 ≈ 3.10 (accept 3.09-3.11)

EVALUATION STEPS:
STEP 1: Degrees of freedom correct? (1.5 points)
- Full: df_between=3 AND df_within=48
- Partial 1 pt: One correct
- Partial 0.5 pt: Both attempted but errors
- None: Missing/wrong

STEP 2: Mean Squares correct? (2.5 points)
- Full 2.5 pts: MSB≈21.60 AND MSW≈6.97
- Partial 2 pts: Both with minor rounding
- Partial 1.5 pts: One correct
- Partial 1 pt: Both attempted errors
- Partial 0.5 pt: Minimal
- None: Missing/wrong

STEP 3: F-statistic correct? (2 points)
- Full 2 pts: F≈3.10 (3.09-3.11)
- Partial 1.5 pts: Close 3.05-3.15
- Partial 1 pt: Attempted error
- Partial 0.5 pt: Minimal
- None: Missing/wrong

Scoring Guide:
- 6: All correct
- 5: Major values correct, minor rounding
- 4: Most correct, one error
- 3: Several correct, major errors
- 2: Attempted, multiple errors
- 1: Minimal
- 0: No/wrong

---
Component 3: 4-Step Hypothesis Testing - Steps 1 & 2 (6 points)
STEP 1: State the Hypotheses (3 points)
Null H0: All population means equal / No difference in training effectiveness across methods
Alt H1/Ha: At least one differs / Not all means equal / Difference among methods
- 3 pts: Both correct format
- 2 pts: Minor notation
- 1 pt: Attempted unclear
- 0: Missing/wrong

STEP 2: Significance Level & Critical Value (3 points)
Alpha=0.05 (assume standard), df1=3, df2=48, F_crit(3,48,0.05)≈2.80 (accept 2.79-2.81)
- 3 pts: Alpha, df correct, F_crit≈2.80
- 2 pts: Alpha+df correct, crit off
- 1 pt: Some present
- 0: Missing/wrong

Scoring:
- 6: All correct
- 5: Minor crit issue
- 4: Hypo correct, crit issue
- 3: Attempted incomplete
- 2: Major issues
- 1: Minimal
- 0: Missing

---
Component 4: 4-Step Hypothesis Testing - Steps 3 & 4 (6 points)
STEP 3: Test Statistic (2 points) F≈3.10 (from Comp 2)
- 2 pts: Correct
- 1 pt: Error
- 0: Missing/wrong

STEP 4: Decision & Interpret (4 points)
Decision: F=3.10 > 2.80, reject H0
Interpret: Significant difference in effectiveness among training methods / At least one method differs
Decision (2 pts):
- 2: Reject with reasoning
- 1: Correct weak reason
- 0: Wrong/no
Interpret (2 pts):
- 2: Clear context (methods, effectiveness)
- 1: Attempted lack clarity
- 0: No/wrong

Scoring:
- 6: All correct clear
- 5: Correct, clearer interpret
- 4: Decision correct, weak interpret
- 3: Some correct
- 2: Major errors
- 1: Minimal
- 0: Missing

---
COMMON MISTAKES:
1. N=52 (12+14+15+11)
2. SSW=SST-SSB=334.64
3. df_within=48
4. F=MSB/MSW
5. Ha: "at least one differs"
6. F_crit≈2.80 for df(3,48)
7. Reject since 3.10>2.80
8. Interpret re: training methods effectiveness

FEEDBACK EXAMPLES:
- df error: "N=52, df_within=48."
- Wrong hypo: "Ha: at least one mean differs."
- Wrong decision: "F=3.10 > 2.80, reject H0."
- Missing interpret: "Interpret re: training methods."

---
ORIGINALITY CHECK:
Signs: textbook-perfect, no voice, polished structure.
- If concern: all components=0, originality_concern=true, feedback="Due to originality concern, your points are frozen. You can get them back if you provide oral explanation for this paper."
- If original: false, proceed.

STUDENT ANSWER: {student_answer}

SCORING INSTRUCTIONS FOR SUB-SCORES:
- component1_taskscore: use task_description_present (1 if True, 0 False)
- component1_autoformatscore: use no_autoformatting_present (1 if True, 0 False)

Return grading in this exact JSON format:
{{
    "originality_concern": true/false,
    "component1_score": 0-2,
    "component1_taskscore": 0-1,
    "component1_autoformatscore": 0-1,
    "component1_explanation": "brief explanation for header",
    "component2_score": 0-6,
    "component2_explanation": "brief explanation for ANOVA calculations",
    "component3_score": 0-6,
    "component3_explanation": "brief explanation for Steps 1&2",
    "component4_score": 0-6,
    "component4_explanation": "brief explanation for Steps 3&4",
    "total_points": 0-20,
    "max_points": 20,
    "percentage": percentage as number,
    "feedback": "SHORT teacher's comment, not invitation",
    "vibe": "one-sentence overall impression of student's ANOVA understanding"
}}"""

        result = self.grade_with_prompt(student_answer, prompt, additional_checks=formatting_check)
        if "error" not in result:
            component_keys = ["component1_score", "component2_score", "component3_score", "component4_score"]
            result = self.validate_component_scores(result, component_keys, 20)
        return result

    def print_grading_results(self, grading):
        """Display grading results."""
        print("=" * 60)
        print("GRADING RESULTS - HW10.5")
        print("ANOVA Training Methods Effectiveness")
        print("=" * 60)

        if "component1_score" in grading:
            if grading.get("originality_concern"):
                print("ORIGINALITY CONCERN DETECTED")
                print("All points frozen. See feedback below.")
            print("BREAKDOWN:")
            print(f"Component 1 (Header): {grading.get('component1_score', 'N/A')}/2")
            print(f"  Task description: {grading.get('component1_taskscore', 'N/A')}/1 (regex)")
            print(f"  No autoformatting: {grading.get('component1_autoformatscore', 'N/A')}/1 (regex)")
            if grading.get("component1_explanation"):
                print(f"  {grading['component1_explanation']}")
            print(f"Component 2 (ANOVA Calculations): {grading.get('component2_score', 'N/A')}/6")
            if grading.get("component2_explanation"):
                print(f"  {grading['component2_explanation']}")
            print(f"Component 3 (Hypotheses/Test Setup): {grading.get('component3_score', 'N/A')}/6")
            if grading.get("component3_explanation"):
                print(f"  {grading['component3_explanation']}")
            print(f"Component 4 (Test Statistic/Decision): {grading.get('component4_score', 'N/A')}/6")
            if grading.get("component4_explanation"):
                print(f"  {grading['component4_explanation']}")
            print("-" * 40)
            print(f"SCORE: {grading.get('total_points', 'N/A')}/{grading.get('max_points', 20)} (20)")
            print(f"PERCENTAGE: {grading.get('percentage', 'N/A')}")
            print("=" * 60)
            print("FEEDBACK")
            print("=" * 60)
            print(textwrap.fill(grading.get("feedback", "No feedback available."), width=60))
            print("=" * 60)
            print("THE VIBE")
            print("=" * 60)
            print(textwrap.fill(grading.get("vibe", "N/A"), width=60))
        elif "error" in grading:
            print("=" * 60)
            print("ERROR")
            print("=" * 60)
            print(grading.get("error"))
        if "raw_response" in grading:
            print("Response")
            print(grading["raw_response"][:500])


if __name__ == "__main__":
    print("Welcome to the Homework AI Evaluator System!")
    print("=" * 60)
    evaluator = HW10_5Evaluator()
    print("HOMEWORK 10.5 EVALUATOR")
    print("ANOVA Training Methods")
    print("=" * 60)
    print("Enter the student's answer to HOMEWORK 10.5.")
    print("Press Enter twice when finished, or type END on a new line.")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    if len(lines) >= 2 and lines[-1] == "" and lines[-2] == "":
        lines = lines[:-2]  # Remove the two empty lines

    student_answer = "\n".join(lines)

    if not student_answer.strip():
        print("Error: No answer provided. Exiting.")
        exit(1)

    print("=" * 60)
    print("EVALUATING...")
    print("=" * 60)

    grading = evaluator.grade_hw10_5_answer(student_answer)

    evaluator.print_grading_results(grading)