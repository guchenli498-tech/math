# 项目结构说明

## 完整目录结构

```
2025 CQUICM Problem D/
│
├── README.md                          # 项目主说明文档
├── .gitignore                        # Git忽略文件
├── PROJECT_STRUCTURE.md              # 本文件：项目结构说明
│
├── data/                             # 数据文件夹
│   ├── README.md                     # 数据说明文档
│   ├── DATA_INVENTORY.md             # 数据清单
│   │
│   ├── raw/                          # 原始数据（问题包提供）
│   │   ├── DSNY_Districts_20251026.csv
│   │   └── data_dictionary.xlsx
│   │
│   ├── external/                     # 外部数据（下载）
│   │   ├── 311_rodent_complaints_manhattan.csv
│   │   ├── 311_rodent_manhattan.csv  # 备份
│   │   └── district_features.csv     # 备份
│   │
│   ├── features/                     # 特征矩阵
│   │   ├── district_features.csv              # 基础版
│   │   └── district_features_enhanced.csv    # 增强版（含估算数据）
│   │
│   ├── processed/                    # 清理后的数据（最终使用）
│   │   ├── 311_rodent_complaints_cleaned.csv
│   │   ├── district_features_cleaned.csv
│   │   ├── data_quality_report.json
│   │   └── DATA_ANALYSIS_REPORT.md
│   │
│   └── maps/                         # 地图文件
│       └── manhattan_districts_map.png
│
├── scripts/                          # Python脚本
│   ├── README.md                     # 脚本说明
│   │
│   ├── 数据收集/
│   │   ├── download_311_data.py      # 下载311投诉数据
│   │   ├── download_census_data.py   # 下载人口普查数据
│   │   └── collect_missing_data.py   # 收集缺失数据
│   │
│   ├── 数据预处理/
│   │   ├── preprocess_data.py        # 创建特征矩阵
│   │   └── estimate_missing_data.py  # 估算缺失数据
│   │
│   └── 数据分析/
│       └── analyze_and_clean_data.py # 分析、清理、生成报告
│
├── docs/                             # 文档文件夹
│   ├── README.md                     # 文档说明
│   ├── Problem_D_准备工作清单.md
│   ├── 数据分析和需求清单.md
│   ├── 数据获取详细指南.md
│   ├── 数据获取快速开始.md
│   ├── 数据获取状态.md
│   └── 数据阶段完整流程说明.md
│
├── notebooks/                        # Jupyter Notebooks（待用）
│
└── 2025 CQU-MCM-ICM  Problems/      # 问题包（原始文件）
    └── Problems/
        └── 2025_CQUICM_Problem_D_Data/
```

## 文件夹说明

### data/ - 数据文件夹
- **raw/**: 原始数据，从问题包直接获取，不做修改
- **external/**: 外部下载的数据（NYC Open Data等）
- **features/**: 处理后的特征矩阵，用于建模
- **processed/**: 清理后的最终数据，**建模时使用这个文件夹的数据**
- **maps/**: 地图和可视化文件

### scripts/ - 脚本文件夹
所有Python脚本按功能分类：
- 数据收集：下载外部数据
- 数据预处理：创建特征矩阵
- 数据分析：质量分析和清理

### docs/ - 文档文件夹
项目相关的所有文档和指南

### notebooks/ - Notebooks文件夹
用于Jupyter Notebook分析（待用）

## 数据文件说明

### 最终使用的数据文件

**建模时使用以下文件**：
1. `data/processed/311_rodent_complaints_cleaned.csv` - 清理后的311投诉数据
2. `data/processed/district_features_cleaned.csv` - 清理后的区域特征矩阵

### 数据文件版本

- **基础版**: `district_features.csv` - 基础特征
- **增强版**: `district_features_enhanced.csv` - 含估算数据
- **清理版**: `district_features_cleaned.csv` - **最终使用版本**

## 脚本执行路径

所有脚本在 `scripts/` 文件夹中，使用相对路径访问 `data/` 文件夹：
- 脚本中路径：`../data/...`
- 从项目根目录执行：`python scripts/script_name.py`

## 文件命名规范

- **Python脚本**: 小写字母，下划线分隔（`snake_case`）
- **数据文件**: 小写字母，下划线分隔，描述性名称
- **文档文件**: 中文名称，描述性

## 注意事项

1. **不要修改** `data/raw/` 中的原始数据
2. **使用** `data/processed/` 中的清理后数据
3. **脚本路径**: 所有脚本使用相对路径 `../data/`
4. **数据备份**: `data/external/` 中有部分备份文件

---

最后更新：2025-11-16

