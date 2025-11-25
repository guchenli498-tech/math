"""
下载人口普查数据 - Problem D
从NYC Open Data获取人口和社会经济数据
"""

import requests
import pandas as pd
import sys

print("=" * 60)
print("人口普查数据下载工具")
print("=" * 60)

# 数据集ID
DATASET_ID = "37yn-6x8y"
BASE_URL = f"https://data.cityofnewyork.us/resource/{DATASET_ID}.json"

def download_census_data():
    """
    下载人口普查数据（按NTA划分）
    """
    print("\n1. 准备下载人口普查数据...")
    
    # 需要的字段
    select_fields = [
        "nta_code", "nta_name", 
        "total_population", 
        "median_household_income",
        "poverty_rate",
        "total_housing_units",
        "borough"
    ]
    
    params = {
        "$limit": 200,  # NTA数量有限
        "$select": ",".join(select_fields),
        "$where": "borough='Manhattan' OR borough='MANHATTAN'"
    }
    
    print("   正在下载...")
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        
        if not data:
            print("   ⚠ 没有找到数据")
            return None
        
        df = pd.DataFrame(data)
        
        print(f"   ✓ 成功下载 {len(df)} 条记录")
        
        # 保存数据
        output_file = "census_nta_manhattan.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"   ✓ 已保存到 {output_file}")
        
        # 显示前几行
        print("\n   数据预览:")
        print(df.head())
        
        # 统计信息
        print("\n   统计信息:")
        print(f"   - 总NTA数: {len(df)}")
        if 'total_population' in df.columns:
            try:
                total_pop = pd.to_numeric(df['total_population'], errors='coerce').sum()
                print(f"   - 总人口: {total_pop:,.0f}")
            except:
                pass
        
        print("\n   ⚠ 注意: 这个数据是按NTA划分的，需要映射到DSNY区域（MN01-MN12）")
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"   ✗ 网络错误: {e}")
        print("\n   建议: 直接从网页下载")
        print("   https://data.cityofnewyork.us/City-Government/Census-Demographics-at-the-Neighborhood-Tabulation-Area/37yn-6x8y")
        return None
    except Exception as e:
        print(f"   ✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None

def download_without_api():
    """
    提供手动下载指南
    """
    print("\n" + "=" * 60)
    print("手动下载指南")
    print("=" * 60)
    print("\n如果API下载失败，可以手动下载:")
    print("\n1. 访问: https://data.cityofnewyork.us/City-Government/Census-Demographics-at-the-Neighborhood-Tabulation-Area/37yn-6x8y")
    print("\n2. 点击右上角 'Export' → 选择 'CSV'")
    print("\n3. 保存文件为: census_nta_manhattan.csv")
    print("\n4. 注意: 需要筛选曼哈顿的数据，或下载后筛选")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    # 检查是否安装了requests
    try:
        import requests
    except ImportError:
        print("错误: 需要安装 requests 库")
        print("运行: pip install requests")
        sys.exit(1)
    
    # 尝试下载
    df = download_census_data()
    
    if df is None:
        download_without_api()
    else:
        print("\n" + "=" * 60)
        print("下载完成！")
        print("=" * 60)
        print("\n下一步:")
        print("1. 将NTA数据映射到DSNY区域（MN01-MN12）")
        print("2. 计算各区域的人口、收入、贫困率等指标")
        print("3. 用于公平性分析和垃圾产生量估算")
        print("=" * 60)

