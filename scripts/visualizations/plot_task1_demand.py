"""
任务1.1a 图表：区级周垃圾量
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "features" / "district_demand_reestimated.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(DATA_FILE)
    df = df.sort_values("weekly_waste_tons_est", ascending=False)

    plt.figure(figsize=(10, 5))
    bars = plt.bar(df["district"], df["weekly_waste_tons_est"], color="#4E79A7")
    plt.xlabel("District")
    plt.ylabel("Weekly Waste (tons)")
    plt.title("Task 1.1a: Estimated Weekly Waste by District")
    plt.xticks(rotation=45)
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 30,
            f"{height:.0f}",
            ha="center",
            va="bottom",
            fontsize=8,
        )
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "task1_demand.png", dpi=300)
    plt.close()
    print("已生成 outputs/figures/task1_demand.png")


if __name__ == "__main__":
    main()


