# Standard library imports
from os import getcwd, listdir, remove
from os.path import join, isfile
from datetime import datetime
import logging as log

# Third party imports
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Local application imports
from environment.env_setting import ENVIRONMENT, Host

class stock_manager():
    def __init__(self):
        self.url_dict = \
        {'econpile' : 'https://www.investing.com/equities/econpile-holdings-bhd-historical-data' ,\
         'gamuda'   : 'https://www.investing.com/equities/gamuda-bhd-historical-data'            ,\
         'pie'      : 'https://www.investing.com/equities/pie-industrial-bhd-historical-data'    ,\
         'inari'    : 'https://www.investing.com/equities/inari-amertron-bhd-historical-data'    ,\
         'maybank'  : 'https://www.investing.com/equities/malayan-banking-bhd-historical-data'   ,\
         'hi-p'     : 'https://www.investing.com/equities/hi-p-international-ltd-historical-data',\
         'sunning'  : 'https://www.investing.com/equities/sunningdale-tech-ltd-historical-data'  ,\
         'genM'     : 'https://www.investing.com/equities/genting-malaysia-bhd-historical-data'  ,\
         'ST'       : 'https://www.investing.com/equities/singapore-technologies-engineering-historical-data'}
        
        self.log      = log.getLogger('{:<15}'.format('stock_manager'))
        self.log.info('Initialize Stock Library')
        
    def list_all(self):
        index = 1
        for stock in self.url_dict.keys():
            print ('Stock {0} : {1}.csv'.format(index, stock))
            index+=1
        self.log.info('List all stock')

class csv_scraper():
    
    #directories
    current_dir       = getcwd()
    database_dir      = join(current_dir, 'Database')
    gecko_path        = join(current_dir, 'tools\gecko\gecko.exe')
    
    #firefox configs
    save_config       = 'browser.download.folderList'
    show_dwload_start = 'browser.download.manager.showWhenStarting'
    save_without_ask  = 'browser.helperApps.neverAsk.saveToDisk'
    download_dir      = 'browser.download.dir'  
    
    #variables
    custom_save       = 2
    csv_format        = 'text/csv' #MIME format
    
    def __init__(self, url_dict):
    
        self.url_dict     = url_dict
        self.profile      = 0
        self.browser      = 0
        self.log          = log.getLogger('{:<15}'.format('scraper'))
        
        self.delete_all_csv()
        self.setup_firefox()
        self.login()
        self.update_all_csv()
        
        
    def setup_firefox(self):
        self.profile  = webdriver.FirefoxProfile()
        self.profile.set_preference(self.save_config      , self.custom_save )
        self.profile.set_preference(self.download_dir     , self.database_dir)
        self.profile.set_preference(self.save_without_ask , self.csv_format  )
        self.profile.set_preference(self.show_dwload_start, False            )
        
        if ENVIRONMENT == Host.COMPANY:
            username       = 'uia64930'
            password       = 'Outmyhouse95:D'  
            company_http   = 'cias3basic.conti.de' #Conti proxy
            company_port   = '8080'
            proxy_http     = 'network.proxy.http'    
            proxy_port     = 'network.proxy.http_port'
            socks_username = 'network.proxy.socks_username'
            socks_password = 'network.proxy.socks_password'
            self.profile.set_preference(proxy_http       , company_http)
            self.profile.set_preference(proxy_port       , company_port)
            self.profile.set_preference(socks_username   , username    )
            self.profile.set_preference(socks_password   , password    )
        
        try:
            self.browser = webdriver.Firefox(self.profile, executable_path = self.gecko_path)
            self.log.info('Webdriver init success')
        except WebDriverException:
            self.browser.close()
            self.log.error('Webdriver: Path Error',exec_info = True)
            
        
    def login(self):
     
        url            = "https://www.investing.com/"
        email	   	   = "emailautomation95@gmail.com"
        password	   = "Outmyhouse95"
        webSignIn      = "//a[@class='login bold']"
        popUpSignIn    = "//a[starts-with(@onclick, 'login')]"

        
        self.browser.get(url)
        self.browser.find_element_by_xpath(webSignIn).click()
        self.browser.find_element_by_id("loginFormUser_email").send_keys(email)
        self.browser.find_element_by_id("loginForm_password").send_keys(password)
        self.browser.find_element_by_xpath(popUpSignIn).click()
        self.log.info('Login using {0}'.format(email))
        
    def update_all_csv(self):
        
        download_xp  = "//a[@title='Download Data']"
        
        dt           = datetime.now()
        today        = dt.strftime("%m/%d/%Y")
        x3_year_ago  = datetime(year  = dt.year - 3, 
                                month = dt.month   , 
                                day   = dt.day  - 1).strftime("%m/%d/%Y")
        
        
        for url in self.url_dict.values():
            self.browser.get(url)
            self.browser.find_element_by_id("widgetFieldDateRange").click()
            
            self.browser.find_element_by_id("startDate").clear()
            self.browser.find_element_by_id("startDate").send_keys(x3_year_ago)
            
            self.browser.find_element_by_id("endDate").clear()
            self.browser.find_element_by_id("endDate").send_keys(today)
            
            self.browser.find_element_by_id("applyBtn").click()
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, "curr_table")))
            self.browser.find_element_by_xpath(download_xp).click()
        
        self.log.info('Updated all csv')
        
    def delete_all_csv(self):
    
        all_csv = [csv for csv in listdir(self.database_dir)\
                   if isfile(join(self.database_dir, csv)) ]
                   
        for csv in all_csv:
            remove(join(self.database_dir, csv))
        
        self.log.info('Deleted all csv')
        
if __name__ == "__main__":
    from analytic_lib import init_logger
    init_logger(log_level = log.INFO)
    stock = stock_manager()
    stock.list_all()
    scraper = csv_scraper(stock.url_dict)
    #search_engine = data_processor()
    