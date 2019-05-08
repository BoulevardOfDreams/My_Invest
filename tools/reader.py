# Standard library imports
import os

# Third party imports
import numpy
import talib
import pandas as pd


def read_file(file_name):

	"""
	Return excel data if file exist
	else
	print error captured
	"""
	
	current_dir = os.getcwd()
	csv_path = os.path.join(current_dir,'Database',file_name)
	
	try:
		data = pd.read_csv(csv_path, 
						   usecols = ['Date','Close','Volume'], 
						   parse_dates = ['Date'])
		
		return data.dropna()
		
	except FileNotFoundError:
		print("[FileNotFoundError]File Name Not found in {0}".format(csv_path))
		return None
		
	
if __name__ == "__main__":
	df = read_file('Econpile_data1.csv')
	print(df)
	