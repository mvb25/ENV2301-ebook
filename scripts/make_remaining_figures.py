from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Ellipse, Polygon, FancyArrowPatch
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]

plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 11,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
})


def out(ch, name):
    p = ROOT / 'figures' / ch
    p.mkdir(parents=True, exist_ok=True)
    return p / name


def save(fig, path, dpi=220):
    fig.savefig(path, dpi=dpi, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def box(ax, xy, w, h, text, lw=1.3, fs=10, rounded=True):
    x,y=xy
    patch = FancyBboxPatch((x,y),w,h, boxstyle='round,pad=0.02,rounding_size=0.02' if rounded else 'square,pad=0.02',
                           fill=False, linewidth=lw)
    ax.add_patch(patch)
    ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=fs,wrap=True)
    return patch


def arrow(ax, a, b, lw=1.3, style='-|>', connectionstyle='arc3'):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle=style,mutation_scale=12,linewidth=lw,
                                connectionstyle=connectionstyle))

# 1.2 pollution causal pathway
fig, ax = plt.subplots(figsize=(10,3.6)); ax.set_axis_off(); ax.set_xlim(0,1); ax.set_ylim(0,1)
labels=[('Pollutant\ngeneration',0.03),('Treatment',0.24),('Discharge',0.43),('Downstream\nexposure',0.62),('Ecological\nresponse',0.82)]
for t,x in labels: box(ax,(x,0.55),0.15,0.20,t)
for (_,x1),(_,x2) in zip(labels[:-1],labels[1:]): arrow(ax,(x1+0.15,0.65),(x2,0.65))
for x,t in [(0.44,'Outlet\nchemistry'),(0.63,'Water chemistry\n+ flow'),(0.83,'Biological\nmonitoring')]:
    box(ax,(x,0.12),0.14,0.18,t,lw=1.0,fs=9)
    arrow(ax,(x+0.07,0.30),(x+0.07,0.54),lw=1.0)
save(fig,out('ch01','fig1_2_pollution_pathway.png'))

# 1.3 SET local record vs landscape representation
fig, axs = plt.subplots(1,2,figsize=(10,4.0), gridspec_kw={'width_ratios':[1,1.2]})
ax=axs[0]
y=np.array([0,0.8,1.5,2.4,3.0,3.8,4.6]); x=np.arange(len(y))
ax.plot(x,y,marker='o'); ax.set_xlabel('Monitoring time'); ax.set_ylabel('Surface elevation change'); ax.set_xticks([]); ax.spines[['top','right']].set_visible(False)
ax.text(0.04,0.93,'One SET',transform=ax.transAxes,ha='left',va='top',weight='bold')
ax=axs[1]; ax.set_axis_off(); ax.set_xlim(0,10); ax.set_ylim(0,7)
# mangrove patch abstract coastline
poly=Polygon([(0.4,0.8),(9.4,0.8),(9.2,6.0),(7.8,6.4),(5.8,5.7),(3.8,6.5),(1.1,5.7)],fill=False,linewidth=1.4)
ax.add_patch(poly)
# channels
ax.plot([1.0,3.0,5.0,7.5,9.1],[1.3,2.0,1.2,2.3,1.5],linewidth=1.0)
for p in [(2,4.7),(4.2,3.5),(6.0,4.8),(7.8,3.4),(5.0,2.2)]:
    ax.add_patch(Circle(p,0.15,fill=False,linewidth=1.1))
ax.add_patch(Circle((2,4.7),0.30,fill=False,linewidth=2.0))
ax.text(2,5.2,'SET',ha='center',va='bottom',weight='bold')
ax.text(5.0,6.65,'A variable mangrove landscape',ha='center',va='bottom')
ax.text(5.0,0.22,'A precise local record does not by itself describe all locations',ha='center',va='bottom',fontsize=9)
save(fig,out('ch01','fig1_3_set_scale.png'))

# 2.2 vegetation-environment feedback framework
fig, ax = plt.subplots(figsize=(10,5.1)); ax.set_axis_off(); ax.set_xlim(0,1); ax.set_ylim(0,1)
box(ax,(0.05,0.70),0.18,0.15,'Landscape context\n& history',fs=9)
box(ax,(0.05,0.40),0.18,0.15,'Disturbance\n& land use',fs=9)
box(ax,(0.32,0.68),0.20,0.16,'Species\navailability')
box(ax,(0.32,0.35),0.20,0.16,'Abiotic & biotic\nconditions')
box(ax,(0.62,0.52),0.17,0.17,'Species\nperformance')
box(ax,(0.84,0.52),0.13,0.17,'Plant\ncommunity')
arrow(ax,(0.23,0.77),(0.32,0.76)); arrow(ax,(0.23,0.48),(0.32,0.43))
arrow(ax,(0.52,0.76),(0.62,0.63)); arrow(ax,(0.52,0.43),(0.62,0.57)); arrow(ax,(0.79,0.605),(0.84,0.605))
# feedback community to conditions
arrow(ax,(0.90,0.52),(0.52,0.38),connectionstyle='arc3,rad=-0.33')
# community to availability via reproduction/source
arrow(ax,(0.90,0.69),(0.52,0.77),connectionstyle='arc3,rad=0.28')
ax.text(0.72,0.20,'Feedbacks allow vegetation to alter\nthe conditions and species pool that shape later change',ha='center',va='center',fontsize=9)
save(fig,out('ch02','fig2_2_feedback_framework.png'))

# 2.3 life-history strategies across demographic stages
fig, ax = plt.subplots(figsize=(10,4.4)); ax.set_xlim(-0.5,4.5); ax.set_ylim(-0.15,1.15); ax.set_yticks([0,1]); ax.set_yticklabels(['Persistence / stress tolerance','Rapid colonisation / acquisition']); ax.set_xticks(range(5)); ax.set_xticklabels(['Availability','Establishment','Growth','Survival','Reproduction']); ax.spines[['top','right']].set_visible(False)
# two contrasting strategies
x=np.arange(5)
ax.plot(x,[1.0,0.75,1.0,0.25,0.95],marker='o',linewidth=2,label='Fast / acquisitive')
ax.plot(x,[0.25,0.75,0.35,1.0,0.40],marker='o',linewidth=2,label='Persistent / conservative')
ax.set_ylim(-0.2,1.2); ax.set_yticks([]); ax.legend(frameon=False,ncol=2,loc='upper center',bbox_to_anchor=(0.5,1.14))
ax.set_xlabel('Different strategies can succeed at different stages of the life cycle')
save(fig,out('ch02','fig2_3_trait_strategies.png'))

# 2.4 alternative successional pathways
fig, axs = plt.subplots(1,3,figsize=(10.5,3.4),sharex=True,sharey=True)
t=np.linspace(0,1,100)
# converge
axs[0].plot(t,0.2+0.7*(1-np.exp(-4*t)),linewidth=2); axs[0].plot(t,0.65+0.25*(1-np.exp(-3*t)),linewidth=2)
# remain separated / parallel
axs[1].plot(t,0.15+0.55*t,linewidth=2); axs[1].plot(t,0.45+0.55*t,linewidth=2)
# diverge
axs[2].plot(t,0.35+0.5*t,linewidth=2); axs[2].plot(t,0.35+0.15*t,linewidth=2)
for ax,label in zip(axs,['Converge','Remain different','Diverge']):
    ax.text(0.5,0.95,label,transform=ax.transAxes,ha='center',va='top',weight='bold'); ax.set_xticks([]); ax.set_yticks([]); ax.spines[['top','right']].set_visible(False); ax.set_xlabel('Time')
axs[0].set_ylabel('Vegetation state')
save(fig,out('ch02','fig2_4_alternative_pathways.png'))

# 2.5 intervention roles
fig, axs = plt.subplots(1,3,figsize=(10.5,3.8))
for ax in axs: ax.set_axis_off(); ax.set_xlim(0,1); ax.set_ylim(0,1)
# substitute
box(axs[0],(0.05,0.38),0.25,0.20,'Missing\nprocess',fs=9); box(axs[0],(0.65,0.38),0.25,0.20,'Outcome',fs=9); arrow(axs[0],(0.30,0.48),(0.65,0.48)); axs[0].plot([0.39,0.57],[0.57,0.39],linewidth=1.4); axs[0].plot([0.39,0.57],[0.39,0.57],linewidth=1.4); axs[0].text(0.5,0.73,'Intervention substitutes',ha='center',weight='bold'); arrow(axs[0],(0.5,0.69),(0.5,0.53))
# initiate
box(axs[1],(0.05,0.38),0.25,0.20,'Blocked\nprocess',fs=9); box(axs[1],(0.65,0.38),0.25,0.20,'Self-sustaining\nchange',fs=9); arrow(axs[1],(0.30,0.48),(0.65,0.48)); axs[1].text(0.5,0.73,'Intervention initiates',ha='center',weight='bold'); arrow(axs[1],(0.5,0.69),(0.5,0.53))
# enhance
box(axs[2],(0.05,0.38),0.25,0.20,'Weak\nprocess',fs=9); box(axs[2],(0.65,0.38),0.25,0.20,'Stronger\nresponse',fs=9); arrow(axs[2],(0.30,0.48),(0.65,0.48),lw=2.2); axs[2].text(0.5,0.73,'Intervention enhances',ha='center',weight='bold'); arrow(axs[2],(0.5,0.69),(0.5,0.53))
save(fig,out('ch02','fig2_5_intervention_roles.png'))

# 3.2 canopy/light methods and supports
fig, ax = plt.subplots(figsize=(10,4.3)); ax.set_xlim(0,10); ax.set_ylim(0,4); ax.set_axis_off()
methods=[('PAR sensor',1.0,0.6,0.35),('Canopy photo',4.0,1.4,1.0),('Canopy / LAI\nmeasurement',7.2,2.3,1.8)]
for name,x,spatial,temporal in methods:
    ax.add_patch(Circle((x,2.2),0.25,fill=False,linewidth=1.5)); ax.text(x,3.0,name,ha='center',va='center',weight='bold')
    ax.hlines(1.45,x-spatial/2,x+spatial/2,linewidth=4); ax.vlines(x,0.45,0.45+temporal,linewidth=4)
ax.text(0.3,1.45,'Spatial\nsupport',ha='left',va='center',fontsize=9); ax.text(0.3,0.75,'Temporal\nsupport',ha='left',va='center',fontsize=9)
ax.text(9.6,0.25,'Methods can describe different parts of the same light environment',ha='right',va='bottom',fontsize=9)
save(fig,out('ch03','fig3_2_light_methods.png'))

# 3.3 soil gas flux components
fig, axs = plt.subplots(1,2,figsize=(9.5,4.1),sharey=True)
for ax,title,light in zip(axs,['Transparent chamber','Opaque chamber'],[True,False]):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_axis_off(); ax.text(0.5,0.95,title,ha='center',va='top',weight='bold')
    # soil
    ax.add_patch(Rectangle((0.08,0.08),0.84,0.28,fill=False,linewidth=1.4)); ax.text(0.5,0.13,'soil + roots + microbes',ha='center',fontsize=9)
    # chamber
    ax.add_patch(Rectangle((0.25,0.36),0.5,0.43,fill=False,linewidth=1.6)); ax.text(0.5,0.70,'chamber',ha='center')
    # respiration up
    arrow(ax,(0.42,0.30),(0.42,0.61),lw=1.7); ax.text(0.28,0.46,'CO$_2$',fontsize=9)
    if light:
        # downward uptake
        arrow(ax,(0.61,0.62),(0.61,0.34),lw=1.7); ax.text(0.65,0.46,'light-dependent\nuptake',fontsize=8,va='center')
        ax.annotate('',xy=(0.76,0.82),xytext=(0.90,0.95),arrowprops=dict(arrowstyle='-|>',lw=1.2))
    else:
        ax.add_patch(Rectangle((0.25,0.36),0.5,0.43,fill=False,linewidth=3.0))
    arrow(ax,(0.50,0.79),(0.50,0.92),lw=1.8)
    ax.text(0.55,0.86,'net flux',fontsize=9,va='center')
save(fig,out('ch03','fig3_3_flux_components.png'))

# 7.2 constrained trajectories + extrapolation
fig, ax = plt.subplots(figsize=(9.5,4.4))
rng=np.random.default_rng(3); x=np.array([0,1,2,3,4,5]); y=1.2+2.5*(1-np.exp(-0.55*x))+rng.normal(0,0.07,len(x))
ax.scatter(x,y,zorder=4)
xx=np.linspace(0,8,200)
# simple fits: linear and saturating-like chosen to fit observed range
coef=np.polyfit(x,y,1); lin=np.polyval(coef,xx)
# saturating with plausible form anchored approximately
sat=1.15+2.85*(1-np.exp(-0.52*xx))
ax.plot(xx[xx<=5],lin[xx<=5],linewidth=1.6); ax.plot(xx[xx<=5],sat[xx<=5],linewidth=1.6)
ax.plot(xx[xx>5],lin[xx>5],linestyle='--',linewidth=1.6); ax.plot(xx[xx>5],sat[xx>5],linestyle='--',linewidth=1.6)
ax.axvspan(5,8,alpha=0.08); ax.text(6.5,ax.get_ylim()[1]*0.96,'beyond observed period',ha='center',va='top',fontsize=9)
ax.set_xlabel('Time'); ax.set_ylabel('Response'); ax.spines[['top','right']].set_visible(False)
save(fig,out('ch07','fig7_2_constrained_trajectories.png'))

# 7.3 temporal grain and duration
fig, axs=plt.subplots(1,2,figsize=(10.2,4.0))
# frequency/grain
ax=axs[0]; t=np.linspace(0,10,500); y=np.sin(2*np.pi*t/2.2)+0.35*np.sin(2*np.pi*t/0.5)
ax.plot(t,y,linewidth=1.1); fine=np.arange(0,10.01,0.5); coarse=np.arange(0,10.01,2.0)
ax.scatter(fine,np.interp(fine,t,y),s=16,label='frequent'); ax.scatter(coarse,np.interp(coarse,t,y),s=35,marker='s',label='coarse')
ax.set_xlabel('Time'); ax.set_ylabel('Environmental response'); ax.legend(frameon=False,loc='upper right'); ax.spines[['top','right']].set_visible(False)
# duration
ax=axs[1]; ax.set_xlim(0,24); ax.set_ylim(0,3); ax.set_yticks([0.9,2.1]); ax.set_yticklabels(['24 monthly\nobservations','24 annual\nobservations']); ax.set_xlabel('Study duration'); ax.set_xticks([0,2,5,10,15,20,24])
for xx in np.linspace(0,2,24): ax.plot(xx,2.1,'o',ms=3)
for xx in np.linspace(0,24,24): ax.plot(xx,0.9,'o',ms=3)
ax.hlines(2.1,0,2,linewidth=1); ax.hlines(0.9,0,24,linewidth=1); ax.spines[['top','right','left']].set_visible(False); ax.tick_params(axis='y',length=0)
save(fig,out('ch07','fig7_3_temporal_grain_duration.png'))

# 7.5 chronosequence logic
fig, axs=plt.subplots(1,2,figsize=(10.2,4.2),sharey=True)
# longitudinal
ax=axs[0]; t=np.array([1,5,10,20,35]); state=1+3*(1-np.exp(-t/12)); ax.plot(t,state,marker='o'); ax.set_xlabel('Time since disturbance'); ax.set_ylabel('Forest state'); ax.spines[['top','right']].set_visible(False); ax.text(0.05,0.94,'Same site through time',transform=ax.transAxes,ha='left',va='top',weight='bold')
# chronoseq different sites
ax=axs[1]; age=np.array([1,5,10,20,35]); base=1+3*(1-np.exp(-age/12)); offsets=np.array([0.0,0.35,-0.2,0.45,-0.3]); ax.scatter(age,base+offsets,s=55); ax.plot(age,base,linestyle='--',linewidth=1.2); ax.set_xlabel('Age of different sites'); ax.spines[['top','right','left']].set_visible(False); ax.tick_params(axis='y',left=False,labelleft=False); ax.text(0.05,0.94,'Space-for-time',transform=ax.transAxes,ha='left',va='top',weight='bold')
for x,y,i in zip(age,base+offsets,range(1,6)): ax.text(x,y+0.12,f'Site {i}',ha='center',fontsize=8)
save(fig,out('ch07','fig7_5_chronosequence.png'))

# 8.2 distance and detection
fig, axs=plt.subplots(1,2,figsize=(9.8,4.2))
ax=axs[0]; ax.set_aspect('equal'); ax.set_xlim(-1.1,1.1); ax.set_ylim(-1.1,1.1); ax.axis('off')
for r in [0.35,0.7,1.0]: ax.add_patch(Circle((0,0),r,fill=False,linewidth=1.0))
ax.plot(0,0,marker='^',ms=9); pts=np.array([[.2,.15],[-.4,.1],[.55,.35],[-.65,-.45],[.85,-.15],[-.1,.8]])
ax.scatter(pts[:,0],pts[:,1],s=25); ax.text(0,-1.06,'Point-count station',ha='center',va='top',fontsize=9)
ax=axs[1]; d=np.linspace(0,100,200); p=np.exp(-(d/55)**2); p2=np.exp(-(d/38)**2)
ax.plot(d,p,label='open vegetation'); ax.plot(d,p2,label='dense vegetation'); ax.set_xlabel('Distance from observer'); ax.set_ylabel('Probability of detection'); ax.set_ylim(0,1.05); ax.spines[['top','right']].set_visible(False); ax.legend(frameon=False)
save(fig,out('ch08','fig8_2_distance_detection.png'))

# 8.3 methods as filters matrix
fig, ax=plt.subplots(figsize=(9.8,4.6)); ax.set_axis_off(); ax.set_xlim(0,7); ax.set_ylim(0,6)
animals=['calling bird','quiet bird','ground mammal','small mammal','frog']
methods=['Point count','Acoustic','Camera','Mist net','Pitfall']
# matrix strength 0/1
M=np.array([[1,1,0,1,0],[1,0,0,1,0],[0,0,1,0,0],[0,0,1,1,0],[0,1,0,0,1]])
for j,a in enumerate(animals): ax.text(j+1.65,5.5,a,ha='center',va='bottom',fontsize=8,rotation=20)
for i,m in enumerate(methods): ax.text(0.75,4.7-i,m,ha='right',va='center',fontsize=9)
for i in range(5):
    for j in range(5):
        ax.add_patch(Circle((j+1.65,4.7-i),0.13,fill=bool(M[i,j]),linewidth=1.1))
ax.text(4.1,0.25,'Different methods reveal different subsets of the same community',ha='center',fontsize=9)
save(fig,out('ch08','fig8_3_method_filters.png'))

# 8.4 movement/stations/effort
fig, axs=plt.subplots(1,2,figsize=(10.2,4.2))
ax=axs[0]; ax.set_aspect('equal'); ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis('off')
# stations
for x,y in [(2,2),(5,2.5),(8,2),(3.5,5.2),(7,5)]: ax.plot(x,y,marker='s',ms=7)
# home ranges
for cx,cy,w,h in [(3.5,3.1,5.2,3.7),(6.8,3.6,4.6,4.4),(5.0,4.7,3.3,2.4)]: ax.add_patch(Ellipse((cx,cy),w,h,fill=False,linewidth=1.2,linestyle='--'))
ax.text(5,6.7,'Animal movement can connect several stations',ha='center',va='top',fontsize=9)
ax=axs[1]; ax.set_xlim(0,10); ax.set_ylim(0,6); ax.axis('off')
# equal effort layouts
ax.text(2.5,5.5,'Few long deployments',ha='center',weight='bold',fontsize=9); ax.text(7.5,5.5,'More shorter deployments',ha='center',weight='bold',fontsize=9)
for x in [1.8,3.2]: ax.add_patch(Rectangle((x-0.18,1.1),0.36,3.6,fill=False,linewidth=1.3))
for x in np.linspace(5.6,9.2,6): ax.add_patch(Rectangle((x-0.13,2.2),0.26,1.2,fill=False,linewidth=1.1))
ax.text(5,0.45,'Equal total camera-days can represent space differently',ha='center',fontsize=9)
save(fig,out('ch08','fig8_4_movement_effort.png'))

# 8.5 habitat effect on abundance and detection
fig, ax=plt.subplots(figsize=(9.8,4.2)); ax.set_axis_off(); ax.set_xlim(0,1); ax.set_ylim(0,1)
box(ax,(0.06,0.43),0.18,0.16,'Habitat\nstructure')
box(ax,(0.39,0.65),0.18,0.16,'True\nabundance')
box(ax,(0.39,0.20),0.18,0.16,'Detection\nprobability')
box(ax,(0.75,0.43),0.18,0.16,'Recorded\ndetections')
arrow(ax,(0.24,0.53),(0.39,0.72)); arrow(ax,(0.24,0.49),(0.39,0.29)); arrow(ax,(0.57,0.73),(0.75,0.55)); arrow(ax,(0.57,0.28),(0.75,0.47))
ax.text(0.50,0.04,'The same habitat variable can change both animals and how easily we observe them',ha='center',fontsize=9)
save(fig,out('ch08','fig8_5_habitat_detection_confound.png'))

# 8.6 seed dispersal observation pathway
fig, ax=plt.subplots(figsize=(10.5,4.3)); ax.set_axis_off(); ax.set_xlim(0,1); ax.set_ylim(0,1)
steps=[('Source\ntrees',0.03),('Frugivore\nactivity',0.23),('Seed\nmovement',0.43),('Seed\nrain',0.63),('Recruitment',0.82)]
for t,x in steps: box(ax,(x,0.55),0.14,0.17,t,fs=9)
for (_,x1),(_,x2) in zip(steps[:-1],steps[1:]): arrow(ax,(x1+0.14,0.635),(x2,0.635))
methods=[('Landscape\nmap',0.03),('Point count /\nacoustic',0.23),('Feeding /\ntracking',0.43),('Seed traps',0.63),('Seedling\nplots',0.82)]
for t,x in methods:
    ax.text(x+0.07,0.20,t,ha='center',va='center',fontsize=8)
    arrow(ax,(x+0.07,0.29),(x+0.07,0.53),lw=0.9)
save(fig,out('ch08','fig8_6_process_linkage.png'))

# 9.1 observational -> experimental continuum
fig, ax=plt.subplots(figsize=(10,3.4)); ax.set_axis_off(); ax.set_xlim(0,1); ax.set_ylim(0,1)
arrow(ax,(0.08,0.52),(0.92,0.52),lw=1.8)
positions=[(0.15,'Natural\nvariation'),(0.38,'Matched\ncomparison'),(0.61,'Quasi-\nexperiment'),(0.84,'Randomised\nfield experiment')]
for x,t in positions:
    ax.plot(x,0.52,'o',ms=9); ax.text(x,0.68,t,ha='center',va='bottom',fontsize=9)
ax.text(0.10,0.22,'less control over exposure',ha='left',fontsize=9); ax.text(0.90,0.22,'more control over exposure',ha='right',fontsize=9)
save(fig,out('ch09','fig9_1_design_continuum.png'))

# 9.4 random assignment / blocking / matching
fig, axs=plt.subplots(1,3,figsize=(10.5,4.2))
for ax,title in zip(axs,['Random assignment','Blocking','Matching']):
    ax.set_axis_off(); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.text(0.5,0.94,title,ha='center',va='top',weight='bold')
# Random assignment: 8 units -> 2 groups
for i,y in enumerate(np.linspace(.18,.75,8)): axs[0].plot(.18,y,'o',ms=7)
for i,y in enumerate(np.linspace(.24,.72,4)): axs[0].plot(.78,y,'o',ms=7); axs[0].plot(.58,y,'o',ms=7)
arrow(axs[0],(.30,.48),(.52,.48)); axs[0].text(.58,.10,'A',ha='center'); axs[0].text(.78,.10,'B',ha='center')
# blocking by background condition (low/high)
for yy in [.28,.68]:
    axs[1].add_patch(Rectangle((.08,yy-.12),.84,.24,fill=False,linewidth=1.0))
    for xx in [.22,.38,.62,.78]: axs[1].plot(xx,yy,'o',ms=7)
    axs[1].text(.03,yy,'block',ha='left',va='center',fontsize=8)
axs[1].text(.5,.10,'assign treatments within each block',ha='center',fontsize=8)
# matching pairs
pairs=[(.25,.70),(.25,.50),(.25,.30)]
for x,y in pairs:
    axs[2].plot(x,y,'o',ms=7); axs[2].plot(.75,y,'o',ms=7); axs[2].plot([x+.05,.70],[y,y],linestyle='--',linewidth=1)
axs[2].text(.25,.12,'treated',ha='center',fontsize=8); axs[2].text(.75,.12,'comparison',ha='center',fontsize=8)
save(fig,out('ch09','fig9_4_assignment_blocking_matching.png'))

# 9.5 interaction lines
fig, axs=plt.subplots(1,2,figsize=(9.5,4.1),sharey=True)
x=np.array([0,1])
axs[0].plot(x,[1.0,2.0],marker='o'); axs[0].plot(x,[2.0,3.0],marker='o'); axs[0].set_title('Little interaction')
axs[1].plot(x,[1.0,1.25],marker='o'); axs[1].plot(x,[1.8,3.4],marker='o'); axs[1].set_title('Interaction')
for ax in axs:
    ax.set_xticks([0,1]); ax.set_xticklabels(['No nutrients','Nutrients added']); ax.set_xlabel('Nutrient treatment'); ax.spines[['top','right']].set_visible(False)
axs[0].set_ylabel('Seedling growth'); axs[0].legend(['Lianas present','Lianas removed'],frameon=False,loc='upper left')
save(fig,out('ch09','fig9_5_interaction.png'))

print('Generated remaining figures')
