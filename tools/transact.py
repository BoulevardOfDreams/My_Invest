# Standard library imports
import logging as log
from enum import Enum

# Third party imports
import numpy as np

# Local application imports

class signal(Enum):
    none = 0
    buy  = 1
    sell = 2
    
class transact():
    def __init__(self, buy, sell, df_close):
        
        self.log          = log.getLogger('{:<15}'.format('transact'))
        self.close        = df_close.to_numpy()[::-1]
        self.transact_pts = self.__process(buy, sell)
        
    def __process(self, buy, sell):
        '''
            determine buy and sell points
            parameter:  buy    = buy points  (type: np.ndarray.bool) 
                        sell   = sell points (type: np.ndarray.bool)
            return   :  result = transact pts(type: np.ndarray.int)
                        0: No Action
                        1: Buy
                        2: Sell 
        '''
        buy_signal      = 1
        sell_signal     = 2
        previous        = sell_signal
        result          = np.zeros(len(buy))
        is_overlap      = np.all(buy & sell)
        
        if is_overlap:
            self.log.warning('buy sell points overlapping')
        
        for i in range(1,len(buy)):
            
            if previous == sell_signal:
                
                is_buy    = (buy[i] == True)
                
                if is_buy:
                    previous  = buy_signal  
                    result[i] = buy_signal
                
            else:
                
                is_sell   = (sell[i] == True)
                
                if is_sell:
                    previous  = sell_signal 
                    result[i] = sell_signal
                
        self.log.info('process buy and sell signals')
        return result
    
    def calc_NetProfit(self):
        '''
            Calculate fund percent after sell
            return   :  ls_result = fund percent after sell (type: np.ndarray.float32)
        '''
        sell           = self.close[self.transact_pts == 2]
        buy            = self.close[self.transact_pts == 1][:len(sell)]
        ls_result      = []
        fund_perct     = 1
        
        
        #profit include interest
        pii_percent = ((sell-buy)/buy) - 0.011
        
        for pii in pii_percent:
            fund_perct += fund_perct*pii
            ls_result.append(fund_perct)
        
        #initial fund percent = 1
        ls_result.insert(0, fund_perct)
        
        #convert to percent
        ls_result = [r*100 for r in ls_result]
        
        self.log.info('calculate earning/loss percent')
        return ls_result
        
    
        
        