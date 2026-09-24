import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.ndimage import gaussian_filter
from PIL import Image

OUT = Path(__file__).resolve().parents[1] / 'figures' / 'ch04'
OUT.mkdir(parents=True, exist_ok=True)
TMP = OUT / '_tmp_fig4_1'
TMP.mkdir(exist_ok=True)

rng = np.random.default_rng(2301)

# Build a spatially structured 10 x 10 toy landscape.
field = gaussian_filter(rng.normal(size=(10, 10)), sigma=1.35)
field = (field - field.min()) / (field.max() - field.min())
pop_grid = 45 + 285 * field
pop = pop_grid.ravel()
true_mean = pop.mean()

# Repeated sampling from the finite population.
def sample_means(n, reps=5000, local_rng=None):
    r = local_rng if local_rng is not None else rng
    out = np.empty(reps)
    for i in range(reps):
        idx = r.choice(len(pop), size=n, replace=False)
        out[i] = pop[idx].mean()
    return out

means5 = sample_means(5, 5000, np.random.default_rng(4105))
means20 = sample_means(20, 5000, np.random.default_rng(4120))

# Choose a representative, comparatively smooth accumulating sample rather than
# an unusually jagged single random sequence.
search_rng = np.random.default_rng(4501)
best = None
best_score = np.inf
for _ in range(5000):
    order = search_rng.permutation(len(pop))
    running = np.cumsum(pop[order]) / np.arange(1, len(pop) + 1)
    # Reward a visible early departure, but avoid pathological oscillation.
    roughness = np.mean(np.abs(np.diff(running[:50])))
    late_error = np.mean(np.abs(running[20:50] - true_mean))
    early_error = abs(running[1] - true_mean)
    penalty = 0 if early_error > 12 else (12 - early_error) * 2
    score = roughness + 0.45 * late_error + penalty
    if score < best_score:
        best_score = score
        best = running
running = best

# Panel A: 100-cell mosaic map.
fig, ax = plt.subplots(figsize=(5.4, 4.25))
im = ax.imshow(pop_grid, interpolation='nearest')
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel('10 × 10 equal-area plots')
cbar = fig.colorbar(im, ax=ax, fraction=0.048, pad=0.04)
cbar.set_label('Plot biomass (Mg ha$^{-1}$)')
ax.text(0.02, 0.98, 'A', transform=ax.transAxes, va='top', ha='left', fontweight='bold', fontsize=14,
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.75, pad=1.5))
fig.savefig(TMP/'A.png', dpi=190, bbox_inches='tight')
plt.close(fig)

# Panel B: one representative accumulating sample.
fig, ax = plt.subplots(figsize=(5.4, 4.25))
x = np.arange(1, 51)
ax.plot(x, running[:50], linewidth=1.8, color='tab:blue')
ax.axhline(true_mean, linestyle='--', linewidth=1, color='0.35')
ax.set_xlim(1, 50)
ax.set_xlabel('Number of plots sampled')
ax.set_ylabel('Running mean (Mg ha$^{-1}$)')
ax.text(0.02, 0.98, 'B', transform=ax.transAxes, va='top', ha='left', fontweight='bold', fontsize=14)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.savefig(TMP/'B.png', dpi=190, bbox_inches='tight')
plt.close(fig)

# Panel C: distributions for n = 5 and n = 20.
fig, ax = plt.subplots(figsize=(5.4, 4.25))
bins = np.linspace(min(means5.min(), means20.min()), max(means5.max(), means20.max()), 36)
ax.hist(means5, bins=bins, density=True, alpha=0.48, label='n = 5', color='tab:blue')
ax.hist(means20, bins=bins, density=True, alpha=0.48, label='n = 20', color='tab:orange')
ax.axvline(true_mean, linestyle='--', linewidth=1, color='0.35')
ax.set_xlabel('Estimated mean biomass (Mg ha$^{-1}$)')
ax.set_ylabel('Relative frequency')
ax.legend(frameon=False)
ax.text(0.02, 0.98, 'C', transform=ax.transAxes, va='top', ha='left', fontweight='bold', fontsize=14)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.savefig(TMP/'C.png', dpi=190, bbox_inches='tight')
plt.close(fig)

# Panel D: repeated sample means across n = 1..50. Light grey generally,
# with n=5 and n=20 highlighted as requested.
fig, ax = plt.subplots(figsize=(5.4, 4.25))
cloud_rng = np.random.default_rng(4777)
for n in range(1, 51):
    vals = sample_means(n, 36, cloud_rng)
    jitter = cloud_rng.normal(0, 0.085, len(vals))
    if n == 5:
        ax.scatter(np.full(len(vals), n) + jitter, vals, s=15, alpha=0.78, color='tab:blue', zorder=3)
    elif n == 20:
        ax.scatter(np.full(len(vals), n) + jitter, vals, s=15, alpha=0.78, color='tab:orange', zorder=3)
    else:
        ax.scatter(np.full(len(vals), n) + jitter, vals, s=10, alpha=0.34, color='lightgrey', edgecolors='none', zorder=1)
ax.axhline(true_mean, linestyle='--', linewidth=1, color='0.35')
ax.set_xlim(0.5, 50.5)
ax.set_xlabel('Number of plots sampled')
ax.set_ylabel('Estimated mean biomass (Mg ha$^{-1}$)')
ax.text(0.02, 0.98, 'D', transform=ax.transAxes, va='top', ha='left', fontweight='bold', fontsize=14)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.savefig(TMP/'D.png', dpi=190, bbox_inches='tight')
plt.close(fig)

# Compose four independently generated chart panels into one figure.
paths = [TMP/f'{p}.png' for p in 'ABCD']
ims = [Image.open(p).convert('RGB') for p in paths]
maxw = max(im.width for im in ims)
maxh = max(im.height for im in ims)
canvas = Image.new('RGB', (maxw*2, maxh*2), 'white')
for im, (col, row) in zip(ims, [(0,0),(1,0),(0,1),(1,1)]):
    x0 = col*maxw + (maxw-im.width)//2
    y0 = row*maxh + (maxh-im.height)//2
    canvas.paste(im, (x0,y0))
canvas.save(OUT/'fig4_1_sampling_variability.png', dpi=(190,190))

# Clean temporary panels.
for p in paths:
    p.unlink(missing_ok=True)
TMP.rmdir()
