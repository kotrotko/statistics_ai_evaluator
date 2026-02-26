"""
question2_3_evaluator.py
Excel Histogram + Figure Formatting + X-axis Labels + Bar Chart vs Histogram
"""

import re

from config import BaseEvaluator
from config.output_formatter import OutputFormatter


class Question2_3Evaluator(BaseEvaluator):
    """
    Evaluator for Question 2_3: Excel Histogram, Figure Formatting, and Chart Comparison.

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    def __init__(self):
        """Initialize evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1200
        )
        # Initialize output formatter
        self.formatter = OutputFormatter(default_width=60)

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check if required elements (histogram, figure numbering, x-axis, comparison) are present.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "histogram_built": False,
            "figure_numbered": False,
            "x_axis_labels": False,
            "bar_histogram_difference": False
        }

        evidence = []

        # Check for histogram creation
        histogram_patterns = [r'\bhistogram\b', r'\bbuild\b', r'\bcreate\b', r'\bexcel\b', r'\bchart\b']
        for pattern in histogram_patterns:
            if re.search(pattern, text_lower):
                elements_found["histogram_built"] = True
                evidence.append(f"Found histogram indicator: {pattern}")
                break

        # Check for figure numbering/titling
        figure_patterns = [r'\bfigure 2\b', r'\bhistogram 2\b', r'\bnumber\b', r'\btitle\b', r'\bintroduce\b']
        for pattern in figure_patterns:
            if re.search(pattern, text_lower):
                elements_found["figure_numbered"] = True
                evidence.append(f"Found figure numbering indicator: {pattern}")
                break

        # Check for x-axis labels
        axis_patterns = [r'\bx-axis\b', r'\bx axis\b', r'\bhorizontal axis\b', r'\blabel\b', r'\baxis label\b']
        for pattern in axis_patterns:
            if re.search(pattern, text_lower):
                elements_found["x_axis_labels"] = True
                evidence.append(f"Found x-axis indicator: {pattern}")
                break

        # Check for bar chart vs histogram explanation
        comparison_patterns = [r'\bbar chart\b', r'\bdifference\b', r'\bhistogram\b.*\bbar\b', r'\bcontinuous\b', r'\bcategorical\b']
        comparison_count = sum(1 for pattern in comparison_patterns if re.search(pattern, text_lower))
        if comparison_count >= 2:
            elements_found["bar_histogram_difference"] = True
            evidence.append("Found bar chart vs histogram comparison indicators")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear element indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_question2_3_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Question 2_3: Excel histogram, figure formatting, x-axis labels, and chart comparison.
        Returns detailed grading breakdown.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API
        """

        # Test mode for verification without API
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 5,
                    "component_2_score": 4,
                    "component_3_score": 5,
                    "component_4_score": 4,
                },
                max_points=20,
                feedback="[TEST MODE] Good histogram creation and x-axis labeling. Minor improvements needed in figure numbering and comparison explanation.",
                vibe="Student demonstrates solid understanding of Excel charts and statistical visualization concepts",
                additional_data={
                    "element_check": {
                        "elements_found": {
                            "histogram_built": True,
                            "figure_numbered": True,
                            "x_axis_labels": True,
                            "bar_histogram_difference": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Students must:
1. Build a histogram in Excel for the Q5 variable, numbered as "Histogram 2" (5 points)
2. Introduce, number, and title the histogram as a Figure (5 points)
3. Ensure correct X-axis labels are present (5 points)
4. Answer: What is the difference between bar chart and histogram? (5 points)

Note: AI usage was encouraged but optional for this task.

Total: 20 points

STUDENT ANSWER:
{student_answer}

**IMPORTANT NOTES:**
- Students submit text descriptions of their work since visual elements (actual histograms, screenshots, Excel files) cannot be captured in text
- If student REFERENCES or DESCRIBES the required elements (e.g., "I built a histogram in Excel", "I labeled the x-axis with score values"), ASSUME they completed it in their actual document
- DO NOT penalize for "missing" visual elements if they clearly describe what they did
- Give credit for AI usage if mentioned, but don't penalize if not mentioned (it was optional)

**HYBRID GRADING APPROACH:**

**Component 1: Excel Histogram Creation - STRICT (0-5 points)**
- 5 points: Student correctly built a histogram in Excel for Q5 variable (Histogram 2)
- 4 points: Built histogram with minor issues (e.g., wrong chart type initially, formatting issues)
- 2-3 points: Attempted histogram but with significant issues or unclear description
- 0-1 points: Did not build histogram or completely incorrect

**Component 2: Figure Introduction/Numbering/Title - STRICT (0-5 points)**
- 5 points: Student correctly introduced, numbered (as Figure 2 or similar), and titled the histogram
- 4 points: Has 2 of 3 elements (introduction, number, title)
- 2-3 points: Has 1 of 3 elements
- 0-1 points: Missing all three elements

**Component 3: X-axis Labels - STRICT (0-5 points)**
- 5 points: Student correctly ensured proper X-axis labels (score values: 0-10 or bins)
- 4 points: X-axis labels present with minor issues (e.g., slight formatting problems)
- 2-3 points: X-axis labels unclear, incomplete, or partially correct
- 0-1 points: Missing X-axis labels or completely incorrect

**Component 4: Bar Chart vs Histogram Difference - STRICT (0-5 points)**
- 5 points: Student correctly explained the key difference (histogram shows continuous/quantitative data distribution with no gaps between bars; bar chart shows categorical/discrete data with gaps between bars)
- 4 points: Correct explanation with minor inaccuracies or missing one key detail
- 2-3 points: Partial understanding (mentions some differences but misses key concepts)
- 0-1 points: Incorrect explanation or did not answer

**KEY DIFFERENCES (for reference):**
- **Histogram**: Displays continuous/quantitative data, bars touch (no gaps), shows frequency distribution
- **Bar Chart**: Displays categorical/discrete data, bars have gaps, compares different categories

**CRITICAL RULES:**
1. Each component is STRICT - must be present to earn points
2. If student meets requirements exactly: 5/5 points
3. If student does extra correct work beyond requirements: 5/5 points + praise in explanation
4. Minor issues are acceptable if the core requirement is met
5. Bonus acknowledgment (not points) if student mentions using AI effectively

**SCORING PROCESS:**
1. Score Component 1 (Histogram Creation): __/5
2. Score Component 2 (Figure Numbering/Title): __/5
3. Score Component 3 (X-axis Labels): __/5
4. Score Component 4 (Bar vs Histogram): __/5
5. Total = sum of four scores

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- Acknowledges what elements they successfully completed
- Points out any missing components specifically
- Comments on their explanation of bar chart vs histogram
- Mentions AI usage if they referenced it
- Explains what would improve their score
- Remains encouraging and constructive

Return your grading in this exact JSON format:
{{
  "component_1_score": <0-5>,
  "component_1_explanation": "<if score < 5: one sentence explaining what's missing or problematic; if score = 5 AND student did good extra work beyond requirements (provided helpful examples, added clear explanations, showed original insight, caught errors): one sentence of praise; otherwise empty string>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<if score < 5: one sentence explaining what's missing or problematic; if score = 5 AND student did good extra work beyond requirements (provided helpful examples, added clear explanations, showed original insight, caught errors): one sentence of praise; otherwise empty string>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<if score < 5: one sentence explaining what's missing or problematic; if score = 5 AND student did good extra work beyond requirements (provided helpful examples, added clear explanations, showed original insight, caught errors): one sentence of praise; otherwise empty string>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<if score < 5: one sentence explaining what's missing or problematic; if score = 5 AND student did good extra work beyond requirements (provided helpful examples, added clear explanations, showed original insight, caught errors): one sentence of praise; otherwise empty string>",
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative explanation - which elements they completed well, what's missing, quality of their bar chart vs histogram explanation, how to improve>",
  "vibe": "<one-sentence overall impression of their Excel skills and conceptual understanding>"
}}"""
        # Check for required elements
        element_check = self.check_required_elements(student_answer)

        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"element_check": element_check}
        )

        # If grading succeeded, validate component scores
        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
                "component_4_score"
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
            "component_1_score": "Component 1 (Excel Histogram Creation)",
            "component_2_score": "Component 2 (Figure Number/Title)",
            "component_3_score": "Component 3 (X-axis Labels)",
            "component_4_score": "Component 4 (Bar Chart vs Histogram)"
        }

        # Define component types (all STRICT for this question)
        component_types = {
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT"
        }

        # Use formatter to display results
        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 2_3",
            question_description="Excel Histogram + Figure Formatting + Chart Comparison",
            component_labels=component_labels,
            max_score=5,
            component_types=component_types,
            check_configs=None,  # No automatic checks for this question
            width=60,
            mode="HYBRID"
        )