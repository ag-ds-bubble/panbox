from ipywidgets import widgets
from ..._configs.pansim_configs import *

class PanSimSlab2Section1Layer1:
    def __init__(self):
        self.layoutS2Section1Layer1()

    def layoutS2Section1Layer1(self):
        # Slab 1
        self.S2_L1_header_LBL = widgets.Label('Canvas/ Area Properties', layout={'border'  : '1px solid black', 'width' : '572px', 'height' : '28px'})
        self.S2_L1_country_DD = widgets.Dropdown(options=['--'], value='--', description='Country:', disabled=False, layout={'width' : '200px', 'height' : '25px'})
        self.S2_L1_state_DD = widgets.Dropdown(options=['--'], value='--', description='State:', disabled=False, layout={'width' : '200px', 'height' : '25px'})

        style = {'description_width': 'initial'}
        self.S2_L1_msperday_IS = widgets.IntSlider(value=0, min=0, max=999, step=1, description='ms/Day:',
                                                     orientation='horizontal', readout=True, style=style)
        self.S2_L1_popdensity_FS = widgets.FloatSlider(value=0, min=0, max=999, step=0.5, description='Density(#People/km2):'.translate(SUP),
                                                     orientation='horizontal', readout=True, style=style)
        self.S2_L1_initialaffected_IS = widgets.IntSlider(value=0, min=0, max=999, step=1, description='InitialInfect(#People):',
                                                          orientation='horizontal', readout=True, style=style)

        self.S2_L1_VBOX1 = widgets.VBox([self.S2_L1_country_DD, self.S2_L1_popdensity_FS, self.S2_L1_msperday_IS], layout={'width' : '285px', 'height' : '128px'})
        self.S2_L1_VBOX2 = widgets.VBox([self.S2_L1_state_DD, self.S2_L1_initialaffected_IS], layout={'width' : '285px', 'height' : '128px'})
        self.S2_L1_HBOX1 = widgets.HBox([self.S2_L1_VBOX1, self.S2_L1_VBOX2], layout={'margin' : '0px 0px -23px 0px'})
        self.S2_L1_VBOX3 = widgets.VBox([self.S2_L1_header_LBL, self.S2_L1_HBOX1], layout={'height' : '130px', 'margin' : '0px 0px 0px 0px'})

        self.S2_L1_country_DD.disabled = pansimConfigs['properties.area.demographicwise.disabled']
        self.S2_L1_state_DD.disabled   = pansimConfigs['properties.area.demographicwise.disabled']
        