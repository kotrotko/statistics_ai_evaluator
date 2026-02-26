"""
question_mid_v1_1.py
Midterm Variant 1 - Question 1 Evaluator
Manual Computations: ΣX, ΣY², ΣXY, (ΣY)²
"""

import re
import textwrap

from config import BaseEvaluator

class QuestionMidV1_1Evaluator(BaseEvaluator):
    """
    Evaluator for Midterm Variant 1 Question 1.

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
            "name": False,
            "title": False,
            "task_description": False,
            "sigma_x": False,
            "sigma_y2": False,
            "sigma_xy": False,
            "sigma_y_squared": False
        }

        evidence = []

        # Check for student name
        first_lines = student_answer[:200]
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

        # Check for title
        if re.search(r'\bmidterm\b', text_lower) and (re.search(r'\bvariant\s*1\b', text_lower) or re.search(r'\bv\s*1\b', text_lower)):
            elements_found["title"] = True
            evidence.append("Title found")

        # Check for task description
        if re.search(r'use\s+the\s+following\s+dataset|manual\s+computation', text_lower):
            elements_found["task_description"] = True
            evidence.append("Task description found")

        # Check for calculations
        if re.search(r'22', student_answer):
            elements_found["sigma_x"] = True
            evidence.append("ΣX=22 found")

        if re.search(r'87', student_answer):
            elements_found["sigma_y2"] = True
            evidence.append("ΣY²=87 found")

        if re.search(r'79', student_answer):
            elements_found["sigma_xy"] = True
            evidence.append("ΣXY=79 found")

        if re.search(r'361', student_answer):
            elements_found["sigma_y_squared"] = True
            evidence.append("(ΣY)²=361 found")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No elements found"]
        }

    def grade_midterm_v1_q1(self, student_answer: str, test_mode: bool = False):
        """
        Grade Midterm Variant 1 Question 1.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API

        Returns:
            Detailed grading breakdown dictionary
        """
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 5,
                    "component_2_score": 5,
                    "component_3_score": 5,
                    "component_4_score": 5
                },
                max_points=20,
                feedback="Excellent work on all calculations.",
                vibe="Strong understanding of summation notation",
                additional_data={
                    "element_check": {
                        "elements_found": {"name": True, "title": True, "task_description": True, "sigma_x": True, "sigma_y2": True, "sigma_xy": True, "sigma_y_squared": True},
                        "evidence": ["Test mode"]
                    }
                }
            )

        element_check = self.check_required_elements(student_answer)

        prompt = f"""You are grading a midterm exam statistics question using RUBRICATOR approach - strict point-by-point scoring.

**QUESTION:**
Use the following dataset for manual computations:
X: 3, 5, 7, 6, 1
Y: 7, 3, 4, 2, 3

Calculate:
a. ΣX
b. ΣY²
c. ΣXY
d. (ΣY)²

**CORRECT ANSWERS:**
a) ΣX = 22
b) ΣY² = 87
c) ΣXY = 79
d) (ΣY)² = 361

**GRADING STRUCTURE:**
Component 1: Name + Title + Task Description + All Four Calculations (5 points)
Component 2: ΣY² calculation (5 points)
Component 3: ΣXY calculation (5 points)
Component 4: (ΣY)² calculation (5 points)
Total: 20 points

STUDENT ANSWER:
{student_answer}

**ELEMENT DETECTION:**
Found: {element_check['elements_found']}
Evidence: {element_check['evidence']}
**Component 1: Name + Title + Task Description + ΣX Calculation (0-5 points)**

STEP 1 - Check for student name (STRICT):
- Look for name at TOP: "Name: John Doe", "Written by: Jane Smith", "By: Alex Brown"
- If NO name: Deduct 1 point
- Required feedback: "Your name is expected here. Minus 1 point."

STEP 2 - Check for title (STRICT):
- Use elements_found["title"] value from automatic detection above
- If False: 0 points, add feedback "Title should contain 'Midterm' and 'Variant 1'. Minus 1 point."
- If True: 1 point

STEP 3 - Check for task description (STRICT):
- Must reference dataset or task: "Use the following dataset for manual computations"
- If NO task description: Deduct 1 point
- Required feedback: "Task description is missing. Minus 1 point."

STEP 4 - Check ΣX calculation details (STRICT):
- Student must show manual calculation steps for ΣX (e.g. 3+5+7+6+1)
- More than one version is allowed
- If NO calculation details shown: Deduct 1 point
- Required feedback: "ΣX calculation steps are missing. Minus 1 point."

STEP 5 - Check ΣX calculation answer (STRICT):
- Answer must be present and correct: ΣX = 22
- If answer missing or incorrect: Deduct 1 point
- Required feedback: "ΣX answer is missing or incorrect. Minus 1 point."

FINAL Component 1 score:
- Start at 5 points
- Deduct 1 for each absent/incorrect element (name, title, task, details, answer)
- Range: 0-5

**Component 2: ΣY² Calculation (0-5 points)**

STRICT RUBRIC:
- ΣY² = 87 correct with work: 5 points
- Correct, minimal work: 4 points
- Right method, wrong arithmetic: 2-3 points
- Wrong method or confuses with (ΣY)²: 0-1 points
- Missing: 0 points

**Component 3: ΣXY Calculation (0-5 points)**

STRICT RUBRIC:
- ΣXY = 79 correct with work: 5 points
- Correct, minimal work: 4 points
- Right method, wrong arithmetic: 2-3 points
- Wrong method: 0-1 points
- Missing: 0 points

**Component 4: (ΣY)² Calculation (0-5 points)**

STRICT RUBRIC:
- (ΣY)² = 361 correct with work: 5 points
- Correct, minimal work: 4 points
- Right method, wrong arithmetic: 2-3 points
- Wrong method or confuses with ΣY²: 0-1 points
- Missing: 0 points

**SCORING:**
1. Component 1: __/5
2. Component 2: __/5
3. Component 3: __/5
4. Component 4: __/5
Total: 0-20

Return JSON:
{{
  "component_1_score": <0-5>,
  "component_1_explanation": "<if < 5: explain missing; if 5 + exceptional: praise; else empty>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<if < 5: explain missing; if 5 + exceptional: praise; else empty>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<if < 5: explain missing; if 5 + exceptional: praise; else empty>",
  "component_4_score": <0-5>,
  "component_4_explanation": "<if < 5: explain missing; if 5 + exceptional: praise; else empty>",
  "total_points": <0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative feedback>",
  "vibe": "<one-sentence impression>"
}}"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"element_check": element_check}
        )

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
        """Display grading results"""
        print("=" * 60)
        print("GRADING RESULTS - MIDTERM V1 QUESTION 1")
        print("Manual Computations: ΣX, ΣY², ΣXY, (ΣY)²")
        print("=" * 60)

        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Name + Title + Task + ΣXΣX Calculations): {grading.get('component_1_score', 'N/A')}/5")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (ΣY²): {grading.get('component_2_score', 'N/A')}/5")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (ΣXY): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 ((ΣY)²): {grading.get('component_4_score', 'N/A')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points', 'N/A')}/{grading.get('max_points', 20)}")
        print(f"PERCENTAGE: {grading.get('percentage', 'N/A')}%")

        print("\n" + "=" * 60)
        print("FEEDBACK:")
        print("=" * 60)
        feedback_text = grading.get('feedback', 'No feedback available')
        wrapped_feedback = textwrap.fill(feedback_text, width=60)
        print(wrapped_feedback)

        print("\n" + "=" * 60)
        print("THE VIBE:")
        print("=" * 60)
        vibe_text = grading.get('vibe', 'N/A')
        wrapped_vibe = textwrap.fill(vibe_text, width=60)
        print(wrapped_vibe)

        if 'error' in grading:
            print("\n" + "=" * 60)
            print("ERROR:")
            print("=" * 60)
            print(grading.get('error'))
            if 'raw_response' in grading:
                print("\nRaw Response:")
                print(grading['raw_response'][:500])

def main():
    """    Main function to run a test case for the evaluator.    """
    # 1. Create an instance of your evaluator
    evaluator = QuestionMidV1_1Evaluator()
    # 2. Define a sample student answer to test with
    sample_student_answer = """    
    Name: John Doe    
    Midterm - Variant 1    
    Here are the manual computations for the dataset provided.    
    a. ΣX = 3 + 5 + 7 + 6 + 1 = 22    
    b. ΣY² = 7² + 3² + 4² + 2² + 3² = 49 + 9 + 16 + 4 + 9 = 87    
    c. ΣXY = (3*7) + (5*3) + (7*4) + (6*2) + (1*3) = 21 + 15 + 28 + 12 + 3 = 79    
    d. (ΣY)² = (7 + 3 + 4 + 2 + 3)² = (19)² = 361    """
    # 3. Call the grading method
    print("Grading student answer...")
    grading_results = evaluator.grade_midterm_v1_q1(sample_student_answer)
    # 4. Print the formatted results
    evaluator.print_grading_results(grading_results)

if __name__ == "__main__":
    main()