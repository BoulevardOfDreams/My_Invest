# Standard library imports
import os
import logging as log

# Third party imports
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
from analysis.macd import MACD
from analysis.sma import SMA
from tools.functionality import setup_plot, save
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
        fig, axis = plt.subplots(2, sharex = True)
        df        = read_file(stock_data)
        name      = stock_data[:4]
        close     = df['Price'].to_numpy()[::-1]
        

        M           = MACD(df['Price'])
        Sma         = SMA(df['Price'], 50)
        
        temp_buy    = Sma.test_buy_abv_sma()    &\
                      M.test_buy_momentum(True)
                 
        temp_sell   = Sma.test_sell_below_sma() &\
                      M.test_sell_negative()
                      
        # temp_buy    = M.test_buy_momentum(True)
                 
        # temp_sell   = M.test_sell_negative()
                    
        T           = transact(temp_buy, temp_sell)
        
        buy         = T.transact_pts==1
        sell        = T.transact_pts==2
        
        
        setup_plot(axis    ,\
                   close   ,\
                   M.macd  ,\
                   M.signal,\
                   M.hist  ,\
                   Sma.sma ,\
                   buy     ,\
                   sell    )
                   
        save(name,fig)
                   
        
    
if __name__ == "__main__":
    main()
    
	
	