from ..pansim_view.pansim_view_handler import PanSimViewHandler
import pandas as pd
import numpy as np

class ActiveBase:

    def __init__(self):
        self.pansimData = {}
        density_data = pd.read_csv('panbox/_animutils/population_density.csv', index_col=0)
        density_data['Population_Density'] = (density_data['Population_Density']/density_data['Population_Density'].max())*1500
        self.pansimData['popdensity_data'] = density_data
        self.pansimView = PanSimViewHandler()

    def initialise_parameters(self):
        # Canvas Based
        self.countries = self.pansimData['popdensity_data'].Country.unique().tolist()
        self.country = self.countries[0]

        _tempcountry = self.pansimData['popdensity_data'].Country.unique().tolist()[0]
        self.states = self.pansimData['popdensity_data'].set_index('Country').loc[_tempcountry].State.unique().tolist()
        self.state = self.states[0]

        _tempstate = self.states[0]
        _popdensity = self.pansimData['popdensity_data'].set_index('Country').loc[_tempcountry].set_index('State').loc[_tempstate]
        self.population_density = int(np.round(_popdensity['Population_Density']))
        self.ms_per_day = 5
        self.initially_infected_people = 10
        self.r_naught_after = 2.2

        # Disease Based
        self.infection_radius = 1
        self.quarentineafter = 14
        self.transmission_probab = 0.4
        self.fatality_rate = 0.02
        self.incubation_period = 28
        self.asymptomatic_percent = 0.5


        # Counter Measures
        self.socialdistancing_reulsiveforce = 0.0
        self.travelling_radius = 100
        self.intervene_after_days = 10

    def reset_widgets(self):

        self.pansimView.S2_L1_country_DD.options = self.countries
        self.pansimView.S2_L1_country_DD.value = self.countries[0]

        _tempcountry = self.pansimData['popdensity_data'].Country.unique().tolist()
        self.states = self.pansimData['popdensity_data'].set_index('Country').loc[self.country].State.unique().tolist()
        self.state = self.states[0]

        self.pansimView.S2_L1_state_DD.options = self.states
        self.pansimView.S2_L1_state_DD.value = self.state

        _popdensity = self.pansimData['popdensity_data'].set_index('Country').loc[self.country].set_index('State').loc[self.pansimView.S2_L1_state_DD.value]
        _popdensity = _popdensity['Population_Density']
        
        self.pansimView.S2_L1_msperday_IS.min = 1
        self.pansimView.S2_L1_msperday_IS.value = 5
        self.pansimView.S2_L1_msperday_IS.max = 30

        self.pansimView.S2_L1_popdensity_FS.max = 1500
        self.pansimView.S2_L1_popdensity_FS.min = 10
        self.pansimView.S2_L1_popdensity_FS.value = _popdensity



        self.pansimView.S2_L1_initialaffected_IS.min = 1
        self.pansimView.S2_L1_initialaffected_IS.value = 10
        self.pansimView.S2_L1_initialaffected_IS.max = 100

        

        self.pansimView.S2_L2_infectradii_FS.min = 0.1
        self.pansimView.S2_L2_infectradii_FS.value = 1
        self.pansimView.S2_L2_infectradii_FS.max = 20

        self.pansimView.S2_L2_transmissionprob_FS.min = 0
        self.pansimView.S2_L2_transmissionprob_FS.value = 0.4
        self.pansimView.S2_L2_transmissionprob_FS.max = 1
        
        self.pansimView.S2_L2_incubperiod_IS.min = 0
        self.pansimView.S2_L2_incubperiod_IS.value = 14
        self.pansimView.S2_L2_incubperiod_IS.max = 50

        self.pansimView.S2_L2_quarentineafter_IS.min = 0
        self.pansimView.S2_L2_quarentineafter_IS.value = 2
        self.pansimView.S2_L2_quarentineafter_IS.max = 100

        self.pansimView.S2_L2_fatalityrate_FS.min = 0.0
        self.pansimView.S2_L2_fatalityrate_FS.value = 0.02
        self.pansimView.S2_L2_fatalityrate_FS.max = 1.0

        self.pansimView.S2_L2_asymptrate_FS.min = 0.0
        self.pansimView.S2_L2_asymptrate_FS.value = 0.0
        self.pansimView.S2_L2_asymptrate_FS.max = 1.0



        self.pansimView.S2_L3_socialdist_FS.min = 0.0
        self.pansimView.S2_L3_socialdist_FS.value = 0.0
        self.pansimView.S2_L3_socialdist_FS.max = 1.0

        self.pansimView.S2_L3_travelradii_FS.min = 10
        self.pansimView.S2_L3_travelradii_FS.value = 100
        self.pansimView.S2_L3_travelradii_FS.max = 100

        self.pansimView.S2_L3_interventionday_BIT.min = 0
        self.pansimView.S2_L3_interventionday_BIT.value = 10
        self.pansimView.S2_L3_interventionday_BIT.max = 1500

        self.pansimView.S2_L3_transproobafter_FS.min = 0.0
        self.pansimView.S2_L3_transproobafter_FS.value = 0.5
        self.pansimView.S2_L3_transproobafter_FS.max = 1.0

    def pull_curr_param_values(self, change=None):

        # Canvas Based
        self.selected_country = self.pansimView.S2_L1_country_DD.value
        self.selected_state = self.pansimView.S2_L1_state_DD.value
        self.population_density = int(np.round(self.pansimView.S2_L1_popdensity_FS.value))
        self.ms_per_day = self.pansimView.S2_L1_msperday_IS.value
        self.initially_infected_people = int(self.pansimView.S2_L1_initialaffected_IS.value)
        self.r_naught_after = self.pansimView.S2_L3_transproobafter_FS.value

        # Disease Based
        self.infection_radius = self.pansimView.S2_L2_infectradii_FS.value
        self.transmission_probab = self.pansimView.S2_L2_transmissionprob_FS.value
        self.incubation_period = self.pansimView.S2_L2_incubperiod_IS.value
        self.quarentineafter = self.pansimView.S2_L2_quarentineafter_IS.value
        self.fatality_rate = self.pansimView.S2_L2_fatalityrate_FS.value
        self.asymptomatic_percent = self.pansimView.S2_L2_asymptrate_FS.value

        # Counter Measures
        self.socialdistancing_reulsiveforce = self.pansimView.S2_L3_socialdist_FS.value
        self.travelling_radius = self.pansimView.S2_L3_travelradii_FS.value
        self.intervene_after_days = self.pansimView.S2_L3_interventionday_BIT.value


