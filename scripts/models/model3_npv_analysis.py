"""
Model 3: 垃圾桶政策的成本-效益 (NPV) 分析
----------------------------------------
基于任务(5) 的要求，评估“垃圾桶替代垃圾袋”政策在评估期内的净现值。
"""

from __future__ import annotations

import io
from pathlib import Path

import numpy as np
import pandas as pd


# --- 1. 引用 Model 2 的输出（示例值，可由实际仿真结果替换） ---
MODEL_2_OUTPUT = {
    "Rats_Baseline": 13_434,
    "Rats_Bins": 6_717,  # 假设 bins 方案将鼠群减半，与任务描述一致
    "Target_Rats_Reduction_Pct": 0.50,
}


# --- 2. 经济与政策参数 ---
ECONOMIC_PARAMS = {
    "T": 10,
    "DISCOUNT_RATE": 0.05,
    "COST_BIN_PER_UNIT": 120,
    "COST_TRUCK_MOD": 50_000,
    "COST_ANNUAL_MAINT": 5,
    "BENEFIT_TRUCK_ANNUAL": 250_000,
    "BENEFIT_RAT_VALUE": 500,
    "BIN_EFFICIENCY_BOOST": 0.25,
    "BINS_PER_BUILDING_1TO9": 4,
    "DEFAULT_TRUCK_COUNT": 728,
}


def calculate_npv_for_policy(df_features: pd.DataFrame, model_output: dict) -> dict:
    """
    根据区域特征与 Model 2 结果，计算垃圾桶政策的 NPV。
    返回包含 NPV、初始成本、年效益、卡车节省数量等指标的字典。
    """

    required_cols = [
        "buildings_1to9_units_count",
        "trucks_needed_2x",
        "estimated_rodent_complaints",
    ]
    missing = [col for col in required_cols if col not in df_features.columns]
    if missing:
        raise ValueError(f"缺少必要字段: {missing}")

    total_buildings_1to9 = df_features["buildings_1to9_units_count"].sum()
    total_bins_needed = (
        total_buildings_1to9 * ECONOMIC_PARAMS["BINS_PER_BUILDING_1TO9"]
    )
    c0_bins_purchase = total_bins_needed * ECONOMIC_PARAMS["COST_BIN_PER_UNIT"]

    initial_trucks = ECONOMIC_PARAMS["DEFAULT_TRUCK_COUNT"]
    c0_truck_mod = initial_trucks * ECONOMIC_PARAMS["COST_TRUCK_MOD"]
    c0_total = c0_bins_purchase + c0_truck_mod

    base_trucks = df_features["trucks_needed_2x"].sum()
    trucks_saved = base_trucks - (
        base_trucks / (1 + ECONOMIC_PARAMS["BIN_EFFICIENCY_BOOST"])
    )
    b_ops_savings = trucks_saved * ECONOMIC_PARAMS["BENEFIT_TRUCK_ANNUAL"]

    rats_baseline = df_features["estimated_rodent_complaints"].sum()
    rats_reduction = (
        rats_baseline * model_output["Target_Rats_Reduction_Pct"]
    )
    b_health_savings = rats_reduction * ECONOMIC_PARAMS["BENEFIT_RAT_VALUE"]

    annual_benefit = b_ops_savings + b_health_savings
    annual_cost = total_bins_needed * ECONOMIC_PARAMS["COST_ANNUAL_MAINT"]

    npv = -c0_total
    r = ECONOMIC_PARAMS["DISCOUNT_RATE"]
    t_horizon = ECONOMIC_PARAMS["T"]
    for year in range(1, t_horizon + 1):
        npv += (annual_benefit - annual_cost) / ((1 + r) ** year)

    return {
        "NPV": npv,
        "Initial_Cost": c0_total,
        "Annual_Benefit": annual_benefit,
        "Annual_Cost": annual_cost,
        "Trucks_Saved": trucks_saved,
        "Bins_Needed": total_bins_needed,
    }


def load_feature_data(path: Path) -> pd.DataFrame:
    """读取特征矩阵；如路径不存在，抛出友好的错误。"""
    if not path.exists():
        raise FileNotFoundError(f"找不到特征数据文件: {path}")
    return pd.read_csv(path)


def run_model3(
    feature_csv_path: Path | None = None,
    inline_csv_text: str | None = None,
) -> dict:
    """
    主入口：优先从文件读取数据，否则使用内嵌 CSV 文本（便于 Notebook 调试）。
    返回 NPV 计算结果。
    """

    if feature_csv_path:
        df_features = load_feature_data(feature_csv_path)
    elif inline_csv_text:
        df_features = pd.read_csv(io.StringIO(inline_csv_text))
    else:
        raise ValueError("必须提供 feature_csv_path 或 inline_csv_text。")

    result = calculate_npv_for_policy(df_features, MODEL_2_OUTPUT)
    return result


def print_summary(result: dict):
    """将 NPV 结果打印为易读格式。"""
    print("\n--- Model 3: 垃圾桶政策 NPV 分析 ---")
    print(
        f"评估期: {ECONOMIC_PARAMS['T']} 年, 贴现率: {ECONOMIC_PARAMS['DISCOUNT_RATE']:.0%}"
    )
    print("-" * 40)
    print(f"所需垃圾桶总数: {result['Bins_Needed']:,.0f} 个")
    print(f"节省的卡车数量: {result['Trucks_Saved']:.1f} 辆")
    print(f"总初始投资 (C0): ${result['Initial_Cost']:,.0f}")
    print(f"年度总效益 (B_t): ${result['Annual_Benefit']:,.0f}")
    print(f"年度维护成本 (C_t): ${result['Annual_Cost']:,.0f}")
    print("-" * 40)
    print(f"净现值 (NPV): ${result['NPV']:,.0f}")

    if result["NPV"] > 0:
        print("✅ 政策建议: NPV > 0，从经济角度可行。")
    else:
        print("❌ 政策建议: NPV < 0，需重新评估或优化政策设计。")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    feature_path = project_root / "data" / "features" / "district_features_enhanced.csv"

    analysis_result = run_model3(feature_csv_path=feature_path)
    print_summary(analysis_result)

