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
    
def get_price_indexOf(price):
    '''
        price index  = today_price/ytd_price * today_price_index
        return price_index = price index      (type: np.ndarray.uint16)
    '''
    price_index = np.zeros(len(price), dtype = np.float64)
    price_index[0] = 1000 
    
    for today in range(1, len(price)):
        ytd = today -1
        price_index[today] = price[today]/price[ytd]*price_index[ytd]

    return price_index.astype(np.uint16)

def plot_MA(axis       ,\
            plt_no     ,\
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

    axis[plt_no].set_title(   'Stock')
    axis[plt_no].set(xlabel =  'Days')
    axis[plt_no].set(ylabel = 'Price')
    axis[plt_no].plot(close ,    'b-')

    #plot moving averages
    for MA, color in zip(movingavg, colors):    
        axis[plt_no].plot(MA , color) 
    


def plot_transact(axis   ,\
                  plt_no ,\
                  close  ,\
                  buy    ,\
                  sell   ):
    '''
        plot buying and selling pts on MA graph
    '''
    
    logger = log.getLogger('{:<15}'.format('plot transact points on MA graph'))
    
    #plot buy, sell pts
    axis[plt_no].plot(buy  , close[buy] , 'k.')
    axis[plt_no].plot(sell , close[sell], 'r.')


def plot_fund(axis    ,\
              plt_no   ,\
              sell_pt ,\
              fund    ):
    '''
        plot fund percentage according to sell point
    '''
    logger  = log.getLogger('{:<15}'.format('plot fund percentage'))

    #fund start with 100%
    fund    = np.concatenate(([100], fund))
    sell_pt = np.concatenate(([0]  , sell_pt))
        
    axis[plt_no].set_title(   'Earnings')
    axis[plt_no].set(xlabel = 'Days'    )
    axis[plt_no].set(ylabel = 'Percent' )

    for i in range(1, len(fund)):
        if fund[i]>fund[i-1]:
            axis[plt_no].plot(sell_pt[i], fund[i], 'g.')
            
        else:
            axis[plt_no].plot(sell_pt[i], fund[i], 'r.')
            
        axis[plt_no].annotate(str(int(fund[i])), xy=(sell_pt[i], fund[i]))
    
def plot_LGR(axis    ,\
             plt_no  ,\
             buy_pts ,\
             m       ,\
             c       ,\
             period  ):
    '''
        plot linear regression line
    '''
    for index in range(0, len(buy_pts)):
        start = buy_pts[index] - period + 1 #array index start with 0, so add 1
        end   = buy_pts[index]
        buy_x = np.arange(start, end)
        price = m[index]*buy_x + c[index]

        axis[plt_no].plot(buy_x, price, 'k-')
    
def plot_price_index(axis        ,\
                     plt_no      ,\
                     price_index ):
    '''
        plot stock price index
    '''
    axis[plt_no].set_title('Price Index')
    axis[plt_no].set(xlabel = 'Days'    )
    axis[plt_no].set(ylabel = 'Index' )
    axis[plt_no].plot(price_index, 'r-')
    
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