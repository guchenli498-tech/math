"""
任务2.2 图表：服务量 / 目标量
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "outputs" / "task2_efficiency_equity_results.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(DATA_FILE).sort_values("optimal_service_tons", ascending=False)

    plt.figure(figsize=(9, 4))
    colors = ["#E15759" if r >= 1 else "#4E79A7" for r in df["service_ratio"]]
    bars = plt.bar(df["district"], df["service_ratio"], color=colors)
    plt.axhline(1.0, color="#999999", linestyle="--", linewidth=1)
    plt.ylabel("Service / Target")
    plt.title("Task 2.2: Service Ratio by District")
    plt.xticks(rotation=45)
    for bar, ratio in zip(bars, df["service_ratio"]):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            ratio + 0.05,
            f"{ratio:.2f}",
            ha="center",
            fontsize=8,
        )
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "task2_service_ratio.png", dpi=300)
    plt.close()
    print("已生成 task2_service_ratio.png")


if __name__ == "__main__":
    main()


