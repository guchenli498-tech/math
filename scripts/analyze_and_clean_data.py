"""
数据分析和清理 - Problem D
1. 分析数据质量
2. 处理异常值
3. 生成清理后的数据
4. 生成分析报告
"""
import pandas as pd
import numpy as np
import json
from datetime import datetime

print("=" * 60)
print("数据分析和清理工具")
print("=" * 60)

# ==================== 1. 分析311投诉数据 ====================
print("\n" + "=" * 60)
print("1. 分析311老鼠投诉数据")
print("=" * 60)

def analyze_311_data():
    """分析311投诉数据质量"""
    try:
        df = pd.read_csv('../data/external/311_rodent_complaints_manhattan.csv')
        print(f"\n   总记录数: {len(df):,}")
        print(f"   列数: {len(df.columns)}")
        print(f"   列名: {list(df.columns)}")
        
        # 缺失值分析
        print("\n   缺失值统计:")
        missing = df.isnull().sum()
        missing_pct = (missing / len(df) * 100).round(2)
        for col in df.columns:
            if missing[col] > 0:
                print(f"     {col}: {missing[col]:,} ({missing_pct[col]}%)")
        
        # 坐标数据质量
        print("\n   坐标数据质量:")
        valid_coords = df.dropna(subset=['latitude', 'longitude'])
        print(f"     有效坐标记录: {len(valid_coords):,} ({len(valid_coords)/len(df)*100:.1f}%)")
        
        # 检查坐标范围（曼哈顿大致范围）
        if len(valid_coords) > 0:
            lat_range = (valid_coords['latitude'].min(), valid_coords['latitude'].max())
            lon_range = (valid_coords['longitude'].min(), valid_coords['longitude'].max())
            print(f"     纬度范围: {lat_range[0]:.4f} - {lat_range[1]:.4f}")
            print(f"     经度范围: {lon_range[0]:.4f} - {lon_range[1]:.4f}")
            
            # 检查异常坐标（曼哈顿大致范围：40.7-40.9, -74.0--73.9）
            outliers = valid_coords[
                (valid_coords['latitude'] < 40.7) | (valid_coords['latitude'] > 40.9) |
                (valid_coords['longitude'] < -74.05) | (valid_coords['longitude'] > -73.9)
            ]
            if len(outliers) > 0:
                print(f"     ⚠️ 异常坐标记录: {len(outliers)} 条")
            else:
                print(f"     ✓ 坐标范围正常")
        
        # 时间数据质量
        if 'created_date' in df.columns:
            print("\n   时间数据质量:")
            df['created_date'] = pd.to_datetime(df['created_date'], errors='coerce')
            valid_dates = df.dropna(subset=['created_date'])
            print(f"     有效日期记录: {len(valid_dates):,}")
            if len(valid_dates) > 0:
                print(f"     时间范围: {valid_dates['created_date'].min()} 到 {valid_dates['created_date'].max()}")
                
                # 检查未来日期（异常）
                future_dates = valid_dates[valid_dates['created_date'] > pd.Timestamp.now()]
                if len(future_dates) > 0:
                    print(f"     ⚠️ 未来日期记录: {len(future_dates)} 条")
        
        # 重复记录检查
        print("\n   重复记录检查:")
        duplicates = df.duplicated(subset=['unique_key']).sum() if 'unique_key' in df.columns else 0
        print(f"     重复记录: {duplicates} 条")
        
        return df
        
    except Exception as e:
        print(f"   ✗ 错误: {e}")
        return None

# ==================== 2. 分析区域特征数据 ====================
print("\n" + "=" * 60)
print("2. 分析区域特征数据")
print("=" * 60)

def analyze_district_features():
    """分析区域特征数据质量"""
    try:
        # 分析基础版本
        df_base = pd.read_csv('../data/features/district_features.csv')
        print(f"\n   基础版本 (district_features.csv):")
        print(f"     区域数: {len(df_base)}")
        print(f"     列数: {len(df_base.columns)}")
        
        # 分析增强版本
        df_enhanced = pd.read_csv('../data/features/district_features_enhanced.csv')
        print(f"\n   增强版本 (district_features_enhanced.csv):")
        print(f"     区域数: {len(df_enhanced)}")
        print(f"     列数: {len(df_enhanced.columns)}")
        
        # 缺失值分析
        print("\n   缺失值统计:")
        missing = df_enhanced.isnull().sum()
        for col in df_enhanced.columns:
            if missing[col] > 0:
                print(f"     {col}: {missing[col]} ({missing[col]/len(df_enhanced)*100:.1f}%)")
        
        if missing.sum() == 0:
            print("     ✓ 无缺失值")
        
        # 数值范围检查
        print("\n   数值范围检查:")
        numeric_cols = df_enhanced.select_dtypes(include=[np.number]).columns
        
        for col in ['estimated_population', 'weekly_waste_tons', 'median_household_income', 
                   'poverty_rate', 'buildings_1to9_units_count']:
            if col in df_enhanced.columns:
                values = df_enhanced[col]
                print(f"     {col}:")
                print(f"       最小值: {values.min():,.0f}")
                print(f"       最大值: {values.max():,.0f}")
                print(f"       平均值: {values.mean():,.0f}")
                print(f"       中位数: {values.median():,.0f}")
                
                # 检查异常值（使用IQR方法）
                Q1 = values.quantile(0.25)
                Q3 = values.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = values[(values < lower_bound) | (values > upper_bound)]
                if len(outliers) > 0:
                    print(f"       ⚠️ 异常值: {len(outliers)} 个区域")
                else:
                    print(f"       ✓ 无异常值")
        
        # 逻辑一致性检查
        print("\n   逻辑一致性检查:")
        
        # 检查：垃圾量应该与人口相关
        if 'estimated_population' in df_enhanced.columns and 'weekly_waste_tons' in df_enhanced.columns:
            waste_per_person = (df_enhanced['weekly_waste_tons'] * 2000 / df_enhanced['estimated_population']).mean()
            print(f"     人均每周垃圾量: {waste_per_person:.2f} 磅")
            if waste_per_person < 10 or waste_per_person > 30:
                print(f"     ⚠️ 人均垃圾量异常（正常范围约15-25磅/周）")
            else:
                print(f"     ✓ 人均垃圾量正常")
        
        # 检查：贫困率应该在合理范围
        if 'poverty_rate' in df_enhanced.columns:
            poverty_range = (df_enhanced['poverty_rate'].min(), df_enhanced['poverty_rate'].max())
            if poverty_range[0] < 0 or poverty_range[1] > 50:
                print(f"     ⚠️ 贫困率范围异常: {poverty_range[0]:.1f}% - {poverty_range[1]:.1f}%")
            else:
                print(f"     ✓ 贫困率范围正常: {poverty_range[0]:.1f}% - {poverty_range[1]:.1f}%")
        
        return df_enhanced
        
    except Exception as e:
        print(f"   ✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None

# ==================== 3. 清理数据 ====================
print("\n" + "=" * 60)
print("3. 清理数据")
print("=" * 60)

def clean_311_data(df):
    """清理311投诉数据"""
    if df is None:
        return None
    
    print("\n   清理步骤:")
    df_clean = df.copy()
    original_count = len(df_clean)
    
    # 1. 移除重复记录
    if 'unique_key' in df_clean.columns:
        duplicates = df_clean.duplicated(subset=['unique_key']).sum()
        if duplicates > 0:
            df_clean = df_clean.drop_duplicates(subset=['unique_key'])
            print(f"     1. 移除重复记录: {duplicates} 条")
    
    # 2. 移除无效坐标
    invalid_coords = df_clean[
        df_clean['latitude'].isna() | 
        df_clean['longitude'].isna() |
        (df_clean['latitude'] < 40.7) | (df_clean['latitude'] > 40.9) |
        (df_clean['longitude'] < -74.05) | (df_clean['longitude'] > -73.9)
    ]
    if len(invalid_coords) > 0:
        df_clean = df_clean.drop(invalid_coords.index)
        print(f"     2. 移除无效坐标: {len(invalid_coords)} 条")
    
    # 3. 移除未来日期
    if 'created_date' in df_clean.columns:
        df_clean['created_date'] = pd.to_datetime(df_clean['created_date'], errors='coerce')
        future_dates = df_clean[df_clean['created_date'] > pd.Timestamp.now()]
        if len(future_dates) > 0:
            df_clean = df_clean.drop(future_dates.index)
            print(f"     3. 移除未来日期: {len(future_dates)} 条")
    
    removed = original_count - len(df_clean)
    print(f"\n     清理后记录数: {len(df_clean):,} (移除了 {removed} 条)")
    
    return df_clean

def clean_district_features(df):
    """清理区域特征数据"""
    if df is None:
        return None
    
    print("\n   清理步骤:")
    df_clean = df.copy()
    
    # 确保所有区域都存在
    expected_districts = [f'MN{i:02d}' for i in range(1, 13)]
    missing = set(expected_districts) - set(df_clean['district'].values)
    if missing:
        print(f"     ⚠️ 缺失区域: {missing}")
    
    # 处理负值（不应该有负值）
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        negatives = (df_clean[col] < 0).sum()
        if negatives > 0:
            print(f"     ⚠️ {col} 有 {negatives} 个负值，已设为0")
            df_clean[col] = df_clean[col].clip(lower=0)
    
    # 处理异常大的值（使用IQR方法）
    for col in ['estimated_population', 'weekly_waste_tons']:
        if col in df_clean.columns:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            upper_bound = Q3 + 3 * IQR  # 使用3倍IQR，更宽松
            outliers = df_clean[df_clean[col] > upper_bound]
            if len(outliers) > 0:
                print(f"     ⚠️ {col} 有 {len(outliers)} 个异常大值，已限制到上限")
                df_clean[col] = df_clean[col].clip(upper=upper_bound)
    
    print(f"     ✓ 清理完成")
    
    return df_clean

# ==================== 4. 保存清理后的数据 ====================
print("\n" + "=" * 60)
print("4. 保存清理后的数据")
print("=" * 60)

def save_cleaned_data(df_311_clean, df_district_clean):
    """保存清理后的数据"""
    if df_311_clean is not None:
        output_file = '../data/processed/311_rodent_complaints_cleaned.csv'
        df_311_clean.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n   ✓ 清理后的311数据已保存: {output_file}")
        print(f"     记录数: {len(df_311_clean):,}")
    
    if df_district_clean is not None:
        output_file = '../data/processed/district_features_cleaned.csv'
        df_district_clean.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"   ✓ 清理后的区域特征已保存: {output_file}")
        print(f"     区域数: {len(df_district_clean)}")

# ==================== 5. 生成分析报告 ====================
print("\n" + "=" * 60)
print("5. 生成分析报告")
print("=" * 60)

def generate_report(df_311, df_311_clean, df_district):
    """生成数据分析报告"""
    report = {
        "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data_sources": {
            "311_complaints": {
                "original_count": len(df_311) if df_311 is not None else 0,
                "cleaned_count": len(df_311_clean) if df_311_clean is not None else 0,
                "removed_count": (len(df_311) - len(df_311_clean)) if (df_311 is not None and df_311_clean is not None) else 0
            },
            "district_features": {
                "district_count": len(df_district) if df_district is not None else 0
            }
        },
        "data_quality": {},
        "issues_found": [],
        "recommendations": []
    }
    
    # 311数据质量
    if df_311 is not None:
        missing_coords = df_311[df_311['latitude'].isna() | df_311['longitude'].isna()].shape[0]
        report["data_quality"]["311_complaints"] = {
            "missing_coordinates": missing_coords,
            "missing_coordinates_pct": round(missing_coords / len(df_311) * 100, 2),
            "duplicates": df_311.duplicated(subset=['unique_key']).sum() if 'unique_key' in df_311.columns else 0
        }
    
    # 区域特征数据质量
    if df_district is not None:
        missing_values = df_district.isnull().sum().sum()
        report["data_quality"]["district_features"] = {
            "missing_values": int(missing_values),
            "completeness": round((1 - missing_values / (len(df_district) * len(df_district.columns))) * 100, 2)
        }
    
    # 转换numpy类型为Python原生类型
    def convert_numpy_types(obj):
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, dict):
            return {key: convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy_types(item) for item in obj]
        return obj
    
    report = convert_numpy_types(report)
    
    # 保存报告
    report_file = '../data/processed/data_quality_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n   ✓ 分析报告已保存: {report_file}")
    
    # 生成文本报告
    text_report = f"""
数据质量分析报告
生成时间: {report['report_date']}

=== 数据概览 ===
311投诉数据:
  - 原始记录数: {report['data_sources']['311_complaints']['original_count']:,}
  - 清理后记录数: {report['data_sources']['311_complaints']['cleaned_count']:,}
  - 移除记录数: {report['data_sources']['311_complaints']['removed_count']:,}

区域特征数据:
  - 区域数量: {report['data_sources']['district_features']['district_count']}

=== 数据质量 ===
311投诉数据:
  - 缺失坐标: {report['data_quality'].get('311_complaints', {}).get('missing_coordinates', 0):,}
  - 重复记录: {report['data_quality'].get('311_complaints', {}).get('duplicates', 0):,}

区域特征数据:
  - 缺失值总数: {report['data_quality'].get('district_features', {}).get('missing_values', 0)}
  - 完整度: {report['data_quality'].get('district_features', {}).get('completeness', 0):.1f}%

=== 建议 ===
1. 311数据已清理，可用于分析
2. 区域特征数据完整，可直接使用
3. 部分数据为估算值，需在报告中说明
"""
    
    text_report_file = '../data/processed/data_quality_report.txt'
    with open(text_report_file, 'w', encoding='utf-8') as f:
        f.write(text_report)
    print(f"   ✓ 文本报告已保存: {text_report_file}")

# ==================== 主程序 ====================
if __name__ == "__main__":
    # 分析数据
    df_311 = analyze_311_data()
    df_district = analyze_district_features()
    
    # 清理数据
    df_311_clean = clean_311_data(df_311)
    df_district_clean = clean_district_features(df_district)
    
    # 保存清理后的数据
    save_cleaned_data(df_311_clean, df_district_clean)
    
    # 生成报告
    generate_report(df_311, df_311_clean, df_district_clean)
    
    print("\n" + "=" * 60)
    print("数据分析和清理完成！")
    print("=" * 60)
    print("\n输出文件:")
    print("  - data/processed/311_rodent_complaints_cleaned.csv")
    print("  - data/processed/district_features_cleaned.csv")
    print("  - data/processed/data_quality_report.json")
    print("  - data/processed/data_quality_report.txt")
    print("=" * 60)

