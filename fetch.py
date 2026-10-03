# /// script
# requires-python = ">=3.12"
# dependencies = ["requests", "pandas", "beautifulsoup4"]
# ///

import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
out_file = DATA_DIR / "eruptions.tsv"

url = "https://www.ngdc.noaa.gov/hazel/view/hazards/volcano/event-data"
print(f"Downloading volcanic eruption data from NOAA...")

# 用 requests 获取页面 HTML
response = requests.get(url, timeout=30)
response.raise_for_status()

# 用 BeautifulSoup 解析表格
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table')

if not table:
    print("ERROR: No table found on the page!")
    print("Page title:", soup.title.string if soup.title else "No title")
    # 打印页面前200个字符看看是什么
    print("Page preview:", response.text[:300])
    raise RuntimeError("No table found")

# 用 pandas 读取 BeautifulSoup 找到的表格
df = pd.read_html(str(table))[0]

# 清理列名
df.columns = [str(c).strip() for c in df.columns]
print(f"Column names: {df.columns.tolist()}")
print(f"Total records: {len(df)}")
print(df.head(3))

df.to_csv(out_file, sep='\t', index=False)
print(f"\n✅ Saved to: {out_file}")
print(f"File size: {out_file.stat().st_size / 1024:.1f} KB")