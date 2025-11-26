"""
任务5.2：Bins 政策 NPV 与敏感性分析
------------------------------------
基于车队节省与鼠患收益，估算10年期 NPV，并测试关键参数敏感性。
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EFFECT_FILE = PROJECT_ROOT / "outputs" / "task5_bins_policy_effects.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "task5_npv_sensitivity.csv"

CAPEX_PER_BIN = 400
NUM_BINS = 100000
ANNUAL_TRUCK_COST = 200000
PUBLIC_HEALTH_VALUE_PER_UNIT = 500
YEARS = 10


def npv(cashflows, discount_rate):
    return sum(cf / ((1 + discount_rate) ** t) for t, cf in enumerate(cashflows, start=1))


def main():
    df = pd.read_csv(EFFECT_FILE)
    avg_truck_saving = (df["trucks_needed_2x_est"] - df["trucks_after_bins"]).mean()
    avg_rat_reduction = (df["steady_rat"] - df["steady_rat_after_bins"]).mean()

    discount_rates = [0.05, 0.07, 0.1]
    efficiency_gain = [0.3, 0.4, 0.5]

    records = []
    for r in discount_rates:
        for eff in efficiency_gain:
            annual_saving = avg_truck_saving * eff * ANNUAL_TRUCK_COST
            annual_health = avg_rat_reduction * PUBLIC_HEALTH_VALUE_PER_UNIT
            cashflows = [annual_saving + annual_health] * YEARS
            npv_value = npv(cashflows, r) - CAPEX_PER_BIN * NUM_BINS
            records.append(
                {
                    "discount_rate": r,
                    "efficiency_gain": eff,
                    "npv": npv_value,
                }
            )

    out_df = pd.DataFrame(records)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(OUTPUT_FILE, index=False)
    print("已生成 NPV 敏感性分析：", OUTPUT_FILE)


if __name__ == "__main__":
    main()


