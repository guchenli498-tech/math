"""
任务4.1 图表：各区有效暴露时间与 Gi
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "features" / "district_exposure_estimates.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(DATA_FILE)

    fig, ax1 = plt.subplots(figsize=(8, 4))
    ax1.bar(df["district"], df["effective_exposure"], color="#E15759")
    ax1.set_ylabel("Effective Exposure (hours)")
    ax1.set_xticklabels(df["district"], rotation=45)

    ax2 = ax1.twinx()
    ax2.plot(df["district"], df["gi_tons"], color="#4E79A7", marker="o")
    ax2.set_ylabel("Gi (tons)")

    plt.title("Task 4.1: Exposure Hours and Gi")
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "task4_1_exposure_gi.png", dpi=300)
    plt.close(fig)
    print("已生成 task4_1_exposure_gi.png")


if __name__ == "__main__":
    main()


