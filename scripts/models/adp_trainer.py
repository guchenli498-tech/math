"""
ADP（Approximate Dynamic Programming）简化训练器
------------------------------------------------------------------
基于 Task (4) 的鼠群动力学模型，构建一个线性值函数近似的
ADP 训练流程，用于在多策略（AM/PM 清运、Bins）之间学习长期
收益（负鼠量+成本）的估计。
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy.integrate import odeint

# 复用已有的鼠群动力学模型参数
from rat_dynamics_model import RAT_MODEL_PARAMS, rat_dynamics

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FEATURE_FILE = PROJECT_ROOT / "data" / "features" / "district_features_enhanced.csv"


# ——————————————————— 配置项 ——————————————————— #
@dataclass
class ADPConfig:
    episodes: int = 150
    horizon_days: int = 30
    gamma: float = 0.95
    learning_rate: float = 0.05
    epsilon_start: float = 0.2
    epsilon_min: float = 0.02
    epsilon_decay: float = 0.97
    process_noise: float = 50.0
    step_duration: float = 1.0  # 单步代表 1 天
    seed: int = 42


ACTIONS: Dict[str, Dict[str, float]] = {
    "AM_BAGS": {"G": 1.5, "cost_penalty": 450.0},
    "PM_BAGS": {"G": 0.8, "cost_penalty": 250.0},
    "BINS": {"G": 0.05, "cost_penalty": 120.0},
}


# ——————————————————— 线性值函数 ——————————————————— #
class LinearValueFunction:
    def __init__(self, dim: int):
        self.weights = np.zeros(dim, dtype=float)

    def predict(self, features: np.ndarray) -> float:
        return float(np.dot(self.weights, features))

    def update(self, features: np.ndarray, target: float, lr: float) -> float:
        estimate = self.predict(features)
        td_error = target - estimate
        self.weights += lr * td_error * features
        return td_error


# ——————————————————— ADP 训练核心 ——————————————————— #
class ADPTrainer:
    def __init__(self, district_df: pd.DataFrame, config: ADPConfig):
        self.df = district_df.reset_index(drop=True)
        self.config = config
        self.value_fn = LinearValueFunction(dim=4)
        self.rng = np.random.default_rng(config.seed)

    # ---------- 状态与特征 ----------
    def _init_state_from_row(self, row: pd.Series) -> Dict[str, float]:
        init_rats = max(row["estimated_rodent_complaints"], 1200)
        poverty = row["poverty_rate"] / 30.0  # 归一化
        k_effective = RAT_MODEL_PARAMS["K_base"] * (1 + row["poverty_rate"] / 50.0)
        return {"N": init_rats, "K": k_effective, "poverty": poverty, "G": 0.8}

    @staticmethod
    def _featurize(state: Dict[str, float]) -> np.ndarray:
        n_norm = state["N"] / max(state["K"], 1.0)
        poverty = state["poverty"]
        g_norm = state["G"] / 1.5
        return np.array([1.0, n_norm, poverty, g_norm], dtype=float)

    # ---------- 策略选择 ----------
    def _epsilon_greedy_action(self, state: Dict[str, float], epsilon: float) -> str:
        if self.rng.random() < epsilon:
            return self.rng.choice(list(ACTIONS.keys()))
        return self._greedy_action(state)

    def _greedy_action(self, state: Dict[str, float]) -> str:
        best_action = None
        best_value = -np.inf
        for action in ACTIONS:
            q_value = self._lookahead_value(state, action)
            if q_value > best_value:
                best_value = q_value
                best_action = action
        return best_action or "PM_BAGS"

    def _lookahead_value(self, state: Dict[str, float], action: str) -> float:
        next_state, reward = self._simulate_transition(state, action, stochastic=False)
        next_value = self.value_fn.predict(self._featurize(next_state))
        return reward + self.config.gamma * next_value

    # ---------- 环境动力学 ----------
    def _simulate_transition(
        self, state: Dict[str, float], action: str, stochastic: bool = True
    ) -> Tuple[Dict[str, float], float]:
        params = ACTIONS[action]
        G = params["G"]

        t_grid = np.linspace(0, self.config.step_duration, 8)
        sol = odeint(
            rat_dynamics,
            state["N"],
            t_grid,
            args=(
                RAT_MODEL_PARAMS["alpha"],
                state["K"],
                RAT_MODEL_PARAMS["eta"],
                G,
                RAT_MODEL_PARAMS["delta"],
                RAT_MODEL_PARAMS["H"],
            ),
        )
        next_n = float(sol[-1][0])

        if stochastic:
            next_n += self.rng.normal(0, self.config.process_noise)

        next_n = max(next_n, 0.0)
        next_state = {
            "N": next_n,
            "K": state["K"],
            "poverty": state["poverty"],
            "G": G,
        }
        reward = -(next_n + params["cost_penalty"])
        return next_state, reward

    # ---------- 训练主循环 ----------
    def train(self) -> pd.DataFrame:
        history: List[Dict[str, float]] = []
        epsilon = self.config.epsilon_start

        for ep in range(1, self.config.episodes + 1):
            row = self.df.sample(n=1, random_state=self.rng.integers(0, 1e9)).iloc[0]
            state = self._init_state_from_row(row)
            episode_return = 0.0

            for _ in range(self.config.horizon_days):
                action = self._epsilon_greedy_action(state, epsilon)
                next_state, reward = self._simulate_transition(state, action)

                target = reward + self.config.gamma * self.value_fn.predict(
                    self._featurize(next_state)
                )
                self.value_fn.update(
                    self._featurize(state), target, self.config.learning_rate
                )

                episode_return += reward
                state = next_state

            epsilon = max(self.config.epsilon_min, epsilon * self.config.epsilon_decay)
            history.append({"episode": ep, "return": episode_return, "epsilon": epsilon})

        return pd.DataFrame(history)

    # ---------- 策略评估 ----------
    def evaluate_policy(self, horizon: int = 30) -> pd.DataFrame:
        records: List[Dict[str, float]] = []
        for _, row in self.df.iterrows():
            state = self._init_state_from_row(row)
            total_reward = 0.0
            for _ in range(horizon):
                action = self._greedy_action(state)
                state, reward = self._simulate_transition(state, action, stochastic=False)
                total_reward += reward

            records.append(
                {
                    "district": row["district"],
                    "best_action": self._greedy_action(self._init_state_from_row(row)),
                    "value_estimate": self.value_fn.predict(self._featurize(state)),
                    "terminal_rat_level": state["N"],
                    "cumulative_reward": total_reward,
                }
            )
        return pd.DataFrame(records)


# ——————————————————— 数据加载 & CLI ——————————————————— #
def load_district_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"找不到特征文件：{path}")
    df = pd.read_csv(path)
    required_cols = {"district", "estimated_rodent_complaints", "poverty_rate"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"缺失必要列：{missing}")
    return df


def main():
    parser = argparse.ArgumentParser(description="简化版 ADP 训练器")
    parser.add_argument(
        "--feature-file",
        type=Path,
        default=DEFAULT_FEATURE_FILE,
        help="包含区级特征的 CSV 文件路径",
    )
    parser.add_argument("--episodes", type=int, default=150)
    parser.add_argument("--horizon", type=int, default=30)
    args = parser.parse_args()

    df = load_district_data(args.feature_file)
    config = ADPConfig(episodes=args.episodes, horizon_days=args.horizon)
    trainer = ADPTrainer(df, config)

    history = trainer.train()
    policy_df = trainer.evaluate_policy()

    print("\n=== 训练完成：Episode Returns (最后 5 条) ===")
    print(history.tail())
    print("\n=== 策略评估（贪心策略） ===")
    
    # --- 注意：这里原来的打印语句 ---
    print(
        policy_df[["district", "best_action", "terminal_rat_level", "cumulative_reward"]]
    )
    print("\n线性值函数权重：", trainer.value_fn.weights)

    # --- 请把新增的代码加在这里，并保持同样的缩进 ---
    print("\n=== [关键检查] 最终策略选择详情 ===")
    print(policy_df[["district", "best_action", "cumulative_reward"]])
    print("\n=== 策略统计 ===")
    print(policy_df["best_action"].value_counts())

if __name__ == "__main__":
    main()


