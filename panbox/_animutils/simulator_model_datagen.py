import pandas as pd
import numpy as np

class ModelAnimDataGenerator(object):
    
    def __init__(self, modelname = 'S_I_R'):
        self.modelName = modelname

    def dataGen(self, _dp):

        if self.modelName == 'S_I_R':
            dates, oderes, _ = _dp
            for each in range(1, len(oderes)+1):
                yield dates[:each], oderes[:each,:]