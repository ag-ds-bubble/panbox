  
"""
Epidimiological Models
===================================================
This module implements Epidemiological models for the following purposes :-
    - Generate a setup report
    - Simulate a buildup of a model
    - Fit and Preddict on the real world data for the disease

Models Included:-
    - SIR :: Simple Epidemiological model, Succeptible-Infected-Removed

These models are a mixture of Ordinary Differential Equation (ODE) and 
Partial Differential Models (PDE), depending on time-dependent/time-indep-
ndent parameters.

"""


from .panmodels.panmodel_sir import SIRModel