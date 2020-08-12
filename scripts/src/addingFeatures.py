import pandas as pd
import sys
sys.path.append('/media/laura/dados/Projects/Work/searchKeyword')
from scripts.src.sslInfo import checkSSL
from bs4 import BeautifulSoup
import requests
from scripts.src.malwareCheck import checkAll
import json
from scripts.src.getFontImg import getPublicUrlImg
import os
from google.cloud import storage

from datetime import datetime
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/media/laura/dados/Projects/Work/searchKeyword/scripts/credentials.json'

client = storage.Client()
bucket = client.get_bucket('fileimageapibucket')


def addSSL(df):
    df['SSL'] = df['url'].apply(checkSSL)
    return df


def getTitle(url):
    # url='http://'+url
    r = requests.get(url)
    try:
        soup = BeautifulSoup(r.content, "html")

        title = soup.title.string

        return title
    except:
        return None


def getDescription(url):
    url='http://'+url
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html")
    meta = soup.find_all('meta')
    # print(meta)
    for tag in meta:

        if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['description']:
            # print(tag.attrs['content'])
            return tag.attrs['content']
        else:
            return None


def getKeywords(url):
    # url='http://'+url
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
    df = pd.read_csv('scripts/out/urlCleaned.csv')
   
    df = addSSL(df)
    
    df=df[df['SSL']==True]
    
    df = addMeta(df)
    
    df = checkAll(df)
    
    # df['date']=datetime.now()
    
    df.to_csv('scripts/out/urlFeatures.csv', index=False)


def getDfFromJson(file, columns):
    with open(file) as content:
        dict_content = json.load(content)

    df = pd.DataFrame.from_dict(dict_content, orient='index')
    df.reset_index(level=0, inplace=True)
    df.columns = columns
    return df


def addingColorsAndFontInfo():
    frames = []
    df = pd.read_csv('scripts/out/urlFeatures.csv')
    print(df)
    # for file in [('scripts/out/urlColors.json', ['url', 'color']), ('scripts/out/urlFont.json', ['url', 'font'])]:
    #     aux = getDfFromJson(file[0], file[1])
    #     frames.append(aux)
    # a = pd.merge(frames[0], frames[1], on='url')
    
    # a = pd.merge(a[['url','color','font']], df,on='url')
    
    # a['imgUrl'] = a['url'].apply(lambda x: getPublicUrlImg(bucket, x))
    # a['date']=datetime.now()
    # a.to_csv('scripts/out/urlFinal.csv', index=False)



    
    
   
   
    