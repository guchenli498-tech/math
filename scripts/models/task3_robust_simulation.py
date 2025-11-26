"""
任务3.2：鲁棒性仿真框架
--------------------------------
基于任务1/2的决策输出与场景配置，运行多次蒙特卡洛仿真，
评估服务缺口、MAD超限概率等指标。
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Dict, List

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from scripts.models.task1_frequency_optimizer import (
    enumerate_plans,
    load_district_data,
    DEFAULT_FEATURE_FILE,
)

SCENARIO_FILE = PROJECT_ROOT / "data" / "scenarios" / "task3_scenarios.json"
EQUITY_FILE = PROJECT_ROOT / "data" / "features" / "district_equity_targets.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "task3_robust_simulation.csv"

NUM_SIMULATIONS = 200


def load_scenarios():
    with open(SCENARIO_FILE, "r", encoding="utf-8") as f:
        scenarios = json.load(f)
    return scenarios


def sample_scenario(scenarios):
    probs = [s["probability"] for s in scenarios]
    choice = np.random.choice(len(scenarios), p=probs)
    return scenarios[choice]


def load_targets():
    df = pd.read_csv(EQUITY_FILE)
    return df.set_index("district")


def simulate_once(plan, scenarios, targets):
    scenario = sample_scenario(scenarios)
    total_deficit = 0.0
    ratios = []
    min_ratio = 1.0

    for district, freq in plan.freq_map.items():
        target_tons = targets.loc[district]["target_service_tons"]
        base_service = targets.loc[district]["baseline_service_tons"]
        service = (
            freq
            * base_service
            / 2
            * scenario["vehicle_availability"]
            / scenario["travel_time_multiplier"]
        )
        service *= 1 / scenario["waste_multiplier"]
        ratio = service / target_tons
        min_ratio = min(min_ratio, ratio)
        ratios.append(ratio)
        if service < target_tons:
            total_deficit += target_tons - service

    ratios = np.array(ratios)
    mad = np.mean(np.abs(ratios - np.mean(ratios)))

    return {
        "scenario": scenario["name"],
        "deficit_tons": total_deficit,
        "mad": mad,
        "min_service_ratio": min_ratio,
    }


def main():
    df = load_district_data(DEFAULT_FEATURE_FILE)
    plan = enumerate_plans(df, top_k=1)[0]
    scenarios = load_scenarios()
    targets = load_targets()

    records: List[Dict[str, float]] = []
    for _ in range(NUM_SIMULATIONS):
        records.append(simulate_once(plan, scenarios, targets))

    result_df = pd.DataFrame(records)
    result_df.to_csv(OUTPUT_FILE, index=False)
    print("仿真指标统计：")
    print(result_df.describe())


if __name__ == "__main__":
    main()


