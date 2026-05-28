"""
cw14_2.py
Classwork 14: Chi Square
Step system: method justification, hypotheses, significance level, and statistical inference
Evaluation method name: def grade_question_cw14_2_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2

class CW14_2Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 14_2.

    Task 2. Name the method you choose and justify it based on the data level (5 points). State the hypotheses in needed form (5 points). State the significance level α, calculate df, find the critical value. (5 points). Open the JASP > Frequencies > Contingency Tables tool. Make sure that you have Physical Activity on Rows and Fruit Consumption on Columns. Include the “Contingency Tables” table, number it, make sure that it is introduced, numbered, and named (5 points).

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
            "method_justification": False,
            "hypotheses": False,
            "significance_setup": False,
            "inference": False,
        }

        evidence = []

        # Checkpoint 1 — Method justification (Step 1)
        if re.search(
                r'chi[\s-]?square|chi[\s-]?squared|χ²|categorical|nominal|'
                r'independence|contingency|non[\s-]?parametric',
                text_lower
        ):
            elements_found["method_justification"] = True
            evidence.append("Method justification found")
        else:
            evidence.append("Method justification NOT found")

        # Checkpoint 2 — Hypotheses (Step 2)
        if re.search(
                r'h[0o]\s*:|h[1a]\s*:|null\s*hypothesis|alternative\s*hypothesis|'
                r'independent|not\s*independent|associated|no\s*association',
                text_lower
        ):
            elements_found["hypotheses"] = True
            evidence.append("Hypotheses found")
        else:
            evidence.append("Hypotheses NOT found")

        # Checkpoint 3 — Significance level, df, critical value (Step 3)
        if re.search(
                r'α|alpha|significance\s*level|df\s*=|\bdf\b|degrees\s*of\s*freedom|'
                r'critical\s*value|χ²\s*crit|chi[\s-]?square\s*critical',
                text_lower
        ):
            elements_found["significance_setup"] = True
            evidence.append("Significance setup found")
        else:
            evidence.append("Significance setup NOT found")

        # Checkpoint 4 — Contingency table (Step 4)
        if re.search(
                r'table\s*\d+|contingency\s*table|\bfrequency\b|'
                r'physical\s*activity|fruit\s*consumption',
                text_lower
        ):
            elements_found["contingency_table"] = True
            evidence.append("Contingency table found")
        else:
            evidence.append("Contingency table NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_question_cw14_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 14.2: Chi Square step system.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 1,
                    "component_2_score": 4,
                    "component_3_score": 5,
                    "component_4_score": 5,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Strong structured answer with all steps present.",
                vibe="Clear Chi Square step-system reasoning",
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["make sure that you have"],
        )

        prompt = f"""You are grading a statistics assignment using a STRICT rubric.

**TASK DESCRIPTION:**
Task 2. Name the method you choose and justify it based on the data level (5 points). State the hypotheses in needed form (5 points). State the significance level α, calculate df, find the critical value. (5 points). Open the JASP > Frequencies > Contingency Tables tool. Make sure that you have Physical Activity on Rows and Fruit Consumption on Columns. Include the “Contingency Tables” table, number it, make sure that it is introduced, numbered, and named

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

Component 1: Formatting (2 points)
DO NOT SCORE — handled externally. Leave component_1_score as 0.
Use AUTOMATIC FORMATTING DETECTION RESULT above.
- 1 point: Task description present
- 1 point: No auto-formatting detected (no bullet points, numbered lists, etc.)

Component 2: Step 1 — Method Choice and Justification (5 points)
Student must name Chi Square test of independence and justify why it is appropriate
based on the level of measurement of the variables (both categorical/nominal).

- 2 points: Method name explicitly stated in a sentence (e.g., "I will use the Chi Square test of independence")
- 1 point: Data level argument provided (both variables are categorical/nominal)
- 1 point: One variable argument provided (variable name referenced in justification)
- 1 point: Independence/association argument provided (why Chi Square fits the research question)
- 0 points: Completely absent

CRITICAL: Justification must reference data level (categorical/nominal), not just say
"Chi Square is appropriate."

Component 3: Step 2 — State the Hypotheses (4 points)
Student must state both H0 and H1 in correct form for Chi Square test of independence.

- 2 points: H0 correctly stated (the two variables are independent / no association)
- 2 points: H1 correctly stated (the two variables are not independent / there is an association)
- 1 point each: Hypothesis present but imprecise or missing variable reference
- 0 points each: Absent or completely wrong

Accept symbolic or verbal forms. Variables must be identifiable (physical activity,
fruit consumption, or equivalent).

Component 4: Step 3 — Significance Level, df, Critical Value (4 points)
Student must state α, calculate df correctly, and identify the critical value.

- 1 point: Significance level α stated (e.g., α = 0.05)
- 2 points: df calculated correctly using (R-1)(C-1); for a 3×3 table df = 4
- 1 point: Critical value stated correctly corresponding to the df and α

CRITICAL: df for Chi Square = (rows - 1)(columns - 1). For a 3×3 table: df = 4.
Accept any correct critical value corresponding to the stated df and α.
Task 2. Name the method you choose and justify it based on the data level (5 points). State the hypotheses in needed form (5 points). State the significance level α, calculate df, find the critical value. (5 points). Open the JASP > Frequencies > Contingency Tables tool. Make sure that you have Physical Activity on Rows and Fruit Consumption on Columns. Include the “Contingency Tables” table, number it, make sure that it is introduced, numbered, and named 
Component 5: Step 4 — Contingency Table (5 points)
Student must include the Contingency Tables output from JASP, properly introduced, numbered, and named,
with Physical Activity on Rows and Fruit Consumption on Columns.

- 1 point: The actual contingency table with numerical data is present
- 1 point: Introductory phrase present before the table
- 1 point: Reference to table number in the introductory phrase
- 1 point: Standalone table number present on the table itself
- 1 point: Descriptive table title present (naming both variables)
- CRITICAL: Do NOT accept a chi-square test table as a substitute for the contingency table.
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text.

**CORRECT ANSWER REFERENCE:**
The appropriate method is the χ² (Chi-square) test of independence because both variables—physical activity level (low, moderate, vigorous) and fruit consumption level (low, medium, high)—are categorical variables measured at the nominal/ordinal level. This test is used to examine whether there is a significant association between two categorical variables in one sample.
H₀ (Null hypothesis): Physical activity level and fruit consumption level are independent among college students (there is no association between them).
H₁ (Alternative hypothesis): Physical activity level and fruit consumption level are not independent among college students (there is an association between them).
Significance level: α = 0.05
df = (3−1)*(3-1) = 4
 χ_critical^2(0.05,4) = 9.488
Table 1 is the contingency table showing the distribution of physical activity levels by fruit consumption among college students.
Table 1
Contingency Table of Physical Activity and Fruit Consumption
Contingency Tables 
	Fruit Consumption	
Physical Activity	Low	Medium	High	Total
Low		69		25		14		108	
Moderate		206		126		111		443	
Vigorous		294		170		169		633	
Total		569		321		294		1184	

Note.  Each cell displays the observed counts

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
  "component_2_score": <0-5>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-4>,
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
}}
"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"element_check": element_check,
                               "formatting_check": formatting_check,
                               }
        )

        if "error" not in result:
            result = self.validate_component_scores(
                result,
                [
                    "component_1_score",
                    "component_2_score",
                    "component_3_score",
                    "component_4_score",
                    "component_5_score",
                ],
                20
            )

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
            "component_2_score": "Method Choice and Justification",
            "component_3_score": "Hypotheses",
            "component_4_score": "Significance Level, df, Critical Value",
            "component_5_score": "Contingency Table",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
            "component_4_score": "HYBRID",
            "component_5_score": "STRICT",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 5,
            "component_3_score": 4,
            "component_4_score": 4,
            "component_5_score": 5,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="CLASSWORK 14_2",
            question_description="Chi Square — Method / Hypotheses / α df CV / Contingency Table",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )