import os
from google.cloud import vision
from google.cloud import storage
import pandas as pd
from scripts.src.getFontImg import getPublicUrlImg
import json


PATH_CREDENTIALS=os.path.abspath('scripts/credentials.json')
# print(PATH_CREDENTIALS)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PATH_CREDENTIALS
client = vision.ImageAnnotatorClient()

clientStorage = storage.Client()
bucket = clientStorage.get_bucket('fileimageapibucket')
# df = pd.read_csv('scripts/out/urlLogosCrop.csv')
# df['url'] = df['url'].apply(lambda x: x[x[8:].find('/') + 8:].replace('/', ''))
# url = df['url'].to_list()
# urlColors = dict.fromkeys(url, None)


def clamp(x):

    return max(0, min(int(x), 255))


def toHex(r, g, b, ):

    return '#{0:02x}{1:02x}{2:02x}'.format(clamp(r), clamp(g), clamp(b))


def detect_properties_uri(uri):
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.image_properties(image=image)
    props = response.image_properties_annotation

    colors = []
    for color in props.dominant_colors.colors:


        hex = toHex(color.color.red, color.color.green, color.color.blue)

        colors.append((color.pixel_fraction, hex))

    if response.error.message:
        print('error on google image',uri)
        return -1
        # raise Exception(
        #     '{}\nFor more info on error messages, check: '
        #     'https://cloud.google.com/apis/design/errors'.format(
        #         response.error.message))

    return colors


def getAllColors():
    df = pd.read_csv('scripts/out/urlLogosCrop.csv')
    df['url'] = df['url'].apply(lambda x: x[x[8:].find('/') + 8:].replace('/', ''))
    url = df['url'].to_list()
    urlColors = dict.fromkeys(url, None)
    for f in url:
        
        files = bucket.list_blobs(prefix='img/'+f)
        
        fileList = [file.name for file in files if '.' in file.name]
        
        
        for file in fileList:
            
            if 'crop.png' in file:
                newUrl = getPublicUrlImg(bucket, file)
                colors = detect_properties_uri(newUrl)
                urlColors[f] = colors
    with open('scripts/out/urlColors.json', 'w') as json_file:
        json.dump(urlColors, json_file)
