import pandas as pd
import numpy as np

class PanSimDataGenerator(object):
    
    def __init__(self, _initial_infected = 20, _initial_asymtomatic_pct = 0.5, _pop_density = 500, 
                _intervention_after = 0, _generator_type = 'angle_based', _simupdate_rate = 5, _rnaught_after=1.0):
        
        # Initialise the parameters needed to generate these datapoints
        # This will be connected to the handles that will affect the 
        # points that will be generated further
        
        # Initial Initialisations an for Simulator
        # Data Related
        self.pop_density = _pop_density
        self.initial_infected = _initial_infected
        self.intervention_after = _intervention_after
        self.simupdate_rate = _simupdate_rate
        self.rnaught_after = _rnaught_after
        self.asympt_pct = _initial_asymtomatic_pct

        self.infect_radii = 1
        self.fatality_rate = 0.2
        self.trans_proba = 0.2
        self.quarantine_after = 2 * (1000/self.simupdate_rate)
        self.incub_period = 14 * (1000/self.simupdate_rate)
        self.social_distancing_factor = 0.0
        self.travel_radii = 100
        
        # Population Movement
        self.each_step = 0.005
        self.focus_angle = np.pi/2 #degrees
        self._pop_cord_t_minus = np.random.uniform(low=0, high=1, size=(self.pop_density, 2))
        self._pop_status = np.array([1]*int(_initial_infected*(1-_initial_asymtomatic_pct)) + 
                                    [3]*int(_initial_infected*_initial_asymtomatic_pct) + 
                                    [0]*(self.pop_density-_initial_infected))
        popstatusdiff = int(self.pop_density) - len(self._pop_status)
        if popstatusdiff>0 : self._pop_status = np.append(self._pop_status, np.array([0]*popstatusdiff))

        np.random.shuffle(self._pop_status)
        self.days_since_infected = np.array([-1]*self.pop_density)
        self.days_since_infected[self._pop_status.nonzero()[0]] = 0

        first_move = self.each_step*np.random.choice([-1,1], size=(self.pop_density, 2))
        self._pop_cord_t_naught = self._pop_cord_t_minus+first_move
        self.generator_type = _generator_type
        
    def simulator_datagen(self):
        
        while True:
            if self.generator_type == 'angle_based':
                _slope = np.arctan2(self._pop_cord_t_naught[:,1] - self._pop_cord_t_minus[:,1], 
                                    self._pop_cord_t_naught[:,0] - self._pop_cord_t_minus[:,0])
                _possible_deviations = np.linspace(-self.focus_angle/2,self.focus_angle/2, 100)
                _slope_deviation = _slope + np.random.choice(_possible_deviations, size=(self.pop_density,))
                _slope_deviation = self.each_step*np.c_[np.cos(_slope_deviation), np.sin(_slope_deviation)]
                self._pop_cord_t_naught += _slope_deviation
                self._pop_cord_t_naught = np.clip(self._pop_cord_t_naught, a_min=0, a_max=1)

            elif self.generator_type == 'random':
                self._pop_cord_t_naught += self.each_step * (np.random((self.pop_density, 2)) - 0.5) * 10
            
            _repulsion_check = (self._pop_cord_t_naught == 0) | (self._pop_cord_t_naught == 1)
            
            if any(_repulsion_check.sum(axis=1) > 0):
                _index_tobe_redrawn = _repulsion_check.sum(axis=1) > 0
                _slope = np.arctan2(self._pop_cord_t_naught[:,1][_index_tobe_redrawn] - self._pop_cord_t_minus[:,1][_index_tobe_redrawn], 
                                    self._pop_cord_t_naught[:,0][_index_tobe_redrawn] - self._pop_cord_t_minus[:,0][_index_tobe_redrawn])
                _slope_deviation = np.pi/2 - _slope
                _slope_deviation = self.each_step*np.c_[np.cos(_slope_deviation), np.sin(_slope_deviation)]
                self._pop_cord_t_minus[_index_tobe_redrawn] = self._pop_cord_t_naught[_index_tobe_redrawn]
                self._pop_cord_t_naught[_index_tobe_redrawn] += _slope_deviation
                
            # 0 : Sucessiptible
            # 1 : Infected
            # 2 : Removed
            # 3 : Asymptomatic
            # 4 : Quarentined

            # Monitor status of the population

            # Assign quarantined
            if self.quarantine_after != 0:
                check1 = self.days_since_infected == self.quarantine_after
                check2 = self._pop_status == 1
                self._pop_status[check1&check2] = 4
            
            # Assign asymptomatic people
            update_asympt_infected_no = int((self._pop_status == 1).sum()*self.asympt_pct) - (self._pop_status == 3).sum()
            if update_asympt_infected_no > 0 :
                self._pop_status[(self._pop_status == 1).nonzero()[0][:update_asympt_infected_no]] = 3

            # Assign Removed People
            # Cured..
            check1 = self.days_since_infected == self.incub_period
            check2 = self._pop_status == 1
            check3 = self._pop_status == 3
            check4 = self._pop_status == 4
            check5 = check2|check3|check4
            self._pop_status[check1&check5] = 2
            # Died..
            check0 = self.days_since_infected != 0.0
            check1 = self.days_since_infected%((1000/self.simupdate_rate))
            check1 = check1==0.0
            check2 = self._pop_status == 1
            check3 = self._pop_status == 3
            check4 = self._pop_status == 4
            check5 = check2|check3|check4
            check6 = check0&check1&check5
            deathbucket = np.random.choice([True, False], size=(check6.sum()), 
                                           p=[self.fatality_rate, 1-self.fatality_rate])
            self._pop_status[check6.nonzero()[0][deathbucket]] = 2


            _sucessiptible = self._pop_cord_t_naught[self._pop_status == 0]
            _sucessiptible_index = (self._pop_status == 0).nonzero()[0]
            
            _infected = self._pop_cord_t_naught[self._pop_status == 1]
            _infected_index = (self._pop_status == 1).nonzero()[0].tolist()
            
            _asymptomatic = self._pop_cord_t_naught[self._pop_status == 3]
            _asymptomatic_index = (self._pop_status == 3).nonzero()[0].tolist()
            
            _allinfected = self._pop_cord_t_naught[(self._pop_status == 1) | (self._pop_status == 3)]
            _allinfected_index = _infected_index
            _allinfected_index += _asymptomatic_index
            _dist = np.linalg.norm(_sucessiptible - _allinfected[:,None], axis=-1)
            _dist_mask =(_dist<(self.infect_radii/1000)).astype(int)
    
            # Assign new infections
            _new_infections = np.array([k for k in np.unique(_sucessiptible_index*_dist_mask) if k!= 0]).tolist()
            _transmission_probabilities = np.random.choice([True, False], size=len(_new_infections), p=[self.trans_proba,1-self.trans_proba])
            if _new_infections != []:
                self._pop_status[np.array(_new_infections)[_transmission_probabilities]] = 1
            
            # Update number of ms/days for this simulation
            self.days_since_infected[self._pop_status == 1] += 1
            self.days_since_infected[self._pop_status == 3] += 1
            self.days_since_infected[self._pop_status == 4] += 1
            
            yield self._pop_cord_t_naught, self._pop_status
    