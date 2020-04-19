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
from tools.functionality import save, np_shift, plot_MA, plot_fund, plot_transact
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
        fig, axis = plt.subplots(2, sharex = True)
        df        = read_file(stock_data)
        name      = stock_data[:4]
        close     = df['Price'].to_numpy()[::-1]
        
        M        = MACD(df['Price'])
        R        = RSI(df['Price'], 14)
        S200     = SMA(df['Price'],200)
        S50      = SMA(df['Price'], 50)
        S30      = SMA(df['Price'], 30)
        S15      = SMA(df['Price'], 15)
        
        temp_buy      = (S30.sma > S50.sma)
        temp_sell     = (S30.sma < S50.sma) 
                    
        T           = transact(temp_buy, temp_sell, df['Price'])
        
        buy         = T.transact_pts==1
        sell        = T.transact_pts==2

        fund        = T.calc_NetProfit()
        s_index     = np.zeros(len(fund)).astype(int)

        #Get index of selling points
        s_index[1:] = np.where(sell)[0] 
        
        #plot
        sub0 = 0
        sub1 = 1
        sub2 = 2

        plot_MA(axis      ,\
                sub0      ,\
                close     ,\
                S30.sma   ,\
                S50.sma   )
        
        plot_transact(axis  ,\
                      sub0  ,\
                      close ,\
                      buy   ,\
                      sell  )

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
    
	
	