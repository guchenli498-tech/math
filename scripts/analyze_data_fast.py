import pandas as pd
import numpy as np

print("=" * 60)
print("数据文件分析")
print("=" * 60)

# 只读取前6列（关键列）
key_columns = ['DISTRICT', 'DISTRICTCODE', 'OBJECTID', 'SHAPE_Area', 'SHAPE_Length', 'multipolygon']

try:
    print("\n1. 读取关键列数据...")
    df = pd.read_csv('2025 CQU-MCM-ICM  Problems/Problems/2025_CQUICM_Problem_D_Data/DSNY_Districts_20251026.csv', 
                     usecols=key_columns)
    
    print(f"   ✓ 成功读取 {len(df)} 行数据")
    
    print("\n2. 数据基本信息:")
    print(f"   总行数: {len(df)}")
    print(f"   总列数: {len(df.columns)}")
    print(f"   列名: {list(df.columns)}")
    
    print("\n3. 曼哈顿区域信息 (MN01-MN12):")
    manhattan = df[df['DISTRICT'].str.startswith('MN', na=False)].copy()
    print(f"   曼哈顿区域数量: {len(manhattan)}")
    
    if len(manhattan) > 0:
        print("\n   各区域详情:")
        for idx, row in manhattan.iterrows():
            print(f"   - {row['DISTRICT']:8s} | 代码: {row['DISTRICTCODE']:8s} | "
                  f"面积: {row['SHAPE_Area']:,.0f} 平方英尺 | "
                  f"长度: {row['SHAPE_Length']:,.0f} 英尺")
    
    print("\n4. 数据统计:")
    print(f"   总面积 (平方英尺): {df['SHAPE_Area'].sum():,.0f}")
    print(f"   平均面积 (平方英尺): {df['SHAPE_Area'].mean():,.0f}")
    print(f"   总长度 (英尺): {df['SHAPE_Length'].sum():,.0f}")
    
    print("\n5. 缺失值检查:")
    print(df.isnull().sum())
    
    print("\n6. 前5行数据预览:")
    print(df.head())
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)

