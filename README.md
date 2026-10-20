# CS130: Causal Inference with Math Training

One Python script compares an experimental benchmark with exactly three observational linear regressions. Data are downloaded from the original researchers' public, commit-pinned URL on every run. No local input data or credentials are needed.

## Run

Use Python 3.12 in a virtual environment:

```sh
python -m venv .venv
# Activate .venv, then:
python -m pip install -r requirements.txt
python analysis.py
```

The same analysis.py and requirements.txt run from the [public assignment Gist](https://gist.github.com/dasnidm/3faad783b934b4a6f4a8e7f5b238184c). The script prints the results and writes the four small files in results/ next to the script. An internet connection is required for the data download.

## Design

- Treatment: math training; active control: vocabulary training.
- Outcome: mathPost, the math post-test score.
- Original data: 2,200 participants, 33 variables, no missing values.
- Benchmark: random assignment within people who selected math (mathSel = 1), N = 607. This estimates the math-preference subgroup effect, the original study's experimental ATT comparison.
- Observational comparison: preference-concordant arms (mathSel = mathGrp), N = 1,105.
- Both comparisons use exactly the same 288 treated participants. Experimental controls number 319; observational controls number 817. The estimates overlap in treated observations and are not independent.

The definitions follow the original package documentation's "ATT math" and "QED math" examples. The full-sample ATE is a different estimand and is not substituted for this benchmark.

## Plan and models

[PLAN.md](PLAN.md) was committed and publicly pushed **before any assignment regressions were run**: [initial plan commit](https://github.com/dasnidm/cs130-causal-inference-math-vocabulary/commit/6c2cdb3e1ce35ce5071c343a72e28f44a26b66f8). Published documentation and example results had already been consulted; this is not a claim of blinded or independent preregistration.

The fixed agreement rule requires an observational point estimate to fall inside the benchmark's 95% Student-t confidence interval. This is an exercise-specific descriptive rule, not a formal equivalence test or proof of no bias.

All three observational specifications use the same sample and an intercept:

1. Eleven demographic covariates.
2. The same demographics plus math and vocabulary pre-tests.
3. All 25 baseline covariates, adding educational, math-specific and psychosocial measures.

See PLAN.md for the exact variable lists. All reported SEs are conventional non-robust OLS SEs. All CIs use the residual-degrees-of-freedom Student-t distribution. No post-treatment covariates or additional specification searches are used.

## Outputs

- [Table for writing the assignment](results/table.md): benchmark and exactly three observational estimates, SEs, CIs and the fixed classification.
- [Unrounded results](results/estimates.csv).
- [Four-arm counts and means](results/sample_summary.csv).
- [Source, exact formulas and decomposition numbers](results/details.json).

Independent matrix calculations verified all four estimates, conventional SEs and confidence intervals. These are analysis materials; the student's narrative answers are not included.

## Functional differences from the replication examples

This implementation fixes a reliability rule before fitting, uses a shared-treated ATT benchmark, fits exactly three nested observational specifications, and exports one comparison table with conventional standard errors, confidence intervals, and reliability classifications. It also reports the unadjusted selection-bias decomposition.

## Sources and attribution

- [Assigned dataset page](https://rctvsobs.org/dataset/math-vocabulary-wsc).
- [Original researchers' WSCdata repository](https://github.com/jzangela/WSCdata).
- [Pinned documentation and group definitions](https://github.com/jzangela/WSCdata/blob/6360a5247567c0ff632cd12aa2f6b3cfff92b2b6/R/WSCdata.R).
- [Pinned CSV](https://raw.githubusercontent.com/jzangela/WSCdata/6360a5247567c0ff632cd12aa2f6b3cfff92b2b6/data-raw/df2200_cleaned.csv).
- [Original data preparation](https://github.com/jzangela/WSCdata/blob/6360a5247567c0ff632cd12aa2f6b3cfff92b2b6/data-raw/WSCdata_prep.R) confirms that this CSV creates the package's WSCdata object.
- [Original data/package license](https://github.com/jzangela/WSCdata/blob/6360a5247567c0ff632cd12aa2f6b3cfff92b2b6/LICENSE.md). Data are not redistributed in this repository.

Keller, Bryan, Vivian C. Wong, Sangbaek Park, Jingru Zhang, Patrick Sheehan, and Peter M. Steiner. 2025. "A New Four-Arm Within-Study Comparison: Design, Implementation, and Data." Observational Studies 11(2): 153-188. https://muse.jhu.edu/pub/56/article/963647

The package documentation and data were inspected. The journal article full text was not obtained. The script was independently implemented with ChatGPT assistance using the documented design. Student review and the required per-question AI disclosure/chat link remain the student's responsibility.
