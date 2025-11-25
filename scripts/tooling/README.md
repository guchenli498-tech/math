# Scripts 文件夹说明

本文件夹包含所有Python脚本，用于数据收集、预处理、分析和清理。

## 脚本列表

### 数据收集脚本

1. **download_311_data.py**
   - 功能：从NYC Open Data下载311老鼠投诉数据
   - 输出：`data/external/311_rodent_complaints_manhattan.csv`
   - 使用：`python scripts/download_311_data.py`

2. **download_census_data.py**
   - 功能：下载人口普查数据（可选）
   - 输出：`data/external/census_nta_manhattan.csv`
   - 使用：`python scripts/download_census_data.py`

3. **collect_missing_data.py**
   - 功能：尝试收集缺失数据（收入、建筑等）
   - 使用：`python scripts/collect_missing_data.py`

### 数据预处理脚本

4. **preprocess_data.py**
   - 功能：提取DSNY区域数据，创建区域特征矩阵
   - 输入：原始DSNY数据、311投诉数据
   - 输出：`data/features/district_features.csv`
   - 使用：`python scripts/preprocess_data.py`

5. **estimate_missing_data.py**
   - 功能：估算缺失数据（收入、贫困率、建筑数据）
   - 输入：`data/features/district_features.csv`
   - 输出：`data/features/district_features_enhanced.csv`
   - 使用：`python scripts/estimate_missing_data.py`

### 数据分析脚本

6. **analyze_and_clean_data.py**
   - 功能：分析数据质量，清理数据，生成报告
   - 输入：所有数据文件
   - 输出：
     - `data/processed/311_rodent_complaints_cleaned.csv`
     - `data/processed/district_features_cleaned.csv`
     - `data/processed/data_quality_report.json`
     - `data/processed/DATA_ANALYSIS_REPORT.md`
   - 使用：`python scripts/analyze_and_clean_data.py`

### 辅助脚本

7. **analyze_data.py** / **analyze_data_fast.py**
   - 功能：快速分析数据结构（开发用）
   - 状态：已弃用，功能已整合到主脚本

8. **快速数据获取脚本.py**
   - 功能：数据获取工具集合（开发用）
   - 状态：已弃用，功能已拆分到各专门脚本

## 执行顺序

建议按以下顺序执行脚本：

1. `download_311_data.py` - 下载311数据
2. `preprocess_data.py` - 创建基础特征矩阵
3. `estimate_missing_data.py` - 补充估算数据
4. `analyze_and_clean_data.py` - 分析和清理

## 注意事项

- 所有脚本输出到 `data/` 文件夹的相应子文件夹
- 脚本会创建必要的文件夹（如果不存在）
- 部分脚本需要网络连接（下载数据）

