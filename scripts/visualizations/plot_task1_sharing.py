"""
任务1.2 图表：专属车队 vs 跨区共享
"""

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from scripts.models.task1_frequency_optimizer import (
    compute_shared_schedule,
    enumerate_plans,
    load_district_data,
    DEFAULT_FEATURE_FILE,
)

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = load_district_data(DEFAULT_FEATURE_FILE)
    plan = enumerate_plans(df, top_k=1)[0]
    shared_loads, _ = compute_shared_schedule(df, plan)
    shared_peak = max(shared_loads)
    dedicated = plan.dedicated_trucks

    labels = ["Dedicated Fleets", "Shared Fleet"]
    values = [dedicated, shared_peak]
    colors = ["#4E79A7", "#F28E2B"]

    plt.figure(figsize=(5, 4))
    plt.bar(labels, values, color=colors)
    plt.ylabel("Number of Trucks")
    plt.title("Task 1.2: Dedicated vs Shared Fleet Size")
    for x, y in zip(labels, values):
        plt.text(x, y + 3, f"{y}", ha="center")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "task1_sharing.png", dpi=300)
    plt.close()

    plt.figure(figsize=(6, 4))
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    plt.bar(days, shared_loads, color="#76B7B2")
    plt.ylabel("Trucks Needed")
    plt.title("Task 1.2: Shared Fleet Daily Load")
    for x, y in zip(days, shared_loads):
        plt.text(x, y + 2, f"{y}", ha="center")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "task1_shared_daily_load.png", dpi=300)
    plt.close()
    print("已生成 task1_sharing 图表")


if __name__ == "__main__":
    main()


