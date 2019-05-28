# Standard library imports
import os
import logging as log

# Third party imports
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from selenium import webdriver

# Local application imports
from environment.env_setting import ENVIRONMENT, Host 

class stock_manager():
    def __init__(self):
        self.url_dict = \
        {'econpile' : 'https://www.investing.com/equities/econpile-holdings-bhd-historical-data',\
         'gamuda  ' : 'https://www.investing.com/equities/gamuda-bhd-historical-data'           }   
        
    def list_all(self):
        index = 1
        for stock in self.url_dict.keys():
            print ('Stock {0} : {1}.csv'.format(index, stock))
            index+=1
    

class csv_scraper():
    
    #directories
    current_dir       = os.getcwd()
    database_dir      = os.path.join(current_dir, '..', 'Database')
    gecko_path        = os.path.join(current_dir, '..', 'tools\gecko\gecko.exe')
    
    #firefox configs
    save_config       = 'browser.download.folderList'
    show_dwload_start = 'browser.download.manager.showWhenStarting'
    save_without_ask  = 'browser.helperApps.neverAsk.saveToDisk'
    download_dir      = 'browser.download.dir'  
    
    #variables
    custom_save       = 2
    csv_format        = 'text/csv' #MIME format
    
    def __init__(self, url_dict):
        self.url_dict = url_dict 
        self.profile  = webdriver.FirefoxProfile()
        self.profile.set_preference(self.save_config      , self.custom_save )
        self.profile.set_preference(self.download_dir     , self.database_dir)
        self.profile.set_preference(self.save_without_ask , self.csv_format  )
        self.profile.set_preference(self.show_dwload_start, False            )
        
        if ENVIRONMENT == Host.COMPANY:
            company_http  = 'uia64930:Pass:D@cias3basic.conti.de' #Conti proxy
            company_port  = '8080'
            proxy_http    = 'network.proxy.http'    
            proxy_port    = 'network.proxy.http_port' 
            self.profile.set_preference(proxy_http       , company_http)
            self.profile.set_preference(proxy_port       , company_port)
        
        self.browser = webdriver.Firefox(self.profile, executable_path = self.gecko_path)
        self.update_all_csv()
        
    def update_all_csv(self):
        
        download_xp = "//a[@title='Download Data']"
        
        for url in self.url_dict.values():
            self.browser.get(url)
            #WebElement result = self.browser.find_element_by_xpath(download_xp)
            #print(result.getText())
        
if __name__ == "__main__":
    stock = stock_manager()
    stock.list_all()
    scraper = csv_scraper(stock.url_dict)
    
    #search_engine = data_processor()
    