# Standard library imports
import os
import logging as log

# Third party imports
import talib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import ExcelWriter
from pandas import ExcelFile
from talib import MA_Type

# Local application imports
from tools.reader import read_file
from tools.functionality import np_shift
from tools.scraper import csv_scraper, stock_manager

class context():
    def __init__(self):
        self.MA200 = 200
        self.MA100 = 100
        self.MA50  = 50

def init_logger(log_level):

    log.basicConfig(level    = log_level    , \
                    filename = 'logfile.log', \
                    filemode = 'w'          , \
                    format   = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

	

def RSI__IsOverbought(rsi_value, upper_limit):
    '''
    parameter: rsi_value = value from talib.RSI
    return	 : range of days where overbought happens. (True = 'Overbought')
    '''
    dummy_val = 50
    return np_shift((rsi_value>=upper_limit),1,0)& \
          (np_shift(rsi_value,1,dummy_val)>rsi_value)
		  
def RSI__IsOversold(rsi_value, lower_limit):
    '''
    parameter: rsi_value = value from talib.RSI
    return	 : range of days where oversold happens. (True = 'Oversold')
    '''
    dummy_val = 50
    return np_shift((rsi_value<=lower_limit),1,0)& \
           (np_shift(rsi_value,1,dummy_val)<rsi_value)

def RSI_analysis(close_data, timeperiod, upper_limit = 70, lower_limit = 30):
    '''
    parameter: close_data = closing price array (type: np.ndarray.float64)
    return	 : rsi_buy_signal  = range of days to 'Buy'. True = 'Buy'
               rsi_sell_signal = range of days to 'Sell'. True ='Sell'	
    '''
    dummy_value 	= 50
    rsi_value		= talib.RSI(close_data, timeperiod).astype(np.float32)
    rsi_value 		= rsi_value[~np.isnan(rsi_value)] #only select non-nan RSI value			  
    rsi_buy_signal  = RSI__IsOversold(rsi_value, lower_limit)
    rsi_sell_signal	= RSI__IsOverbought(rsi_value,upper_limit)
    return (rsi_value,rsi_buy_signal,rsi_sell_signal)
	
def SMA_analysis(close_data, period):
    '''
    parameter: close_data = closing price array (type: np.ndarray.float64)
    return	 : 1. signal
                  - within period  = False(Invalid)
                  - greater period = return True(above SMA) and False(below SMA)
               2. SMA
                  - moving average result
    '''
    data_len 		= len(close_data)
    SMA				= np.zeros(data_len)
    signal 			= np.zeros(data_len, dtype = bool)

    if data_len > period:
        SMA  			= talib.SMA(close_data, period).astype(np.float32)
        signal[period:] = close_data[period:] > SMA[period:]
        log.info('SMA: Complete')
        return (signal, SMA)
    else:
        log.error('SMA: Data length < 200 ')
        return (signal, SMA)

class MACD():

    '''
    parameter: class init
	           df_close        = closing price                    [df  : required]
               fastperiod      = fast EMA period   , < slowperiod [int : optional]
			   slowperiod      = slow EMA period   , > fastperiod [int : optional]
			   signalperiod    = signal EMA period , < fastperiod [int : optional]                  	  	
    '''
	
    def __init__(self, df_close , \
                fastperiod  = 12, \
                slowperiod  = 26, \
                signalperiod= 9   ):
        
        self.log            = log.getLogger('{:<15}'.format('macd'))
        self.close_data     = df_close.to_numpy()[::-1]
        self.fastperiod		= fastperiod
        self.slowperiod		= slowperiod
        self.signalperiod	= signalperiod

        self.macd, self.signal, self.hist = self.analyse(df_close)
        
        
        
    def analyse(self, close):
        '''
        parameter: close  = closing price (type: dataframe)         
        return   : macd   = macd          (type: np.ndarray.float64)							  
                   signal = signal        (type: np.ndarray.float64)
			       hist	  = macd - signal (type: np.ndarray.float64)
        '''
        self.log.info('MACD	   :Start Analysis               \n\
                          Parameter:                         \n\
                          fastperiod   = {self.fastperiod}   \n\
                          slowperiod   = {self.slowperiod}   \n\
                          signalperiod = {self.signalperiod} \n'.format(self=self))
        
        close_data		                  = close.to_numpy()
        self.macd, self.signal, self.hist = talib.MACD(
                                            close_data[::-1],\
                                            self.fastperiod ,\
                                            self.slowperiod ,\
                                            self.signalperiod)
        return (self.macd, self.signal, self.hist)
        
    def plot(self, axis):
	
        axis[0].set_title('Stock'              )
        axis[0].set(xlabel = 'Days'            )
        axis[0].set(ylabel = 'Price'           )
        axis[0].plot(self.close_data ,     'b-')
        axis[1].set_title('Macd ({0},{1},{2})'.format(self.fastperiod,\
                                                      self.slowperiod,\
                                                      self.signalperiod))
        axis[1].set(xlabel = 'Days'            )
        axis[1].set(ylabel = 'Index'           )
        axis[1].plot(self.macd       ,     'r-')
        axis[1].plot(self.signal     ,     'g-')
        axis[1].bar(range(0,   len(self.hist)),\
                    height = self.hist        ,\
                    color  = 'green' )
        plt.show()
        self.log.info('plot successful')        

    def buy_on_up_momentum(self, mode = 'simulation'):
    
        hist_len = len(self.hist)
        base_len = 0.002
        thres    = 0
        
        if mode == 'simulation':
            result   = np.zeros(hist_len).astype(bool)
            
            for i in range(2, hist_len):
                gradient  = (self.hist[i]-self.hist[i-2])/base_len
                result[i] = gradient > thres
             
            return result
        elif mode == 'actual':
            gradient  = (self.hist[i]-self.hist[i-2])/base_len
            return gradient > thres
        else:
            self.log.exception('No handle for mode : {0}'.format(mode))
            raise Exception('Only allow <simulation> or <actual> mode')
        
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
if __name__ == "__main__":
	
    # init_logger(log_level = log.INFO)
    
    # stock = stock_manager()
    # stock.list_all()
    # scraper = csv_scraper(stock.url_dict)
    
    from os import getcwd, listdir
    from os.path import join, isfile
    database_dir  = os.path.join(os.getcwd(), 'Database')
    csv_list      = [csv for csv in listdir(database_dir)\
                    if isfile(join(database_dir, csv))]
    econpile_data = csv_list[0]
    fig, axis = plt.subplots(2, sharex = True)
    df = read_file(econpile_data)

    Macd      = MACD(df['Price'])
    result    = Macd.buy_on_up_momentum('simulation')
    close     = df['Price'].to_numpy()[::-1]
    buy_pts_X = np.arange(len(close))[result]
    buy_pts_Y = close[result]
    axis[0].plot(buy_pts_X, buy_pts_Y, 'k.')
    Macd.plot(axis)
	# signal, SMA200 = SMA200_analysis(Econpile_close)
	
	# x_normal = np.arange(0, len(Econpile_close))
	# y_normal = Econpile_close
	# f, axarr = plt.subplots(2, sharex = True)
	# axarr[0].plot(x_normal, y_normal)
	# axarr[0].plot(x_normal, SMA200, 'r-')
	# axarr[1].plot(x_normal, signal, 'g-')
	
	# axarr[0].set(ylabel = 'Econpile_data')
	# axarr[1].set(ylabel = 'Buy Signal'	 )
	# plt.show()
	# OPEN LATER 1
	# timeperiod = 14
	# rsi_value,rsi_buy,rsi_sell = RSI_analysis(Econpile_close,timeperiod)
	# x_normal = np.arange(0, len(Econpile_close)-timeperiod)
	# y_normal = Econpile_close[timeperiod:]
	# plt.plot(x_normal, y_normal, 'g-')
	# plt.plot(x_normal[rsi_sell], y_normal[rsi_sell],'r.')
	# plt.plot(x_normal[rsi_buy], y_normal[rsi_buy],'b.')
	# print(rsi_buy[:150])
	# plt.show()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	# plt.plot(x_normal, rsi_value, 'g-')
	# plt.plot(x_normal[rsi_sell], rsi_value[rsi_sell],'r.')
	# plt.plot(x_normal[rsi_buy], rsi_value[rsi_buy],'b.')
	#plot_signal('Econpile',Econpile_close,rsi_buy,'r-')
	#print(Econpile_close)
	# print(type(close_price))
	
	#npA = numpy.random.random(50)
	#print(npA)
	#print(type(npA))
	#output1 = talib.EMA(close_price, timeperiod = 50)
	
	#print(output1)
	#print(len(output1))
	# analysis["macd"], analysis["macd_Signal"], analysis["macd_Hist"] = talib.MACD(
	# close_price,
	# fastperiod = 12,
	# slowperiod = 26,
	# signalperiod = 9
	# )
	
	
	# analysis['rsi'] = talib.RSI(close_price, timeperiod = 16).astype(np.float32)
	#Non_nan_value = ~np.isnan(analysis['rsi'])
	#analysis['rsi'] = analysis['rsi'][Non_nan_value].astype(int)
	#overbought and decreasing
	# rsi_overbought_level = 80
	# analysis['rsi_overbought'] = np.where(
	# (analysis['rsi'] >= 80 ) & 
	# (np_shift(analysis['rsi'],1)>analysis['rsi']),1,0)
	
	# print(analysis['rsi'][0:50])
	# print(analysis['rsi'][0:50]>=80)
	# print((np_shift(analysis['rsi'],1)>analysis['rsi'])[0:50])
	# print(type(analysis['rsi']))
	# print((np_shift(analysis['rsi'],1))[23])
	# print(analysis['rsi'][23])
	
	#print(analysis['rsi_overbought'][0:100])
	# x_normal = np.arange(0, len(close_price))
	# y_normal = close_price
	# x_16 = np.arange(0, len(close_price))
	# y_16 = analysis["rsi"]
	# f, axarr = plt.subplots(2, sharex = True)
	# axarr[0].plot(x_normal, y_normal)
	# axarr[1].plot(x_16, y_16, 'r-')
	# axarr[1].plot(x_16, analysis["rsi"], 'g-')
	# plt.show()


	