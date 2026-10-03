# Process

## Tools

I used Python with `pandas` for data loading and cleaning, `matplotlib` for visualization, and `uv` as the package manager and script runner. The data was fetched from NOAA NCEI's Significant Volcanic Eruptions Database using `requests`. An AI assistant (Qwen) helped write the initial versions of `fetch.py` and `plot.py`.

## Kept

I kept the log-scale y-axis for the death toll. Initially the AI generated a linear-scale scatter plot, but the death values span from 1 to over 10,000 — a linear scale compressed almost all points into the bottom of the chart, making it unreadable. Switching to `ax.set_yscale("log")` spread the points across the full height and revealed the actual distribution across orders of magnitude. I also kept the annotation of the top 5 deadliest eruptions, which adds concrete historical context to the abstract scatter pattern.

## Rejected

I rejected the AI's first attempt at using Chinese labels for axis titles and annotations. The plot rendered with square blocks (`[][][]`) instead of Chinese characters because matplotlib's default font on Windows doesn't include CJK glyphs. Rather than installing and configuring a Chinese font, I decided to make the entire visualization English-only, which is more appropriate for academic submission anyway. I also rejected using `Total Deaths` as the y-axis — the AI initially suggested it, but that column includes secondary effects (famine, tsunami) that conflate the direct relationship between VEI and eruption-caused fatalities. I chose `Deaths` (direct fatalities) instead.