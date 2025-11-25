"""
从原始 DSNY CSV 中重建 WKT 列并直接保存为 Pickle，避免再次被 CSV 解析破坏
"""
import csv
from pathlib import Path
import geopandas as gpd
from shapely import wkt

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "DSNY_Districts_20251026.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "DSNY_Districts_Cleaned.pkl"

print("=" * 60)
print("修复 DSNY WKT 并导出 Pickle")
print("=" * 60)

if not RAW_PATH.exists():
    print(f"✗ 找不到原始文件: {RAW_PATH}")
    exit(1)

rows = []
with RAW_PATH.open("r", encoding="utf-8") as src:
    reader = csv.reader(src)
    header = next(reader, None)
    if not header:
        print("✗ 原始文件为空")
        exit(1)

with RAW_PATH.open("r", encoding="utf-8") as src:
    next(src)  # 跳过头

    def clean_wkt_string(wkt_str):
        if not isinstance(wkt_str, str):
            return None

        wkt_str = wkt_str.strip().strip('"').replace('"', "")
        wkt_str = wkt_str.replace("MULT POLYGON", "MULTIPOLYGON")

        start = wkt_str.find("MULTIPOLYGON")
        if start == -1:
            return None

        wkt_clean = wkt_str[start:].strip()
        end_idx = wkt_clean.rfind(")))")
        if end_idx != -1:
            wkt_clean = wkt_clean[: end_idx + 3]

        try:
            wkt.loads(wkt_clean)
            return wkt_clean
        except Exception:
            return None

    for line in src:
        if "MULTIPOLYGON" not in line:
            continue
        wkt_start = line.find("MULTIPOLYGON")
        prefix = line[:wkt_start]
        wkt_raw = line[wkt_start:]

        parts = [p.strip().strip('"') for p in prefix.split(",") if p.strip()]
        if len(parts) < 2:
            continue
        district = parts[0]
        district_code = parts[1]

        wkt_final = clean_wkt_string(wkt_raw)
        if not wkt_final:
            continue

        try:
            geom = wkt.loads(wkt_final)
        except Exception as exc:
            preview = wkt_final[:120] + ("..." if len(wkt_final) > 120 else "")
            print(f"✗ 无法解析几何：{district} - {exc}")
            print(f"   片段: {preview}")
            continue

        rows.append({"DISTRICT": district, "DISTRICTCODE": district_code, "geometry": geom})

if not rows:
    print("✗ 没有可用的几何数据")
    exit(1)

gdf = gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:4326")
gdf.to_pickle(OUTPUT_PATH)

print(f"✓ 保存 {len(gdf)} 个区域到 {OUTPUT_PATH}")

