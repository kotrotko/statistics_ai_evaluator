"""
fin_v1_2.py
Final Exam Variant 1
Hypothesis Testing — Method Selection and Hypotheses
Evaluation method name: def grade_question_fin_v1_2_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter

class FIN_V1_2Evaluator(BaseEvaluator, ):
    """
    Evaluator for Final Exam Variant 2, Task 2.

    Task: The student suggested that anxiety among those forced to study online
    (due to changing country) was, on average, higher than among classroom students.
    Which statistical method will you choose? (4 pts) Why? (4 pts)
    One-tailed or two-tailed? (4 pts) Why? (4 pts)
    State null and alternative hypotheses explicitly. (4 pts)

    Formatting: task description (1 point) + no autoformatting (1 point)
    Total: 20 points (strictly).
    """

    def __init__(self):
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1200
        )
        self.formatter = OutputFormatter(default_width=60)

    def check_formatting_elements(self, student_answer: str) -> dict:
        text_lower = student_answer.lower()

        elements_found = {
            "task_description": False,
            "no_autoformatting": True,
        }

        evidence = []

        # Key phrases that would only appear if the student copied the task description
        pedagogical_markers = [
            "will you choose",
            "why",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        autoformat_patterns = [
            r'(?m)(?:^\s*\d+[\.\)]\s+\S.*\n){2,}',
            r'^\s*[-•*]\s+\S',
        ]

        for pattern in autoformat_patterns:
            if re.search(pattern, student_answer, re.MULTILINE):
                elements_found["no_autoformatting"] = False
                evidence.append("Autoformatting detected")
                break

        if elements_found["no_autoformatting"]:
            evidence.append("No autoformatting found")

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def check_required_elements(self, student_answer: str) -> dict:
        text_lower = student_answer.lower()

        elements_found = {
            "hypotheses_h0": False,
            "hypotheses_h1": False,
            "hypotheses_h0_math": False,
            "hypotheses_h1_math": False,
        }

        evidence = []

        # H0 and H1 — tracked individually
        if re.search(r'h0\s*:|h₀\s*:', text_lower):
            elements_found["hypotheses_h0"] = True
            evidence.append("Found H0")
        if re.search(r'h1\s*:|ha\s*:|h₁\s*:', text_lower):
            elements_found["hypotheses_h1"] = True
            evidence.append("Found H1/Ha")

        # H0 math: μ and = near H0 label, no inequality
        h0_match = re.search(r'h0\s*:([^\n]{0,60})', student_answer, re.IGNORECASE)
        if h0_match and re.search(r'μ', h0_match.group(1)) and re.search(r'=', h0_match.group(1)) \
                and not re.search(r'[><!≠]', h0_match.group(1)):
            elements_found["hypotheses_h0_math"] = True
            evidence.append("Found H0 math expression")
        else:
            evidence.append("H0 math expression NOT found")

        # H1 math: μ and > near H1/Ha label
        h1_match = re.search(r'(?:h1|ha|h₁)\s*:([^\n]{0,60})', student_answer, re.IGNORECASE)
        if h1_match and re.search(r'μ', h1_match.group(1)) and re.search(r'>', h1_match.group(1)):
            elements_found["hypotheses_h1_math"] = True
            evidence.append("Found H1 math expression")
        else:
            evidence.append("H1 math expression NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_question_fin_v1_2_answer(self, student_answer: str, test_mode: bool = False):

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_2_score": 4,
                    "component_3_score": 5,
                    "component_4_score": 5,
                    "component_5_score": 4,
                },
                max_points=20,
                feedback="[TEST MODE] Good answer with correct method, justification, direction, and hypotheses.",
                vibe="Student demonstrates solid understanding of hypothesis testing with independent samples",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "task_description": True,
                            "no_autoformatting": True,
                        },
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        formatting_check = self.check_formatting_elements(student_answer)
        element_check = self.check_required_elements(student_answer)
        es = element_check["elements_found"]

        prompt = f"""You are grading a statistics final exam paper.

TASK: The student suggested that the level of anxiety among those who were forced
to study online due to changing country was, on average, higher than among those
who continued to study in the classroom.
Questions asked:
1. Which statistical method will you choose to test this research hypothesis? (4 points)
2. Why? (4 points)
3. Will you choose a one-tailed or two-tailed test? (4 points)
4. Why? (4 points)
5. State the null and alternative hypotheses explicitly. (4 points)

Use STRICT rubric-based grading. Total score MUST be exactly 20 points.

ELEMENT DETECTION RESULTS (USE AS FACTS):
hypotheses_h0_math_present = {es["hypotheses_h0_math"]}
hypotheses_h1_math_present = {es["hypotheses_h1_math"]}

---

**RUBRIC**

**Component 1: Formatting (2 points)**
Start with 2 points.

Step 1 Task description (1 point)
Use task_description_present.

Step 2 No autoformatting (1 point)
Use no_autoformatting_present.

**Component 2: Statistical Method (4 points)**
Student must name the correct statistical test.

- 4 points: Correctly names independent-samples t-test (also acceptable: independent t-test,
  two-sample t-test, Student's t-test for independent groups)
- 2 points: Names "t-test" without specifying independent samples (partially correct)
- 0 points: Wrong method (e.g., paired t-test, ANOVA, chi-square) or absent

Component 3: Method Justification (5 points)
Student must explain WHY the independent-samples t-test is appropriate.

- 5 points: Explains both (a) comparing means of two groups AND (b) groups are independent
  (i.e., different students, no overlap between online and classroom groups)
- 3 points: Mentions two groups and independence, but one explanation is weak or vague
- 2 points: Mentions only one of the two required elements (either groups or independence)
- 1 point: Vague reference to comparing groups without clear reasoning
- 0 points: Absent or incorrect

Component 4: Direction Choice and Justification (5 points)
Student must state one-tailed test AND explain why.

- 5 points: States one-tailed AND explains that the hypothesis is directional — specifically
  predicts that online group has HIGHER anxiety than classroom group
- 4 points: Explicitly states one-tailed test but justification is vague or incomplete
- 2 points: Implies directionality without naming one-tailed
- 0 points: States two-tailed, or absent

Component 5: Hypotheses (4 points total)
Two sub-components: H0 and H1, each worth 2 points.

Sub-component 5a: Null hypothesis H0 (2 points)
- component_5a_statement_score = 1 if H0 stated correctly in words
  (no difference in mean anxiety, or online group does NOT have higher anxiety).
  component_5a_statement_score = 0 if absent or incorrect.
- component_5a_math_score: use hypotheses_h0_math_present fact. Do not evaluate yourself.
- component_5a_score = component_5a_statement_score + component_5a_math_score

Sub-component 5b: Alternative hypothesis H1 (2 points)
- component_5b_statement_score = 1 if H1 stated correctly in words
  (online group has higher mean anxiety than classroom group).
  component_5b_statement_score = 0 if absent or incorrect.
- component_5b_math_score: use hypotheses_h1_math_present fact. Do not evaluate yourself.
- component_5b_score = component_5b_statement_score + component_5b_math_score
---

EXAMPLE OF A COMPLETE ANSWER

Task 2. The student suggested that the level of anxiety among those who were forced to study online due changing a country, was, on average, higher than those who continued to study in the classroom. Which statistical method will you choose to test this research hypotheses? (4 points) Why? (4 points) Will you choose a one-tailed or two-tailed test? (4 points) Why? (4 points) State the null and alternative hypotheses explicitly (4 points).
A suitable statistical method for testing this hypothesis would be the independent-samples t-test (also called the independent t-test).
The independent-samples t-test is appropriate because the study compares the mean level of anxiety between two independent groups: (1) students who were forced to study online due to changing country; (2) students who continued classroom-based study. 
A one-tailed test should be chosen because the research hypothesis is directional. The student specifically predicts that anxiety among students studying online after changing country is higher than among students continuing classroom learning. Therefore, the analysis tests for an increase in one specific direction rather than for any difference in general.
The hypotheses can be stated as follows:
Null hypothesis (H₀):
There is no difference in mean anxiety levels between the two groups, or the online group does not have higher anxiety.
H0:μonline = μclassroom
Alternative hypothesis (H₁):
Students who were forced to study online due to changing country have a higher mean level of anxiety than students who continued classroom study.
H1:μonline > μclassroom

---

ORIGINALITY CHECK:

IMPORTANT:
Students are required to copy the following task description into their answer.
This exact text is NEVER an originality concern and must be fully excluded before evaluation:

--- TASK DESCRIPTION START ---
The student suggested that the level of anxiety among those who were forced to study online
due changing a country, was, on average, higher than those who continued to study in the
classroom. Which statistical method will you choose to test this research hypotheses? Why?
Will you choose a one-tailed or two-tailed test? Why? State the null and alternative
hypotheses explicitly.
--- TASK DESCRIPTION END ---

STEP 1: Remove any text matching or paraphrasing the block above.
STEP 2: Evaluate ONLY what remains.
STEP 3: Set originality_concern = true ONLY if the remaining text is AI-generated or generic,
with no personal reasoning connected to the specific context of this problem.

Otherwise set originality_concern = false.

DO NOT modify or override component scores based on originality_concern.

STUDENT ANSWER:
{student_answer}

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<brief>",
  "component_5_score": <0-4>,
  "component_5a_score": <0-2>,
  "component_5a_statement_score": <0-1>,
  "component_5a_math_score": <0-1>,
  "component_5b_score": <0-2>,
  "component_5b_statement_score": <0-1>,
  "component_5b_math_score": <0-1>,
  "component_5_explanation": "<brief>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression>"
}}

SCORING INSTRUCTIONS:

component_1_task_score = 1 if task_description_present else 0
component_1_autoformat_score = 1 if no_autoformatting_present else 0
component_1_score = component_1_task_score + component_1_autoformat_score

component_5a_math_score = 1 if hypotheses_h0_math_present else 0
component_5a_score = component_5a_statement_score + component_5a_math_score
component_5b_math_score = 1 if hypotheses_h1_math_present else 0
component_5b_score = component_5b_statement_score + component_5b_math_score
component_5_score = component_5a_score + component_5b_score

total_points = component_1_score + component_2_score + component_3_score +
               component_4_score + component_5_score
"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"formatting_check": formatting_check,
                               "element_check": element_check,
            }
        )

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
        """Display grading results using OutputFormatter.

        Args:
            grading: Grading result dictionary
        """
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Statistical Method",
            "component_3_score": "Method Justification",
            "component_4_score": "Direction Choice and Justification",
            "component_5_score": "Hypotheses (H0 + H1)",
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT",
            "component_5_score": "STRICT",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 4,
            "component_3_score": 5,
            "component_4_score": 5,
            "component_5_score": 4,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="FIN_V1_2",
            question_description="Hypothesis Testing — Method Selection and Hypotheses",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="STRICT"
        )