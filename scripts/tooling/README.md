# Scripts 目录说明

脚本分布在四个子文件夹内，用于支撑数据流水线、空间映射与建模分析。

## 1. pipelines/  —— 数据流水线

- `download_311_data.py`：抓取 311 鼠患投诉数据。
- `download_census_data.py`：尝试通过 API 获取普查数据。
- `collect_missing_data.py`：补齐收入、建筑等缺失字段。
- `preprocess_data.py`：合并 DSNY + 311，构建基础特征矩阵。
- `estimate_missing_data.py`：用估算逻辑增加收入/贫困/建筑字段。
- `analyze_and_clean_data.py`：质量检查、清洗、生成报告。
- `analyze_data.py` / `analyze_data_fast.py`：快速探索版（保留以备查）。

> 推荐顺序：download → preprocess → estimate → analyze_and_clean。

## 2. spatial/ —— WKT 修复与投诉映射

- `fix_dsny_wkt.py`：重新拼接被拆散的 WKT 字段。
- `fix_dsny_to_pickle.py`：将 DSNY CSV 转存为 Pickle，避免再次被切分。
- `map_complaints_to_districts.py`：使用 GeoPandas 做精准空间映射。
- `map_complaints_simple.py`：无需 GeoPandas 的近似映射方案。
- `SPATIAL_MAPPING_README.md`：空间映射的环境依赖与操作说明。

## 3. models/ —— 任务 3/4/5 的建模脚本

- `model1_robustness_analysis.py`：车辆故障 + 垃圾激增的 Monte Carlo 鲁棒性。
- `rat_dynamics_model.py`：鼠群动力学微分方程（Model 2）。
- `model3_npv_analysis.py`：垃圾桶政策的 NPV 评估（引用 Model 2 输出）。

## 4. tooling/ —— 依赖与指南（本文件夹）

- `requirements.txt`：项目依赖清单。
- `install_dependencies.py`：批量安装工具脚本。
- `README.md`：当前说明文档。

## 通用注意事项

- 所有脚本默认在项目根目录执行，内部路径以 `../data/` 访问数据。
- 输出会写入 `data/` 下相应子目录，请确认磁盘有写权限。
- 若使用 Conda 环境，建议 `conda activate mcm` 后再运行脚本。

