"""
修复 DSNY_Districts_20251026.csv 中被拆散的 WKT 列
原始文件的 multipolygon 列被拆成了数千个空列，需要重新拼接
"""
import csv
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "DSNY_Districts_20251026.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "DSNY_Districts_20251026_clean.csv"

print("=" * 60)
print("修复 DSNY WKT 列")
print("=" * 60)

if not RAW_PATH.exists():
    print(f"✗ 找不到原始文件: {RAW_PATH}")
    exit(1)

row_count = 0
valid_wkt = 0

with RAW_PATH.open("r", encoding="utf-8") as src, OUTPUT_PATH.open(
    "w", encoding="utf-8", newline=""
) as dst:
    # 使用 csv.reader 按标准 CSV 解析
    reader = csv.reader(src)
    header = next(reader, None)
    if not header:
        print("✗ 原始文件为空")
        exit(1)
    base_header = header[:5]
    writer = csv.writer(dst)
    writer.writerow(base_header + ["WKT"])

    for row in reader:
        if len(row) < 6:
            continue
        base_cols = [
            row[0].strip(),
            row[1].strip(),
            row[2].strip(),
            row[3].strip(),
            row[4].strip(),
        ]
        wkt = row[5].strip()
        row_count += 1
        if wkt:
            valid_wkt += 1
        writer.writerow(base_cols + [wkt])

print(f"✓ 已处理 {row_count} 行，非空WKT {valid_wkt} 行")
print(f"✓ 输出文件: {OUTPUT_PATH}")

