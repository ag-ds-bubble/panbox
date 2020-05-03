
from .pansim_anim_datagen import PanSimDataGenerator
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import numpy as np

# 0 : Sucessiptible
# 1 : Infected
# 2 : Removed
# 3 : Asymptomatic
# 4 : Quarentined

class PanSimulator(PanSimDataGenerator):
    
    def __init__(self, _initial_infected = 20, _initial_asymtomatic_pct = 0.5, _pop_density = 500,  _intervention_after = 0, _generator_type = 'angle_based', _simupdate_rate = 5, _rnaught_after=1.0):

        super().__init__(_initial_infected = _initial_infected, _initial_asymtomatic_pct = _initial_asymtomatic_pct,
                         _pop_density = _pop_density, _intervention_after = _intervention_after, 
                         _generator_type = _generator_type, _simupdate_rate = _simupdate_rate, _rnaught_after=_rnaught_after)
        self.daystatus = np.array([1,0,0,0,0])
        self.dayindex = []
        plt.rcParams['figure.dpi'] = 100

    def update_dynamic_params(self, _infect_radii = 2, _fatality_rate = 0.2, _trans_proba = 0.2, _incub_period = 14,
                              _quarantine_after = 2, _asympt_pct = 0.5, _social_distancing_factor = 0.0, _travel_radii = 100):
         
        self.infect_radii = _infect_radii
        self.fatality_rate = _fatality_rate
        self.trans_proba = _trans_proba
        self.asympt_pct = _asympt_pct
        self.quarantine_after = _quarantine_after * (1000/self.simupdate_rate)
        self.incub_period = _incub_period * (1000/self.simupdate_rate)
        self.social_distancing_factor = _social_distancing_factor
        self.travel_radii = _travel_radii

    def instantiate_sim_canvas(self):
        
        # Data Stream
        self.data_stream = self.simulator_datagen()
        # Plotting setup
        self._max_scatter_size = 30
        self._min_scatter_size = 0.02
        self.scatter_size = self._max_scatter_size*(np.exp(-((self.pop_density-10)/1000)*np.pi*0.5))
        self.scatter_size = np.clip(self.scatter_size, a_min=self._min_scatter_size, a_max=self._max_scatter_size)
        self.glow_radius = np.zeros(shape = self.pop_density)
        self.glow_cord = np.zeros(shape = (self.pop_density,2))
        self.SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        
        self.scatter_colormap = {0:'white',1:'red',2:'gray',3:'yellow',4:'purple'}
        self.scatter_edgecolormap = {0:'red',1:'gray',2:'yellow',3:'purple',4:'green'}
        self._edgelinewidth = 0.01*self.scatter_size if self.scatter_size > 1 else 0.0
        self.fig, self.ax = plt.subplots(figsize=(4,4))
        self.ani = animation.FuncAnimation(self.fig, self.update_sim_canvas, interval=self.simupdate_rate, 
                                           init_func=self.setup_sim_canvas, blit=True)
        plt.show()

    def instantiate_day_canvas(self):
        self.day_fig, self.day_ax = plt.subplots(figsize=(10,1.3))
        self.day_ani = animation.FuncAnimation(self.day_fig, self.update_day_canvas, interval=self.simupdate_rate, 
                                               init_func=self.setup_day_canvas, blit=True)
        plt.show()
    

    def setup_sim_canvas(self):
        """Initial drawing of the scatter plot."""
        _popcoord, _popstatus = next(self.data_stream)
        self.popstatus = _popstatus
        _c = np.vectorize(self.scatter_colormap.get)(_popstatus)
        _ec = np.vectorize(self.scatter_edgecolormap.get)(_popstatus)
        
        _glowstatus = _popstatus[(_popstatus==1) | (_popstatus == 3)]
        _glowcord = _popcoord[(_popstatus==1) | (_popstatus == 3)]
        _glowradius = self.scatter_size * 10
        _gec = np.vectorize(self.scatter_edgecolormap.get)(_glowstatus)
        
        self.ax.set_facecolor("black")
        self.ax.set_xlim(-0.02,1.02)
        self.ax.set_ylim(-0.02,1.02)
        self.ax.grid(which='both',linestyle='--')
        self.ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

        self.scat = self.ax.scatter(x = _popcoord[:,0], y = _popcoord[:,1], 
                                    facecolors=_c, edgecolors=_ec,
                                    c = _c, s = self.scatter_size,
                                    linewidths=self._edgelinewidth)
        
        self.scat_glow = self.ax.scatter(x = _glowcord[:,0], y = _glowcord[:,1], 
                                        facecolors='none', edgecolors=_gec,
                                        s = _glowradius, linewidths=self._edgelinewidth)
        
        self.rnaught_text = self.ax.text(0.8, 0.05, 'R0 : '.translate(self.SUB)+str(0), 
                                      transform=self.ax.transAxes,
                                      color='lightblue', fontweight='heavy', fontsize=10)
        self.day_text = self.ax.text(0.06, 0.05, 'Day : '+ str(0), 
                                      transform=self.ax.transAxes,
                                      color='lightgray', fontweight='light', fontsize=10)
        
        patch1 = plt.Line2D([0,0],[0,1], color='white', marker='o', linestyle='', markeredgecolor='k')
        patch2 = plt.Line2D([0,0],[0,1], color='red', marker='o', linestyle='', markeredgecolor='k')
        patch3 = plt.Line2D([0,0],[0,1], color='gray', marker='o', linestyle='', markeredgecolor='k')
        patch4 = plt.Line2D([0,0],[0,1], color='yellow', marker='o', linestyle='', markeredgecolor='k')
        patch5 = plt.Line2D([0,0],[0,1], color='purple', marker='o', linestyle='', markeredgecolor='k')

        #Create legend from custom artist/label lists
        self.ax.legend([patch1,patch2,patch3,patch4,patch5], 
                       ["Sucessiptible", "Infected", "Removed", 'Asymptomatic', 'Quarantined'],
                       loc='upper center', bbox_to_anchor=(0.5, 1.13),
                       ncol=3, fancybox=True, shadow=True, prop={'size': 8})
        
        return self.scat,
    
    def update_sim_canvas(self, i):
        """Update the scatter plot."""
        _popcoord, _popstatus = next(self.data_stream)
        self.popstatus = _popstatus
        _c = np.vectorize(self.scatter_colormap.get)(_popstatus)
        _ec = np.vectorize(self.scatter_edgecolormap.get)(_popstatus)
        self.scat.set_color(_c)
        self.scat.set_edgecolor(_ec)
        self.scat.set_offsets(_popcoord)
        
        t=i-(20*int(i/20))
        t = t%20 - int(t/10)*(t-10)*2
        _glowstatus = _popstatus[(_popstatus==1) | (_popstatus == 3)]
        _glowcord = _popcoord[(_popstatus==1) | (_popstatus == 3)]
        _glowradius = self.scatter_size*t
        _gec = np.vectorize(self.scatter_colormap.get)(_glowstatus)
        
        self.rnaught_text.set_text('R0: '.translate(self.SUB)+str(float(i)))
        self.day_text.set_text('Day : '+str(int(i/(1000/self.simupdate_rate))))
        self.scat_glow.set_edgecolor(_gec)
        self.scat_glow.set_offsets(_glowcord)
        self.scat_glow.set_sizes([_glowradius]*len(_glowcord))
        self.scat_glow.set_linewidths(t*(0.04*self.infect_radii))
        
        return self.scat,


    def setup_day_canvas(self):

        _unique = np.unique(self.popstatus, return_counts=True)
        _unique = {_unique[0][i]:_unique[1][i] for i in range(len(_unique[0]))}
        for i in range(5):
            if i not in _unique: _unique[i] = 0
        _vc_list = np.array([_unique[0],_unique[1],_unique[2],_unique[3],_unique[4]])/self.pop_density
        
        self.daystatus = np.vstack([self.daystatus,_vc_list])
        self.dayindex = ['Day '+str(k) for k in range(self.daystatus.shape[0])]
        _x = np.arange(self.daystatus.shape[0])
        self.day_ax.tick_params(left=False, labelleft=False, bottom=False,labelbottom=False)
        self.day_ax.set_facecolor('k')
        self.day_ax.grid(which='both',linestyle='-.')
        self.day_ax.set_ylim(0,1)
        
        self.day_ax.fill_between(_x, self.daystatus[:,1], interpolate=True, alpha=1.0,
                                 facecolor='#f5653d', edgecolor='k')
        self.day_ax.fill_between(_x, self.daystatus[:,3], interpolate=True, alpha=0.5,
                                 facecolor='#f2e677', edgecolor='k')
        self.day_ax.fill_between(_x, self.daystatus[:,2], y2=1, interpolate=True, alpha=0.5,
                                 facecolor='#999999', edgecolor='k')
        
        self.day_ax.text(0.955, 0.05, 'Infected : '+ str(np.round(_vc_list[1]*100,2))+'%', 
                        transform=self.day_ax.transAxes, color='k', fontweight='heavy', fontsize=6)
        self.day_ax.text(0.955, 0.35, 'Succeptible : '+ str(np.round(_vc_list[0]*100,2))+'%', 
                         transform=self.day_ax.transAxes, color='k', fontweight='heavy', fontsize=6)
        self.day_ax.text(0.955, 0.75, 'Removed : '+ str(np.round(_vc_list[2]*100,2))+'%', 
                         transform=self.day_ax.transAxes, color='k', fontweight='heavy', fontsize=6)
        self.day_ax.text(0.955, 0.55, 'Asymptomatic : '+ str(np.round(_vc_list[3]*100,2))+'%', 
                         transform=self.day_ax.transAxes, color='k', fontweight='heavy', fontsize=6)
        
        return self.day_fig,

    def update_day_canvas(self, i):

        _unique = np.unique(self.popstatus, return_counts=True)
        _unique = {_unique[0][j]:_unique[1][j] for j in range(len(_unique[0]))}
        for j in range(5):
            if j not in _unique: _unique[j] = 0
        _vc_list = np.array([_unique[0],_unique[1],_unique[2],_unique[3],_unique[4]])/self.pop_density
        self.daystatus = np.vstack([self.daystatus,_vc_list])
        self.dayindex = ['Day '+str(k) for k in range(self.daystatus.shape[0])]
        _x = np.arange(self.daystatus.shape[0])
        
        self.day_ax.clear()
        self.day_ax.grid(which='both',linestyle='--')
        self.day_ax.fill_between(_x, self.daystatus[:,1], interpolate=True, alpha=0.5, 
                                 facecolor='#f5653d', edgecolor='white')
        self.day_ax.fill_between(_x, self.daystatus[:,3], interpolate=True, alpha=0.5,
                                 facecolor='#f2e677', edgecolor='white')
        self.day_ax.fill_between(_x, 1-self.daystatus[:,2], y2=1, interpolate=True, alpha=0.5,
                                 facecolor='#999999', edgecolor='white')
        
        self.day_ax.text(0.955, (_vc_list[3]+_vc_list[1])/2, 'I :'+ str(np.round(_vc_list[1]*100,2))+'%', 
                         transform=self.day_ax.transAxes, color='lightgray', fontweight='heavy', 
                         fontsize=5)
        self.day_ax.text(0.955, _vc_list[3]/2, 'A :'+ str(np.round(_vc_list[3]*100,2))+'%', 
                         transform=self.day_ax.transAxes, color='lightgray', fontweight='heavy', 
                         fontsize=5)
        
        self.day_ax.text(0.955, ((1-_vc_list[2]) + max(_vc_list[3],_vc_list[1]))/2, 'S :'+ str(np.round(_vc_list[0]*100,2))+'%', 
                         transform=self.day_ax.transAxes, color='lightgray', fontweight='heavy', 
                         fontsize=5)
        
        self.day_ax.text(0.955, 1-(_vc_list[2]/2), 'R :'+ str(np.round(_vc_list[2]*100,2))+'%', 
                         transform=self.day_ax.transAxes, color='lightgray', fontweight='heavy', 
                         fontsize=5)

        return self.day_fig,