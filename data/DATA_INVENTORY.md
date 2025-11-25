# 数据清单

## 数据文件总览

### raw/ - 原始数据（3个文件）

1. **DSNY_Districts_20251026.csv**
   - 大小：~75行，7330列
   - 内容：DSNY区域地理数据（所有5个区）
   - 关键列：DISTRICT, DISTRICTCODE, SHAPE_Area, SHAPE_Length
   - 状态：✅ 已整理

2. **data_dictionary.xlsx**
   - 内容：数据字典，说明各列含义
   - 状态：✅ 已整理

### external/ - 外部数据（1个文件）

1. **311_rodent_complaints_manhattan.csv**
   - 大小：19,435条记录
   - 内容：曼哈顿老鼠投诉数据
   - 关键列：created_date, latitude, longitude, complaint_type
   - 状态：✅ 已整理

### features/ - 特征矩阵（1个文件）

1. **district_features.csv**
   - 大小：12行（12个区域）
   - 内容：区域特征矩阵
   - 关键列：district, estimated_population, weekly_waste_tons, estimated_rodent_complaints
   - 状态：✅ 已整理
   - 注意：部分数据为估算值

### maps/ - 地图文件（1个文件）

1. **manhattan_districts_map.png**
   - 内容：曼哈顿区域地图
   - 状态：✅ 已整理

### processed/ - 处理后数据

- 当前为空，用于存放清理后的数据

---

## 数据统计

- 总文件数：6个
- 原始数据：3个
- 外部数据：1个
- 特征数据：1个
- 地图文件：1个

---

## 数据质量说明

### 完整数据
- ✅ 311老鼠投诉数据（19,435条，含坐标和时间）
- ✅ DSNY区域地理数据

### 估算数据（需在报告中说明）
- ⚠️ 区域面积（使用估算值）
- ⚠️ 区域人口（基于面积估算）
- ⚠️ 区域垃圾量（基于人口估算）
- ⚠️ 老鼠投诉分布（平均分配）

### 缺失数据
- ❌ 各区域收入/贫困率（任务2必需）
- ❌ 1-9单元建筑分布（任务5必需）
- ❌ 当前收集频率（可用假设）

---

最后更新：2025-11-16




