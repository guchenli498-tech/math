"""
任务一：纯效率频次枚举器
--------------------------------
在不考虑贫困率或公平性约束的情况下，遍历每个区的
2 次/周与 3 次/周组合，找出所需卡车数量最少的方案。
"""

from __future__ import annotations

import argparse
import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FEATURE_FILE = (
    PROJECT_ROOT / "data" / "features" / "district_demand_reestimated.csv"
)
SERVICE_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


@dataclass
class PlanResult:
    total_truck_days: int
    dedicated_trucks: int
    freq_map: Dict[str, int]


def load_district_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"找不到特征文件：{path}")
    df = pd.read_csv(path)
    required_cols = {
        "district",
        "trucks_needed_2x_est",
        "trucks_needed_3x_est",
    }
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"缺失必要列：{missing}")
    return df.sort_values("district").reset_index(drop=True)


def _truck_col(freq: int) -> str:
    if freq == 2:
        return "trucks_needed_2x_est"
    if freq == 3:
        return "trucks_needed_3x_est"
    raise ValueError("频次只能是 2 或 3")


def evaluate_plan(df: pd.DataFrame, freqs: Tuple[int, ...]) -> PlanResult:
    total_truck_days = 0
    dedicated = 0
    plan: Dict[str, int] = {}
    for idx, freq in enumerate(freqs):
        row = df.iloc[idx]
        col = _truck_col(freq)
        trucks = int(row[col])
        total_truck_days += trucks * freq
        dedicated += trucks
        plan[row["district"]] = freq
    return PlanResult(total_truck_days, dedicated, plan)


def enumerate_plans(df: pd.DataFrame, top_k: int = 5) -> List[PlanResult]:
    best_results: List[PlanResult] = []
    n = len(df)
    freq_choices = list(itertools.product([2, 3], repeat=n))

    for freqs in freq_choices:
        result = evaluate_plan(df, freqs)
        if not best_results:
            best_results.append(result)
            continue

        if result.total_truck_days < best_results[0].total_truck_days:
            best_results = [result]
        elif result.total_truck_days == best_results[0].total_truck_days:
            best_results.append(result)

    return best_results[:top_k]


def format_plan(plan: PlanResult) -> str:
    items = sorted(plan.freq_map.items())
    detail = ", ".join(f"{district}:{freq}x" for district, freq in items)
    return (
        f"总卡车日 {plan.total_truck_days}, 专属车队 {plan.dedicated_trucks} 辆 -> {detail}"
    )


def compute_shared_schedule(
    df: pd.DataFrame, plan: PlanResult
) -> Tuple[List[int], Dict[str, List[str]]]:
    day_loads = [0 for _ in SERVICE_DAYS]
    assignment: Dict[str, List[str]] = {}
    district_map = df.set_index("district")
    district_items = sorted(
        plan.freq_map.items(),
        key=lambda item: district_map.loc[item[0], _truck_col(item[1])],
        reverse=True,
    )

    for district, freq in district_items:
        row = district_map.loc[district]
        trucks = int(row[_truck_col(freq)])
        assignment[district] = []
        available_days = SERVICE_DAYS.copy()
        for _ in range(freq):
            candidates = [
                (day_idx, load)
                for day_idx, load in enumerate(day_loads)
                if SERVICE_DAYS[day_idx] in available_days
            ]
            if not candidates:
                candidates = list(enumerate(day_loads))
            day_idx = min(candidates, key=lambda x: x[1])[0]
            day_loads[day_idx] += trucks
            assignment[district].append(SERVICE_DAYS[day_idx])
            if SERVICE_DAYS[day_idx] in available_days:
                available_days.remove(SERVICE_DAYS[day_idx])

    return day_loads, assignment


def main():
    parser = argparse.ArgumentParser(description="任务一：频次枚举器")
    parser.add_argument(
        "--feature-file",
        type=Path,
        default=DEFAULT_FEATURE_FILE,
        help="包含区级特征的 CSV 路径",
    )
    args = parser.parse_args()

    df = load_district_data(args.feature_file)
    plans = enumerate_plans(df)

    print("=== 纯效率最优方案（可能存在多个）===")
    for idx, plan in enumerate(plans, start=1):
        print(f"[方案 {idx}] {format_plan(plan)}")
        shared_loads, assignment = compute_shared_schedule(df, plan)
        shared_peak = max(shared_loads)
        print(
            f"    共享后需要车队 {shared_peak} 辆（各区单独配备需 {plan.dedicated_trucks} 辆），"
            f"各日负载: "
            + ", ".join(
                f"{day}:{load}" for day, load in zip(SERVICE_DAYS, shared_loads)
            )
        )
        print(
            "    区域调度: "
            + "; ".join(
                f"{district}->{','.join(days)}"
                for district, days in assignment.items()
            )
        )


if __name__ == "__main__":
    main()


