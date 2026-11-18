# Statistical Analysis

`analyze_qcar_statistics.py` is the release exporter used to regenerate manuscript-ready Tables 5 and 7. It reads preserved raw CSVs from `data/` and writes to `results/statistics/`.

`legacy_original/analyze_qcar_statistics.py` is an unchanged earlier script retained for audit. Its old Table 5 exporter used absolute attack-minus-baseline differences and repeated stop-level misses across metric rows. Do not use it for the final manuscript tables.
