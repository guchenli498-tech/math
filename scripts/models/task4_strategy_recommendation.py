"""
任务4.3：AM/PM 与 Bins 区域策略建议
--------------------------------------
根据鼠患仿真结果，输出每区的推荐策略。
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAT_RESULT_FILE = PROJECT_ROOT / "outputs" / "task4_rat_simulation.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "task4_strategy_recommendation.csv"


def main():
    df = pd.read_csv(RAT_RESULT_FILE)
    threshold = df["steady_rat"].median()
    records = []

    for _, row in df.iterrows():
        recommendation = (
            "保持当前 AM+BINS 并持续监测"
            if row["steady_rat"] <= threshold
            else "提升 BINS 覆盖并优先安排 AM 收集"
        )
        records.append(
            {
                "district": row["district"],
                "current_strategy": row["strategy"],
                "steady_rat": row["steady_rat"],
                "recommendation": recommendation,
            }
        )

    out_df = pd.DataFrame(records)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(OUTPUT_FILE, index=False)
    print("已生成策略建议：", OUTPUT_FILE)


if __name__ == "__main__":
    main()


