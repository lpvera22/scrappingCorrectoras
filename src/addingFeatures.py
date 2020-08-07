import pandas as pd
from src.sslInfo import checkSSL
from bs4 import BeautifulSoup
import requests
from src.malwareCheck import checkAll


def addSSL(df):
    df['SSL'] = df['url'].apply(checkSSL)
    return df


def getTitle(url):
    r = requests.get(url)
    try:
        soup = BeautifulSoup(r.content, "html")

        title = soup.title.string

        return title
    except:
        return None


def getDescription(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html")
    meta = soup.find_all('meta')
    print(meta)
    for tag in meta:

        if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['description']:
            print(tag.attrs['content'])
            return tag.attrs['content']
        else:
            return None


def getKeywords(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    meta_list = soup.find_all("meta")
    entry = None
    for meta in meta_list:
        if 'name' in meta.attrs:
            name = meta.attrs['name']
            if name in ['keywords', 'Keywords']:
                entry = meta.attrs['content']

    return entry


def addMeta(df):
    df['title'] = df['url'].apply(getTitle)
    df['keywords'] = df['url'].apply(getKeywords)
    return df


def addingFeatures():
    df = pd.read_csv('out/urlCleaned.csv')
    df = addSSL(df)
    df = addMeta(df)
    df = checkAll(df)
    df.to_csv('out/urlFeatures.csv', index=False)
