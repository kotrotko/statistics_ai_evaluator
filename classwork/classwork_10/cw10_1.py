"""
cw10_1.py
Classwork 10: One-Way ANOVA
Evaluation method name: def grade_cw10_1_answer
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter


class CW10_1Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 10_1.

    Task:
    What is the role of the 'Participant' variable? (5 points)
    Should it be included in your analysis? Why? (5 points)
    State the problem with your own words (5 points)
    Formulate the main Research question (5 points)

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
        first_lines = student_answer[:200]

        elements_found = {
            "name": False,
            "paper_title": False,
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
        if re.search(r'question\s*10[\._]?1', text_lower) or re.search(r'hypothesis\s*testing', text_lower):
            elements_found["title"] = True
            evidence.append("Title found")
        else:
            evidence.append("Title NOT found")

        # STEP 3 — Task Description (strict)
        if re.search(r'task|assignment|instructions?|dataset|problem\s*description', text_lower):
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # STEP 4 — Autoformatting (no bullet points, no excessive bold/headers)
        autoformat_violations = len(re.findall(r'^\s*[-•*]\s', student_answer, re.MULTILINE))
        bold_violations = len(re.findall(r'\*\*|__', student_answer))
        if autoformat_violations <= 2 and bold_violations <= 2:
            elements_found["autoformatting"] = True
            evidence.append("No excessive autoformatting detected")
        else:
            evidence.append(
                f"Autoformatting detected: {autoformat_violations} bullets, {bold_violations} bold markers")

        # Participant variable role
        if re.search(r'(participant|variable|role\s*of|identifier)', text_lower):
            elements_found["participant_role"] = True
            evidence.append("Found participant variable role")

        # Should it be included
        if re.search(r'(should\s*not|not\s*be\s*included|exclude|label|meaningless)', text_lower):
            elements_found["inclusion_decision"] = True
            evidence.append("Found inclusion decision")

        # Problem statement
        if re.search(r'personality|facebook\s*friends|social\s*media|characteristic', text_lower) and re.search(
                r'(problem\s*statement|state\s*the\s*problem|problem\s*:)', text_lower):
            elements_found["problem_statement"] = True
            evidence.append("Found problem statement")

        # Research question
        if re.search(r'\?', student_answer) and re.search(r'(research\s*question|question\s*:)', text_lower):
            elements_found["research_question"] = True
            evidence.append("Found research question with question mark")

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def grade_question_cw10_1_answer(self, student_answer: str, test_mode: bool = False):
        """
         Grade Question10_1: Hypothesis Testing Setup.
         Returns detailed grading breakdown.

         Args:
             student_answer: The student's response text
             test_mode: If True, returns mock data without calling API
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
                    "element_check": {
                        "elements_found": {
                            "name": False,
                            "title": False,
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

• What is the role of the 'Participant' variable? (5 points)  
• Should it be included in your analysis? Why? (5 points)  
• State the problem with your own words (5 points)  
• Formulate the main Research question (5 points)

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Reasoning is required; no calculations are necessary
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion

**RUBRIC**

Component 1: Formatting (4 points)
- Student name present: 1 point
- Paper title present (e.g., "Classwork 10"): 1 point
- Task is copied correctly from assignment: 1 point
- No autoformatting: 1 point

Component 2: Role of Participant Variable (4 points)
The 'Participant' variable is an identifier/ID variable that uniquely identifies each subject in the study.
- 4 points: Correctly identifies as ID/identifier variable with clear explanation
- 3 points: Partially correct (e.g., mentions uniqueness but lacks precision)
- 2 points: Shows some understanding but confused or incomplete
- 1 point: Attempted but mostly incorrect
- 0 points: Completely blank

Component 3: Should It Be Included & Why (4 points)
The Participant variable should NOT be included in the analysis because:
- It's an identifier, not a variable of interest
- It doesn't contain meaningful data for statistical analysis
- Including ID variables can cause errors or meaningless results

- 4 points: Correctly states NO with clear, logical reasoning
- 3 points: Correct answer but weak or incomplete reasoning
- 2 points: Incorrect answer OR correct answer with illogical reasoning
- 1 point: Attempted but mostly wrong
- 0 points: Completely blank

Component 4: Problem Statement (4 points)s
- 4 points: Clear, specific, well-articulated problem in own words
- 3 points: Problem present but vague or lacks context
- 2 points: Problem poorly articulated but shows some understanding
- 1 point: Attempted but unclear or off-topic
- 0 points: Completely blank

Component 5: Research Question (4 points)
Should formulate a testable question about the relationship between groups/conditions and number of Facebook friends.
- 4 points: Clear, testable question directly addressing the problem
- 3 points: Question present but vague or partially addresses problem
- 2 points: Question unclear or poorly formulated
- 1 point: Attempted but not testable or irrelevant
- 0 points: Completely blank

---

EXAMPLE OF A COMPLETE ANSWER

Role of Participant Variable:
The 'Participant' variable is an identifier variable that assigns a unique number to each participant in the study. It serves to distinguish between different subjects.

Should It Be Included:
No, the Participant variable should not be included in the analysis. It is merely an ID number and does not contain any meaningful data about the participants' characteristics or outcomes. Including it would be inappropriate as it's not a variable of theoretical or practical interest.

Problem Statement:
This study examines whether there is a relationship between personality characteristics and the number of Facebook friends people have. Researchers want to understand if different personality types are associated with different levels of social media connectivity.

Research Question:
Is there a significant difference in the number of Facebook friends across different personality characteristic groups?

---

**ORIGINALITY CHECK:**
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
            "component_1_score": "Task Setup (Name/Title?Task/Formatting)",
            "component_2_score": "Participant Variable Role",
            "component_3_score": "Should Be Included & Why",
            "component_4_score": "Problem Statement",
            "component_5_score": "Research Question"
        }

        component_types = {
            "component_1_score": "HYBRID",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
            "component_4_score": "HYBRID",
            "component_5_score": "HYBRID"
        }

        # Define max scores for each component
        max_scores = {
            "component_1_score": 4,
            "component_2_score": 4,
            "component_3_score": 4,
            "component_4_score": 4,
            "component_5_score": 4
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="CW10_1",
            question_description="One-Way ANOVA - Facebook Friends Analysis",
            component_labels=component_labels,
            max_score=4,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )
