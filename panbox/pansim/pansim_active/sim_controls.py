from ...pansim.pansim_view.pansim_view_handler import PanSimViewHandler
from ..._animutils.pansim_anim import PanSimulator, plt
from ...pansim.pansim_active.base import ActiveBase

from IPython.display import display, clear_output
import matplotlib.animation as animation

class ActiveSimController(ActiveBase):


    def __init__(self):
       # Add handlerss
        super().__init__()
        self.animstatus = 'idle'


    def update_state(self, change):

        # Find out which country the DD currently holds
        # Update the state list and options
        self.country = self.pansimView.S2_L1_country_DD.value
        _tempcountry = self.pansimData['popdensity_data'].Country.unique().tolist()
        self.states = self.pansimData['popdensity_data'].set_index('Country').loc[self.country].State.unique().tolist()
        self.state = self.states[0]

        self.pansimView.S2_L1_state_DD.options = self.states
        self.pansimView.S2_L1_state_DD.value = self.state


    def update_popdensity(self, change):

        _popdensity = self.pansimData['popdensity_data'].set_index('Country').loc[self.country].set_index('State').loc[self.pansimView.S2_L1_state_DD.value]
        self.population_density = _popdensity['Population_Density']
        self.pansimView.S2_L1_popdensity_FS.value = self.population_density


    def onclick_playbtn(self, change):
        
        self.pull_curr_param_values()
        if self.animstatus == 'idle':
            self.simulatorHandler = PanSimulator(_initial_infected = self.initially_infected_people, _initial_asymtomatic_pct = self.asymptomatic_percent, 
                                                _pop_density = self.population_density,  _intervention_after = self.intervene_after_days, 
                                                _generator_type = 'angle_based', _simupdate_rate = self.ms_per_day, _rnaught_after=self.r_naught_after)
            self.simulatorHandler.update_dynamic_params(_infect_radii = self.infection_radius , _fatality_rate = self.fatality_rate,
                                                         _trans_proba = self.transmission_probab, _incub_period = self.incubation_period,
                                                        _quarantine_after = self.quarentineafter, _asympt_pct = self.asymptomatic_percent,
                                                         _social_distancing_factor = self.socialdistancing_reulsiveforce, _travel_radii = self.travelling_radius)

            with self.pansimView.S2_simulation_OUT:
                clear_output(wait=True)
                self.simulatorHandler.instantiate_sim_canvas()
                plt.show()
                self.animstatus = 'playing'
            with self.pansimView.S1_distribution_OUT:
                clear_output(wait=True)
                self.simulatorHandler.instantiate_day_canvas()
                plt.show()
                self.animstatus = 'playing'
        else:
            self.simulatorHandler.ani.event_source.start()
            self.animstatus = 'playing'


    def onclick_pausebtn(self, change):
        self.simulatorHandler.ani.event_source.stop()
        self.animstatus = 'paused'
        

    def onclick_resetbtn(self, change):
        self.reset_widgets()
        with self.pansimView.S2_simulation_OUT:
            clear_output(wait=True)
            self.simulatorHandler.ani.event_source.stop()
            self.simulatorHandler.scat.set_offsets([0,0])
            self.simulatorHandler.scat_glow.set_offsets([0,0])
            self.simulatorHandler.rnaught_text.set_text('R0: '.translate(self.simulatorHandler.SUB)+str(float(0)))
            self.simulatorHandler.day_text.set_text('Day : '+str(0))
            display(self.simulatorHandler.scat.figure)
            self.animstatus = 'idle'

        with self.pansimView.S1_distribution_OUT:
            clear_output(wait=True)
            display('Simulation Stopped')


    def update_dynamic_params(self, change):
        # self.intervene_after_days = self.pansimView.S2_L3_interventionday_BIT.value

        if 'simulatorHandler' in self.__dir__():

            self.simulatorHandler.update_dynamic_params(_infect_radii = self.infection_radius, _fatality_rate = self.fatality_rate,
                                                        _trans_proba = self.transmission_probab, _incub_period = self.incubation_period,
                                                        _quarantine_after = 2, _asympt_pct = self.asymptomatic_percent, 
                                                        _social_distancing_factor = self.socialdistancing_reulsiveforce, _travel_radii = self.travelling_radius)



    