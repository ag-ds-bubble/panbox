from ipywidgets import widgets
from .pansim_view_slab1 import PanSimSlab1
from .pansim_view_slab2 import PanSimSlab2

class PanSimViewHandler(PanSimSlab2, PanSimSlab1):
    def __init__(self):
        super().__init__()
        self.layoutS1()
        self.layoutS2()


    # @classmethod
    def layoutPanSimView(self):
        # Final Boxing
        self.pansim_View = widgets.VBox([self.S1_distribution_OUT, self.S2_HBOX])
        return self.pansim_View
        