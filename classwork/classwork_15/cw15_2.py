"""
cw15_2.py
Classwork 15: Exploratory Factor Analysis
Factor Creation
Evaluation method name: def grade_question_cw15_2_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter
from config.formatting_checks import check_formatting_elements_type2

class CW15_2Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 15_2.

    Task 2. Factor Creation. Include Factor Loadings table, based on promax rotation (5 points). How many factors do you see? What is proportion of items shows strong factor loading ((≥ .40)? What does it mean in terms of clustering into latent factors? Which items showed weaker loading and higher uniqueness, indicating weaker representation within their factors?  (5 points). Number of Factors. Play with different values for Eigenvalues: try 1, 2, 3, 4 and 0 (some settings may show an error). What happens to the number of extracted factors (5 points)? Which number seems most reasonable and why (5 points)? Then, for further analysis, use 1 as default, since no theory predicts a specific number of eigenvalues.  Setting to 1 extracts all factors with eigenvalue > 1.
    """

    def __init__(self):
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

        # Regex-derived rubric checkpoints passed into AUTOMATIC DETECTION
        # inside the grading prompt. Used by the LLM to support consistent
        # hybrid rubric grading, especially for strict required elements.
        elements_found = {
            "factor_loadings_table": False,
            "three_factor_structure": False,
            "eigenvalue_behavior": False,
        }

        evidence = []

        # Checkpoint 1 — Factor loadings table (promax)
        if re.search(r'promax|factor\s*loading|table\s*4', text_lower):
            elements_found["factor_loadings_table"] = True
            evidence.append("Factor loadings table found")
        else:
            evidence.append("Factor loadings table NOT found")

        # Checkpoint 2 — Three-factor structure identification
        if re.search(r'three[\s-]?factor|3[\s-]?factor|three\s*factor', text_lower):
            elements_found["three_factor_structure"] = True
            evidence.append("Three-factor structure found")
        else:
            evidence.append("Three-factor structure NOT found")

        # Checkpoint 3 — Eigenvalue behavior
        if re.search(r'eigenvalue', text_lower) and \
                re.search(r'fewer|more|number\s*of\s*factor', text_lower):
            elements_found["eigenvalue_behavior"] = True
            evidence.append("Eigenvalue behavior found")
        else:
            evidence.append("Eigenvalue behavior NOT found")

        # Checkpoint 4 — Rotation comparison (oblique vs orthogonal)
        if re.search(r'oblique|oblimin|varimax|orthogonal', text_lower) and \
                re.search(r'if you have factors|correlated|independent|interpretable', text_lower):
            elements_found["rotation_comparison"] = True
            evidence.append("Rotation comparison found")
        else:
            evidence.append("Rotation comparison NOT found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"]
        }

    def grade_question_cw15_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 15.2: Factor Creation and Rotation
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
                    "component_3_score": 5,
                    "component_4_score": 5,
                    "component_5_score": 5,
                },
                max_points=20,
                feedback="[TEST MODE] Factor structure identified. Eigenvalue behavior described. Oblique rotation justified.",
                vibe="Student demonstrates solid understanding of EFA factor extraction and rotation.",
                additional_data={
                    # Mock mirrors what check_required_elements and
                    # check_formatting_elements_type2 return in actual grading
                    "element_check": {
                        # Simulates check_required_elements() output in test mode.
                        # Keys must match elements_found in check_required_elements exactly.
                        "elements_found": {
                            "factor_loadings_table": True,
                            "three_factor_structure": True,
                            "eigenvalue_behavior": True,
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    },
                    "formatting_check": {
                        "elements_found": {
                            "task_description": True,
                            "autoformatting": True,
                        },
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        formatting_check = check_formatting_elements_type2(
            student_answer,
            pedagogical_markers=["if you have factors", "how many factors do you see"]
        )

        prompt = f"""You are grading a statistics classwork assignment on Exploratory Factor Analysis.

**TASK DESCRIPTION:**
Include Factor Loadings table, based on promax rotation (5 points). 
How many factors do you see? What is proportion of items shows strong factor
loading ((≥ .40)? What does it mean in terms of clustering into latent factors?
Which items showed weaker loading and higher uniqueness, indicating weaker
representation within their factors?  (5 points). 
Number of Factors. Play with different values for Eigenvalues: try 1, 2, 3, 4 and
(some settings may show an error). What happens to the number of extracted factors
(5 points)? Which number seems most reasonable and why (5 points)? 
Then, for further analysis, use 1 as default, since no theory predicts a specific
number of eigenvalues.  Setting to 1 extracts all factors with eigenvalue > 1.

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

**RUBRIC**

**Component 1: Formatting (2 points):**
Use AUTOMATIC FORMATTING DETECTION RESULT above.
- 1 point: Task description correctly formatted
- 1 point: Proper autoformatting and structure

**Component 2: Factor Loadings Table (5 points):**
Use AUTOMATIC DETECTION above.
- 1 point: Introductory phrase present before the table
- 1 point: Reference to table number in introductory phrase
- 1 point: Standalone table number present
- 1 point: Descriptive table title present
- 1 point: Table itself with numerical data present
- CRITICAL: A label above the table such as "Table 4. Factor Loadings" counts as a title
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 3: Factor Structure Interpretation (5 points):**
- 1 point: Number of factors correctly identified as 3
- 1 point: Factor composition described (Factor 1: x4, x5, x6; Factor 2: x7, x8, x9; Factor 3: x1, x2, x3)
- 1 point: Proportion of items with strong factor loading (≥ .40) stated
- 1 point: Meaning of clustering into latent factors explained
- 1 point: Items with weaker loading and higher uniqueness identified (x2 and x9)
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 4: Eigenvalues and Number of Factors (4 points):**
- 1 point: Describes what happens when eigenvalue is set to 1
- 1 point: Describes what happens when eigenvalue is set to 2, 3, and 4
- 1 point: Describes what happens when eigenvalue is set to 0 (error or more factors)
- 1 point: Correctly explains the relationship (higher cut-off → fewer factors retained)
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**Component 5: Most Reasonable Eigenvalue (4 points):**
- 1 point: Identifies eigenvalue > 1 as the most reasonable setting
- 1 point: Justifies using meaningful factor loadings as criterion
- 1 point: Justifies using interpretable factor structure as criterion
- 1 point: Explains why higher or lower cut-offs are less appropriate
- CRITICAL: Do NOT assume elements are present if not explicitly written in the student's text

**CORRECT ANSWER REFERENCE:**

On the Table 4, we see the rotated Exploratory Factor Analysis solution using promax rotation identified a three-factor structure, with most items showing acceptable to strong factor loadings (≥ .40), indicating that the variables clustered meaningfully into three latent factors. 
Interpretation: Factor 1 was mainly defined by x5, x4, and x6; Factor 2 by x7, x8, and x9; and Factor 3 by x3, x1, and x2, suggesting that the questionnaire measures three underlying constructs, although x2 and x9 showed relatively weaker loadings and higher uniqueness, indicating weaker representation by their factors.
Table 4. Factor Loadings 
 	Factor 1	Factor 2	Factor 3	Uniqueness
x5		0.895		 		 		0.246	
x4		0.849		 		 		0.272	
x6		0.804		 		 		0.309	
x7		 		0.759		 		0.481	
x8		 		0.710		 		0.480	
x9		 		0.476		 		0.540	
x3		 		 		0.699		0.547	
x1		 		 		0.598		0.523	
x2		 		 		0.531		0.745	

Note.  Applied rotation method is promax.

Number of Factors. 
As the eigenvalue cut-off increased from 1 to 2, 3, and 4, fewer factors were extracted because only stronger factors were retained, while setting it to 0 allowed more factors (or produced an error), showing that the eigenvalue criterion directly determines the number of extracted factors.

Reasonable eigenvalue. 
The most reasonable solution is eigenvalue = 1 because it retained three factors with meaningful factor loadings and interpretable structure, while higher cut-offs removed potentially important factors and lower values included weak or statistically unstable factors.

**FEEDBACK RULES**
- Identify which components were completed correctly
- Point out missing or incomplete elements explicitly
- Maintain supportive tone

Return JSON only:
{{
  "originality_concern": <true/false>,
  "component_1_score": <0-2>,
  "component_1_task_score": <0-1>,
  "component_1_autoformat_score": <0-1>,
  "component_1_explanation": "<brief explanation for formatting>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<brief>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<brief>",
  "component_4_score": <0-4>,
  "component_4_explanation": "<brief>",
  "component_5_score": <0-4>,
  "component_5_explanation": "<brief>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<SHORT teacher's comment, not an invitation for discussion>",
  "vibe": "<one-sentence overall impression>"
}}
"""

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
        """Display grading results using OutputFormatter."""
        # Define component labels
        component_labels = {
            "component_1_score": "Formatting (Task desc / Autoformatting)",
            "component_2_score": "Factor Loadings Table",
            "component_3_score": "Factor Structure Interpretation",
            "component_4_score": "Eigenvalues and Number of Factors",
            "component_5_score": "Most Reasonable Eigenvalue",
        }

        # Define component types
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "HYBRID",
            "component_3_score": "HYBRID",
            "component_4_score": "HYBRID",
            "component_5_score": "HYBRID",
        }

        max_scores = {
            "component_1_score": 2,
            "component_2_score": 5,
            "component_3_score": 5,
            "component_4_score": 4,
            "component_5_score": 4,
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="CW15_2",
            question_description="EFA - Factor Creation",
            component_labels=component_labels,
            max_score=max_scores,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )
