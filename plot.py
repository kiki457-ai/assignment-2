# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas", "matplotlib", "numpy"]
# ///

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---- 读取数据 ----
DATA_FILE = Path("data") / "eruptions.tsv"
OUT_DIR = Path("out")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "vei_vs_deaths.png"

df = pd.read_csv(DATA_FILE, sep='\t')

# 提取需要的列
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["VEI"] = pd.to_numeric(df["VEI"], errors="coerce")
df["Deaths"] = pd.to_numeric(df["Deaths"], errors="coerce")
df["Total Deaths"] = pd.to_numeric(df["Total Deaths"], errors="coerce")
df["Name"] = df["Name"].astype(str)

print(f"总记录数: {len(df)}")

# 只保留 VEI 和 Deaths 都有效的记录
valid = df.dropna(subset=["VEI", "Deaths"])
print(f"VEI和死亡人数都有记录的: {len(valid)} 条")

missing_deaths = df[df["Deaths"].isna()]
print(f"死亡人数未知的: {len(missing_deaths)} 条")

# ---- 画图 ----
fig, ax = plt.subplots(figsize=(11, 7))

# 散点：横轴VEI，纵轴死亡人数
ax.scatter(valid["VEI"], valid["Deaths"],
           alpha=0.5, s=50, edgecolors="white", linewidths=0.5,
           color="#d62728", zorder=2, label="有死亡记录的喷发")

# 纵轴用对数刻度
ax.set_yscale("log")
ax.set_ylim(0.5, max(valid["Deaths"]) * 2)

# 横轴设为整数刻度
ax.set_xticks(range(0, 9))
ax.set_xticklabels([f"VEI {i}" for i in range(0, 9)], rotation=45)

ax.set_xlabel("VEI（火山爆发指数）", fontsize=12)
ax.set_ylabel("死亡人数（对数刻度）", fontsize=12)
ax.set_title("火山爆发强度与死亡人数的关系", fontsize=14, fontweight="bold", pad=15)

ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

# 标注死亡人数最多的 5 次喷发
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
print(f"\n✅ 图片已保存到: {OUT_FILE}")