# Statistical Methods

## Continuous Measurements

Means, ranges, and sample standard deviations use valid numeric observations only; standard deviation uses `ddof=1`. Missing values are not imputed. Bootstrap 95% confidence intervals for the mean use percentile bounds from 10,000 resamples with NumPy random seed 42.

Pre/post continuous comparisons aggregate the 18 Lu2, Yang, and Lu3 trials in each condition and use two-sided Mann–Whitney U tests. Values are not rounded before testing.

## Missed Stop Outcomes

Missed-stop outcomes are vehicle-level final-stop outcomes. Because pre- and post-mitigation runs are independent rather than paired, the analysis uses two-sided Fisher exact tests for each stop location. The contingency table is `[[pre missed, pre valid], [post missed, post valid]]`.

## Table 5

Table 5 reports attack-specific, stop-specific values. Percentage change is:

```text
100 * (attack_mean - baseline_mean) / baseline_mean
```

The underlying means and inferential statistics are unchanged. Missed outcomes appear only on final-stop rows.

## Table 7

Table 7 aggregates Lu2, Yang, and Lu3, reports exact machine-readable p-values, and presents one stop-level Fisher result on each final-stop row. The first-detection rows use an em dash for missed outcomes and Fisher p-values.

## Reproduction

Run `python scripts/reproduce_statistics.py`. The release script is the corrected manuscript exporter. The unmodified earlier exporter is retained at `src/statistics/legacy_original/analyze_qcar_statistics.py` for provenance.
