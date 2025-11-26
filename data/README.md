# Problem D 数据文件夹说明

## 文件夹结构

```
data/
├── raw/              # 原始数据（从问题包直接获取）
├── external/         # 外部下载的数据（NYC Open Data等）
├── processed/          # 处理后的数据（清理、转换后）
├── features/        # 特征矩阵（用于建模）
└── maps/            # 地图文件
```

---

## 数据文件说明

### raw/ - 原始数据

**DSNY_Districts_20251026.csv**
- 来源：问题包提供
- 内容：DSNY区域地理数据（包含所有5个区）
- 列：DISTRICT, DISTRICTCODE, OBJECTID, SHAPE_Area, SHAPE_Length, multipolygon
- 用途：提取曼哈顿12个区域（MN01-MN12）的地理信息

**data_dictionary.xlsx**
- 来源：问题包提供
- 内容：数据字典，说明各列含义
- 用途：理解数据结构

---

### external/ - 外部数据

**311_rodent_complaints_manhattan.csv**
- 来源：NYC Open Data (https://data.cityofnewyork.us)
- 下载日期：2025年
- 内容：曼哈顿地区老鼠投诉数据（19,435条记录）
- 列：
  - unique_key: 唯一标识
  - created_date: 投诉日期
  - complaint_type: 投诉类型（Rodent）
  - descriptor: 描述
  - incident_address: 地址
  - borough: 行政区（MANHATTAN）
  - latitude, longitude: 坐标
  - status: 状态
- 用途：任务4（老鼠问题分析）
- 数据范围：最近2年

---

### features/ - 特征矩阵（建模输入）

| 文件 | 说明 | 用途 |
|------|------|------|
| `district_features.csv` | 原始特征矩阵（基础人口/垃圾量） | Task 1 的初始估计 |
| `district_features_enhanced.csv` | 增强版特征（收入、贫困率、建筑估算） | Task 2/5 的公平性与Bins数据 |
| `district_demand_reestimated.csv` | 基于鼠患投诉 + 建筑权重重新分配 4.8M lbs/day 的需求、2×/3× 卡车数 | Task 1 频次枚举 & Task 3 场景基线 |
| `district_equity_targets.csv` | 由 `task2_equity_setup.py` 生成的目标频率、目标清运量、公平权重 | Task 2 线性规划输入 |
| `district_exposure_estimates.csv` | 由 `task4_exposure_time.py` 计算的 AM/PM 暴露时间、Bins 覆盖、Gi(t) | Task 4 鼠患动力学模型 |

> 以上文件均为脚本自动生成，若重新运行脚本请备份必要版本。

---

### maps/ - 地图文件

**manhattan_districts_map.png**
- 来源：问题包提供
- 内容：曼哈顿区域地图可视化
- 用途：可视化参考

---

## 数据状态

### ✅ 已有数据
- DSNY区域地理数据（raw）
- 311老鼠投诉数据（external）
- 区域特征矩阵（features）

### ⚠️ 缺失数据（已用估算值补充）
- ✅ 各区域收入/贫困率（任务2必需）- **已估算，见district_features_enhanced.csv**
- ✅ 1-9单元建筑分布（任务5必需）- **已估算，见district_features_enhanced.csv**
- ⚠️ 当前收集频率（可用假设：2次/周）

**注意**：估算数据基于曼哈顿实际情况和问题描述，在报告中需明确说明为估算值。
- 街道网络数据（可选）

---

## 数据使用说明

- Task 1/3 主要依赖 `features/district_demand_reestimated.csv` 与场景文件。
- Task 2 使用 `district_equity_targets.csv` 中的目标服务量与公平权重。
- Task 4 的鼠患模型读取 `district_exposure_estimates.csv`；Bins 政策评估使用 `outputs/task4_*.csv` 衍生的结果。

如需重新生成，请先运行相关脚本，再在此 README 中更新说明。

---

## 注意事项

1. **估算数据**：district_features.csv中部分数据为估算值（面积、人口），在报告中需明确说明
2. **数据来源**：所有外部数据需注明来源
3. **数据版本**：重要数据更新时建议保留历史版本

---

最后更新：2025-11-26

