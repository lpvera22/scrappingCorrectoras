from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
import os
import pandas as pd
import numpy as np
from datetime import date
import csv
from selenium.webdriver.firefox.options import Options
import multiprocessing as mp
from multiprocessing.dummy import Pool as ThreadPool
import functools
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
from time import *
import multiprocessing
from memory_profiler import profile
import sys
import logging
from pyvirtualdisplay import Display
# print(sys.path)
filec = pd.read_csv('scripts/data/CEP-dados-2018-UTF8/ceps.csv')
urlsNot=pd.read_csv('scripts/data/excludeUrls.csv')
filec = filec[filec.index >= 73/2714]
# filec = filec.head()
filecep = filec['cep'].tolist()
# filecep=[28950000]
# os.system('rm /root/projects/scrappingCorrectoras/scripts/out/*')

threadLocal = threading.local()


def get_driver():
    driver = getattr(threadLocal, 'driver', None)
    if driver is None:
        options = Options()
        options.headless = True

        driver = webdriver.Firefox(options=options)

        setattr(threadLocal, 'driver', driver)
    return driver


def getLinks(driver,urls):
    
    liElements = driver.find_elements_by_class_name('b_algo')
    liElementsAds = driver.find_elements_by_class_name('b_ad')
    # print('liElements and ads---->',liElements,liElementsAds)
    for i in liElements:
        try:
            link = i.find_element_by_xpath('./h2/a').get_attribute('href')
        except Exception as e: 
            print("error on links",e)
        # print('link---------->',link)
        urls.append(link)
        # print(url_cleans)

    for i in liElementsAds:

        # link = i.find_element_by_xpath('./ul/li/div/div[1]/div/div/cite/a').text
        link = i.find_element_by_xpath('.//*[contains(text(), "http")]').text
        # print('link---------->',link)
        urls.append(link)
        # print(url_cleans)

    return urls


# @profile
def getUrlbyCEP(cep, search, i):
    # print('CEP PROCESS----->',i)
    f = open('scripts/out/' + str(i) + '.csv', 'w')
    f.write('url,cep')
    f.write('\n')
    
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)

    # driver = get_driver()

    driver.get(
        'https://www.bing.com/account/general?ru=https%3a%2f%2fwww.bing.com%2f%3fFORM%3dZ9FD1&FORM=O2HV65#location')
    
    for c in cep:
        driver.get(
        'https://www.bing.com/account/general?ru=https%3a%2f%2fwww.bing.com%2f%3fFORM%3dZ9FD1&FORM=O2HV65#location')
        title = driver.title
        # print(title)
        sleep(2)
        # print('starting with CEP----->',c)

        cepInput = driver.find_element_by_id('geoname')
        # print(cepInput)

        cepInput.clear()
        cepInput.send_keys(c)

        sleep(2)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(2)
        saveBtn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sv_btn"))
        )
        saveBtn.click()
        sleep(5)

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "geoname")))
            driver.find_element_by_id('geoname')
            continue




        except:
            print('CEP FOUND=======>',c)
            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sb_form_q")))
            searchInput = driver.find_element_by_id('sb_form_q')
            searchInput.clear()
            for s in search:
                print('***********************SEARCH KEYWORD-****************************',s)
                searchInput.send_keys(s)

                driver.find_element_by_id('sb_form_q').send_keys(Keys.ENTER)
                # print(driver.title)
                sleep(2)

                url_cleans = [] 
                
                
                
                
                try:
                    for l in range(3):
                        sleep(2)
                        url_cleans = getLinks(driver,url_cleans)
                        more=driver.find_element_by_xpath('//*[@title="Próxima página"]')

                        if more:
                            more.click()
                    
                            sleep(2)
                        else:
                            break
                except:
                    url_cleans = getLinks(driver,url_cleans)

                    
                
                    
                if len(url_cleans)>0:
                    
                    
                    
                    for u in url_cleans:
                                    
                        issave=True
                        for z in urlsNot['url'].to_list():
                            # print(z)
                            if u.find(z)!=-1:
                                # print(u)
                                issave=False
                                
                        
                        if issave:
                            
                            print('URL-->',u,c)
                            f.write(str(u) + ',' + str(c))
                            f.write('\n')
                else:
                    print('NO URLSSS----->',driver.getCurrentUrl())
                driver.get('https://www.bing.com/')
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sb_form_q")))
                searchInput = driver.find_element_by_id('sb_form_q')
                searchInput.clear()
                
    

        
    f.close()
    # driver.quit()
    


def getUrlCleans(search):
    start = strptime(asctime())

    f = open('out/' + str(date.today()) + '.csv', 'w')
    f.write('url,cep')
    f.write('\n')

    url_cleans = []
    cont = 0

    f_partial = functools.partial(getUrlbyCEP, search=search, f=f)
    ThreadPool(3).map(f_partial, filecep)

    f.close()
    end = strptime(asctime())
    print(end[4] - start[4])


def createProcess(func, l):
    return multiprocessing.Process(target=func, args=l)


def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


# @profile
def testFunction(l):
    sleep(5)

def getUrlCleansNoMult(search,num):
    with Display():
        getUrlbyCEP(filecep,search,0)

def getUrlCleansMultiprocessing(search,num):
    
    
    f_partial = functools.partial(getUrlbyCEP, search=search,cep=filecep)
    pro = []
    list_div = chunkIt(filecep, num)

    for i in range(num):
        aux = createProcess(getUrlbyCEP, (list_div[i], search, i))

        pro.append(aux)

    for p in range(num):
        pro[p].start()
        
        
    for p in range(num):
        pro[p].join()

    
# if __name__ == '__main__':
#     print(urlsNot)
    