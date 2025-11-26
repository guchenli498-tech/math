"""
任务2.1：公平性指标与目标服务量
-----------------------------------
基于任务1的需求估计和社会经济数据，为每个卫生区
定义目标服务频率、目标清运量以及公平性权重，供后续
效率 vs 公平模型使用。
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEMAND_FILE = PROJECT_ROOT / "data" / "features" / "district_demand_reestimated.csv"
SOCIO_FILE = PROJECT_ROOT / "data" / "features" / "district_features_enhanced.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "features" / "district_equity_targets.csv"

POVERTY_THRESHOLD = 18.0  # >= 18% 视为高贫困区
FAIRNESS_WEIGHT = 0.35  # 控制贫困区目标清运量增幅


def load_data() -> pd.DataFrame:
    if not DEMAND_FILE.exists() or not SOCIO_FILE.exists():
        raise FileNotFoundError("缺少需求或社会经济特征文件")

    demand_df = pd.read_csv(DEMAND_FILE)
    socio_df = pd.read_csv(SOCIO_FILE)[["district", "poverty_rate", "median_household_income"]]

    merged = demand_df.merge(socio_df, on="district", how="left", suffixes=("", "_soc"))
    if merged["poverty_rate"].isna().any():
        missing = merged[merged["poverty_rate"].isna()]["district"].tolist()
        raise ValueError(f"以下区域缺少贫困率：{missing}")
    return merged


def compute_targets(df: pd.DataFrame) -> pd.DataFrame:
    poverty = df["poverty_rate"]
    poverty_norm = (poverty - poverty.min()) / (poverty.max() - poverty.min())
    poverty_centered = poverty_norm - poverty_norm.mean()

    df["equity_weight"] = 1 + FAIRNESS_WEIGHT * poverty_centered
    df["equity_weight"] = df["equity_weight"].clip(lower=0.8, upper=1.3)

    df["target_pickups_per_week"] = np.where(poverty >= POVERTY_THRESHOLD, 3, 2)
    df["target_service_tons"] = df["weekly_waste_tons_est"] * df["equity_weight"]

    df["baseline_service_tons"] = df["weekly_waste_tons_est"]
    df["fairness_priority_score"] = 0.6 * poverty_norm + 0.4 * (
        df["equity_weight"] / df["equity_weight"].max()
    )
    return df


def main():
    parser = argparse.ArgumentParser(description="任务2.1：公平性指标生成")
    parser.add_argument("--output-file", type=Path, default=OUTPUT_FILE)
    args = parser.parse_args()

    df = load_data()
    df = compute_targets(df)
    df.to_csv(args.output_file, index=False)

    print("=== 公平性目标生成完成 ===")
    print(df[
        [
            "district",
            "poverty_rate",
            "target_pickups_per_week",
            "target_service_tons",
            "equity_weight",
            "fairness_priority_score",
        ]
    ].to_string(index=False))


if __name__ == "__main__":
    main()


