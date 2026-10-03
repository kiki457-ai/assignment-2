# /// script
# requires-python = ">=3.12"
# dependencies = ["requests", "pandas", "lxml", "html5lib"]
# ///

import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
out_file = DATA_DIR / "eruptions.tsv"

url = "https://www.ngdc.noaa.gov/hazel/view/hazards/volcano/event-data"
print(f"Downloading volcanic eruption data from NOAA...")

# 指定 flavor='lxml' 避免默认用 html5lib 时环境兼容问题
tables = pd.read_html(url, flavor='lxml')
df = tables[0]

# 清理列名，去掉前后空格
df.columns = [str(c).strip() for c in df.columns]
print(f"Column names: {df.columns.tolist()}")
print(f"Total records: {len(df)}")
print(df.head(3))

df.to_csv(out_file, sep='\t', index=False)
print(f"\n✅ Saved to: {out_file}")
print(f"File size: {out_file.stat().st_size / 1024:.1f} KB")