# Standard library imports
import logging as log

# Third party imports
import talib
import numpy as np

# Local application imports

class EMA():
    def __init__(self, close, period = 10):
        self.period = period
        self.close = close
        self.log    = log.getLogger('{:<15}'.format('ema'))
        self.__analysis()
        
    def __analysis(self):
        self.log.info('EMA, Period = {0}'.format(self.period))
        
        self.ema   = talib.EMA(self.close, self.period).astype(np.float32)
        
        
        