"""
Generates the "5 types of databases" overview chart for Lesson 1.3.
Run: python3 generate_database_types.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch
import random

plt.rcParams["font.family"] = "DejaVu Sans"

NAVY = "#1f3a5f"
BLUE = "#2f6fb3"
TEAL = "#2a9d8f"
ORANGE = "#e76f51"
GOLD = "#e9c46a"
PURPLE = "#8e6db5"
GREY = "#6c757d"

fig, axes = plt.subplots(1, 5, figsize=(19, 4.6))

# ---------------------------------------------------------------------------
# Panel 1: Relational (SQL)
# ---------------------------------------------------------------------------
ax = axes[0]
ax.set_xlim(0, 6); ax.set_ylim(0, 6); ax.axis("off")
rows, cols = 4, 3
x0, y0, w, h = 0.6, 1.3, 4.8, 3.6
cw, rh = w/cols, h/rows
headers = ["id", "name", "price"]
for r in range(rows):
    for c in range(cols):
        x = x0 + c*cw
        y = y0 + (rows-1-r)*rh
        color = BLUE if r == 0 else ("#eef3f7" if r % 2 == 0 else "white")
        rect = Rectangle((x, y), cw, rh, linewidth=1.2, edgecolor=NAVY, facecolor=color)
        ax.add_patch(rect)
        if r == 0:
            ax.text(x+cw/2, y+rh/2, headers[c], ha="center", va="center",
                    fontsize=9, fontweight="bold", color="white")
        else:
            ax.text(x+cw/2, y+rh/2, "...", ha="center", va="center", fontsize=8, color=GREY)
ax.set_title("Relational (SQL)", fontsize=12.5, fontweight="bold", color=NAVY, pad=10)
ax.text(3, 0.5, "Rows & columns,\nlinked by keys", ha="center", fontsize=8.5, color=GREY)

# ---------------------------------------------------------------------------
# Panel 2: Key-Value
# ---------------------------------------------------------------------------
ax = axes[1]
ax.set_xlim(0, 6); ax.set_ylim(0, 6); ax.axis("off")
key_box = FancyBboxPatch((0.5, 2.6), 1.9, 1.0, boxstyle="round,pad=0.02,rounding_size=0.1",
                          linewidth=1.6, edgecolor=NAVY, facecolor=GOLD)
ax.add_patch(key_box)
ax.text(1.45, 3.1, "session:42", ha="center", va="center", fontsize=8.5, fontweight="bold", color=NAVY)

arrow = FancyArrowPatch((2.5, 3.1), (3.4, 3.1), arrowstyle="-|>", mutation_scale=20, lw=2, color=NAVY)
ax.add_patch(arrow)

val_box = FancyBboxPatch((3.5, 2.2), 2.0, 1.8, boxstyle="round,pad=0.02,rounding_size=0.1",
                          linewidth=1.6, edgecolor=NAVY, facecolor=TEAL)
ax.add_patch(val_box)
ax.text(4.5, 3.1, "opaque\nvalue", ha="center", va="center", fontsize=9, fontweight="bold", color="white")
ax.set_title("Key-Value", fontsize=12.5, fontweight="bold", color=NAVY, pad=10)
ax.text(3, 0.9, "Look up a value\nby its key, instantly", ha="center", fontsize=8.5, color=GREY)

# ---------------------------------------------------------------------------
# Panel 3: Document
# ---------------------------------------------------------------------------
ax = axes[2]
ax.set_xlim(0, 6); ax.set_ylim(0, 6); ax.axis("off")
# stack of two documents behind, one in front
for dx, dy, alpha in [(0.5, 0.9, 0.4), (0.25, 1.15, 1.0)]:
    doc = FancyBboxPatch((1.0+dx-0.25, 1.3+dy-0.15), 3.2, 3.3, boxstyle="round,pad=0.02,rounding_size=0.08",
                          linewidth=1.4, edgecolor=NAVY, facecolor=ORANGE, alpha=alpha)
    ax.add_patch(doc)
lines_json = ['{ "title": "...",', '  "author": {', '     "name": "..." },', '  "tags": [".."] }']
for i, line in enumerate(lines_json):
    ax.text(1.55, 4.0 - i*0.55, line, ha="left", va="center", fontsize=7.6,
            color="white", family="monospace", fontweight="bold")
ax.set_title("Document", fontsize=12.5, fontweight="bold", color=NAVY, pad=10)
ax.text(3, 0.5, "Nested, flexible\nJSON-like records", ha="center", fontsize=8.5, color=GREY)

# ---------------------------------------------------------------------------
# Panel 4: Column-Family
# ---------------------------------------------------------------------------
ax = axes[3]
ax.set_xlim(0, 6); ax.set_ylim(0, 6); ax.axis("off")
random.seed(7)
row_keys = ["user_42", "user_43", "user_44"]
col_names = ["name", "city", "last_login", "plan"]
present = [
    [1,1,1,0],
    [1,0,1,1],
    [1,1,0,0],
]
x0, y0, cw, rh = 1.1, 1.2, 1.0, 1.05
for ri, rk in enumerate(row_keys):
    y = y0 + (len(row_keys)-1-ri)*rh
    ax.text(0.15, y+rh/2, rk, ha="left", va="center", fontsize=7.5, fontweight="bold", color=NAVY)
    for ci in range(4):
        x = x0 + ci*cw
        filled = present[ri][ci]
        color = PURPLE if filled else "#eeeeee"
        rect = Rectangle((x, y), cw-0.08, rh-0.15, linewidth=1, edgecolor=NAVY, facecolor=color)
        ax.add_patch(rect)
        if filled:
            ax.text(x+cw/2-0.04, y+(rh-0.15)/2, col_names[ci], ha="center", va="center",
                     fontsize=6.3, color="white")
ax.set_title("Column-Family", fontsize=12.5, fontweight="bold", color=NAVY, pad=10)
ax.text(3, 0.4, "Sparse columns per row —\neach row can differ", ha="center", fontsize=8.5, color=GREY)

# ---------------------------------------------------------------------------
# Panel 5: Graph
# ---------------------------------------------------------------------------
ax = axes[4]
ax.set_xlim(0, 6); ax.set_ylim(0, 6); ax.axis("off")
nodes = {"Alice": (1.2, 4.5), "Bob": (4.4, 4.7), "Carla": (4.8, 1.8), "Dan": (1.0, 1.6), "Eve": (3.0, 3.1)}
edges = [("Alice","Bob"), ("Bob","Carla"), ("Alice","Dan"), ("Dan","Carla"), ("Alice","Eve"), ("Eve","Carla")]
for a, b in edges:
    x1,y1 = nodes[a]; x2,y2 = nodes[b]
    ax.plot([x1,x2],[y1,y2], color=GREY, lw=1.3, zorder=0)
for name, (x,y) in nodes.items():
    circ = Circle((x,y), 0.55, facecolor=NAVY, edgecolor=NAVY, lw=1.4, zorder=2)
    ax.add_patch(circ)
    ax.text(x, y, name[:2], ha="center", va="center", fontsize=8.5, color="white", fontweight="bold", zorder=3)
ax.set_title("Graph", fontsize=12.5, fontweight="bold", color=NAVY, pad=10)
ax.text(3, 0.4, "Relationships are\nstored directly", ha="center", fontsize=8.5, color=GREY)

fig.suptitle("5 Common Types of Databases", fontsize=16, fontweight="bold", color=NAVY, y=1.06)
plt.tight_layout()
plt.savefig("database-types-overview.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved database-types-overview.png")
