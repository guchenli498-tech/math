"""
任务4.2：鼠患动力学仿真
--------------------------------
基于暴露时间估计及已有 rat_dynamics_model，比较
不同策略（AM/PM、Bins）下的稳态鼠群数量。
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd
from scipy.integrate import odeint

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from scripts.models.rat_dynamics_model import RAT_MODEL_PARAMS, rat_dynamics

EXPOSURE_FILE = PROJECT_ROOT / "data" / "features" / "district_exposure_estimates.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "task4_rat_simulation.csv"


def simulate_rat_level(initial_n: float, gi: float, days: int = 60):
    params = RAT_MODEL_PARAMS.copy()
    params["G"] = gi
    t_grid = np.linspace(0, days, days * 2)
    sol = odeint(
        rat_dynamics,
        initial_n,
        t_grid,
        args=(
            params["alpha"],
            params["K_base"],
            params["eta"],
            params["G"],
            params["delta"],
            params["H"],
        ),
    )
    return float(sol[-1][0])


def main():
    df = pd.read_csv(EXPOSURE_FILE)
    records = []
    for _, row in df.iterrows():
        district = row["district"]
        gi = row["gi_tons"]
        baseline_n = 1500  # 以投诉量为代理
        steady = simulate_rat_level(baseline_n, gi)
        records.append(
            {
                "district": district,
                "freq": row["freq"],
                "strategy": row["strategy"],
                "gi_tons": gi,
                "steady_rat": steady,
            }
        )

    out_df = pd.DataFrame(records)
    OUTPUT_FILE.parent.mkdir(exist_ok=True, parents=True)
    out_df.to_csv(OUTPUT_FILE, index=False)
    print("已生成鼠患仿真结果：", OUTPUT_FILE)


if __name__ == "__main__":
    main()


