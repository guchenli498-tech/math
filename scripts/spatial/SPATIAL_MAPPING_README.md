# 空间映射说明

## 目标

将311投诉数据的经纬度坐标映射到DSNY区域（MN01-MN12）

## 方法1：使用geopandas（推荐）

### 安装依赖

**Windows用户（推荐使用conda）**：
```bash
conda install -c conda-forge geopandas shapely
```

**或使用pip（可能需要先安装GDAL）**：
```bash
pip install geopandas shapely
```

如果pip安装失败，可以：
1. 下载GDAL wheel文件：https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal
2. 或使用conda安装

### 运行脚本

```bash
python scripts/map_complaints_to_districts.py
```

## 方法2：从NYC Open Data下载Shapefile（如果CSV处理失败）

如果CSV中的multipolygon数据无法解析，可以：

1. 访问：https://data.cityofnewyork.us
2. 搜索："Sanitation Districts" 或 "DSNY Zones"
3. 下载Shapefile或GeoJSON格式
4. 使用geopandas读取：

```python
import geopandas as gpd

# 读取Shapefile
gdf = gpd.read_file('path/to/sanitation_districts.shp')

# 或读取GeoJSON
gdf = gpd.read_file('path/to/sanitation_districts.geojson')
```

## 方法3：简化版本（如果无法安装geopandas）

如果无法安装geopandas，可以使用近似方法：

1. 基于坐标范围估算区域
2. 使用曼哈顿已知区域边界（手动定义）
3. 使用邮政编码作为中间映射

## 输出文件

成功运行后会生成：
- `data/features/district_features_with_mapped_complaints.csv` - 包含真实映射的投诉数据
- `data/processed/311_complaints_mapped_to_districts.csv` - 完整映射数据

## 注意事项

- CSV文件中的multipolygon数据可能分散在多个列中（7330列）
- 如果WKT解析失败，建议下载Shapefile格式
- 确保坐标系一致（EPSG:4326）

