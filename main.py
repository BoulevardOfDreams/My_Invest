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
from tools.functionality import setup_plot, save, np_shift
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
    
    # stock = stock_manager()
    # stock.list_all()
    # scraper = csv_scraper(stock.url_dict)
    
    from os import getcwd, listdir, remove
    from os.path import join, isfile
    
    database_dir  = os.path.join(os.getcwd(), 'Database')
    fig_dir       = os.path.join(os.getcwd(), 'result\\figure')
    csv_list      = [csv for csv in listdir(database_dir)\
                    if isfile(join(database_dir, csv))]
    
    #remove fig
    for filename in listdir(fig_dir):
            pdf = os.path.join(fig_dir, filename)
            remove(pdf)
    
    for stock_data in csv_list:
        fig, axis = plt.subplots(3, sharex = True)
        df        = read_file(stock_data)
        name      = stock_data[:4]
        close     = df['Price'].to_numpy()[::-1]
        

        M        = MACD(df['Price'])
        S50      = SMA(df['Price'], 50)
        E30      = EMA(df['Price'], 30)
        E25      = EMA(df['Price'], 25)
        
                 
        temp          = np_shift(S50.sma, 1, 100)
        diff_50       = S50.sma - temp
        result_50     = np.ones(len(close)).astype(bool)

        for i in range(1):
            now       = np_shift(diff_50, i  , 100)
            later     = np_shift(diff_50, i+1, 100)
            result_50 &= ((now > later) & (now > 0))
        
        temp2         = np_shift(E30.ema, 1, 100)
        d_30_trend    = np.where(E30.ema < temp2, 1, 0).astype(bool)
        
        temp_buy      =  result_50 & (close < S50.sma)
        temp_sell     = (M.macd < 0) & d_30_trend
                    
        T           = transact(temp_buy, temp_sell, df['Price'])
        
        buy         = T.transact_pts==1
        sell        = T.transact_pts==2
        
        fund        = T.calc_NetProfit()
        s_index     = np.zeros(len(fund)).astype(int)
        s_index[1:] = np.where(sell)[0]
        
        
        setup_plot(axis    ,\
                   close   ,\
                   M.macd  ,\
                   M.signal,\
                   M.hist  ,\
                   S50.sma ,\
                   E30.ema  ,\
                   buy     ,\
                   sell    ,\
                   s_index ,\
                   fund     )
                   
        save(name,fig)
                   
        
    
if __name__ == "__main__":
    main()
    
	
	