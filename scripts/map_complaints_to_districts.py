"""
将311投诉数据映射到DSNY区域
使用空间连接（Spatial Join）将经纬度坐标映射到MN01-MN12区域
"""
import pandas as pd
import geopandas as gpd
from shapely import wkt
from shapely.geometry import Point
import numpy as np

print("=" * 60)
print("311投诉数据映射到DSNY区域")
print("=" * 60)

# ==================== 1. 读取DSNY区域数据 ====================
print("\n1. 读取DSNY区域数据...")
try:
    districts_df = pd.read_csv('../data/raw/DSNY_Districts_20251026.csv')
    print(f"   ✓ 读取 {len(districts_df)} 行数据")
    
    # 检查multipolygon列
    if 'multipolygon' not in districts_df.columns:
        print("   ✗ 错误：找不到 'multipolygon' 列")
        print("   可用列：", list(districts_df.columns)[:10])
        exit(1)
    
    # 筛选曼哈顿区域
    manhattan_districts = districts_df[districts_df['DISTRICT'].str.startswith('MN', na=False)].copy()
    print(f"   ✓ 找到 {len(manhattan_districts)} 个曼哈顿区域")
    
    # 检查multipolygon数据
    print("\n   检查multipolygon数据...")
    valid_geom = manhattan_districts['multipolygon'].notna()
    print(f"     有效几何数据: {valid_geom.sum()} 个区域")
    
    if valid_geom.sum() == 0:
        print("   ⚠️ 警告：所有区域的multipolygon都是空的")
        print("   将尝试从其他列提取几何信息...")
        
        # 尝试查找其他可能的几何列
        possible_geom_cols = [col for col in districts_df.columns if 'geom' in col.lower() or 'shape' in col.lower()]
        if possible_geom_cols:
            print(f"   找到可能的几何列: {possible_geom_cols}")
        else:
            print("   ✗ 无法找到几何数据，需要从NYC Open Data下载Shapefile")
            exit(1)
    else:
        # 处理multipolygon列（WKT格式）
        print("   处理multipolygon数据（WKT格式）...")
        
        # 只处理有效的几何数据
        manhattan_districts_valid = manhattan_districts[valid_geom].copy()
        
        # 将WKT字符串转换为几何对象
        try:
            manhattan_districts_valid['geometry'] = manhattan_districts_valid['multipolygon'].apply(
                lambda x: wkt.loads(x) if pd.notna(x) and isinstance(x, str) else None
            )
            print(f"   ✓ 成功转换 {len(manhattan_districts_valid)} 个区域的几何数据")
        except Exception as e:
            print(f"   ✗ 错误：无法解析WKT格式: {e}")
            print("   尝试其他方法...")
            
            # 尝试直接读取（可能已经是几何对象）
            try:
                manhattan_districts_valid['geometry'] = manhattan_districts_valid['multipolygon']
            except:
                print("   ✗ 无法处理几何数据")
                exit(1)
        
        # 转换为GeoDataFrame
        gdf_districts = gpd.GeoDataFrame(manhattan_districts_valid, geometry='geometry')
        
        # 设置坐标系（NYC Open Data通常是EPSG:4326）
        gdf_districts.set_crs(epsg=4326, inplace=True)
        print(f"   ✓ 创建GeoDataFrame，坐标系: EPSG:4326")
        
        # 显示区域列表
        print("\n   区域列表:")
        for idx, row in gdf_districts.iterrows():
            print(f"     {row['DISTRICT']:6s} | 代码: {row['DISTRICTCODE']:6s}")
        
except Exception as e:
    print(f"   ✗ 错误: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# ==================== 2. 读取311投诉数据 ====================
print("\n2. 读取311投诉数据...")
try:
    rat_df = pd.read_csv('../data/external/311_rodent_complaints_manhattan.csv')
    print(f"   ✓ 读取 {len(rat_df):,} 条投诉记录")
    
    # 清洗：去掉没有经纬度的数据
    rat_df_clean = rat_df.dropna(subset=['latitude', 'longitude'])
    print(f"   ✓ 有效坐标记录: {len(rat_df_clean):,} 条")
    
    # 检查坐标范围
    lat_range = (rat_df_clean['latitude'].min(), rat_df_clean['latitude'].max())
    lon_range = (rat_df_clean['longitude'].min(), rat_df_clean['longitude'].max())
    print(f"   坐标范围: 纬度 {lat_range[0]:.4f}-{lat_range[1]:.4f}, 经度 {lon_range[0]:.4f}-{lon_range[1]:.4f}")
    
    # 移除异常坐标（曼哈顿范围：40.7-40.9, -74.05--73.9）
    valid_coords = rat_df_clean[
        (rat_df_clean['latitude'] >= 40.7) & (rat_df_clean['latitude'] <= 40.9) &
        (rat_df_clean['longitude'] >= -74.05) & (rat_df_clean['longitude'] <= -73.9)
    ]
    print(f"   ✓ 有效坐标（曼哈顿范围）: {len(valid_coords):,} 条")
    
    # 将经纬度转换为几何点
    geometry_points = [Point(xy) for xy in zip(valid_coords['longitude'], valid_coords['latitude'])]
    gdf_rats = gpd.GeoDataFrame(valid_coords, geometry=geometry_points)
    gdf_rats.set_crs(epsg=4326, inplace=True)
    print(f"   ✓ 创建GeoDataFrame")
    
except Exception as e:
    print(f"   ✗ 错误: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# ==================== 3. 空间连接 ====================
print("\n3. 执行空间连接（Spatial Join）...")
try:
    # 空间连接：判断每个投诉点在哪个区域内
    # how='inner' 会只保留在区域内的点
    # predicate='within' 表示点在多边形内
    joined_data = gpd.sjoin(gdf_rats, gdf_districts, how='inner', predicate='within')
    
    print(f"   ✓ 成功映射 {len(joined_data):,} 条投诉到区域")
    print(f"   映射率: {len(joined_data)/len(valid_coords)*100:.1f}%")
    
    # 统计各区域的投诉数
    district_complaints = joined_data.groupby('DISTRICT').size().reset_index(name='rodent_complaints')
    print("\n   各区域投诉统计:")
    for idx, row in district_complaints.iterrows():
        print(f"     {row['DISTRICT']:6s}: {row['rodent_complaints']:5,} 条")
    
    # 检查是否有区域没有投诉
    all_districts = set(gdf_districts['DISTRICT'].unique())
    mapped_districts = set(district_complaints['DISTRICT'].unique())
    missing = all_districts - mapped_districts
    if missing:
        print(f"\n   ⚠️ 以下区域没有投诉数据: {missing}")
        # 为缺失区域添加0值
        for dist in missing:
            district_complaints = pd.concat([
                district_complaints,
                pd.DataFrame({'DISTRICT': [dist], 'rodent_complaints': [0]})
            ], ignore_index=True)
    
except Exception as e:
    print(f"   ✗ 错误: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# ==================== 4. 更新区域特征矩阵 ====================
print("\n4. 更新区域特征矩阵...")
try:
    # 读取现有的特征矩阵
    df_features = pd.read_csv('../data/features/district_features_enhanced.csv')
    print(f"   ✓ 读取现有特征矩阵: {len(df_features)} 个区域")
    
    # 合并投诉数据
    df_features = df_features.merge(
        district_complaints,
        left_on='district',
        right_on='DISTRICT',
        how='left'
    )
    
    # 填充缺失值（如果有区域没有投诉）
    df_features['rodent_complaints'] = df_features['rodent_complaints'].fillna(0).astype(int)
    
    # 如果原来有estimated_rodent_complaints列，替换它
    if 'estimated_rodent_complaints' in df_features.columns:
        df_features = df_features.drop(columns=['estimated_rodent_complaints'])
    
    # 重命名列
    df_features = df_features.rename(columns={'rodent_complaints': 'rodent_complaints_mapped'})
    
    # 移除临时列
    if 'DISTRICT' in df_features.columns:
        df_features = df_features.drop(columns=['DISTRICT'])
    
    # 保存更新后的特征矩阵
    output_file = '../data/features/district_features_with_mapped_complaints.csv'
    df_features.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"   ✓ 已保存到: {output_file}")
    
    # 同时更新cleaned版本
    output_file_cleaned = '../data/processed/district_features_cleaned.csv'
    df_features.to_csv(output_file_cleaned, index=False, encoding='utf-8-sig')
    print(f"   ✓ 已更新清理版本: {output_file_cleaned}")
    
    # 显示更新后的数据
    print("\n   更新后的区域特征（前5行）:")
    display_cols = ['district', 'estimated_population', 'rodent_complaints_mapped', 'weekly_waste_tons']
    print(df_features[display_cols].head().to_string(index=False))
    
except Exception as e:
    print(f"   ✗ 错误: {e}")
    import traceback
    traceback.print_exc()

# ==================== 5. 保存映射结果 ====================
print("\n5. 保存映射结果...")
try:
    # 保存完整的映射数据（可选，用于后续分析）
    output_mapped = '../data/processed/311_complaints_mapped_to_districts.csv'
    joined_data_save = joined_data[['unique_key', 'created_date', 'complaint_type', 
                                     'latitude', 'longitude', 'DISTRICT', 'DISTRICTCODE']].copy()
    joined_data_save.to_csv(output_mapped, index=False, encoding='utf-8-sig')
    print(f"   ✓ 完整映射数据已保存: {output_mapped}")
    print(f"     记录数: {len(joined_data_save):,}")
    
except Exception as e:
    print(f"   ⚠️ 警告: 保存映射数据时出错: {e}")

print("\n" + "=" * 60)
print("映射完成！")
print("=" * 60)
print("\n输出文件:")
print("  1. data/features/district_features_with_mapped_complaints.csv")
print("  2. data/processed/district_features_cleaned.csv (已更新)")
print("  3. data/processed/311_complaints_mapped_to_districts.csv")
print("\n下一步:")
print("  - 使用更新后的特征矩阵进行建模")
print("  - 分析各区域的老鼠投诉分布")
print("=" * 60)

