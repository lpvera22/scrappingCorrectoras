import json
import os
import requests
from google.cloud import storage
import glob
import pandas as pd
import sys
# print(sys.path)

PATH_CREDENTIALS=os.path.abspath('scripts/credentials.json')

# print(PATH_CREDENTIALS)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PATH_CREDENTIALS
client = storage.Client()
bucket = client.get_bucket('fileimageapibucket')
# df = pd.read_csv('scripts/out/urlLogosCrop.csv')

# df['url'] = df['url'].apply(lambda x: x[x[8:].find('/') + 8:].replace('/', ''))
# url = df['url'].to_list()
# urlFont = dict.fromkeys(url, None)

path = '/media/laura/dados/Projects/Work/searchKeyword/scripts/out/img'


def upload_local_directory_to_gcs(local_path, gcs_path):
    assert os.path.isdir(local_path)
    for local_file in glob.glob(local_path + '/**'):
        if not os.path.isfile(local_file):
            upload_local_directory_to_gcs(local_file, gcs_path + "/" + os.path.basename(local_file))
        else:
            remote_path = os.path.join(gcs_path, local_file[1 + len(local_path):])
            blob = bucket.blob(remote_path)
            blob.upload_from_filename(local_file)



    
def whatFontApi(bucket, blob):
    urlJson = getUrl(bucket, blob)
    # urlJson = 'https://storage.googleapis.com/fileimageapibucket/json/configAPi.json'
    url = 'https://www.whatfontis.com/api/'
    params = {'file': urlJson, 'limit': 2}
    # print(params)
    try:
        x = requests.get(url, params=params)
        
        if x.status_code != 200:
            raise Exception(x.content)
        j = json.loads(x.text)
        # return j['FONT']['INFO']['TITLE']
        return j
    except:
        return -1


def getPublicUrlImg(bucket, file):
    # print(file)
    gcs_url = 'https://storage.googleapis.com/%(bucket)s/%(file)s' % {'bucket': bucket.name, 'file': file}
    return gcs_url


def downloadJsonFile():
    blob = bucket.get_blob('json/configApi.json')
    fileName = blob.name.split('/')[-1]
    blob.download_to_filename(fileName)


def modifyJsonAllUpload(newFile):
    with open('scripts/src/configAPi.json', 'w') as outfile:
        json.dump(newFile, outfile)
    blob = bucket.blob('json/calApiFont.json')
    with open('scripts/src/configAPi.json', 'rb') as f:
        blob.upload_from_file(f)


def modifyJsonFileUpload(newUrl):
    with open('scripts/src/configAPi.json') as f:
        data = json.load(f)
    data['FONT']['INFO']['urlimage'] = newUrl
    with open('scripts/src/configAPi.json', 'w') as f:
        json.dump(data, f)
    blob = bucket.blob('json/configApi.json')
    with open('scripts/src/configAPi.json', 'rb') as f:
        blob.upload_from_file(f)


def getUrl(bucket, blob):
    url = 'https://storage.googleapis.com/{}/{}'
    # blob = bucket.blob('json/configApi.json')
    url = url.format(bucket.name, blob.name)
    return url


def resetConfigApiJson():
    urlDefault = {
        "FONT": {
            "API_KEY": "c39b4f3d6d15f83a2f3f3df1f771aae530e32beef025e8de749fe945cf05a890",
            "P": "1",
            "F": "0",
            "INFO": {
                "urlimage": "https://www.whatfontis.com/api/img/A.png"
            }
        }
    }

    with open('scripts/src/configAPi.json', 'w') as outfile:
        json.dump(urlDefault, outfile)
    blob = bucket.blob('json/configAPi.json')
    with open('scripts/src/configAPi.json', 'rb') as f:
        blob.upload_from_file(f)

def downloadJsonfile():
    blob=bucket.get_blob('json/configApi.json')
    fileName=blob.name.split('/')[-1]
    blob.download_to_filename(fileName)
def getFontsByUrlImg():
    df = pd.read_csv('scripts/out/imgUrls.csv',sep=';')
    print(df)
    df=df.dropna()
    df['domain'] = df['url'].apply(lambda x: x[x[8:].find('/') + 8:].replace('/', ''))
    downloadJsonfile()
    df['font']=df['imgSrc'].apply(getFont)
    print('final',df)
    df.to_csv('scripts/out/urlsFontImg.csv',sep=';',index=False)
def getAllFonts():
    df = pd.read_csv('scripts/out/urlLogosCrop.csv')

    df['url'] = df['url'].apply(lambda x: x[x[8:].find('/') + 8:].replace('/', ''))
    url = df['url'].to_list()
    urlFont = dict.fromkeys(url, None)
    upload_local_directory_to_gcs(path, 'img')
    downloadJsonfile()
    
    for f in url:
        files = bucket.list_blobs(prefix='img/'+f)
        fileList = [file.name for file in files if '.' in file.name]
        for file in fileList:
            if 'crop.png' in file:
                # print(file)
                newUrl = getPublicUrlImg(bucket, file)
                modifyJsonFileUpload(newUrl)
                
                    
                font = whatFontApi(bucket, bucket.blob('json/configApi.json'))
                
                if font !=-1:
                    if isinstance(font, list):
                        urlFont[f] = font[0]['title']
                        
                    else:

                        modifyJsonAllUpload(font)
                        allFont = whatFontApi(bucket, bucket.blob('json/calApiFont.json'))
                        if allFont!=-1:
                            
                            urlFont[f] = allFont[0]['title']
                            
                        else:
                            
                            urlFont[f] = None
                    resetConfigApiJson()
                else:
                    urlFont[f] = None
    with open('scripts/out/urlFont.json', 'w') as json_file:
        json.dump(urlFont, json_file)

def getFont(imgurl):
    modifyJsonFileUpload(imgurl)
    font = whatFontApi(bucket, bucket.blob('json/configApi.json'))
    if font !=-1:
        if isinstance(font, list):
            return font[0]['title']
            
        else:

            modifyJsonAllUpload(font)
            allFont = whatFontApi(bucket, bucket.blob('json/calApiFont.json'))
            if allFont!=-1:
                
                return allFont[0]['title']
                
            else:
                
                return None
        resetConfigApiJson()
    else:
        return None