"""
区级垃圾量重估脚本
--------------------------------
基于题干给出的 NYC 日垃圾总量（24M lbs），假设曼哈顿占 20%，
结合鼠患投诉与小型住宅比例构造需求权重，将日/周垃圾量重新分配
给 12 个区，并计算 2x/3x 服务频次下的专属卡车需求。
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FEATURE_FILE = (
    PROJECT_ROOT / "data" / "features" / "district_features_with_mapped_complaints.csv"
)
OUTPUT_FILE = (
    PROJECT_ROOT / "data" / "features" / "district_demand_reestimated.csv"
)

NYC_DAILY_WASTE_LBS = 24_000_000  # 题干给定
MANHATTAN_SHARE = 0.20  # 可调参数
TRUCK_CAP_TONS = 12.0
TRIPS_PER_DAY = 2
DAYS_PER_WEEK = 6
TRUCK_WEEKLY_CAP_TONS = TRUCK_CAP_TONS * TRIPS_PER_DAY * DAYS_PER_WEEK


def load_features(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"找不到特征文件：{path}")
    df = pd.read_csv(path)
    required_cols = {
        "district",
        "rodent_complaints",
        "buildings_1to9_units_ratio",
    }
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"缺失必要列：{missing}")
    return df


def build_demand_weights(df: pd.DataFrame) -> pd.Series:
    rods = df["rodent_complaints"].fillna(0).astype(float)
    housing = df["buildings_1to9_units_ratio"].fillna(0.0).astype(float)

    if rods.max() == 0:
        rod_weight = np.ones(len(df))
    else:
        rod_weight = rods / rods.max()

    housing_weight = housing / housing.max() if housing.max() > 0 else np.ones(len(df))

    combined = 0.6 * rod_weight + 0.4 * housing_weight
    combined = combined.replace([np.inf, -np.inf], 0).fillna(0)
    if combined.sum() == 0:
        raise ValueError("需求权重全为零，无法分配垃圾量")
    return combined / combined.sum()


def compute_truck_need(weekly_tons: pd.Series, pickups_per_week: int) -> pd.Series:
    per_service_tons = weekly_tons / pickups_per_week
    min_trucks = per_service_tons / (TRUCK_CAP_TONS * TRIPS_PER_DAY)
    weekly_based = weekly_tons / TRUCK_WEEKLY_CAP_TONS
    return np.ceil(np.maximum(min_trucks, weekly_based)).astype(int)


def main():
    parser = argparse.ArgumentParser(description="区级垃圾量重估")
    parser.add_argument(
        "--feature-file",
        type=Path,
        default=DEFAULT_FEATURE_FILE,
        help="包含 rodent_complaints 和 housing 比例的 CSV",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=OUTPUT_FILE,
        help="输出带有重估字段的 CSV",
    )
    parser.add_argument(
        "--manhattan-share",
        type=float,
        default=MANHATTAN_SHARE,
        help="曼哈顿占纽约市垃圾总量的比例",
    )
    args = parser.parse_args()

    df = load_features(args.feature_file)
    weights = build_demand_weights(df)

    manhattan_daily_lbs = NYC_DAILY_WASTE_LBS * args.manhattan_share
    manhattan_weekly_tons = manhattan_daily_lbs * 7 / 2000

    df["weight"] = weights
    df["daily_waste_lbs_est"] = manhattan_daily_lbs * weights
    df["weekly_waste_tons_est"] = df["daily_waste_lbs_est"] * 7 / 2000

    df["trucks_needed_2x_est"] = compute_truck_need(df["weekly_waste_tons_est"], 2)
    df["trucks_needed_3x_est"] = compute_truck_need(df["weekly_waste_tons_est"], 3)

    df.to_csv(args.output_file, index=False)

    print("=== 重估完成 ===")
    print(f"曼哈顿日均垃圾量假设：{manhattan_daily_lbs:,.0f} lbs")
    print(f"总周垃圾量：{manhattan_weekly_tons:,.0f} 吨")
    print("\n各区概览：")
    print(
        df[
            [
                "district",
                "weight",
                "weekly_waste_tons_est",
                "trucks_needed_2x_est",
                "trucks_needed_3x_est",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()


