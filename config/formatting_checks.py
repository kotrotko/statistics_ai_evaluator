"""
formatting_checks.py
Reusable formatting check functions for all evaluators.
"""

import re


def check_formatting_elements_type2(student_answer: str, pedagogical_markers: list) -> dict:
    """
    Check formatting elements in the student's answer.

    Args:
        student_answer: The student's response text
        pedagogical_markers: List of phrases unique to the task description

    Returns:
        Dictionary with elements_found (dict of bools) and evidence (list of str)
    """
    text_lower = student_answer.lower()

    elements_found = {
        "task_description": False,
        "autoformatting": False,
    }

    evidence = []

    # Key phrases that would only appear if the student copied the task description
    if any(marker in text_lower for marker in pedagogical_markers):
        elements_found["task_description"] = True
        evidence.append("Task description found")
    else:
        evidence.append("Task description NOT found")

    # autoformatting
    # catches bullet points: - item, • item, * item
    autoformat_violations = len(re.findall(r'^\s*[-•*]\s', student_answer, re.MULTILINE))
    print(f"DEBUG autoformat_violations: {autoformat_violations}")

    if autoformat_violations > 0:
        evidence.append("Autoformatting detected")
    else:
        elements_found["autoformatting"] = True
        evidence.append("No autoformatting detected")

    return {
        "elements_found": elements_found,
        "evidence": evidence
    }