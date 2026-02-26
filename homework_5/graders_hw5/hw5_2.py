"""
hw5_2.py
Sampling Distribution - Effect of Sample Size Evaluator
Evaluation method name: grade_question_hw5_2_answer
"""

import re
import textwrap

from config import BaseEvaluator


class HW5_2Evaluator(BaseEvaluator):
    """
    Evaluator for Sampling Distribution - Effect of Sample Size Question.

    Inherits common functionality from BaseEvaluator.
    Contains only question-specific logic.
    """

    TASK_DESCRIPTION = "4. What effect does sample size have on the shape of a sampling distribution?"

    def __init__(self):
        """Initialize evaluator with API handler."""
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1500
        )

    def check_originality(self, student_answer: str) -> dict:
        """
        Heuristic check for likely AI-generated or copied text.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with originality flag and evidence
        """
        text_lower = student_answer.lower()
        ai_indicators = [
            r'as an ai language model',
            r'certainly[!,]? here',
            r'sure[!,]? here(?:\'s| is)',
            r'i(?:\'m| am) here to help',
            r'it(?:\'s| is) worth noting that',
            r'in conclusion,?\s+the sampling distribution',
            r'it is important to note that',
            r'in summary,?\s+(?:as|the|larger)',
            r'furthermore,?\s+(?:it|the|larger)',
            r'moreover,?\s+(?:it|the|larger)',
        ]

        flags = []
        for pattern in ai_indicators:
            if re.search(pattern, text_lower):
                flags.append(f"AI-language pattern detected: '{pattern}'")

        # Flag suspiciously long, perfectly structured answers with no personal voice
        word_count = len(student_answer.split())
        if word_count > 300 and len(flags) >= 2:
            flags.append("Unusually long and polished answer with multiple AI markers")

        return {
            "likely_ai_generated": len(flags) >= 2,
            "flags": flags if flags else ["No strong AI-generation signals detected"]
        }

    def check_formatting_elements(self, student_answer: str) -> dict:
        """
        Check if student includes the required task description.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with found elements and evidence
        """
        text_lower = student_answer.lower()
        task_lower = self.TASK_DESCRIPTION.lower()

        elements_found = {
            "task_description": False,
            "task_number_mentioned": False
        }
        evidence = []

        # Check for substantial match with the task description
        key_phrases = [
            r'what effect does sample size have',
            r'effect.*sample size.*sampling distribution',
            r'sample size.*shape.*sampling distribution',
            r'shape of a sampling distribution'
        ]
        for pattern in key_phrases:
            if re.search(pattern, text_lower):
                elements_found["task_description"] = True
                evidence.append(f"Task description phrase found: '{pattern}'")
                break

        # Check for question number
        if re.search(r'\b4[\.\):]', student_answer):
            elements_found["task_number_mentioned"] = True
            evidence.append("Question number '4.' is present")

        return {
            "elements_found": elements_found,
            "evidence": evidence if evidence else ["Task description not found"]
        }

    def check_content_elements(self, student_answer: str) -> dict:
        """
        Check whether the student's answer addresses normality and spread.

        Args:
            student_answer: The student's response text

        Returns:
            Dictionary with content flags and evidence
        """
        text_lower = student_answer.lower()

        content_found = {
            "mentions_normality": False,
            "explains_normality": False,
            "mentions_clt": False,
            "mentions_spread": False,
            "explains_spread": False,
            "mentions_clustering": False
        }
        evidence = []

        # Normality mentions
        normality_patterns = [
            r'normal(?:ly)?(?:\s+distribution)?',
            r'bell[\s-]?curve',
            r'bell[\s-]?shaped',
            r'approaches?\s+normal',
            r'normally\s+distributed'
        ]
        for pattern in normality_patterns:
            if re.search(pattern, text_lower):
                content_found["mentions_normality"] = True
                evidence.append(f"Normality mentioned: '{pattern}'")
                break

        # Normality explanation (not just mentioned)
        normality_explain_patterns = [
            r'as\s+(?:the\s+)?sample\s+size\s+(?:increases?|grows?|gets?\s+larger)',
            r'larger\s+sample\s+(?:size|sizes)',
            r'increase\s+in\s+sample\s+size',
            r'greater\s+(?:the\s+)?sample\s+size'
        ]
        for pattern in normality_explain_patterns:
            if re.search(pattern, text_lower) and content_found["mentions_normality"]:
                content_found["explains_normality"] = True
                evidence.append("Normality is linked to sample size increase — explanation present")
                break

        # Central Limit Theorem
        clt_patterns = [
            r'central\s+limit\s+theorem',
            r'\bclt\b'
        ]
        for pattern in clt_patterns:
            if re.search(pattern, text_lower):
                content_found["mentions_clt"] = True
                evidence.append("Central Limit Theorem explicitly mentioned")
                break

        # Spread/variability mentions
        spread_patterns = [
            r'narrow(?:er|s)?',
            r'standard\s+error',
            r'variabilit(?:y|ies)',
            r'spread(?:s|ing)?',
            r'taller',
            r'less\s+(?:variable|spread|variation)',
            r'smaller\s+(?:spread|variance|variability|standard)',
            r'decreases?\s+(?:in\s+)?(?:spread|variability|variation)'
        ]
        for pattern in spread_patterns:
            if re.search(pattern, text_lower):
                content_found["mentions_spread"] = True
                evidence.append(f"Spread/variability mentioned: '{pattern}'")
                break

        # Spread explanation (linked to sample size)
        if content_found["mentions_spread"]:
            spread_explain_patterns = [
                r'larger\s+sample.*narrow',
                r'narrow.*larger\s+sample',
                r'larger\s+sample.*(?:less|smaller)\s+(?:spread|variab)',
                r'sample\s+size.*(?:standard\s+error|variability|spread)',
                r'(?:standard\s+error|variability|spread).*sample\s+size'
            ]
            for pattern in spread_explain_patterns:
                if re.search(pattern, text_lower):
                    content_found["explains_spread"] = True
                    evidence.append("Spread is linked to sample size — explanation present")
                    break

        # Clustering around population mean
        clustering_patterns = [
            r'cluster(?:ed|s|ing)?\s+(?:closely\s+)?around',
            r'closer?\s+to\s+(?:the\s+)?(?:true\s+)?(?:population\s+)?mean',
            r'more\s+likely\s+to\s+be\s+(?:close|near|around)',
            r'centered?\s+(?:around|on|at)\s+(?:the\s+)?(?:population|true)?\s*mean',
            r'around\s+the\s+(?:true\s+)?population\s+mean'
        ]
        for pattern in clustering_patterns:
            if re.search(pattern, text_lower):
                content_found["mentions_clustering"] = True
                evidence.append("Clustering around population mean mentioned")
                break

        return {
            "content_found": content_found,
            "evidence": evidence if evidence else ["No relevant content elements detected"]
        }

    def grade_question_hw5_2_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade the student's answer to HW5 Question 2 (5_2).

        Args:
            student_answer: The student's response text
            test_mode: If True, return mock results without calling API

        Returns:
            Dictionary with component scores, feedback, and vibe
        """
        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_1_score": 1,
                    "component_2_score": 9,
                    "component_3_score": 9
                },
                max_points=20,
                feedback="Test mode feedback for sampling distribution question.",
                vibe="Test mode vibe assessment",
                additional_data={
                    "formatting_check": {
                        "elements_found": {
                            "task_description": True,
                            "task_number_mentioned": True
                        },
                        "evidence": ["Test mode - all elements present"]
                    },
                    "content_check": {
                        "content_found": {
                            "mentions_normality": True,
                            "explains_normality": True,
                            "mentions_clt": True,
                            "mentions_spread": True,
                            "explains_spread": True,
                            "mentions_clustering": True
                        },
                        "evidence": ["Test mode - all content elements present"]
                    }
                }
            )

        # --- Originality gate ---
        originality_check = self.check_originality(student_answer)
        if originality_check["likely_ai_generated"]:
            return {
                "component_1_score": 0,
                "component_1_explanation": "Originality concern — evaluation frozen.",
                "component_2_score": 0,
                "component_2_explanation": "Originality concern — evaluation frozen.",
                "component_3_score": 0,
                "component_3_explanation": "Originality concern — evaluation frozen.",
                "total_points": 0,
                "max_points": 20,
                "percentage": 0,
                "feedback": (
                    "Due to originality concern, your points are frozen. "
                    "You can get them back if you provide oral explanation for this paper."
                ),
                "vibe": "Possible AI-generated content detected; manual review recommended.",
                "originality_check": originality_check
            }

        formatting_check = self.check_formatting_elements(student_answer)
        content_check = self.check_content_elements(student_answer)

        prompt = f"""You are grading a statistics homework assignment about sampling distributions.

**TASK DESCRIPTION (5_2):**
{self.TASK_DESCRIPTION}

**RUBRIC (20 points total):**

**Component 1: Task Description (1 point)**
- 1 point: Task description is copied/included (exactly or very closely) before the answer
- 0 points: Task description is missing or significantly altered

**Component 2: Effect on Shape / Normality (9 points total)**
Use AI judgment for completeness and correctness; no strict formula required.

Scoring:
- 9 points: Clearly and fully explains that as sample size increases, the sampling distribution of sample means approaches a normal (bell-shaped) distribution, WITH reasoning or citation of the Central Limit Theorem
- 7–8 points: Clearly explains normality effect with good reasoning but minor gaps
- 5–6 points: Mentions normality and links it to sample size but explanation is thin or partially correct
- 3–4 points: Mentions normality but provides NO explanation or reasoning; or mentions CLT without connecting it to shape
- 1–2 points: Vaguely references shape without accuracy
- 0 points: Shape effect incorrect or not addressed at all

**Component 3: Effect on Spread / Variability (10 points total)**
Use AI judgment for completeness and correctness; no strict formula required.

Scoring:
- 10 points: Clearly explains BOTH that larger samples → narrower distribution (smaller variability / smaller standard error) AND that sample means cluster more closely around the true population mean, with good reasoning
- 6–9 points: Explains narrower distribution clearly but clustering mention is absent or weak; OR explains clustering well but narrower/spread language is missing
- 4–5 points: Mentions variability/spread decreasing but explanation is minimal or partially correct
- 1–3 points: Vaguely mentions spread without explaining direction or connection to sample size
- 0 points: Spread/variability effect incorrect or not addressed at all

**SCORING GUIDANCE EXAMPLE:**
An answer stating that the sampling distribution becomes more normal as sample size increases (CLT stated), and that larger samples produce narrower, taller distributions with means clustering around the population mean should receive 18–19 points depending on minor content-related inaccuracies.

**TYPICAL MISTAKES AND PENALTIES:**
- If Task Description (question text) is absent: Component 1 = 0 (feedback: "The Task Description is expected.")
- Discussing only normality but not spread, or vice versa: Deduct up to 9 points from the missing component
- A response that only lists conclusions without any explanation caps at 4 points per component

**STUDENT ANSWER:**
{student_answer}

**AUTOMATIC FORMATTING DETECTION:**
Elements Found: {formatting_check['elements_found']}
Evidence: {formatting_check['evidence']}

**AUTOMATIC CONTENT DETECTION:**
Content Found: {content_check['content_found']}
Evidence: {content_check['evidence']}

**SCORING PROCESS:**
1. Score Component 1 (Task Description): __/1
2. Score Component 2 (Normality/Shape): __/9
   - Consider: Is normality mentioned? Is it explained and linked to sample size? Is CLT cited?
3. Score Component 3 (Spread/Variability): __/9
   - Consider: Is narrower distribution mentioned? Is clustering around mean mentioned? Is there reasoning?
4. Total = sum of all three components (max 20)

**FEEDBACK STRUCTURE:**
Provide narrative feedback that:
- States whether the task description is present
- Evaluates how well the student explained the normality/shape effect
- Evaluates how well the student explained the spread/variability effect
- Points out any missing elements (CLT, clustering, standard error, etc.)
- Remains constructive and specific

Return your grading in this exact JSON format:
{{
  "component_1_score": <0-1>,
  "component_1_explanation": "<if score < 1: one sentence explaining what's missing; if score = 1 AND notable: brief praise; otherwise empty string>",
  "component_2_score": <0-9>,
  "component_2_explanation": "<REQUIRED: Always explain. State what normality/shape elements are present or missing, and why the score was assigned>",
  "component_3_score": <0-10>,
  "component_3_explanation": "<REQUIRED: Always explain. State what spread/variability elements are present or missing, and why the score was assigned>",
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage as number>,
  "feedback": "<narrative explanation covering: (1) task description presence, (2) quality of normality explanation, (3) quality of spread/variability explanation, (4) any missing elements>",
  "vibe": "<one-sentence assessment of the student's conceptual understanding and explanation quality>"
}}"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "formatting_check": formatting_check,
                "content_check": content_check,
                "originality_check": originality_check
            }
        )

        if "error" not in result:
            component_keys = [
                "component_1_score",
                "component_2_score",
                "component_3_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading: dict):
        """Pretty-print grading results to console."""
        print("=" * 60)
        print("GRADING RESULTS - HW5_2")
        print("Sampling Distribution - Effect of Sample Size")
        print("=" * 60)

        # Originality freeze notice
        if grading.get("total_points") == 0 and "originality" in grading.get("vibe", "").lower():
            print("\n⚠️  ORIGINALITY CONCERN DETECTED — POINTS FROZEN")
            print(grading.get("feedback", ""))
            return

        if "component_1_score" in grading:
            print("\nCOMPONENT BREAKDOWN:")
            print(f"  Component 1 (Task Description): {grading.get('component_1_score', 'N/A')}/1")
            if grading.get("component_1_explanation"):
                print(f"    → {grading.get('component_1_explanation')}")

            print(f"  Component 2 (Effect on Shape / Normality): {grading.get('component_2_score', 'N/A')}/9")
            if grading.get("component_2_explanation"):
                wrapped = textwrap.fill(
                    grading.get("component_2_explanation"),
                    width=54, initial_indent="    → ", subsequent_indent="      "
                )
                print(wrapped)

            print(f"  Component 3 (Effect on Spread / Variability): {grading.get('component_3_score', 'N/A')}/9")
            if grading.get("component_3_explanation"):
                wrapped = textwrap.fill(
                    grading.get("component_3_explanation"),
                    width=54, initial_indent="    → ", subsequent_indent="      "
                )
                print(wrapped)

            print(f"  {'─' * 40}")

        print(f"\nTOTAL SCORE: {grading.get('total_points', 'N/A')}/{grading.get('max_points', 20)}")
        print(f"PERCENTAGE: {grading.get('percentage', 'N/A')}%")

        print("\n" + "=" * 60)
        print("FEEDBACK:")
        print("=" * 60)
        feedback_text = grading.get("feedback", "No feedback available")
        print(textwrap.fill(feedback_text, width=60))

        print("\n" + "=" * 60)
        print("THE VIBE:")
        print("=" * 60)
        vibe_text = grading.get("vibe", "N/A")
        print(textwrap.fill(vibe_text, width=60))

        if "error" in grading:
            print("\n" + "=" * 60)
            print("ERROR:")
            print("=" * 60)
            print(grading.get("error"))
            if "raw_response" in grading:
                print("\nRaw Response:")
                print(grading["raw_response"][:500])


if __name__ == "__main__":
    print("Welcome to the Homework AI Evaluator System!")
    print("=" * 60)

    evaluator = HW5_2Evaluator()

    print("=" * 60)
    print("HOMEWORK 5 - QUESTION 5_2 EVALUATOR")
    print("Sampling Distribution - Effect of Sample Size")
    print("=" * 60)
    print("\nPlease enter the student's answer to QUESTION 5_2.")
    print("(Press Enter twice when finished, or type 'END' on a new line)\n")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
        if len(lines) >= 2 and lines[-1] == "" and lines[-2] == "":
            lines = lines[:-2]
            break

    student_answer = "\n".join(lines)

    if not student_answer.strip():
        print("\n❌ Error: No answer provided. Exiting.")
        exit(1)

    print("\n" + "=" * 60)
    print("EVALUATING...")
    print("=" * 60)

    grading = evaluator.grade_question_hw5_2_answer(student_answer)

    evaluator.print_grading_results(grading)


class HW5_1Evaluator:
    pass