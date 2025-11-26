"""
任务4.1：暴露时间与 Gi(t) 计算
--------------------------------
根据频率和 AM/PM 策略估算各区垃圾暴露时间，
并计算供鼠患模型使用的可获取垃圾量 Gi。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEMAND_FILE = PROJECT_ROOT / "data" / "features" / "district_demand_reestimated.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "features" / "district_exposure_estimates.csv"


@dataclass
class ExposureParams:
    am_window: float = 11  # 8pm 到次日7am
    pm_window: float = 13  # 6pm 到次日7am
    bins_reduction: float = 0.4  # 容器可获取量降低到40%


def main():
    df = pd.read_csv(DEMAND_FILE)
    params = ExposureParams()

    results = []
    for _, row in df.iterrows():
        district = row["district"]
        freq = 3 if district in {"MN01", "MN06", "MN11"} else 2
        strategy = "AM" if district in {"MN03", "MN04", "MN05", "MN06"} else "PM"
        bins_adoption = 0.5 if row["buildings_1to9_units_ratio"] > 0.7 else 0.3

        if strategy == "AM":
            exposure_hours = params.am_window
        else:
            exposure_hours = params.pm_window

        effective_exposure = exposure_hours * (1 - bins_adoption * (1 - params.bins_reduction))
        gi = row["weekly_waste_tons_est"] * (effective_exposure / 24) / freq

        results.append(
            {
                "district": district,
                "freq": freq,
                "strategy": strategy,
                "bins_adoption": bins_adoption,
                "exposure_hours": exposure_hours,
                "effective_exposure": effective_exposure,
                "gi_tons": gi,
            }
        )

    out_df = pd.DataFrame(results)
    out_df.to_csv(OUTPUT_FILE, index=False)
    print(f"已写入暴露时间估计：{OUTPUT_FILE}")


if __name__ == "__main__":
    main()


