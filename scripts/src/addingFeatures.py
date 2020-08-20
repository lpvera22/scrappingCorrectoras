import pandas as pd
import sys
#sys.path.append('/media/laura/dados/Projects/Work/searchKeyword')
from src.sslInfo import checkSSL
from bs4 import BeautifulSoup
import requests
from src.malwareCheck import checkAll
import json
from src.getFontImg import getPublicUrlImg
import os
from google.cloud import storage
import re
from datetime import datetime

PATH_CREDENTIALS=os.path.abspath('scripts/credentials.json')
# print(PATH_CREDENTIALS)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PATH_CREDENTIALS

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
    # df = pd.read_csv('scripts/out/urlCleaned.csv')
    df = pd.read_csv('scripts/out/urlLogosCrop.csv')
    
    df=df[['url']]
    df = addSSL(df)
    
    df=df[df['SSL']==True]
    # print(df)
    
    df = addMeta(df)
    # print(df)
    
    df = checkAll(df)
    # print(df)
    
    df['date']=datetime.now()
    # print(df)
    
    df.to_csv('scripts/out/urlFeatures.csv', index=False)


def getDfFromJson(file, columns):
    with open(file) as content:
        dict_content = json.load(content)

    df = pd.DataFrame.from_dict(dict_content, orient='index')
    df.reset_index(level=0, inplace=True)
    df.columns = columns
    return df
def cleaningUrl(url):
    m=re.search('https?://([A-Za-z_0-9.-]+).*', url)
    return str(m.group(1))
    

def addingColorsAndFontInfo():
    frames = []
    
    
    dfFeat = pd.read_csv('scripts/out/urlFeatures.csv')
    dfFeat['domain']=dfFeat['url'].apply(lambda x: x[x[8:].find('/') + 8:].replace('/', ''))
    
    
    fileColor='scripts/out/urlColors.json'
    dfColor=pd.read_json(fileColor,orient='index')
    dfColor.reset_index(inplace=True)
    dfColor=dfColor.rename(columns={"index": "url"})
    
    frames.append(dfColor)
    
    
    fileFont='scripts/out/urlFont.json'
    dfFont=pd.read_json(fileFont,orient='index')
    dfFont.reset_index(inplace=True)
    dfFont=dfFont.rename(columns={"index": "url",0:"font"})
    frames.append(dfFont)
    
    
    
    
    a = pd.merge(frames[0], frames[1], on='url')
    
    a=a.rename(columns={"url": "domain"})
    
    a = pd.merge(a,dfFeat,on='domain')
    
    
    
    # # a['imgUrl'] = a['domain'].apply(lambda x: getPublicUrlImg(bucket, x))
    
    
    a.to_csv('scripts/out/urlFinal.csv', index=False)



    
    
   
   
    
