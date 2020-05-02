
from .._configs.panmodel_configs import *
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
    
    def __init__(self, startdate, till, granularity, modelname):
        self.configParams = panmodel_configs
        self.modelName = modelname
        self._granularity = granularity
        self._till = till
        self._startDate = startdate
        self._noOfDays = 0
        self._timeBasedRates = []
        self._datesInBetween = []

        # Parameter Checks
        assert datetime.strptime(self._startDate, '%Y-%m-%d'), StartDateErr
        assert self._till.split(' ')[-1] in ['Month', 'Months', 'month', 'months', 'Day', 'Days', 'day', 'days', 'Year', 'Years', 'year', 'years'], ProjectionErr
        assert type(int(self._till.split(' ')[0])) == int, ProjectionErr
        assert self._granularity in ['Months', 'Days','Years'], ProjectionGranErr1
        
        self._startDate = datetime.strptime(startdate, "%Y-%m-%d")
        if self._till.split(' ')[-1] in ['Day', 'Days', 'day', 'days']:
            self._endDate = self._startDate+relativedelta(days=int(till.split(' ')[0]))
        
        elif self._till.split(' ')[-1] in ['Month', 'Months', 'month', 'months']:
            self._endDate = self._startDate+relativedelta(months=int(till.split(' ')[0]))
        
        elif self._till.split(' ')[-1] in ['Year', 'Years', 'year', 'years']:
            self._endDate = self._startDate+relativedelta(years=int(till.split(' ')[0]))

        self._noOfDays = (self._endDate - self._startDate).days
        self._datesInBetween = [self._startDate+relativedelta(days=k) for k in range(self._noOfDays+1)]

        _available = []
        if self._noOfDays > 0:
            _available.append('Days')
        if self._noOfDays > 30:
            _available.append('Months')
        if self._noOfDays > 365:
            _available.append('Years')
        
        assert self._granularity in _available, ProjectionGranErr2.format(startdate, till,
                                                                                   self._granularity, _available)
        
    def _retrieve_parameters(self):

        # Calculate Time Dependent Values
        self._timeBasedRates = []


        if self.modelName == 'S_I_R':
            # SIR
            modes = ['sir.tr.cr', 'sir.tr.pr', 'sir.rm.recov']
            for _mode in modes:
                vals = self._calc_tdependent_rates(mode = _mode)
                self._timeBasedRates.append(vals)
            self._timeBasedRates = np.c_[self._timeBasedRates].T

            self._total_pop = self.configParams['params.sir.tpop.val']
            self._pandemic_name = self.configParams['general.pandemic.name']
            self._beta = self.configParams['params.sir.tr.cr.val']
            self._tproba = self.configParams['params.sir.tr.pr.val']
            self._infec_pop = self.configParams['params.sir.in.val']
            self._remov_pop = self.configParams['params.sir.rm.val']
            self._remov_recov_pct = self.configParams['params.sir.rm.recov.val']

            self._beta0 = self._timeBasedRates[:,0][0]
            self._tproba0 = self._timeBasedRates[:,1][0]
            self._gamma0 = self._timeBasedRates[:,2][0]



    def _calc_tdependent_rates(self, mode):
        '''
        parameters - 
            effect_dict : dict
                Dictionary Containing the Effect Dates and the value associated to it
            mode : str
                Takes values only from ['succecptible_pct', 'testing_pct', 'testing_pct.recovery']
        '''
        date_counter = self._startDate
        default_value = self.configParams[f'params.{mode}.val']
        delta_time = self.configParams[f'params.{mode}.etd']
        effect_dict = self.configParams[f'params.{mode}.es']
        value_list = [default_value]
        effect_dates = [datetime.strptime(k, "%Y-%m-%d") for k in effect_dict.keys()]

        while date_counter < self._endDate:
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

    def _tdependent_rates_gen(self):
        for i in range(self._timeBasedRates.shape[0]):
            yield self._timeBasedRates[i]

    def setup_report(self):
        fig, _ = plt.subplots()
        return fig
