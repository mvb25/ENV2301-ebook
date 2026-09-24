import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image

OUT = Path(__file__).resolve().parents[1] / 'figures' / 'ch04'
TMP = OUT / '_tmp_fig4_2'
TMP.mkdir(exist_ok=True)
rng = np.random.default_rng(4231)

# Two effect sizes crossed with two sample sizes. Ecological spread is kept
# comparable across panels so that effect magnitude and sample size can be
# read independently.
configs = [
    ('large_few', 32, 7, 1.70),
    ('large_many', 32, 42, 1.70),
    ('small_few', 4, 7, 0.24),
    ('small_many', 4, 42, 0.24),
]

panel_files = []
letters = list('ABCDEFGH')
li = 0

# Group comparisons. Use the same within-treatment SD throughout.
for key, diff, n, slope in configs:
    no_hunt = rng.normal(24, 9.5, n)
    hunt = rng.normal(24 + diff, 9.5, n)
    fig, ax = plt.subplots(figsize=(3.25, 3.35))
    ax.boxplot([hunt, no_hunt], positions=[1, 2], widths=0.50,
               patch_artist=False, showfliers=False)
    for pos, vals, col in zip([1, 2], [hunt, no_hunt], ['tab:blue', 'tab:orange']):
        jitter = rng.normal(0, 0.05, len(vals))
        ax.scatter(np.full(len(vals), pos) + jitter, vals, s=22,
                   alpha=0.68, color=col)
    means = [hunt.mean(), no_hunt.mean()]
    ses = [hunt.std(ddof=1)/np.sqrt(n), no_hunt.std(ddof=1)/np.sqrt(n)]
    ax.errorbar([1, 2], means, yerr=ses, fmt='o', capsize=5,
                linewidth=1.8, markersize=6, color='black')
    ax.set_xticks([1, 2], ['Hunting', 'No hunting'])
    ax.set_ylabel('Understory plants (m$^{-2}$)')
    ax.set_ylim(-2, 72)
    ax.text(0.03, 0.97, letters[li], transform=ax.transAxes, va='top',
            fontweight='bold', fontsize=13)
    ax.text(0.5, 0.05, f'n = {n} plots / treatment', transform=ax.transAxes,
            ha='center', fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    path = TMP / f'{key}_group.png'
    panel_files.append(path)
    fig.savefig(path, dpi=190, bbox_inches='tight')
    plt.close(fig)
    li += 1

# Continuous relationships. Strong and weak slopes are deliberately made
# visually distinct, while residual variation is held comparable.
for key, diff, n, slope in configs:
    x = np.linspace(1.0, 19.0, n) + rng.normal(0, 0.30, n)
    y = 57 - slope*x + rng.normal(0, 5.0, n)
    coeff = np.polyfit(x, y, 1)
    xg = np.linspace(0, 20, 100)
    yg = coeff[0]*xg + coeff[1]
    fig, ax = plt.subplots(figsize=(3.25, 3.35))
    ax.scatter(x, y, s=23, alpha=0.70, color='tab:blue')
    ax.plot(xg, yg, linewidth=2.0, color='tab:blue')
    ax.set_xlim(0, 20)
    ax.set_ylim(15, 61)
    ax.set_xlabel('Deer abundance (relative units)')
    ax.set_ylabel('Understory plants (m$^{-2}$)')
    ax.text(0.03, 0.97, letters[li], transform=ax.transAxes, va='top',
            fontweight='bold', fontsize=13)
    ax.text(0.5, 0.05, f'n = {n} plots', transform=ax.transAxes,
            ha='center', fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    path = TMP / f'{key}_rel.png'
    panel_files.append(path)
    fig.savefig(path, dpi=190, bbox_inches='tight')
    plt.close(fig)
    li += 1

ims = [Image.open(p).convert('RGB') for p in panel_files]
maxw = max(i.width for i in ims)
maxh = max(i.height for i in ims)
canvas = Image.new('RGB', (maxw*4, maxh*2), 'white')
for idx, im in enumerate(ims):
    row = 0 if idx < 4 else 1
    col = idx if idx < 4 else idx-4
    x0 = col*maxw + (maxw-im.width)//2
    y0 = row*maxh + (maxh-im.height)//2
    canvas.paste(im, (x0, y0))
canvas.save(OUT/'fig4_2_pattern_variability_sample_size.png', dpi=(190,190))

for p in panel_files:
    p.unlink(missing_ok=True)
TMP.rmdir()
