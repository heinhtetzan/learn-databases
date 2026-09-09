"""
Generates static chart images used throughout the course.
Run: python3 generate_charts.py
Output: PNG files in this same directory (assets/images/).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

plt.rcParams["font.family"] = "DejaVu Sans"

NAVY = "#1f3a5f"
BLUE = "#2f6fb3"
TEAL = "#2a9d8f"
ORANGE = "#e76f51"
GOLD = "#e9c46a"
GREY = "#6c757d"
LIGHT = "#f4f6f8"

# ---------------------------------------------------------------------------
# 1. Normalization forms - progressive table shrinking / redundancy removal
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 4, figsize=(14, 4))
titles = ["Unnormalized\n(repeating groups)", "1NF\n(atomic values)", "2NF\n(no partial dependency)", "3NF\n(no transitive dependency)"]
colors = [ORANGE, GOLD, TEAL, BLUE]
redundancy = [1.0, 0.75, 0.45, 0.15]
for ax, title, color, r in zip(axes, titles, colors, redundancy):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title(title, fontsize=11, fontweight="bold", color=NAVY)
    rows = 5
    for i in range(rows):
        redundant = i < int(rows * r)
        c = ORANGE if redundant else "#d9e4ec"
        rect = FancyBboxPatch((0.1, 0.85 - i*0.16), 0.8, 0.12,
                               boxstyle="round,pad=0.01,rounding_size=0.02",
                               linewidth=1, edgecolor=NAVY, facecolor=c)
        ax.add_patch(rect)
fig.suptitle("Normalization: reducing redundancy step by step", fontsize=14, fontweight="bold", color=NAVY, y=1.03)
plt.tight_layout()
plt.savefig("normalization-forms.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

# ---------------------------------------------------------------------------
# 2. B-Tree index structure
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")

def node(ax, x, y, label, color=BLUE, w=1.4, h=0.6):
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.02,rounding_size=0.05",
                           linewidth=1.5, edgecolor=NAVY, facecolor=color)
    ax.add_patch(rect)
    ax.text(x, y, label, ha="center", va="center", fontsize=9, color="white", fontweight="bold")

# root
node(ax, 5, 5, "50 | 90", NAVY, w=1.8)
# level 2
node(ax, 2, 3.2, "10 | 30", BLUE)
node(ax, 5, 3.2, "60 | 75", BLUE)
node(ax, 8, 3.2, "95 | 99", BLUE)
# connections root -> level2
for x in [2, 5, 8]:
    ax.plot([5, x], [4.7, 3.5], color=GREY, lw=1.2, zorder=0)

# leaf level
leaves = [
    (0.8, "1..9"), (2, "10..29"), (3.2, "30..49"),
    (4.2, "50..59"), (5, "60..74"), (5.8, "75..89"),
    (7, "90..94"), (8, "95..98"), (9.2, "99..")
]
parents = [2,2,2, 5,5,5, 8,8,8]
for (x, label), px in zip(leaves, parents):
    node(ax, x, 1.2, label, TEAL, w=1.1, h=0.5)
    ax.plot([px, x], [2.9, 1.45], color=GREY, lw=1, zorder=0)

# leaf chain (sequential pointers)
xs = [x for x, _ in leaves]
ax.plot(xs, [0.75]*len(xs), color=ORANGE, lw=1.5, linestyle="--", zorder=0)
ax.text(9.7, 0.75, "→ linked leaves\n(range scans)", fontsize=8, color=ORANGE, va="center")

ax.set_title("B-Tree Index: root → internal nodes → sorted leaf pages", fontsize=13, fontweight="bold", color=NAVY)
plt.tight_layout()
plt.savefig("btree-index.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

# ---------------------------------------------------------------------------
# 3. CAP theorem triangle
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 7))
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

import math
cx, cy, r = 5, 4.6, 3.6
angles = [90, 210, 330]
labels = ["Consistency\n(every read sees\nthe latest write)",
          "Availability\n(every request\ngets a response)",
          "Partition Tolerance\n(keeps working despite\nnetwork splits)"]
colors3 = [BLUE, TEAL, ORANGE]
pts = []
for a in angles:
    x = cx + r*math.cos(math.radians(a))
    y = cy + r*math.sin(math.radians(a))
    pts.append((x, y))

triangle = plt.Polygon(pts, closed=True, fill=True, facecolor="#eef3f7", edgecolor=NAVY, lw=2, zorder=0)
ax.add_patch(triangle)

for (x, y), label, c in zip(pts, labels, colors3):
    circ = Circle((x, y), 0.95, facecolor=c, edgecolor=NAVY, lw=1.5, zorder=2)
    ax.add_patch(circ)
    ty = y + (1.3 if y > cy else -1.3)
    ax.text(x, ty, label, ha="center", va="center", fontsize=9.5, color=NAVY, fontweight="bold")

ax.text(cx, cy, "Pick 2\n(in practice: partition\ntolerance is mandatory,\nso choose CP or AP)",
        ha="center", va="center", fontsize=9.5, color=NAVY, style="italic")
ax.set_title("CAP Theorem", fontsize=15, fontweight="bold", color=NAVY, y=1.02)
plt.tight_layout()
plt.savefig("cap-theorem.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

# ---------------------------------------------------------------------------
# 4. Replication topologies
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

def draw_node(ax, x, y, label, color=BLUE, r=0.55):
    circ = Circle((x, y), r, facecolor=color, edgecolor=NAVY, lw=1.5, zorder=2)
    ax.add_patch(circ)
    ax.text(x, y, label, ha="center", va="center", fontsize=8.5, color="white", fontweight="bold")

def arrow(ax, x1, y1, x2, y2, color=GREY, style="-|>"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=1.6))

# Single-leader
ax = axes[0]; ax.set_xlim(0,6); ax.set_ylim(0,6); ax.axis("off")
draw_node(ax, 3, 4.8, "Leader\n(writes)", NAVY)
draw_node(ax, 1.2, 2, "Replica", BLUE)
draw_node(ax, 3, 2, "Replica", BLUE)
draw_node(ax, 4.8, 2, "Replica", BLUE)
for x in [1.2, 3, 4.8]:
    arrow(ax, 3, 4.3, x, 2.5)
ax.set_title("Single-Leader\n(reads: any node, writes: leader only)", fontsize=10.5, fontweight="bold", color=NAVY)

# Multi-leader
ax = axes[1]; ax.set_xlim(0,6); ax.set_ylim(0,6); ax.axis("off")
draw_node(ax, 1.8, 4, "Leader A\n(Region 1)", TEAL)
draw_node(ax, 4.2, 4, "Leader B\n(Region 2)", TEAL)
draw_node(ax, 1.8, 1.6, "Replica", BLUE)
draw_node(ax, 4.2, 1.6, "Replica", BLUE)
arrow(ax, 2.4, 4, 3.6, 4, style="<|-|>")
arrow(ax, 1.8, 3.45, 1.8, 2.15)
arrow(ax, 4.2, 3.45, 4.2, 2.15)
ax.set_title("Multi-Leader\n(writes accepted in multiple regions,\nchanges sync + can conflict)", fontsize=10.5, fontweight="bold", color=NAVY)

# Leaderless
ax = axes[2]; ax.set_xlim(0,6); ax.set_ylim(0,6); ax.axis("off")
positions = [(3, 4.8), (1.2, 3.2), (4.8, 3.2), (1.8, 1.4), (4.2, 1.4)]
for (x, y) in positions:
    draw_node(ax, x, y, "Node", ORANGE, r=0.5)
for i in range(len(positions)):
    for j in range(i+1, len(positions)):
        x1,y1 = positions[i]; x2,y2 = positions[j]
        ax.plot([x1,x2],[y1,y2], color=GREY, lw=0.8, alpha=0.5, zorder=0)
ax.set_title("Leaderless\n(client writes to N nodes,\nquorum reads/writes: R + W > N)", fontsize=10.5, fontweight="bold", color=NAVY)

fig.suptitle("Replication Topologies", fontsize=15, fontweight="bold", color=NAVY, y=1.05)
plt.tight_layout()
plt.savefig("replication-topologies.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

# ---------------------------------------------------------------------------
# 5. SQL vs NoSQL comparison (radar-ish grouped bar)
# ---------------------------------------------------------------------------
categories = ["Schema\nflexibility", "Horizontal\nscalability", "Complex\njoins/queries", "Strong\nconsistency", "Write\nthroughput\n(large scale)"]
sql_scores = [2, 2, 5, 5, 2]
nosql_scores = [5, 5, 2, 2.5, 4.5]

x = np.arange(len(categories))
width = 0.35
fig, ax = plt.subplots(figsize=(11, 5.5))
b1 = ax.bar(x - width/2, sql_scores, width, label="Relational (SQL)", color=BLUE, edgecolor=NAVY)
b2 = ax.bar(x + width/2, nosql_scores, width, label="NoSQL", color=TEAL, edgecolor=NAVY)
ax.set_ylim(0, 6)
ax.set_ylabel("Relative strength (1-5, illustrative)", fontsize=10)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=9.5)
ax.set_title("SQL vs NoSQL: general tendencies\n(actual results vary a lot by specific product)", fontsize=13, fontweight="bold", color=NAVY)
ax.legend(frameon=False, fontsize=10)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("sql-vs-nosql-comparison.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

# ---------------------------------------------------------------------------
# 6. DBMS architecture layers
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 7))
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

layers = [
    ("Client applications / drivers", ORANGE, 8.6),
    ("Query parser & planner\n(parse SQL → logical plan → optimize)", GOLD, 7.2),
    ("Execution engine\n(joins, sorts, aggregates)", TEAL, 5.6),
    ("Transaction manager\n(ACID, concurrency control, locks/MVCC)", BLUE, 4.0),
    ("Storage engine\n(indexes, buffer/page cache, B-trees / LSM trees)", NAVY, 2.4),
    ("Disk / SSD (data files, WAL / redo log)", GREY, 0.9),
]
for label, color, y in layers:
    rect = FancyBboxPatch((0.6, y-0.55), 8.8, 1.05, boxstyle="round,pad=0.02,rounding_size=0.06",
                           linewidth=1.5, edgecolor=NAVY, facecolor=color)
    ax.add_patch(rect)
    txt_color = "white"
    ax.text(5, y, label, ha="center", va="center", fontsize=10, color=txt_color, fontweight="bold")

for y1, y2 in zip([8.05, 6.65, 5.05, 3.45, 1.85], [7.75, 6.35, 4.75, 3.15, 1.55]):
    ax.annotate("", xy=(5, y2), xytext=(5, y1), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.4))

ax.set_title("Anatomy of a DBMS", fontsize=15, fontweight="bold", color=NAVY, y=1.02)
plt.tight_layout()
plt.savefig("dbms-architecture.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

# ---------------------------------------------------------------------------
# 7. Vertical vs Horizontal scaling
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11, 5))

ax = axes[0]; ax.set_xlim(0,6); ax.set_ylim(0,6); ax.axis("off")
sizes = [0.6, 0.9, 1.3, 1.8]
xpos = [1, 2.3, 3.9, 5.6]
for s, x in zip(sizes, xpos):
    rect = FancyBboxPatch((x-s/2, 1.5-s/2), s, s, boxstyle="round,pad=0.02,rounding_size=0.05",
                           linewidth=1.5, edgecolor=NAVY, facecolor=BLUE)
    ax.add_patch(rect)
ax.annotate("", xy=(5.9, 1.5), xytext=(0.4, 1.5), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.2, linestyle="--"))
ax.set_title("Vertical Scaling\n(one bigger machine: more CPU/RAM/disk)", fontsize=11, fontweight="bold", color=NAVY)

ax = axes[1]; ax.set_xlim(0,6); ax.set_ylim(0,6); ax.axis("off")
draw_node(ax, 3, 4.8, "Router /\nCoordinator", NAVY, r=0.6)
shard_x = [0.9, 2.3, 3.7, 5.1]
for i, x in enumerate(shard_x):
    draw_node(ax, x, 2.2, f"Shard {i+1}", TEAL, r=0.55)
    arrow(ax, 3, 4.2, x, 2.75)
ax.set_title("Horizontal Scaling\n(more machines, data partitioned across shards)", fontsize=11, fontweight="bold", color=NAVY)

plt.tight_layout()
plt.savefig("scaling-vertical-vs-horizontal.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

print("All charts generated successfully.")
