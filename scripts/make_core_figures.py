from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle

ROOT = Path(__file__).resolve().parents[1]


def save(fig, rel, w=0.95):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=190, bbox_inches='tight', pad_inches=0.12)
    plt.close(fig)


def box(ax, x, y, w, h, text, fs=10):
    p = FancyBboxPatch((x,y), w,h, boxstyle='round,pad=0.025,rounding_size=0.03', fill=False, linewidth=1.2)
    ax.add_patch(p)
    ax.text(x+w/2, y+h/2, text, ha='center', va='center', fontsize=fs, wrap=True)

# Figure 1.1: inquiry logic
fig, ax = plt.subplots(figsize=(12.5,4.0)); ax.set_xlim(0,12.5); ax.set_ylim(0,4); ax.axis('off')
labels = [
    'Environmental issue\nor knowledge gap', 'Working understanding\nof the system', 'Question or\nobjective',
    'Information and\ncomparisons needed', 'Variables, measurements\nand methods', 'Sampling in\nspace and time',
    'Observations\nand constraints', 'Analysis and\ninterpretation', 'Bounded conclusion\nor decision']
coords=[]
for i,l in enumerate(labels):
    row = 0 if i<5 else 1
    col = i if i<5 else i-5
    x = 0.15 + col*2.42
    y = 2.35 if row==0 else 0.55
    box(ax,x,y,2.0,0.8,l,9.5); coords.append((x,y))
for i in range(4):
    x,y=coords[i]; nx,ny=coords[i+1]
    ax.annotate('', xy=(nx,ny+0.4), xytext=(x+2.0,y+0.4), arrowprops=dict(arrowstyle='->', lw=1.1))
# turn down
x,y=coords[4]; nx,ny=coords[5]
ax.annotate('',xy=(nx+1.0,ny+0.8),xytext=(x+1.0,y),arrowprops=dict(arrowstyle='->',lw=1.1,connectionstyle='arc3,rad=-0.35'))
for i in range(5,8):
    x,y=coords[i]; nx,ny=coords[i+1]
    ax.annotate('',xy=(nx,ny+0.4),xytext=(x+2.0,y+0.4),arrowprops=dict(arrowstyle='->',lw=1.1))
# back arrows to indicate adaptation
ax.annotate('',xy=(3.2,2.3),xytext=(8.2,1.4),arrowprops=dict(arrowstyle='->',lw=1.0,linestyle='dashed',connectionstyle='arc3,rad=0.28'))
ax.text(6.0,1.85,'fieldwork or analysis may revise earlier decisions',ha='center',fontsize=9)
save(fig,'figures/ch01/fig1_1_inquiry_logic.png')

# Figure 2.1 causal pathway
fig, ax = plt.subplots(figsize=(11,2.8)); ax.set_xlim(0,11); ax.set_ylim(0,2.8); ax.axis('off')
labels=['Reduced grazing\nor mowing','Woody recruitment','Canopy development','Lower understory\nlight','Species-specific\nperformance']
for i,l in enumerate(labels):
    x=0.2+i*2.15; box(ax,x,1.0,1.65,0.8,l,10)
    if i<4: ax.annotate('',xy=(x+2.1,1.4),xytext=(x+1.65,1.4),arrowprops=dict(arrowstyle='->',lw=1.2))
ax.text(5.5,0.35,'Each arrow is a proposition that can be evaluated with observations.',ha='center',fontsize=9)
save(fig,'figures/ch02/fig2_1_causal_pathway.png')

# Figure 3.1 measurement chain
fig, ax = plt.subplots(figsize=(12,3.1)); ax.set_xlim(0,12); ax.set_ylim(0,3.1); ax.axis('off')
labels=['Concept or\nprocess','Observable\nvariable','Measurement\nmethod','Sampling\nunit','Spatial & temporal\ndesign','Supported\ninference']
for i,l in enumerate(labels):
    x=.15+i*1.95; box(ax,x,1.25,1.55,.75,l,9.5)
    if i<5: ax.annotate('',xy=(x+1.9,1.62),xytext=(x+1.55,1.62),arrowprops=dict(arrowstyle='->',lw=1.1))
ax.text(5.95,.55,'Decisions at each step constrain what the observations can represent.',ha='center',fontsize=9)
save(fig,'figures/ch03/fig3_1_measurement_chain.png')

# Figure 3.4 accuracy / precision dartboards
fig, axes = plt.subplots(1,4,figsize=(11.2,2.9))
rng=np.random.default_rng(23)
configs=[('Accurate & precise',(0,0),0.10),('Accurate, less precise',(0,0),0.30),('Biased but precise',(0.42,0.28),0.10),('Biased & variable',(0.42,0.28),0.30)]
for ax,(ttl,mu,sd) in zip(axes,configs):
    ax.set_aspect('equal'); ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.axis('off')
    for r in [0.85,0.55,0.25]: ax.add_patch(Circle((0,0),r,fill=False,lw=0.9))
    pts=rng.normal(mu,sd,size=(18,2)); ax.scatter(pts[:,0],pts[:,1],s=13)
    ax.plot(0,0,marker='+',markersize=9)
    ax.set_title(ttl,fontsize=9.5)
save(fig,'figures/ch03/fig3_4_accuracy_precision.png')

# Figure 5.1 target/access/selected units
fig, ax = plt.subplots(figsize=(9.3,4.3)); ax.set_xlim(0,10); ax.set_ylim(0,5); ax.axis('off')
ax.add_patch(Rectangle((.4,.45),9.0,4.0,fill=False,lw=1.4)); ax.text(.65,4.1,'Target population',fontsize=11,weight='bold')
ax.add_patch(Rectangle((2.0,1.1),5.8,2.75,fill=False,lw=1.3)); ax.text(2.25,3.55,'Accessible population',fontsize=10.5,weight='bold')
rng=np.random.default_rng(7)
pts=np.column_stack([rng.uniform(.7,9.1,55),rng.uniform(.8,4.05,55)])
inside=(pts[:,0]>2.15)&(pts[:,0]<7.65)&(pts[:,1]>1.35)&(pts[:,1]<3.65)
ax.scatter(pts[:,0],pts[:,1],s=18,alpha=.55)
sel=np.where(inside)[0][::4][:8]
ax.scatter(pts[sel,0],pts[sel,1],s=70,facecolors='none',linewidths=1.5)
ax.text(6.05,.55,'circled points = selected sampling units',fontsize=9)
save(fig,'figures/ch05/fig5_1_target_access_sample.png')

# Figure 7.1 two points, many trajectories
fig, ax = plt.subplots(figsize=(7.7,4.2)); ax.set_xlim(0,10); ax.set_ylim(0,10); ax.spines[['top','right']].set_visible(False)
ax.set_xlabel('Time'); ax.set_ylabel('Response')
x=np.linspace(2,8,200)
curves=[3+4*(x-2)/6,
        3+4*((x-2)/6)**0.45,
        3+4*((x-2)/6)**2.2,
        3+4*(x-2)/6+1.5*np.sin(np.pi*(x-2)/3),
        3+4*(x-2)/6-1.6*np.sin(np.pi*(x-2)/3)]
for y in curves: ax.plot(x,y,lw=1.25,alpha=.7)
ax.scatter([2,8],[3,7],s=45,zorder=5)
ax.text(5,9.2,'The same two observations can fit very different trajectories',ha='center',fontsize=10)
save(fig,'figures/ch07/fig7_1_two_points_trajectories.png')

# Figure 7.4 repeated same units vs new samples
fig, axes = plt.subplots(1,2,figsize=(10.5,4.0),sharey=True)
rng=np.random.default_rng(17); times=np.arange(5)
for i in range(7):
    start=rng.normal(4,1); slope=rng.normal(.55,.18); vals=start+slope*times+rng.normal(0,.18,5)
    axes[0].plot(times,vals,marker='o',lw=1)
axes[0].set_title('Follow the same units'); axes[0].set_xlabel('Census'); axes[0].set_ylabel('Response')
for t in times:
    vals=rng.normal(4+.55*t,1.0,7); axes[1].scatter(np.full(7,t)+rng.normal(0,.04,7),vals,s=20)
axes[1].plot(times,[4+.55*t for t in times],lw=1.3)
axes[1].set_title('Draw a new sample each census'); axes[1].set_xlabel('Census')
for ax in axes: ax.spines[['top','right']].set_visible(False)
save(fig,'figures/ch07/fig7_4_repeated_vs_new.png')

# Figure 8.1 presence -> availability -> detection -> recording
fig, ax = plt.subplots(figsize=(10.5,3.6)); ax.set_xlim(0,10.5); ax.set_ylim(0,3.6); ax.axis('off')
rng=np.random.default_rng(31)
labels=['Present / using site','Available to method','Detected','Recorded correctly']
counts=[24,15,9,7]
for j,(lab,n) in enumerate(zip(labels,counts)):
    x=.35+j*2.55
    ax.add_patch(Rectangle((x,.5),2.0,2.3,fill=False,lw=1.1))
    pts=rng.uniform([x+.18,.75],[x+1.82,2.55],size=(n,2)); ax.scatter(pts[:,0],pts[:,1],s=18)
    ax.text(x+1.0,3.03,lab,ha='center',fontsize=9.5)
    if j<3: ax.annotate('',xy=(x+2.45,1.65),xytext=(x+2.05,1.65),arrowprops=dict(arrowstyle='->',lw=1.1))
save(fig,'figures/ch08/fig8_1_detection_filter.png')

# Figure 9.2 counterfactual problem
fig, axes = plt.subplots(1,2,figsize=(10.4,4.0),sharey=True)
# after-only
axes[0].scatter([0,1],[6.2,8.0],s=40); axes[0].set_xticks([0,1],['Comparison','Treated']); axes[0].set_title('After-only comparison')
axes[0].set_ylabel('Response'); axes[0].text(.5,8.7,'Difference after treatment',ha='center',fontsize=9)
# before after
axes[1].plot([0,1],[5.0,7.8],marker='o',label='Treated'); axes[1].plot([0,1],[4.2,6.5],marker='o',label='Comparison')
axes[1].plot([0,1],[5.0,7.3],linestyle='--',lw=1.1,label='Unobserved counterfactual')
axes[1].set_xticks([0,1],['Before','After']); axes[1].set_title('Before-after still needs a counterfactual'); axes[1].legend(frameon=False,fontsize=8)
for ax in axes: ax.spines[['top','right']].set_visible(False)
save(fig,'figures/ch09/fig9_2_counterfactual.png')

# Figure 9.3 BACI
fig, ax = plt.subplots(figsize=(7.6,4.2)); ax.set_xlim(-.1,1.1); ax.set_ylim(2.5,10); ax.spines[['top','right']].set_visible(False)
ax.plot([0,1],[4.0,8.0],marker='o',lw=1.5,label='Treated')
ax.plot([0,1],[4.6,6.0],marker='o',lw=1.5,label='Comparison')
ax.set_xticks([0,1],['Before','After']); ax.set_ylabel('Response'); ax.legend(frameon=False)
ax.annotate('change = +4.0',xy=(1,8.0),xytext=(.55,9.0),arrowprops=dict(arrowstyle='->',lw=.9),fontsize=9)
ax.annotate('change = +1.4',xy=(1,6.0),xytext=(.55,5.1),arrowprops=dict(arrowstyle='->',lw=.9),fontsize=9)
ax.text(.5,3.0,'BACI contrast = difference between these changes',ha='center',fontsize=9.5)
save(fig,'figures/ch09/fig9_3_baci.png')
