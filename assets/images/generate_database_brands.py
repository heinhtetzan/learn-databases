"""
Generates the "Database Brands by Type" overview chart for Lesson 1.4.
Uses plain text labels in colored boxes -- no trademarked logos.
Run: python3 generate_database_brands.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

plt.rcParams["font.family"] = "DejaVu Sans"

NAVY = "#1f3a5f"
BLUE = "#2f6fb3"
TEAL = "#2a9d8f"
ORANGE = "#e76f51"
GOLD = "#e9c46a"
PURPLE = "#8e6db5"
GREY = "#6c757d"

columns = [
    ("Relational (SQL)", BLUE, ["PostgreSQL", "MySQL", "SQL Server", "Oracle DB", "SQLite"]),
    ("Key-Value", GOLD, ["Redis", "DynamoDB", "Memcached"]),
    ("Document", ORANGE, ["MongoDB", "Couchbase"]),
    ("Column-Family", PURPLE, ["Cassandra", "HBase"]),
    ("Graph", TEAL, ["Neo4j", "Neptune"]),
]

fig, ax = plt.subplots(figsize=(15.6, 6.5))
ax.set_xlim(0, 15.9); ax.set_ylim(0, 7); ax.axis("off")

col_w = 2.7
gap = 0.35
x = 0.3
for title, color, brands in columns:
    header = FancyBboxPatch((x, 5.9), col_w, 0.75, boxstyle="round,pad=0.02,rounding_size=0.08",
                             linewidth=1.6, edgecolor=NAVY, facecolor=color)
    ax.add_patch(header)
    ax.text(x + col_w/2, 6.27, title, ha="center", va="center", fontsize=10.5,
            fontweight="bold", color="white")

    y = 5.2
    for brand in brands:
        box = FancyBboxPatch((x + 0.15, y - 0.55), col_w - 0.3, 0.68,
                              boxstyle="round,pad=0.02,rounding_size=0.06",
                              linewidth=1.2, edgecolor=color, facecolor="white")
        ax.add_patch(box)
        ax.text(x + col_w/2, y - 0.21, brand, ha="center", va="center",
                fontsize=9.5, color=NAVY, fontweight="bold")
        y -= 0.85

    x += col_w + gap

ax.set_title("Database Brands, Grouped by Type", fontsize=16, fontweight="bold", color=NAVY, y=1.02)
plt.tight_layout()
plt.savefig("database-brands.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved database-brands.png")
