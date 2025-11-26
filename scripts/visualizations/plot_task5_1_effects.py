"""
任务5.1 图表：车队与鼠患政策影响
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "outputs" / "task5_bins_policy_effects.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(DATA_FILE)
    df = df.sort_values("trucks_needed_2x_est", ascending=False)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharex=True)

    axes[0].bar(df["district"], df["trucks_needed_2x_est"], label="Before", color="#E15759")
    axes[0].bar(df["district"], df["trucks_after_bins"], label="After", color="#4E79A7", alpha=0.7)
    axes[0].set_ylabel("Trucks Needed (avg)")
    axes[0].set_title("Task 5.1: Fleet Impact")
    axes[0].legend()
    axes[0].tick_params(axis="x", rotation=45)

    axes[1].bar(df["district"], df["steady_rat"], label="Before", color="#E15759")
    axes[1].bar(df["district"], df["steady_rat_after_bins"], label="After", color="#4E79A7", alpha=0.7)
    axes[1].set_ylabel("Steady Rat Level")
    axes[1].set_title("Task 5.1: Rat Impact")
    axes[1].legend()
    axes[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "task5_1_policy_effects.png", dpi=300)
    plt.close(fig)
    print("已生成 task5_1_policy_effects.png")


if __name__ == "__main__":
    main()


