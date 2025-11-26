"""
任务2.2：效率+公平线性模型
--------------------------------
构建一个小规模的线性规划模型，在既定区级需求/目标下，
平衡车队效率与公平性约束（MAD、最小服务水平）。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import pandas as pd
import pulp

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EQUITY_FILE = PROJECT_ROOT / "data" / "features" / "district_equity_targets.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "task2_efficiency_equity_results.csv"

EPSILON_MAD = 0.10
LAMBDA_COST = 1.0
LAMBDA_FAIR = 200.0


@dataclass
class District:
    name: str
    baseline_tons: float
    target_tons: float
    target_pickups: int
    trucks_2x: int
    trucks_3x: int
    poverty_rate: float


def load_districts() -> List[District]:
    df = pd.read_csv(EQUITY_FILE)
    required = [
        "district",
        "baseline_service_tons",
        "target_service_tons",
        "target_pickups_per_week",
        "trucks_needed_2x_est",
        "trucks_needed_3x_est",
        "poverty_rate",
    ]
    if not set(required).issubset(df.columns):
        missing = set(required) - set(df.columns)
        raise ValueError(f"公平性文件缺少必要列：{missing}")

    districts = []
    for _, row in df.iterrows():
        districts.append(
            District(
                name=row["district"],
                baseline_tons=float(row["baseline_service_tons"]),
                target_tons=float(row["target_service_tons"]),
                target_pickups=int(row["target_pickups_per_week"]),
                trucks_2x=int(row["trucks_needed_2x_est"]),
                trucks_3x=int(row["trucks_needed_3x_est"]),
                poverty_rate=float(row["poverty_rate"]),
            )
        )
    return districts


def build_model(districts: List[District]) -> pulp.LpProblem:
    model = pulp.LpProblem("EfficiencyEquity", pulp.LpMinimize)

    freq_vars = {
        d.name: pulp.LpVariable(f"freq_{d.name}", lowBound=0, upBound=3, cat="Integer")
        for d in districts
    }
    service_vars = {
        d.name: pulp.LpVariable(f"service_{d.name}", lowBound=0)
        for d in districts
    }
    fair_dev_pos = {d.name: pulp.LpVariable(f"dev_pos_{d.name}", lowBound=0) for d in districts}
    fair_dev_neg = {d.name: pulp.LpVariable(f"dev_neg_{d.name}", lowBound=0) for d in districts}
    m_var = pulp.LpVariable("min_service", lowBound=0)

    avg_service = pulp.LpVariable("avg_service", lowBound=0)

    model += (
        LAMBDA_COST * pulp.lpSum(service_vars[d.name] for d in districts)
        + LAMBDA_FAIR * (-m_var)
    )

    for d in districts:
        model += service_vars[d.name] <= d.baseline_tons * (freq_vars[d.name] / 2 + 0.5)
        model += service_vars[d.name] >= 0.8 * d.baseline_tons
        model += service_vars[d.name] >= d.target_tons * 0.9
        model += fair_dev_pos[d.name] - fair_dev_neg[d.name] == service_vars[d.name] - avg_service
        model += m_var <= service_vars[d.name] / d.target_tons

    model += avg_service == (
        1 / len(districts)
    ) * pulp.lpSum(service_vars[d.name] for d in districts)
    model += (
        (1 / len(districts))
        * pulp.lpSum(fair_dev_pos[d.name] + fair_dev_neg[d.name] for d in districts)
        <= EPSILON_MAD * avg_service
    )

    return model, freq_vars, service_vars


def solve_model():
    districts = load_districts()
    model, freq_vars, service_vars = build_model(districts)
    model.solve(pulp.PULP_CBC_CMD(msg=False))

    results: List[Dict[str, float]] = []
    for d in districts:
        freq = freq_vars[d.name].value()
        service = service_vars[d.name].value()
        results.append(
            {
                "district": d.name,
                "optimal_freq": freq,
                "optimal_service_tons": service,
                "target_service_tons": d.target_tons,
                "service_ratio": service / d.target_tons,
            }
        )

    out_df = pd.DataFrame(results)
    OUTPUT_FILE.parent.mkdir(exist_ok=True, parents=True)
    out_df.to_csv(OUTPUT_FILE, index=False)

    print("=== 任务2.2 求解完成 ===")
    print(out_df.to_string(index=False))


if __name__ == "__main__":
    solve_model()


