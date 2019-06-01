# Standard library imports
from os import getcwd, listdir, remove
from os.path import join, isfile
import logging as log

# Third party imports
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

# Local application imports
from environment.env_setting import ENVIRONMENT, Host 

class stock_manager():
    def __init__(self):
        self.url_dict = \
        {'econpile' : 'https://www.investing.com/equities/econpile-holdings-bhd-historical-data',\
         'gamuda  ' : 'https://www.investing.com/equities/gamuda-bhd-historical-data'           }   
        log.info('Initialize Stock Library')
        
    def list_all(self):
        index = 1
        for stock in self.url_dict.keys():
            print ('Stock {0} : {1}.csv'.format(index, stock))
            index+=1
    

class csv_scraper():
    
    #directories
    current_dir       = getcwd()
    database_dir      = join(current_dir, '..', 'Database')
    gecko_path        = join(current_dir, '..', 'tools\gecko\gecko.exe')
    
    #firefox configs
    save_config       = 'browser.download.folderList'
    show_dwload_start = 'browser.download.manager.showWhenStarting'
    save_without_ask  = 'browser.helperApps.neverAsk.saveToDisk'
    download_dir      = 'browser.download.dir'  
    
    #variables
    custom_save       = 2
    csv_format        = 'text/csv' #MIME format
    
    def __init__(self, url_dict):
    
        self.url_dict    = url_dict
        self.profile  = 0
        self.browser  = 0
        
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
            company_http  = 'uia64930:Pass:D@cias3basic.conti.de' #Conti proxy
            company_port  = '8080'
            proxy_http    = 'network.proxy.http'    
            proxy_port    = 'network.proxy.http_port' 
            self.profile.set_preference(proxy_http       , company_http)
            self.profile.set_preference(proxy_port       , company_port)
        
        self.browser = webdriver.Firefox(self.profile, executable_path = self.gecko_path)
        
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
        
    def update_all_csv(self):
        
        download_xp = "//a[@title='Download Data']"
        startDate   = "06/01/2013"
        endDate     = "06/01/2019"
        
        for url in self.url_dict.values():
            self.browser.get(url)
            self.browser.find_element_by_id("widgetFieldDateRange").click()
            
            Date_txt = self.browser.find_element_by_id("startDate")
            Date_txt.clear()
            Date_txt.send_keys(startDate)
            
            Date_txt = self.browser.find_element_by_id("endDate")
            Date_txt.clear()
            Date_txt.send_keys(endDate)
            
            self.browser.find_element_by_id("applyBtn").click()
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, "curr_table")))
            self.browser.find_element_by_xpath(download_xp).click()
            
    def delete_all_csv(self):
    
        all_csv = [csv for csv in listdir(self.database_dir)\
                   if isfile(join(self.database_dir, csv)) ]
                   
        for csv in all_csv:
            remove(join(self.database_dir, csv))
        
        
        
if __name__ == "__main__":
    stock = stock_manager()
    stock.list_all()
    scraper = csv_scraper(stock.url_dict)
    #search_engine = data_processor()
    