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
    import shutil
    
    database_dir  = os.path.join(os.getcwd(), 'Database')
    fig_dir       = os.path.join(os.getcwd(), 'result\\figure')
    csv_list      = [csv for csv in listdir(database_dir)\
                    if isfile(join(database_dir, csv))]
    
    for filename in listdir(fig_dir):
            pdf = os.path.join(fig_dir, filename)
            remove(pdf)
    
    for stock_data in csv_list:
        fig, axis = plt.subplots(2, sharex = True)
        df        = read_file(stock_data)
        name      = stock_data[:4]
        
        #macd
        M         = MACD(df['Price'])
        result    = M.test_buy_momentum(True)
        close     = df['Price'].to_numpy()[::-1]

        # MACD testing
        # buy_pts_X = np.arange(len(close))[result]
        # buy_pts_Y = close[result]
        # axis[0].plot(buy_pts_X, buy_pts_Y, 'k.')
        # normal_x  = np.arange(len(close))
        
        #sma
        Sma    = SMA(df['Price'], 50)
        result = Sma.test_buy_abv_sma()
        y      = close[result]
        x      = np.arange(len(close))[result]
        
        setup_plot(axis    ,\
                   close   ,\
                   M.macd  ,\
                   M.signal,\
                   M.hist  ,\
                   Sma.sma ,\
                   x       ,\
                   y       )
                   
        save(name,fig)
                   
        
    
if __name__ == "__main__":
    main()
    
	
	