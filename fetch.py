# /// script
# requires-python = ">=3.12"
# dependencies = ["requests"]
# ///

import requests
from pathlib import Path

# NOAA NCEI Significant Volcanic Eruptions Database
URL = "https://www.ngdc.noaa.gov/hazel/view/hazards/volcano/event-data"

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
out_file = DATA_DIR / "eruptions.tsv"

print(f"Downloading volcanic eruption data from NOAA...")
response = requests.get(URL)
response.raise_for_status()

with open(out_file, "wb") as f:
    f.write(response.content)

print(f"✅ Saved to: {out_file}")
print(f"File size: {out_file.stat().st_size / 1024:.1f} KB")