# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 23:28:58 2017

@author: morales
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotVisibleException
import time

class session:
    def __init__(self, path_j):
        self.path_j = path_j
        self.driver =  0       
        self.get_driver()
         
    def get_driver(self):
        self.driver = webdriver.Chrome(self.path_j)
        self.driver.set_window_size(width=1920,height=1080)
        self.driver.get("https://www.etoro.com/en/login")
        self.print_title()
    
    def print_title(self):
        print self.driver.title
        
    def close_driver(self):
        self.driver.quit()
        print "Driver was closed"
        
class set_workspace:
    def __init__(self, login, password, driver):
        self.login = login
        self.password = password
        self.driver = driver
        
    def do_login(self):
        try:
            time.sleep(2)
            search_box = self.driver.find_element_by_name('username')
            search_box.clear()
            search_box.send_keys(self.login)
            search_box = self.driver.find_element_by_name('password')
            search_box.clear()
            search_box.send_keys(self.password)
            self.driver.find_element_by_class_name('w-login-action').click()

        except Exception:
            print "We are not in the login page"

    def close_popups(self):
        
        time.sleep(2)
        popups_names= ['inmplayer-popover-close-button','e-kyc-x']
        
        for name in popups_names:
            try:
                self.driver.find_element_by_class_name(name).click()
                print "Popup with name: ", name, " is now closed"
                time.sleep(2)
                
            except Exception:
                print "Popup with name: ", name, " was not found"


    def open_left_menu(self):
        try:  
            res = self.driver.find_element_by_class_name('e-toggle-icon')
            res.click()
            print "Left menu now opened"
        except Exception:
            print "Left menu is already opened"
            
    def type_portfolio(self, type_portfolio = 'virtual'):
        self.open_left_menu()
        time.sleep(0.2)
        self.driver.find_element_by_class_name("i-menu-link-mode-demo").click()
        time.sleep(0.2)

        el = self.driver.find_elements_by_class_name('drop-select-box-option')
        time.sleep(0.2)
        if type_portfolio == 'virtual':
        #Go to virtual portfolio
            el[1].click()
        else:
            el[0].click()
            
        try:
            self.driver.find_element_by_class_name('w-sm-footer-button').click()
            print type_portfolio, " portfolio is loaded"
        except Exception:
            print "We are already in the ", type_portfolio, " portfolio" 
    
    def choose_option(self, option): 
        self.open_left_menu()
        time.sleep(0.5)
        el = self.driver.find_elements_by_class_name("i-menu-link")
        time.sleep(0.5)
        
        el[option].click()

    
    def set_portfolio(self):

        for k in range(0,5):
            try:
                self.choose_option(1)            
                print  "Portfolio list is loaded"
                break
            except Exception:
                    print "Something happened :S" 
            
    def set_watchlist(self):
        
        for k in range(0,5):
            try:
                self.choose_option(0)            
                print  "Watchlist is loaded"
                break
            except Exception:
                    print "Something happened :S" 
                    
class open_transaction:
    
    def __init__(self, session):
        self.session = session
        self.driver = session.driver        
        
        self.stock_pos = 0
        self.money = 0.0
        
    def execute(self, stock_pos, money, position_type = 'buy'):
        
        #self.session.set_watchlist() #Make sure we are in the porfolio list
        self.stock_pos = stock_pos        
        time.sleep(1)
        Portfolio = self.driver.find_elements_by_class_name('list-avatar-ph')
        print Portfolio
        Portfolio[self.stock_pos].click()
        time.sleep(1)
        
        #Click trade stock
        Trade = self.driver.find_elements_by_class_name('button-standard')
        Trade[1].click()        
        
        time.sleep(1)
        if(position_type == 'sell'):
            order_type = self.driver.find_element_by_class_name('execution-head-button')
        elif(position_type == 'buy'):
            order_type = self.driver.find_element_by_class_name('execution-head')
        else:
            print 'Invalid order'
        
        order_type.click()
        
        #Set quantity to trade
        input_vals = self.driver.find_element_by_class_name('stepper-value')
        input_vals.clear()
        input_vals.send_keys(str(money))
        
        time.sleep(0.5)

        #Execute the trade (Two times required)
        self.driver.find_element_by_class_name('execution-button').click()
        time.sleep(0.5)
        self.driver.find_element_by_class_name('execution-button').click()
        
        
class close_transaction:
    
    def __init__(self, session):
        self.session = session
        self.driver = session.driver        
        
        self.stock_pos = 0
        
    def execute(self, stock_pos= 0):
        
        #Click the stock to close
        self.stock_pos = stock_pos        
        time.sleep(1)
        Portfolio = self.driver.find_elements_by_class_name('table-avatar-ph')
        print Portfolio
        Portfolio[self.stock_pos].click()
        time.sleep(1)
        
        #Click x in the stock
        self.driver.find_elements_by_class_name('e-btn')[2].click()        
        time.sleep(0.5)
        self.driver.find_element_by_class_name('w-sm-footer-button').click()
