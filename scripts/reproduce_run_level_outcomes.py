from __future__ import annotations

import runpy
from pathlib import Path

import pandas as pd
from scipy.stats import fisher_exact


REPO_ROOT = Path(__file__).resolve().parents[1]
STATISTICS = runpy.run_path(str(REPO_ROOT / "src" / "statistics" / "analyze_qcar_statistics.py"))
OUTPUT_DIR = REPO_ROOT / "results" / "statistics"


def main() -> None:
    stop_level = pd.concat(
        [STATISTICS["load_pre_attack"](), STATISTICS["load_post_mitigation"]()],
        ignore_index=True,
    )
    rows = []
    for (condition, attack_pattern, run_id), group in stop_level.groupby(
        ["condition", "attack_pattern", "run_id"], sort=True
    ):
        unmet_stop_ids = sorted(
            int(stop_id) for stop_id in group.loc[group["missed_stop_outcome"] == 1, "stop_id"]
        )
        rows.append(
            {
                "condition": condition,
                "attack_pattern": attack_pattern,
                "run_id": int(run_id),
                "missed_any_required_stop": int(bool(unmet_stop_ids)),
                "unmet_stop_ids": ";".join(map(str, unmet_stop_ids)),
                "source_file": group["source_file"].iloc[0],
            }
        )
    outcomes = pd.DataFrame(rows)
    counts = outcomes.groupby("condition")["missed_any_required_stop"].agg(["sum", "count"])
    pre_failed = int(counts.loc["pre_mitigation_attack", "sum"])
    pre_total = int(counts.loc["pre_mitigation_attack", "count"])
    post_failed = int(counts.loc["post_mitigation", "sum"])
    post_total = int(counts.loc["post_mitigation", "count"])
    p_value = fisher_exact(
        [[pre_failed, pre_total - pre_failed], [post_failed, post_total - post_failed]],
        alternative="two-sided",
    ).pvalue
    if (pre_failed, pre_total, post_failed, post_total) != (8, 18, 0, 18):
        raise RuntimeError("Run-level outcomes do not reproduce the manuscript's Table 8")
    outcomes.to_csv(OUTPUT_DIR / "run_level_outcomes.csv", index=False)
    (OUTPUT_DIR / "run_level_outcomes_summary.txt").write_text(
        "Table 8 independent vehicle-run outcomes\n"
        f"Pre-mitigation: {pre_failed}/{pre_total} runs missed at least one required stop\n"
        f"Post-mitigation: {post_failed}/{post_total} runs missed at least one required stop\n"
        f"Two-sided Fisher exact p = {p_value:.4f}\n"
        "An unobserved later route requirement after an earlier termination is not a separate observed stop attempt.\n"
        "Source: raw pre- and post-mitigation CSV files; see run_level_outcomes.csv for run IDs.\n",
        encoding="utf-8",
    )
    print(f"Pre {pre_failed}/{pre_total}; post {post_failed}/{post_total}; Fisher p={p_value:.4f}")


if __name__ == "__main__":
    main()
