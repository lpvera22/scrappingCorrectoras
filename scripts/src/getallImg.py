import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import urllib
import time


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """

    try:
        parsed = urlparse(url)
        requests.get(url, verify=True)
        valid = bool(parsed.netloc) and bool(parsed.scheme)
    except:
        valid = False
    return valid


def get_all_images(url):
    """
    Returns all image URLs on a single `url`
    """
    driver.get(url)
    soup = bs(requests.get(url).content, "html.parser")
    urls = []

    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        if is_valid(img_url):
            urls.append(img_url)
        return urls


def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True,
                    unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))


def getAll(url, path):
    # get all images
    imgs = get_all_images(url)
    for img in imgs:
        # for each image, download it
        download(img, path)


def seleniumGetImg(url, path,f):
    print('inside....',url)
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    driver.get(url)
    time.sleep(2)
    # get the image source
    try:
        imgs = driver.find_elements_by_tag_name('img')
        for i in range(len(imgs)):


            src = imgs[i].get_attribute('src')
            alt = imgs[i].get_attribute('alt')
            try:
                r = requests.get(src)
            except ValueError:
                print('it is going to wait 30 min now.....GO TO GET A COFFEE!')
                time.sleep(30)
                r = requests.get(src)
            if is_valid(src):
                
                f.write(url + ';' + src)
                f.write('\n')
                if not os.path.isdir('scripts/out/img/' + path):
                    
                    os.makedirs('scripts/out/img/' + path)
                
                # print('existe')
                    
                with open('scripts/out/img/' + path + '/' + str(i) + '.png', 'wb') as outfile:
                    outfile.write(r.content)






    except ValueError:
        print('error on url---->',url)

    driver.close()


# if __name__ == '__main__':
#     df = pd.read_csv('../out/urlFeatures.csv')
#     for url in df['url'].to_list():
#         print(url)
#         m = re.search('https?://([A-Za-z_0-9.-]+).*', url)
#         seleniumGetImg(url, str(m.group(1)))
