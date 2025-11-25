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
│   ├── preprocess_data.py            # 数据预处理
│   ├── estimate_missing_data.py      # 估算缺失数据
│   ├── analyze_and_clean_data.py    # 数据分析和清理
│   ├── map_complaints_to_districts.py # 空间映射（需要geopandas）
│   └── map_complaints_simple.py      # 简化版映射（无需geopandas）
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
# Windows用户推荐使用conda
conda install -c conda-forge geopandas shapely

# 或使用pip（可能需要先安装GDAL）
pip install geopandas shapely
```

如果geopandas安装困难，可以使用简化版脚本（`map_complaints_simple.py`）

### 2. 数据收集

```bash
# 下载311老鼠投诉数据
python scripts/download_311_data.py

# 预处理数据，创建特征矩阵
python scripts/preprocess_data.py

# 估算缺失数据（收入、建筑等）
python scripts/estimate_missing_data.py
```

### 3. 空间映射（关键步骤）

**方法1：使用geopandas（精确）**：
```bash
python scripts/map_complaints_to_districts.py
```

**方法2：简化版（近似）**：
```bash
python scripts/map_complaints_simple.py
```

### 4. 数据分析与清理

```bash
python scripts/analyze_and_clean_data.py
```

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

### 关键改进

✅ **空间映射已完成**：311投诉数据已精确映射到MN01-MN12区域
- 使用geopandas进行空间连接（Spatial Join）
- 将经纬度坐标映射到DSNY区域边界
- 更新了区域特征矩阵，使用真实投诉数据替代估算值

### 数据来源

1. **原始数据**: 问题包提供（DSNY区域数据）
2. **外部数据**: NYC Open Data（311投诉数据）
3. **估算数据**: 基于问题描述和实际情况估算（收入、建筑等）

## 任务分工

### 数据阶段（已完成）✅
- ✅ 数据收集
- ✅ 数据预处理
- ✅ **空间映射**（经纬度→区域）
- ✅ 数据分析
- ✅ 数据清理
- ✅ 生成报告

### 建模阶段（待进行）⏳
- ⏳ 任务1：资源分配策略
- ⏳ 任务2：效率与公平性评估
- ⏳ 任务3：中断场景分析
- ⏳ 任务4：老鼠问题分析
- ⏳ 任务5：垃圾桶政策影响

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

最后更新：2025-11-16
