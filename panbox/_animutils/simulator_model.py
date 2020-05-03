
import numpy as np
from .simulator_model_datagen import ModelAnimDataGenerator
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.animation as animation

class ModelSimulator():
    
    def __init__(self, datapacket, modelname="S_I_R"):
        
        # Initialise the Figure
        plt.rcParams['figure.dpi'] = 50
        self.sim_fig, self.sim_ax = plt.subplots(figsize=(19.5,8))
        self.sim_fig.tight_layout()
        _,_,self.scaleFactor = datapacket
        
        # Initialise Datageneator
        self.dataGenerator = ModelAnimDataGenerator(modelname=modelname)
        self.modelDataGenerator = self.dataGenerator.dataGen(_dp = datapacket)

        self.sim_ani = animation.FuncAnimation(self.sim_fig, self.update_canvas, interval=100, 
                                               init_func = self.setup_canvas, blit=True)
        plt.show()
        
    def setup_canvas(self):

        # Check the dates
        dates, data = next(self.modelDataGenerator)

        self.sim_ax.tick_params(left=False, labelleft=False,)
        self.sim_ax.set_facecolor('k')
        self.sim_ax.grid(which='both',linestyle='-.')
        self.sim_ax.set_ylim(0,1)

        # Add Pandemic Name Label
        prop = dict(facecolor='none', edgecolor='lightgray', lw=4, boxstyle='round, pad=0.2')
        self.sim_ax.text(0.015,0.87, 'COVID-19', 
                    transform=self.sim_ax.transAxes, color='w',
                    fontweight='heavy', fontsize=60, bbox = prop)

        # Add population and succeptible
        prop = dict(facecolor='#5c5c5c', edgecolor='#ffe680', lw=2, boxstyle='round')
        self.pop_text = '1,00,00,000'
        self.sim_ax.text(0.015,0.77, 'Population', 
                         transform=self.sim_ax.transAxes, color='w',
                         fontweight='heavy', fontsize=10, bbox = prop)
        self.poptext = self.sim_ax.text(0.015,0.735, self.pop_text, 
                                        transform=self.sim_ax.transAxes, color='w',
                                        fontweight='heavy', fontsize=10)

        prop = dict(facecolor='#5c5c5c', edgecolor='#ffe680', lw=2, boxstyle='round')
        self.succep_text = '1,00,000'
        self.sim_ax.text(0.075,0.77, 'Succeptible', 
                                 transform=self.sim_ax.transAxes, color='w',
                                 fontweight='heavy', fontsize=10, bbox = prop)
        self.succeptext = self.sim_ax.text(0.075,0.735, self.succep_text, 
                                            transform=self.sim_ax.transAxes, color='w',
                                            fontweight='heavy', fontsize=10)

        # Add Infected
        prop = dict(facecolor='#ff7575', edgecolor='#ffe680', lw=2, boxstyle='round')
        self.sim_fig.patches.extend([Rectangle((0.035,0.55), 0.1, 0.152, fill=True, 
                                  alpha=1, facecolor='none', edgecolor='w', lw=1,
                                  transform=self.sim_fig.transFigure, figure=self.sim_fig, zorder=1)])
        self.sim_fig.patches.extend([Rectangle((0.08,0.55), 0.055, 0.07, fill=True, 
                                  alpha=1, facecolor='none', edgecolor='w', lw=1,
                                  transform=self.sim_fig.transFigure, figure=self.sim_fig, zorder=1)])
        self.sim_fig.patches.extend([Rectangle((0.08,0.63), 0.055, 0.07, fill=True, 
                                  alpha=1, facecolor='none', edgecolor='w', lw=1,
                                  transform=self.sim_fig.transFigure, figure=self.sim_fig, zorder=1)])

        prop = dict(facecolor='#a34d4d', edgecolor='w', lw=2)
        self.infected_text = '{0}\n    %'.format('00.0')
        self.sim_ax.text(0.0153,0.558,'I\nN\nF\nE\nC\nT\nE\nD', 
                    transform=self.sim_ax.transAxes, color='w',
                    fontweight='light', fontsize=8.2, bbox = prop)
        self.infectedtext = self.sim_ax.text(0.026,0.615, self.infected_text, 
                                              transform=self.sim_ax.transAxes, color='w',
                                              fontweight='heavy', fontsize=13)


        prop = dict(facecolor='#a34d4d', edgecolor='w', lw=1)
        self.testing_text = '{0}%'.format('00.0')
        self.sim_ax.text(0.062,0.68,'    Tested    ', 
                    transform=self.sim_ax.transAxes, color='w',
                    fontweight='heavy', fontsize=10, bbox = prop)
        self.testingtext = self.sim_ax.text(0.067,0.64,self.testing_text, 
                        transform=self.sim_ax.transAxes, color='w',
                        fontweight='heavy', fontsize=15)

        prop = dict(facecolor='#a34d4d', edgecolor='w', lw=1)
        self.asympto_text = '{0}%'.format('00.0')
        self.sim_ax.text(0.061,0.6,'   Asympto   ', 
                    transform=self.sim_ax.transAxes, color='w',
                    fontweight='heavy', fontsize=10, bbox = prop)
        self.asymptotext = self.sim_ax.text(0.067,0.56,self.asympto_text, 
                                            transform=self.sim_ax.transAxes, color='w',
                                            fontweight='heavy', fontsize=15)


        # Add Removed

        prop = dict(facecolor='#5c5c5c', edgecolor='#ffe680', lw=2, boxstyle='round')
        self.sim_fig.patches.extend([Rectangle((0.035,0.35), 0.1, 0.152, fill=True, 
                                  alpha=1, facecolor='none', edgecolor='w', lw=1,
                                  transform=self.sim_fig.transFigure, figure=self.sim_fig, zorder=1)])
        self.sim_fig.patches.extend([Rectangle((0.08,0.35), 0.055, 0.07, fill=True, 
                                  alpha=1, facecolor='none', edgecolor='w', lw=1,
                                  transform=self.sim_fig.transFigure, figure=self.sim_fig, zorder=1)])
        self.sim_fig.patches.extend([Rectangle((0.08,0.43), 0.055, 0.07, fill=True, 
                                  alpha=1, facecolor='none', edgecolor='w', lw=1,
                                  transform=self.sim_fig.transFigure, figure=self.sim_fig, zorder=1)])

        prop = dict(facecolor='#5c5c5c', edgecolor='w', lw=2)
        self.removed_text = '{0}\n    %'.format('00.0')
        self.sim_ax.text(0.015,0.342,'R\nE\nM\nO\nV\nE\nD\n', 
                    transform=self.sim_ax.transAxes, color='w',
                    fontweight='light', fontsize=8.2, bbox = prop)
        self.removedtext = self.sim_ax.text(0.025, 0.4, self.infected_text, 
                    transform=self.sim_ax.transAxes, color='w',
                    fontweight='heavy', fontsize=13)


        prop = dict(facecolor='#5c5c5c', edgecolor='w', lw=2)
        self.recov_text = '{0}%'.format('00.0')
        self.sim_ax.text(0.0625, 0.47,' Recovered ', 
                    transform=self.sim_ax.transAxes, color='w',
                    fontweight='heavy', fontsize=10, bbox = prop)
        self.recovtext = self.sim_ax.text(0.067,0.43,self.recov_text, 
                    transform=self.sim_ax.transAxes, color='w',
                    fontweight='heavy', fontsize=15)

        prop = dict(facecolor='#5c5c5c', edgecolor='w', lw=2)
        self.death_text = '{0}%'.format('00.0')
        self.sim_ax.text(0.062,0.38,'    Death      ', 
                    transform=self.sim_ax.transAxes, color='w',
                    fontweight='heavy', fontsize=10, bbox = prop)
        self.deathtext = self.sim_ax.text(0.066, 0.34,self.death_text, 
                    transform=self.sim_ax.transAxes, color='w',
                    fontweight='heavy', fontsize=15)

        self.infectedfill = self.sim_ax.fill_between(dates, data[:,1], interpolate=True, alpha=1.0,
                                 facecolor='#f5653d', edgecolor='k')
        self.removedfill = self.sim_ax.fill_between(dates, 1-data[:,2], y2=1, interpolate=True, alpha=0.5,
                                 facecolor='#999999', edgecolor='k')
        
        infec_val = data[:,1][-1]
        self.infeclbl_text = 'Infected \n{0}%'
        self.infeclbltext = self.sim_ax.text(0.96, infec_val*0.5, 
                                             self.infeclbl_text.format(str(np.round(infec_val*100,2))),
                                             transform=self.sim_ax.transAxes, color='r', 
                                             fontweight='heavy', fontsize=10)

        succep_val = data[:,0][-1]
        self.succeclbl_text ='Succeptible \n{0}%' 
        self.succeclbltext = self.sim_ax.text(0.955, infec_val+succep_val*0.5, 
                                               self.succeclbl_text.format(str(np.round(succep_val*100,2))), 
                                               transform=self.sim_ax.transAxes, color='w',
                                               fontweight='heavy', fontsize=10)

        recov_val = data[:, 2][-1]
        self.recovlbl_text = 'Removed \n{0}%'
        self.recovlbltext = self.sim_ax.text(0.955,1 - 0.5*recov_val - 0.04, 
                                            self.recovlbl_text.format(str(np.round(recov_val*100,2))), 
                                            transform=self.sim_ax.transAxes, color='lightgray', 
                                            fontweight='heavy', fontsize=10)
        
        return self.sim_fig,
    
    def update_canvas(self, i):
        
        dates, data = next(self.modelDataGenerator)

        self.sim_ax.set_xlim(dates[0], dates[-1])
        succep_pct_lst = data[:,0][-1]
        infec_pct_lst = data[:,1][-1]
        remov_pct_lst = data[:,2][-1]
        
        self.succeptext.set_text(str(int(np.round(succep_pct_lst*self.scaleFactor))))
        self.succeptext.set_text(str(int(np.round(succep_pct_lst*self.scaleFactor))))
        
        self.infected_text = '{0}%'.format(np.round(infec_pct_lst*100, 1))
        self.infectedtext.set_text(self.infected_text)
        self.testingtext.set_text('--.-')
        self.asymptotext.set_text('--.-')
        
        self.removed_text = '{0}%'.format(np.round(remov_pct_lst*100, 1))
        self.removedtext.set_text(self.removed_text)
        self.recovtext.set_text('--.-')
        self.deathtext.set_text('--.-')
        
        _infectext = self.infeclbl_text.format(str(np.round(infec_pct_lst*100,2)))
        self.infeclbltext.set_text(_infectext)
        self.infeclbltext.set_position((0.96, infec_pct_lst*0.5))
        
        _succectext = self.succeclbl_text.format(str(np.round(succep_pct_lst*100,2)))
        self.succeclbltext.set_text(_succectext)
        self.succeclbltext.set_position((0.955, infec_pct_lst+succep_pct_lst*0.5))
        
        _removtext = self.recovlbl_text.format(str(np.round(remov_pct_lst*100,2)))
        self.recovlbltext.set_text(_removtext)
        self.recovlbltext.set_position((0.955,1 - 0.5*remov_pct_lst - 0.04))

        self.infectedfill.remove()
        self.infectedfill = self.sim_ax.fill_between(dates, data[:,1], interpolate=True, alpha=1.0,
                                                     facecolor='#f5653d', edgecolor='k')
        self.removedfill.remove()
        self.removedfill = self.sim_ax.fill_between(dates, 1-data[:,2], y2=1, interpolate=True, alpha=0.5,
                                                    facecolor='#999999', edgecolor='k')
        
        return self.sim_fig,
    