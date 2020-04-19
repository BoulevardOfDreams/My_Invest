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
    


def plot_MA(axis       ,\
            index      ,\
            close      ,\
            *movingavg ):
    '''
        plot moving averages
        note* = max number MA allowed is 
                according to number of colors 
                (currently is 3)
    '''

    logger = log.getLogger('{:<15}'.format('plot moving averages'))
    colors = ('c-','r-','m-')    

    axis[index].set_title(   'Stock')
    axis[index].set(xlabel =  'Days')
    axis[index].set(ylabel = 'Price')
    axis[index].plot(close ,    'b-')

    #plot moving averages
    for MA, color in zip(movingavg, colors):    
        axis[index].plot(MA , color) 
    


def plot_transact(axis  ,\
                  index ,\
                  close ,\
                  buy   ,\
                  sell  ):
    '''
        plot buying and selling pts on MA graph
    '''
    
    logger = log.getLogger('{:<15}'.format('plot transact points on MA graph'))
    
    #plot buy, sell pts
    x = np.arange(len(close))
    axis[index].plot(x[buy] , close[buy] , 'k.')
    axis[index].plot(x[sell], close[sell], 'r.')


def plot_fund(axis    ,\
              index   ,\
              sell_pt ,\
              fund    ):
    
    '''
        plot fund percentage according to sell point
    '''
    
    logger = log.getLogger('{:<15}'.format('plot fund percentage'))
    
    axis[index].set_title(   'Earnings')
    axis[index].set(xlabel = 'Days'    )
    axis[index].set(ylabel = 'Percent' )

    for i in range(1, len(fund)):
        if fund[i]>fund[i-1]:
            axis[index].plot(sell_pt[i], fund[i], 'g.')
            
        else:
            axis[index].plot(sell_pt[i], fund[i], 'r.')
            
        axis[index].annotate(str(int(fund[i])), xy=(sell_pt[i], fund[i]))
    

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
    
    #macd, hist
    axis[1].set_title('Macd ({0},{1},{2})'.format(12,26,9))
    axis[1].set(xlabel     =  'Days')
    axis[1].set(ylabel     = 'Index')
    axis[1].plot(macd      ,    'r-')
    axis[1].plot(signal    ,    'g-')
    axis[1].bar(range(0,   len(hist)),\
                height     =  hist   ,\
                color      = 'green')
                
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