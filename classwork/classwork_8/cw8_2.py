"""
cw8_2.py
Classwork 8: Repeated Measures T-test
Normality Checking / Shapiro-Wilk / Table / Normality inference / Reasoning
Evaluation method name: def grade_cw8_2_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2

class CW8_2Evaluator (BaseEvaluator):
    """
    Evaluator for Normality Checking.
    Task 2. Which method did you apply to check normality? Name it. (5 points).
    Insert the table, introduce, number, and title it. (5 points).
    Provide a decision rule. Check the normality assumption with significance level  = 0.001. Make a conclusion: Is this distribution normal? (5 points)
    Provide your reasoning: how did you know? (5 points)

    Inherits common functionality from BaseEvaluator.
    """

    def __init__(self):
        """Initialize the evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1200
        )
        # Initialize output formatter
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
            "task_description": False,
            "normality_method": False,
            "normality_conclusion": False,
            "reasoning": False
        }

        evidence = []

        # Checkpoint 1 — Task description
        task_full_text = "Which method did you apply to check normality? Name it. (5 points). Insert the table, introduce, number, and title it. (5 points). Provide a decision rule. Check the normality assumption with significance level  = 0.001. Make a conclusion: Is this distribution normal? (5 points) Provide your reasoning: how did you know? (5 points)"

        if task_full_text.lower() in text_lower:
            elements_found["task_description"] = True
            evidence.append("Task description found")
        else:
            evidence.append("Task description NOT found")

        # Checkpoint 2 — Normality method (strict)
        if re.search(r'shapiro[\s-]?wilk|normality\s*test|s-w\s*test|kolmogorov|anderson', text_lower):
            elements_found["normality_method"] = True
            evidence.append("Normality method found")
        else:
            evidence.append("Normality method NOT found")

        # Checkpoint 3 — Normality conclusion (yes/no)
        if re.search(r'distribution\s*is\s*(not\s*)?normal|is\s*(not\s*)?normally\s*distributed|normal\s*distribution', text_lower):
            elements_found["normality_conclusion"] = True
            evidence.append("Normality conclusion found")
        else:
            evidence.append("Normality conclusion NOT found")

        # Checkpoint 4 — Reasoning with α
        if re.search(r'α\s*=\s*0\.001|alpha\s*=\s*0\.001|significance\s*level', text_lower) and \
                re.search(r'p[\s-]?value|p\s*[<>]=?\s*0\.', text_lower):
            elements_found["reasoning"] = True
            evidence.append("Reasoning with α found")
        else:
            evidence.append("Reasoning with α NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_cw8_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 8.2: Normality Check.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 2,
                    "component_2_score": 4,
                    "component_3_score": 5,
                    "component_4_score": 4,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Method not stated explicitly. Table present. No clear yes/no conclusion. Reasoning partially correct.",
                vibe="Student shows partial understanding; normality method and conclusion need improvement",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "task_description": True,
                            "normality_method": True,
                            "normality_conclusion": True,
                            "reasoning": True
                        },
                        "all_present": False,
                        "evidence": ["Test mode - partial elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["did you apply", "how did you know"]
        )

        prompt = f"""You are grading a statistics assignment about normality checking using a **STRICT rubric-based approach.

**TASK DESCRIPTION:**
Task 2. Which method did you apply to check normality? Name it. (5 points). Insert the table, introduce, number, and title it. (5 points). Provide a decision rule. Check the normality assumption with significance level  = 0.001. Make a conclusion: Is this distribution normal? (5 points) Provide your reasoning: how did you know? (5 points)

Total: 20 points

STUDENT ANSWER:
{student_answer}

**IMPORTANT NOTES:**
- Students submit text descriptions of their work since visual elements (actual diagrams, screenshots, formatted documents) cannot be captured in text
- If student REFERENCES or DESCRIBES the required elements (e.g., "I used APA format to describe findings", "I inserted the frequency distribution diagram"), ASSUME they completed it in their actual document
- DO NOT penalize for "missing" visual elements if they clearly describe what they did

**IMPORTANT GRADING RULES:**
1. Total score MUST be exactly 20 points
2. Reasoning is required; calculations are mandatory
3. Feedback should be SHORT, written as a teacher's comment
4. Feedback CANNOT be an invitation for further discussion
5. Award partial credit where reasoning is mostly correct but incomplete
6. It is expected to see both student's logic and calculations, not only the final answer
7. Explanations must be SPECIFIC and ACTIONABLE - avoid vague phrases like "lacks depth", "could be better", "needs improvement". Instead, point to what is actually missing or what was done well.

**HYBRID GRADING APPROACH:**

**AUTOMATIC FORMATTING DETECTION RESULT:**
Task description correctly formatted (1 point if True): {formatting_check['elements_found']['task_description']}
Proper autoformatting and structure (1 point if True): {formatting_check['elements_found']['autoformatting']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC DETECTION:**
{element_check['elements_found']}  

**RUBRIC:**

**Component 1: Formatting (2 points):**
Use AUTOMATIC FORMATTING DETECTION RESULT above.
- 1 point: Task description correctly formatted
- 1 point: Proper autoformatting and structure

**Component 2: Method Name (4 points):**
- 4 points: Method name explicitly stated in a sentence (e.g., "I used the Shapiro-Wilk test")
- 0 points: Method name only in table header, or not mentioned at all
- CRITICAL: Must explicitly state the method name in text, not just in a table

**Component 3: Table 1 (5 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Table itself with numerical data present
- 1 point: Introductory phrase present before the table
- 1 point: Reference to table number in introductory phrase
- 1 point: Standalone table number present
- 1 point: Descriptive table title present
- CRITICAL: A label above the table such as "Test of Normality (Shapiro-Wilk)" counts as a title
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Inference (4 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Decision rule stated
- 1 point: Obtained p-value reported
- 1 point: Correct α = 0.001 used
- 1 point: Clear normality statement (yes/no conclusion)

**Component 5: Explanation (5 points):**
- 5 points: Reasoning correct and complete (proper comparison of p-value with α = 0.001, correct conclusion)
- 3 points: Reasoning mostly correct but incomplete
- 1 point: Student attempts to explain but reasoning is incorrect
- 0 points: No explanation provided
- CRITICAL: Evaluate reasoning and conclusion INDEPENDENTLY
- CRITICAL: If student correctly applies decision rule but final conclusion contradicts it, deduct 1 point for wrong conclusion only
- CRITICAL: If student incorrectly applies decision rule (e.g. p > α → not normal), deduct points for wrong reasoning regardless of conclusion

**CORRECT ANSWER REFERENCE:**
The normality assumption was checked using the Shapiro–Wilk test. 
The Table 1 presents Shapiro-Wilk test in JASP for given variable

Table 1
Test of Normality (Shapiro-Wilk) for given variables
 	 	 	W	p
Moon	-	Other	0.913	.148
The decision rule is to reject the null hypothesis of normality only if p < α.
Here, the significance level is α=0.001, and the obtained value is p=0.002. Since p > α, we fail to reject the null hypothesis of normality. Therefore, the distribution is considered normal at the α=0.001 significance level because there is no sufficient

**FEEDBACK RULES**
- Identify which components were completed correctly
- Point out missing or incomplete elements explicitly
- Maintain supportive tone

Return JSON only:
{{
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief>",
  "component_2_score": <0-4>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-4>,
  "component_4_explanation": "<brief>",
  "component_5_score": <0-5>,
  "component_5_explanation": "<brief>",
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative feedback>",
  "vibe": "<one-sentence overall impression>"
}}"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "element_check": element_check,
                "formatting_check": formatting_check,
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
        """
        Display grading results using OutputFormatter.

        Args:
            grading: Grading result dictionary
        """
        # Define component labels
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Method Name",
            "component_3_score": "Table 1",
            "component_4_score": "Inference",
            "component_5_score": "Explanation",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT",
            "component_5_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 4,
            "component_3_score": 5,
            "component_4_score": 4,
            "component_5_score": 5,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 8_2",
            question_description="Normality Check - Shapiro-Wilk / Table / Inference / Explanation",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )
