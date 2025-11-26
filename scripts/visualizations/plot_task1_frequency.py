"""
任务1.1b 图表：最优频率配置（2x/3x）
"""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from scripts.models.task1_frequency_optimizer import (
    enumerate_plans,
    load_district_data,
    DEFAULT_FEATURE_FILE,
)

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = load_district_data(DEFAULT_FEATURE_FILE)
    plan = enumerate_plans(df, top_k=1)[0]
    freq_df = (
        pd.DataFrame(list(plan.freq_map.items()), columns=["district", "freq"])
        .sort_values("district")
    )

    colors = freq_df["freq"].map({2: "#59A14F", 3: "#E15759"})

    plt.figure(figsize=(9, 4))
    bars = plt.bar(freq_df["district"], freq_df["freq"], color=colors)
    plt.ylim(0, 3.5)
    plt.yticks([2, 3])
    plt.ylabel("Pickups per Week")
    plt.title("Task 1.1b: Optimal Frequency Configuration")
    plt.xticks(rotation=45)
    for bar, freq in zip(bars, freq_df["freq"]):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            freq + 0.05,
            f"{freq}x",
            ha="center",
            fontsize=8,
        )

    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color="#59A14F", label="2×/week"),
        plt.Rectangle((0, 0), 1, 1, color="#E15759", label="3×/week"),
    ]
    plt.legend(handles=legend_handles, loc="upper right")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "task1_frequency.png", dpi=300)
    plt.close()
    print("已生成 outputs/figures/task1_frequency.png")


if __name__ == "__main__":
    main()


