"""
Generates a Venn-style "types of joins" chart for Lesson 2.11.
Run: python3 generate_join_venn.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import numpy as np

plt.rcParams["font.family"] = "DejaVu Sans"

NAVY = "#1f3a5f"
BLUE = "#2f6fb3"
TEAL = "#2a9d8f"
GREY = "#c9ced4"
FILL = "#e76f51"

def venn_mask(ax, title, keep_left_only, keep_overlap, keep_right_only):
    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-1.3, 1.4)
    ax.axis("off")
    ax.set_aspect("equal")

    n = 400
    x = np.linspace(-1.8, 1.8, n)
    y = np.linspace(-1.3, 1.3, n)
    X, Y = np.meshgrid(x, y)

    r = 1.0
    cx_l, cx_r = -0.5, 0.5
    in_left = (X - cx_l)**2 + Y**2 <= r**2
    in_right = (X - cx_r)**2 + Y**2 <= r**2

    left_only = in_left & ~in_right
    right_only = in_right & ~in_left
    overlap = in_left & in_right

    color = np.ones((n, n, 4))
    color[..., 3] = 0  # fully transparent base

    def paint(mask, hexcolor, alpha=0.85):
        rgb = tuple(int(hexcolor[i:i+2], 16)/255 for i in (1, 3, 5))
        color[mask, 0] = rgb[0]
        color[mask, 1] = rgb[1]
        color[mask, 2] = rgb[2]
        color[mask, 3] = alpha

    if keep_left_only:
        paint(left_only, FILL)
    if keep_right_only:
        paint(right_only, FILL)
    if keep_overlap:
        paint(overlap, FILL)

    ax.imshow(color, extent=(-1.8, 1.8, -1.3, 1.3), origin="lower", zorder=2)

    # outlines on top
    left_c = Circle((cx_l, 0), r, facecolor="none", edgecolor=NAVY, lw=2, zorder=3)
    right_c = Circle((cx_r, 0), r, facecolor="none", edgecolor=NAVY, lw=2, zorder=3)
    ax.add_patch(left_c)
    ax.add_patch(right_c)

    ax.text(cx_l - 0.62, 1.15, "Left table", fontsize=9.5, color=NAVY, fontweight="bold", ha="center")
    ax.text(cx_r + 0.62, 1.15, "Right table", fontsize=9.5, color=NAVY, fontweight="bold", ha="center")
    ax.set_title(title, fontsize=13, fontweight="bold", color=NAVY, pad=14)


fig, axes = plt.subplots(1, 4, figsize=(17, 5.2))

venn_mask(axes[0], "INNER JOIN\nonly matches", keep_left_only=False, keep_overlap=True, keep_right_only=False)
venn_mask(axes[1], "LEFT JOIN\nall of left + matches", keep_left_only=True, keep_overlap=True, keep_right_only=False)
venn_mask(axes[2], "RIGHT JOIN\nall of right + matches", keep_left_only=False, keep_overlap=True, keep_right_only=True)
venn_mask(axes[3], "FULL OUTER JOIN\neverything", keep_left_only=True, keep_overlap=True, keep_right_only=True)

fig.suptitle("The 4 Join Types", fontsize=17, fontweight="bold", color=NAVY, y=1.06)
plt.tight_layout()
plt.savefig("join-types-venn.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved join-types-venn.png")
