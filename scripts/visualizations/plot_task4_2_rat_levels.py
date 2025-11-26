"""
任务4.2 图表：稳态鼠群水平
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "outputs" / "task4_rat_simulation.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(DATA_FILE)
    df = df.sort_values("steady_rat", ascending=False)

    plt.figure(figsize=(8, 4))
    plt.bar(df["district"], df["steady_rat"], color="#59A14F")
    plt.xticks(rotation=45)
    plt.ylabel("Steady Rat Level (proxy)")
    plt.title("Task 4.2: Steady Rat Levels by District")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "task4_2_rat_levels.png", dpi=300)
    plt.close()
    print("已生成 task4_2_rat_levels.png")


if __name__ == "__main__":
    main()


