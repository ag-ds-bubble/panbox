from ..pansim_active.sim_controls import ActiveSimController


class PanSimAssembler(ActiveSimController):

    def __init__(self):
        super().__init__()

    def initialise_pansim(self):
        self.initialise_parameters()

    def instantiate_pansim(self):

        self.reset_widgets()
        
        self.pansimView.S2_L1_country_DD.observe(self.update_state, names=['value'])
        self.pansimView.S2_L1_state_DD.observe(self.update_popdensity, names=['value'])

        self.pansimView.S2_L1_msperday_IS.observe(self.pull_curr_param_values, names=['value'])
        self.pansimView.S2_L1_popdensity_FS.observe(self.pull_curr_param_values, names=['value'])
        self.pansimView.S2_L1_initialaffected_IS.observe(self.pull_curr_param_values, names=['value'])

        self.pansimView.S2_L2_infectradii_FS.observe(self.pull_curr_param_values, names=['value'])
        self.pansimView.S2_L2_transmissionprob_FS.observe(self.pull_curr_param_values, names=['value'])
        self.pansimView.S2_L2_incubperiod_IS.observe(self.pull_curr_param_values, names=['value'])
        self.pansimView.S2_L2_quarentineafter_IS.observe(self.pull_curr_param_values, names=['value'])
        self.pansimView.S2_L2_fatalityrate_FS.observe(self.pull_curr_param_values, names=['value'])
        self.pansimView.S2_L2_asymptrate_FS.observe(self.pull_curr_param_values, names=['value'])

        self.pansimView.S2_L3_socialdist_FS.observe(self.pull_curr_param_values, names=['value'])
        self.pansimView.S2_L3_travelradii_FS.observe(self.pull_curr_param_values, names=['value'])
        self.pansimView.S2_L3_interventionday_BIT.observe(self.pull_curr_param_values, names=['value'])

        self.pansimView.S2_L2_infectradii_FS.observe(self.update_dynamic_params, names=['value'])
        self.pansimView.S2_L2_transmissionprob_FS.observe(self.update_dynamic_params, names=['value'])
        self.pansimView.S2_L2_incubperiod_IS.observe(self.update_dynamic_params, names=['value'])
        self.pansimView.S2_L2_quarentineafter_IS.observe(self.update_dynamic_params, names=['value'])
        self.pansimView.S2_L2_fatalityrate_FS.observe(self.update_dynamic_params, names=['value'])
        self.pansimView.S2_L2_asymptrate_FS.observe(self.update_dynamic_params, names=['value'])

        self.pansimView.S2_L3_socialdist_FS.observe(self.update_dynamic_params, names=['value'])
        self.pansimView.S2_L3_travelradii_FS.observe(self.update_dynamic_params, names=['value'])
        self.pansimView.S2_L3_transproobafter_FS.observe(self.pull_curr_param_values, names=['value'])

        self.pansimView.S2_play_BTN.on_click(self.onclick_playbtn)
        self.pansimView.S2_pause_BTN.on_click(self.onclick_pausebtn)
        self.pansimView.S2_reset_BTN.on_click(self.onclick_resetbtn)

        return  self.pansimView.layoutPanSimView()