"""
任务5.2 图表：NPV敏感性分析
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "outputs" / "task5_npv_sensitivity.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(DATA_FILE)
    pivot = df.pivot(index="discount_rate", columns="efficiency_gain", values="npv")

    plt.figure(figsize=(6, 4))
    plt.imshow(pivot / 1e6, cmap="RdYlGn", origin="lower")
    plt.xticks(range(len(pivot.columns)), pivot.columns)
    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.colorbar(label="NPV (million USD)")
    plt.xlabel("Efficiency Gain")
    plt.ylabel("Discount Rate")
    plt.title("Task 5.2: NPV Sensitivity")
    for i, r in enumerate(pivot.index):
        for j, eff in enumerate(pivot.columns):
            value = pivot.loc[r, eff] / 1e6
            plt.text(j, i, f"{value:.1f}", ha="center", va="center", color="black")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "task5_2_npv_heatmap.png", dpi=300)
    plt.close()
    print("已生成 task5_2_npv_heatmap.png")


if __name__ == "__main__":
    main()


