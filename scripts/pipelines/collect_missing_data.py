"""
收集缺失数据 - Problem D
1. 各区域收入/贫困率（任务2必需）
2. 1-9单元建筑分布（任务5必需）
"""
import requests
import pandas as pd
import json
from datetime import datetime

print("=" * 60)
print("缺失数据收集工具")
print("=" * 60)

# ==================== 1. 收集收入/贫困率数据 ====================
print("\n" + "=" * 60)
print("1. 收集各区域收入/贫困率数据")
print("=" * 60)

def collect_income_data():
    """尝试从多个数据源收集收入数据"""
    
    # 方法1: 尝试NYC Open Data - 人口普查数据
    print("\n方法1: 尝试NYC Open Data...")
    datasets = [
        {
            "name": "人口普查数据（NTA级别）",
            "url": "https://data.cityofnewyork.us/api/views/37yn-6x8y/rows.csv",
            "description": "包含收入、贫困率等"
        },
        {
            "name": "社区区划数据",
            "url": "https://data.cityofnewyork.us/api/views/kvif-wxim/rows.csv",
            "description": "社区社会经济数据"
        }
    ]
    
    for dataset in datasets:
        try:
            print(f"\n   尝试: {dataset['name']}")
            response = requests.get(dataset['url'], timeout=30)
            if response.status_code == 200:
                # 保存原始数据
                filename = f"data/external/census_data_raw.csv"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"   ✓ 成功下载到 {filename}")
                
                # 尝试读取和分析
                try:
                    df = pd.read_csv(filename, nrows=10)
                    print(f"   ✓ 数据列: {list(df.columns)[:10]}")
                    return filename
                except:
                    print("   ⚠ 数据格式可能有问题，但已保存")
                    return filename
            else:
                print(f"   ✗ HTTP {response.status_code}")
        except Exception as e:
            print(f"   ✗ 错误: {e}")
    
    return None

def collect_income_manual():
    """手动收集指南"""
    print("\n" + "-" * 60)
    print("手动收集收入/贫困率数据的方法：")
    print("-" * 60)
    print("\n方法A: 美国人口普查局")
    print("  1. 访问: https://data.census.gov/")
    print("  2. 搜索: 'Manhattan census tract income'")
    print("  3. 选择: American Community Survey (ACS) 5-Year Estimates")
    print("  4. 下载: Median Household Income 和 Poverty Rate")
    print("  5. 保存到: data/external/census_income_manual.csv")
    
    print("\n方法B: NYC Department of City Planning")
    print("  1. 访问: https://www.nyc.gov/site/planning/index.page")
    print("  2. 查找: Community Profiles 或 Census Data")
    print("  3. 下载曼哈顿各社区的收入数据")
    
    print("\n方法C: 使用估算值（如果找不到）")
    print("  - 可以基于区域位置和人口密度估算")
    print("  - 曼哈顿平均收入约$75,000-100,000")
    print("  - 贫困率约15-20%")

# ==================== 2. 收集建筑数据 ====================
print("\n" + "=" * 60)
print("2. 收集1-9单元建筑分布数据")
print("=" * 60)

def collect_building_data():
    """收集1-9单元建筑数据"""
    
    # 方法1: NYC Open Data - 建筑足迹
    print("\n方法1: 尝试NYC Open Data - 建筑数据...")
    datasets = [
        {
            "name": "建筑足迹数据",
            "url": "https://data.cityofnewyork.us/api/views/nqwf-w8eh/rows.csv",
            "description": "包含住宅单元数"
        },
        {
            "name": "建筑数据",
            "url": "https://data.cityofnewyork.us/api/views/7x9x-zs6i/rows.csv",
            "description": "建筑信息"
        }
    ]
    
    for dataset in datasets:
        try:
            print(f"\n   尝试: {dataset['name']}")
            response = requests.get(dataset['url'], timeout=60)
            if response.status_code == 200:
                filename = f"data/external/buildings_raw.csv"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"   ✓ 成功下载到 {filename}")
                
                # 检查文件大小
                import os
                size_mb = os.path.getsize(filename) / (1024 * 1024)
                print(f"   ✓ 文件大小: {size_mb:.2f} MB")
                
                if size_mb > 100:
                    print("   ⚠ 文件较大，建议使用筛选条件下载")
                
                return filename
            else:
                print(f"   ✗ HTTP {response.status_code}")
        except Exception as e:
            print(f"   ✗ 错误: {e}")
    
    return None

def collect_building_manual():
    """手动收集指南"""
    print("\n" + "-" * 60)
    print("手动收集建筑数据的方法：")
    print("-" * 60)
    print("\n方法A: NYC Open Data - 建筑足迹")
    print("  1. 访问: https://data.cityofnewyork.us/Housing-Development/Building-Footprints/nqwf-w8eh")
    print("  2. 点击 Filter:")
    print("     - borough = 'MANHATTAN'")
    print("     - residential_units 在 1-9 之间")
    print("  3. 点击 Export → CSV")
    print("  4. 保存到: data/external/buildings_1to9_units.csv")
    
    print("\n方法B: NYC Department of Buildings")
    print("  1. 访问: https://www.nyc.gov/site/buildings/index.page")
    print("  2. 查找: Building Data 或 Housing Data")
    
    print("\n方法C: 使用估算值（基于问题描述）")
    print("  - 问题说: 91%的建筑是1-9单元（全NYC）")
    print("  - 曼哈顿比例可能较低（约70-80%）")
    print("  - 可以基于区域人口估算建筑数量")

# ==================== 3. 处理收集到的数据 ====================
def process_collected_data():
    """处理收集到的数据，映射到DSNY区域"""
    print("\n" + "=" * 60)
    print("3. 处理收集到的数据")
    print("=" * 60)
    
    print("\n如果成功收集到数据，需要：")
    print("  1. 将数据映射到DSNY区域（MN01-MN12）")
    print("  2. 更新 district_features.csv")
    print("  3. 运行数据清理脚本")
    
    print("\n提示: 可以使用 preprocess_data.py 的扩展版本来处理")

# ==================== 主程序 ====================
if __name__ == "__main__":
    import sys
    
    # 检查requests库
    try:
        import requests
    except ImportError:
        print("错误: 需要安装 requests 库")
        print("运行: pip install requests")
        sys.exit(1)
    
    # 收集收入数据
    income_file = collect_income_data()
    if not income_file:
        collect_income_manual()
    
    # 收集建筑数据
    building_file = collect_building_data()
    if not building_file:
        collect_building_manual()
    
    # 处理数据
    process_collected_data()
    
    print("\n" + "=" * 60)
    print("数据收集完成！")
    print("=" * 60)
    print("\n下一步:")
    print("1. 检查 data/external/ 文件夹中的新数据")
    print("2. 如果API失败，按照手动指南下载")
    print("3. 如果都找不到，使用估算脚本生成数据")
    print("=" * 60)

