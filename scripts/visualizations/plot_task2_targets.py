"""
任务2.1 图表：贫困率与目标频率/清运量
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "features" / "district_equity_targets.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(DATA_FILE).sort_values("poverty_rate", ascending=False)

    fig, ax1 = plt.subplots(figsize=(9, 4))
    ax1.bar(
        df["district"],
        df["poverty_rate"],
        color="#E15759",
        label="Poverty Rate (%)",
    )
    ax1.set_ylabel("Poverty Rate (%)", color="#E15759")
    ax1.tick_params(axis="y", labelcolor="#E15759")
    ax1.set_xticklabels(df["district"], rotation=45)

    ax2 = ax1.twinx()
    ax2.plot(
        df["district"],
        df["target_pickups_per_week"],
        color="#4E79A7",
        marker="o",
        label="Target Pickups",
    )
    ax2.set_ylim(1.5, 3.5)
    ax2.set_ylabel("Target Pickups/Week", color="#4E79A7")
    ax2.tick_params(axis="y", labelcolor="#4E79A7")

    plt.title("Task 2.1: Poverty vs Target Pickup Frequency")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "task2_poverty_target.png", dpi=300)
    plt.close(fig)
    print("已生成 task2_poverty_target.png")


if __name__ == "__main__":
    main()


