"""
Generates the "Data -> Information" concept chart for Lesson 1.1.
Run: python3 generate_data_vs_information.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.family"] = "DejaVu Sans"

NAVY = "#1f3a5f"
BLUE = "#2f6fb3"
TEAL = "#2a9d8f"
ORANGE = "#e76f51"
GREY = "#6c757d"

fig, ax = plt.subplots(figsize=(11, 5.5))
ax.set_xlim(0, 11)
ax.set_ylim(0, 5.5)
ax.axis("off")

# --- Left side: scattered raw data fragments ---
fragments = [
    ("Alice", 1.2, 4.3),
    ("42", 2.3, 3.6),
    ("2026-01-05", 0.9, 2.8),
    ("mail.com", 2.1, 2.0),
    ("NYC", 1.0, 1.2),
]
for text, x, y in fragments:
    box = FancyBboxPatch((x - 0.55, y - 0.3), 1.1, 0.6,
                          boxstyle="round,pad=0.02,rounding_size=0.08",
                          linewidth=1.4, edgecolor=GREY, facecolor="#eef1f4")
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center", fontsize=9, color=NAVY)

ax.text(1.4, 5.0, "Raw DATA\n(isolated facts, no context)",
        ha="center", va="center", fontsize=11, fontweight="bold", color=ORANGE)

# --- Arrow with label ---
arrow = FancyArrowPatch((3.1, 2.8), (5.9, 2.8),
                         arrowstyle="-|>", mutation_scale=25, lw=2.4, color=NAVY)
ax.add_patch(arrow)
ax.text(4.5, 3.15, "organize +\ngive context", ha="center", va="center",
        fontsize=9, color=NAVY, style="italic")

# --- Right side: assembled information card ---
card = FancyBboxPatch((6.1, 1.1), 4.4, 3.6, boxstyle="round,pad=0.03,rounding_size=0.12",
                       linewidth=2, edgecolor=NAVY, facecolor=TEAL)
ax.add_patch(card)
ax.text(8.3, 4.35, "Customer Record", ha="center", va="center",
        fontsize=11.5, fontweight="bold", color="white")
lines = [
    "Name:      Alice",
    "Age:       42",
    "Signed up: 2026-01-05",
    "Email:     alice@mail.com",
    "City:      NYC",
]
for i, line in enumerate(lines):
    ax.text(6.5, 3.75 - i * 0.5, line, ha="left", va="center",
            fontsize=10, color="white", family="monospace")

ax.text(8.3, 4.9, "INFORMATION\n(meaningful, usable)",
        ha="center", va="center", fontsize=11, fontweight="bold", color=BLUE)

ax.set_title("From Data to Information", fontsize=15, fontweight="bold", color=NAVY, y=1.03)
plt.tight_layout()
plt.savefig("data-vs-information.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

print("Saved data-vs-information.png")
