# Standard library imports
import os

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
	
if __name__ == "__main__":
	df = read_file('Econpile_data.csv')
	Econpile_close = (df['Close'].to_numpy())
	timeperiod = 14
	rsi_value,rsi_buy,rsi_sell = RSI_analysis(Econpile_close,timeperiod)
	x_normal = np.arange(0, len(Econpile_close)-timeperiod)
	y_normal = Econpile_close[timeperiod:]
	plt.plot(x_normal, y_normal, 'g-')
	plt.plot(x_normal[rsi_sell], y_normal[rsi_sell],'r.')
	plt.plot(x_normal[rsi_buy], y_normal[rsi_buy],'b.')
	
	# plt.plot(x_normal, rsi_value, 'g-')
	# plt.plot(x_normal[rsi_sell], rsi_value[rsi_sell],'r.')
	# plt.plot(x_normal[rsi_buy], rsi_value[rsi_buy],'b.')
	print(rsi_buy[:150])
	plt.show()
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


	