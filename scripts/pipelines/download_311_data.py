"""
下载311老鼠投诉数据 - Problem D
从NYC Open Data获取曼哈顿地区的老鼠投诉数据
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import sys

print("=" * 60)
print("311老鼠投诉数据下载工具")
print("=" * 60)

# 可选：从 https://data.cityofnewyork.us/profile/app_tokens 获取App Token
# 可以提高API请求限制
APP_TOKEN = None  # 如果有，填写在这里，例如: "YOUR_APP_TOKEN_HERE"

# 数据集ID
DATASET_ID = "erm2-nwe9"
BASE_URL = f"https://data.cityofnewyork.us/resource/{DATASET_ID}.json"

def download_311_data(use_token=True, limit=50000, years=2):
    """
    下载311老鼠投诉数据
    
    参数:
    - use_token: 是否使用App Token
    - limit: 最大记录数
    - years: 下载最近几年的数据
    """
    print(f"\n1. 准备下载最近{years}年的曼哈顿老鼠投诉数据...")
    
    # 计算日期范围
    start_date = (datetime.now() - timedelta(days=365*years)).strftime("%Y-%m-%d")
    
    # 构建查询参数
    params = {
        "$where": f"complaint_type LIKE '%Rodent%' AND borough='MANHATTAN' AND created_date >= '{start_date}'",
        "$limit": limit,
        "$select": "unique_key,created_date,complaint_type,descriptor,incident_address,borough,latitude,longitude,status",
        "$order": "created_date DESC"
    }
    
    # 添加App Token（如果提供）
    if use_token and APP_TOKEN:
        params["$$app_token"] = APP_TOKEN
        print("   ✓ 使用App Token")
    else:
        print("   ⚠ 未使用App Token（可能有限制）")
    
    print(f"   查询条件: 曼哈顿，最近{years}年，最多{limit}条记录")
    print("   正在下载...")
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=120)
        response.raise_for_status()
        
        data = response.json()
        
        if not data:
            print("   ⚠ 没有找到数据")
            return None
        
        df = pd.DataFrame(data)
        
        print(f"   ✓ 成功下载 {len(df)} 条记录")
        
        # 数据基本信息
        if 'created_date' in df.columns:
            df['created_date'] = pd.to_datetime(df['created_date'], errors='coerce')
            print(f"   时间范围: {df['created_date'].min()} 到 {df['created_date'].max()}")
        
        # 保存数据
        output_file = "../data/external/311_rodent_complaints_manhattan.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"   ✓ 已保存到 {output_file}")
        
        # 显示前几行
        print("\n   数据预览:")
        print(df.head())
        
        # 统计信息
        print("\n   统计信息:")
        print(f"   - 总记录数: {len(df)}")
        if 'complaint_type' in df.columns:
            print(f"   - 投诉类型分布:")
            print(df['complaint_type'].value_counts().head())
        if 'status' in df.columns:
            print(f"   - 状态分布:")
            print(df['status'].value_counts().head())
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"   ✗ 网络错误: {e}")
        print("\n   建议:")
        print("   1. 检查网络连接")
        print("   2. 直接从网页下载:")
        print("      https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9")
        print("   3. 在网页上设置筛选条件后导出CSV")
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
    print("\n1. 访问: https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9")
    print("\n2. 点击右上角 'Filter' 按钮")
    print("\n3. 设置筛选条件:")
    print("   - complaint_type 包含 'Rodent' 或 'Mouse' 或 'Rat'")
    print("   - borough = 'MANHATTAN'")
    print("   - created_date >= 最近2-3年（可选，减少数据量）")
    print("\n4. 点击 'Export' → 选择 'CSV'")
    print("\n5. 保存文件为: 311_rodent_manhattan.csv")
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
    df = download_311_data(use_token=bool(APP_TOKEN), limit=50000, years=2)
    
    if df is None:
        download_without_api()
    else:
        print("\n" + "=" * 60)
        print("下载完成！")
        print("=" * 60)
        print("\n下一步:")
        print("1. 检查数据质量")
        print("2. 将投诉位置映射到DSNY区域（MN01-MN12）")
        print("3. 分析各区域的老鼠投诉密度")
        print("=" * 60)

