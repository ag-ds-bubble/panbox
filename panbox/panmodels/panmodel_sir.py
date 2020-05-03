
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow
import os, random, warnings
warnings.filterwarnings('ignore')
import seaborn as sns
from scipy.integrate import odeint
from .panmodel_base import ModelBase
from .._animutils.simulator_model import ModelSimulator

class SIRModel(ModelBase):
    
    def __init__(self, startdate='2020-01-01', till = "6 Months", granularity = 'Days'):
        """
         startdate: 
         till: 
         granularity :
         modelname : 
        
        SIRModel - Pandemic Simulator Model(Succeptible, Infected and Removed).
        This model is defined by the folllowing differenntial equations :-
        
        Equations
        ----------
        dS = -beta*S*I/N
        dI = beta*S*I/N - gamma*I
        dR = gamma*I

        This Model provides the interface for the following :-
            1) Pandemic Growth Simulator
            2) Estimating the Growth of a particular Country

        Parameters
        ----------
        startdate : str, optional,  default '2020-01-01'
            Start date of the model for Simulator as well as Estimator.
            Must be in the format : "%Y-%m-%d"
        till : str, optional, default '6 Months'
            Months till when the Predictions/Simulation should be made.
            Must be in the format : "{Count} Any Of[Months, Month, Years, Year, Days, Day]"
            Ex "6 Months" or "5 Years"
        granularity : str, optional, default 'Days'
            Granularity  of the predictions to be made.
            Can take values only from ['Years', 'Months', 'Days']
        
        Attributes
        ----------
        """
        super().__init__(startdate=startdate, till = till, granularity = granularity, modelname = 'S_I_R')
        
    def setup_report(self):
        
        # Retrieve Updated Configurations
        super()._retrieve_parameters()

        modelname = "\_".join(self.modelName.split('_'))
        plt.rcParams['figure.dpi'] = 100
        plt.rcParams["axes.edgecolor"] = "black"
        plt.rcParams["axes.linewidth"] = 1

        fig, axes = plt.subplots(1,3, figsize=(25,7))
        _titles = [r'Contact Rate; $\beta$', r'Transmission Probability $p$',  r'Recovery; $\gamma$']
        
        fig.patches.extend([plt.Rectangle((0.1,-0.45),0.82,1.4,
                            fill=False, alpha=1, facecolor='none', 
                            zorder=-1, edgecolor='k', lw=5,
                            transform=fig.transFigure, figure=fig)])

        for idx, eachAx in enumerate(axes.ravel()):
            eachAx.set_facecolor('k')
            eachAx.grid(color='w', linestyle='-.', linewidth=1)
            eachAx.set_ylim(0, self._timeBasedRates[:,idx].max()*1.3)
            eachAx.fill_between(x= self._datesInBetween, y1=self._timeBasedRates[:,idx], y2 = 0, 
                                edgecolor='w', linewidth=2)
            eachAx.set_title(_titles[idx], fontsize=20)


        # Disease Name
        props = dict(boxstyle='round', facecolor='none', alpha=0.5, edgecolor='k')
        fig.text(0.55, -0.25, f'{self._pandemic_name}', fontsize=(50/len(self._pandemic_name))*7, family = 'monospace',
                 verticalalignment='center', horizontalalignment='center', bbox=props)
        fig.text(0.55, -0.35, 'M O D E L   S E T U P', fontsize=20, family = 'monospace',
                 verticalalignment='center', horizontalalignment='center')

        # Model Architecture
        props = dict(boxstyle='round', facecolor='red', alpha=0.5, edgecolor='k')
        fig.text(0.175, -0.09, f'Model\n Architecture \n',  fontsize=20,
                 verticalalignment='center', horizontalalignment='center', bbox=props)
        fig.text(0.175, -0.13, r'$(with\ default\ values)$',  fontsize=13,
                 verticalalignment='center', horizontalalignment='center')

        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5, edgecolor='k')
        fig.text(0.175, -0.3, f'Model Name\n\n', fontsize=20,
                 verticalalignment='center', horizontalalignment='center', bbox=props)

        fig.text(0.175, -0.33, f'${modelname}$', fontsize=(50/len(modelname))*5,
                 verticalalignment='center', horizontalalignment='center')

        ## Add Model
        fig.patches.extend([plt.Rectangle((0.25,-0.4), 0.665, 0.4, fill=False, 
                                          alpha=1, facecolor='none', edgecolor='k', lw=1,
                                          transform=fig.transFigure, figure=fig, zorder=-1)])
        
        ## Succeptible
        if 'S' not in modelname:
            ls = '-.'
            alpha_succep = 0.2
        else:
            ls = '-'
            alpha_succep = 1
        
        self._total_pop = f'{self._total_pop:,}'
        _fsize = (10/len(self._total_pop))*19 if (10/len(self._total_pop))*19 <= 14.5 else 14.5
        fig.text(0.26, -0.11, f'\n\n val = {self._total_pop}', fontsize=_fsize, alpha=alpha_succep,
                 verticalalignment='baseline', horizontalalignment='left', bbox=props)
        fig.text(0.305, -0.06, r'$S(t)$', fontsize=30, alpha=alpha_succep,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.305, -0.15, 'Succeptible', fontsize=12, alpha=alpha_succep,
                 verticalalignment='center', horizontalalignment='center')


        ## Infections
        if 'I' not in modelname:
            ls = '-.'
            alpha_infec = 0.2
        else:
            ls = '-'
            alpha_infec = 1
        fig.patches.extend([plt.arrow(0.35, -0.07, 0.19, 0, clip_on=False,
                                      length_includes_head=True, color='k', 
                                      alpha=alpha_infec, linestyle=ls, zorder=3333,
                                      transform=fig.transFigure, figure=fig,
                                      head_width=0.02, head_length=0.006)])
        self._infec_pop = f'{self._infec_pop:,}'
        _fsize = 14.5
        fig.text(0.43, -0.055, r'$\beta(t_{0}) = $'+f'{self._beta} , '\
                 +r'$\ p = $'+f'{self._tproba}', fontsize=12,alpha=alpha_infec,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.422, -0.105, 'Interactions; \n Transmission Probability', fontsize=12, alpha=alpha_infec,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.555, -0.11, f'\n\n val = {self._infec_pop}', fontsize=_fsize, alpha=alpha_infec,
                 verticalalignment='baseline', horizontalalignment='left', bbox=props)
        fig.text(0.575, -0.06, r'$I(t)$', fontsize=30, alpha=alpha_infec,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.575, -0.15, 'Infections', fontsize=12, alpha=alpha_infec,
                 verticalalignment='center', horizontalalignment='center')

        
        ## Recovered
        if any(k in modelname for k in ['r', 'R']):
            ls = '-'
            alpha_recovered = 1
        else:
            ls = '-.'
            alpha_recovered = 0.2

        fig.patches.extend([plt.arrow(0.6, -0.07, 0.24, 0, clip_on=False,
                                      length_includes_head=True, color='k', 
                                      alpha=alpha_recovered, linestyle=ls, zorder=3333,
                                      transform=fig.transFigure, figure=fig,
                                      head_width=0.02, head_length=0.006)])
        _fsize = 14.5
        fig.text(0.7, -0.055, r'$\gamma(t_{0}) = $'+f'{self._remov_recov_pct}', fontsize=12,alpha=alpha_recovered,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.7, -0.09, 'Recovery Rate', fontsize=12, alpha=alpha_recovered,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.85, -0.11, f'\n\n val = {0}', fontsize=_fsize, alpha=alpha_recovered,
                 verticalalignment='baseline', horizontalalignment='left', bbox=props)
        fig.text(0.867, -0.06, r'$R(t)$', fontsize=30, alpha=alpha_recovered,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.867, -0.15, 'Recovered', fontsize=12, alpha=alpha_recovered,
                 verticalalignment='center', horizontalalignment='center')


        plt.close()
        
        return fig
       
    def solve_ode(self, y0, t, beta, gamma):

        succ, infec, _ = y0
        k = int(t)
        if k >= len(beta):
            k = len(beta)-1
        dS = -beta[k]*succ*infec
        dI = beta[k]*succ*infec - gamma[k]*infec
        dR = gamma[k]*infec
        return dS, dI, dR

    def simulate_model(self):
        
        # Retrieve Updated Configurations
        super()._retrieve_parameters()

        # Initialise Constants
        _contact_rate = self._timeBasedRates[:, 0]
        _trans_proba = self._timeBasedRates[:, 1]
        _beta = _contact_rate*_trans_proba

        _gamma = self._timeBasedRates[:, 2]
        _simdays = np.arange(self._noOfDays)

        beta, gamma = (_beta/self._total_pop), _gamma

        # Scale Beta for Number of Days in the Simulation
        succeptible_t0   = self._total_pop - self._infec_pop - self._remov_pop
        Y0 = [succeptible_t0, self._infec_pop, self._remov_pop]
        odeResult = odeint(self.solve_ode, Y0, _simdays, args = (beta, gamma))
        _scalefactor = odeResult.sum(axis=1)[0]
        odeResult = np.divide(odeResult, odeResult.sum(axis=1).reshape(-1,1))

        # Initialise the Animator Model
        _dataPacket = (self._datesInBetween, odeResult, _scalefactor)
        self.modelSimulator = ModelSimulator(datapacket = _dataPacket, modelname='S_I_R')





