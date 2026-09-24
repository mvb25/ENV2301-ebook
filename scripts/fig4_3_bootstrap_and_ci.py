import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from pathlib import Path
from PIL import Image
from scipy.stats import t

OUT = Path(__file__).resolve().parents[1] / 'figures' / 'ch04'
TMP = OUT / '_tmp_fig4_3'
TMP.mkdir(exist_ok=True)
rng = np.random.default_rng(4433)

# A: bootstrap distribution and percentile interval.
pop = rng.lognormal(mean=np.log(150), sigma=0.38, size=5000)
obs = rng.choice(pop, size=24, replace=False)
obs_mean = obs.mean()
boot = np.array([rng.choice(obs, size=len(obs), replace=True).mean() for _ in range(5000)])
lo, hi = np.quantile(boot, [0.025, 0.975])

fig, ax = plt.subplots(figsize=(6.2, 4.4))
counts, bins, patches = ax.hist(boot, bins=40, density=True, alpha=0.45, color='0.65')
# Highlight bars whose centres fall in the central 95%.
for patch, left, right in zip(patches, bins[:-1], bins[1:]):
    centre = (left + right) / 2
    if lo <= centre <= hi:
        patch.set_color('tab:blue')
        patch.set_alpha(0.60)
ax.axvline(obs_mean, linewidth=1.2, linestyle='--', color='black')
ax.axvline(lo, linewidth=1.2, color='black')
ax.axvline(hi, linewidth=1.2, color='black')
ax.set_xlabel('Bootstrap estimate of mean biomass (Mg ha$^{-1}$)')
ax.set_ylabel('Relative frequency')
ax.text(0.02, 0.97, 'A', transform=ax.transAxes, va='top', fontweight='bold', fontsize=14)
ax.text(lo, ax.get_ylim()[1]*0.90, '2.5%', ha='right', va='top', fontsize=9)
ax.text(hi, ax.get_ylim()[1]*0.90, '97.5%', ha='left', va='top', fontsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
pA = TMP/'A.png'
fig.savefig(pA, dpi=190, bbox_inches='tight')
plt.close(fig)

# B: confidence intervals from repeated hypothetical studies. Intervals that
# miss the true mean are orange; all others remain neutral grey.
true_mean = 150
true_sd = 45
n = 18
records = []
for i in range(40):
    vals = rng.normal(true_mean, true_sd, n)
    m = vals.mean()
    se = vals.std(ddof=1)/np.sqrt(n)
    crit = t.ppf(0.975, df=n-1)
    l, h = m-crit*se, m+crit*se
    records.append((m, l, h, l <= true_mean <= h))

fig, ax = plt.subplots(figsize=(6.2, 4.4))
cover_segments = []
miss_segments = []
cover_x, cover_y, miss_x, miss_y = [], [], [], []
for i, (m, l, h, covers) in enumerate(records, start=1):
    if covers:
        cover_segments.append([(l, i), (h, i)])
        cover_x.append(m); cover_y.append(i)
    else:
        miss_segments.append([(l, i), (h, i)])
        miss_x.append(m); miss_y.append(i)
if cover_segments:
    ax.add_collection(LineCollection(cover_segments, linewidths=1.2, colors='0.45'))
if miss_segments:
    ax.add_collection(LineCollection(miss_segments, linewidths=1.7, colors='tab:orange'))
if cover_x:
    ax.scatter(cover_x, cover_y, s=13, color='0.35')
if miss_x:
    ax.scatter(miss_x, miss_y, s=18, color='tab:orange')
ax.axvline(true_mean, linewidth=1.3, linestyle=':', color='black')
ax.autoscale()
ax.set_xlabel('Estimated mean and 95% confidence interval')
ax.set_ylabel('Repeated study')
ax.set_yticks([])
ax.text(0.02, 0.97, 'B', transform=ax.transAxes, va='top', fontweight='bold', fontsize=14)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
pB = TMP/'B.png'
fig.savefig(pB, dpi=190, bbox_inches='tight')
plt.close(fig)

ims = [Image.open(pA).convert('RGB'), Image.open(pB).convert('RGB')]
maxw = max(i.width for i in ims)
maxh = max(i.height for i in ims)
canvas = Image.new('RGB', (maxw*2, maxh), 'white')
for col, im in enumerate(ims):
    canvas.paste(im, (col*maxw+(maxw-im.width)//2, (maxh-im.height)//2))
canvas.save(OUT/'fig4_3_bootstrap_and_ci.png', dpi=(190,190))
pA.unlink(); pB.unlink(); TMP.rmdir()
