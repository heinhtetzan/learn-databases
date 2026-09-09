"""
Generates the "Paper Ledger -> Spreadsheet -> Database" evolution chart
for Lesson 1.2.
Run: python3 generate_storage_evolution.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Ellipse, FancyArrowPatch

plt.rcParams["font.family"] = "DejaVu Sans"

NAVY = "#1f3a5f"
BLUE = "#2f6fb3"
TEAL = "#2a9d8f"
ORANGE = "#e76f51"
GOLD = "#e9c46a"
GREY = "#6c757d"
PAPER = "#f7f0dd"

fig, axes = plt.subplots(1, 3, figsize=(15, 5.5))

# ---------------------------------------------------------------------------
# Panel 1: Paper Ledger
# ---------------------------------------------------------------------------
ax = axes[0]
ax.set_xlim(0, 6); ax.set_ylim(0, 7); ax.axis("off")

page = FancyBboxPatch((0.6, 0.8), 4.8, 5.6, boxstyle="round,pad=0.02,rounding_size=0.08",
                       linewidth=1.8, edgecolor=NAVY, facecolor=PAPER)
ax.add_patch(page)
ax.text(3, 6.0, "SALES LEDGER", ha="center", va="center", fontsize=11,
        fontweight="bold", color=NAVY, family="serif")
ax.plot([0.95, 5.05], [5.7, 5.7], color=NAVY, lw=1)

# handwritten-looking ruled lines with scattered entries
import random
random.seed(3)
for i in range(7):
    y = 5.2 - i * 0.6
    ax.plot([0.95, 5.05], [y, y], color="#c9c0a8", lw=0.8)
    ax.text(1.1, y + 0.15, f"item #{i+1}  ...........  ${random.randint(5,99)}",
            fontsize=7.5, color=NAVY, family="cursive", alpha=0.85)

ax.set_title("Paper Ledger", fontsize=13, fontweight="bold", color=NAVY, pad=12)
ax.text(3, 0.3, "Handwritten · one physical copy ·\nslow to search · easy to lose/damage",
        ha="center", va="center", fontsize=9, color=GREY)

# ---------------------------------------------------------------------------
# Panel 2: Spreadsheet
# ---------------------------------------------------------------------------
ax = axes[1]
ax.set_xlim(0, 6); ax.set_ylim(0, 7); ax.axis("off")

rows, cols = 6, 4
x0, y0, w, h = 0.6, 1.0, 4.8, 5.2
cw, rh = w/cols, h/rows
for r in range(rows):
    for c in range(cols):
        x = x0 + c*cw
        y = y0 + (rows-1-r)*rh
        color = GOLD if r == 0 else ("#eef3f7" if (r % 2 == 0) else "white")
        rect = Rectangle((x, y), cw, rh, linewidth=1, edgecolor=GREY, facecolor=color)
        ax.add_patch(rect)
        if r == 0:
            headers = ["Item", "Qty", "Price", "Total"]
            ax.text(x + cw/2, y + rh/2, headers[c], ha="center", va="center",
                    fontsize=8.5, fontweight="bold", color=NAVY)
        else:
            ax.text(x + cw/2, y + rh/2, "...", ha="center", va="center",
                    fontsize=8, color=GREY)

ax.set_title("Spreadsheet", fontsize=13, fontweight="bold", color=NAVY, pad=12)
ax.text(3, 0.3, "Digital, formula-driven · sortable ·\nno enforced rules · gets messy across many users/sheets",
        ha="center", va="center", fontsize=9, color=GREY)

# ---------------------------------------------------------------------------
# Panel 3: Database
# ---------------------------------------------------------------------------
ax = axes[2]
ax.set_xlim(0, 6); ax.set_ylim(0, 7); ax.axis("off")

# classic "cylinder" database icon
cx, cy_top, cy_bot, rw, rh_e = 3, 4.6, 2.0, 1.5, 0.35
body = Rectangle((cx-rw, cy_bot), rw*2, cy_top-cy_bot, facecolor=BLUE, edgecolor=NAVY, lw=1.8, zorder=1)
ax.add_patch(body)
bottom_ell = Ellipse((cx, cy_bot), rw*2, rh_e*2, facecolor=BLUE, edgecolor=NAVY, lw=1.8, zorder=1)
ax.add_patch(bottom_ell)
top_ell = Ellipse((cx, cy_top), rw*2, rh_e*2, facecolor=NAVY, edgecolor=NAVY, lw=1.8, zorder=2)
ax.add_patch(top_ell)
# ring lines to suggest stacked layers
for frac in (0.33, 0.66):
    yy = cy_bot + (cy_top-cy_bot)*frac
    ax.add_patch(Ellipse((cx, yy), rw*2, rh_e*2, facecolor="none", edgecolor="#7fa8d6", lw=1))

ax.text(cx, (cy_top+cy_bot)/2, "DB", ha="center", va="center",
        fontsize=13, fontweight="bold", color="white", zorder=3)

# connected users / apps around it
users = [(0.7, 5.8), (5.3, 5.8), (0.7, 1.3), (5.3, 1.3)]
labels = ["App", "Report", "Admin", "API"]
for (ux, uy), label in zip(users, labels):
    circ = Circle((ux, uy), 0.45, facecolor=TEAL, edgecolor=NAVY, lw=1.4, zorder=3)
    ax.add_patch(circ)
    ax.text(ux, uy, label, ha="center", va="center", fontsize=7.5, color="white",
            fontweight="bold", zorder=4)
    ax.plot([ux, cx], [uy, (cy_top+cy_bot)/2], color=GREY, lw=1, linestyle="--", zorder=0)

ax.set_title("Database", fontsize=13, fontweight="bold", color=NAVY, pad=12)
ax.text(3, 0.3, "Structured + indexed · enforces rules ·\nmany users/apps at once · fast, reliable search",
        ha="center", va="center", fontsize=9, color=GREY)

fig.suptitle("From Paper to Database: How We Store Data Over Time", fontsize=15,
             fontweight="bold", color=NAVY, y=1.04)
plt.tight_layout()
plt.savefig("storage-evolution.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

print("Saved storage-evolution.png")
