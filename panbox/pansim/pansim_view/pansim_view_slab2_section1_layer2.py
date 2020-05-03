from ipywidgets import widgets

class PanSimSlab2Section1Layer2:
    def __init__(self):
        self.layoutS2Section1Layer2()
        
    
    def layoutS2Section1Layer2(self):
        self.S2_L2_header_LBL = widgets.Label('Disease Parameters',
                                              layout={'border'  : '1px solid black',
                                                      'width' : '572px',
                                                      'height' : '28px'})

        style = {'description_width': 'initial'}
        self.S2_L2_infectradii_FS = widgets.FloatSlider(value=1, min=0, max=999, step=0.1, description='InfectRadii(mt):',
                                                     orientation='horizontal', readout=True, style=style)
        self.S2_L2_transmissionprob_FS = widgets.FloatSlider(value=0, min=0, max=999, step=0.01, description='TransmissionProb:',
                                                     orientation='horizontal', readout=True, style=style)
        self.S2_L2_incubperiod_IS = widgets.IntSlider(value=0, min=0, max=999, step=1, description='IncubPeriod(days):',
                                                     orientation='horizontal', readout=True, style=style)
        self.S2_L2_quarentineafter_IS = widgets.IntSlider(value=0, min=0, max=999, step=1, description='QuarentineAfter(days):',
                                                     orientation='horizontal', readout=True, style=style)
        self.S2_L2_fatalityrate_FS = widgets.FloatSlider(value=0, min=0, max=999, step=0.01, description='FatalityRate:',
                                                     orientation='horizontal', readout=True, style=style)
        self.S2_L2_asymptrate_FS = widgets.FloatSlider(value=0, min=0, max=999, step=0.01, description='AsymptPct:',
                                                     orientation='horizontal', readout=True, style=style)

        self.S2_L2_VBOX1 = widgets.VBox([self.S2_L2_infectradii_FS, self.S2_L2_transmissionprob_FS, self.S2_L2_incubperiod_IS],
                                        layout={'width' : '285px', 'height' : '120px'})
        self.S2_L2_VBOX2 = widgets.VBox([self.S2_L2_quarentineafter_IS,  self.S2_L2_fatalityrate_FS, self.S2_L2_asymptrate_FS],
                                        layout={'width' : '285px', 'height' : '120px'})
        self.S2_L2_HBOX1 = widgets.HBox([self.S2_L2_VBOX1, self.S2_L2_VBOX2],
                                         layout={'margin' : '0px 0px 0px 0px'})
        self.S2_L2_VBOX3 = widgets.VBox([self.S2_L2_header_LBL, self.S2_L2_HBOX1],
                                        layout={'height' : '160px', 'margin' : '0px 0px 0px 0px'})