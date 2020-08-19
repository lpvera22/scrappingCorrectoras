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
import logging

file = pd.read_csv('../data/CEP-dados-2018-UTF8/ceps.csv')

#file = file[file.index >= 732664]
filecep = file['cep'].tolist()



threadLocal = threading.local()


def get_driver():
    driver = getattr(threadLocal, 'driver', None)
    if driver is None:
        options = Options()
        options.headless = True

        driver = webdriver.Firefox(options=options)

        setattr(threadLocal, 'driver', driver)
    return driver


def getLinks(driver, url_cleans):
    liElements = driver.find_elements_by_class_name('b_algo')
    liElementsAds = driver.find_elements_by_class_name('b_ad')
    print('liElements and ads---->',liElements,liElementsAds)
    for i in liElements:
        link = i.find_element_by_xpath('./h2/a').get_attribute('href')
        print('link---------->',link)
        url_cleans.append(link)
        print(url_cleans)

    for i in liElementsAds:

        # link = i.find_element_by_xpath('./ul/li/div/div[1]/div/div/cite/a').text
        link = i.find_element_by_xpath('.//*[contains(text(), "http")]').text
        print('link---------->',link)
        url_cleans.append(link)
        print(url_cleans)

    return url_cleans


# @profile
def getUrlbyCEP(cep, search, i):
    #print(cep)
    f = open('out/' + str(i) + '.csv', 'w')
    f.write('url,cep')
    f.write('\n')
    
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)

    # driver = get_driver()

    driver.get(
        'https://www.bing.com/account/general?ru=https%3a%2f%2fwww.bing.com%2f%3fFORM%3dZ9FD1&FORM=O2HV65#location')
    
    for s in search:
        try:
            # print(s)
            driver.get(
                'https://www.bing.com/account/general?ru=https%3a%2f%2fwww.bing.com%2f%3fFORM%3dZ9FD1&FORM=O2HV65#location')
            for c in cep:
                # print(c)

                cepInput = driver.find_element_by_id('geoname')
                # print(cepInput)

                cepInput.clear()
                cepInput.send_keys(c)

                sleep(0.5)
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

                saveBtn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "sv_btn"))
                )
                saveBtn.click()
                sleep(0.5)

                try:
                    sleep(0.5)
                    driver.find_element_by_id('geoname')
                    continue




                except:
                    print('continue to search...')
                    searchInput = driver.find_element_by_id('sb_form_q')
                    searchInput.clear()
                    searchInput.send_keys(s)

                    driver.find_element_by_id('sb_form_q').send_keys(Keys.ENTER)
                    sleep(0.5)

                    url_cleans = []

                    for j in range(2):

                        url_cleans = getLinks(driver, url_cleans)
                        
                        sleep(1.5)
                        try:
                            driver.find_element_by_xpath('//*[@title="Próxima página"]').click()
                            url_cleans = getLinks(driver, url_cleans)
                            print('urlCleans',url_cleans)
                            print('found next page....')
                        except:
                            pass

                        print('not found next page....=================>>>>>>>>>>>>',url_cleans)
                        for u in url_cleans:
                            print(u)
                            print(u,c)
                            # res.append((u,c))
                            f.write(str(u) + ',' + str(c))
                            f.write('\n')

                    driver.get(
                        'https://www.bing.com/account/general?ru=https%3a%2f%2fwww.bing.com%2f%3fFORM%3dZ9FD1&FORM=O2HV65#location')
        except:
            print('somethong went wrong whith this',c,'cep')
            
            continue

        
        f.close()
        driver.quit()


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

    
