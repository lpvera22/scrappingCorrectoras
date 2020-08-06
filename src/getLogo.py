from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from os.path import basename
import requests


def getLogoSrc(url):

    soup = BeautifulSoup(urlopen(url).read())
    links = []
    for x in soup.find_all(class_='logo'):
        print(x)

        try:
            if x.name == 'img':
                # links.append(url+'/'+x['src'])
                # print(x['src'])
                return url + '/' + x['src']
            elif x.name == 'a':
                children = x.findChildren("img", recursive=False)
                for c in children:
                    # links.append(url+'/'+c['src'])
                    return url + '/' + c['src']


        except:
            pass


def downloadAllLogo(df):
    pass


if __name__ == '__main__':
    # urlsFeatures = pd.read_csv('../out/urlFeatures.csv')
    # # urlsFeatures=urlsFeatures.head(10)
    # urlsFeatures['logo'] = urlsFeatures['url'].apply(getLogoSrc)
    # # print(urlsFeatures['logo'])
    # getLogoSrc('https://portal.sulamericaseguros.com.br')
    getLogoSrc('https://www.sulamericaauto.com.br')
