"""
hw2_2.py
Graph Improvement Discussion Evaluator
"""

import re
import textwrap

from config import BaseEvaluator

class HW2_2Evaluator(BaseEvaluator):
    """
    Evaluator for Graph Improvement Discussion Question.

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

    def check_improvement_mentions(self, student_answer: str) -> dict:
        """
        Check if student mentions key graph improvements.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found improvements and evidence
        """
        text_lower = student_answer.lower()

        improvements_found = {
            "horizontal_format": False,
            "dimensionality": False,
            "axis_labels": False,
            "zero_baseline": False,
            "exact_values": False
        }

        evidence = []

        # Check for 2D/3D dimensionality discussion
        dim_patterns = [
            r'\b2[-\s]?d(imension)?(al)?\b',
            r'\b3[-\s]?d(imension)?(al)?\b',
            r'\bdimension\b',
            r'\bflat\b',
            r'\bperspective\b',
            r'\bdepth\b'
        ]
        for pattern in dim_patterns:
            if re.search(pattern, text_lower):
                improvements_found["dimensionality"] = True
                evidence.append(f"Found dimensionality mention: {pattern}")
                break

        # Check for axis labeling discussion
                # Check for axis labeling discussion
        axis_patterns = [
            r'\baxis.*label',
            r'\blabel.*axis',
            r'\by[-\s]axis.*label',
            r'\bx[-\s]axis.*label',
            r'\blabel.*y[-\s]axis',
            r'\blabel.*x[-\s]axis',
            r'\baxes.*label',
            r'\blabel.*axes'
            ]
        for pattern in axis_patterns:
            if re.search(pattern, text_lower):
                improvements_found["axis_labels"] = True
                evidence.append(f"Found axis label mention: {pattern}")
                break

        # Check for zero baseline discussion
        zero_patterns = [
            r'\bzero\b',
            r'\bstart.*0\b',
            r'\bbaseline\b',
            r'\bbegin.*0\b',
            r'\b0\s*baseline\b',
            r'\bfrom\s*0\b'
        ]
        for pattern in zero_patterns:
            if re.search(pattern, text_lower):
                improvements_found["zero_baseline"] = True
                evidence.append(f"Found zero baseline mention: {pattern}")
                break

        # Check for exact values/frequencies discussion
        value_patterns = [
            r'\bexact\b',
            r'\bnumber(s)?\b',
            r'\bvalue(s)?\b',
            r'\bcount(s)?\b',
            r'\bfrequenc(y|ies)\b',
            r'\bdata\s*label(s)?\b',
            r'\badd.*number\b'
        ]
        for pattern in value_patterns:
            if re.search(pattern, text_lower):
                improvements_found["exact_values"] = True
                evidence.append(f"Found exact values mention: {pattern}")
                break
                # Check for horizontal format discussion
        horizontal_patterns = [
            r'\bhorizontal\b',
            r'\brotate\b',
            r'\bflip\b',
            r'\borientation\b',
            r'\bcategory\s*label(s)?\b',
            r'\broom\s*for\s*label(s)?\b',
            r'\blabel.*space\b'
        ]
        for pattern in horizontal_patterns:
            if re.search(pattern, text_lower):
                improvements_found["horizontal_format"] = True
                evidence.append(f"Found horizontal format mention: {pattern}")
                break

        return {
            "improvements_found": improvements_found,
            "evidence": evidence if evidence else ["No clear improvement indicators found"],
            "all_present": all([
                improvements_found["horizontal_format"],
                improvements_found["dimensionality"],
                improvements_found["axis_labels"],
                improvements_found["zero_baseline"]
            ])
        }

    def grade_graph_improvement(self, student_answer: str, test_mode: bool = False):
        """
        Grade Graph Improvement Discussion question.

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
                feedback="Excellent analysis of graph improvements including horizontal format, dimensionality, axis labels, and zero baseline.",
                vibe="Student demonstrates strong understanding of data visualization best practices",
                additional_data={
                    "improvement_check": {
                        "improvements_found": {
                            "dimensionality": True,
                            "axis_labels": True,
                            "zero_baseline": True,
                            "exact_values": True,
                            "horizontal_format": True
                        },
                        "all_present": True,
                        "evidence": ["Test mode - all improvements mentioned"]
                    }
                }
            )

        # Check for mentioned improvements
        improvement_check = self.check_improvement_mentions(student_answer)

        # Build the grading prompt
        prompt = f"""You are grading a statistics homework using a **VIBE-BASED approach** - focusing on whether students demonstrate understanding of key graph improvement concepts.

**TASK DESCRIPTION:**
Students are shown a graph displaying the number of adults and children who prefer each type of soda (130 total surveyed). They must discuss ways to improve the graph.

The rubric includes FOUR REQUIRED improvements (20 points total):
1. The horizontal format is useful when you have many categories because there is more room for the category labels (Foster, p.39) - 5 points
2. The graph should be 2-dimensional - 5 points
3. Both (or only Y) axes should be labelled - 5 points
4. Start the Y axis from 0 rather than 20 - 5 points

BONUS RECOMMENDATION (not graded, but mentioned if absent):
- To add the exact frequency on the bar to understand the exact count without estimating from the axis could be recommended.

Total: 20 points

STUDENT ANSWER:
{student_answer}

**AUTOMATIC IMPROVEMENT DETECTION RESULT:**
Improvements Found: {improvement_check['improvements_found']}
All Key Improvements Present: {improvement_check['all_present']}
Evidence: {improvement_check['evidence']}

**VIBE-BASED GRADING APPROACH:**

For each component, use a generous interpretation:
- Focus on whether the student UNDERSTANDS the concept
- Accept varied phrasings and indirect mentions
- Credit partial understanding appropriately
- Don't require perfect technical terminology

**Component 1: Horizontal Format - VIBE (0-5 points)**
- Focus: Does student mention that the graph should use horizontal bars for better category label readability?
- Evidence: mentions "horizontal", "rotate", "flip", "category labels", "room for labels", "label space"
- Reference: "The horizontal format is useful when you have many categories because there is more room for the category labels (Foster, p.39)"
- Be generous: any discussion of orientation changes to improve label readability
- 0 points: No mention of horizontal format or label space issues
- 2-3 points: Indirect mention of label issues or graph orientation
- 4-5 points: Clear mention that horizontal format would help with category labels

**Component 2: 2-Dimensional Graph - VIBE (0-5 points)**
- Focus: Does student mention that the graph should be 2D (flat) rather than 3D?
- Evidence: mentions "2D", "3D", "dimension", "flat", "perspective", "depth"
- Be generous: any discussion of removing 3D effects or making it simpler/flatter
- 0 points: No mention of dimensionality issues
- 2-3 points: Indirect or unclear mention of simplifying the graph
- 4-5 points: Clear mention that graph should be 2D or avoid 3D effects

**Component 3: Axis Labels - VIBE (0-5 points)**
- Focus: Does student mention labeling the axes (especially Y-axis)?
- Evidence: mentions "axis", "axes", "label", "Y-axis", "X-axis"
- Be generous: any discussion of adding labels or clarifying what axes represent
- 0 points: No mention of axis labeling
- 2-3 points: Vague mention of labels or clarity
- 4-5 points: Clear mention of adding axis labels

**Component 4: Zero Baseline - VIBE (0-5 points)**
- Focus: Does student mention starting Y-axis from 0 instead of 20 or a higher value?
- Evidence: mentions "zero", "start at 0", "baseline", "from 0", "begin at 0"
- Be generous: any discussion of the axis not starting at appropriate value
- 0 points: No mention of baseline or starting point
- 2-3 points: Mentions scale issues but unclear about zero baseline
- 4-5 points: Clear mention of starting axis at 0

**BONUS RECOMMENDATION (Not Scored):**
- Check if student mentioned adding exact frequencies/values on bars
- This is a GOOD practice but NOT required for full credit
- If absent, mention it in feedback as "could be recommended"

**CRITICAL RULES:**
1. All components are VIBE-BASED - focus on understanding, not exact wording
2. Students don't need to use technical terms if the concept is clear
3. Credit creative or insightful improvements even if worded differently
4. Be generous with interpretation - if it's plausible they meant it, give credit
5. Don't penalize for NOT mentioning exact values on bars (it's bonus only)

**SCORING PROCESS:**
1. Score Component 1 (Horizontal Format) - VIBE: __/5
2. Score Component 2 (2D Graph) - VIBE: __/5
3. Score Component 3 (Axis Labels) - VIBE: __/5
4. Score Component 4 (Zero Baseline) - VIBE: __/5
5. Total = sum of four scores (max 20)

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- Acknowledges which improvements they identified
- Points out any missing key improvements specifically
- If they didn't mention exact values on bars, note: "Additionally, adding exact frequency labels on bars could be recommended to help readers understand exact counts without estimating from the axis."
- Explains why these improvements matter for data visualization
- Remains encouraging and constructive
- Suggests how they could strengthen their analysis

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
  "feedback": "<narrative explanation - which improvements they identified well, what's missing, mention exact values as optional recommendation if absent, why these improvements matter for effective data visualization>",
  "vibe": "<one-sentence overall impression of their understanding of data visualization principles>",
  "mentioned_exact_values": <true/false - did student mention exact frequency labels as bonus?>
}}"""

        # Use parent class method for API call and parsing
        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={"improvement_check": improvement_check}
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
        print("GRADING RESULTS - HW2_2 (VIBE MODE)")
        print("Graph Improvement Discussion")
        print("=" * 60)

        # Print component breakdown if available
        if 'component_1_score' in grading:
            print("\nCOMPONENT BREAKDOWN:")

            print(f"  Component 1 (Horizontal Format): {grading.get('component_1_score', 'N/A')}/5")
            if grading.get('component_1_explanation'):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (2D Graph): {grading.get('component_2_score', 'N/A')}/5")
            if grading.get('component_2_explanation'):
                print(f"    → {grading.get('component_2_explanation')}")

            print(f"  Component 3 (Axis Labels): {grading.get('component_3_score', 'N/A')}/5")
            if grading.get('component_3_explanation'):
                print(f"    → {grading.get('component_3_explanation')}")

            print(f"  Component 4 (Zero Baseline): {grading.get('component_4_score', 'N/A')}/5")
            if grading.get('component_4_explanation'):
                print(f"    → {grading.get('component_4_explanation')}")

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points', 'N/A')}/{grading.get('max_points', 20)}")
        print(f"PERCENTAGE: {grading.get('percentage', 'N/A')}%")

        # Show bonus recommendation status
        if 'mentioned_exact_values' in grading:
            if grading.get('mentioned_exact_values'):
                print("\n✓ Bonus: Student mentioned exact frequency labels (recommended)")
            else:
                print("\nℹ Bonus recommendation not mentioned: Adding exact frequency labels on bars")

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
    print("Welcome to the Homework AI Evaluator System!")
    print("=" * 60)

    # Initialize evaluator
    evaluator = HW2_2Evaluator()

    # Prompt user for student's answer
    print("=" * 60)
    print("HOMEWORK 2 - QUESTION 2_2 EVALUATOR")
    print("Graph Improvement Discussion")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION 2_2.")
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
    grading = evaluator.grade_graph_improvement(student_answer)

    # Display results
    evaluator.print_grading_results(grading)