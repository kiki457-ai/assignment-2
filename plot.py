# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas", "matplotlib", "numpy"]
# ///

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_FILE = Path("data") / "eruptions.tsv"
OUT_DIR = Path("out")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "vei_vs_deaths.png"

# ---- Load data ----
df = pd.read_csv(DATA_FILE, sep='\t')

# Convert types
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["VEI"] = pd.to_numeric(df["VEI"], errors="coerce")
df["Deaths"] = pd.to_numeric(df["Deaths"], errors="coerce")
df["Total Deaths"] = pd.to_numeric(df["Total Deaths"], errors="coerce")
df["Name"] = df["Name"].astype(str)

print(f"Total records: {len(df)}")

valid = df.dropna(subset=["VEI", "Deaths"])
print(f"Records with both VEI and Deaths: {len(valid)}")

# ---- Plot ----
fig, ax = plt.subplots(figsize=(11, 7))

ax.scatter(valid["VEI"], valid["Deaths"],
           alpha=0.5, s=50, edgecolors="white", linewidths=0.5,
           color="#d62728", zorder=2)

ax.set_yscale("log")
ax.set_ylim(0.5, max(valid["Deaths"]) * 2)

ax.set_xticks(range(0, 9))
ax.set_xticklabels([f"VEI {i}" for i in range(0, 9)], rotation=45)

ax.set_xlabel("VEI (Volcanic Explosivity Index)", fontsize=12)
ax.set_ylabel("Number of Deaths (Log Scale)", fontsize=12)
ax.set_title("Relationship between Volcanic Eruption Intensity and Fatalities",
             fontsize=14, fontweight="bold", pad=15)

ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

# Annotate top 5 deadliest
top_deaths = valid.nlargest(5, "Deaths")
for _, row in top_deaths.iterrows():
    year_str = int(row["Year"]) if pd.notna(row["Year"]) else "?"
    label = f"{row['Name']}\n({year_str})"
    ax.annotate(label,
                xy=(row["VEI"], row["Deaths"]),
                xytext=(15, 5), textcoords="offset points",
                fontsize=8.5, color="#333333", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#333333", alpha=0.6, lw=1.2))

plt.tight_layout()
plt.savefig(OUT_FILE, dpi=150, bbox_inches="tight")
print(f"\n✅ Plot saved to: {OUT_FILE}")