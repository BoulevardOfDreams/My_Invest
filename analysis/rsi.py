# Standard library imports
import logging as log
import warnings as warn

# Third party imports
import talib
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
from tools.functionality import np_shift

class RSI():
    def __init__(self, df_close, timeperiod):
        self.log   = log.getLogger('{:<15}'.format('rsi'))
  
        close_data = df_close.to_numpy()[::-1]
        self.rsi   = self.analyse(close_data, timeperiod)
        
    def analyse(self, close_data, timeperiod):
        '''
        rsi analysis
        '''
    
        self.log.info('start rsi analysis')
        
        result = talib.RSI(close_data, timeperiod).astype(np.float32)
        result[np.isnan(result)] = 50
        return result
        
    def isOverbought(self, upper_limit = 70):
        '''
        parameter: upper_limit = higher than upper_limit is overbought
        return	 : range of days where overbought happens. (True = 'Overbought')
        '''
        
        self.log.info('measure overbought, thres = {}'.format(upper_limit))
        return (self.rsi > upper_limit)
        
    def isOversold(self, lower_limit = 30):
        '''
        parameter: lower_limit = lower than lower_limit is oversold
        return	 : range of days where oversold happens. (True = 'Oversold')
        '''
        
        self.log.info('measure oversold, thres = {}'.format(lower_limit))
        return (self.rsi < lower_limit)
        
def RSI__IsOverbought(rsi_value, upper_limit):
    '''
    parameter: upper_limit = higher than upper_limit is over bought
    return	 : range of days where overbought happens. (True = 'Overbought')
    '''
    dummy_val = 50
    return np_shift((rsi_value>=upper_limit),1,0)& \
          (np_shift(rsi_value,1,dummy_val)>rsi_value)
		  
def RSI__IsOversold(rsi_value, lower_limit):
    '''
    parameter: lower_limit = smaller than lower_limit is over sold
    return	 : range of days where oversold happens. (True = 'Oversold')
    '''
    dummy_val = 50
    return np_shift((rsi_value<=lower_limit),1,0)& \
           (np_shift(rsi_value,1,dummy_val)<rsi_value)

def RSI_analysis(close_data, timeperiod, upper_limit = 70, lower_limit = 30):
    '''
    parameter: close_data = closing price array (type: np.ndarray.float64)
    return	 : rsi_buy_signal  = range of days to 'Buy'. True = 'Buy'
               rsi_sell_signal = range of days to 'Sell'. True ='Sell'	
    '''
    dummy_value 	= 50
    rsi_value		= talib.RSI(close_data, timeperiod).astype(np.float32)
    rsi_value 		= rsi_value[~np.isnan(rsi_value)] #only select non-nan RSI value			  
    rsi_buy_signal  = RSI__IsOversold(rsi_value, lower_limit)
    rsi_sell_signal	= RSI__IsOverbought(rsi_value,upper_limit)
    return (rsi_value,rsi_buy_signal,rsi_sell_signal)
    
