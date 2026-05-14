"""
Main application for statistics grading system.
"""

from config.input_handler import InputHandler

from classwork.classwork_1 import (
    CW1_1Evaluator,
    # CW1_2Evaluator,
    # CW1_3Evaluator,
    # CW1_4Evaluator,
    # CW1_5Evaluator
)
# from classwork.classwork_1.graders import Question1_1Evaluator, Question1_2Evaluator

from classwork.classwork_2 import (
    CW2_1Evaluator,
    # CW2_2Evaluator,
    # CW2_3Evaluator,
    # CW2_4Evaluator,
    # CW2_5Evaluator
)
from classwork.classwork_2.graders import Question2_2Evaluator, Question2_3Evaluator
from classwork.classwork_2.graders.question2_4_evaluator import Question2_4Evaluator

from classwork.classwork_3 import (
    CW3_1Evaluator,
    # CW3_2Evaluator,
    # CW3_3Evaluator,
    # CW3_4Evaluator,
    # CW3_5Evaluator
)

from classwork.classwork_4 import (
    CW4_1Evaluator,
    # CW4_2Evaluator,
    # CW4_3Evaluator,
    # CW4_4Evaluator,
    # CW4_5Evaluator
)

from classwork.classwork_5 import (
    CW5_1Evaluator,
    # CW5_2Evaluator,
    # CW5_3Evaluator,
    # CW5_4Evaluator,
    # CW5_5Evaluator
)

from classwork.classwork_7 import (
    CW7_1Evaluator,
    # CW7_2Evaluator,
    # CW7_3Evaluator,
    # CW7_4Evaluator,
    # CW7_5Evaluator
)

from classwork.classwork_8 import (
    CW8_1Evaluator,
    # CW8_2Evaluator,
    # CW8_3Evaluator,
    # CW8_4Evaluator,
    # CW8_5Evaluator
)

from classwork.classwork_9 import (
    CW9_1Evaluator,
    # CW9_2Evaluator,
    # CW9_3Evaluator,
    # CW9_4Evaluator,
    # CW9_5Evaluator
)
from classwork.classwork_10 import (
    CW10_1Evaluator,
    CW10_2Evaluator,
    CW10_3Evaluator,
    CW10_4Evaluator,
    CW10_5Evaluator
)
from classwork.classwork_12 import (
    CW12_1Evaluator,
    CW12_2Evaluator,
    CW12_3Evaluator,
    CW12_4Evaluator,
    CW12_5Evaluator
)
from classwork.classwork_13 import (
    CW13_1Evaluator,
    CW13_2Evaluator,
    CW13_3Evaluator,
    CW13_4Evaluator,
    CW13_5Evaluator
)
from classwork.classwork_14 import (
    CW14_1Evaluator,
    CW14_2Evaluator,
    CW14_3Evaluator,
    CW14_4Evaluator,
    CW14_5Evaluator
)
from classwork.classwork_15 import (
    CW15_1Evaluator,
    CW15_2Evaluator,
    CW15_3Evaluator,
    CW15_4Evaluator,
    CW15_5Evaluator
)

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
from homework.homework_9 import (
    HW9_1Evaluator,
    HW9_2Evaluator,
    HW9_3Evaluator,
)
from homework.homework_10 import (
    HW10_1Evaluator,
    HW10_2Evaluator,
    HW10_3Evaluator,
    HW10_4Evaluator,
    HW10_5Evaluator
)
from homework.homework_12 import (
    HW12_1Evaluator,
    HW12_2Evaluator,
    HW12_3Evaluator,
    HW12_4Evaluator,
    HW12_5Evaluator
)
from homework.homework_13 import (
    HW13_1Evaluator,
    HW13_2Evaluator,
    HW13_3Evaluator,
    HW13_4Evaluator,
    HW13_5Evaluator
)

from homework.homework_14 import (
    HW14_1Evaluator,
    HW14_2Evaluator,
    HW14_3Evaluator,
    HW14_4Evaluator,
    HW14_5Evaluator
)

from classwork.classwork_3.graders.question3_1_evaluator import Question3_1Evaluator
from classwork.classwork_3.graders.question3_2_evaluator import Question3_2Evaluator
from classwork.classwork_3.graders.question3_3_evaluator import Question3_3Evaluator
from classwork.classwork_4.graders.question4_1_evaluator import Question4_1Evaluator
from classwork.classwork_5.graders.question5_1_evaluator import Question5_1Evaluator
from classwork.classwork_5.graders.question5_2_evaluator import Question5_2Evaluator

from exams.midterm_v1.question_mid_v1_1 import QuestionMidV1_1Evaluator
from exams.midterm_v1.mid_v1_2 import MidV1_2Evaluator
from exams.fin_v1 import FIN_V1_1Evaluator
from exams.final_v1.fin_v1_2 import FIN_V1_2Evaluator

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
    evaluator = evaluator_class()
    input_handler = InputHandler()

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

        "cw1_1": (CW1_1Evaluator, "CLASSWORK 1.1",
                "General Skills: Mean Formula",
                "grade_question_cw1_1_answer", {}),
        # "1_2": (Question1_2Evaluator, "QUESTION 1.2",
        #         "Mean Calculation with JASP",
        #         "grade_question1_2_answer", {"mode": "real"}),
        "cw2_1": (CW2_1Evaluator, "CLASSWORK 2.1",
                "Frequencies + Cumulative Frequencies + Percentiles",
                "grade_question_cw2_1_answer", {}),
        "2_2": (Question2_2Evaluator, "QUESTION 2.2",
                "APA Format + Diagram + Numbering + JASP",
                "grade_question2_2_answer", {}),
        "2_3": (Question2_3Evaluator, "QUESTION 2.3",
                "Excel Histogram + Figure Formatting + Chart Comparison",
                "grade_question2_3_answer", {}),
        "2_4": (Question2_4Evaluator, "QUESTION 2.4",
                "Radar Chart + Dataset Description + Circular Transformation",
                "grade_radar_chart", {}),

        "cw3_1": (CW3_1Evaluator, "CLASSWORK 3.1",
                  "Mean, Median, Mode by Gender (GPA & IQ)",
                  "grade_question_cw3_1_answer", {}),

        "3_1": (Question3_1Evaluator, "QUESTION 3.1",
                "Central Tendency by Gender",
                "grade_question3_1_answer", {}),
        "3_2": (Question3_2Evaluator, "QUESTION 3.2",
                "Range, Variance, Standard Deviation (GPA & IQ)",
                "grade_variability", {}),
        "3_3": (Question3_3Evaluator, "QUESTION 3.3",
                "Distribution Plots with Density Curves by Gender",
                "grade_distribution_plots", {}),

        "cw4_1": (CW4_1Evaluator, "CLASSWORK 4.1",
                  "Mean, SD Table + Normal Distribution Figures for IQ and GPA",
                  "grade_question_cw4_1_answer", {}),

        "4_1": (Question4_1Evaluator, "QUESTION 4.1",
                "Multiple Comparisons Error Probability",
                "grade_question_cw4_1_answer", {}),

        "cw5_1": (CW5_1Evaluator, "CLASSWORK 5.1",
                  "Central Limit Theorem - Standard Error True/False Question",
                  "grade_question_cw5_1_answer", {}),

        "5_1": (Question5_1Evaluator, "QUESTION 5.1",
                "Central Limit Theorem - Standard Error True/False",
                "grade_question5_1_answer", {}),
        "5_2": (Question5_2Evaluator, "QUESTION 5.2",
                "Standard Error Calculation",
                "grade_question_hw5_2_answer", {}),
        "cw7_1": (CW7_1Evaluator, "QUESTION 7.1",
                "One Group T Test - Problem Statement / RQ / Hypotheses / α df CV",
                "grade_question7_1_answer", {}),
        # "7_2": (Question7_2Evaluator, "QUESTION 7.2",
        #         "Normality Check - Shapiro-Wilk / Table / Conclusion / Reasoning",
        #         "grade_question7_2_answer", {}),
        # "7_3": (Question7_3Evaluator, "QUESTION 7.3",
        #         "Wilcoxon Signed Rank Test - Test Value / Approach / Table / Mean & Median",
        #         "grade_question7_3_answer", {}),
        # "7_4": (Question7_4Evaluator, "QUESTION 7.4",
        #         "Wilcoxon Table / APA Formatting / Interpretation / Descriptive Plot",
        #         "grade_question7_4_answer", {}),
        # "7_5": (Question7_5Evaluator, "QUESTION 7.5",
        #         "Output Description / Effect Size / Gender Context / Cultural Context",
        #         "grade_question7_5_answer", {}),
        "cw8_1": (CW8_1Evaluator, "CLASSWORK 8.1",
                  "Statistical Method Selection and Justification",
                  "grade_question_cw8_1_answer", {}),
        # "cw8_2": (CW8_2Evaluator, "CLASSWORK 8.2",
        #           "Normality Check - Method / Conclusion / Reasoning",
        #           "grade_cw8_2_answer", {}),
        # "cw8_3": (CW8_3Evaluator, "CLASSWORK 8.3",
        #           "Hypothesis Testing Setup - Hypotheses / α / df / CV",
        #           "grade_question_cw8_3_answer", {}),
        # "cw8_4": (CW8_4Evaluator, "CLASSWORK 8.4",
        #           "Means Comparison - Justification / Table / Inference / Effect Size / Plot",
        #           "grade_cw8_4_answer", {}),
        # "cw8_5": (CW8_5Evaluator, "CLASSWORK 8.5",
        #           "Summary - APA Result / Research Question Answer",
        #           "grade_cw8_5_answer", {}),
        "cw9_1": (CW9_1Evaluator, "CLASSWORK 9.1",
                  "Problem statement, RQ, method, and justification",
                  "grade_question_cw9_1_answer", {}),
        # "cw9_2": (CW9_2Evaluator, "CLASSWORK 9.2",
        #           "Normality Check - Method / Normal Distribution / Reasoning",
        #           "grade_question_cw9_2_answer", {}),
        # "cw9_3": (CW9_3Evaluator, "CLASSWORK 9.3",
        #           "Variance Homogeneity Check - Method / Homogenous Variance / Method Form Selection",
        #           "grade_question_cw9_3_answer", {}),
        # "cw9_4": (CW9_4Evaluator, "CLASSWORK 9.4",
        #           "Hypothesis Testing Setup - Hypotheses / α / df / CV",
        #           "grade_cw9_4_answer", {}),
        # "cw9_5": (CW9_5Evaluator, "CLASSWORK 9.5",
        #           "Statistical Analysis and Interpretation",
        #           "grade_cw9_5_answer", {}),
        "cw10_1": (CW10_1Evaluator, "CLASSWORK 10.1",
                   "ANOVA Method Selection and Justification",
                   "grade_question_cw10_1_answer", {}),
        "cw10_2": (CW10_2Evaluator, "CLASSWORK 10.2",
                   "ANOVA Method Selection and Justification",
                   "grade_question_cw10_2_answer", {}),
        "cw10_3": (CW10_3Evaluator, "CLASSWORK 10.3",
                   "ANOVA Method Selection and Justification",
                   "grade_question_cw10_3_answer", {}),
        "cw10_4": (CW10_4Evaluator, "CLASSWORK 10.4",
                   "ANOVA Method Selection and Justification",
                   "grade_question_cw10_4_answer", {}),
        "cw10_5": (CW10_5Evaluator, "CLASSWORK 10.5",
                   "ANOVA Method Selection and Justification",
                   "grade_question_cw10_5_answer", {}),
        "cw12_1": (CW12_1Evaluator, "CLASSWORK 12.1",
                   "Correlation Method Selection and Justification",
                   "grade_question_cw12_1_answer", {}),
        "cw12_2": (CW12_2Evaluator, "CLASSWORK 12.2",
                   "Correlation Normality Check",
                   "grade_question_cw12_2_answer", {}),
        "cw12_3": (CW12_3Evaluator, "CLASSWORK 12.3",
                   "Correlation Hypothesis Testing Setup",
                   "grade_question_cw12_3_answer", {}),
        "cw12_4": (CW12_4Evaluator, "CLASSWORK 12.4",
                   "Correlation Hypothesis Testing",
                   "grade_question_cw12_4_answer", {}),
        "cw12_5": (CW12_5Evaluator, "CLASSWORK 12.5",
                   "Correlation Summary",
                   "grade_question_cw12_5_answer", {}),
        "cw13_1": (CW13_1Evaluator, "CLASSWORK 13.1",
                   "Linear Regression - Problem Statement and Research Question",
                   "grade_question_cw13_1_answer", {}),
        "cw13_2": (CW13_2Evaluator, "CLASSWORK 13.2",
                   "Linear Regression - Assumption Checks",
                   "grade_question_cw13_2_answer", {}),
        # "cw13_3": (CW13_3Evaluator, "CLASSWORK 13.3",
        #            "Linear Regression - Step System",
        #            "grade_question_cw13_3_answer", {}),
        "cw13_4": (CW13_4Evaluator, "CLASSWORK 13.4",
                   "Linear Regression - Equation and R²",
                   "grade_question_cw13_4_answer", {}),
        "cw13_5": (CW13_5Evaluator, "CLASSWORK 13.5",
                   "Linear Regression - Results and Answer to Research Question",
                   "grade_question_cw13_5_answer", {}),
        "cw14_1": (CW14_1Evaluator, "CLASSWORK 14.1",
                   "Chi Square - Problem Statement and Research Question",
                   "grade_question_cw14_1_answer", {}),
        "cw14_2": (CW14_2Evaluator, "CLASSWORK 14.2",
                   "Chi Square - Step System",
                   "grade_question_cw14_2_answer", {}),
        "cw14_3": (CW14_3Evaluator, "CLASSWORK 14.3",
                   "Chi Square - Test for Independence",
                   "grade_question_cw14_3_answer", {}),
        "cw14_4": (CW14_4Evaluator, "CLASSWORK 14.4",
                   "Chi Square - Cramer's V Effect Size",
                   "grade_question_cw14_4_answer", {}),
        "cw14_5": (CW14_5Evaluator, "CLASSWORK 14.5",
                   "Chi Square - Results and Answer to Research Question",
                   "grade_question_cw14_5_answer", {}),

        "cw15_1": (CW15_1Evaluator, "CLASSWORK 15.1",
                   "EFA - Initial Setup, Assumption Checks, and Model Fit",
                   "grade_question_cw15_1_answer", {}),
        "cw15_2": (CW15_2Evaluator, "CLASSWORK 15.2",
                   "EFA - Factor Creation and Rotation",
                   "grade_question_cw15_2_answer", {}),
        "cw15_3": (CW15_3Evaluator, "CLASSWORK 15.3",
                   "Communalities",
                   "grade_question_cw15_3_answer", {}),
        "cw15_4": (CW15_4Evaluator, "CLASSWORK 15.4",
                   "Plots",
                   "grade_question_cw15_4_answer", {}),
        "cw15_5": (CW15_5Evaluator, "CLASSWORK 15.5",
                   "Summary",
                   "grade_question_cw15_5_answer", {}),



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
        "hw9_1": (HW9_1Evaluator, "HOMEWORK 9.1",
                  "Independent Groups T-Test Research Questions",
                  "grade_hw9_1_answer", {}),
        "hw9_2": (HW9_2Evaluator, "HOMEWORK 9.2",
                  "Standard Error Calculation",
                  "grade_hw9_2_answer", {}),
        "hw9_3": (HW9_3Evaluator, "HOMEWORK 9.3",
                  "Standard Error Calculation",
                  "grade_hw9_3_answer", {}),
        "hw10_1": (HW10_1Evaluator, "HOMEWORK 10.1",
                   "Standard Error Calculation",
                   "grade_hw10_1_answer", {}),
        "hw10_2": (HW10_2Evaluator, "HOMEWORK 10.2",
                   "Standard Error Calculation",
                   "grade_hw10_2_answer", {}),
        "hw10_3": (HW10_3Evaluator, "HOMEWORK 10.3",
                   "Standard Error Calculation",
                   "grade_hw10_3_answer", {}),
        "hw10_4": (HW10_4Evaluator, "HOMEWORK 10.4",
                   "Standard Error Calculation",
                   "grade_hw10_4_answer", {}),
        "hw10_5": (HW10_5Evaluator, "HOMEWORK 10.5",
                   "Standard Error Calculation",
                   "grade_hw10_5_answer", {}),
        "hw12_1": (HW12_1Evaluator, "HOMEWORK 12.1",
                   "Three Characteristics of a Correlation Coefficient",
                   "grade_hw12_1_answer", {}),
        "hw12_2": (HW12_2Evaluator, "HOMEWORK 12.2",
                   "Data Visualization Importance",
                   "grade_hw12_2_answer", {}),
        "hw12_3": (HW12_3Evaluator, "HOMEWORK 12.3",
                   "Direction and Magnitude of Correlation Coefficients",
                   "grade_hw12_3_answer", {}),
        "hw12_4": (HW12_4Evaluator, "HOMEWORK 12.4",
                   "Correlation Matrix: Direction and Magnitude",
                   "grade_hw12_4_answer", {}),
        "hw12_5": (HW12_5Evaluator, "HOMEWORK 12.5",
                   "Correlation Hypothesis Testing",
                   "grade_hw12_5_answer", {}),
        "hw13_1": (HW13_1Evaluator, "HOMEWORK 13.1",
                   "What is a Residual?",
                   "grade_hw13_1_answer", {}),
        "hw13_2": (HW13_2Evaluator, "HOMEWORK 13.2",
                   "Two Parameters of the Line of Best Fit",
                   "grade_hw13_2_answer", {}),
        "hw13_3": (HW13_3Evaluator, "HOMEWORK 13.3",
                   "ANOVA Tables for Simple Linear Regression",
                   "grade_hw13_3_answer", {}),
        "hw13_4": (HW13_4Evaluator, "HOMEWORK 13.4",
                   "Predicting Scores Using Line of Best Fit",
                   "grade_hw13_4_answer", {}),
        "hw13_5": (HW13_5Evaluator, "HOMEWORK 13.5",
                   "Line of Best Fit and Hypothesis Testing",
                   "grade_hw13_5_answer", {}),

        "hw14_1": (HW14_1Evaluator, "HOMEWORK 14.1",
                   "What does a goodness-of-fit test assess?",
                   "grade_hw14_1_answer", {}),
        "hw14_2": (HW14_2Evaluator, "HOMEWORK 14.2",
                   "What does a test-for-independence assess",
                   "grade_hw14_2_answer", {}),
        "hw14_3": (HW14_3Evaluator, "HOMEWORK 14.3",
                   "Effect size for chi-square test",
                   "grade_hw14_3_answer", {}),
        "hw14_4": (HW14_4Evaluator, "HOMEWORK 14.4",
                   "Chi-Square Goodness-Of-Fit for Pizza",
                   "grade_hw14_4_answer", {}),
        "hw14_5": (HW14_5Evaluator, "HOMEWORK 14.5",
                   "Chi-Square for independence against discrimination",
                   "grade_hw14_5_answer", {}),


        "mid_v1_1": (QuestionMidV1_1Evaluator,
                     "MIDTERM V1 - QUESTION 1",
                     "Manual Computations",
                     "grade_midterm_v1_q1", {}),
        "mid_v1_2": (MidV1_2Evaluator,
                     "MIDTERM V1 - QUESTION 2",
                     "Histogram Creation - Body/Tails Labeling & Distribution Shape",
                     "grade_midv1_question2_answer", {}),

        "fin_v1_1": (FIN_V1_1Evaluator,
             "FINAL V1 - QUESTION 1",
             "Mean, Median, Symmetry, and Unimodality",
             "grade_question_fin_v1_answer", {}),

        "fin_v1_2": (FIN_V1_2Evaluator,
                "FINAL V1 - QUESTION 2",
                "Method and Hypotheses statement",
                "grade_question_fin_v1_2_answer", {}),
    }

    while True:
        print("\n" + "=" * 60)
        print("STATISTICS AI EVALUATOR")
        print("=" * 60)
        print("Type 0 to exit")
        print("=" * 60)

        available_options = ", ".join(evaluators.keys())
        prompt = f"Select an evaluator (0, {available_options}):\n"
        choice = input(prompt).strip()

        if choice == "0":
            print("\n Goodbye!")
            break

        if choice not in evaluators:
            print(f"\n❌ Invalid choice '{choice}'. Please try again: 0, {available_options}")
            continue

        evaluator_class, q_name, q_desc, method, extra_kwargs = evaluators[choice]
        run_evaluator(evaluator_class, q_name, q_desc, method, **extra_kwargs)

        choice_input = input("\nWould you like to evaluate another student? (y/n): ").strip().lower()

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