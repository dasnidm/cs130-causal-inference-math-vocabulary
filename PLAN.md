# Q4 analysis plan

Recorded before running any regression for this assignment. This is an AI-prepared analysis plan, not the student's written response or a claim of independent student work. Source documentation and its published example results were consulted before recording this plan.

## Question and estimand

Outcome: mathPost (math post-test points). Treatment: math training (mathGrp = 1); active control: vocabulary training (mathGrp = 0).

Target the average causal effect among people who selected math (mathSel = 1), the study's experimental ATT comparison. Do not confuse this with the ATE in all 2,200 participants.

- Experimental benchmark: mathSel = 1, comparing randomly assigned math with vocabulary (288 versus 319; N = 607).
- Observational sample: mathSel = mathGrp (288 math-selecting math trainees versus 817 vocabulary-selecting vocabulary trainees; N = 1,105).
- The 288 treated participants are identical in both comparisons. The experimental and observational estimates are therefore not independent.
- Follow the group construction in the original package documentation, R/WSCdata.R, examples "ATT math" and "QED math".

## Reliability rule fixed before fitting

Call an observational point estimate reliable for this exercise if it lies inside the experimental benchmark's two-sided 95% Student-t confidence interval, including the endpoints. Evaluate unrounded estimates. This allows for benchmark sampling uncertainty. It is a descriptive agreement rule, not a formal equivalence test or proof of no selection bias; it does not incorporate the observational estimate's uncertainty.

## Exactly three observational OLS specifications

All use the same observational sample, outcome, and treatment indicator; include an intercept. No specification selection or changes after seeing results.

1. Demographics: female, white, black, asian, hisp, married, logAge, income, collegeS, collegeM, collegeD.
2. Demographics plus pre-tests: specification 1 + mathPre + vocabPre.
3. Full baseline adjustment: specification 2 + calc + logBooks + mathLike + big5O + big5C + big5E + big5A + big5N + AMAS + logBDI + MCS + GSES.

Only pre-treatment covariates are included. Specification 1 controls broad demographic differences; specification 2 adds baseline achievement; specification 3 adds domain-specific and other measured predictors of preference and achievement. Do not add post-treatment measures, including MCSpost or vocabPost. Do not run other outcome or specification searches.

## Estimation and outputs

Use OLS with conventional non-robust standard errors (pooled homoskedastic residual variance, residual degrees of freedom). The benchmark is an intercept-plus-treatment OLS regression, equivalent to the experimental mean difference. Report Student-t 95% confidence intervals.

Create one table with the experimental benchmark and exactly three observational estimates, conventional SEs, CIs, N, absolute distance from the benchmark and the fixed reliability classification. Also record the four arm counts, baseline/outcome means, and the naive observational mean difference (computed as a difference in means, not an additional regression).

The acquired public CSV has 2,200 rows, 33 columns, and no missing values. Stop if the pinned file's hash, dimensions, binary coding, arm counts, or required completeness changes; do not silently change samples or specifications.

## Reproducible data source

Original researchers: https://github.com/jzangela/WSCdata
Source commit: 6360a5247567c0ff632cd12aa2f6b3cfff92b2b6
CSV: https://raw.githubusercontent.com/jzangela/WSCdata/6360a5247567c0ff632cd12aa2f6b3cfff92b2b6/data-raw/df2200_cleaned.csv
CSV SHA-256: cc67f453da430840a2262538ca8ba14cf2fc49bc10050225d570d649dca8cdaf
Original documentation: https://github.com/jzangela/WSCdata/blob/6360a5247567c0ff632cd12aa2f6b3cfff92b2b6/R/WSCdata.R
Dataset page: https://rctvsobs.org/dataset/math-vocabulary-wsc

Keller, Bryan, Vivian C. Wong, Sangbaek Park, Jingru Zhang, Patrick Sheehan, and Peter M. Steiner. 2025. "A New Four-Arm Within-Study Comparison: Design, Implementation, and Data." Observational Studies 11(2): 153-188. https://muse.jhu.edu/pub/56/article/963647

The primary package's source and documentation were read. The journal article full text was not obtained; do not claim to have read it. Public data remain with the original researchers and are downloaded by URL on every run.
