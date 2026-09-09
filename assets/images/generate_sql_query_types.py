"""
Generates the "Types of SQL Queries" chart for Lesson 2.3 (DDL/DML/DQL/DCL/TCL).
Run: python3 generate_sql_query_types.py
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
    ("DDL\nData Definition", BLUE, ["CREATE", "ALTER", "DROP", "TRUNCATE"], "Defines structure"),
    ("DML\nData Manipulation", TEAL, ["INSERT", "UPDATE", "DELETE"], "Changes data"),
    ("DQL\nData Query", GOLD, ["SELECT"], "Reads data"),
    ("DCL\nData Control", ORANGE, ["GRANT", "REVOKE"], "Manages permissions"),
    ("TCL\nTransaction Control", PURPLE, ["BEGIN", "COMMIT", "ROLLBACK", "SAVEPOINT"], "Groups statements safely"),
]

fig, ax = plt.subplots(figsize=(17.5, 6.6))
ax.set_xlim(0, 17.8); ax.set_ylim(0, 7); ax.axis("off")

col_w = 3.1
gap = 0.35
x = 0.3
for title, color, items, subtitle in columns:
    header = FancyBboxPatch((x, 5.75), col_w, 0.95, boxstyle="round,pad=0.02,rounding_size=0.08",
                             linewidth=1.6, edgecolor=NAVY, facecolor=color)
    ax.add_patch(header)
    ax.text(x + col_w/2, 6.22, title, ha="center", va="center", fontsize=11,
            fontweight="bold", color="white", linespacing=1.3)

    y = 5.0
    for item in items:
        box = FancyBboxPatch((x + 0.15, y - 0.55), col_w - 0.3, 0.68,
                              boxstyle="round,pad=0.02,rounding_size=0.06",
                              linewidth=1.2, edgecolor=color, facecolor="white")
        ax.add_patch(box)
        ax.text(x + col_w/2, y - 0.21, item, ha="center", va="center",
                fontsize=10, color=NAVY, fontweight="bold", family="monospace")
        y -= 0.85

    ax.text(x + col_w/2, 0.5, subtitle, ha="center", va="center", fontsize=9, color="#555", style="italic")

    x += col_w + gap

ax.set_title("Types of SQL Queries", fontsize=17, fontweight="bold", color=NAVY, y=1.03)
plt.tight_layout()
plt.savefig("sql-query-types.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved sql-query-types.png")
