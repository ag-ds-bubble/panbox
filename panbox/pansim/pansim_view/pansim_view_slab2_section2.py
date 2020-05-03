from ipywidgets import widgets

class PanSimSlab2Section2:
    def __init__(self):
         self.layoutS2Section2()

    
    def layoutS2Section2(self):
        self.S2_simulation_OUT =  widgets.Output(layout={'border'  : '2px solid black', 
                                                        'height' : '365px',
                                                        'width'  : '400px'})
        
        self.S2_play_BTN = widgets.Button(description="Play", layout={'height' : '29px', 'width'  : '128px'})
        self.S2_pause_BTN = widgets.Button(description="Pause", layout={'height' : '29px', 'width'  : '128px'})
        self.S2_reset_BTN = widgets.Button(description="Reset", layout={'height' : '29px', 'width'  : '128px'})

        self.S2_simulation_control_HBOX = widgets.HBox([self.S2_play_BTN, self.S2_pause_BTN, 
                                                        self.S2_reset_BTN], 
                                                layout={'border': '0.5px solid black'})
                                              
        self.S2_simulation_VBOX = widgets.VBox([self.S2_simulation_OUT,self.S2_simulation_control_HBOX], 
                                                layout={'border': '0.5px solid black'})
