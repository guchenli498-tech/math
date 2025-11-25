"""
数据预处理 - 将311投诉和人口数据映射到DSNY区域
"""
import pandas as pd
import numpy as np
import json

print("=" * 60)
print("数据预处理：映射到DSNY区域")
print("=" * 60)

# 1. 读取311数据
print("\n1. 读取311老鼠投诉数据...")
try:
    df_311 = pd.read_csv("../data/external/311_rodent_complaints_manhattan.csv")
    print(f"   ✓ 读取 {len(df_311)} 条投诉记录")
    
    # 检查坐标
    df_311_clean = df_311.dropna(subset=['latitude', 'longitude'])
    print(f"   ✓ 有效坐标记录: {len(df_311_clean)} 条")
    
except FileNotFoundError:
    print("   ✗ 找不到 311_rodent_manhattan.csv")
    print("   请先下载311数据")
    exit(1)

# 2. 读取人口普查数据（可选）
print("\n2. 读取人口普查数据...")
df_census = None
try:
    df_census = pd.read_csv("census_nta_manhattan.csv")
    print(f"   ✓ 读取 {len(df_census)} 个NTA区域")
    
    # 筛选曼哈顿（如果有borough列）
    if 'borough' in df_census.columns:
        df_census = df_census[df_census['borough'].str.upper().str.contains('MANHATTAN', na=False)]
        print(f"   ✓ 曼哈顿NTA: {len(df_census)} 个")
    
except FileNotFoundError:
    print("   ⚠ 找不到 census_nta_manhattan.csv（可选数据）")
    print("   将使用估算值继续")
except Exception as e:
    print(f"   ⚠ 读取人口数据时出错: {e}")
    print("   将使用估算值继续")

# 3. 读取DSNY区域数据
print("\n3. 读取DSNY区域数据...")
try:
    # 只读取关键列
    key_cols = ['DISTRICT', 'DISTRICTCODE', 'SHAPE_Area', 'SHAPE_Length']
    df_dsny = pd.read_csv('../2025 CQU-MCM-ICM  Problems/Problems/2025_CQUICM_Problem_D_Data/DSNY_Districts_20251026.csv',
                          usecols=key_cols)
    
    # 筛选曼哈顿区域
    manhattan_districts = df_dsny[df_dsny['DISTRICT'].str.startswith('MN', na=False)].copy()
    
    # 转换数据类型（可能是字符串）
    manhattan_districts['SHAPE_Area'] = pd.to_numeric(manhattan_districts['SHAPE_Area'], errors='coerce')
    manhattan_districts['SHAPE_Length'] = pd.to_numeric(manhattan_districts['SHAPE_Length'], errors='coerce')
    
    print(f"   ✓ 找到 {len(manhattan_districts)} 个曼哈顿区域")
    
    # 显示区域列表
    print("\n   曼哈顿区域列表:")
    for idx, row in manhattan_districts.iterrows():
        if pd.notna(row['SHAPE_Area']):
            area_acre = row['SHAPE_Area'] / 43560  # 转换为英亩
            print(f"   {row['DISTRICT']:6s} | 代码: {row['DISTRICTCODE']:6s} | 面积: {area_acre:,.1f} 英亩")
        else:
            print(f"   {row['DISTRICT']:6s} | 代码: {row['DISTRICTCODE']:6s} | 面积: 未知")
    
except Exception as e:
    print(f"   ✗ 错误: {e}")
    exit(1)

# 4. 创建区域特征矩阵（基础版本）
print("\n4. 创建区域特征矩阵...")

# 初始化区域数据框
district_features = manhattan_districts[['DISTRICT', 'DISTRICTCODE', 'SHAPE_Area']].copy()
district_features.columns = ['district', 'district_code', 'area_sqft']
# 确保area_sqft是数字类型
district_features['area_sqft'] = pd.to_numeric(district_features['area_sqft'], errors='coerce')

# 如果所有面积都是NaN，使用估算值（曼哈顿平均区域面积约2-3平方英里）
if district_features['area_sqft'].isna().all():
    # 曼哈顿总面积约23平方英里，12个区域平均约1.9平方英里 = 约52,000,000平方英尺
    estimated_area_sqft = 52000000
    district_features['area_sqft'] = estimated_area_sqft
    print("   ⚠ 面积数据缺失，使用估算值")
else:
    # 填充缺失值（如果有）
    mean_area = district_features['area_sqft'].mean()
    if pd.isna(mean_area) or mean_area == 0:
        mean_area = 52000000  # 使用估算值
    district_features['area_sqft'] = district_features['area_sqft'].fillna(mean_area)

district_features['area_acre'] = district_features['area_sqft'] / 43560

# 统计311投诉（简单版本 - 基于坐标范围估算）
# 注意：这是简化版本，精确映射需要地理空间操作
print("\n   统计311投诉（简化版本）...")
print("   ⚠ 注意：精确映射需要地理空间操作，这里使用估算")

# 基于问题描述估算各区域投诉数
# 假设投诉分布与面积相关（简化）
total_complaints = len(df_311_clean)
# 确保area_acre没有NaN或inf
area_acre_sum = district_features['area_acre'].sum()
if pd.isna(area_acre_sum) or area_acre_sum == 0:
    # 如果面积总和无效，平均分配
    district_features['estimated_rodent_complaints'] = (total_complaints / len(district_features)).round().astype(int)
else:
    district_features['estimated_rodent_complaints'] = (
        total_complaints * district_features['area_acre'] / area_acre_sum
    ).round()
    # 处理NaN值
    district_features['estimated_rodent_complaints'] = district_features['estimated_rodent_complaints'].fillna(
        total_complaints / len(district_features)
    ).round().astype(int)

print(f"   总投诉数: {total_complaints}")
print(f"   分配到12个区域")

# 5. 基于问题描述估算其他数据
print("\n5. 基于问题描述估算其他数据...")

# 估算人口（基于面积，假设人口密度）
# 曼哈顿总人口约160万，12个区域平均约13.3万
avg_pop_per_district = 133000
district_features['estimated_population'] = (
    avg_pop_per_district * district_features['area_acre'] / district_features['area_acre'].mean()
).round().astype(int)

# 估算垃圾产生量（每人每天3.5磅）
district_features['daily_waste_lbs'] = district_features['estimated_population'] * 3.5
district_features['daily_waste_tons'] = district_features['daily_waste_lbs'] / 2000
district_features['weekly_waste_tons'] = district_features['daily_waste_tons'] * 7

# 估算所需卡车数（假设每周收集2次，每车12吨）
district_features['trucks_needed_2x'] = np.ceil(district_features['weekly_waste_tons'] / 2 / 12).astype(int)
district_features['trucks_needed_3x'] = np.ceil(district_features['weekly_waste_tons'] / 3 / 12).astype(int)

# 当前收集频率（假设）
district_features['current_pickups_per_week'] = 2

print("   ✓ 已估算：人口、垃圾产生量、卡车需求")

# 6. 保存结果
output_file = "../data/features/district_features.csv"
district_features.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n   ✓ 区域特征矩阵已保存到: {output_file}")

# 显示结果
print("\n" + "=" * 60)
print("区域特征矩阵预览:")
print("=" * 60)
print(district_features.to_string(index=False))

print("\n" + "=" * 60)
print("预处理完成！")
print("=" * 60)
print("\n下一步:")
print("1. 检查 district_features.csv")
print("2. 如果需要精确的地理映射，需要使用geopandas进行空间连接")
print("3. 开始建立优化模型")
print("=" * 60)

