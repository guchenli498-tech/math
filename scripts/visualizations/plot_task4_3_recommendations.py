"""
任务4.3 图表：策略建议分类
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "outputs" / "task4_strategy_recommendation.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(DATA_FILE)
    counts = df["recommendation"].value_counts()

    plt.figure(figsize=(5, 4))
    counts.plot(kind="bar", color="#4E79A7")
    plt.ylabel("Number of Districts")
    plt.title("Task 4.3: Recommendation Summary")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "task4_3_recommendations.png", dpi=300)
    plt.close()
    print("已生成 task4_3_recommendations.png")


if __name__ == "__main__":
    main()


