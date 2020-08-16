import io
import os
import pandas as pd
from google.cloud import vision
import re
import difflib
from PIL import Image, ImageDraw
import pathlib

PATH_CREDENTIALS=os.path.abspath('scripts/credentials.json')
# print(PATH_CREDENTIALS)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PATH_CREDENTIALS
client = vision.ImageAnnotatorClient()

# df = pd.read_csv('scripts/out/urlCleaned.csv')
rootImg = 'scripts/out/img/'
rootData = 'scripts/out/'


def draw_hint(file_name, image_folder, vects):
    image_file = os.path.join(image_folder, file_name)
    im = Image.open(image_file)

    try:
        draw = ImageDraw.Draw(im)
        draw.polygon([
            vects[0].x, vects[0].y,
            vects[1].x, vects[1].y,
            vects[2].x, vects[2].y,
            vects[3].x, vects[3].y], None, 'red')
        im.save(image_folder + '/output-hint.png', 'PNG')

    except:
        im.save(image_folder + '/output-hint.png', 'PNG')


def similar(seq1, seq2):
    return difflib.SequenceMatcher(a=seq1.lower(), b=seq2.lower()).ratio() > 0.9


def verticesLogoUrl(file_name, image_folder, keywordLogo):
    image_path = os.path.join(image_folder, file_name)

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.logo_detection(image=image)
    logos = response.logo_annotations

    if not logos:
        return '', -1
    else:

        for logo in logos:

            exist = logo.description.find(keywordLogo)

            if exist != -1:

                return logo.bounding_poly.vertices

            else:
                return '', -1


def getLogo(image_folder, file_name, keywordLogo):
    image_path = os.path.join(file_name, image_folder)
    try:
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.logo_detection(image=image)
        logos = response.logo_annotations

        if not logos:
            return -1
        else:

            for logo in logos:

                exist = logo.description.find(keywordLogo)

                if exist != -1:

                    return logo
                else:
                    return -1
    except:
        return -1


def crop_to_hint(file_name, image_folder, vects):
    image_file = os.path.join(image_folder, file_name)
    im = Image.open(image_file)
    im2 = im.crop([vects[0].x, vects[0].y,
                   vects[2].x - 1, vects[2].y - 1])

    im2.save(image_folder + '/crop.png', 'PNG')


def findLogoOnUrl():
    df = pd.read_csv('scripts/out/urlCleaned.csv')
    urlLogo = {}
    for url in df['url'].to_list():
        # print(url)
        m = re.search('https?://([A-Za-z_0-9.-]+).*', url)
        pathImg = rootImg + str(m.group(1))

        for subdir, dirs, files in os.walk(pathImg):
            for file in range(len(files)):

                logo = getLogo(files[file], subdir, 'SulAmérica')

                if logo != -1:
                    crop_to_hint(files[file], subdir, logo.bounding_poly.vertices)

                    draw_hint(files[file], subdir, logo.bounding_poly.vertices)
                    urlLogo[url] = os.path.join(subdir, 'crop.png')

                    break

    dfUrl = pd.DataFrame.from_dict(urlLogo, orient='index', columns=['logoUrl'])
    dfUrl['url'] = dfUrl.index
    dfUrl.reset_index(drop=True, inplace=True)
    dfUrl.to_csv(rootData + 'urlLogosCrop.csv', index=False)
