"""
cw12_1.py
Classwork 12: Spearman's Rho correlation
Evaluation method name: def grade_question_cw12_1_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter


class CW12_1Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 12_1.

    Task: In class, go to the video https://www.youtube.com/watch?v=o4kO7_2_2gw (Dr. E) at 3:15. You will calculate the Spearman’s ρ using file Spearman fictional data.csv from the same video or from ecourse. Use variables scale 10 – 15 only (inclusively, 6 variables).  State the problem with your own words (10 points). Formulate the main Research question (10 points).
    """

    def __init__(self):
        super().__init__()
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
        title_patterns = [
            r'^\s*classwork\s*12',
            r'^\s*cw\s*12\b',
            r'^\s*class\s*work\s*(week\s*)?12',
            r'^\s*in.?class\s*12'
        ]
        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE):
                elements_found["title"] = True
                evidence.append("Title found")
                break
        if not elements_found["title"]:
            evidence.append("Title NOT found")

        # STEP 3 — Task description (strict)

        if re.search(
                r'spearman|rank\s*correlation|scale[s]?\s*(10|ten)|research\s+question|state\s+the\s+problem|problem\s+statement',
                text_lower):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # STEP 4 — Autoformatting (no bullet points, no excessive bold/headers)
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

    def grade_question_cw12_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question CW12_1: Spearman's Rho - Problem Statement & Research Question.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
        """
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 4,
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
                            "title": False,
                            "task_description": False,
                            "no_autoformatting": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics classwork assignment.

You are grading a statistics classwork assignment.

**TASK DESCRIPTION:**

- State the problem with your own words (5 points)
- Formulate Research question (5 points)
- Visualize data with Plots > Scatter plot. Include your visualization as Figure 1. Introduce, number, and title it (5 points)
- Interpret it: is it linear? (5 points)

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
Should describe the correlation analysis context using file bpc.csv (scales 10–15, 6 variables representing a bipolar psychological construct for Emotional Stability/Neuroticism).

- 4 points: Clear, specific, well-articulated problem in own words
- 3 points: Problem present but vague or lacks context
- 2 points: Problem poorly articulated but shows some understanding
- 1 point: Attempted but unclear or off-topic
- 0 points: Completely blank

**Component 3: Research Question (4 points)**
Student must formulate a clear, testable Research Question for the Spearman's rho analysis.

- 4 points: Clear, testable question directly addressing the problem
- 3 points: Question present but vague or partially addresses problem
- 2 points: Question unclear or poorly formulated
- 1 point: Attempted but not testable or irrelevant
- 0 points: Completely blank

**Component 3: Research Question (4 points)**
Should formulate a testable question about the relationships among the six Emotional Stability/Neuroticism scales (10–15).

- 4 points: Clear, testable question directly addressing the problem
- 3 points: Question present but vague or partially addresses problem
- 2 points: Question unclear or poorly formulated
- 1 point: Attempted but not testable or irrelevant
- 0 points: Completely blank

**Component 4: Figure 1 - Scatter Plot (4 points)**
Should include a scatter plot of scales 10–15, properly introduced, numbered, and titled as Figure 1.

- 4 points: Visualization present, properly introduced, numbered, and titled as Figure 1
- 3 points: Visualization present but missing title or numbering
- 2 points: Visualization present but poorly introduced or labeled
- 1 point: Attempted but incomplete or missing figure
- 0 points: Completely blank

**Component 5: Linearity Interpretation (4 points)**
Should interpret the scatter plot and state whether the relationships between the six scales are linear.

- 4 points: Clear, correct interpretation of linearity with reference to the plot
- 3 points: Interpretation present but vague or lacking reference to the plot
- 2 points: Interpretation attempted but unclear or partially incorrect
- 1 point: Attempted but mostly incorrect or irrelevant
- 0 points: Completely blank

---

EXAMPLE OF A COMPLETE ANSWER

Problem Statement:
The problem is: We do not know whether scale10, scale11, scale12, scale13, scale14, and scale15 are related to one another, nor do we know the strength and direction of these relationships.

Research Question:
What is the direction, magnitude, and form of the relationships among scale10, scale11, scale12, scale13, scale14, and scale15?

Data Visualization:
The data visualization of the items in columns 10 through 15 is illustrated in Figure 1.
Figure 1. Data visualization

Linearity:
The relationships between variables are linear.

---
ORIGINALITY CHECK:

Before finalizing scores, assess whether the answer appears to be AI-generated or copied.
Signs include: textbook-perfect phrasing with no personal voice, unnaturally polished
structure, or language that reads like a Wikipedia/ChatGPT excerpt rather than a student explanation.
- If originality concern detected: set all component scores to 0, set originality_concern to true,
  and set feedback to EXACTLY: "Due to originality concern, your points are frozen. You can get them back if you provide oral explanation for this paper."
- If original student work: set originality_concern to false and proceed normally.

---

STUDENT ANSWER:
{student_answer}

Return grading in this exact JSON format:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-4>,
  "component_1_explanation": "<brief explanation for task setup>",
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief explanation>",
  "component_3_score": <0-4>,
  "component_3_explanation": "<brief explanation>",
  "component_4_score": <0-4>,
  "component_4_explanation": "<brief explanation>",
  "component_5_score": <0-4>,
  "component_5_explanation": "<brief explanation>",
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
                "element_check": element_check
            }
        )

        # If grading succeeded, validate component scores
        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score",
                "component_5_score"
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
            "component_4_score": "Visualization",
            "component_5_score": "Interpretation",                                 "component_3_score": "Research Question",
        }

        component_types = {
            "component_1_score": "HYBRID",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
            "component_4_score": "HYBRID",
            "component_5_score": "HYBRID",
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="CW12_1",
            question_description="Spearman's Rho - Problem Statement & Research Question",
            component_labels=component_labels,
            max_score=4,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )
