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

### features/ - 特征矩阵

**district_features.csv**
- 来源：基于raw和external数据生成
- 内容：12个曼哈顿区域的特征矩阵（基础版本）

**district_features_enhanced.csv**
- 来源：基于district_features.csv + 估算数据生成
- 内容：增强版特征矩阵，包含收入、贫困率、建筑数据
- 新增列：
  - median_household_income: 收入中位数（估算）
  - poverty_rate: 贫困率（估算）
  - estimated_households: 估算户数
  - estimated_total_buildings: 估算总建筑数
  - buildings_1to9_units_count: 1-9单元建筑数量（估算）
  - households_1to9_units: 1-9单元建筑中的家庭数（估算）
- 注意：新增数据为估算值，需在报告中说明
- 列：
  - district: 区域代码（MN01-MN12）
  - district_code: 区域数字代码（101-112）
  - area_sqft: 面积（平方英尺，估算值）
  - area_acre: 面积（英亩）
  - estimated_rodent_complaints: 估算的老鼠投诉数
  - estimated_population: 估算人口
  - daily_waste_lbs: 每日垃圾量（磅）
  - daily_waste_tons: 每日垃圾量（吨）
  - weekly_waste_tons: 每周垃圾量（吨）
  - trucks_needed_2x: 每周2次收集需要的卡车数
  - trucks_needed_3x: 每周3次收集需要的卡车数
  - current_pickups_per_week: 当前收集频率（假设为2）
- 用途：所有5个任务的基础数据
- 注意：部分数据为估算值，在报告中需说明

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

### 建模时使用
主要使用 `features/district_features.csv` 作为基础数据

### 分析时使用
- 老鼠问题分析：使用 `external/311_rodent_complaints_manhattan.csv`
- 地理分析：使用 `raw/DSNY_Districts_20251026.csv`

### 数据更新
- 如果获取到新数据，按类型放入对应文件夹
- 更新特征矩阵后，替换 `features/district_features.csv`
- 更新此README说明

---

## 注意事项

1. **估算数据**：district_features.csv中部分数据为估算值（面积、人口），在报告中需明确说明
2. **数据来源**：所有外部数据需注明来源
3. **数据版本**：重要数据更新时建议保留历史版本

---

最后更新：2025年

