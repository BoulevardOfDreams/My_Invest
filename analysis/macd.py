# Standard library imports
import logging as log

# Third party imports
import talib
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
from tools.functionality import np_shift

        
def RSI__IsOverbought(rsi_value, upper_limit):
    '''
    parameter: rsi_value = value from talib.RSI
    return	 : range of days where overbought happens. (True = 'Overbought')
    '''
    dummy_val = 50
    return np_shift((rsi_value>=upper_limit),1,0)& \
          (np_shift(rsi_value,1,dummy_val)>rsi_value)
		  
def RSI__IsOversold(rsi_value, lower_limit):
    '''
    parameter: rsi_value = value from talib.RSI
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

class MACD():

    '''
    parameter: class init
	           df_close        = closing price                    [df  : required]
               fastperiod      = fast EMA period   , < slowperiod [int : optional]
			   slowperiod      = slow EMA period   , > fastperiod [int : optional]
			   signalperiod    = signal EMA period , < fastperiod [int : optional]                  	  	
    '''
	
    def __init__(self, df_close , \
                fastperiod  = 12, \
                slowperiod  = 26, \
                signalperiod= 9   ):
        
        self.log            = log.getLogger('{:<15}'.format('macd'))
        self.close_data     = df_close.to_numpy()[::-1]
        self.fastperiod		= fastperiod
        self.slowperiod		= slowperiod
        self.signalperiod	= signalperiod

        self.macd, self.signal, self.hist = self.analyse(df_close)
        
        
        
    def analyse(self, close):
        '''
        parameter: close  = closing price (type: dataframe)         
        return   : macd   = macd          (type: np.ndarray.float64)							  
                   signal = signal        (type: np.ndarray.float64)
			       hist	  = macd - signal (type: np.ndarray.float64)
        '''
        self.log.info('MACD	   :Start Analysis               \n\
                          Parameter:                         \n\
                          fastperiod   = {self.fastperiod}   \n\
                          slowperiod   = {self.slowperiod}   \n\
                          signalperiod = {self.signalperiod} \n'.format(self=self))
        
        close_data		                  = close.to_numpy()
        self.macd, self.signal, self.hist = talib.MACD(
                                            close_data[::-1],\
                                            self.fastperiod ,\
                                            self.slowperiod ,\
                                            self.signalperiod)
        return (self.macd, self.signal, self.hist)    

    def test_buy_momentum(self, strict_mode = False):
    
        days     = 2
        thres    = 0
        hist_len = len(self.hist)
        result   = np.zeros(hist_len).astype(bool)
            
        for i in range(1, hist_len):
        
            hist_diff = self.hist[i]-self.hist[i-1]
            gradient  = (hist_diff)/days
            
            if strict_mode:
                result[i] = gradient > thres and self.hist[i] > 0
            else:
                result[i] = gradient > thres
                
        self.log.info('test momentum buy, strict = {}'.format(strict_mode))
        
        return result
    
    def buy_on_momentum(self, strict_mode = False):
            
        hist_today   = self.hist[-1]
        hist_last    = self.hist[-2]
        gradient     = (hist_today-hist_last)/base_len
        result       = gradient > thres
        
        if strict_mode:
            result = result and hist_today > 0
        
        self.log.info('real buy on momentun, strict = {}'.format(strict_mode))
        
        return result
        
    def test_buy_positive(self):
        self.log.info('test buy positive histogram')
        return np.where(self.hist > 0, 1, 0).astype(bool)
    
    def buy_positive_hist(self):
        self.log.info('real buy positive histogram')
        return self.hist[-1] > 0
        
    def test_sell_negative(self):
        self.log.info('test sell negative histogram')
        return np.where(self.hist < 0, 1, 0).astype(bool)
        
    def sell_negative_hist(self):
        self.log.info('real sell negative histogram')
        return self.hist[-1] < 0
        
if __name__ == "__main__":
    print(__name__)