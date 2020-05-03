from .core_configs import *

panmodel_configs = {
                    'general.pandemic.name' : 'Pandemic',

                    #SIR
                    'params.sir.tpop.val' : 7_75_66_886,

                    'params.sir.tr.cr.es': {},
                    'params.sir.tr.pr.es': {},
                    'params.sir.tr.cr.etd': 10,
                    'params.sir.tr.pr.etd': 10,
                    'params.sir.tr.cr.val' : 0.6, # social distancing
                    'params.sir.tr.pr.val' : 0.2, # better handwashing
                    'params.sir.in.val' : 30,
                    
                    'params.sir.rm.recov.es': {},
                    'params.sir.rm.recov.etd': 10,
                    'params.sir.rm.recov.val': 0.01,
                    'params.sir.rm.val' : 0
                    
                    
                    }




StartDateErr = '''The '_start_date' format should be only of %Y-%m-%d format.'''
ProjectionErr = '''The '_projections_till' parameter takes period only in the format of : \
1 Day/ 198 Days/ 1 Month/ 3 Months/ 1 Year/ 2 Years'''
ProjectionGranErr1 = '''The '_projection_granularity' parameter can only be \
one of : ['Days', 'Months', 'Years']'''
ProjectionGranErr2 = '''With '_start_date' as {0}, and '_projections_till' set to {1}, granularity \
of {2} is not possible. '_projection_granularity' can be only one of {3} '''
