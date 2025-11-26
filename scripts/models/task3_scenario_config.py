"""
任务3.1：中断场景配置
--------------------------------
定义车辆故障、垃圾激增、天气延误等场景的参数，
供后续鲁棒性仿真引用。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "data" / "scenarios" / "task3_scenarios.json"
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


@dataclass
class Scenario:
    name: str
    probability: float
    vehicle_availability: float  # fraction of fleet available
    waste_multiplier: float
    travel_time_multiplier: float


def main():
    scenarios = [
        Scenario("Baseline", 0.6, 1.0, 1.0, 1.0),
        Scenario("VehicleFailure", 0.15, 0.85, 1.0, 1.0),
        Scenario("WasteSpike", 0.15, 1.0, 1.4, 1.0),
        Scenario("SevereWeather", 0.1, 0.9, 1.2, 1.3),
    ]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump([scenario.__dict__ for scenario in scenarios], f, indent=2)

    print(f"已写入场景配置：{OUTPUT_FILE}")


if __name__ == "__main__":
    main()


