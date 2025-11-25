"""
简化版：将311投诉映射到区域（不使用geopandas）
基于坐标范围近似映射（如果无法安装geopandas）
"""
import pandas as pd
import numpy as np

print("=" * 60)
print("311投诉数据映射到DSNY区域（简化版）")
print("=" * 60)
print("\n注意：这是近似方法，精确映射需要使用geopandas")
print("=" * 60)

# 曼哈顿各区域的大致坐标范围（近似值）
# 这些值需要根据实际地图调整
DISTRICT_BOUNDS = {
    'MN01': {'lat_min': 40.75, 'lat_max': 40.80, 'lon_min': -73.98, 'lon_max': -73.93},  # 上东区
    'MN02': {'lat_min': 40.75, 'lat_max': 40.80, 'lon_min': -74.00, 'lon_max': -73.98},  # 上西区
    'MN03': {'lat_min': 40.80, 'lat_max': 40.85, 'lon_min': -73.96, 'lon_max': -73.92},  # 哈林区
    'MN04': {'lat_min': 40.82, 'lat_max': 40.87, 'lon_min': -73.95, 'lon_max': -73.90},  # 华盛顿高地
    'MN05': {'lat_min': 40.85, 'lat_max': 40.88, 'lon_min': -73.94, 'lon_max': -73.90},  # 上曼哈顿
    'MN06': {'lat_min': 40.72, 'lat_max': 40.75, 'lon_min': -73.99, 'lon_max': -73.95},  # 中城北
    'MN07': {'lat_min': 40.70, 'lat_max': 40.75, 'lon_min': -73.99, 'lon_max': -73.95},  # 中城
    'MN08': {'lat_min': 40.70, 'lat_max': 40.75, 'lon_min': -73.98, 'lon_max': -73.93},  # 中城东
    'MN09': {'lat_min': 40.70, 'lat_max': 40.75, 'lon_min': -74.01, 'lon_max': -73.98},  # 中城西
    'MN10': {'lat_min': 40.68, 'lat_max': 40.72, 'lon_min': -73.98, 'lon_max': -73.93},  # 下城东
    'MN11': {'lat_min': 40.68, 'lat_max': 40.72, 'lon_min': -74.01, 'lon_max': -73.98},  # 下城西
    'MN12': {'lat_min': 40.70, 'lat_max': 40.72, 'lon_min': -74.02, 'lon_max': -73.99},  # 下城南
}

def assign_district(lat, lon):
    """根据坐标分配区域"""
    for district, bounds in DISTRICT_BOUNDS.items():
        if (bounds['lat_min'] <= lat <= bounds['lat_max'] and
            bounds['lon_min'] <= lon <= bounds['lon_max']):
            return district
    return None

# 读取311数据
print("\n1. 读取311投诉数据...")
# 尝试多个可能的路径
possible_paths = [
    '../data/external/311_rodent_complaints_manhattan.csv',
    '../../data/external/311_rodent_complaints_manhattan.csv',
    '../data/external/311_rodent_manhattan.csv'
]

rat_df = None
for path in possible_paths:
    try:
        rat_df = pd.read_csv(path)
        print(f"   ✓ 从 {path} 读取数据")
        break
    except FileNotFoundError:
        continue

if rat_df is None:
    print("   ✗ 错误：找不到311投诉数据文件")
    print("   请确保文件在以下位置之一：")
    for path in possible_paths:
        print(f"     - {path}")
    exit(1)
rat_df_clean = rat_df.dropna(subset=['latitude', 'longitude'])
print(f"   ✓ 有效坐标记录: {len(rat_df_clean):,} 条")

# 映射到区域
print("\n2. 映射到区域（基于坐标范围）...")
rat_df_clean = rat_df_clean.copy()  # 避免SettingWithCopyWarning
rat_df_clean['DISTRICT'] = rat_df_clean.apply(
    lambda row: assign_district(row['latitude'], row['longitude']), 
    axis=1
)

# 统计
mapped = rat_df_clean[rat_df_clean['DISTRICT'].notna()]
print(f"   ✓ 成功映射: {len(mapped):,} 条 ({len(mapped)/len(rat_df_clean)*100:.1f}%)")
print(f"   ⚠️ 未映射: {rat_df_clean['DISTRICT'].isna().sum():,} 条")

district_counts = mapped.groupby('DISTRICT').size().reset_index(name='rodent_complaints')
print("\n   各区域投诉统计:")
for idx, row in district_counts.iterrows():
    print(f"     {row['DISTRICT']:6s}: {row['rodent_complaints']:5,} 条")

# 更新特征矩阵
print("\n3. 更新区域特征矩阵...")
# 尝试多个可能的路径
possible_paths = [
    '../data/features/district_features_enhanced.csv',
    '../../data/features/district_features_enhanced.csv'
]

df_features = None
for path in possible_paths:
    try:
        df_features = pd.read_csv(path)
        print(f"   ✓ 从 {path} 读取数据")
        break
    except FileNotFoundError:
        continue

if df_features is None:
    print("   ✗ 错误：找不到特征矩阵文件")
    exit(1)
df_features = df_features.merge(district_counts, left_on='district', right_on='DISTRICT', how='left')
df_features['rodent_complaints'] = df_features['rodent_complaints'].fillna(0).astype(int)
df_features = df_features.drop(columns=['DISTRICT'])

output_file = '../data/features/district_features_with_mapped_complaints.csv'
df_features.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"   ✓ 已保存到: {output_file}")

print("\n" + "=" * 60)
print("映射完成（简化版）！")
print("=" * 60)
print("\n注意：这是近似方法，建议安装geopandas进行精确映射")
print("=" * 60)

