"""
Model 1：鲁棒性 Monte Carlo 模拟框架
-----------------------------------
用于任务 (3) 的中断场景分析，评估垃圾清运策略在车辆故障与垃圾激增下的服务平等性。
"""

import io
import numpy as np
import pandas as pd

TRUCK_CAPACITY = 12.0  # 每辆卡车日清运能力（吨）

STOCHASTIC_PARAMS = {
    "VEHICLE_FAILURE_PROB": 0.10,
    "WASTE_SPIKE_FACTOR": 1.5,
    "SPIKE_PROBABILITY": 0.20,
    "MAD_THRESHOLD": 0.10,
    "SIMULATION_DAYS": 30,
    "SIMULATION_RUNS": 100,
}


def calculate_mad(service_levels: np.ndarray) -> float:
    """计算服务平等性 MAD 指标。"""
    if service_levels.size == 0:
        return 0.0
    g_bar = service_levels.mean()
    deviations = np.abs(service_levels - g_bar)
    return deviations.mean()


def run_robustness_simulation(df_strategy: pd.DataFrame) -> pd.DataFrame:
    """Monte Carlo 模拟车辆故障与垃圾激增对服务水平的影响。"""
    results = []
    total_required_trucks = df_strategy["trucks_required"].sum()
    allocation_ratio = df_strategy["trucks_required"] / total_required_trucks
    target_qty = df_strategy["weekly_waste_tons"]

    for run in range(STOCHASTIC_PARAMS["SIMULATION_RUNS"]):
        collected_qty = pd.Series(0.0, index=df_strategy.index)

        for _ in range(STOCHASTIC_PARAMS["SIMULATION_DAYS"]):
            failed_trucks = np.random.binomial(
                total_required_trucks, STOCHASTIC_PARAMS["VEHICLE_FAILURE_PROB"]
            )
            operational_trucks = max(total_required_trucks - failed_trucks, 0)

            spike_multiplier = (
                STOCHASTIC_PARAMS["WASTE_SPIKE_FACTOR"]
                if np.random.rand() < STOCHASTIC_PARAMS["SPIKE_PROBABILITY"]
                else 1.0
            )

            daily_capacity = operational_trucks * TRUCK_CAPACITY * spike_multiplier

            collected_qty += allocation_ratio * daily_capacity

        service_levels = collected_qty / target_qty
        service_levels = service_levels.replace([np.inf, -np.inf], 0).to_numpy()
        mad_value = calculate_mad(service_levels)

        results.append({"run": run, "mad_value": mad_value})

    return pd.DataFrame(results)


def run_demo_simulation():
    """示例：使用内置数据验证鲁棒性框架。"""
    data_csv = """district,poverty_rate,assigned_frequency,trucks_required,weekly_waste_tons
MN03,24.0,3,46,1629.25
MN04,22.5,3,46,1629.25
MN05,19.5,3,46,1629.25
MN06,17.2,3,46,1629.25
MN11,13.9,2,68,1629.25
MN01,11.3,2,68,1629.25
MN10,10.3,2,68,1629.25
MN02,14.1,2,68,1629.25
MN08,8.0,2,68,1629.25
MN07,9.9,2,68,1629.25
MN09,6.5,2,68,1629.25
MN12,13.4,2,68,1629.25"""

    df_data = pd.read_csv(io.StringIO(data_csv))
    df_strategy = df_data[
        [
            "district",
            "poverty_rate",
            "assigned_frequency",
            "trucks_required",
            "weekly_waste_tons",
        ]
    ].set_index("district")

    robustness_results = run_robustness_simulation(df_strategy)
    mean_mad = robustness_results["mad_value"].mean()
    mad_pass_rate = (
        robustness_results["mad_value"]
        <= STOCHASTIC_PARAMS["MAD_THRESHOLD"]
    ).mean()

    print("\n--- Model 1 鲁棒性分析 (Monte Carlo 模拟) ---")
    print(
        f"模拟次数: {STOCHASTIC_PARAMS['SIMULATION_RUNS']} 次，持续 {STOCHASTIC_PARAMS['SIMULATION_DAYS']} 天"
    )
    print("-" * 50)
    print(f"平均服务不平等指数 (Mean MAD): {mean_mad:.4f}")
    print(
        f"MAD 达标率 (<= {STOCHASTIC_PARAMS['MAD_THRESHOLD']:.2f}): {mad_pass_rate:.1%}"
    )
    print("-" * 50)

    if mad_pass_rate >= 0.90:
        print("✅ 鲁棒性结论: 策略健壮。")
    else:
        print("⚠️ 鲁棒性结论: 策略敏感，需调整。")


if __name__ == "__main__":
    run_demo_simulation()

