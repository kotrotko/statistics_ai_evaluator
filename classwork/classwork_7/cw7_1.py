"""
question7_1_evaluator.py
Hypothesis Testing - Problem Statement, Research Question, Hypotheses, α/df/CV
"""
import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter


class CW7_1Evaluator(BaseEvaluator):
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
            "title": False,
            "task_description": False,
            "autoformatting": False,
            "problem_statement": False,
            "research_question": False,
            "hypotheses_h0": False,
            "hypotheses_h1": False,
            "alpha": False,
            "df": False,
            "cv": False
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
            evidence.append(f"Autoformatting detected: {autoformat_violations} bullets, {bold_violations} bold markers")

        # Research question
        if re.search(r'\?', student_answer) and re.search(r'(research\s*question|question\s*:)', text_lower):
            elements_found["research_question"] = True
            evidence.append("Found research question with question mark")

        # Hypotheses — split H0 and H1 separately
        if re.search(r'h0\s*:', text_lower):
            elements_found["hypotheses_h0"] = True
            evidence.append("Found H0")
        if re.search(r'h1\s*:|ha\s*:', text_lower):
            elements_found["hypotheses_h1"] = True
            evidence.append("Found H1/Ha")

        # Alpha, df, CV — tracked individually
        if re.search(r'\bα\b|\balpha\b|\ba\s*=\s*0\.\d+', text_lower):
            elements_found["alpha"] = True
            evidence.append("Found α")
        if re.search(r'\bdf\b|\bdegrees\s*of\s*freedom\b', text_lower):
            elements_found["df"] = True
            evidence.append("Found df")
        if re.search(r'\bcv\b|\bcritical\s*value\b|t\s*=\s*[±\-]?\d+\.\d+', text_lower):
            elements_found["cv"] = True
            evidence.append("Found CV")

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
                    "component_1_score": 2,
                    "component_2_score": 3,
                    "component_3_score": 3,
                    "component_4_score": 2,
                    "component_5_score": 2,
                },
                max_points=20,
                feedback="[TEST MODE] Problem statement is a conclusion. Hypotheses acceptable. Missing α and CV.",
                vibe="Student shows partial understanding; key elements missing in problem statement and CV",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "name": False,
                            "title": False,
                            "task_description": False,
                            "autoformatting": True,
                            "problem_statement": False,
                            "research_question": True,
                            "hypotheses_h0": True,
                            "hypotheses_h1": True,
                            "alpha": False,
                            "df": True,
                            "cv": False
                        },
                        "evidence": ["Test mode - partial elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics classwork assignment using a **STRICT rubric-based approach**.

**TASK DESCRIPTION:**
Students must complete a one-sample t-test hypothesis testing setup with 5 sections worth 4 points each (total 20 points).

Total: 20 points.

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Focus on conceptual understanding over formatting
3. Ignore minor symbol errors (e.g., = instead of ≠ is a typing issue, not a conceptual error)
4. Feedback should be SHORT, written as a teacher's comment
5. Feedback CANNOT be an invitation for further discussion

**RUBRIC:**

Component 1: Formatting (4 points total)
- Student name present: 1 point
- Paper title present (e.g., "Classwork 7"): 1 point
- Task is copied correctly from assignment: 1 point
- No autoformatting: 1 point

Component 2: Problem Statement (4 points)
- Describes what is unknown or a research gap (not a conclusion): 4 points
- Present but weakly formulated: 2 points
- Missing or is a conclusion/finding: 0 points

Component 3: Research Question (4 points)
- Phrased as a clear question with question mark: required
- References the population mean or comparison value (e.g., 73): 2 points
- Minor grammar errors acceptable if meaning is clear: full credit
- Missing question mark or not a question: max 2 points

Component 4: Hypotheses (4 points — 2 per hypothesis)
Per hypothesis (H0 and H1/Ha), award:
- 1 point: correct statistical statement (direction, equality)
- 1 point: expressed in required form (math: μ = 73, or equivalent words)
- Ignore = vs ≠ symbol typos — treat as formatting, not conceptual error

Component 5: α, df, CV (4 points)
- States α (e.g., α = 0.05): 1 point
- Calculates df correctly (n−1): 1 point
- Provides CV as an actual number (e.g., ±2.131): 2 points
  - Saying "found from table" without a value = 0 points for CV

**CORRECT ANSWER REFERENCE:**
Problem: We do not know whether men's mean indoor gardening score differs from reference value 73.
Research Question: Do men score significantly different from 73 on the indoor gardening test?
H0: μ = 73 | H1: μ ≠ 73 (two-tailed)
α = 0.05, df = 15, CV = ±2.131

STUDENT ANSWER:
{student_answer}

Return grading in this exact JSON format:
{{
  "component_1_score": <0-4>,
  "component_1_explanation": "<brief explanation>",
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
            "component_1_score": "Formatting (Name/Title/Task/Autoformat)",
            "component_2_score": "Problem Statement",
            "component_3_score": "Research Question",
            "component_4_score": "Hypotheses H₀ and H₁",
            "component_5_score": "α, df, and CV"
        }

        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
            "component_4_score": "HYBRID",
            "component_5_score": "HYBRID"
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 7_1",
            question_description="Hypothesis Testing - Problem Statement, Research Question, Hypotheses, α/df/CV",
            component_labels=component_labels,
            max_score=4,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )