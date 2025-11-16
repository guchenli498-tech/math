"""
快速数据获取脚本 - Problem D
用于从NYC Open Data获取关键数据
"""

import pandas as pd
import requests
import json
from datetime import datetime

print("=" * 60)
print("Problem D - 数据获取工具")
print("=" * 60)

# NYC Open Data API端点
NYC_OPEN_DATA_BASE = "https://data.cityofnewyork.us/resource/"

# 数据源列表
DATA_SOURCES = {
    "311_rodent": {
        "name": "311服务请求 - 老鼠投诉",
        "dataset_id": "erm2-nwe9",
        "description": "用于分析老鼠问题与垃圾的关系",
        "filters": {
            "complaint_type": "Rodent",
            "borough": "MANHATTAN"
        }
    },
    "census": {
        "name": "人口普查数据",
        "dataset_id": "37yn-6x8y",
        "description": "人口、收入、贫困率等社会经济指标"
    },
    "buildings": {
        "name": "建筑数据",
        "dataset_id": "nqwf-w8eh",
        "description": "用于统计1-9单元住宅建筑"
    }
}

def download_311_rodent_data(limit=10000):
    """
    下载311老鼠投诉数据
    """
    print("\n1. 下载311老鼠投诉数据...")
    url = f"{NYC_OPEN_DATA_BASE}erm2-nwe9.json"
    
    # 构建查询参数
    params = {
        "$where": "complaint_type LIKE '%Rodent%' AND borough='MANHATTAN'",
        "$limit": limit,
        "$select": "unique_key,created_date,complaint_type,descriptor,incident_address,borough,latitude,longitude"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            print(f"   ✓ 成功下载 {len(df)} 条记录")
            df.to_csv("data_311_rodent.csv", index=False)
            print("   ✓ 已保存到 data_311_rodent.csv")
            return df
        else:
            print(f"   ✗ 错误: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"   ✗ 错误: {e}")
        print("   ⚠ 提示: 可以手动从以下网址下载:")
        print("   https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9")
        return None

def analyze_dsny_districts():
    """
    分析现有DSNY区域数据
    """
    print("\n2. 分析DSNY区域数据...")
    try:
        # 只读取关键列
        key_cols = ['DISTRICT', 'DISTRICTCODE', 'SHAPE_Area', 'SHAPE_Length']
        df = pd.read_csv('2025 CQU-MCM-ICM  Problems/Problems/2025_CQUICM_Problem_D_Data/DSNY_Districts_20251026.csv',
                        usecols=key_cols)
        
        # 筛选曼哈顿区域
        manhattan = df[df['DISTRICT'].str.startswith('MN', na=False)].copy()
        
        print(f"   ✓ 找到 {len(manhattan)} 个曼哈顿区域")
        print("\n   区域列表:")
        for idx, row in manhattan.iterrows():
            area_sqft = row['SHAPE_Area']
            area_acre = area_sqft / 43560  # 转换为英亩
            print(f"   {row['DISTRICT']:6s} | 代码: {row['DISTRICTCODE']:6s} | "
                  f"面积: {area_acre:,.1f} 英亩 ({area_sqft:,.0f} 平方英尺)")
        
        manhattan.to_csv("data_manhattan_districts.csv", index=False)
        print("\n   ✓ 已保存到 data_manhattan_districts.csv")
        return manhattan
        
    except Exception as e:
        print(f"   ✗ 错误: {e}")
        return None

def create_data_requirements_summary():
    """
    创建数据需求摘要
    """
    print("\n3. 生成数据需求摘要...")
    
    requirements = """
# 数据获取状态

## 已有数据 ✅
- DSNY区域地理数据 (DSNY_Districts_20251026.csv)
- 区域地图 (map.png)
- 数据字典 (Open-Data-Dictionary-DSNY-Districts-2024-01-30.xlsx)

## 需要获取的数据 ⚠️

### 高优先级
1. **311老鼠投诉数据**
   - 来源: NYC Open Data
   - URL: https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9
   - 筛选: Complaint Type = "Rodent", Borough = "MANHATTAN"
   - 用途: 分析老鼠问题与垃圾收集的关系

2. **人口普查数据**
   - 来源: NYC Open Data
   - URL: https://data.cityofnewyork.us/City-Government/Census-Demographics-at-the-Neighborhood-Tabulation-Area/37yn-6x8y
   - 需要字段: 人口、收入中位数、贫困率、住房单元数
   - 用途: 公平性分析、垃圾产生量估算

3. **建筑数据**
   - 来源: NYC Open Data
   - URL: https://data.cityofnewyork.us/Housing-Development/Building-Footprints/nqwf-w8eh
   - 筛选: 1-9单元住宅建筑
   - 用途: 分析垃圾桶政策影响

4. **垃圾产生量数据**
   - 来源: DSNY月度报告或估算
   - 需要: 各区域每日/每周垃圾量（吨或磅）
   - 用途: 确定收集频率需求

### 中优先级
5. **街道网络数据**
   - 来源: OpenStreetMap (通过osmnx库)
   - 用途: 路径规划

6. **当前收集调度数据**
   - 来源: DSNY或估算
   - 需要: 各区域收集频率、时间窗口
   - 用途: 优化基准

## 数据获取建议

1. **立即开始**: 下载311数据和人口普查数据（公开可用）
2. **估算数据**: 如果无法获取精确数据，使用问题描述中的信息进行估算
3. **文献调研**: 查找相关研究中的参数估计值

## 估算公式（基于问题描述）

- 全NYC: 24百万磅/天 = 12,000吨/天
- 曼哈顿约占NYC的20-25%，估算: 2,400-3,000吨/天
- 12个区域平均: 200-250吨/天/区域
- 每袋垃圾: 15-30磅，平均22.5磅
- 每车容量: 12吨 = 24,000磅 ≈ 1,067袋/车
"""
    
    with open("数据获取状态.md", "w", encoding="utf-8") as f:
        f.write(requirements)
    
    print("   ✓ 已保存到 数据获取状态.md")

if __name__ == "__main__":
    # 分析现有数据
    manhattan_districts = analyze_dsny_districts()
    
    # 尝试下载311数据（可能需要API密钥或手动下载）
    print("\n" + "=" * 60)
    print("提示: 311数据下载可能需要:")
    print("1. 访问 https://data.cityofnewyork.us 手动下载")
    print("2. 或使用SODA API（需要注册）")
    print("=" * 60)
    
    # 创建需求摘要
    create_data_requirements_summary()
    
    print("\n" + "=" * 60)
    print("数据准备完成！")
    print("=" * 60)
    print("\n下一步:")
    print("1. 访问NYC Open Data网站手动下载311数据")
    print("2. 下载人口普查数据")
    print("3. 开始建立基础模型框架")
    print("=" * 60)

