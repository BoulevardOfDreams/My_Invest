# Standard library imports
import logging as log
import warnings as warn

# Third party imports
import talib
import numpy as np

# Local application imports
from tools.functionality import np_shift

class SMA():
    def __init__(self, close, period = 50):
        self.log    = log.getLogger('{:<15}'.format('sma'))
        self.close  = close
        self.period = period
        
        #Catch all warning :(
        warn.simplefilter("ignore")
        
        self.__analysis()
        
    def __analysis(self):
        self.log.info('SMA, Period = {0}'.format(self.period))
        
        self.sma  = talib.SMA(self.close, self.period).astype(np.float32)
    
    def test_buy_abv_sma(self, strict_mode = False):
    
        self.log.info('test buy abv sma, strict = {}'.format(strict_mode))

        abv_sma = np.where(self.close>self.sma, 1, 0).astype(bool) #NAN comparison warning
        
        if strict_mode:
            abv_2_days = np_shift(abv_sma,   \
                                  shift=2,   \
                                  fill_value=0)
            return abv_sma & abv_2_days
        else:
            return abv_sma
    
    def buy_abv_sma(self, strict_mode = False):
    
        self.log.info('test buy abv sma, strict = {}'.format(strict_mode))
        abv_sma = self.close[-1] > self.sma[-1]
        
        if strict_mode:
            abv_2_days = self.close[-3] > self.sma[-3]
            return abv_sma & abv_2_days
        else: 
            return abv_sma
        
    def test_sell_below_sma(self):
        
        self.log.info('test sell below sma')
        return np.where(self.sma > self.close, 1, 0).astype(bool) #NAN comparison warning
        
    def sell_below_sma(self):
    
        self.log.info('sell below sma')
        return self.sma[-1] > self.close[-1]
        
        
    
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