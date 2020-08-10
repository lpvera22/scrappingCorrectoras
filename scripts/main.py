import sys
sys.path.append('/media/laura/dados/Projects/Work/searchKeyword')
from scripts.src.seleniumBingSearch import getUrlCleansMultiprocessing
from scripts.src.cleaningUrls import cleaningUrls
from scripts.src.addingFeatures import addingFeatures, addingColorsAndFontInfo
from scripts.src.googleDetectLogo import findLogoOnUrl
from scripts.src.getFontImg import getAllFonts
from scripts.src.googleImgProp import getAllColors
from scripts.src.ScrapingToDb import getScrapingtoDb
import pandas as pd
import time

cep = pd.read_csv('data/CEP-dados-2018-UTF8/ceps.csv')
ceplist = cep['cep'].to_list()


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


def main(search):
    getUrlCleansMultiprocessing(search)
    # cleaningUrls(8)
    # findLogoOnUrl()
    # getAllFonts()
    # getAllColors()
    # addingFeatures()

    # addingColorsAndFontInfo()
    
    


if __name__ == '__main__':
    start_time = time.time()
    keywords = ['SulAmerica', 'sulamerica']
    main(keywords)
    print('---%s seconds---' % (convert(time.time() - start_time)))
