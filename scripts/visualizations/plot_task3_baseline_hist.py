"""
任务3.2 图表：基准仿真指标分布
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "outputs" / "task3_robust_simulation.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(DATA_FILE)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    axes[0].hist(df["deficit_tons"], bins=20, color="#E15759", alpha=0.8)
    axes[0].set_title("Task 3.2: Service Deficit Distribution")
    axes[0].set_xlabel("Deficit (tons)")
    axes[0].set_ylabel("Frequency")

    axes[1].hist(df["min_service_ratio"], bins=20, color="#4E79A7", alpha=0.8)
    axes[1].set_title("Task 3.2: Minimum Service Ratio Distribution")
    axes[1].set_xlabel("Min Service Ratio")

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "task3_baseline_hist.png", dpi=300)
    plt.close(fig)
    print("已生成 task3_baseline_hist.png")


if __name__ == "__main__":
    main()


