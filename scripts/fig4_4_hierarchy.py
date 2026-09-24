import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'figures' / 'ch04'

fig, ax = plt.subplots(figsize=(12.2, 6.0))
ax.set_xlim(0, 12.2)
ax.set_ylim(0, 6.0)
ax.axis('off')

leaf_cols = ['tab:green', 'goldenrod', 'tab:orange', 'tab:blue']

# Two sites, each containing two plots; each plot contains two trees;
# each tree carries four coloured sampled leaves: 32 leaf measurements total.
site_specs = [
    (0.35, 0.55, 5.55, 4.85, 'Site 1'),
    (6.30, 0.55, 5.55, 4.85, 'Site 2'),
]
plot_positions = []
for sx, sy, sw, sh, label in site_specs:
    ax.add_patch(Rectangle((sx, sy), sw, sh, fill=False, linewidth=1.8, edgecolor='0.35'))
    ax.text(sx + sw/2, sy + sh + 0.20, label, ha='center', va='bottom', fontsize=13, fontweight='bold')
    # two plots within each site
    pw = 2.35; ph = 3.55
    pxs = [sx + 0.35, sx + sw - pw - 0.35]
    for j, px in enumerate(pxs, start=1):
        py = sy + 0.55
        ax.add_patch(Rectangle((px, py), pw, ph, fill=False, linewidth=1.25, edgecolor='0.55'))
        plot_positions.append((px, py, pw, ph))

# Draw two trees in each plot, with four coloured leaves per tree.
for plot_i, (px, py, pw, ph) in enumerate(plot_positions, start=1):
    tree_xs = [px + 0.72, px + 1.63]
    for tx in tree_xs:
        # trunk
        ax.plot([tx, tx], [py + 0.55, py + 1.70], color='0.35', linewidth=2.0)
        ax.plot([tx, tx - 0.28], [py + 1.35, py + 1.70], color='0.35', linewidth=1.3)
        ax.plot([tx, tx + 0.28], [py + 1.35, py + 1.70], color='0.35', linewidth=1.3)
        # canopy outline
        ax.add_patch(Ellipse((tx, py + 2.18), 1.05, 1.05, fill=False, linewidth=1.0, edgecolor='0.65'))
        leaf_offsets = [(-0.27, 0.18), (0.25, 0.18), (-0.18, -0.20), (0.22, -0.18)]
        for col, (dx, dy) in zip(leaf_cols, leaf_offsets):
            ax.add_patch(Ellipse((tx + dx, py + 2.18 + dy), 0.23, 0.13,
                                 angle=25 if dx < 0 else -25,
                                 facecolor=col, edgecolor='white', linewidth=0.5))
    ax.text(px + pw/2, py + 0.17, f'Plot {plot_i}', ha='center', va='center', fontsize=10)

# A compact visual key below the hierarchy.
ax.text(0.45, 0.20, '4 sampled leaves per tree', fontsize=11, ha='left')
ax.text(3.60, 0.20, '8 trees', fontsize=11, ha='left')
ax.text(5.55, 0.20, '4 plots', fontsize=11, ha='left')
ax.text(7.35, 0.20, '2 sites', fontsize=11, ha='left')
ax.text(9.10, 0.20, '= 32 leaf measurements', fontsize=11, ha='left')

fig.savefig(OUT/'fig4_4_hierarchy.png', dpi=200, bbox_inches='tight', pad_inches=0.08)
plt.close(fig)
