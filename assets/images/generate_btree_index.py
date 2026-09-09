"""
Generates a B-Tree index structure chart for Lesson 2.15.
Run: python3 generate_btree_index.py
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
GREY = "#6c757d"

fig, ax = plt.subplots(figsize=(11, 6.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.4)
ax.axis("off")

def node(x, y, label, color=BLUE, w=1.5, h=0.6):
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.02,rounding_size=0.05",
                           linewidth=1.5, edgecolor=NAVY, facecolor=color)
    ax.add_patch(rect)
    ax.text(x, y, label, ha="center", va="center", fontsize=9, color="white", fontweight="bold")

# root
node(5, 5.4, "product_id\n50 | 90", NAVY, w=2.0, h=0.85)
# level 2
node(2, 3.6, "10 | 30", BLUE)
node(5, 3.6, "60 | 75", BLUE)
node(8, 3.6, "95 | 99", BLUE)
for x in [2, 5, 8]:
    ax.plot([5, x], [4.95, 3.95], color=GREY, lw=1.2, zorder=0)

# leaf level
leaves = [
    (0.8, "1..9"), (2, "10..29"), (3.2, "30..49"),
    (4.2, "50..59"), (5, "60..74"), (5.8, "75..89"),
    (7, "90..94"), (8, "95..98"), (9.2, "99..")
]
parents = [2,2,2, 5,5,5, 8,8,8]
for (x, label), px in zip(leaves, parents):
    node(x, 1.6, label, TEAL, w=1.1, h=0.5)
    ax.plot([px, x], [3.3, 1.85], color=GREY, lw=1, zorder=0)

# leaf chain (sequential pointers)
xs = [x for x, _ in leaves]
ax.plot(xs, [1.15]*len(xs), color=ORANGE, lw=1.5, linestyle="--", zorder=0)
ax.text(9.7, 1.15, "→ linked leaves\n(fast range scans)", fontsize=8, color=ORANGE, va="center")

ax.text(5, 0.35, "e.g. WHERE product_id = 62 → root → \"60 | 75\" node → leaf \"60..74\" → row",
        ha="center", fontsize=9, color=NAVY, style="italic")

ax.set_title("B-Tree Index: root → internal nodes → sorted leaf pages", fontsize=14,
             fontweight="bold", color=NAVY, y=1.03)
plt.tight_layout()
plt.savefig("btree-index.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved btree-index.png")
