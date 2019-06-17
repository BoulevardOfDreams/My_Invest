# Standard library imports
import logging as log

# Third party imports
import talib
import numpy as np
import matplotlib.pyplot as plt

class SMA():
    def __init__(self, df_close, period = 50):
        self.log    = log.getLogger('{:<15}'.format('sma'))
        self.close  = df_close.to_numpy()[::-1]
        self.period = period
        
        self.analysis(df_close)
        
        
    def analysis(self, df_close):
        self.log.info('SMA, Period = {0}'.format(self.period))
        
        close        = df_close.to_numpy()[::-1]
        self.result  = talib.SMA(close, self.period).astype(np.float32)
        
    def test_buy_abv_sma(self):
        self.log.info('test buy above sma')
        return np.where(self.close>self.SMA, 1, 0).astype(bool)
    
    def buy_abv_sma(self):
        self.log.info('real buy above sma')
        return self.close > self.SMA
        
        
def SMA_analysis(close_data, period):
    '''
    parameter: close_data = closing price array (type: np.ndarray.float64)
    return	 : 1. signal
                  - within period  = False(Invalid)
                  - greater period = return True(above SMA) and False(below SMA)
               2. SMA
                  - moving average result
    '''
    data_len 		= len(close_data)
    SMA				= np.zeros(data_len)
    signal 			= np.zeros(data_len, dtype = bool)

    if data_len > period:
        SMA  			= talib.SMA(close_data, period).astype(np.float32)
        signal[period:] = close_data[period:] > SMA[period:]
        log.info('SMA: Complete')
        return (signal, SMA)
    else:
        log.error('SMA: Data length < 200 ')
        return (signal, SMA)