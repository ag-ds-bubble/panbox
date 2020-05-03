  
"""
Epidimiological Simulator
===================================================
This module implemets an IPython Widget based simulator,
to gauge at the growth of the disease in a rather controlled
environment. 

This widget has conntrolling parameters for:- 
    - Properties for the initial population
    - Growth of the disease
    - Counter Measures
"""

from .pansim.pansim_active.active_assembler import PanSimAssembler as _PanSimAssembler


class PanSim:
    def __init__(self):
        self.panSimAssembler = _PanSimAssembler()

    # Simulator
    def assemblePanSim(self):
        self.panSimAssembler.initialise_pansim()
        return self.panSimAssembler.instantiate_pansim()
