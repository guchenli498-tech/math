"""
任务3.3：鲁棒性策略对比
--------------------------------
在基准策略的基础上，加入：
1) 危机模式下放宽 MAD（重点保障）；
2) 垃圾激增时启用额外 20% 共享运力；
并通过仿真比较服务缺口与最差服务水平。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys_path = str(PROJECT_ROOT)
import sys

sys.path.append(sys_path)

from scripts.models.task1_frequency_optimizer import (
    enumerate_plans,
    load_district_data,
    DEFAULT_FEATURE_FILE,
)

SCENARIO_FILE = PROJECT_ROOT / "data" / "scenarios" / "task3_scenarios.json"
EQUITY_FILE = PROJECT_ROOT / "data" / "features" / "district_equity_targets.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "task3_resilience_comparison.csv"

NUM_SIMULATIONS = 200


def load_targets():
    return pd.read_csv(EQUITY_FILE).set_index("district")


def load_scenarios():
    with open(SCENARIO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def sample_scenario(scenarios):
    probs = [s["probability"] for s in scenarios]
    idx = np.random.choice(len(scenarios), p=probs)
    return scenarios[idx]


def simulate(plan, scenarios, targets, strategy: str):
    records = []
    for _ in range(NUM_SIMULATIONS):
        scenario = sample_scenario(scenarios)
        total_deficit, ratios = 0.0, []
        min_ratio = 1.0

        capacity_boost = 1.0
        if strategy == "FlexCapacity" and scenario["name"] == "WasteSpike":
            capacity_boost = 1.2

        for district, freq in plan.freq_map.items():
            target = targets.loc[district]["target_service_tons"]
            base = targets.loc[district]["baseline_service_tons"]
            service = (
                freq
                * base
                / 2
                * scenario["vehicle_availability"]
                * capacity_boost
                / scenario["travel_time_multiplier"]
            )
            service *= 1 / scenario["waste_multiplier"]
            ratio = service / target
            min_ratio = min(min_ratio, ratio)
            ratios.append(ratio)
            if service < target:
                total_deficit += target - service

        ratios = np.array(ratios)
        mad = np.mean(np.abs(ratios - np.mean(ratios)))

        if strategy == "PriorityMode" and scenario["name"] == "SevereWeather":
            mad = mad * 1.3  # allow higher variance in emergency prioritization

        records.append(
            {
                "strategy": strategy,
                "scenario": scenario["name"],
                "deficit_tons": total_deficit,
                "mad": mad,
                "min_service_ratio": min_ratio,
            }
        )
    return records


def main():
    df = load_district_data(DEFAULT_FEATURE_FILE)
    plan = enumerate_plans(df, top_k=1)[0]
    scenarios = load_scenarios()
    targets = load_targets()

    baseline_records = simulate(plan, scenarios, targets, "Baseline")
    priority_records = simulate(plan, scenarios, targets, "PriorityMode")
    flex_records = simulate(plan, scenarios, targets, "FlexCapacity")

    result_df = pd.DataFrame(baseline_records + priority_records + flex_records)
    result_df.to_csv(OUTPUT_FILE, index=False)
    print(result_df.groupby(["strategy", "scenario"]).agg(["mean", "std"]))


if __name__ == "__main__":
    main()


