from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

OUT_DIR = '../../out/'


def getUrlCleansMultiprocessing(search):
    pass


def getUrlbyCEP(cep, search, i):
    # f = open(OUT_DIR + str(i) + '.csv', 'w')
    # f.write('url,cep')
    # f.write('\n')
    options = Options()
    # options.headless = True
    driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver", options=options)
    driver.get('https://www.bing.com/account/general?ru=https%3a%2f%2fwww.bing.com%2f&FORM=O2HV65#location')
    for c in cep:

        if len(str(c)) <= 7:
            c = str(0) + str(c)
        print(c)
        cepInput = driver.find_element_by_id('geoname')
        cepInput.clear()
        cepInput.send_keys(c)
        sleep(0.5)
        cepInput.send_keys(Keys.ENTER)


        try:
            driver.find_element_by_id('geoname')
            continue
        except:
            searchInput = driver.find_element_by_id('sb_form_q')
            searchInput.clear()
            searchInput.send_keys(search)
            driver.find_element_by_id('sb_form_q').send_keys(Keys.ENTER)
            sleep(0.5)
            url_cleans = []

            for i in range(1):
                url_cleans = getLinks(driver, url_cleans)
                driver.find_element_by_xpath('//*[@title="Próxima página"]').click()
        driver.get('https://www.bing.com/account/general?ru=https%3a%2f%2fwww.bing.com%2f&FORM=O2HV65#location')


def getLinks(d, url):
    liElements = d.find_elements_by_class_name('b_algo')
    liElementsAds = d.find_elements_by_class_name('b_ad')
    for i in liElements:
        link = i.find_element_by_xpath('./h2/a').get_attribute('href')
        url.append(link)
    for i in liElementsAds:
        link = i.find_element_by_xpath('./ul/li/div/h2/a').get_attribute('href')
        url.append(link)

    return url


if __name__ == '__main__':
    cep = pd.read_csv('../../data/ceps.csv')
    ceplist = cep['cep'].to_list()

    getUrlbyCEP(ceplist, 'sulamerica', '')
