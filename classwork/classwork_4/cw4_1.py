"""
cw4_1.py
Classwork 4: Normal Distribution And Probability
Mean, SD Table + Normal Distribution Figures for IQ and GPA
Evaluation method name: def grade_question_cw4_1_answer
"""

import re
from config import BaseEvaluator
from config.output_formatter import OutputFormatter


class CW4_1Evaluator(BaseEvaluator):
    """
    Evaluator for Classwork 4_1: Distributions and Graphs.
    """

    def __init__(self):
        super().__init__(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1400
        )
        self.formatter = OutputFormatter(default_width=60)

    def check_formatting_elements(self, student_answer: str) -> dict:
        """
        Check document-level formatting: title, task description, autoformatting.
        """
        text_lower = student_answer.lower()
        first_lines = student_answer[:200]

        elements_found = {
            "name": False,
            "title": False,
            "task_description": False,
            "autoformatting": False,
        }

        evidence = []

        # STEP 1 - Name (strict)
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

        # STEP 2 - Title (strict)
        title_patterns = [
            r'^\s*classwork\s*4',
            r'^\s*cw\s*4\b',
            r'^\s*class\s*work\s*(week\s*)?4',
            r'^\s*in.?class\s*4'
        ]

        for pattern in title_patterns:
            if re.search(pattern, first_lines, re.IGNORECASE | re.MULTILINE):
                elements_found["title"] = True
                evidence.append("Title found")
                break
        if not elements_found["title"]:
            evidence.append("Title NOT found")

        # STEP 3 — Task Description (strict)
        pedagogical_markers = [
            "distributions and graphs",
            "normal distribution",
            "mean and standard deviation",
            "histogram",
            "density curve",
        ]

        if any(marker in text_lower for marker in pedagogical_markers):
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
            evidence.append(
                f"Autoformatting detected: {autoformat_violations} bullets, {bold_violations} bold markers")

        return {
            "elements_found": elements_found,
            "evidence": evidence
        }

    def check_required_elements(self, student_answer: str) -> dict:
        """
        Check for presence of key content elements: table, figures, IQ, GPA, SD.
        """
        text_lower = student_answer.lower()

        checks = {
            "table_1": bool(re.search(r'\btable\s*1\b', text_lower)),
            "figure_1": bool(re.search(r'\bfigure\s*1\b', text_lower)),
            "figure_2": bool(re.search(r'\bfigure\s*2\b', text_lower)),
            "iq": bool(re.search(r'\biq\b', text_lower)),
            "gpa": bool(re.search(r'\bgpa\b', text_lower)),
            "mean": bool(re.search(r'\bmean\b', text_lower)),
            "std_deviation": bool(re.search(
                r'std\.?\s*deviation|standard\s*deviation', text_lower
            )),
            "histogram": bool(re.search(r'\bhistogram\b', text_lower)),
            "density": bool(re.search(r'\bdensity\b', text_lower)),
        }

        return {
            "checks": checks,
            "all_present": all(checks.values())
        }

    def grade_question_cw4_1_answer(self, student_answer: str, test_mode: bool = False):
        """
        Grade Classwork 4_1: Distributions and Graphs.
        """

        if test_mode:
            return self.create_mock_result(
                component_scores={
                    "component_0_score": 4,
                    "component_1_score": 6,
                    "component_2_score": 5,
                    "component_3_score": 5,
                },
                max_points=20,
                feedback="Excellent work with proper APA formatting, table, and both distribution figures.",
                vibe="Strong understanding of distributions and APA style",
                additional_data={"detection": "test mode"}
            )

        formatting_check = self.check_formatting_elements(student_answer)
        formatting_summary = formatting_check["elements_found"]
        element_check = self.check_required_elements(student_answer)

        formatting_block = f"""
HEADER DETECTION RESULTS (DO NOT RE-EVALUATE):

paper_title_present = {formatting_summary["title"]}
task_description_present = {formatting_summary["task_description"]}
no_autoformatting_present = {formatting_summary["autoformatting"]}

CONTENT DETECTION RESULTS (DO NOT RE-EVALUATE):
table_1_present = {element_check["checks"]["table_1"]}
figure_1_present = {element_check["checks"]["figure_1"]}
figure_2_present = {element_check["checks"]["figure_2"]}
iq_present = {element_check["checks"]["iq"]}
gpa_present = {element_check["checks"]["gpa"]}
mean_present = {element_check["checks"]["mean"]}
std_deviation_present = {element_check["checks"]["std_deviation"]}
histogram_present = {element_check["checks"]["histogram"]}
density_present = {element_check["checks"]["density"]}
"""

        prompt = f"""{formatting_block}

You are grading a statistics classwork assignment using a **HYBRID grading approach**.

TASK: Students must calculate mean and SD for IQ and GPA in JASP, present results
in an APA-formatted table, and draw normal distributions for both variables using
histograms and density curves, formatted as APA figures.

Total: 20 points.

STUDENT ANSWER:
{student_answer}

**IMPORTANT NOTES:**
- Students submit text descriptions since visual elements cannot be captured in text
- If student references a table or figure (e.g., "Table 1 presents...", "Figure 1 shows..."),
  ASSUME the visual exists in their actual document
- Do NOT penalize for missing visuals if they clearly reference and describe them
- Focus on whether correct elements are present and properly formatted

---

**Component 0: Document Formatting - STRICT (0-4 points)**
Award 1 point each for:
- Student name present in first two lines (two capitalized words): use LLM judgment
- Paper title present: use paper_title_present
- Task description copied in: use task_description_present
- No autoformatting: use no_autoformatting_present

---

**Component 1: Table 1 - STRICT (0-6 points)**

Table 1 formatting (0-4 points), award 1 point each for:
- Introductory phrase present (e.g., "Table 1 presents the mean and standard deviation...")
- Reference to table number in introductory phrase (e.g., "...in Table 1")
- Table number present (e.g., "Table 1")
- Table title present and descriptive (e.g., "Means and Standard Deviations of IQ and GPA")

Table 1 content (0-2 points):
- 2 points: Both IQ and GPA values present with both mean and SD reported correctly
- 1 point: Only one variable present, or one measure (mean OR SD) missing
- 0 points: Table content absent entirely

---

**Component 2: Figure 1 (IQ distribution) - STRICT (0-5 points)**

Figure 1 formatting (0-4 points), award 1 point each for:
- Introductory phrase present (e.g., "Figure 1 presents the normal distribution of IQ...")
- Reference to figure number in introductory phrase (e.g., "...in Figure 1")
- Figure number present (e.g., "Figure 1")
- Figure title present and descriptive (e.g., "Distribution of IQ")

Figure 1 content (0-1 point):
- 1 point: Figure 1 referenced or described (histogram and/or density curve for IQ)
- 0 points: Figure 1 absent entirely

---

**Component 3: Figure 2 (GPA distribution) - STRICT (0-5 points)**

Figure 2 formatting (0-4 points), award 1 point each for:
- Introductory phrase present (e.g., "Figure 2 presents the normal distribution of GPA...")
- Reference to figure number in introductory phrase (e.g., "...in Figure 2")
- Figure number present (e.g., "Figure 2")
- Figure title present and descriptive (e.g., "Distribution of GPA")

Figure 2 content (0-1 point):
- 1 point: Figure 2 referenced or described (histogram and/or density curve for GPA)
- 0 points: Figure 2 absent entirely

---

**CRITICAL RULES:**
1. Total must equal exactly 20 points maximum
2. Each component is STRICT - must meet requirements to earn points
3. Minor formatting issues are acceptable if the core requirement is met
4. Use detection results above for objective checks; use LLM judgment only for name

**SCORING PROCESS:**
1. Score Component 0 (Document formatting): __/4
2. Score Component 1 (Table 1): __/6
3. Score Component 2 (Figure 1 - IQ): __/5
4. Score Component 3 (Figure 2 - GPA): __/5
5. Total = sum of four scores

Return your grading in this exact JSON format:
{{
  "component_0_score": <0-4>,
  "component_0_explanation": "<if score < 4: one sentence explaining what is missing; if score = 4 AND extra good work: one sentence of praise; otherwise empty string>",
  "component_1_score": <0-6>,
  "component_1_explanation": "<if score < 6: one sentence explaining what is missing; if score = 6 AND extra good work: one sentence of praise; otherwise empty string>",
  "component_2_score": <0-5>,
  "component_2_explanation": "<if score < 5: one sentence explaining what is missing; if score = 5 AND extra good work: one sentence of praise; otherwise empty string>",
  "component_3_score": <0-5>,
  "component_3_explanation": "<if score < 5: one sentence explaining what is missing; if score = 5 AND extra good work: one sentence of praise; otherwise empty string>",
  "total_points": <sum of above, 0-20>,
  "max_points": 20,
  "percentage": <percentage>,
  "feedback": "<narrative explanation - what they did well, what is missing, how to improve>",
  "vibe": "<one-sentence overall impression of their work>"
}}"""

        result = self.grade_with_prompt(
            student_answer=student_answer,
            prompt=prompt,
            additional_checks={
                "formatting_check": formatting_check,
                "element_check": element_check
            }
        )

        if "error" not in result:
            component_keys = [
                "component_0_score",
                "component_1_score",
                "component_2_score",
                "component_3_score",
            ]
            result = self.validate_component_scores(result, component_keys, 20)

        return result

    def print_grading_results(self, grading):
        """
        Display grading results using OutputFormatter.

        Args:
            grading: Grading result dictionary
        """
        component_labels = {
            "component_0_score": "Component 0 (Document formatting)",
            "component_1_score": "Component 1 (Table 1 - formatting + content)",
            "component_2_score": "Component 2 (Figure 1 - IQ distribution)",
            "component_3_score": "Component 3 (Figure 2 - GPA distribution)"
        }

        component_types = {
            "component_0_score": "STRICT",
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT"
        }

        self.formatter.print_grading_results(
            grading=grading,
            question_name="QUESTION 4_1",
            question_description="Distributions and Graphs - Table and Figures",
            component_labels=component_labels,
            max_score=5,
            component_types=component_types,
            check_configs=None,
            width=60,
            mode="HYBRID"
        )