"""
cw10_2.py
Classwork 10: One-Way ANOVA
Assumption checking: normality and variance homogeneity
Evaluation method name: def grade_question_cw10_2_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2

class CW10_2Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 10_2.

    Task 2. Name the visualization method used to check normality and include it to the introductory phrase with reference, number, and title it in APA style (5 points).
    Produce and include the corresponding graph and interpret it in terms of normality checking (5 points).
    Name the statistical test used to assess homogeneity of variances and include it to APA-style introductory phrase (5 points).
    Present the results in a table. What can you say about the variance homogeneity based on the output? (5 points).

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
            "normality_method": False,
            "figure_present": False,
            "homogeneity_method": False,
            "table_present": False,
            "homogeneity_conclusion": False,
        }

        evidence = []

        # Checkpoint 1 — Normality method (Q-Q Plot)
        if re.search(r'q[\s-]?q\s*plot|qq\s*plot|quantile[\s-]?quantile', text_lower):
            elements_found["normality_method"] = True
            evidence.append("Normality method found (Q-Q Plot)")
        else:
            evidence.append("Normality method NOT found")

        # Checkpoint 2 — Graph present
        if re.search(r'figure\s*\d|graph|plot|q[\s-]?q|histogram', text_lower):
            elements_found["graph_present"] = True
            evidence.append("Graph found")
        else:
            evidence.append("Graph NOT found")

        # Checkpoint 3 — Homogeneity method
        if re.search(r'levene|bartlett|variance\s*homogeneity|homogeneity\s*test|homoscedasticity', text_lower):
            elements_found["homogeneity_method"] = True
            evidence.append("Homogeneity method found")
        else:
            evidence.append("Homogeneity method NOT found")

        # Checkpoint 4 — Homogeneity conclusion
        if re.search(r'variance\s*(is|are)\s*(not\s*)?homogeneous|homogeneity\s*(is|are)\s*(not\s*)?satisfied|equal\s*variance', text_lower):
            elements_found["homogeneity_conclusion"] = True
            evidence.append("Homogeneity conclusion found")
        else:
            evidence.append("Homogeneity conclusion NOT found")

        # Checkpoint 5 — Table present
        if re.search(r'table\s*\d|p[\s-]?value|statistic|levene|bartlett', text_lower):
            elements_found["table_present"] = True
            evidence.append("Table found")
        else:
            evidence.append("Table NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_question_cw10_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 10.2: Assumption Checking - Normality and Variance Homogeneity.
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
                feedback="[TEST MODE] Normality check complete. Graph present with minor APA issues. Homogeneity conclusion clear. Table present.",
                vibe="Student shows solid understanding of assumption checking and APA formatting",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "task_description": True,
                            "normality_method": True,
                            "graph_present": True,
                            "homogeneity_method": True,
                            "homogeneity_conclusion": True,
                            "table_present": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - partial elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["what can you say"]
        )

        prompt = f"""You are grading a statistics assignment about normality and variance homogeneity checking using a **STRICT rubric-based approach.

**TASK DESCRIPTION:**
Task 2. Name the visualization method used to check normality and include it to the introductory phrase with reference, number, and title it in APA style (5 points).  Produce and include the corresponding graph and interpret it in terms of normality checking (5 points). Name the statistical test used to assess homogeneity of variances and include it to APA-style introductory phrase (5 points). Present the results in a table. What can you say about the variance homogeneity based on the output? (5 points).

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

**Component 2: Q-Q Plot Name (4 points):**
- 4 points: Method name explicitly stated in a sentence (e.g., "I used a Q-Q Plot to check normality")
- 0 points: Method name only in figure caption or table header, or not mentioned at all
- CRITICAL: Must explicitly state the method name in text, not just in a figure or caption

**Component 3: Figure 1 (5 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Figure itself present and referenced
- 1 point: Introductory phrase present before the figure
- 1 point: Reference to figure number in introductory phrase
- 1 point: Standalone figure number present (e.g., "Figure 1")
- 1 point: Descriptive figure title present
- CRITICAL: A label such as "Q-Q Plot of Residuals" counts as a title
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Levene's Name & Table (4 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Homogeneity method explicitly named (e.g., "Levene's test")
- 1 point: Introductory phrase present before the table
- 1 point: Reference to table number in introductory phrase
- 1 point: Standalone table number present (e.g., "Table 1")
- CRITICAL: Must explicitly state the method name in text, not just in a table header

**Component 5: Conclusion on Homogeneity (5 points):**
Use AUTOMATIC DETECTION above.
- 2 points: Decision rule stated
- 1 point: Numeric values of α and p reported
- 1 point: Statistical inference stated (e.g., "since p > α, we fail to reject...")
- 1 point: Clear conclusion on homogeneity (e.g., "variances are homogeneous" or "variances are not equal")
- CRITICAL: Must explicitly state whether variances are homogeneous or not
- CRITICAL: Conclusion must be based on comparison of p-value with α

**CORRECT ANSWER REFERENCE:**
Normality. We check normality using Q-Q Plot. According the plot (see Figure 1), our distribution looks normal.
Figure 1
Q-Q Plot for given variable 
 
Variance homogeneity. We check variance homogeneity using Levene’s test. The Table 1 presents Levene’s test for given variable
Table 1
Test for Equality of Variances for given variable 
F	df1	df2	p
2.607	4.000	129.0	.039

The decision rule is to reject the null hypothesis of variance homogeneity only if p < α.
Here, the significance level is α=0.05, and the obtained value is p=0.039. Since p < α, we reject the null hypothesis of variance homogeneity. Therefore, the variance is considered not homogenous at the α=0.05 significancе level.

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
                "formatting_check": formatting_check
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
            "component_2_score": "Q-Q Plot Name",
            "component_3_score": "Figure 1",
            "component_4_score": "Levene's Name & Table",
            "component_5_score": "Conclusion on Homogeneity",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "STRICT",
            "component_4_score": "HYBRID",
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
            question_name="QUESTION 10_2",
            question_description="Assumption Checking: Normality and Variance Homogeneity",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )