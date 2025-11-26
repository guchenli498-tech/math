"""
任务2.3 图表：效率-公平权衡曲线
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "outputs" / "task2_tradeoff_curve.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(DATA_FILE)

    plt.figure(figsize=(6, 4))
    for lam, subdf in df.groupby("lambda_fair"):
        plt.plot(
            subdf["epsilon_mad"],
            subdf["total_service_tons"],
            marker="o",
            label=f"λ_fair={lam}",
        )
    plt.xlabel("MAD Threshold ε")
    plt.ylabel("Total Service (tons/week)")
    plt.title("Task 2.3: Efficiency vs Fairness Trade-off")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "task2_tradeoff_curve.png", dpi=300)
    plt.close()

    plt.figure(figsize=(6, 4))
    for eps, subdf in df.groupby("epsilon_mad"):
        plt.plot(
            subdf["lambda_fair"],
            subdf["min_service_ratio"],
            marker="s",
            label=f"ε={eps}",
        )
    plt.xlabel("λ_fair")
    plt.ylabel("Minimum Service Ratio m")
    plt.title("Task 2.3: Minimum Service Level vs λ")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "task2_min_service_curve.png", dpi=300)
    plt.close()
    print("已生成 task2_tradeoff 曲线图")


if __name__ == "__main__":
    main()


