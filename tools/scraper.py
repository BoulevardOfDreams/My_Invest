# Standard library imports
import os
import logging as log

# Third party imports
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from selenium import webdriver

# Local application imports

class data_processor():
    
    #directories
    current_dir       = os.getcwd()
    database_dir      = os.path.join(current_dir, '..', 'Database')
    
    #firefox configs
    save_config       = 'browser.download.folderList'
    show_dwload_start = 'browser.download.manager.showWhenStarting'
    save_without_ask  = 'browser.helperApps.neverAsk.saveToDisk'
    download_dir      = 'browser.download.dir'
    custom_save       = 2
    csv_format        = 'text/csv' #MIME format  
    
    
    def __init__(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference(self.save_config      , self.custom_save )
        profile.set_preference(self.download_dir     , self.database_dir)
        profile.set_preference(self.save_without_ask , self.csv_format  )
        profile.set_preference(self.show_dwload_start, False       )
        
if __name__ == "__main__":
    search_engine = data_processor()
    