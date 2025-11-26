```
outputs/
├── figures/                       # 所有任务图表（任务号写在文件名中）
│   ├── task1_*.png
│   ├── task2_*.png
│   ├── task3_*.png
│   ├── task4_*.png
│   └── task5_*.png
├── task1_frequency_history.csv    # 频次枚举/共享排班历史（若运行时保存）
├── task2_equity_targets.csv       # 公平性目标（同 data/features 中的副本）
├── task2_tradeoff_curve.csv       # 效率-公平权衡数据
├── task3_robust_simulation.csv    # 基准鲁棒性仿真结果
├── task3_resilience_comparison.csv# 基准 vs Priority/Flex 策略对比
├── task4_rat_simulation.csv       # 鼠患动力学仿真输出
├── task4_strategy_recommendation.csv # AM/PM + Bins 建议
├── task5_bins_policy_effects.csv  # Bins 对车队/鼠患影响
├── task5_npv_sensitivity.csv      # NPV 参数敏感性表
└── task5_policy_summary.txt       # 政策建议文字总结
```

- 所有 `.png` 图表按任务编号命名，可直接嵌入论文。
- `.csv` 文件是各任务的主要量化结果，重新运行脚本会覆盖旧版本，必要时请另行备份。
- 若输出目录新增文件，请同步更新本 README。

