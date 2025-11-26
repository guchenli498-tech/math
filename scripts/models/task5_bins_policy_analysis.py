"""
任务5.1：Bins 政策影响评估
--------------------------------
估算强制推广 Bins 对车队需求和鼠患稳态的影响。
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEMAND_FILE = PROJECT_ROOT / "data" / "features" / "district_demand_reestimated.csv"
RAT_FILE = PROJECT_ROOT / "outputs" / "task4_rat_simulation.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "task5_bins_policy_effects.csv"


def main():
    demand_df = pd.read_csv(DEMAND_FILE)
    rat_df = pd.read_csv(RAT_FILE)

    demand_df["bins_adoption"] = demand_df["buildings_1to9_units_ratio"] * 0.8
    baseline_exposure = 12
    demand_df["effective_exposure"] = baseline_exposure * (1 - demand_df["bins_adoption"] * 0.6)
    demand_df["trucks_after_bins"] = (
        demand_df["effective_exposure"] / baseline_exposure
    ) * demand_df["trucks_needed_2x_est"]

    merged = demand_df.merge(rat_df[["district", "steady_rat"]], on="district", how="left")
    merged["steady_rat_after_bins"] = merged["steady_rat"] * 0.6

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    merged[
        ["district", "trucks_needed_2x_est", "trucks_after_bins", "steady_rat", "steady_rat_after_bins"]
    ].to_csv(OUTPUT_FILE, index=False)
    print("已生成 Bins 政策影响数据：", OUTPUT_FILE)


if __name__ == "__main__":
    main()


