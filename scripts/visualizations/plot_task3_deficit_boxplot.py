"""
任务3 图表：不同策略/场景下的服务缺口箱线图
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
    plt.figure(figsize=(8, 5))
    df.boxplot(column="deficit_tons", by=["strategy", "scenario"])
    plt.ylabel("Service Deficit (tons)")
    plt.title("Task 3: Deficit Distribution by Strategy & Scenario")
    plt.suptitle("")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "task3_deficit_boxplot.png", dpi=300)
    plt.close()
    print("已生成 task3_deficit_boxplot.png")


if __name__ == "__main__":
    main()


