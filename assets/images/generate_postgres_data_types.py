"""
Generates the "PostgreSQL Data Types, Grouped" chart for Lesson 2.4.
Run: python3 generate_postgres_data_types.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams["font.family"] = "DejaVu Sans"

NAVY = "#1f3a5f"
BLUE = "#2f6fb3"
TEAL = "#2a9d8f"
ORANGE = "#e76f51"
GOLD = "#e9c46a"
PURPLE = "#8e6db5"

columns = [
    ("Numeric", BLUE, ["INTEGER", "BIGINT", "DECIMAL(p,s)", "SERIAL"]),
    ("Text", TEAL, ["TEXT", "VARCHAR(n)", "CHAR(n)"]),
    ("Boolean", GOLD, ["BOOLEAN"]),
    ("Date / Time", ORANGE, ["DATE", "TIME", "TIMESTAMP", "TIMESTAMPTZ", "INTERVAL"]),
    ("PostgreSQL-Special", PURPLE, ["UUID", "JSONB", "ARRAY", "ENUM"]),
]

fig, ax = plt.subplots(figsize=(17.5, 6.8))
ax.set_xlim(0, 17.8); ax.set_ylim(0, 7.2); ax.axis("off")

col_w = 3.1
gap = 0.35
x = 0.3
for title, color, items in columns:
    header = FancyBboxPatch((x, 5.95), col_w, 0.75, boxstyle="round,pad=0.02,rounding_size=0.08",
                             linewidth=1.6, edgecolor=NAVY, facecolor=color)
    ax.add_patch(header)
    ax.text(x + col_w/2, 6.32, title, ha="center", va="center", fontsize=11,
            fontweight="bold", color="white")

    y = 5.25
    for item in items:
        box = FancyBboxPatch((x + 0.15, y - 0.55), col_w - 0.3, 0.68,
                              boxstyle="round,pad=0.02,rounding_size=0.06",
                              linewidth=1.2, edgecolor=color, facecolor="white")
        ax.add_patch(box)
        ax.text(x + col_w/2, y - 0.21, item, ha="center", va="center",
                fontsize=9.5, color=NAVY, fontweight="bold", family="monospace")
        y -= 0.85

    x += col_w + gap

ax.set_title("PostgreSQL Data Types, Grouped", fontsize=17, fontweight="bold", color=NAVY, y=1.02)
plt.tight_layout()
plt.savefig("postgres-data-types.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved postgres-data-types.png")
