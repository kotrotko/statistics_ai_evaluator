from classwork.classwork_12 import CW12_4Evaluator

e = CW12_4Evaluator()

broken_text = """Table 2 presents the correlation matrix for the six variables.
Table 2
Correlation Matrix for Given Variables
Correlation matrix for given variables
Variable                scale10 scale11 scale12 scale13 scale14 scale15
1. scale10      Spearman's rho  —
        p-value —
2. scale11      Spearman's rho  0.296   —
        p-value .001    —
3. scale12      Spearman's rho  -0.453  -0.337  —
        p-value < .001  < .001  —
4. scale13      Spearman's rho  -0.522  -0.146  0.391   —
        p-value < .001  .117    < .001  —
5. scale14      Spearman's rho  0.386   0.298   -0.469  -0.242  —
        p-value < .001  .001    < .001  .009    —
6. scale15      Spearman's rho  -0.380  -0.125  0.303   0.298   -0.221  —
        p-value < .001  .180    < .001  .001    .017    —
Of the 15 pairwise correlations shown in Table 2, 13 are statistically significant at α = .05. The only two non-significant correlations are scale11–scale13 (ρ = -0.146, p = .117) and scale11–scale15 (ρ = -0.125, p = .180); all remaining pairs reach significance and are flagged acccorrelation analysis, the correlation coefficient itself serves as the effect size, since it conveys both the strength and the direction of the relationship in a single value.
The scatterplot is less informative for Spearman correlation because Spearman's rho is calculated on the ranked data rather than on the raw continuous values. Because these variables have a small number of repeated scale points, many observations overlap in the scatterplot, so the visual pattern becomes less clear than the numerical coefficient."""

for i in range(3):
    result = e.grade_cw12_4_answer(broken_text)
    print(f"Run {i+1}:", result.get("parse_error"))

