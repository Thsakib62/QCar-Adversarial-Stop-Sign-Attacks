from __future__ import annotations

import math
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact, mannwhitneyu


REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = REPO_ROOT / "results" / "statistics"
BOOTSTRAP_RESAMPLES = 10_000
BOOTSTRAP_SEED = 42
VALID_STOP_THRESHOLD_M = 0.8

BASELINE_FILE = REPO_ROOT / "data" / "baseline" / "nonattacked_30_runs_for_stats.csv"
PRE_ATTACK_FILE = REPO_ROOT / "data" / "pre_mitigation" / "Testbed Data - Attacked.csv"
POST_MITIGATION_FILE = REPO_ROOT / "data" / "post_mitigation" / "Mitigation_results.csv"
ADDITIONAL_POST_MITIGATION_FILE = REPO_ROOT / "data" / "additional_patterns" / "7_Mitigations.csv"

MAIN_PATTERNS = ["Lu2", "Yang", "Lu3"]
DISTANCE_METRICS = ["detection_distance_m", "final_stop_distance_m"]


def clean_numeric(value: object) -> float:
    if pd.isna(value):
        return np.nan
    text = str(value).strip()
    if not text or text in {"-", "NA", "N/A", "nan"}:
        return np.nan
    match = re.search(r"[-+]?\d*\.?\d+", text)
    return float(match.group(0)) if match else np.nan


def normalize_pattern(value: object) -> str:
    text = str(value).strip()
    aliases = {"Yang3": "Yang", "yang3": "Yang", "yang": "Yang", "lu2": "Lu2", "lu3": "Lu3"}
    return aliases.get(text, text)


def bootstrap_mean_ci(values: pd.Series | list[float]) -> tuple[float, float]:
    arr = pd.Series(values, dtype="float64").dropna().to_numpy()
    if len(arr) < 2:
        return np.nan, np.nan
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    samples = rng.choice(arr, size=(BOOTSTRAP_RESAMPLES, len(arr)), replace=True)
    means = samples.mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def mean_or_nan(values: pd.Series) -> float:
    values = pd.to_numeric(values, errors="coerce").dropna()
    return float(values.mean()) if len(values) else np.nan


def sd_or_nan(values: pd.Series) -> float:
    values = pd.to_numeric(values, errors="coerce").dropna()
    return float(values.std(ddof=1)) if len(values) >= 2 else np.nan


def range_text(values: pd.Series) -> str:
    values = pd.to_numeric(values, errors="coerce").dropna()
    if len(values) == 0:
        return "NA"
    return f"[{values.min():.3f}, {values.max():.3f}]"


def ci_text(lower: float, upper: float) -> str:
    if pd.isna(lower) or pd.isna(upper):
        return "NA"
    return f"[{lower:.3f}, {upper:.3f}]"


def missed_text(missed: int, total: int) -> str:
    return f"{missed}/{total}"


def is_missed_stop_outcome(final_stop_distance: float) -> int:
    return int(pd.isna(final_stop_distance) or final_stop_distance > VALID_STOP_THRESHOLD_M)


def load_baseline() -> pd.DataFrame:
    df = pd.read_csv(BASELINE_FILE)
    records: list[dict[str, object]] = []
    for _, row in df.iterrows():
        for stop_id in [1, 2, 3]:
            det = clean_numeric(row[f"Stop Sign {stop_id} Detection Distance (meters)"])
            final = clean_numeric(row[f"Stop Sign {stop_id} Final Stopping Distance (meters)"])
            track = clean_numeric(row[f"Stop Sign {stop_id} Tracking Count (in Frames)"])
            records.append(
                {
                    "condition": "baseline_clean",
                    "attack_pattern": "clean",
                    "run_id": int(clean_numeric(row["Experimental Run"])),
                    "stop_id": stop_id,
                    "detection_distance_m": det,
                    "final_stop_distance_m": final,
                    "tracking_count_frames": track,
                    "missed_stop_outcome": is_missed_stop_outcome(final),
                    "path_size_m": clean_numeric(row.get("Path Size (meters)", np.nan)),
                    "route_completion_time_s": np.nan,
                    "source_file": BASELINE_FILE.name,
                }
            )
    return pd.DataFrame.from_records(records)


def load_pre_attack() -> pd.DataFrame:
    df = pd.read_csv(PRE_ATTACK_FILE, dtype=str)
    df["Attacked Stop SIgn"] = df["Attacked Stop SIgn"].replace("", np.nan).ffill()
    df["attack_pattern"] = df["Attacked Stop SIgn"].map(normalize_pattern)

    records: list[dict[str, object]] = []
    for _, row in df.iterrows():
        for stop_id in [1, 2, 3]:
            det = clean_numeric(row[f"Stop Sign {stop_id} Detection Distance (meters)"])
            final = clean_numeric(row[f"Stop Sign {stop_id} Final Stopping Distance (meters)"])
            track = clean_numeric(row[f"Stop Sign {stop_id} Tracking Count (in Frames)"])
            records.append(
                {
                    "condition": "pre_mitigation_attack",
                    "attack_pattern": row["attack_pattern"],
                    "run_id": int(clean_numeric(row["Eerimental Run "])),
                    "stop_id": stop_id,
                    "detection_distance_m": det,
                    "final_stop_distance_m": final,
                    "tracking_count_frames": track,
                    "missed_stop_outcome": is_missed_stop_outcome(final),
                    "path_size_m": clean_numeric(row.get("Path Size (meters)", np.nan)),
                    "route_completion_time_s": clean_numeric(row.get("Time to Complete the path (seconds)", np.nan)),
                    "source_file": PRE_ATTACK_FILE.name,
                }
            )
    return pd.DataFrame.from_records(records)


def load_post_mitigation() -> pd.DataFrame:
    df = pd.read_csv(POST_MITIGATION_FILE, dtype=str)
    records: list[dict[str, object]] = []
    for _, row in df.iterrows():
        for stop_id in [1, 2, 3]:
            det = clean_numeric(row[f"Stop {stop_id} Detection"])
            final = clean_numeric(row[f"Stop {stop_id} Final Stop"])
            records.append(
                {
                    "condition": "post_mitigation",
                    "attack_pattern": normalize_pattern(row["Attack"]),
                    "run_id": int(clean_numeric(row["Run"])),
                    "stop_id": stop_id,
                    "detection_distance_m": det,
                    "final_stop_distance_m": final,
                    "tracking_count_frames": np.nan,
                    "missed_stop_outcome": is_missed_stop_outcome(final),
                    "path_size_m": np.nan,
                    "route_completion_time_s": np.nan,
                    "source_file": POST_MITIGATION_FILE.name,
                }
            )
    return pd.DataFrame.from_records(records)


def load_additional_post_mitigation() -> pd.DataFrame:
    if not ADDITIONAL_POST_MITIGATION_FILE.exists():
        return pd.DataFrame()

    df = pd.read_csv(ADDITIONAL_POST_MITIGATION_FILE, dtype=str)
    df["Attack"] = df["Attack"].replace("", np.nan).ffill()
    records: list[dict[str, object]] = []
    for _, row in df.iterrows():
        for stop_id in [1, 2, 3]:
            det = clean_numeric(row[f"S{stop_id} Detect"])
            final = clean_numeric(row[f"S{stop_id} Final"])
            records.append(
                {
                    "condition": "post_mitigation",
                    "attack_pattern": normalize_pattern(row["Attack"]),
                    "run_id": int(clean_numeric(row["Run"])),
                    "stop_id": stop_id,
                    "detection_distance_m": det,
                    "final_stop_distance_m": final,
                    "tracking_count_frames": np.nan,
                    "missed_stop_outcome": is_missed_stop_outcome(final),
                    "path_size_m": np.nan,
                    "route_completion_time_s": np.nan,
                    "source_file": ADDITIONAL_POST_MITIGATION_FILE.name,
                }
            )
    return pd.DataFrame.from_records(records)


def make_metric_long(stop_level: pd.DataFrame) -> pd.DataFrame:
    metric_cols = [
        "detection_distance_m",
        "final_stop_distance_m",
        "tracking_count_frames",
    ]
    id_cols = [
        "condition",
        "attack_pattern",
        "run_id",
        "stop_id",
        "missed_stop_outcome",
        "path_size_m",
        "route_completion_time_s",
        "source_file",
    ]
    long_df = stop_level.melt(
        id_vars=id_cols,
        value_vars=metric_cols,
        var_name="metric",
        value_name="value",
    )
    return long_df.sort_values(["condition", "attack_pattern", "run_id", "stop_id", "metric"])


def summarize_group(df: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for keys, group in df.groupby(group_cols, dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        key_data = dict(zip(group_cols, keys))
        values = pd.to_numeric(group["value"], errors="coerce").dropna()
        total_runs = group[["run_id"]].drop_duplicates().shape[0]
        missed_by_run_stop = group[["run_id", "stop_id", "missed_stop_outcome"]].drop_duplicates()
        missed_count = int(missed_by_run_stop["missed_stop_outcome"].sum())
        ci_low, ci_high = bootstrap_mean_ci(values)
        rows.append(
            {
                **key_data,
                "n_total": total_runs,
                "n_valid": int(values.shape[0]),
                "mean": mean_or_nan(values),
                "std_dev": sd_or_nan(values),
                "min": float(values.min()) if len(values) else np.nan,
                "max": float(values.max()) if len(values) else np.nan,
                "bootstrap_ci_95_lower": ci_low,
                "bootstrap_ci_95_upper": ci_high,
                "bootstrap_ci_note": "computed" if len(values) >= 2 else "NA: fewer than 2 valid numeric values",
                "missed_stop_outcomes": missed_count,
                "missed_stop_outcomes_text": missed_text(missed_count, total_runs),
            }
        )
    return pd.DataFrame(rows)


def baseline_summary(clean_long: pd.DataFrame) -> pd.DataFrame:
    distance = clean_long[
        (clean_long["condition"] == "baseline_clean")
        & (clean_long["metric"].isin(DISTANCE_METRICS))
    ]
    return summarize_group(distance, ["condition", "attack_pattern", "stop_id", "metric"])


def table5_summary(all_long: pd.DataFrame, baseline: pd.DataFrame) -> pd.DataFrame:
    pre = all_long[
        (all_long["condition"] == "pre_mitigation_attack")
        & (all_long["attack_pattern"].isin(MAIN_PATTERNS))
        & (all_long["metric"].isin(DISTANCE_METRICS))
    ]
    summary = summarize_group(pre, ["condition", "attack_pattern", "stop_id", "metric"])
    baseline_means = baseline[["stop_id", "metric", "mean"]].rename(columns={"mean": "baseline_clean_mean"})
    summary = summary.merge(baseline_means, on=["stop_id", "metric"], how="left")
    summary["attack_minus_baseline_mean"] = summary["mean"] - summary["baseline_clean_mean"]
    summary["percent_change_vs_baseline"] = (
        100 * summary["attack_minus_baseline_mean"] / summary["baseline_clean_mean"]
    )
    summary["attack_pattern"] = pd.Categorical(
        summary["attack_pattern"], categories=MAIN_PATTERNS, ordered=True
    )
    return summary.sort_values(["attack_pattern", "stop_id", "metric"])


def mannwhitney_p(pre_values: pd.Series, post_values: pd.Series) -> float:
    pre_valid = pd.to_numeric(pre_values, errors="coerce").dropna()
    post_valid = pd.to_numeric(post_values, errors="coerce").dropna()
    if len(pre_valid) < 2 or len(post_valid) < 2:
        return np.nan
    return float(mannwhitneyu(pre_valid, post_valid, alternative="two-sided").pvalue)


def table7_summary(stop_level: pd.DataFrame, baseline: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, object]] = []
    tests: list[dict[str, object]] = []
    main = stop_level[stop_level["attack_pattern"].isin(MAIN_PATTERNS)].copy()

    baseline_means = baseline.set_index(["stop_id", "metric"])["mean"].to_dict()

    for stop_id in [1, 2, 3]:
        for metric in DISTANCE_METRICS:
            pre = main[(main["condition"] == "pre_mitigation_attack") & (main["stop_id"] == stop_id)]
            post = main[(main["condition"] == "post_mitigation") & (main["stop_id"] == stop_id)]
            pre_values = pre[metric]
            post_values = post[metric]

            pre_ci_low, pre_ci_high = bootstrap_mean_ci(pre_values)
            post_ci_low, post_ci_high = bootstrap_mean_ci(post_values)
            pre_missed = int(pre[["attack_pattern", "run_id", "stop_id", "missed_stop_outcome"]].drop_duplicates()["missed_stop_outcome"].sum())
            post_missed = int(post[["attack_pattern", "run_id", "stop_id", "missed_stop_outcome"]].drop_duplicates()["missed_stop_outcome"].sum())
            pre_total = pre[["attack_pattern", "run_id"]].drop_duplicates().shape[0]
            post_total = post[["attack_pattern", "run_id"]].drop_duplicates().shape[0]
            table = [[pre_missed, pre_total - pre_missed], [post_missed, post_total - post_missed]]
            fisher_p = float(fisher_exact(table, alternative="two-sided").pvalue)
            reduction_pp = (pre_missed / pre_total - post_missed / post_total) * 100 if pre_total and post_total else np.nan
            mw_p = mannwhitney_p(pre_values, post_values)

            is_final_stop_row = metric == "final_stop_distance_m"
            row = {
                "stop_id": stop_id,
                "metric": metric,
                "baseline_clean_mean": baseline_means.get((stop_id, metric), np.nan),
                "pre_n_total": pre_total,
                "pre_n_valid": int(pd.to_numeric(pre_values, errors="coerce").dropna().shape[0]),
                "pre_mean": mean_or_nan(pre_values),
                "pre_std_dev": sd_or_nan(pre_values),
                "pre_ci_95_lower": pre_ci_low,
                "pre_ci_95_upper": pre_ci_high,
                "pre_range": range_text(pre_values),
                "pre_missed_stop_outcomes": pre_missed,
                "pre_missed_stop_outcomes_text": missed_text(pre_missed, pre_total),
                "post_n_total": post_total,
                "post_n_valid": int(pd.to_numeric(post_values, errors="coerce").dropna().shape[0]),
                "post_mean": mean_or_nan(post_values),
                "post_std_dev": sd_or_nan(post_values),
                "post_ci_95_lower": post_ci_low,
                "post_ci_95_upper": post_ci_high,
                "post_range": range_text(post_values),
                "post_missed_stop_outcomes": post_missed,
                "post_missed_stop_outcomes_text": missed_text(post_missed, post_total),
                "post_minus_pre_mean": mean_or_nan(post_values) - mean_or_nan(pre_values),
                "mannwhitneyu_p_value": mw_p,
                "fisher_exact_p_value": fisher_p if is_final_stop_row else np.nan,
                "absolute_missed_outcome_reduction_pp": reduction_pp if is_final_stop_row else np.nan,
            }
            rows.append(row)
            tests.append(
                {
                    "comparison": "pre_vs_post_main_designs",
                    "attack_pattern": "Lu2+Yang+Lu3",
                    "stop_id": stop_id,
                    "metric": metric,
                    "test": "Mann-Whitney U",
                    "p_value": mw_p,
                    "note": "Two-sided independent rank-sum test on valid numeric values.",
                }
            )
            if is_final_stop_row:
                tests.append(
                    {
                        "comparison": "pre_vs_post_main_designs",
                        "attack_pattern": "Lu2+Yang+Lu3",
                        "stop_id": stop_id,
                        "metric": "missed_stop_outcome",
                        "test": "Fisher exact",
                        "p_value": fisher_p,
                        "note": f"Two-sided Fisher exact test using [[{pre_missed}, {pre_total - pre_missed}], [{post_missed}, {post_total - post_missed}]].",
                    }
                )
    return pd.DataFrame(rows), pd.DataFrame(tests)


def build_additional_design_summary(stop_level: pd.DataFrame) -> pd.DataFrame:
    post = stop_level[stop_level["condition"] == "post_mitigation"].copy()
    additional = post[~post["attack_pattern"].isin(MAIN_PATTERNS)]
    if additional.empty:
        return pd.DataFrame()
    rows = []
    for pattern, group in additional.groupby("attack_pattern"):
        run_level = group.groupby("run_id", as_index=False).agg(
            missed_stop_outcomes=("missed_stop_outcome", "sum"),
            route_completion_time_s=("route_completion_time_s", "first"),
        )
        values = pd.to_numeric(run_level["route_completion_time_s"], errors="coerce").dropna()
        ci_low, ci_high = bootstrap_mean_ci(values)
        rows.append(
            {
                "attack_pattern": pattern,
                "n_runs": run_level.shape[0],
                "runs_with_any_missed_stop_outcome": int((run_level["missed_stop_outcomes"] > 0).sum()),
                "total_stop_level_missed_outcomes": int(run_level["missed_stop_outcomes"].sum()),
                "route_completion_mean_s": mean_or_nan(values),
                "route_completion_std_dev_s": sd_or_nan(values),
                "route_completion_ci_95_lower_s": ci_low,
                "route_completion_ci_95_upper_s": ci_high,
                "route_completion_range_s": range_text(values),
            }
        )
    return pd.DataFrame(rows)


def fmt(value: float, digits: int = 3) -> str:
    if pd.isna(value):
        return "NA"
    return f"{value:.{digits}f}"


def fmt_p(value: float) -> str:
    if pd.isna(value):
        return "NA"
    if value < 0.0001:
        return "<0.0001"
    return f"{value:.4f}"


def metric_name(metric: str) -> str:
    return {
        "detection_distance_m": "First detection",
        "final_stop_distance_m": "Final stopping distance",
    }.get(metric, metric)


def write_table5_text(table5: pd.DataFrame) -> str:
    lines = [
        "TABLE 5. Pre-mitigation attack summary for Lu2, Yang, and Lu3.",
        "",
        "Attack | Stop | Metric | n valid / total | Mean +/- SD | 95% bootstrap CI | Range | Change vs. baseline | Missed stop outcome",
        "---|---:|---|---|---|---|---|---:|---",
    ]
    for _, row in table5.iterrows():
        lines.append(
            f"{row['attack_pattern']} | {int(row['stop_id'])} | {metric_name(row['metric'])} | "
            f"{int(row['n_valid'])}/{int(row['n_total'])} | {fmt(row['mean'])} +/- {fmt(row['std_dev'])} | "
            f"{ci_text(row['bootstrap_ci_95_lower'], row['bootstrap_ci_95_upper'])} | "
            f"[{fmt(row['min'])}, {fmt(row['max'])}] | {fmt(row['percent_change_vs_baseline'], 1)}% | "
            f"{row['missed_stop_outcomes_text'] if row['metric'] == 'final_stop_distance_m' else '—'}"
        )
    lines.append("")
    lines.append(
        "Note: Statistics use valid numeric values only. NA indicates fewer than two valid values for SD or bootstrap CI. "
        "Change vs. baseline uses the corresponding 30-run clean-sign baseline mean. Missed stop outcomes are vehicle-level "
        "final-stop outcomes and are displayed only on final-stopping-distance rows."
    )
    return "\n".join(lines) + "\n"


def write_table7_text(table7: pd.DataFrame) -> str:
    lines = [
        "TABLE 7. Pre- and post-mitigation summary aggregated across Lu2, Yang, and Lu3.",
        "",
        "Fisher's exact test was used for missed stop outcomes because the pre- and post-mitigation runs were independent.",
        "",
        "Stop | Metric | Baseline mean | Pre n valid / total | Pre mean +/- SD | Pre 95% CI | Pre range | Post n valid / total | Post mean +/- SD | Post 95% CI | Post range | Post - pre | Mann-Whitney p | Missed stop outcome pre -> post | Fisher p | Reduction",
        "---:|---|---:|---|---|---|---|---|---|---|---|---:|---:|---|---:|---:",
    ]
    for _, row in table7.iterrows():
        lines.append(
            f"{int(row['stop_id'])} | {metric_name(row['metric'])} | {fmt(row['baseline_clean_mean'])} | "
            f"{int(row['pre_n_valid'])}/{int(row['pre_n_total'])} | {fmt(row['pre_mean'])} +/- {fmt(row['pre_std_dev'])} | "
            f"{ci_text(row['pre_ci_95_lower'], row['pre_ci_95_upper'])} | {row['pre_range']} | "
            f"{int(row['post_n_valid'])}/{int(row['post_n_total'])} | {fmt(row['post_mean'])} +/- {fmt(row['post_std_dev'])} | "
            f"{ci_text(row['post_ci_95_lower'], row['post_ci_95_upper'])} | {row['post_range']} | "
            f"{fmt(row['post_minus_pre_mean'])} | {fmt_p(row['mannwhitneyu_p_value'])} | "
            f"{row['pre_missed_stop_outcomes_text'] + ' -> ' + row['post_missed_stop_outcomes_text'] if row['metric'] == 'final_stop_distance_m' else '—'} | "
            f"{fmt_p(row['fisher_exact_p_value']) if row['metric'] == 'final_stop_distance_m' else '—'} | "
            f"{fmt(row['absolute_missed_outcome_reduction_pp'], 1) + ' pp' if row['metric'] == 'final_stop_distance_m' else '—'}"
        )
    lines.extend(
        [
            "",
            "Note: Pre/post values aggregate six independent runs each for Lu2, Yang, and Lu3 (18 total per condition). "
            "Missing values are not replaced with zero. Fisher results and missed outcomes are stop-level and appear only "
            "on final-stopping-distance rows.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_stats_paragraphs(table7: pd.DataFrame, additional: pd.DataFrame) -> str:
    final_rows = table7[table7["metric"] == "final_stop_distance_m"]
    total_pre_missed = int(final_rows["pre_missed_stop_outcomes"].sum())
    total_post_missed = int(final_rows["post_missed_stop_outcomes"].sum())
    total_pre = int(final_rows["pre_n_total"].sum())
    total_post = int(final_rows["post_n_total"].sum())
    lines = [
        "Across the 30 clean baseline runs, distance metrics were summarized using means, standard deviations, ranges, and 10,000-resample bootstrap 95% confidence intervals for the mean.",
        "",
        "For the three primary adversarial designs (Lu2, Yang, and Lu3), pre- and post-mitigation experiments were treated as independent groups because they used the same route and physical protocol but different detector/model configurations. Therefore, missed stop outcome counts were compared using two-sided Fisher exact tests rather than McNemar's test.",
        "",
        f"Aggregated across Lu2, Yang, and Lu3, pre-mitigation runs produced {total_pre_missed}/{total_pre} stop-level missed stop outcomes, compared with {total_post_missed}/{total_post} after mitigation. This corresponds to an absolute reduction of {((total_pre_missed / total_pre) - (total_post_missed / total_post)) * 100:.1f} percentage points in missed stop outcomes.",
        "",
        "For continuous distance metrics, two-sided Mann-Whitney U tests were used for valid numeric pre- versus post-mitigation values. P-values are reported descriptively and should not be overinterpreted given the small sample sizes.",
    ]
    if not additional.empty:
        lines.append("")
        if int(additional["total_stop_level_missed_outcomes"].sum()) == 0:
            lines.append(
                "The seven additional post-mitigation designs completed the route without missed stop outcomes across the available post-mitigation runs per additional printed design; these limited checks are not used to claim full generalization."
            )
        else:
            lines.append(
                "The seven additional post-mitigation designs were summarized separately as limited checks and are not used to claim full generalization."
            )
    else:
        lines.append("")
        lines.append("No run-level files for seven additional post-mitigation designs were found in the analysis directory; therefore, no generalization claim is made for additional printed designs in these outputs.")
    return "\n".join(lines) + "\n"


def write_notes(
    input_files: list[Path],
    stop_level: pd.DataFrame,
    missing_summary: pd.DataFrame,
    assumptions: list[str],
) -> str:
    mapping = [
        "nonattacked_30_runs_for_stats.csv -> condition=baseline_clean, attack_pattern=clean",
        "Testbed Data - Attacked.csv -> condition=pre_mitigation_attack, attack_pattern from forward-filled `Attacked Stop SIgn`; Yang3 normalized to Yang",
        "Mitigation_results.csv -> condition=post_mitigation, attack_pattern from `Attack`",
    ]
    if any(path.name == ADDITIONAL_POST_MITIGATION_FILE.name for path in input_files):
        mapping.append("7_Mitigations.csv -> condition=post_mitigation, attack_pattern from forward-filled `Attack`")
    counts = stop_level[["condition", "attack_pattern", "run_id"]].drop_duplicates().groupby(["condition", "attack_pattern"]).size()
    lines = ["INPUT FILES FOUND"]
    lines.extend(f"- {p.name}" for p in input_files)
    lines.extend(["", "INFERRED CONDITION/PATTERN MAPPING"])
    lines.extend(f"- {item}" for item in mapping)
    lines.extend(["", "ROW COUNTS PER CONDITION AND ATTACK PATTERN", counts.to_string(), "", "MISSING-VALUE SUMMARY"])
    lines.append(missing_summary.to_string(index=False))
    lines.extend(["", "ASSUMPTIONS MADE"])
    lines.extend(f"- {item}" for item in assumptions)
    return "\n".join(lines) + "\n"


def build_missing_summary(stop_level: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (condition, pattern), group in stop_level.groupby(["condition", "attack_pattern"]):
        rows.append(
            {
                "condition": condition,
                "attack_pattern": pattern,
                "rows_stop_level": group.shape[0],
                "missing_detection_distance": int(group["detection_distance_m"].isna().sum()),
                "missing_final_stop_distance": int(group["final_stop_distance_m"].isna().sum()),
                "missing_tracking_count": int(group["tracking_count_frames"].isna().sum()),
                "missed_stop_outcomes": int(group["missed_stop_outcome"].sum()),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    input_files = [BASELINE_FILE, PRE_ATTACK_FILE, POST_MITIGATION_FILE]
    if ADDITIONAL_POST_MITIGATION_FILE.exists():
        input_files.append(ADDITIONAL_POST_MITIGATION_FILE)
    print("INPUT FILES FOUND")
    for file in input_files:
        print(f"- {file.relative_to(REPO_ROOT).as_posix()}")

    baseline_stop = load_baseline()
    pre_stop = load_pre_attack()
    post_stop = load_post_mitigation()
    additional_post_stop = load_additional_post_mitigation()
    stop_level = pd.concat([baseline_stop, pre_stop, post_stop, additional_post_stop], ignore_index=True)
    long_df = make_metric_long(stop_level)

    assumptions = [
        "Blank attack-pattern cells in Testbed Data - Attacked.csv were forward-filled.",
        "Yang3 in the pre-mitigation file was normalized to Yang.",
        "Dash and footnote-marked values were parsed as missing or numeric values as appropriate; missing distances were not replaced with zero.",
        f"Vehicle-level final-stop missed_stop_outcome=1 when final stopping distance is missing or exceeds {VALID_STOP_THRESHOLD_M:.1f} m; a missing first-detection value alone is not counted as a missed stop outcome.",
        "Pre- and post-mitigation runs were treated as independent groups.",
        "Bootstrap confidence intervals used 10,000 resamples and random seed 42.",
        "Bootstrap confidence intervals marked NA have fewer than 2 valid numeric values.",
    ]
    if ADDITIONAL_POST_MITIGATION_FILE.exists():
        additional_counts = additional_post_stop[["attack_pattern", "run_id"]].drop_duplicates().groupby("attack_pattern").size()
        assumptions.append(
            "7_Mitigations.csv was treated as post_mitigation for seven additional printed designs; observed run counts were used as recorded: "
            + ", ".join(f"{pattern}={count}" for pattern, count in additional_counts.items())
            + "."
        )
        assumptions.append("7_Mitigations.csv does not contain route completion time; route completion summaries are therefore NA.")
    else:
        assumptions.append("No separate run-level files for seven additional post-mitigation designs were found in this directory.")

    missing_summary = build_missing_summary(stop_level)
    counts = stop_level[["condition", "attack_pattern", "run_id"]].drop_duplicates().groupby(["condition", "attack_pattern"]).size()

    print("\nINFERRED CONDITION/PATTERN MAPPING")
    print("- nonattacked_30_runs_for_stats.csv -> condition=baseline_clean, attack_pattern=clean")
    print("- Testbed Data - Attacked.csv -> condition=pre_mitigation_attack, attack_pattern from forward-filled `Attacked Stop SIgn`; Yang3 normalized to Yang")
    print("- Mitigation_results.csv -> condition=post_mitigation, attack_pattern from `Attack`")
    if ADDITIONAL_POST_MITIGATION_FILE.exists():
        print("- 7_Mitigations.csv -> condition=post_mitigation, attack_pattern from forward-filled `Attack`")
    print("\nROW COUNTS PER CONDITION AND ATTACK PATTERN")
    print(counts.to_string())
    print("\nMISSING-VALUE SUMMARY")
    print(missing_summary.to_string(index=False))
    print("\nASSUMPTIONS MADE")
    for assumption in assumptions:
        print(f"- {assumption}")

    baseline = baseline_summary(long_df)
    table5 = table5_summary(long_df, baseline)
    table7, tests = table7_summary(stop_level, baseline)
    additional = build_additional_design_summary(stop_level)

    long_df.to_csv(OUTPUT_DIR / "cleaned_long_format.csv", index=False, na_rep="NA")
    baseline.to_csv(OUTPUT_DIR / "baseline_summary.csv", index=False, na_rep="NA")
    table5.to_csv(OUTPUT_DIR / "table5_attack_summary.csv", index=False, na_rep="NA")
    table7.to_csv(OUTPUT_DIR / "table7_pre_post_summary.csv", index=False, na_rep="NA")
    tests.to_csv(OUTPUT_DIR / "statistical_tests.csv", index=False, na_rep="NA")

    additional_path = OUTPUT_DIR / "seven_design_post_mitigation_summary.csv"
    if not additional.empty:
        additional.to_csv(additional_path, index=False, na_rep="NA")
    elif additional_path.exists():
        additional_path.unlink()

    (OUTPUT_DIR / "manuscript_ready_table5.txt").write_text(write_table5_text(table5), encoding="utf-8")
    (OUTPUT_DIR / "manuscript_ready_table7.txt").write_text(write_table7_text(table7), encoding="utf-8")
    (OUTPUT_DIR / "manuscript_ready_stats_paragraphs.txt").write_text(
        write_stats_paragraphs(table7, additional),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "analysis_notes.txt").write_text(
        write_notes(input_files, stop_level, missing_summary, assumptions),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
