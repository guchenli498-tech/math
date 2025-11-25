"""
估算缺失数据 - Problem D
如果无法获取真实数据，使用合理假设生成估算值
"""
import pandas as pd
import numpy as np

print("=" * 60)
print("缺失数据估算工具")
print("=" * 60)

# 读取现有特征矩阵
print("\n1. 读取现有数据...")
try:
    df = pd.read_csv('../data/features/district_features.csv')
    print(f"   ✓ 读取 {len(df)} 个区域")
except FileNotFoundError:
    print("   ✗ 找不到 district_features.csv")
    exit(1)

# ==================== 估算收入/贫困率 ====================
print("\n2. 估算各区域收入/贫困率...")

# 基于曼哈顿实际情况的估算
# 曼哈顿收入中位数约$75,000-100,000，但区域差异大
# 假设：上城（MN01-MN06）收入较低，下城（MN07-MN12）收入较高

# 区域收入估算（美元）
income_base = {
    'MN01': 65000,  # 上东区，收入较高
    'MN02': 55000,  # 上西区
    'MN03': 45000,  # 哈林区，收入较低
    'MN04': 50000,  # 华盛顿高地
    'MN05': 48000,  # 上曼哈顿
    'MN06': 52000,  # 中城北
    'MN07': 85000,  # 中城，收入高
    'MN08': 90000,  # 中城东
    'MN09': 95000,  # 中城西
    'MN10': 80000,  # 下城东
    'MN11': 75000,  # 下城西
    'MN12': 70000   # 下城南
}

# 贫困率估算（%）
# 假设：收入越低，贫困率越高
poverty_base = {
    'MN01': 12,
    'MN02': 15,
    'MN03': 25,  # 哈林区贫困率较高
    'MN04': 22,
    'MN05': 20,
    'MN06': 18,
    'MN07': 10,
    'MN08': 8,
    'MN09': 7,
    'MN10': 11,
    'MN11': 13,
    'MN12': 14
}

# 添加随机波动（±10%）
np.random.seed(42)  # 固定随机种子，保证可重复
df['median_household_income'] = df['district'].map(income_base) * (1 + np.random.uniform(-0.1, 0.1, len(df)))
df['poverty_rate'] = df['district'].map(poverty_base) * (1 + np.random.uniform(-0.1, 0.1, len(df)))

# 四舍五入
df['median_household_income'] = df['median_household_income'].round().astype(int)
df['poverty_rate'] = df['poverty_rate'].round(1)

print("   ✓ 已估算收入中位数和贫困率")
print("\n   收入范围: ${:,.0f} - ${:,.0f}".format(
    df['median_household_income'].min(), 
    df['median_household_income'].max()
))
print("   贫困率范围: {:.1f}% - {:.1f}%".format(
    df['poverty_rate'].min(), 
    df['poverty_rate'].max()
))

# ==================== 估算1-9单元建筑数量 ====================
print("\n3. 估算1-9单元建筑分布...")

# 基于问题描述：
# - 全NYC: 91%的建筑是1-9单元，41%的家庭
# - 曼哈顿比例可能较低（更多大型建筑）
# - 假设：曼哈顿约70-75%的建筑是1-9单元

# 估算每个区域的建筑总数（基于人口）
# 假设：平均每户2.5人，每建筑平均10-15户
df['estimated_households'] = (df['estimated_population'] / 2.5).round().astype(int)
df['estimated_total_buildings'] = (df['estimated_households'] / 12).round().astype(int)

# 估算1-9单元建筑比例（上城区域比例更高）
building_ratio = {
    'MN01': 0.75,  # 上城，更多小型建筑
    'MN02': 0.72,
    'MN03': 0.78,  # 哈林区，小型建筑多
    'MN04': 0.76,
    'MN05': 0.74,
    'MN06': 0.70,
    'MN07': 0.65,  # 中城，大型建筑多
    'MN08': 0.63,
    'MN09': 0.60,
    'MN10': 0.68,
    'MN11': 0.70,
    'MN12': 0.72
}

df['buildings_1to9_units_ratio'] = df['district'].map(building_ratio)
df['buildings_1to9_units_count'] = (df['estimated_total_buildings'] * df['buildings_1to9_units_ratio']).round().astype(int)
df['households_1to9_units'] = (df['estimated_households'] * 0.41).round().astype(int)  # 41%的家庭

print("   ✓ 已估算1-9单元建筑数量")
print(f"\n   总建筑数: {df['estimated_total_buildings'].sum():,}")
print(f"   1-9单元建筑数: {df['buildings_1to9_units_count'].sum():,}")
print(f"   1-9单元建筑比例: {df['buildings_1to9_units_count'].sum() / df['estimated_total_buildings'].sum() * 100:.1f}%")

# ==================== 保存更新后的数据 ====================
print("\n4. 保存更新后的数据...")

output_file = '../data/features/district_features_enhanced.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"   ✓ 已保存到: {output_file}")

# 显示更新后的数据
print("\n" + "=" * 60)
print("更新后的区域特征（前5行）:")
print("=" * 60)
display_cols = ['district', 'estimated_population', 'median_household_income', 
                'poverty_rate', 'buildings_1to9_units_count', 'weekly_waste_tons']
print(df[display_cols].head().to_string(index=False))

print("\n" + "=" * 60)
print("数据估算完成！")
print("=" * 60)
print("\n注意:")
print("1. 这些是估算值，在报告中需明确说明")
print("2. 如果后续获取到真实数据，应替换这些估算值")
print("3. 估算基于曼哈顿实际情况和问题描述")
print("=" * 60)

