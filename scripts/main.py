import sys
sys.path.append('/media/laura/dados/Projects/Work/searchKeyword')
from scripts.src.seleniumBingSearch import getUrlCleansMultiprocessing
from scripts.src.cleaningUrls import cleaningUrls
from scripts.src.addingFeatures import addingFeatures, addingColorsAndFontInfo
from scripts.src.googleDetectLogo import findLogoOnUrl
from scripts.src.getFontImg import getAllFonts
from scripts.src.googleImgProp import getAllColors
from scripts.src.ScrapingToDb import getScrapingtoDb
from scripts.src.getallImg import seleniumGetImg
import pandas as pd
import time
import re





def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


def main(search):
    getUrlCleansMultiprocessing(search,5)
    cleaningUrls(5)
    dfCleaned = pd.read_csv('scripts/out/urlCleaned.csv')
    f = open('scripts/out/imgUrls.csv', 'w')
    f.write('url,imgSrc')
    f.write('\n')
    for url in dfCleaned['url'].to_list():
        
        m = re.search('https?://([A-Za-z_0-9.-]+).*', url)
        seleniumGetImg(url, str(m.group(1)),f)
    
    findLogoOnUrl()
    getAllFonts()
    getAllColors()
    addingFeatures()
    addingColorsAndFontInfo()
    getScrapingtoDb()
    
    


if __name__ == '__main__':
    start_time = time.time()
    keywords = ['SulAmerica', 'sulamerica']
    main(keywords)
    print('---%s seconds---' % (convert(time.time() - start_time)))
