from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import re
import os
import random
import pandas as pd
import csv
import os
# import unidecode
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import math
import logging
import sys
import chromedriver_binary
import threading
import requests
import json

allurls = ['"category":1,"type":1,','"category":4,"type":0,','"category":3,"type":0,','"category":10,"type":1,','"category":3,"type":1,','"category":1,"type":0,','"category":2,"type":0,','"category":5,"type":1,','"category":12,"type":0,','"category":6,"type":0,','"category":12,"type":1,','"category":9,"type":0,','"category":6,"type":1,','"category":7,"type":1,','"category":4,"type":1,','"category":2,"type":1,','"category":13,"type":1,','"category":14,"type":1,','"category":11,"type":1,','"category":5,"type":0,']
FailedFetchRequests = []
jsondata = ''
purls = []
alldata = []
maindata = []
options = webdriver.ChromeOptions()
options.add_argument('-private-window')
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList",2)
print('Opening browser...')
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.implicitly_wait(120)
#wfile=open('./data.csv','a+',newline='',encoding='utf-8')
#writer=csv.DictWriter(wfile, dialect='excel')
driver.get("Website URL")
time.sleep(2)
driver.find_element_by_css_selector('body > div > div > div > section > div.container.sub-nav-container.ng-scope > div > div.sub-menu-items > ul > li:nth-child(2)').click() #I used it to click a section to make webpage active
def myPeriodicFunction():

    # -- create session ---

    session = requests.session()

    headers = {
         #Headers here in JSON
    }

    # set headers for all requests
    session.headers.update(headers)
    cookies = {
         #Cookies here in JSON
               }
    
    data = """{
          "query": {
          "limit": 50,
          "offset": 50,
          "geo": {
          "polygon": [
          {
            "lat": 28.3833333,
            "lng": 36.5833333
          }
         ],
           "type": "polygon"
      },
      "where": {
      """+allurls[i]+"""
      "closed": 0
    }
  }
}"""

    url = "" #Request URL here

    # `json=` add `"Content-Type": "application/json;charset=utf-8"`

    page = session.post(url, json=json.loads(data), cookies=cookies, headers = headers)
    cruise_data = page.json()
    counts = cruise_data['data']['total_found']
    purls.append(counts)
    print(counts)
    


def productPage():

    # -- create session ---

    session = requests.session()

    headers = {
     #Headers here in JSON
    }

    # set headers for all requests
    session.headers.update(headers)
    cookies = {
        #Cookies here in JSON
               }
    # --- search ---

    data = """{
          "query": {
          "limit": 50,
          "offset": """+offset+""",
          "geo": {
          "polygon": [
          {
            "lat": 28.3833333,
            "lng": 36.5833333
          }
         ],
           "type": "polygon"
      },
      "where": {
      """+allurls[j]+"""
      "closed": 0
    }
  }
}"""


    url = "" #Request URL here

    # `json=` add `"Content-Type": "application/json;charset=utf-8"`

    page = session.post(url, json=json.loads(data), cookies=cookies, headers = headers)
    cruise_data = page.json()
    for m in cruise_data['data']['results']:    #Loop in JSON array
        Beds = m.get('bed_rooms','N/A') 
        userID = m.get('id','N/A')
        living =  m.get('living_rooms','N/A')

        alldata.append((Beds,userID,living))        #appending data in array
        

i =0
for i in range(len(allurls)):
     myPeriodicFunction()
     time.sleep(.2)
print(allurls)
print(purls)
time.sleep(2)
j=0
k=0
for j in range(len(allurls)):
    totalcalls =  math.ceil(purls[j]/50)
    print(totalcalls)
    while(k<=totalcalls):
      offset = str(k * 50)
      #print(offset)
      print(k)
      productPage()
      time.sleep(.2)
      k=k+1
    df = pd.DataFrame(alldata,columns =['BED ROOMS','ID','LIVING ROOMS'])
    # if file does not exist write header 
    if not os.path.isfile('DATA.xlsx'):
          df.to_excel('DATA.xlsx', index=False, encoding='utf-8-sig')
    else:# else it exists so append without writing the header
          writer = pd.ExcelWriter('DATA.xlsx', engine='openpyxl', mode='a+')
          df.to_excel(writer)
          writer.save()
    writer.close()

time.sleep(3)
driver.quit()
