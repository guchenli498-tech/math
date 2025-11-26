"""
任务5.3：政策建议与运力释放方案
---------------------------------
综合任务5.1-5.2成果，输出文字总结与运力再利用建议。
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EFFECT_FILE = PROJECT_ROOT / "outputs" / "task5_bins_policy_effects.csv"
NPV_FILE = PROJECT_ROOT / "outputs" / "task5_npv_sensitivity.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "task5_policy_summary.txt"


def main():
    effect_df = pd.read_csv(EFFECT_FILE)
    npv_df = pd.read_csv(NPV_FILE)

    avg_truck_saving = (effect_df["trucks_needed_2x_est"] - effect_df["trucks_after_bins"]).mean()
    avg_rat_drop = (effect_df["steady_rat"] - effect_df["steady_rat_after_bins"]).mean()
    best_npv = npv_df["npv"].max()

    summary = [
        "任务5.3 政策总结：",
        f"- 强制 Bins 预计释放平均 {avg_truck_saving:.1f} 辆车的运力，可用于弹性调度与应急共享。",
        f"- 鼠患稳态平均下降 {avg_rat_drop:.1f} （投诉代理），为后续 AM/PM 策略提供长期保障。",
        f"- NPV 敏感性分析显示最优情景 NPV ≈ {best_npv/1e6:.2f} 亿美元，表明经济上可行。",
        "- 建议把释放的车辆优先投入任务3的弹性运力池，余量用于高贫困区的动态优先调度。",
    ]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(summary), encoding="utf-8")
    print("已生成政策总结：", OUTPUT_FILE)


if __name__ == "__main__":
    main()


