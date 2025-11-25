"""
安装项目依赖
"""
import subprocess
import sys

packages = [
    'pandas>=1.3.0',
    'numpy>=1.20.0',
    'requests>=2.25.0',
    'geopandas>=0.10.0',
    'shapely>=2.0.0'
]

print("=" * 60)
print("安装项目依赖")
print("=" * 60)

for package in packages:
    print(f"\n正在安装 {package}...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        print(f"✓ {package} 安装成功")
    except subprocess.CalledProcessError:
        print(f"✗ {package} 安装失败")
        print("  提示: 如果geopandas安装失败，可能需要先安装GDAL")
        print("  Windows: 下载GDAL wheel文件或使用conda")
        print("  conda install -c conda-forge geopandas")

print("\n" + "=" * 60)
print("依赖安装完成！")
print("=" * 60)

