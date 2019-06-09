# Standard library imports
import os
import logging 

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
    csv_path    = os.path.join(current_dir,'Database',file_name)
    log         = logging.getLogger('{:<15}'.format('reader'))

    try:
        data = pd.read_csv(csv_path, 
                           usecols = ['Date','Price','Vol.'], 
                           parse_dates = ['Date'])
                           
        log.info('Read {0} success'.format(file_name))
        return data.dropna()
		
    except FileNotFoundError:
        log.error("[FileNotFoundError]File Name Not found in {0}".format(csv_path))
        return None
		
	
if __name__ == "__main__":

    #testing purpose
    from os import getcwd, listdir
    from os.path import join, isfile
    database_dir = os.path.join(os.getcwd(), '..', 'Database')
    csv_list     = [csv for csv in listdir(database_dir)\
                    if isfile(join(database_dir, csv))]
    
    for csv in csv_list:
        df = read_file(csv)
        print(df)
	