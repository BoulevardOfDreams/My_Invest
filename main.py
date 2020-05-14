# Standard library imports
import os
import logging as log

# Third party imports
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
from analysis.macd import MACD
from analysis.sma import SMA
from analysis.ema import EMA
from analysis.rsi import RSI
from analysis.regression import linear_regression
from tools.functionality import save, np_shift, get_price_indexOf, plot_MA, plot_fund, plot_transact, plot_LGR, plot_price_index
from tools.logger import init_logger
from tools.reader import read_file
from tools.scraper import csv_scraper, stock_manager
from tools.transact import transact


class context():
    def __init__(self):
        self.MA200 = 200
        self.MA100 = 100
        self.MA50  = 50
        
    
def main():
    init_logger(log_level = log.INFO)
    
    from os import getcwd, listdir, remove
    from os.path import join, isfile
    
    #directories
    database_dir  = os.path.join(os.getcwd(), 'Database')
    fig_dir       = os.path.join(os.getcwd(), 'result\\figure')

    #remove result figure
    for filename in listdir(fig_dir):
            pdf = os.path.join(fig_dir, filename)
            remove(pdf)

    #download data from investing.com and put into database folder
    # stock = stock_manager()
    # stock.list_all()
    # scraper = csv_scraper(stock.url_dict)
   
    csv_list      = [csv for csv in listdir(database_dir)\
                    if isfile(join(database_dir, csv))]
    
    for stock_data in csv_list:
        fig, axis   = plt.subplots(3, sharex = True)
        df          = read_file(stock_data)
        name        = stock_data[:4]
        
        #y-data (price, price index)
        close       = df['Price'].to_numpy()[::-1] #inverse numpy array
        price_index = get_price_indexOf(close)
        
        #analysis
        M        = MACD(df['Price'])
        R        = RSI(df['Price'], 14)
        S200     = SMA(close,      200)
        S50      = SMA(close,       50)
        E5       = EMA(close,        5)
        S15      = SMA(close,       15)
        LGR      = linear_regression(price_index, 30)

        temp_buy      = (E5.ema > S15.sma) & (LGR.m > 0)
        temp_sell     = (E5.ema < S15.sma)

        #Transaction
        T           = transact(temp_buy, temp_sell, df['Price'])
        fund        = T.calc_NetProfit()

        b_index, s_index = T.get_BuySellIndex()

        #plot
        sub0 = 0
        sub1 = 1
        sub2 = 2

        plot_MA(axis      ,\
                sub0      ,\
                close     ,\
                E5.ema    ,\
                S15.sma   )
        
        plot_transact(axis    ,\
                      sub0    ,\
                      close   ,\
                      b_index ,\
                      s_index )

        plot_price_index(axis        ,\
                         sub2        ,\
                         price_index )

        plot_LGR(axis           ,\
                 sub2           ,\
                 b_index        ,\
                 LGR.m[b_index] ,\
                 LGR.c[b_index] ,\
                 30      )
        
        plot_fund(axis      ,\
                  sub1      ,\
                  s_index   ,\
                  fund      )
        
        # setup_plot(axis    ,\
                   # close   ,\
                   # M.macd  ,\
                   # M.signal,\
                   # M.hist  ,\
                   # S50.sma ,\
                   # S30.sma ,\
                   # buy     ,\
                   # sell    ,\
                   # s_index ,\
                   # fund    ,\
                   # R.rsi   )
                   
        save(name,fig) 
    
if __name__ == "__main__":
    main()
    
	
	