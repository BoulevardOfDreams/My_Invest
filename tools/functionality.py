# Standard library imports
import logging as log
from os.path import join

# Third party imports
import numpy as np
import matplotlib.pyplot as plt

def np_shift(arr, num, fill_value=np.nan):
    result = np.empty_like(arr)
    if num > 0:
        result[:num] = fill_value
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = fill_value
        result[:num] = arr[-num:]
    else:
        result = arr
    return result
    
    
def setup_plot(axis       ,\
               close      ,\
               macd       ,\
               signal     ,\
               hist       ,\
               sma        ,\
               ema        ,\
               buy        ,\
               sell       ,\
               s_index    ,\
               fund       ,\
               rsi        ):
    '''
        plot all graph and save (modifiable)
    '''
    logger            = log.getLogger('{:<15}'.format('plot'))
    
    #sma, ema
    axis[0].set_title(       'Stock')
    axis[0].set(xlabel     =  'Days')
    axis[0].set(ylabel     = 'Price')
    axis[0].plot(close     ,    'b-')
    axis[0].plot(sma       ,    'r-') 
    axis[0].plot(ema       ,    'm-')
    
    #macd, hist
    axis[1].set_title('Macd ({0},{1},{2})'.format(12,26,9))
    axis[1].set(xlabel     =  'Days')
    axis[1].set(ylabel     = 'Index')
    axis[1].plot(macd      ,    'r-')
    axis[1].plot(signal    ,    'g-')
    axis[1].bar(range(0,   len(hist)),\
                height     =  hist   ,\
                color      = 'green')
                
    #buy, sell
    x = np.arange(len(close))
    axis[0].plot(x[buy] , close[buy] , 'k.')
    axis[0].plot(x[sell], close[sell], 'r.')
                
    #earning plot
    axis[2].set_title(       'Earnings')
    axis[2].set(xlabel     = 'Days'    )
    axis[2].set(ylabel     = 'Percent' )
    
    for i in range(1, len(fund)):
        if fund[i]>fund[i-1]:
            axis[2].plot(s_index[i], fund[i], 'g.')
            
        else:
            axis[2].plot(s_index[i], fund[i], 'r.')
            
        axis[2].annotate(str(int(fund[i])), xy=(s_index[i], fund[i]))
    
    logger.info('setup')
    
    #rsi
    upper_limit = np.ones(len(hist))*65
    lower_limit = np.ones(len(hist))*30
    axis[3].set_title(      'RSI' )
    axis[3].set(xlabel    = 'Days')
    axis[3].set(ylabel    = 'val' )
    axis[3].plot(upper_limit , 'r')
    axis[3].plot(lower_limit , 'r')
    axis[3].plot(rsi         , 'g')   
    
    
def save(name, fig, format = '.pdf'):

    logger = log.getLogger('{:<15}'.format('save'))
    
    fig_path = join('.\\result\\figure', name + format)
    fig.savefig(fig_path)
    
    logger.info('{} saved'.format(name))