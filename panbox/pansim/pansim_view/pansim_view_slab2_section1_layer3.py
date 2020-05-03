from ipywidgets import widgets
from ..._configs.pansim_configs import *


class PanSimSlab2Section1Layer3:
    def __init__(self):
        self.layoutS2Section1Layer3()

    
    def layoutS2Section1Layer3(self):
        self.S2_L3_header_LBL = widgets.Label('Counter Measure Parameters',
                                              layout={'border' : '1px solid black',
                                                      'width' : '572px',
                                                      'height' : '28px'})
        style = {'description_width': 'initial'}
        self.S2_L3_socialdist_FS = widgets.FloatSlider(value=0, min=0, max=999, step=0.01, description='SocialDist(force):',
                                                     orientation='horizontal', readout=True, style=style)
        self.S2_L3_travelradii_FS = widgets.FloatSlider(value=0, min=0, max=999, step=0.1, description='TravelRadii(km):',
                                                     orientation='horizontal', readout=True, style=style)
        self.S2_L3_interventionday_BIT = widgets.BoundedFloatText(value=7.0, min=0, max=100, step=0.5, description='Transmission(days after) @:', 
                                                               disabled=False, style=style, layout={'width' : '250px'})
        self.S2_L3_transproobafter_FS = widgets.FloatSlider(value=0, min=0, max=999, step=0.1, description='Transmission Reduction(%):'.translate(SUB),
                                                 orientation='horizontal', readout=True, style=style)


        self.S2_L3_VBOX1 = widgets.VBox([self.S2_L3_socialdist_FS, self.S2_L3_interventionday_BIT],
                                        layout={'width' : '295px','height' : '128px'})
        self.S2_L3_VBOX2 = widgets.VBox([self.S2_L3_travelradii_FS, self.S2_L3_transproobafter_FS],
                                        layout={'width' : '295px','height' : '128px'})
        self.S2_L3_HBOX1 = widgets.HBox([self.S2_L3_VBOX1, self.S2_L3_VBOX2],
                                         layout={'margin' : '0px 0px 0px 0px'})
        self.S2_L3_VBOX3 = widgets.VBox([self.S2_L3_header_LBL, self.S2_L3_HBOX1],
                                        layout={'height' : '150px','margin' : '0px 0px 0px 0px'})