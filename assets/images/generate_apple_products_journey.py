"""
Generates the "Apple products table journey" chart for Lesson 2.2 —
shows the products table after insert, after an update, and after a delete.
Includes created_at / updated_at audit columns.
Run: python3 generate_apple_products_journey.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams["font.family"] = "DejaVu Sans"

NAVY = "#1f3a5f"
BLUE = "#2f6fb3"
GREY = "#6c757d"
RED = "#c1121f"

headers = ["id", "name", "category", "price", "stock", "created_at", "updated_at"]
CREATED = "2026-02-01"

rows_after_insert = [
    ["1",  "iPhone 17 Pro",          "smartphone", "$1199.00", "500",  CREATED, CREATED],
    ["2",  "MacBook Air",            "laptop",     "$1099.00", "300",  CREATED, CREATED],
    ["3",  "MacBook Pro",            "laptop",     "$1999.00", "200",  CREATED, CREATED],
    ["4",  "iPad Air",               "tablet",     "$599.00",  "400",  CREATED, CREATED],
    ["5",  "iPad Pro",               "tablet",     "$999.00",  "350",  CREATED, CREATED],
    ["6",  "AirPods Pro",            "audio",      "$249.00",  "1000", CREATED, CREATED],
    ["7",  "AirPods Max",            "audio",      "$549.00",  "250",  CREATED, CREATED],
    ["8",  "Apple Watch Series 11",  "wearable",   "$399.00",  "700",  CREATED, CREATED],
    ["9",  "Apple TV 4K",            "accessory",  "$129.00",  "800",  CREATED, CREATED],
    ["10", "Mac Mini",               "desktop",    "$599.00",  "450",  CREATED, CREATED],
    ["11", "iPhone 17",              "smartphone", "$999.00",  "600",  CREATED, CREATED],
]

col_widths = [0.5, 1.7, 1.0, 0.85, 0.65, 1.05, 1.05]  # id, name, category, price, stock, created_at, updated_at

def draw_table(ax, title, rows, highlight_row=None, strike_row=None, highlight_cols=()):
    ax.axis("off")
    total_w = sum(col_widths)
    rh = 0.5
    nrows = len(rows) + 1
    x0, y0 = 0, 0

    def col_x(c):
        return x0 + sum(col_widths[:c])

    for c, h in enumerate(headers):
        x = col_x(c)
        y = y0 + (nrows-1)*rh
        rect = Rectangle((x, y), col_widths[c], rh, linewidth=1, edgecolor=NAVY, facecolor=BLUE)
        ax.add_patch(rect)
        ax.text(x+col_widths[c]/2, y+rh/2, h, ha="center", va="center", fontsize=7.6,
                fontweight="bold", color="white")

    for r, row in enumerate(rows):
        y = y0 + (nrows-2-r)*rh
        is_strike = (strike_row is not None and r == strike_row)
        is_hl = (highlight_row is not None and r == highlight_row)
        for c, val in enumerate(row):
            x = col_x(c)
            face = "#fbeaea" if is_strike else ("#fff6e0" if is_hl else ("#eef3f7" if r % 2 == 0 else "white"))
            rect = Rectangle((x, y), col_widths[c], rh, linewidth=1, edgecolor=GREY, facecolor=face)
            ax.add_patch(rect)
            txt_color = RED if is_strike else NAVY
            weight = "bold" if (is_hl and c in highlight_cols) else "normal"
            ax.text(x+col_widths[c]/2, y+rh/2, val, ha="center", va="center", fontsize=6.6,
                    color=txt_color, fontweight=weight)
            if is_strike:
                ax.plot([x+0.05, x+col_widths[c]-0.05], [y+rh/2, y+rh/2], color=RED, lw=1.3)

    ax.set_xlim(-0.1, total_w+0.1)
    ax.set_ylim(-0.1, nrows*rh+0.6)
    ax.set_title(title, fontsize=11, fontweight="bold", color=NAVY, pad=8)

fig, axes = plt.subplots(1, 3, figsize=(20, 6.4))

# Stage 1: after INSERT
draw_table(axes[0], "① After INSERT — 11 products added", rows_after_insert)

# Stage 2: after UPDATE (iPhone 17 Pro price + updated_at changed)
rows_after_update = [r[:] for r in rows_after_insert]
rows_after_update[0][3] = "$1249.00"       # price
rows_after_update[0][6] = "2026-02-03"    # updated_at (created_at stays put)
draw_table(axes[1], "② After UPDATE — price & updated_at changed", rows_after_update,
           highlight_row=0, highlight_cols={3, 6})

# Stage 3: after DELETE (AirPods Pro removed)
rows_after_delete = [r[:] for r in rows_after_update]
draw_table(axes[2], "③ After DELETE — AirPods Pro removed", rows_after_delete,
           strike_row=5)

fig.suptitle("The Products Table, Step by Step", fontsize=15, fontweight="bold", color=NAVY, y=1.04)
plt.tight_layout()
plt.savefig("apple-products-journey.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved apple-products-journey.png")
