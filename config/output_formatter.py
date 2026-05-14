"""
Output formatter for displaying grading results.

This module provides utilities for consistently formatting and displaying
grading results across all evaluators.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime


class OutputFormatter:
    """
    Handles formatting and display of grading results.

    Provides methods for printing headers, sections, component breakdowns,
    and complete grading reports in a consistent format.
    """

    def __init__(self, default_width: int = 60):
        """
        Initialize the OutputFormatter.

        Args:
            default_width: Default width for formatted output
        """
        self.default_width = default_width

    def print_header(self, title: str, width: Optional[int] = None, char: str = "=") -> None:
        """
        Print a formatted header.

        Args:
            title: Header title text
            width: Total width of the header (uses default if None)
            char: Character to use for border

        Example:
            >>> formatter = OutputFormatter()
            >>> formatter.print_header("GRADING RESULTS")
            ============================================================
            GRADING RESULTS
            ============================================================
        """
        width = width or self.default_width
        print(char * width)
        print(title)
        print(char * width)

    def print_separator(self, width: Optional[int] = None, char: str = "─") -> None:
        """
        Print a separator line.

        Args:
            width: Width of the separator (uses default if None)
            char: Character to use
        """
        width = width or self.default_width
        print(f"  {char * (width - 2)}")

    def print_section(self, title: str, width: Optional[int] = None) -> None:
        """
        Print a section header.

        Args:
            title: Section title
            width: Total width (uses default if None)

        Example:
            >>> formatter = OutputFormatter()
            >>> formatter.print_section("COMPONENT BREAKDOWN")
        """
        width = width or self.default_width
        print("\n" + "=" * width)
        print(title)
        print("=" * width)

    def print_component_breakdown(self,
                                  grading: Dict[str, Any],
                                  component_labels: Dict[str, str],
                                  max_score: int = 5,
                                  component_types: Optional[Dict[str, str]] = None,
                                  width: Optional[int] = None) -> None:
        """
        Print component scores breakdown.

        Args:
            grading: Grading result dictionary
            component_labels: Dictionary mapping component keys to display labels
            max_score: Maximum score per component (default 5)
            component_types: Optional dictionary mapping component keys to types (STRICT/VIBE)
            width: Display width (uses default if None)

        Example:
            >>> formatter = OutputFormatter()
            >>> formatter.print_component_breakdown(
            ...     grading,
            ...     {"component_1_score": "Introduction with reference"},
            ...     max_score=5,
            ...     component_types={"component_1_score": "VIBE"}
            ... )
            COMPONENT BREAKDOWN:
              Introduction with reference [VIBE]: 5/5
                → Great explanation provided
        """
        width = width or self.default_width
        print("\nCOMPONENT BREAKDOWN:")

        for key, label in component_labels.items():
            score = grading.get(key, 'N/A')

            # Get component type if provided
            comp_type = ""
            if component_types and key in component_types:
                comp_type = f" [{component_types[key]}]"

            # print(f"  {label}{comp_type}: {score}/{max_score}")
            component_max = max_score[key] if isinstance(max_score, dict) else max_score
            print(f"  {label}{comp_type}: {score}/{component_max}")

            # Print explanation if present
            explanation_key = key.replace('_score', '_explanation')
            if explanation_key in grading and grading[explanation_key]:
                print(f"    → {grading[explanation_key]}")

        self.print_separator(width)

    def print_check_results(self,
                           grading: Dict[str, Any],
                           check_configs: List[Dict[str, Any]],
                           width: Optional[int] = None) -> None:
        """
        Print automatic check results (SD removal, extra statistics, etc.).

        Args:
            grading: Grading result dictionary
            check_configs: List of check configurations, each with:
                - check_key: Key in grading dict for check results
                - title: Display title
                - pass_key: Key indicating if check passed
                - pass_message: Message when check passes
                - fail_message: Message when check fails
                - evidence_key: Optional key for evidence
            width: Display width (uses default if None)

        Example:
            >>> formatter = OutputFormatter()
            >>> formatter.print_check_results(grading, [{
            ...     "check_key": "sd_check",
            ...     "title": "SD REMOVAL CHECK",
            ...     "pass_key": "sd_found",
            ...     "pass_message": "SD NOT FOUND - Properly Removed",
            ...     "fail_message": "SD FOUND - Not Removed",
            ...     "evidence_key": "evidence"
            ... }])
        """
        width = width or self.default_width

        for config in check_configs:
            check_result = grading.get(config['check_key'])
            if not check_result:
                continue

            print(f"\n{config['title']}:")

            # Determine pass/fail
            check_passed = not check_result.get(config['pass_key'], False)

            if check_passed:
                print(f"  ✅ {config['pass_message']}")
            else:
                print(f"  ❌ {config['fail_message']}")

            # Print evidence if available
            if 'evidence_key' in config and config['evidence_key'] in check_result:
                evidence = check_result[config['evidence_key']]
                print(f"  Evidence: {evidence}")

            # Print penalty if applicable
            if 'penalty' in check_result and check_result['penalty'] > 0:
                print(f"  Penalty: -{check_result['penalty']} point(s)")

            self.print_separator(width)

    def print_score_summary(self, grading: Dict[str, Any], width: Optional[int] = None) -> None:
        """
        Print total score summary.

        Args:
            grading: Grading result dictionary
            width: Display width (uses default if None)
        """
        width = width or self.default_width
        total = grading.get('total_points', 'N/A')
        max_points = grading.get('max_points', 'N/A')
        percentage = grading.get('percentage', 'N/A')

        print(f"\nTOTAL SCORE: {total}/{max_points}")
        print(f"PERCENTAGE: {percentage}%")

    def print_feedback(self, grading: Dict[str, Any], width: Optional[int] = None) -> None:
        """
        Print feedback section.

        Args:
            grading: Grading result dictionary
            width: Display width (uses default if None)
        """
        width = width or self.default_width
        self.print_section("FEEDBACK", width)
        feedback = grading.get('feedback', 'No feedback available')
        print(feedback)

    def print_vibe(self, grading: Dict[str, Any], width: Optional[int] = None) -> None:
        """
        Print vibe/overall impression section.

        Args:
            grading: Grading result dictionary
            width: Display width (uses default if None)
        """
        width = width or self.default_width
        self.print_section("THE VIBE", width)
        vibe = grading.get('vibe', 'N/A')
        print(vibe)

    def print_error(self, grading: Dict[str, Any], width: Optional[int] = None) -> None:
        """
        Print error information if grading failed.

        Args:
            grading: Grading result dictionary
            width: Display width (uses default if None)
        """
        width = width or self.default_width

        if 'error' not in grading:
            return

        self.print_section("ERROR", width)
        print(grading.get('error'))

        if 'error_message' in grading:
            print(f"\nDetails: {grading['error_message']}")

        if 'raw_response' in grading:
            print("\nRaw Response (first 500 chars):")
            print(grading['raw_response'][:500])

    def print_grading_results(self,
                             grading: Dict[str, Any],
                             question_name: str,
                             question_description: str,
                             component_labels: Dict[str, str],
                             max_score: int = 5,
                             component_types: Optional[Dict[str, str]] = None,
                             check_configs: Optional[List[Dict[str, Any]]] = None,
                             width: Optional[int] = None,
                             mode: str = "HYBRID") -> None:
        """
        Print complete grading results in a standardized format.

        This is the main method that combines all formatting utilities.

        Args:
            grading: Grading result dictionary
            question_name: Question identifier (e.g., "QUESTION 1_2")
            question_description: Brief description
            component_labels: Dictionary of component labels
            max_score: Maximum score per component (default 5)
            component_types: Optional dictionary of component types (STRICT/VIBE)
            check_configs: Optional list of check configurations
            width: Display width (uses default if None)
            mode: Grading mode (HYBRID, STRICT, VIBE)

        Example:
            >>> formatter = OutputFormatter()
            >>> formatter.print_grading_results(
            ...     grading=result,
            ...     question_name="QUESTION 1_2",
            ...     question_description="Mean Calculation with JASP",
            ...     component_labels={
            ...         "component_1_score": "Component 1 (Introduction + Reference)",
            ...         "component_2_score": "Component 2 (APA Numbering + Naming)"
            ...     },
            ...     max_score=5,
            ...     component_types={
            ...         "component_1_score": "VIBE",
            ...         "component_2_score": "STRICT"
            ...     }
            ... )
        """
        width = width or self.default_width

        self.print_header(f"GRADING RESULTS - {question_name} ({mode} MODE)", width)
        print(question_description)
        print("=" * width)

        # Print check results if provided
        if check_configs:
            self.print_check_results(grading, check_configs, width)

        # Print component breakdown
        if component_labels:
            self.print_component_breakdown(grading, component_labels, max_score, component_types, width)

        # Print score summary
        self.print_score_summary(grading, width)

        # Print feedback
        self.print_feedback(grading, width)

        # Print vibe
        self.print_vibe(grading, width)

        # Print error if present
        self.print_error(grading, width)

    def format_grading_report(self,
                             grading: Dict[str, Any],
                             student_id: str,
                             question_name: str,
                             include_timestamp: bool = True) -> str:
        """
        Format grading results as a text report.

        Useful for saving results to files or sending via email.

        Args:
            grading: Grading result dictionary
            student_id: Student identifier
            question_name: Question identifier
            include_timestamp: Whether to include timestamp

        Returns:
            Formatted report as string

        Example:
            >>> formatter = OutputFormatter()
            >>> report = formatter.format_grading_report(result, "student_123", "Q1_2")
            >>> with open("grades.txt", "w") as f:
            ...     f.write(report)
        """
        lines = []
        lines.append("=" * 60)
        lines.append(f"GRADING REPORT - {question_name}")
        lines.append(f"Student ID: {student_id}")

        if include_timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            lines.append(f"Graded on: {timestamp}")

        lines.append("=" * 60)
        lines.append("")

        # Score summary
        lines.append(f"Total Score: {grading.get('total_points', 'N/A')}/{grading.get('max_points', 'N/A')}")
        lines.append(f"Percentage: {grading.get('percentage', 'N/A')}%")
        lines.append("")

        # Feedback
        lines.append("FEEDBACK:")
        lines.append(grading.get('feedback', 'No feedback available'))
        lines.append("")

        # Vibe
        lines.append("OVERALL IMPRESSION:")
        lines.append(grading.get('vibe', 'N/A'))
        lines.append("")

        lines.append("=" * 60)

        return "\n".join(lines)

    def print_batch_summary(self,
                           results: List[Dict[str, Any]],
                           width: Optional[int] = None) -> None:
        """
        Print summary for batch grading results.

        Args:
            results: List of grading result dictionaries
            width: Display width (uses default if None)

        Example:
            >>> formatter = OutputFormatter()
            >>> formatter.print_batch_summary([result1, result2, result3])
            BATCH GRADING SUMMARY
            ============================================================
            Total Students: 3
            Average Score: 85.3%
            Highest Score: 95.0%
            Lowest Score: 75.0%
        """
        width = width or self.default_width

        self.print_header("BATCH GRADING SUMMARY", width)

        if not results:
            print("No results to display")
            return

        total_students = len(results)
        percentages = [r.get('percentage', 0) for r in results if 'percentage' in r]

        if percentages:
            avg_score = sum(percentages) / len(percentages)
            max_score = max(percentages)
            min_score = min(percentages)

            print(f"Total Students: {total_students}")
            print(f"Average Score: {avg_score:.1f}%")
            print(f"Highest Score: {max_score}%")
            print(f"Lowest Score: {min_score}%")
        else:
            print(f"Total Students: {total_students}")
            print("No valid scores found")

        print("=" * width)


# Backward compatibility wrapper functions
def print_grading_results(grading: Dict[str, Any],
                          question_name: str,
                          question_description: str,
                          component_labels: Dict[str, str],
                          max_score: int = 5,
                          component_types: Optional[Dict[str, str]] = None,
                          check_configs: Optional[List[Dict[str, Any]]] = None,
                          width: int = 60,
                          mode: str = "HYBRID") -> None:
    """
    Backward compatibility wrapper for print_grading_results.

    Creates an OutputFormatter instance and calls the method.
    """
    formatter = OutputFormatter(default_width=width)
    formatter.print_grading_results(
        grading=grading,
        question_name=question_name,
        question_description=question_description,
        component_labels=component_labels,
        max_score=max_score,
        component_types=component_types,
        check_configs=check_configs,
        width=width,
        mode=mode
    )


# Example usage and testing
if __name__ == "__main__":
    # Test with sample grading result
    sample_grading = {
        "component_1_score": 5,
        "component_1_explanation": "",
        "component_2_score": 4,
        "component_2_explanation": "Minor formatting issue with fraction placement",
        "component_3_score": 5,
        "component_3_explanation": "",
        "component_4_score": 5,
        "component_4_explanation": "",
        "total_points": 19,
        "max_points": 20,
        "percentage": 95.0,
        "feedback": "Excellent work! Clear explanations and proper formatting.",
        "vibe": "Student demonstrates strong understanding of statistical concepts",
        "sd_check": {
            "sd_found": False,
            "evidence": "No SD found - properly removed"
        }
    }

    print("Testing output_formatter.py (Class-based)...")
    print()

    # Create formatter instance
    formatter = OutputFormatter()

    formatter.print_grading_results(
        grading=sample_grading,
        question_name="TEST QUESTION",
        question_description="This is a test",
        component_labels={
            "component_1_score": "Component 1 (Accent - x̄)",
            "component_2_score": "Component 2 (Fraction - division)",
            "component_3_score": "Component 3 (Script - Σ, subscripts)",
            "component_4_score": "Component 4 (Radical - √)"
        },
        max_score=5,
        component_types={
            "component_1_score": "STRICT",
            "component_2_score": "STRICT",
            "component_3_score": "STRICT",
            "component_4_score": "STRICT"
        },
        check_configs=[{
            "check_key": "sd_check",
            "title": "SD REMOVAL CHECK",
            "pass_key": "sd_found",
            "pass_message": "SD NOT FOUND - Properly Removed",
            "fail_message": "SD FOUND - Not Removed",
            "evidence_key": "evidence"
        }]
    )

    print("\n\nTesting report formatting...")
    report = formatter.format_grading_report(sample_grading, "student_123", "Q1_1")
    print(report)