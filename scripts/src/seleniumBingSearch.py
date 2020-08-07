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

file = pd.read_csv('data/CEP-dados-2018-UTF8/ceps.csv', delimiter='\t', header=None, dtype='str')
file = file[file.index >= 732646]
filecep = file[0].tolist()

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

    for i in liElements:
        link = i.find_element_by_xpath('./h2/a').get_attribute('href')

        url_cleans.append(link)

    for i in liElementsAds:

        # link = i.find_element_by_xpath('./ul/li/div/div[1]/div/div/cite/a').text
        link = i.find_element_by_xpath('.//*[contains(text(), "http")]').text
        url_cleans.append(link)

    return url_cleans


# @profile
def getUrlbyCEP(cep, search, i):
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
        driver.get(
            'https://www.bing.com/account/general?ru=https%3a%2f%2fwww.bing.com%2f%3fFORM%3dZ9FD1&FORM=O2HV65#location')
        for c in cep:

            cepInput = driver.find_element_by_id('geoname')
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
                pass
            searchInput = driver.find_element_by_id('sb_form_q')
            searchInput.clear()
            searchInput.send_keys(s)

            driver.find_element_by_id('sb_form_q').send_keys(Keys.ENTER)
            sleep(0.5)

            url_cleans = []

            for i in range(2):

                url_cleans = getLinks(driver, url_cleans)
                sleep(1.5)
                driver.find_element_by_xpath('//*[@title="Próxima página"]').click()
                url_cleans = getLinks(driver, url_cleans)
                for u in url_cleans:
                    f.write(u + ',' + c)
                    f.write('\n')

            driver.get(
                'https://www.bing.com/account/general?ru=https%3a%2f%2fwww.bing.com%2f%3fFORM%3dZ9FD1&FORM=O2HV65'
                '#location')

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


def getUrlCleansMultiprocessing(search):
    f_partial = functools.partial(getUrlbyCEP, search=search)
    pro = []
    list_div = chunkIt(filecep, 8)

    for i in range(8):
        aux = createProcess(getUrlbyCEP, (list_div[i], search, i))

        pro.append(aux)

    for p in range(4):
        pro[p].start()
    for p in range(4):
        pro[p].join()

    for p in range(4, 8):
        pro[p].start()

    for p in range(4, 8):
        pro[p].join()
