# 2025 CQUICM Problem D: 垃圾收集优化问题

## 项目简介

本项目旨在优化曼哈顿地区的垃圾收集调度，解决效率、公平性、健康风险和老鼠问题等多个目标。

## 项目结构

```
.
├── data/                    # 数据文件夹
│   ├── raw/                # 原始数据（问题包提供）
│   ├── external/           # 外部数据（NYC Open Data等）
│   ├── features/           # 特征矩阵
│   ├── processed/          # 清理后的数据
│   ├── maps/              # 地图文件
│   └── README.md          # 数据说明文档
│
├── scripts/                # Python脚本
│   ├── download_311_data.py          # 下载311投诉数据
│   ├── download_census_data.py       # 下载人口普查数据
│   ├── collect_missing_data.py       # 收集缺失数据
│   ├── preprocess_data.py            # 数据预处理
│   ├── estimate_missing_data.py      # 估算缺失数据
│   └── analyze_and_clean_data.py      # 数据分析和清理
│
├── docs/                   # 文档文件夹
│   ├── Problem_D_准备工作清单.md
│   ├── 数据分析和需求清单.md
│   ├── 数据获取详细指南.md
│   └── 数据阶段完整流程说明.md
│
├── notebooks/              # Jupyter Notebooks（待用）
│
└── README.md              # 项目说明（本文件）
```

## 快速开始

### 1. 数据收集

```bash
# 下载311老鼠投诉数据
python scripts/download_311_data.py

# 预处理数据，创建特征矩阵
python scripts/preprocess_data.py

# 估算缺失数据（收入、建筑等）
python scripts/estimate_missing_data.py
```

### 2. 数据分析与清理

```bash
# 分析数据质量并清理
python scripts/analyze_and_clean_data.py
```

### 3. 使用清理后的数据

清理后的数据位于 `data/processed/`：
- `311_rodent_complaints_cleaned.csv` - 清理后的311投诉数据
- `district_features_cleaned.csv` - 清理后的区域特征矩阵

## 数据说明

详细数据说明请查看：`data/README.md`

### 数据概览

- **311投诉数据**: 19,434条（清理后）
- **区域特征数据**: 12个曼哈顿区域（MN01-MN12）
- **数据完整度**: 100%

### 数据来源

1. **原始数据**: 问题包提供（DSNY区域数据）
2. **外部数据**: NYC Open Data（311投诉数据）
3. **估算数据**: 基于问题描述和实际情况估算

## 任务分工

### 数据阶段（已完成）
- ✅ 数据收集
- ✅ 数据预处理
- ✅ 数据分析
- ✅ 数据清理
- ✅ 生成报告

### 建模阶段（待进行）
- ⏳ 任务1：资源分配策略
- ⏳ 任务2：效率与公平性评估
- ⏳ 任务3：中断场景分析
- ⏳ 任务4：老鼠问题分析
- ⏳ 任务5：垃圾桶政策影响

## 环境要求

```bash
pip install pandas numpy requests
```

## 注意事项

1. **估算数据**: 部分数据为估算值，在报告中需明确说明
2. **数据版本**: 使用 `data/processed/` 中的清理后数据
3. **数据更新**: 如果获取到真实数据，应替换估算值

## 贡献者

- 数据收集与预处理：已完成
- 建模与分析：待进行

## 许可证

本项目用于2025 CQUICM竞赛。

---

最后更新：2025-11-16

