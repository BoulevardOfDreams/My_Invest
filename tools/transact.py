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
    def __init__(self, buy, sell):
        
        self.log          = log.getLogger('{:<15}'.format('transact'))
        self.transact_pts = self.__process(buy, sell)
        
    def __process(self, buy, sell):
        
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
            