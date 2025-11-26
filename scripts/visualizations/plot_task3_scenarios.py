"""
任务3.1 图表：场景概率与影响因子
"""

from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCENARIO_FILE = PROJECT_ROOT / "data" / "scenarios" / "task3_scenarios.json"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    with open(SCENARIO_FILE, "r", encoding="utf-8") as f:
        scenarios = json.load(f)

    names = [s["name"] for s in scenarios]
    probs = [s["probability"] for s in scenarios]
    waste = [s["waste_multiplier"] for s in scenarios]
    vehicle = [s["vehicle_availability"] for s in scenarios]
    travel = [s["travel_time_multiplier"] for s in scenarios]

    fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    axes[0].bar(names, probs, color="#4E79A7")
    axes[0].set_ylabel("Probability")
    axes[0].set_title("Task 3.1: Scenario Probabilities")
    axes[0].set_ylim(0, max(probs) * 1.2)

    x = np.arange(len(names))
    width = 0.25
    axes[1].bar(x - width, vehicle, width, label="Vehicle availability", color="#59A14F")
    axes[1].bar(x, waste, width, label="Waste multiplier", color="#E15759")
    axes[1].bar(x + width, travel, width, label="Travel time multiplier", color="#76B7B2")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(names, rotation=45, ha="right")
    axes[1].set_ylabel("Multiplier")
    axes[1].set_title("Scenario Impact Factors")
    axes[1].legend()

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "task3_scenarios.png", dpi=300)
    plt.close(fig)
    print("已生成 task3_scenarios.png")


if __name__ == "__main__":
    main()


