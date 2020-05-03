
from ..configs.panmodel_configs import *
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow
import os, random, warnings
warnings.filterwarnings('ignore')
import seaborn as sns
from scipy.integrate import odeint


class ModelBase():
    
    def __init__(self, self._preventive_effects={}, _testing_effects={}, _recovery_effects={},
                 _start_date='2020-01-01', _projections_till = "6 Months", _projection_granularity = 'Days',
                 _modelname = 'S_I_R'):
        print('Initialising the SIR Model class..')

        # Parameter Checks
        assert datetime.strptime(_start_date, '%Y-%m-%d'), StartDateErr
        assert _projections_till.split(' ')[-1] in ['Month', 'Months', 'month', 'months',
                                                    'Day', 'Days', 'day', 'days',
                                                    'Year', 'Years', 'year', 'years'], ProjectionErr
        assert type(int(_projections_till.split(' ')[0])) == int, ProjectionErr
        assert _projection_granularity in ['Months', 'Days','Years'], ProjectionGranErr1
        
        self.start_date = datetime.strptime(_start_date, "%Y-%m-%d")
        
        if _projections_till.split(' ')[-1] in ['Day', 'Days', 'day', 'days']:
            self.end_date = self.start_date+relativedelta(days=int(_projections_till.split(' ')[0]))
        
        elif _projections_till.split(' ')[-1] in ['Month', 'Months', 'month', 'months']:
            self.end_date = self.start_date+relativedelta(months=int(_projections_till.split(' ')[0]))
        
        elif _projections_till.split(' ')[-1] in ['Year', 'Years', 'year', 'years']:
            self.end_date = self.start_date+relativedelta(years=int(_projections_till.split(' ')[0]))
        
        
        _days = (self.end_date - self.start_date).days
        _available = []
        if _days > 0:
            _available.append('Days')
        if _days > 30:
            _available.append('Months')
        if _days > 365:
            _available.append('Years')
        
        assert _projection_granularity in _available, ProjectionGranErr2.format(_start_date, _projections_till,
                                                                                _projection_granularity, _available)
        
        # Calculate Time Dependent Values
        self.timebasedRates = []
        for _mode in ['succecptible_pct', 'testing_pct', 'testing_pct.recovery']:
            vals = self.calc_tdependent_rates(mode = _mode)
            self.timebasedRates.append(vals)
            
        self.timebasedRates = np.c_[self.timebasedRates].T
        self.modelname = _modelname
           
    def calc_tdependent_rates(self, mode= 'succecptible_pct'):
        '''
        parameters - 
            effect_dict : dict
                Dictionary Containing the Effect Dates and the value associated to it
            mode : str
                Takes values only from ['succecptible_pct', 'testing_pct', 'testing_pct.recovery']
        '''
        date_counter = self.start_date
        default_value = panmodel_configs[f'params.{mode}.val']
        delta_time = panmodel_configs[f'params.{mode}.etd']
        effect_dict = panmodel_configs[f'params.{mode}.es']
        value_list = [default_value]
        effect_dates = [datetime.strptime(k, "%Y-%m-%d") for k in effect_dict.keys()]
        
        while date_counter < self.end_date:
            if datetime.strftime(date_counter, "%Y-%m-%d") in effect_dict:
                _date = datetime.strftime(date_counter, "%Y-%m-%d")
                _rate = effect_dict[_date]
                _decay_stepper = np.log(1+_rate)/(delta_time*(_rate/abs(_rate)))
                _base_value = value_list[-1]
                
                _jump_dates_delta = np.array([(k-date_counter).days for k in effect_dates])
                _jump_dates_delta = _jump_dates_delta[_jump_dates_delta>0]
                
                if _jump_dates_delta.size == 0:
                    _jump_delta = delta_time
                else:
                    _jump_dates_delta = min(_jump_dates_delta[_jump_dates_delta>0])
                    _jump_delta = min(_jump_dates_delta, delta_time)
                
                value_list += [_base_value*(np.exp((_rate/abs(_rate))*i*_decay_stepper)) for i in range(delta_time+1)][1:_jump_delta+1]
                date_counter += relativedelta(days=int(_jump_delta))
            else:
                value_list.append(value_list[-1])
                date_counter += relativedelta(days=1)
                
        return np.array(value_list)
        
    def get_tdependent_rates(self):
        
        for i in range(self.timebasedRates.shape[0]):
            yield self.timebasedRates[i]
        
    def setup_report_sir(self):
        modelname = "\_".join(self.modelname.split('_'))

        plt.rcParams['figure.dpi'] = 100
        plt.rcParams["axes.edgecolor"] = "black"
        plt.rcParams["axes.linewidth"] = 1

        fig, axes = plt.subplots(1,2, figsize=(25,7))
        _titles = [r'Preventive; $\alpha$', r'Recovery; $\delta$']
        temp = self.timebasedRates
        _days = (self.end_date - self.start_date).days
        _dates = [self.start_date+relativedelta(days=k) for k in range(_days+1)]

        fig.patches.extend([plt.Rectangle((0.1,-0.45),0.82,1.4,
                            fill=False, alpha=1, facecolor='none', 
                            zorder=-1, edgecolor='k', lw=5,
                            transform=fig.transFigure, figure=fig)])
        for idx, eachAx in enumerate(axes.ravel()):

            eachAx.set_facecolor('k')
            eachAx.grid(color='w', linestyle='-.', linewidth=1)
            eachAx.set_ylim(0, temp[:,idx].max()*1.3)
            eachAx.fill_between(x= _dates, y1=temp[:,idx], y2 = 0, 
                                edgecolor='w', linewidth=2)
            eachAx.set_title(_titles[idx], fontsize=20)
            
            if idx == 0:
                t1 = (np.diff(temp[:,0])!=0).astype(int)
                t1 = np.insert(t1, 0, 0)
                nonzero_idx = t1.nonzero()[0]
                t2 = np.insert(np.diff(nonzero_idx), 0 , 0) != 1
                usable_idx = nonzero_idx[t2]
                self._preventive_eff = panmodel_configs['params.sir.sp.es']
                self._total_pop = panmodel_configs['params.sir.tpop.val']
                for _i, _index in enumerate(usable_idx):
                    _x = list(self._preventive_eff.keys())[_i]
                    _y = temp[:,idx][_index]
                    self._total_pop = np.round(_y*self._total_pop, 3)
                    eachAx.text(_x, _y, self._total_pop, color='lightyellow', fontsize=18)

        # Disease Name
        self._pandemic_name = panmodel_configs['general.pandemic.name']
        props = dict(boxstyle='round', facecolor='none', alpha=0.5, edgecolor='k')
        fig.text(0.55, -0.25, f'{self._pandemic_name}', fontsize=(50/len(self._pandemic_name))*7, family = 'monospace',
                 verticalalignment='center', horizontalalignment='center', bbox=props)
        fig.text(0.55, -0.35, 'M O D E L   S E T U P', fontsize=20, family = 'monospace',
                 verticalalignment='center', horizontalalignment='center')

        # Model Architecture
        props = dict(boxstyle='round', facecolor='red', alpha=0.5, edgecolor='k')
        fig.text(0.175, -0.09, f'Model\n Architecture \n',  fontsize=20,
                 verticalalignment='center', horizontalalignment='center', bbox=props)
        fig.text(0.175, -0.13, f'$(with\ default\ values)$',  fontsize=13,
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
        
        # Total Population
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5, edgecolor='k')
        self._total_pop = panmodel_configs['params.sir.tpop.val']
        self._total_pop = f'{self._total_pop:,}'
        _fsize = (10/len(self._total_pop))*19 if (10/len(self._total_pop))*19 <= 14.5 else 14.5

        fig.text(0.258, -0.11, f'\n\n val = {self._total_pop}', fontsize=_fsize,
                 verticalalignment='baseline', horizontalalignment='left', bbox=props)
        fig.text(0.3, -0.06, 'P', fontsize=30,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.3, -0.15, 'Total Population', fontsize=12,
                 verticalalignment='center', horizontalalignment='center')

        ## Succeptible
        if 'S' not in modelname:
            ls = '-.'
            alpha_succep = 0.2
        else:
            ls = '-'
            alpha_succep = 1

        fig.patches.extend([plt.arrow(0.35, -0.07, 0.09, 0, clip_on=False,
                                      length_includes_head=True, color='k', 
                                      alpha=alpha_succep, linestyle=ls, zorder=3333,
                                      transform=fig.transFigure, figure=fig,
                                      head_width=0.02, head_length=0.006)])
        self._alpha0 = panmodel_configs['params.sir.sp.val']
        fig.text(0.402, -0.055, r'$\alpha(t_{0}) = $'+f'{self._alpha0}', fontsize=12,alpha=alpha_succep,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.4, -0.105, 'Succeptible\n Percentage', fontsize=12, alpha=alpha_succep,
                 verticalalignment='center', horizontalalignment='center')
        self._succ_pop = panmodel_configs['params.sir.tpop.val']*panmodel_configs['params.sir.sp.val']
        self._succ_pop = f'{self._succ_pop:,}'
        _fsize = (10/len(self._succ_pop))*19 if (10/len(self._succ_pop))*19 <= 14.5 else 14.5
        fig.text(0.445, -0.11, f'\n\n val = {self._succ_pop}', fontsize=_fsize, alpha=alpha_succep,
                 verticalalignment='baseline', horizontalalignment='left', bbox=props)
        fig.text(0.485, -0.06, r'$S(t)$', fontsize=30, alpha=alpha_succep,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.485, -0.15, 'Succeptible', fontsize=12, alpha=alpha_succep,
                 verticalalignment='center', horizontalalignment='center')


        ## Infections
        if 'I' not in modelname:
            ls = '-.'
            alpha_infec = 0.2
        else:
            ls = '-'
            alpha_infec = 1
        fig.patches.extend([plt.arrow(0.53, -0.07, 0.12, 0, clip_on=False,
                                      length_includes_head=True, color='k', 
                                      alpha=alpha_infec, linestyle=ls, zorder=3333,
                                      transform=fig.transFigure, figure=fig,
                                      head_width=0.02, head_length=0.006)])
        self._beta = panmodel_configs['params.sir.tr.cr.val']
        self._tproba = panmodel_configs['params.sir.tr.pr.val']
        self._infec_pop = panmodel_configs['params.sir.in.val']
        self._infec_pop = f'{self._infec_pop:,}'
        _fsize = 14.5
        fig.text(0.576, -0.055, r'$\beta = $'+f'{self._beta} , '\
                 +r'$\ p = $'+f'{self._tproba}', fontsize=12,alpha=alpha_infec,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.58, -0.105, 'Interactions; \n Transmission Probability', fontsize=12, alpha=alpha_infec,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.655, -0.11, f'\n\n val = {self._infec_pop}', fontsize=_fsize, alpha=alpha_infec,
                 verticalalignment='baseline', horizontalalignment='left', bbox=props)
        fig.text(0.675, -0.06, r'$I(t)$', fontsize=30, alpha=alpha_infec,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.675, -0.15, 'Infections', fontsize=12, alpha=alpha_infec,
                 verticalalignment='center', horizontalalignment='center')

        
        ## Recovered
        if any(k in modelname for k in ['r', 'R']):
            ls = '-'
            alpha_recovered = 1
        else:
            ls = '-.'
            alpha_recovered = 0.2

        fig.patches.extend([plt.arrow(0.7, -0.07, 0.14, 0, clip_on=False,
                                      length_includes_head=True, color='k', 
                                      alpha=alpha_recovered, linestyle=ls, zorder=3333,
                                      transform=fig.transFigure, figure=fig,
                                      head_width=0.02, head_length=0.006)])

        self._test_recov_pct = panmodel_configs['params.testing_pct.recovery.val']
        self._asymp_recov_pct = panmodel_configs['params.asymptomatic_pct.recovery.val']
        _fsize = 14.5
        fig.text(0.75, -0.055, r'$\delta_{1}(t_{0}) = $'+f'{self._test_recov_pct}', fontsize=12,alpha=alpha_recovered,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.75, -0.09, 'Recoverd Percentage', fontsize=12, alpha=alpha_recovered,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.85, -0.11, f'\n\n val = {0}', fontsize=_fsize, alpha=alpha_recovered,
                 verticalalignment='baseline', horizontalalignment='left', bbox=props)
        fig.text(0.867, -0.06, r'$R(t)$', fontsize=30, alpha=alpha_recovered,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.867, -0.15, 'Recovered', fontsize=12, alpha=alpha_recovered,
                 verticalalignment='center', horizontalalignment='center')


        plt.close()
        
        return fig
    
    def setup_report_sitarrd(self):
        modelname = "\_".join(self.modelname.split('_'))

        plt.rcParams['figure.dpi'] = 100
        plt.rcParams["axes.edgecolor"] = "black"
        plt.rcParams["axes.linewidth"] = 1

        fig, axes = plt.subplots(1,3, figsize=(25,7))
        _titles = [r'Preventive; $\alpha$', r'Testing; $\gamma$', r'Recovery; $\delta$']
        temp = self.timebasedRates
        _days = (self.end_date - self.start_date).days
        _dates = [self.start_date+relativedelta(days=k) for k in range(_days+1)]

        fig.patches.extend([plt.Rectangle((0.1,-0.45),0.82,1.4,
                            fill=False, alpha=1, facecolor='none', 
                            zorder=-1, edgecolor='k', lw=5,
                            transform=fig.transFigure, figure=fig)])
        for idx, eachAx in enumerate(axes.ravel()[:3]):

            eachAx.set_facecolor('k')
            eachAx.grid(color='w', linestyle='-.', linewidth=1)
            eachAx.set_ylim(0, temp[:,idx].max()*1.3)
            eachAx.fill_between(x= _dates, y1=temp[:,idx], y2 = 0, 
                                edgecolor='w', linewidth=2)
            eachAx.set_title(_titles[idx], fontsize=20)
            
            if idx == 0:
                t1 = (np.diff(temp[:,0])!=0).astype(int)
                t1 = np.insert(t1, 0, 0)
                nonzero_idx = t1.nonzero()[0]
                t2 = np.insert(np.diff(nonzero_idx), 0 , 0) != 1
                usable_idx = nonzero_idx[t2]
                self._preventive_eff = panmodel_configs['params.sir.sp.es']
                self._total_pop = panmodel_configs['params.sir.tpop.val']
                for _i, _index in enumerate(usable_idx):
                    _x = list(self._preventive_eff.keys())[_i]
                    _y = temp[:,idx][_index]
                    self._total_pop = np.round(_y*self._total_pop, 3)
                    eachAx.text(_x, _y, self._total_pop, color='lightyellow', fontsize=18)

        # Disease Name
        self._pandemic_name = panmodel_configs['general.pandemic.name']
        props = dict(boxstyle='round', facecolor='none', alpha=0.5, edgecolor='k')
        fig.text(0.4, -0.25, f'{self._pandemic_name}', fontsize=(50/len(self._pandemic_name))*7, family = 'monospace',
                 verticalalignment='center', horizontalalignment='center', bbox=props)
        fig.text(0.4, -0.35, 'M O D E L   S E T U P', fontsize=20, family = 'monospace',
                 verticalalignment='center', horizontalalignment='center')

        # Model Architecture
        props = dict(boxstyle='round', facecolor='red', alpha=0.5, edgecolor='k')
        fig.text(0.175, -0.09, f'Model\n Architecture \n',  fontsize=20,
                 verticalalignment='center', horizontalalignment='center', bbox=props)
        fig.text(0.175, -0.13, f'$(with\ default\ values)$',  fontsize=13,
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
        
        # Total Population
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5, edgecolor='k')
        self._total_pop = panmodel_configs['params.sir.tpop.val']
        self._total_pop = f'{self._total_pop:,}'
        _fsize = (10/len(self._total_pop))*19 if (10/len(self._total_pop))*19 <= 14.5 else 14.5

        fig.text(0.258, -0.11, f'\n\n val = {self._total_pop}', fontsize=_fsize,
                 verticalalignment='baseline', horizontalalignment='left', bbox=props)
        fig.text(0.3, -0.06, 'P', fontsize=30,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.3, -0.15, 'Total Population', fontsize=12,
                 verticalalignment='center', horizontalalignment='center')

        ## Succeptible
        if 'S' not in modelname:
            ls = '-.'
            alpha_succep = 0.2
        else:
            ls = '-'
            alpha_succep = 1

        fig.patches.extend([plt.arrow(0.35, -0.07, 0.05, 0, clip_on=False,
                                      length_includes_head=True, color='k', 
                                      alpha=alpha_succep, linestyle=ls, zorder=3333,
                                      transform=fig.transFigure, figure=fig,
                                      head_width=0.02, head_length=0.006)])
        self._alpha0 = panmodel_configs['params.sir.sp.val']
        fig.text(0.372, -0.055, r'$\alpha(t_{0}) = $'+f'{self._alpha0}', fontsize=12,alpha=alpha_succep,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.37, -0.105, 'Succeptible\n Percentage', fontsize=12, alpha=alpha_succep,
                 verticalalignment='center', horizontalalignment='center')
        self._succ_pop = panmodel_configs['params.sir.tpop.val']*panmodel_configs['params.sir.sp.val']
        self._succ_pop = f'{self._succ_pop:,}'
        _fsize = (10/len(self._succ_pop))*19 if (10/len(self._succ_pop))*19 <= 14.5 else 14.5
        fig.text(0.405, -0.11, f'\n\n val = {self._succ_pop}', fontsize=_fsize, alpha=alpha_succep,
                 verticalalignment='baseline', horizontalalignment='left', bbox=props)
        fig.text(0.445, -0.06, r'$S(t)$', fontsize=30, alpha=alpha_succep,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.445, -0.15, 'Succeptible', fontsize=12, alpha=alpha_succep,
                 verticalalignment='center', horizontalalignment='center')


        ## Infections
        if 'I' not in modelname:
            ls = '-.'
            alpha_infec = 0.2
        else:
            ls = '-'
            alpha_infec = 1
        fig.patches.extend([plt.arrow(0.5, -0.07, 0.09, 0, clip_on=False,
                                      length_includes_head=True, color='k', 
                                      alpha=alpha_infec, linestyle=ls, zorder=3333,
                                      transform=fig.transFigure, figure=fig,
                                      head_width=0.02, head_length=0.006)])
        self._beta = panmodel_configs['params.sir.tr.cr.val']
        self._tproba = panmodel_configs['params.sir.tr.pr.val']
        self._infec_pop = panmodel_configs['params.sir.in.val']
        self._infec_pop = f'{self._infec_pop:,}'
        _fsize = 14.5
        fig.text(0.536, -0.055, r'$\beta = $'+f'{self._beta} , '\
                 +r'$\ p = $'+f'{self._tproba}', fontsize=12,alpha=alpha_infec,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.54, -0.105, 'Interactions; \n Transmission Probability', fontsize=12, alpha=alpha_infec,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.595, -0.11, f'\n\n val = {self._infec_pop}', fontsize=_fsize, alpha=alpha_infec,
                 verticalalignment='baseline', horizontalalignment='left', bbox=props)
        fig.text(0.615, -0.06, r'$I(t)$', fontsize=30, alpha=alpha_infec,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.615, -0.15, 'Infections', fontsize=12, alpha=alpha_infec,
                 verticalalignment='center', horizontalalignment='center')

        ## Tested
        if any(k in modelname for k in ['t', 'I']):
            ls = '-'
            alpha_test = 1
        else:
            ls = '-'
            alpha_test = 0.2
        fig.patches.extend([plt.arrow(0.64, -0.07, 0.05, 0, clip_on=False,
                                      length_includes_head=True, color='k', 
                                      alpha=alpha_test, linestyle=ls, zorder=3333,
                                      transform=fig.transFigure, figure=fig,
                                      head_width=0.02, head_length=0.006)])
        self._test_pct = panmodel_configs['params.testing_pct.val']
        _fsize = 14.5
        fig.text(0.662, -0.055, r'$\gamma(t_{0}) = $'+f'{self._test_pct}', fontsize=12,alpha=alpha_test,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.665, -0.105, 'Testing \nPercentage', fontsize=12, alpha=alpha_test,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.695, -0.11, f'\n\n val = {self._infec_pop}', fontsize=_fsize, alpha=alpha_test,
                 verticalalignment='baseline', horizontalalignment='left', bbox=props)
        fig.text(0.715, -0.06, r'$T(t)$', fontsize=30, alpha=alpha_test,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.715, -0.15, 'Tested', fontsize=12, alpha=alpha_test,
                 verticalalignment='center', horizontalalignment='center')

        ## Asymptomatic
        if any(k in modelname for k in ['a', 'I']):
            ls = '-'
            alpha_asymp = 1
        else:
            ls = '-'
            alpha_asymp = 0.2
        fig.patches.extend([plt.arrow(0.641, -0.07, 0., -0.28, clip_on=False,
                                      length_includes_head=True, color='k', lw=0.3,
                                      alpha=alpha_asymp, linestyle=ls, zorder=3333,
                                      transform=fig.transFigure, figure=fig,
                                      head_width=0. , head_length=0.)])
        fig.patches.extend([plt.arrow(0.641, -0.348, 0.05, 0, clip_on=False,
                                      length_includes_head=True, color='k',
                                      alpha=alpha_asymp, linestyle=ls, zorder=3333,
                                      transform=fig.transFigure, figure=fig,
                                      head_width=0.02, head_length=0.006)])

        self._asymp_pct = panmodel_configs['params.asymptomatic_pct.val']
        _fsize = 14.5
        fig.text(0.666, -0.325, r'$1-\gamma(t_{0}) = $'+f'{1-self._test_pct}', fontsize=12,alpha=alpha_asymp,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.665, -0.375, 'Asymptomatic \nPercentage', fontsize=12, alpha=alpha_asymp,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.695, -0.375, f'\n\n val = {0}', fontsize=_fsize, alpha=alpha_asymp,
                 verticalalignment='baseline', horizontalalignment='left', bbox=props)
        fig.text(0.712, -0.33, r'$A(t)$', fontsize=30, alpha=alpha_asymp,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.712, -0.25, 'Asymptomatic\n/Untested', fontsize=12, alpha=alpha_asymp,
                 verticalalignment='center', horizontalalignment='center')



        ## Recovered
        if any(k in modelname for k in ['r', 'R']):
            ls = '-'
            alpha_recovered = 1
        else:
            ls = '-.'
            alpha_recovered = 0.2

        fig.patches.extend([plt.arrow(0.74, -0.07, 0.1, 0, clip_on=False,
                                      length_includes_head=True, color='k', 
                                      alpha=alpha_recovered, linestyle=ls, zorder=3333,
                                      transform=fig.transFigure, figure=fig,
                                      head_width=0.02, head_length=0.006)])
        fig.patches.extend([plt.arrow(0.75, -0.35, 0.02, 0.22, clip_on=False,
                                      length_includes_head=True, color='k', 
                                      alpha=alpha_recovered, linestyle=ls, zorder=3333,
                                      transform=fig.transFigure, figure=fig,
                                      head_width=0.0, head_length=0.00)])
        fig.patches.extend([plt.arrow(0.77, -0.127, 0.07, 0, clip_on=False,
                                      length_includes_head=True, color='k', 
                                      alpha=alpha_recovered, linestyle=ls, zorder=3333,
                                      transform=fig.transFigure, figure=fig,
                                      head_width=0.02, head_length=0.006)])

        self._test_recov_pct = panmodel_configs['params.testing_pct.recovery.val']
        self._asymp_recov_pct = panmodel_configs['params.asymptomatic_pct.recovery.val']
        _fsize = 14.5
        fig.text(0.79, -0.055, r'$\delta_{1}(t_{0}) = $'+f'{self._test_recov_pct}', fontsize=12,alpha=alpha_recovered,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.8, -0.145, r'$\delta_{2}(t_{0}) = $'+f'{self._asymp_recov_pct}', fontsize=12,alpha=alpha_recovered,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.79, -0.09, 'Recoverd Percentage', fontsize=12, alpha=alpha_recovered,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.85, -0.11, f'\n\n val = {0}', fontsize=_fsize, alpha=alpha_recovered,
                 verticalalignment='baseline', horizontalalignment='left', bbox=props)
        fig.text(0.867, -0.06, r'$R(t)$', fontsize=30, alpha=alpha_recovered,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.867, -0.15, 'Recovered', fontsize=12, alpha=alpha_recovered,
                 verticalalignment='center', horizontalalignment='center')


        ## Death
        if any(k in modelname for k in ['d', 'R']):
            ls = '-'
            alpha_death = 1
        else:
            ls = '-.'
            alpha_death = 0.2

        fig.patches.extend([plt.arrow(0.74, -0.35, 0.1, 0, clip_on=False,
                                      length_includes_head=True, color='k', 
                                      alpha=alpha_death, linestyle=ls, zorder=3333,
                                      transform=fig.transFigure, figure=fig,
                                      head_width=0.02, head_length=0.006)])
        fig.patches.extend([plt.arrow(0.75, -0.07, 0.02, -0.245, clip_on=False,
                                      length_includes_head=True, color='k', 
                                      alpha=alpha_death, linestyle=ls, zorder=3333,
                                      transform=fig.transFigure, figure=fig,
                                      head_width=0.0, head_length=0.00)])
        fig.patches.extend([plt.arrow(0.77, -0.315, 0.07, 0, clip_on=False,
                                      length_includes_head=True, color='k', 
                                      alpha=alpha_death, linestyle=ls, zorder=3333,
                                      transform=fig.transFigure, figure=fig,
                                      head_width=0.02, head_length=0.006)])

        self._test_death_pct = panmodel_configs['params.testing_pct.death.val']
        self._asym_death_pct = panmodel_configs['params.asymptomatic_pct.death.val']
        _fsize = 14.5
        fig.text(0.8, -0.30, r'$\psi_{1}(t_{0}) = $'+f'{self._test_death_pct}', fontsize=12,alpha=alpha_death,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.8, -0.335, r'$\psi_{2}(t_{0}) = $'+f'{self._asym_death_pct}', fontsize=12,alpha=alpha_death,
                 verticalalignment='center', horizontalalignment='center')

        fig.text(0.79, -0.37, 'Death Percentage', fontsize=12, alpha=alpha_death,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.85, -0.357, f'\n\n val = {0}', fontsize=_fsize, alpha=alpha_death,
                 verticalalignment='baseline', horizontalalignment='left', bbox=props)
        fig.text(0.867, -0.31, r'$D(t)$', fontsize=30, alpha=alpha_death,
                 verticalalignment='center', horizontalalignment='center')
        fig.text(0.867, -0.385, 'Deaths', fontsize=12, alpha=alpha_death,
                 verticalalignment='center', horizontalalignment='center')

        ## Removed
        fig.patches.extend([plt.Rectangle((0.845,-0.395), 0.055,.389,
                            fill=True, alpha=.1, facecolor='r', 
                            zorder=-1, edgecolor='k', lw=3,
                            transform=fig.transFigure, figure=fig)])
        fig.text(0.895,-0.22, 'R\nE\nM\nO\nV\nE\nD\n', fontsize=17, alpha=alpha_death,
                 verticalalignment='center', horizontalalignment='center')

        plt.close()
        
        return fig
    
    def simulate_model(self):

        # Solve for the ODE based on the model
        # Get the results
        # Animate the results based on the simulation

        pass
        
        