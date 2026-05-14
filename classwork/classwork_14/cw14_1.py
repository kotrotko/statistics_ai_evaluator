"""
cw14_1.py
Classwork 14: Chi Square
Evaluation method name: def grade_question_cw14_1_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter

class CW14_1Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 14_1.

    Task: State the problem with your own words (10 points)
    and formulate Research question (10 points).
    Total (strictly) 20 points.

    Rubric:
    Formatting (4 points: name, title, task description, no autoformatting)
    Problem Statement (8 points)
    Research Question (8 points)
    Total (strictly) 20 points.
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
            "autoformatting": False,
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
            r'^\s*classwork\s*14',
            r'^\s*cw\s*14\b',
            r'^\s*class\s*work\s*(week\s*)?14',
            r'^\s*in.?class\s*14'
        ]

        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["title"] = True
                evidence.append("Title found")
                break
        
        # STEP 3 - Task Description (strict)
        pedagogical_markers = [
            "state the problem with your own words (10 points) and formulate research question",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Step 4 - Autoformatting (no bullet points, no bold/headers)
        autoformat_violations = len(re.findall(r'^\s*[-•*]\s', student_answer, re.MULTILINE))
        bold_violations = len(re.findall(r'\*\*|__', student_answer))
        if autoformat_violations <= 2 and bold_violations <= 2:
            elements_found["autoformatting"] = True
            evidence.append("No excessive autoformatting detected")
        else:
            evidence.append(
                f"Autoformatting detected: {autoformat_violations} bullets, {bold_violations} bold markers")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_question_cw14_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 14.1: Chi Square.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """
        # Test mode for verification without API
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 4,
                    "component_1_name_score": 1,
                    "component_1_title_score": 1,
                    "component_1_task_score": 1,
                    "component_1_autoformat_score": 1,
                    "component_2_score": 8,
                    "component_3_score": 8,
                },
                max_points=20,
                feedback="[TEST MODE] Complete and accurate answer.",
                vibe="Student demonstrates clear understanding of Chi Square problem formulation.",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "name": False,
                            "paper_title": False,
                            "task_description": False,
                            "autoformatting": False,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics classwork assignment.
                    
**TASK DESCRIPTION:**
- State the problem with student's own words 
- Formulate Research question

Total: 20 points.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Reasoning is required; no calculations are necessary
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

---

**RUBRIC**

**Component 1: Formatting (4 points total)**
- Student name present: 1 point
- Paper title present (e.g., "Classwork 14"): 1 point
- Task description present: 1 point
- No autoformatting: 1 point

**Component 2: Problem Statement (8 points)**
Should describe the research problem in their own words, connected to the context
of Chi Square analysis. The problem should reference the variables under investigation
(e.g. physical activity and fruit consumption) and the nature of the question
(association between categorical variables).

- 8 points: Clear, specific, well-articulated problem in own words, connected to Chi Square context
- 6 points: Good statement with minor clarity issues or missing variable context
- 4 points: Problem present but vague or lacks connection to the variables or method
- 2 points: Problem poorly articulated but shows some understanding
- 1 point: Attempted but unclear or off-topic
- 0 points: Completely blank

CRITICAL: Do NOT accept a problem statement that is a restatement of the research question.
CRITICAL: Do NOT accept AI-generated boilerplate without any connection to the specific variables.

**Component 3: Research Question (8 points)**
Should formulate a clear, testable Research Question appropriate for Chi Square
analysis — asking whether there is a significant association between two categorical variables.

- 8 points: Clear, testable question directly addressing the association between
  the two categorical variables (e.g. physical activity and fruit consumption)
- 4 points: Question present but vague or only partially addresses the association
- 2 points: Question unclear or poorly formulated
- 1 point: Attempted but not testable or irrelevant to Chi Square
- 0 points: Completely blank

CRITICAL: The question must be phrased in terms of association or independence between
categorical variables, not in terms of prediction or causation.
CRITICAL: Do NOT accept a research question that is simply copied from an AI tool
without adaptation to the student's own understanding.

---

STUDENT ANSWER:
{student_answer}

Return grading in this exact JSON format:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-4>,
  "formatting_name": <0-1>,
  "formatting_title": <0-1>,
  "formatting_task": <0-1>,
  "formatting_autoforma": <0-1>,
  "component_1_explanation": "<brief explanation for task setur>",
  "component_2_score": <0-8>,
  "component_2_explanation": "<brief explanation for problem statement>",
  "component_3_score": <0-8>,
  "component_3_explanation": "<brief explanation for research question>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression>"
}}
"""
        # Check for required elements
        element_check = self.check_required_elements(student_answer)
        
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                # "originality_check": originality_check,
                "element_check": element_check}
        )

        # If grading succeeded, validate component scores
        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """Display grading results using OutputFormatter.

        Args:
            grading: Grading result dictionary
        """
        component_labels = {
            "component_1_score": "Formatting (Name/Title/Task/Autoformatting)",
            "component_2_score": "Problem Statement",
            "component_3_score": "Research Question",
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
        }

        #  Define max scores for each component
        max_scores = {
            "component_1_score": 4,
            "component_2_score": 8,
            "component_3_score": 8,
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="CW14_1",
            question_description="Chi Square - Problem Statement & Research Question",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )
