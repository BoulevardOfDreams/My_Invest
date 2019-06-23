# Standard library imports
import logging as log

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
    
    
def plot_all(axis       ,\
             close_data ,\
             macd       ,\
             signal     ,\
             hist       ,\
             sma        ,\
             x          ,\
             y          ):
    '''
        plot all graph and save (modifiable)
    '''
    logger            = log.getLogger('{:<15}'.format('plot all'))
    
    #sma
    axis[0].set_title('Stock'              )
    axis[0].set(xlabel = 'Days'            )
    axis[0].set(ylabel = 'Price'           )
    axis[0].plot(close_data      ,     'b-')
    axis[0].plot(sma             ,     'g-') #sma
    
    #macd, hist
    axis[1].set_title('Macd ({0},{1},{2})'.format(12,26,9))
    axis[1].set(xlabel = 'Days'            )
    axis[1].set(ylabel = 'Index'           )
    axis[1].plot(macd            ,     'r-')
    axis[1].plot(signal          ,     'g-')
    axis[1].bar(range(0,   len(hist))     ,\
                height = hist             ,\
                color  = 'green'           )
                
    #TEST ONLY
    axis[0].plot(x, y,                 'k.')
    
    
    log.info('plot and save successful')
    plt.show()
    