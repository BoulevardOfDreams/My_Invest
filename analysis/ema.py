# Standard library imports
import logging as log

# Third party imports
import talib
import numpy as np

# Local application imports

class EMA():
    def __init__(self, df_close, period = 10):
        self.period = period
        self.log    = log.getLogger('{:<15}'.format('ema'))
        self.analysis(df_close, period)
        
    def analysis(self, df_close, period):
        close      = df_close.to_numpy()[::-1]
        self.ema   = talib.EMA(close, self.period).astype(np.float32)
        
        self.log.info('EMA, Period = {0}'.format(self.period))
        
        