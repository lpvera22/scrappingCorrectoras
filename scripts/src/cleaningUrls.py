import pandas as pd
from scripts.src.urlInfo import isUp
from datetime import date
import logging

# reading urls.csv file
def concatUrls(n):
    frames = []

    # n is the number of process
    for i in range(n):
        aux = pd.read_csv('scripts/out/' + str(i) + '.csv', header=0, index_col=False)
        frames.append(aux)

    allUrls = pd.concat(frames, ignore_index=True)

    return allUrls


def regexClean(url):
    if url.find('bing') == -1:
        return url[: url[8:].find('/') + 8]

    else:
        return url


def cleaningUrls(n):
    logging.info('cleaning urls')
    urls = concatUrls(8)
    urls['url'] = urls['url'].astype(str)
    urls['url'] = urls['url'].apply(regexClean)
    urls = urls.drop_duplicates(subset=['url'], keep='last')

    urls['on'] = urls['url'].apply(isUp)
    final = urls[urls['on'] == True]

    final['contador'] = date.today()
    final[['url', 'cep']].to_csv('scripts/out/urlCleaned.csv', index=False)
    logging.info('scripts/out/urlCleaned.csv file saved...')
