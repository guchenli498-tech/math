"""
任务3 图表：服务水平 vs 公平性散点图
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "outputs" / "task3_resilience_comparison.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(DATA_FILE)
    plt.figure(figsize=(6, 5))
    for strategy, subdf in df.groupby("strategy"):
        plt.scatter(
            subdf["min_service_ratio"],
            subdf["mad"],
            label=strategy,
            alpha=0.7,
        )
    plt.xlabel("Minimum Service Ratio")
    plt.ylabel("MAD")
    plt.title("Task 3: Service Level vs Fairness")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "task3_fairness_scatter.png", dpi=300)
    plt.close()
    print("已生成 task3_fairness_scatter.png")


if __name__ == "__main__":
    main()


