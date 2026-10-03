# /// script
# requires-python = ">=3.12"
# dependencies = ["requests", "pandas", "beautifulsoup4"]
# ///

import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
out_file = DATA_DIR / "eruptions.tsv"

url = "https://www.ngdc.noaa.gov/hazel/view/hazards/volcano/event-data"
print(f"Downloading volcanic eruption data from NOAA...")

# 网页返回的是HTML，用read_html解析里面的表格
tables = pd.read_html(url)
df = tables[0]

# 清理列名
df.columns = [c.strip() for c in df.columns]
print(f"Column names: {df.columns.tolist()}")
print(f"Total records: {len(df)}")
print(df.head())

df.to_csv(out_file, sep='\t', index=False)
print(f"\nSaved to: {out_file}")
print(f"File size: {out_file.stat().st_size / 1024:.1f} KB")