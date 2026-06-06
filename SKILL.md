# Code Edit Format Skill

# Rules
- STRICT: Do not refer to "frustration" or other psychological bugs in conversation.
- Suggest corrections in code only
- Include only relevant lines
- Every element in a separate field, ready for copy-pasting
- Location outside the field: Section name, method name, and minimal context enough for IDE Search
- Use BEFORE / AFTER format
- Do not remove or ignore existing comments; editing them according to the task is allowed but must be shown explicitly in BEFORE/AFTER
- Do not invent approaches, structures, or elements de novo
- Follow the example file as a pattern
- Module docstring must follow this exact 4-line scheme:
  - Line 1: file name (e.g. `cw2_3.py`)
  - Line 2: Classwork number and title (e.g. `Classwork 2: Distributions and graphs`)
  - Line 3: task content summary (e.g. `Excel Histogram + X-axis Labels + Bar Chart vs Histogram`)
  - Line 4: evaluation method name, following the pattern `def grade_question_cw<cw number>_<task number>_answer`
- Before suggesting edits, identify any content-specific inputs required by the pattern file (e.g. task description, model answer, rubric, scoring breakdown, classwork title) that are absent from the target file, and ask the user for them before producing any BEFORE/AFTER edits
- When writing a main.py registry entry, follow the Main Registry Skill
- When writing a new cw*.py file, follow the Evaluator File Skill

# Main Registry Skill

## Rules
- Ask for classwork number, task number, and task display description (docstring line 3 of the corresponding cw*.py)
- Produce:
  "cw[cw_number]_[task_number]": (CW[cw_number]_[task_number]Evaluator, "CLASSWORK [cw_number].[task_number]",
                                  "[task display description]",
                                  "grade_question_cw[cw_number]_[task_number]_answer", {}),

# Evaluator File Skill

## Rules
- Follow the cw2_3.py pattern
- Ask for classwork number, task number, classwork title, and task content summary before producing any edits
- File name: cw[cw_number]_[task_number].py
- Class name: CW[cw_number]_[task_number]Evaluator
- Method name: grade_question_cw[cw_number]_[task_number]_answer
- Docstring line 4: Evaluation method name: def grade_question_cw[cw_number]_[task_number]_answer