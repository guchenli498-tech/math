import pandas as pd
import sys

# 读取CSV文件，只读取前几行来分析结构
print("正在读取数据文件...")
try:
    # 先读取第一行看列名
    df_header = pd.read_csv('2025 CQU-MCM-ICM  Problems/Problems/2025_CQUICM_Problem_D_Data/DSNY_Districts_20251026.csv', nrows=0)
    print(f"\n总列数: {len(df_header.columns)}")
    print(f"\n前20个列名:")
    for i, col in enumerate(df_header.columns[:20]):
        print(f"  {i+1}. {col}")
    
    # 读取前5行数据，只读取前10列
    print("\n正在读取数据行...")
    df = pd.read_csv('2025 CQU-MCM-ICM  Problems/Problems/2025_CQUICM_Problem_D_Data/DSNY_Districts_20251026.csv', 
                     nrows=5, 
                     usecols=list(range(min(20, len(df_header.columns)))))
    
    print(f"\n数据行数: {len(df)}")
    print(f"\n前20列的数据:")
    print(df.head())
    
    # 检查关键列
    key_cols = ['DISTRICT', 'DISTRICTCODE', 'OBJECTID', 'SHAPE_Area', 'SHAPE_Length']
    print(f"\n关键列信息:")
    for col in key_cols:
        if col in df.columns:
            print(f"  {col}: 存在")
        else:
            print(f"  {col}: 不存在")
    
    # 如果有DISTRICT列，显示唯一值
    if 'DISTRICT' in df.columns:
        print(f"\n区域信息:")
        print(df[['DISTRICT', 'DISTRICTCODE']].drop_duplicates() if 'DISTRICTCODE' in df.columns else df['DISTRICT'].unique())
        
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

