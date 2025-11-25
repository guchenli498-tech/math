"""
Model 2：鼠群动力学微分方程求解器
用于求解 Task(4) 的老鼠风险参数，并为调度策略提供输入。
"""

import numpy as np
import pandas as pd
from scipy.integrate import odeint

# --- 1. 模型默认参数（可根据实际数据校准） ---
RAT_MODEL_PARAMS = {
    "alpha": 0.8,  # 固有增长率
    "K_base": 10_000,  # 基础环境承载力（降低以增强对垃圾暴露的敏感度）
    "eta": 15_000,  # 垃圾促进系数
    "delta": 0.1,  # 死亡/控制率
    "H": 100.0,  # 半饱和常数
}


# --- 2. 鼠群动力学微分方程 ---
def rat_dynamics(N, t, alpha, K, eta, G, delta, H):
    """dN/dt = 逻辑斯蒂增长 + 垃圾促进 - 控制/死亡"""
    logistic_growth = alpha * N * (1 - N / K)
    garbage_boost = eta * (G / (H + G))
    natural_death = delta * N
    return logistic_growth + garbage_boost - natural_death


# --- 3. 策略驱动的仿真函数 ---
def simulate_rat_population(
    N0,
    K_i,
    T_duration,
    T_step,
    strategy="PM_BAGS",
    strategy_params=None,
):
    """
    模拟单区域在给定清运策略下的鼠群数量轨迹。
    返回：轨迹数组、稳态值、时间数组。
    """

    strategy_params = strategy_params or {}

    # 默认策略影响（可外部覆盖）
    if strategy == "AM_BAGS":
        G_available = strategy_params.get("G", 1.5)
    elif strategy == "PM_BAGS":
        G_available = strategy_params.get("G", 0.8)
    elif strategy == "BINS":
        G_available = strategy_params.get("G", 0.05)
    else:
        G_available = strategy_params.get("G", 0.8)

    alpha = strategy_params.get("alpha", RAT_MODEL_PARAMS["alpha"])
    eta = strategy_params.get("eta", RAT_MODEL_PARAMS["eta"])
    delta = strategy_params.get("delta", RAT_MODEL_PARAMS["delta"])
    H = strategy_params.get("H", RAT_MODEL_PARAMS["H"])

    t = np.linspace(0, T_duration, int(T_duration / T_step))
    sol = odeint(
        rat_dynamics,
        N0,
        t,
        args=(alpha, K_i, eta, G_available, delta, H),
    )
    steady_state = sol[-1][0]
    return sol.flatten(), steady_state, t


def run_demo():
    """示例：以 MN03 区为例比较不同策略的稳态鼠群量。"""
    initial_rats = 8_372
    K_mn03 = RAT_MODEL_PARAMS["K_base"] * 1.5

    solution_am, steady_am, t_am = simulate_rat_population(
        N0=initial_rats,
        K_i=K_mn03,
        T_duration=30,
        T_step=0.1,
        strategy="AM_BAGS",
    )
    solution_bins, steady_bins, t_bins = simulate_rat_population(
        N0=initial_rats,
        K_i=K_mn03,
        T_duration=30,
        T_step=0.1,
        strategy="BINS",
    )

    print("\n--- Model 2 鼠群动力学示例 (MN03) ---")
    print(f"初始投诉/鼠群量 N0: {initial_rats}")
    print(f"AM 清运稳态鼠群: {steady_am:.0f}")
    print(f"Bins 方案稳态鼠群: {steady_bins:.0f}")

    df = pd.DataFrame(
        {
            "time_day": t_am,
            "AM_strategy": solution_am,
            "BIN_strategy": np.interp(t_am, t_bins, solution_bins),
        }
    )
    return df


if __name__ == "__main__":
    demo_df = run_demo()
    print("\n前 5 条时间序列：")
    print(demo_df.head())
