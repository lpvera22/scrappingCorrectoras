from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
import multiprocessing
from functools import partial
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ThreadPool

OUT_DIR = 'out/'


def run_parallel_selenium_processes(datalist, selenium_func):
    pool = Pool()

    # max number of parallel process
    ITERATION_COUNT = cpu_count() - 1

    count_per_iteration = len(datalist) / float(ITERATION_COUNT)

    for i in range(0, ITERATION_COUNT):
        list_start = int(count_per_iteration * i)
        list_end = int(count_per_iteration * (i + 1))
        pool.apply_async(selenium_func, [datalist[list_start:list_end]])


def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out


def createProcess(func, l, i):
    # print('Process', i, 'created...')

    return multiprocessing.Process(target=func, args=l)


def getUrlCleans(search, lista):
    getUrlbyCEP(lista, search, 1)


def teste(x):
    print(len(x))


def getUrlCleansMultiprocessing(search, lista, number):
    list_div = chunkIt(lista, number)

    # list of process
    pro = []
    for i in range(number):
        aux = createProcess(getUrlbyCEP, (list_div[i], search, i), i)
        pro.append(aux)
    for p in range(len(pro)):
        pro[p].start()
        print('process', p, 'started')
    for p in range(len(pro)):
        pro[p].join()
    # for p in range(int(len(pro) / 2)):
    #     print('process', p, 'started')
    #     pro[p].start()
    # for p in range(int(len(pro) / 2)):
    #     pro[p].join()
    #
    # for p in range(int(len(pro) / 2), len(pro)):
    #     pro[p].start()
    # for p in range(int(len(pro) / 2), len(pro)):
    #     pro[p].join()


def getUrlbyCEP(cep, search, i):
    # print(cep, search)
    f = open(OUT_DIR + str(i) + '.csv', 'w')
    f.write('url,cep')
    f.write('\n')
    options = Options()
    # options.headless = True
    driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver", options=options)
    wait = ui.WebDriverWait(driver, 10)
    driver.get('https://www.bing.com/account/general?ru=https%3a%2f%2fwww.bing.com%2f&FORM=O2HV65#location')
    cont = 0

    for c in cep:

        cont += 1

        if cont > 20:
            driver.quit()
            driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver", options=options)
            cont = 0

        driver.get('https://www.bing.com/account/general?ru=https%3a%2f%2fwww.bing.com%2f&FORM=O2HV65#location')

        if len(str(c)) <= 7:
            c = str(0) + str(c)

        try:
            cepInput = driver.find_element_by_id('geoname')
            cepInput.clear()
            cepInput.send_keys(c)

            cepInput.send_keys(Keys.ENTER)
            sleep(0.5)

            try:

                sleep(0.5)
                driver.find_element_by_id('geoname')

                continue
            except:
                for s in search:
                    sleep(0.5)
                    searchInput = driver.find_element_by_id('sb_form_q')
                    searchInput.clear()
                    searchInput.send_keys(s)
                    driver.find_element_by_id('sb_form_q').send_keys(Keys.ENTER)
                    sleep(0.5)
                    url_cleans = []

                    for i in range(2):
                        sleep(0.5)
                        url_cleans = getLinks(driver, url_cleans)

                        for u in url_cleans:
                            # print(u,c)
                            f.write(str(u) + ',' + str(c))
                            f.write('\n')
                        sleep(0.5)
                        secondPageLink = driver.find_element_by_xpath('//*[@title="Próxima página"]')
                        secondPageLink.click()
                    driver.find_element_by_class_name('b_logoArea').click()
                driver.get(
                    'https://www.bing.com/account/general?ru=https%3a%2f%2fwww.bing.com%2f&FORM=O2HV65#location')
        except Exception as e:
            continue

    f.close()
    driver.quit()


def getLinks(d, url):
    liElements = d.find_elements_by_class_name('b_algo')
    liElementsAds = d.find_elements_by_xpath('//*[@className="b_ad"]/ul/li')
    for i in liElements:
        link = i.find_element_by_xpath('./h2/a').get_attribute('href')
        url.append(link)
    for i in liElementsAds:
        link = i.find_element_by_xpath('./div/h2/a').get_attribute('href')
        url.append(link)

    return url
