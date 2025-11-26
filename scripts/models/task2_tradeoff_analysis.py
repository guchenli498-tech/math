"""
任务2.3：效率-公平权衡分析
--------------------------------
扫描不同的公平性权重 (lambda_fair) 与 MAD 阈值，比较
总服务量与最小服务水平之间的关系，输出权衡曲线数据。
"""

from __future__ import annotations

import itertools
from pathlib import Path
from typing import List, Tuple

import pandas as pd
import pulp

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EQUITY_FILE = PROJECT_ROOT / "data" / "features" / "district_equity_targets.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "task2_tradeoff_curve.csv"

from task2_efficiency_equity_model import District, load_districts, build_model


def solve_with_params(lambda_fair: float, epsilon_mad: float) -> Tuple[float, float]:
    districts = load_districts()
    model = pulp.LpProblem("Tradeoff", pulp.LpMinimize)

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

    model += pulp.lpSum(service_vars[d.name] for d in districts) - lambda_fair * m_var

    for d in districts:
        model += service_vars[d.name] <= d.baseline_tons * (freq_vars[d.name] / 2 + 0.5)
        model += service_vars[d.name] >= d.target_tons * 0.8
        model += fair_dev_pos[d.name] - fair_dev_neg[d.name] == service_vars[d.name] - avg_service
        model += m_var <= service_vars[d.name] / d.target_tons

    model += avg_service == (
        1 / len(districts)
    ) * pulp.lpSum(service_vars[d.name] for d in districts)
    model += (
        (1 / len(districts))
        * pulp.lpSum(fair_dev_pos[d.name] + fair_dev_neg[d.name] for d in districts)
        <= epsilon_mad * avg_service
    )

    model.solve(pulp.PULP_CBC_CMD(msg=False))
    total_service = sum(service_vars[d.name].value() for d in districts)
    min_service_ratio = m_var.value()
    return total_service, min_service_ratio


def main():
    lambda_values = [50, 100, 150, 200, 300]
    eps_values = [0.05, 0.08, 0.10, 0.12]

    records: List[dict] = []
    for lam, eps in itertools.product(lambda_values, eps_values):
        total_service, min_ratio = solve_with_params(lam, eps)
        records.append(
            {
                "lambda_fair": lam,
                "epsilon_mad": eps,
                "total_service_tons": total_service,
                "min_service_ratio": min_ratio,
            }
        )
        print(
            f"λ_fair={lam}, ε={eps} -> 总服务量 {total_service:.1f} 吨, "
            f"最差服务水平 {min_ratio:.3f}"
        )

    out_df = pd.DataFrame(records)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(OUTPUT_FILE, index=False)
    print("\n=== 权衡数据写入完成 ===")


if __name__ == "__main__":
    main()


