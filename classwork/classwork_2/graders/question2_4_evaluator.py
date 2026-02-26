"""
question2_4_evaluator.py
Radar Chart Creation and Understanding
"""

import re
import textwrap

from config import BaseEvaluator

class Question2_4Evaluator(BaseEvaluator):
    """
    Evaluator for Radar Chart Question.

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

    def check_radar_elements(self, student_answer: str) -> dict:
        """
        Check if radar chart elements are mentioned.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()

        elements_found = {
            "radar_chart": False,
            "dataset_description": False,
            "figure_number": False,
            "circular_transformation": False
        }

        evidence = []

        # Check for radar chart mention
        radar_patterns = [r'\bradar\b', r'\bspider\b', r'\bweb chart\b', r'\bpolar\b']
        for pattern in radar_patterns:
            if re.search(pattern, text_lower):
                elements_found["radar_chart"] = True
                evidence.append(f"Found radar chart indicator: {pattern}")
                break

        # Check for dataset description/introduction
        desc_patterns = [r'\bdataset\b', r'\bdata description\b', r'\bintroduction\b', r'\bintroductory phrase\b']
        for pattern in desc_patterns:
            if re.search(pattern, text_lower):
                elements_found["dataset_description"] = True
                evidence.append(f"Found dataset description indicator: {pattern}")
                break

        # Check for figure numbering (Figure 3)
        fig_patterns = [r'\bfigure\s*3\b', r'\bfig\.\s*3\b', r'\bdiagram\s*3\b']
        for pattern in fig_patterns:
            if re.search(pattern, text_lower):
                elements_found["figure_number"] = True
                evidence.append(f"Found figure number indicator: {pattern}")
                break

        # Check for circular/transformation explanation
        transform_patterns = [r'\bcircular\b', r'\bscale\b', r'\btransform\b', r'\brepresentation\b', r'\baxes\b', r'\baxis\b']
        for pattern in transform_patterns:
            if re.search(pattern, text_lower):
                elements_found["circular_transformation"] = True
                evidence.append(f"Found transformation indicator: {pattern}")
                break

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["No clear radar chart indicators found"],
            "all_present": all(elements_found.values())
        }

    def grade_radar_chart(self, student_answer: str, test_mode: bool = False):
        """
        Grade Radar Chart question.

        Args:
            student_answer: The student's response text
            test_mode: If True, returns mock data without calling API

        Returns:
            Detailed grading breakdown dictionary
        """
        # Test mode - use base class method
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 5,
                    "component_2_score": 5,
                    "component_3_score": 5,
                    "component_4_score": 5
                },
                max_points=20,
                feedback="Excellent work creating a radar chart with proper dataset description, figure numbering, and clear explanation of circular transformation.",
                vibe="Student demonstrates strong understanding of radar chart creation and visualization transformation",
                additional_data={
                    "radar_check": {
                        "elements_found": {"radar_chart": True, "dataset_description": True, "figure_number": True, "circular_transformation": True},
                        "all_present": True,
                        "evidence": ["Test mode - all elements present"]
                    }
                }
            )

        # Check for required elements
        radar_check = self.check_radar_elements(student_answer)

        # Build the grading prompt
        prompt = f"""You are grading a statistics classwork using a **HYBRID approach** - combining vibe-based holistic grading with strict requirements for specific components.

**TASK DESCRIPTION:**
Students must:
1. Use dataset description from 2.3.1. Radar Chart.xlsx for introductory phrase and Figure description (5 points)
2. Number and title the diagram as Figure 3 (5 points)
3. Build a regular Radar diagram in Excel (5 points)
4. Explain how the radar diagram transforms a regular chart into a circular scale representation (5 points)

Total: 20 points

STUDENT ANSWER:
{student_answer}

**AUTOMATIC ELEMENT DETECTION RESULT:**
Elements Found: {radar_check['elements_found']}
All Required Elements Present: {radar_check['all_present']}
Evidence: {radar_check['evidence']}

**IMPORTANT NOTES:**
- Students submit text descriptions since visual elements (actual charts) cannot be captured in text
- If student REFERENCES a figure/chart (e.g., "Figure 3", "the radar chart shows", "see diagram below"), ASSUME the chart exists in their actual document
- DO NOT penalize for "missing" charts if they clearly reference and discuss the chart
- Focus on whether they understand radar charts and present the required elements appropriately

**HYBRID GRADING APPROACH:**

**Component 1: Dataset description used for intro and figure description - VIBE (0-5 points)**
- Focus: Does the student provide an introductory phrase and describe what the figure shows?
- Evidence: mentions what the dataset contains, provides context for the radar chart
- Be generous: any reasonable dataset description or introduction
- 0 points: No introduction or dataset description
- 2-3 points: Minimal introduction or vague description
- 4-5 points: Clear introductory phrase that describes the dataset/figure content

**Component 2: Figure numbered and titled as Figure 3 - STRICT (0-5 points)**
- 0 points: No figure number or title
- 1 point: Has only number OR title (not both), missing one element
- 3 points: Has both number and title but incorrect number (not Figure 3/Diagram 3)
- 4 points: Correct number (Figure 3 or Diagram 3) and title present but but missing introductory sentence OR has minor APA format issues
- 5 points: Proper APA format with:
  - Figure 3 or Diagram 3 (correct number)
  - Descriptive title for the radar chart
  - Proper formatting
- **STRICT REQUIREMENT**: Must have number "3" (as Figure 3 or Diagram 3) AND a title
- **NOTE**: Accept both "Figure 3" and "Diagram 3" as correct numbering
- **IMPORTANT**: Maximum score is 4 points if introductory sentence is missing, even if number and title are correct

**Component 3: Radar diagram built in Excel - VIBE (0-5 points)**
- Focus: Does the student show evidence of creating a radar chart?
- Evidence: mentions building/creating radar chart, discusses Excel steps, references the chart
- Be generous: any indication they created the chart
- 0 points: No mention of creating a radar chart
- 2-3 points: Mentions radar chart but unclear if they built it
- 4-5 points: Clear evidence of building the radar chart (discusses creation process, mentions Excel, or shows they made it)

**Component 4: Explanation of circular transformation - VIBE (0-5 points)**
- Focus: Does the student explain how radar charts transform regular charts into circular representation?
- Evidence: discusses circular/radial layout, multiple axes, scale representation, or transformation concept
- Key concepts to look for: circular arrangement, axes radiating from center, comparing multiple variables
- 0 points: No explanation of transformation
- 2-3 points: Vague or incomplete explanation
- 4-5 points: Clear explanation of how radar charts use circular scale to represent data differently than regular charts

**CRITICAL RULES:**
1. Components 1, 3, and 4 are VIBE - focus on evidence of understanding
2. Component 2 is STRICT - must have "Figure 3" AND a title
3. Be generous with chart references - if they discuss it, assume they created it
4. Focus on understanding of radar chart visualization concepts
5. Don't over-penalize for imperfect formatting as long as content is there

**SCORING PROCESS:**
1. Score Component 1 (Dataset description/intro) - VIBE: __/5
2. Score Component 2 (Figure 3 number and title) - STRICT: __/5
3. Score Component 3 (Radar diagram built) - VIBE: __/5
4. Score Component 4 (Circular transformation explanation) - VIBE: __/5
5. Total = sum of four scores

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- Acknowledges their radar chart creation and description
- Points out any missing elements specifically
- Comments on their understanding of circular transformation
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
  "feedback": "<narrative explanation - what they did well, what's missing, how to improve>",
  "vibe": "<one-sentence overall impression of their radar chart understanding and execution>"
}}"""

        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"radar_check": radar_check}
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
        """Helper function to display grading results"""
        print("=" * 60)
        print("GRADING RESULTS - QUESTION 2_4 (HYBRID MODE)")
        print("Radar Chart Creation and Understanding")
        print("=" * 60)

        # Print component breakdown if available
        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Dataset description/intro): {grading.get('component_1_score', 'N/A')}/5")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Figure 3 number and title): {grading.get('component_2_score', 'N/A')}/5")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Radar diagram built): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Circular transformation explanation): {grading.get('component_4_score', 'N/A')}/5")
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

if __name__ == "__main__":
    print("Welcome to the Classwork AI Evaluator System!")
    print("=" * 60)

    # Initialize evaluator
    evaluator = Question2_4Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("CLASSWORK 2 - QUESTION 2_4 EVALUATOR")
    print("Radar Chart Creation and Understanding")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION 2_4.")
    print("(Press Enter twice when finished, or type 'END' on a new line)\n")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        lines.append(line)
        # Check if last two lines are empty (double Enter)
        if len(lines) >= 2 and lines[-1] == '' and lines[-2] == '':
            lines = lines[:-2]  # Remove the two empty lines
            break

    student_answer = '\n'.join(lines)

    # Validate input
    if not student_answer.strip():
        print("\n❌ Error: No answer provided. Exiting.")
        exit(1)

    print("\n" + "=" * 60)
    print("EVALUATING...")
    print("=" * 60)

    # Grade with Groq API
    grading = evaluator.grade_radar_chart(student_answer)

    # Display results
    evaluator.print_grading_results(grading)