"""
cw13_1.py
Classwork 13: Linear Regression
Evaluation method name: def grade_question_cw13_1_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter

class CW13_1Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 13_1.

    Task: State the problem with your own words (5 points) and formulate Research question (5 points).
    What is a predictor? What is criterion (outcome) variable? (5 points)
    For Linear Regression in JASP tab, which variable is Dependent? Which one is Predictor
    (independent Variable)? (5 points).
        """

    def __init__(self):
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1200
        )
        self.formatter = OutputFormatter(default_width=60)

    def check_required_elements(self, student_answer: str) -> dict:
        text_lower = student_answer.lower()
        first_lines = student_answer[:200]

        elements_found = {
            "name": False,
            "title": False,
            "task_description": False,
            "no_autoformatting": True,
        }

        evidence = []

        #STEP 1 - Name (strict)
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

        # STEP 2 - Title (strict)
        title_patterns = [
            r'^\s*classwork\s*13',
            r'^\s*cw\s*13\b',
            r'^\s*class\s*work\s*(week\s*)?13',
            r'^\s*in.?class\s*13'
        ]
        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["title"] = True
                evidence.append("Title found")
                break
        if not elements_found["title"]:
                evidence.append("Title NOT found")

        # STEP 3 - Task Description (strict)
        pedagogical_markers = [
            "what is a predictor?",
            "which variable is dependent?",
            "formulate research question",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Step 4 - Autoformatting (no bullet points, no excessive bold/headers)    evidence.append("Task description NOT found") // TODO: Restore
        autoformat_patterns = [
            r'(?m)(?:^\s*\d+[\.\)]\s+\S.*\n){2,}',
            r'^\s*[-•*]\s+\S',
        ]

        for pattern in autoformat_patterns:
            if re.search(pattern, student_answer, re.MULTILINE):
                elements_found["no_autoformatting"] = False
                evidence.append("Autoformatting detected")
                break

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def grade_question_cw13_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question13_1: Problem Statement, Research Question, Predictor and Criterion Definitions, JASP Variable Assignment.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text

        """
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 4,
                    "component_1_name_score": 1,
                    "component_1_title_score": 1,
                    "component_1_task_score": 1,
                    "component_1_autoformat_score": 1,
                    "component_2_score": 4,
                    "component_3_score": 4,
                    "component_4_score": 4,
                    "component_5_score": 4,
                },
                max_points=20,
                feedback="[TEST MODE] Excellent understanding",
                vibe="Student shows partial understanding; key elements missing in problem statement",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "name": False,
                            "paper_title": False,
                            "task_description": False,
                            "no_autoformatting": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )


        prompt = f"""You are grading a statistics classwork assignment.

**TASK DESCRIPTION:**

- State the problem with your own words (5 points) 
- Formulate Research question (5 points).
- What is a predictor? What is criterion (outcome) variable? (5 points)
- For Linear Regression in JASP tab, which variable is Dependent? Which one is Predictor (independent Variable)? (5 points).

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Reasoning is required; no calculations are necessary
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

---

**RUBRIC**

**Component 1: Formatting (4 points total)**
- Student name present: 1 point
- Paper title present (e.g., "Classwork 12"): 1 point
- Task description present: 1 point
- No autoformatting: 1 point

**Component 2: Problem Statement (4 points)**
Should describe the research problem in their own words, connected to the context of linear regression.

- 4 points: Clear, specific, well-articulated problem in own words
- 3 points: Problem present but vague or lacks context
- 2 points: Problem poorly articulated but shows some understanding
- 1 point: Attempted but unclear or off-topic
- 0 points: Completely blank

**Component 3: Research Question (4 points)**
Student must formulate a clear, testable Research Question appropriate for linear regression analysis.

- 4 points: Clear, testable question directly addressing the problem
- 3 points: Question present but vague or partially addresses problem
- 2 points: Question unclear or poorly formulated
- 1 point: Attempted but not testable or irrelevant
- 0 points: Completely blank

**Component 4: Predictor and Criterion Variable Definitions (4 points)**
Student must correctly define both the predictor (independent) variable and the criterion (outcome) variable.

- 4 points: Both defined correctly with clear explanation of their roles in regression
- 3 points: One defined correctly, other vague or missing
- 2 points: Both attempted but definitions unclear or partially wrong
- 1 point: Minimal attempt
- 0 points: Completely blank

Accept: "predictor predicts the outcome", "criterion is what we are trying to predict",
"independent variable", "dependent variable", "outcome variable".
Do NOT accept definitions that confuse predictor with criterion.

**Component 5: JASP Variable Assignment (4 points)**
Student must correctly identify which variable goes in the Dependent box and which goes in the Predictor box in the JASP Linear Regression tab.

- 4 points: Correctly states criterion/outcome = Dependent, predictor/independent = Predictor (Covariates), with clear reasoning
- 3 points: One assignment correct, other missing or wrong
- 2 points: Both attempted but with confusion between the two
- 1 point: Minimal attempt
- 0 points: Completely blank

Accept: "the criterion variable goes into the Dependent box", "the predictor goes into Covariates or Predictor box".
Do NOT accept reversed assignments.

---

EXAMPLE OF A COMPLETE ANSWER

Problem Statement:
This study investigates whether a predictor variable can significantly explain variance in a criterion (outcome) variable using linear regression. The goal is to determine the direction and strength of the linear relationship between the two variables.

Research Question:
Does the predictor variable significantly predict the criterion variable in a linear regression model?

Predictor and Criterion Definitions:
The predictor (independent) variable is the variable used to predict or explain changes in another variable. The criterion (outcome) variable is the dependent variable — the one we are trying to predict or explain.

JASP Variable Assignment:
In the JASP Linear Regression tab, the criterion (outcome) variable is placed in the Dependent box, and the predictor (independent) variable is placed in the Covariates (Predictor) box.

---
ORIGINALITY CHECK:

IMPORTANT:
Students are required to copy the following task description into their answer.
This exact text is NEVER an originality concern and must be fully excluded before evaluation:

--- TASK DESCRIPTION START ---
State the problem with your own words (5 points) and formulate Research question (5 points).
What is a predictor? What is criterion (outcome) variable? (5 points)
For Linear Regression in JASP tab, which variable is Dependent? Which one is Predictor (independent Variable)? (5 points).
--- TASK DESCRIPTION END ---

STEP 1: Remove any text matching or paraphrasing the block above.
STEP 2: Evaluate ONLY what remains — the student's own problem statement, research question, definitions, and JASP variable assignment.
STEP 3: Set originality_concern = true ONLY if the remaining text is AI-generated, generic, and contains no personal reasoning connected to the task.

Otherwise set originality_concern = false.

DO NOT modify or override component scores based on originality_concern.

STUDENT ANSWER:
{student_answer}

Return grading in this exact JSON format:
{{
  "originality_concern": <true/false>,
  "formatting_deductions": <0-4>,
  "formatting_name_deduction": <0-1>,
  "formatting_title_deduction": <0-1>,
  "formatting_task_deduction": <0-1>,
  "formatting_autoformat_deduction": <0-1>,
  "formatting_explanation": "<brief explanation for deductions>",
  "component_1_score": <0-4>,
  "component_1_explanation": "<brief explanation for problem statement>",
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief explanation for research question>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief explanation for predictor and criterion definitions>",
  "component_4_score": <0-4>,
  "component_4_explanation": "<brief explanation for JASP variable assignment>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression>"
}}

"""
        # Check for required elements
        element_check = self.check_required_elements(student_answer)
        
        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "formatting_check": element_check
            }
        )

        # If grading succeeded, validate component scores
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
            "component_1_score": "Task Setup (Name/Title/Task/Formatting)",
            "component_2_score": "Problem Statement",
            "component_3_score": "Research Question",
            "component_4_score": "Predictor and Criterion Definitions",
            "component_5_score": "JASP Variable Assignment",
        }

        component_types = {
            "component_1_score": "HYBRID",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
            "component_4_score": "HYBRID",
            "component_5_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 4,
            "component_2_score": 4,
            "component_3_score": 4,
            "component_4_score": 4,
            "component_5_score": 4,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="CW13_1",
            question_description="Linear Regression - Problem, RQ, Variables",
            component_labels=component_labels,
            max_score=4,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )
