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
├── scripts/                # Python脚本（按功能拆分）
│   ├── pipelines/          # 数据下载、预处理、清洗
│   ├── spatial/            # WKT 修复、空间映射
│   ├── models/             # Task 1-5 的建模代码
│   ├── tooling/            # 依赖安装、脚本说明
│   └── 快速数据获取脚本.py      # 历史辅助脚本（备查）
│
├── docs/                   # 文档文件夹
│   └── ...
│
└── README.md              # 项目说明（本文件）
```

## 快速开始

### 1. 安装依赖

**基础依赖**：
```bash
pip install pandas numpy requests
```

**空间分析（推荐）**：
```bash
# Windows 用户推荐使用 conda
conda install -c conda-forge geopandas shapely

# 或使用 pip（可能需要提前装 GDAL）
pip install geopandas shapely
```

若暂时无法安装 geopandas，可使用简化版脚本（`scripts/spatial/map_complaints_simple.py`）。

### 2. 数据流水线

```bash
# 1) 下载 311 投诉数据
python scripts/pipelines/download_311_data.py

# 2) 预处理 + 估算缺失特征
python scripts/pipelines/preprocess_data.py
python scripts/pipelines/estimate_missing_data.py

# 3) 数据分析 + 清洗报告
python scripts/pipelines/analyze_and_clean_data.py
```

### 3. 空间映射（关键步骤）

**方法1：使用 geopandas（精确）**
```bash
python scripts/spatial/fix_dsny_to_pickle.py      # 清洗 WKT 并生成 Pickle
python scripts/spatial/map_complaints_to_districts.py
```

**方法2：简化版（无需 geopandas）**
```bash
python scripts/spatial/map_complaints_simple.py
```

### 4. 建模脚本入口

- `python scripts/models/model1_robustness_analysis.py`：Task(3) Monte Carlo 鲁棒性。
- `python scripts/models/rat_dynamics_model.py`：Task(4) 鼠群动力学 / bins 风险评估。
- `python scripts/models/model3_npv_analysis.py`：Task(5) 垃圾桶政策 NPV。

> 以上脚本默认读取 `data/features/` 或 `data/processed/`，可按需调整参数/路径。

### 5. 使用清理后的数据

清理后的数据位于 `data/processed/`：
- `311_rodent_complaints_cleaned.csv` - 清理后的311投诉数据
- `district_features_cleaned.csv` - 清理后的区域特征矩阵（**包含真实映射的投诉数据**）

## 数据说明

详细数据说明请查看：`data/README.md`

### 数据概览

- **311投诉数据**: 19,434条（清理后）
- **区域特征数据**: 12个曼哈顿区域（MN01-MN12）
- **数据完整度**: 100%

### 关键改进 / 最新进展

- ✅ **空间映射链路**：`scripts/spatial` 包含 WKT 修复 + 精确映射 + 简化版备选。
- ✅ **数据流水线**：`scripts/pipelines` 覆盖下载 → 预处理 → 估算 → 清洗 的端到端脚本。
- ✅ **建模框架**：
  - Model 1（鲁棒性）：Monte Carlo 仿真车辆故障 / 垃圾激增。
  - Model 2（鼠群动力学）：`scipy.integrate.odeint` 求解，输出风险指标。
  - Model 3（NPV）：调用 Model 2 结果评估垃圾桶政策的经济性。

### 数据来源

1. **原始数据**: 问题包提供（DSNY区域数据）
2. **外部数据**: NYC Open Data（311投诉数据）
3. **估算数据**: 基于问题描述和实际情况估算（收入、建筑等）

## 任务分工

### 数据阶段（已完成）✅
- 数据收集 / 预处理 / 空间映射 / 清洗 / 报告生成

### 建模阶段（进行中）⚙️
- 已完成 Model 1-3 代码框架，可直接调整参数或接入新特征
- 后续重点：完善 Task(1)(2) 的动态调度与公平性度量

## 注意事项

1. **估算数据**: 部分数据为估算值（收入、建筑），在报告中需明确说明
2. **空间映射**: 已使用geopandas进行精确映射，投诉数据为真实值
3. **数据版本**: 使用 `data/processed/` 中的清理后数据
4. **数据更新**: 如果获取到真实数据，应替换估算值

## 贡献者

- 数据收集与预处理：已完成
- 空间映射：已完成
- 建模与分析：待进行

## 许可证

本项目用于2025 CQUICM竞赛。

---

最后更新：2025-11-25
