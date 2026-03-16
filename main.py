"""
Main application for statistics grading system.
"""

from config.input_handler import InputHandler
from classwork.classwork_1.graders import Question1_1Evaluator, Question1_2Evaluator
from classwork.classwork_2.graders import Question2_1Evaluator, Question2_2Evaluator, Question2_3Evaluator
from classwork.classwork_2.graders.question2_4_evaluator import Question2_4Evaluator
from homework.homework_2.graders_hw2 import HW2_2Evaluator
from homework.homework_2.graders_hw2 import HW2_1Evaluator
from homework.homework_3.graders_hw3.hw3_1 import HW3_1Evaluator
from homework.homework_3.graders_hw3.hw3_2 import HW3_2Evaluator
from homework.homework_3.graders_hw3.hw3_3 import HW3_3Evaluator
from homework.homework_3.graders_hw3.hw3_4 import HW3_4Evaluator
from homework.homework_3.graders_hw3.hw3_5 import HW3_5Evaluator
from homework.homework_5 import HW5_1Evaluator
from homework.homework_5.graders_hw5.hw5_2 import HW5_2Evaluator
from homework.homework_5 import HW5_3Evaluator
from homework.homework_7.graders_hw7.hw7_1 import HW7_1Evaluator
from homework.homework_7.graders_hw7.hw7_2 import HW7_2Evaluator
from homework.homework_7.graders_hw7.hw7_3 import HW7_3Evaluator
from homework.homework_7.graders_hw7.hw7_4 import HW7_4Evaluator
from homework.homework_7.graders_hw7.hw7_5 import HW7_5Evaluator
from homework.homework_8.graders_hw8.hw8_1 import HW8_1Evaluator
# from classwork.classwork_7 import Question7_1Evaluator, Question7_2Evaluator, Question7_3Evaluator, Question7_4Evaluator, Question7_5Evaluator
from classwork.classwork_3.graders.question3_1_evaluator import Question3_1Evaluator
from classwork.classwork_3.graders.question3_2_evaluator import Question3_2Evaluator
from classwork.classwork_3.graders.question3_3_evaluator import Question3_3Evaluator
from classwork.classwork_4.graders.question4_1_evaluator import Question4_1Evaluator
from classwork.classwork_5.graders.question5_1_evaluator import Question5_1Evaluator
from classwork.classwork_5.graders.question5_2_evaluator import Question5_2Evaluator
from classwork.classwork_7 import (
    Question7_1Evaluator,
    Question7_2Evaluator,
    Question7_3Evaluator,
    Question7_4Evaluator,
    Question7_5Evaluator
)
from classwork.classwork_8.graders import (
    CW8_1Evaluator,
    CW8_2Evaluator,
    CW8_3Evaluator,
    CW8_4Evaluator,
    CW8_5Evaluator
)
from classwork.classwork_9 import (
    CW9_1Evaluator,
    CW9_2Evaluator,
    CW9_3Evaluator,
    CW9_4Evaluator,
    CW9_5Evaluator
)
from exams.midterm_v1.question_mid_v1_1 import QuestionMidV1_1Evaluator
from exams.midterm_v1.mid_v1_2 import MidV1_2Evaluator

_input_handler = InputHandler()

def run_evaluator(evaluator_class, question_name, question_description, grading_method, **kwargs):
    """
    Run evaluation for a student answer.

    Args:
        evaluator_class: Evaluator class to instantiate
        question_name: Display name of the question
        question_description: Brief description
        grading_method: Method name to call on evaluator
        **kwargs: Additional arguments for print_grading_results
    """
    # Create instances
    evaluator = evaluator_class()
    input_handler = InputHandler()

    # Collect student input
    student_answer = input_handler.collect_and_validate_input(
        question_name=question_name,
        question_description=question_description,
        min_length=10
    )

    if not student_answer:
        print("\n❌ No valid input provided.")
        return

    print("\n" + "=" * 60)
    print("EVALUATING...")
    print("=" * 60)

    grading = getattr(evaluator, grading_method)(student_answer)
    evaluator.print_grading_results(grading, **kwargs)


def main():

    evaluators = {
        "1_1": (Question1_1Evaluator, "QUESTION 1.1",
                "File Setup + Mean Formula with Equation Tools",
                "grade_question1_1_answer", {}),
        "1_2": (Question1_2Evaluator, "QUESTION 1.2",
                "Mean Calculation with JASP",
                "grade_question1_2_answer", {"mode": "real"}),
        "2_1": (Question2_1Evaluator, "QUESTION 2.1",
                "Frequencies + Cumulative Frequencies + Percentiles",
                "grade_frequencies_percentiles", {}),
        "2_2": (Question2_2Evaluator, "QUESTION 2.2",
                "APA Format + Diagram + Numbering + JASP",
                "grade_question2_2_answer", {}),
        "2_3": (Question2_3Evaluator, "QUESTION 2.3",
                "Excel Histogram + Figure Formatting + Chart Comparison",
                "grade_question2_3_answer", {}),
        "2_4": (Question2_4Evaluator, "QUESTION 2.4",
                "Radar Chart + Dataset Description + Circular Transformation",
                "grade_radar_chart", {}),
        "3_1": (Question3_1Evaluator, "QUESTION 3.1",
                "Central Tendency by Gender",
                "grade_question3_1_answer", {}),
        "3_2": (Question3_2Evaluator, "QUESTION 3.2",
                "Range, Variance, Standard Deviation (GPA & IQ)",
                "grade_variability", {}),
        "3_3": (Question3_3Evaluator, "QUESTION 3.3",
                "Distribution Plots with Density Curves by Gender",
                "grade_distribution_plots", {}),
        "4_1": (Question4_1Evaluator, "QUESTION 4.1",
                "Multiple Comparisons Error Probability",
                "grade_question4_1_answer", {}),
        "5_1": (Question5_1Evaluator, "QUESTION 5.1",
                "Central Limit Theorem - Standard Error True/False",
                "grade_question5_1_answer", {}),
        "5_2": (Question5_2Evaluator, "QUESTION 5.2",
                "Standard Error Calculation",
                "grade_question_hw5_2_answer", {}),
        "7_1": (Question7_1Evaluator, "QUESTION 7.1",
                "Hypothesis Testing - Problem Statement / RQ / Hypotheses / α df CV",
                "grade_question7_1_answer", {}),
        "7_2": (Question7_2Evaluator, "QUESTION 7.2",
                "Normality Check - Shapiro-Wilk / Table / Conclusion / Reasoning",
                "grade_question7_2_answer", {}),
        "7_3": (Question7_3Evaluator, "QUESTION 7.3",
                "Wilcoxon Signed Rank Test - Test Value / Approach / Table / Mean & Median",
                "grade_question7_3_answer", {}),
        "7_4": (Question7_4Evaluator, "QUESTION 7.4",
                "Wilcoxon Table / APA Formatting / Interpretation / Descriptive Plot",
                "grade_question7_4_answer", {}),
        "7_5": (Question7_5Evaluator, "QUESTION 7.5",
                "Output Description / Effect Size / Gender Context / Cultural Context",
                "grade_question7_5_answer", {}),
        "cw8_1": (CW8_1Evaluator, "CLASSWORK 8.1",
                  "Statistical Method Selection and Justification",
                  "grade_question_cw8_1_answer", {}),
        "cw8_2": (CW8_2Evaluator, "CLASSWORK 8.2",
                  "Normality Check - Method / Conclusion / Reasoning",
                  "grade_cw8_2_answer", {}),
        "cw8_3": (CW8_3Evaluator, "CLASSWORK 8.3",
                  "Hypothesis Testing Setup - Hypotheses / α / df / CV",
                  "grade_question_cw8_3_answer", {}),
        "cw8_4": (CW8_4Evaluator, "CLASSWORK 8.4",
                  "Means Comparison - Justification / Table / Inference / Effect Size / Plot",
                  "grade_cw8_4_answer",
                  {}),
        "cw8_5": (CW8_5Evaluator, "CLASSWORK 8.5",
                  "Summary - APA Result / Research Question Answer",
                  "grade_cw8_5_answer", {}),
        "cw9_1": (CW9_1Evaluator, "CLASSWORK 9.1",
                  "Statistical Method Selection and Justification",
                  "grade_question_cw9_1_answer", {}),
        "cw9_2": (CW9_2Evaluator, "CLASSWORK 9.2",
                  "Normality Check - Method / Normal Distribution / Reasoning",
                  "grade_question_cw9_2_answer", {}),
        "cw9_3": (CW9_3Evaluator, "CLASSWORK 9.3",
                  "Variance Homogeneity Check - Method / Homogenous Variance / Method Form Selection",
                  "grade_question_cw9_3_answer", {}),
        "cw9_4": (CW9_4Evaluator, "CLASSWORK 9.4",
                  "Hypothesis Testing Setup - Hypotheses / α / df / CV",
                  "grade_cw9_4_answer", {}),
        "cw9_5": (CW9_5Evaluator, "CLASSWORK 9.5",
                  "Statistical Analysis and Interpretation",
                  "grade_cw9_5_answer", {}),
        "hw2_1": (HW2_1Evaluator, "HOMEWORK 2.1",
                  "Pie Chart vs Bar Chart Discussion",
                  "grade_chart_comparison", {}),
        "hw2_2": (HW2_2Evaluator, "HOMEWORK 2.2",
                  "Graph Improvement Discussion",
                  "grade_graph_improvement", {}),
        "hw3_1": (HW3_1Evaluator, "HOMEWORK 3.1",
                  "Mean, Median, Mode Sensitivity Comparison",
                  "grade_sensitivity_comparison", {}),
        "hw3_2": (HW3_2Evaluator, "HOMEWORK 3.2",
                  "Data Sets Creation Evaluator - Mean, Median, Standard Deviation",
                  "grade_data_sets", {}),
        "hw3_3": (HW3_3Evaluator, "HOMEWORK 3.3",
                  "Histogram and Central Tendency Analysis Evaluator",
                  "grade_histogram_analysis", {}),
        "hw3_4": (HW3_4Evaluator, "HOMEWORK 3.4",
                  "Mean, Variance and Standard Deviation with Outlier Analysis Evaluator",
                  "grade_question_hw3_4_answer", {}),
        "hw3_5": (HW3_5Evaluator, "HOMEWORK 3.5",
                  "Mean, Variance and Standard Deviation with Outlier Analysis Evaluator",
                  "grade_question_hw3_5_answer", {}),
        "hw5_1": (HW5_1Evaluator, "HOMEWORK 5.1",
                  "Sampling Distributions: CLT and LLN",
                  "grade_question_hw5_1_answer", {}),
        "hw5_2": (HW5_2Evaluator, "HOMEWORK 5.2",
                  "Sampling Distribution - Effect of Sample Size",
                  "grade_question_hw5_2_answer", {}),
        "hw5_3": (HW5_3Evaluator, "HOMEWORK 5.3",
                  "Sampling Distribution and Z-Score Analysis",
                  "grade_question_hw5_3_answer", {}),
        "hw7_1": (HW7_1Evaluator, "HOMEWORK 7.1",
                  "What Does a Confidence Interval Represent?",
                  "grade_question_hw7_1_answer", {}),
        "hw7_2": (HW7_2Evaluator, "HOMEWORK 7.2",
                  "Confidence Interval Calculations Around Sample Mean",
                  "grade_question_hw7_2_answer", {}),
        "hw7_3": (HW7_3Evaluator, "HOMEWORK 7.3",
                  "One-Sample t-Test Hypothesis Testing (Two-Tailed)",
                  "grade_question_hw7_3_answer", {}),
        "hw7_4": (HW7_4Evaluator, "HOMEWORK 7.4",
                  "Hypothesis Testing Decision-Making",
                  "grade_question_hw7_4_answer", {}),
        "hw7_5": (HW7_5Evaluator, "HOMEWORK 7.5",
                  "One-Sample t-Test Hypothesis Testing (One-Tailed)",
                  "grade_question_hw7_5_answer", {}),
        "hw8_1": (HW8_1Evaluator, "HOMEWORK 8.1",
                  "Dependent-Samples T-Test Research Questions",
                  "grade_question_hw8_1_answer", {}),
        "mid_v1_1": (QuestionMidV1_1Evaluator,
                     "MIDTERM V1 - QUESTION 1",
                     "Manual Computations",
                     "grade_midterm_v1_q1", {}),
        "mid_v1_2": (MidV1_2Evaluator,
                     "MIDTERM V1 - QUESTION 2",
                     "Histogram Creation - Body/Tails Labeling & Distribution Shape",
                     "grade_midv1_question2_answer", {}),
    }

    while True:
        print("\n" + "=" * 60)
        print("STATISTICS AI EVALUATOR")
        print("=" * 60)
        print("Type 0 to exit")
        print("=" * 60)

        # 1. Get all keys from the dictionary (excluding '0' which is handled separately)
        # We sort them to keep the list predictable for the user
        available_options = ", ".join(evaluators.keys())

        # 2. Use an f-string to inject those keys into the prompt automatically
        prompt = f"Select an evaluator (0, {available_options}):\n"

        choice = input(prompt).strip()
        # choice = input(prompt).splitlines()[0].strip() TODO check and remove
        # sys.stdout.write(prompt)
        # sys.stdout.flush()
        # choice = sys.stdin.readline().strip()

        if choice == "0":
            print("\n Goodbye!")
            break

        if choice not in evaluators:
            print(f"\n❌ Invalid choice '{choice}'. Please try again: 0, {available_options}")
            continue

        evaluator_class, q_name, q_desc, method, extra_kwargs = evaluators[choice]
        run_evaluator(evaluator_class, q_name, q_desc, method, **extra_kwargs)

        choice_input = input("\nWould you like to evaluate another student? (y/n): ").strip().lower()

        # If the user just pressed Enter by mistake, 'choice_input' is empty.
        # This 'if' prevents the error message from showing for empty inputs.
        if not choice_input:
            continue

        if choice_input in ("y", "yes"):
            continue

        if choice_input in ("n", "no"):
            print("\n✓ Evaluation session complete. Thank you!")
            return

        print(f"❌ '{choice_input}' is not a valid choice. Please enter 'y' or 'n'.")


if __name__ == "__main__":
    main()
