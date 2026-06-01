# Code Edit Format Skill

## Rules
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
  - Line 4: evaluation method name, following the pattern `def grade_question_cw<N>_<M>_answer`a pattern
- Before suggesting edits, identify any content-specific inputs required by the pattern file (e.g. task description, model answer, rubric, scoring breakdown, classwork title) that are absent from the target file, and ask the user for them before producing any BEFORE/AFTER edits