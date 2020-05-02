from ipywidgets import widgets
from ..pansim_view.pansim_view_slab2_section1_layer1 import PanSimSlab2Section1Layer1
from ..pansim_view.pansim_view_slab2_section1_layer2 import PanSimSlab2Section1Layer2
from ..pansim_view.pansim_view_slab2_section1_layer3 import PanSimSlab2Section1Layer3
from ..pansim_view.pansim_view_slab2_section2 import PanSimSlab2Section2


class PanSimSlab2(PanSimSlab2Section1Layer1, PanSimSlab2Section1Layer2, PanSimSlab2Section1Layer3, PanSimSlab2Section2):
    def __init__(self):
        # super().__init__()
        self.layoutS2Section1Layer1()
        self.layoutS2Section1Layer2()
        self.layoutS2Section1Layer3()
        self.layoutS2Section2()
    
    def layoutS2(self):
        
        self.S2_param_VBOX = widgets.VBox([self.S2_L1_VBOX3,
                                           self.S2_L2_VBOX3,
                                           self.S2_L3_VBOX3],
                                     layout={'border'  : '2px solid black', 
                                                         'height' : '400px',
                                                         'width'  : '580px'})

        self.S2_HBOX = widgets.HBox([self.S2_param_VBOX, self.S2_simulation_VBOX])

