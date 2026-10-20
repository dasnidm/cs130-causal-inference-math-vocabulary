"""Q4: a shared-treated experimental benchmark and three observational OLS models."""
import hashlib
import io
import json
from pathlib import Path
from urllib.request import urlopen

import pandas as pd
import statsmodels.api as sm

SOURCE = "6360a5247567c0ff632cd12aa2f6b3cfff92b2b6"
URL = f"https://raw.githubusercontent.com/jzangela/WSCdata/{SOURCE}/data-raw/df2200_cleaned.csv"
SHA256 = "cc67f453da430840a2262538ca8ba14cf2fc49bc10050225d570d649dca8cdaf"
RULE = "Observational point estimate lies inside the experimental benchmark's 95% t interval."
DEMOGRAPHICS = "female white black asian hisp married logAge income collegeS collegeM collegeD".split()
PRETESTS = DEMOGRAPHICS + ["mathPre", "vocabPre"]
FULL = PRETESTS + "calc logBooks mathLike big5O big5C big5E big5A big5N AMAS logBDI MCS GSES".split()
SPECS = {"1. Demographics": DEMOGRAPHICS, "2. Plus pretests": PRETESTS, "3. Full baseline": FULL}

raw = urlopen(URL, timeout=60).read()  # Always load public cloud data, including in the Gist.
assert hashlib.sha256(raw).hexdigest() == SHA256, "Upstream file changed."
d = pd.read_csv(io.BytesIO(raw))
assert d.shape == (2200, 33) and not d.isna().any().any()
assert set(d.mathGrp.unique()) == set(d.mathSel.unique()) == {0, 1}
assert d.groupby(["mathSel", "mathGrp"]).size().to_dict() == {(0, 0): 817, (0, 1): 776, (1, 0): 319, (1, 1): 288}
rct = d.loc[d.mathSel == 1]  # Experimental ATT: random assignment within math preference.
obs = d.loc[d.mathSel == d.mathGrp]  # Preference-concordant arms: shared treated, different controls.
assert rct.loc[rct.mathGrp == 1].index.equals(obs.loc[obs.mathGrp == 1].index)


def estimate(label, sample, covariates):
    x = sm.add_constant(sample[["mathGrp"] + covariates].astype(float))
    model = sm.OLS(sample.mathPost, x, missing="raise").fit(cov_type="nonrobust", use_t=True)
    assert model.df_resid == len(sample) - x.shape[1], "Rank-deficient model."
    low, high = model.conf_int(alpha=0.05).loc["mathGrp"]
    return {"Model": label, "N": int(model.nobs), "Estimate": model.params["mathGrp"],
            "SE": model.bse["mathGrp"], "CI_low": low, "CI_high": high}


benchmark = estimate("Experimental benchmark (ATT)", rct, [])
rows = [benchmark] + [estimate(name, obs, covariates) for name, covariates in SPECS.items()]
for row in rows:
    row["Abs_gap"] = abs(row["Estimate"] - benchmark["Estimate"])
    row["Reliable"] = "Benchmark" if row is benchmark else (
        "Yes" if benchmark["CI_low"] <= row["Estimate"] <= benchmark["CI_high"] else "No")
results = pd.DataFrame(rows)
arms = d.groupby(["mathSel", "mathGrp"]).agg(
    N=("mathPost", "size"), mathPre_mean=("mathPre", "mean"),
    vocabPre_mean=("vocabPre", "mean"), mathPost_mean=("mathPost", "mean"))
mean = lambda sample, group: float(sample.loc[sample.mathGrp == group, "mathPost"].mean())
naive = mean(obs, 1) - mean(obs, 0)
selection = mean(rct, 0) - mean(obs, 0)
assert abs((naive - benchmark["Estimate"]) - selection) < 1e-10

out = Path(__file__).resolve().parent / "results"
out.mkdir(exist_ok=True)
results.to_csv(out / "estimates.csv", index=False, float_format="%.10f")
arms.to_csv(out / "sample_summary.csv", float_format="%.10f")
metadata = {"data_url": URL, "sha256": SHA256, "rule": RULE,
            "plan_commit": "6c2cdb3e1ce35ce5071c343a72e28f44a26b66f8",
            "naive_observational_difference": naive, "unadjusted_selection_bias_term": selection,
            "specifications": {name: "mathPost ~ mathGrp + " + " + ".join(cov) for name, cov in SPECS.items()}}
(out / "details.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
header = "| Model | N | Estimate | Conventional SE | 95% CI | Absolute gap | Reliable |\n|---|---:|---:|---:|---|---:|---|\n"
table = header + "".join(
    f"| {r['Model']} | {r['N']} | {r['Estimate']:.4f} | {r['SE']:.4f} | "
    f"[{r['CI_low']:.4f}, {r['CI_high']:.4f}] | {r['Abs_gap']:.4f} | {r['Reliable']} |\n" for r in rows)
(out / "table.md").write_text(table, encoding="utf-8")
print(RULE + "\n\n" + table)
print(f"Naive observational difference: {naive:.4f}; unadjusted selection term: {selection:.4f}")
