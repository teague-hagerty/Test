# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 10:42:38 2020

@author: Teague.Hagerty
"""

# import modules
import mysql.connector
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Normalize_name_script import normalize_name as normalize
import pandas as pd

driver = webdriver.Chrome("C:/Users/Teague.Hagerty/OneDrive - Issuer Direct Corporation/Desktop/Selenium/chromedriver.exe")
driver.get("https://www.sec.gov/cgi-bin/browse-edgar?CIK=320193&owner=exclude")
info = driver.find_element_by_class_name('companyName').text


latest_ciks = {}
tickers = ['AAPL', 'FB', 'F']
wrong_ticker = []

count = 0
for ticker in tickers:
    count += 1
    print(count)

    # format the url
    url1 = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK={'
    url2 = '}&owner=exclude&action=getcompany&Find=Search'
    url3 = url1 + ticker + url2
    driver.get(url3)

    #check that element can be found, get name and cik if ticker is found on sec website
    if len(driver.find_elements_by_class_name('companyName')) != 0:
        info = driver.find_element_by_class_name('companyName').text
            # extract the cik and company name, strip both
        cik_name = info.split('CIK#:')[0]
        cik_name = cik_name.strip()
        cik_num = info.split('(see')[0].split('CIK#:')[1]
        cik = cik_num.strip()
        cik = int(cik)
    
        # add it to the set
        match = {cik_name:cik}
        latest_ciks.update(match)

    #append to wrong ticker list if it cant
    else:
        wrong_ticker.append(ticker)
        pass

    # wait 10 seconds
    sleep(10)
 
#normalize all company names
normname_cik = {normalize(k): v for k, v in latest_ciks.items()}

#convert names and ciks to df
cik_df = pd.DataFrame.from_dict(normname_cik, orient = 'index')

#list of company names as they show in db --- could be pulled in from mysql here
company_name = ['Facebook, Inc.', 'Ford Motor Company','Apple Inc.']

#create df of companys from db
df = pd.DataFrame(index=company_name, columns = ['normal_name'])

#add column of normalized names
normalized_name = []
for i in company_name:
    normalized_name.append(normalize(i))
df['normal_name'] = normalized_name

#merge the two df based on matching normalized names
merge = pd.merge(df,cik_df, left_on=df['normal_name'], right_on=cik_df.index, right_index=True)

# turn merged df in to a list of original names and ciks= numbers
name_cik = [merge.index, merge[0]]





