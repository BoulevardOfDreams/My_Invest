# Standard library imports
import logging as log
import warnings as warn

# Third party imports
import talib
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
from tools.functionality import np_shift

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
        
        #Catch all warning :(
        warn.simplefilter('ignore')
        
        self.macd, self.signal, self.hist = self.analyse(df_close)
        
        
        
    def analyse(self, close):
        '''
        parameter: close  = closing price (type: dataframe)         
        return   : macd   = macd          (type: np.ndarray.float64)							  
                   signal = signal        (type: np.ndarray.float64)
			       hist	  = macd - signal (type: np.ndarray.float64)
        '''
        self.log.info('MACD	   :Start Analysis                    \n\
                     {fill:<46}Parameter:                         \n\
                     {fill:<46}fastperiod   = {self.fastperiod}   \n\
                     {fill:<46}slowperiod   = {self.slowperiod}   \n\
                     {fill:<46}signalperiod = {self.signalperiod} \n'.format(self=self, fill=''))
        
        close_data		                  = close.to_numpy()
        self.macd, self.signal, self.hist = talib.MACD(
                                            close_data[::-1],\
                                            self.fastperiod ,\
                                            self.slowperiod ,\
                                            self.signalperiod)
        return (self.macd, self.signal, self.hist)    

    def tbuy_momentum_up(self, strict_mode = False):
    
        days     = 3
        thres    = 0.1
        scale    = 100
        hist_len = len(self.hist)
        result   = np.zeros(hist_len).astype(bool)
            
        for i in range(2, hist_len):
        
            hist_diff = self.hist[i]-self.hist[i-2]
            gradient  = (hist_diff)/days*scale
            
            if strict_mode:
                result[i] = gradient > thres and self.hist[i] > 0
            else:
                result[i] = gradient > thres
                
        self.log.info('tbuy_momentum_up, strict = {}'.format(strict_mode))
        
        return result
    
    def buy_momentum_up(self, strict_mode = False):
            
        hist_today   = self.hist[-1]
        hist_last    = self.hist[-2]
        gradient     = (hist_today-hist_last)/base_len
        result       = gradient > thres
        
        if strict_mode:
            result = result and hist_today > 0
        
        self.log.info('buy_momentum_up, strict = {}'.format(strict_mode))
        
        return result
    
    def tbuy_abv_thres(self, thres, strict_mode = False):
        '''
            test buy when hist > threshold
            parameter: thres  = hist value scale 100 (type: int)         
            return   : buy    = buy signal           (type: np.ndarray.bool)							  
        '''
        
        scale       = 100
        hist_today  = self.hist*scale
        hist_last   = np_shift(self.hist, 1, np.nan)*scale
        
        self.log.info('tbuy_abv_thres, strict = {}'.format(strict_mode))
        
        if strict_mode:
            return (hist_today > thres) &\
                   (hist_last  > thres)
        else:
            return (hist_today > thres)
        
    def buy_abv_thres(self, strict_mode = False):
        
        thres       = 1
        scale       = 100
        hist_today  = self.hist[-1]*scale
        hist_last   = self.hist[-2]*scale
        
        self.log.info('buy_abv_thres, strict = {}'.format(strict_mode))
        
        if strict_mode:
            return (hist_today > thres) and\
                   (hist_last  > thres)
        else:
            return (hist_today > thres)
        
    def tsell_below_thres(self, thres):
        '''
            test sell when hist < threshold
            parameter: thres  = hist value scale 100 (type: int)         
            return   : sell   = sell signal           type: np.ndarray.bool)							  
        '''
        scale       = 100
        
        self.log.info('tsell_below_thres')
        
        return (self.hist*scale)<thres
        
    def sell_below_thres(self):
        thres       = 0
        scale       = 100
        
        self.log.info('sell_below_thres')
        
        return (self.hist[-1]*scale)<thres
        
        
        
if __name__ == "__main__":
    print(__name__)